from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import OperationalError
from datetime import datetime
from typing import List, Optional, Union
import json

from ..database import get_db
from ..models import ChatMessage as ChatMessageModel, User as UserModel, Trip as TripModel, Booking as BookingModel
from ..schemas import ChatMessageCreate, ChatMessageResponse
from ..auth.middleware import verify_token
from ..websocket_manager import manager

router = APIRouter(prefix="/chat")

def _check_user_permission(db: Session, trip_id: int, user_id: int) -> bool:
    """检查用户是否有权限访问聊天室"""
    # 验证行程是否存在
    trip = db.query(TripModel).filter(TripModel.id == trip_id).first()
    if not trip:
        return False
    
    # 验证用户是否有权限（必须是行程的发布者或预订者）
    is_owner = int(getattr(trip, 'owner_id', 0)) == int(user_id)
    is_booker = db.query(BookingModel).filter(
        BookingModel.trip_id == trip_id,
        BookingModel.user_id == user_id
    ).first() is not None
    
    return is_owner or is_booker

# 创建聊天消息
@router.post("/messages/", response_model=ChatMessageResponse)
async def create_chat_message(
    message: ChatMessageCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(verify_token)
):
    try:
        # 验证行程是否存在
        trip = db.query(TripModel).filter(TripModel.id == message.trip_id).first()
        if not trip:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="行程不存在"
            )
        
        # 验证用户是否有权限发送消息（必须是行程的发布者或预订者）
        has_permission = _check_user_permission(db, int(getattr(message, 'trip_id', 0)), int(getattr(current_user, 'id', 0)))
        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="您没有权限在此行程中发送消息"
            )
        
        # 创建聊天消息
        db_message = ChatMessageModel(
            trip_id=int(getattr(message, 'trip_id', 0)),
            sender_id=int(getattr(current_user, 'id', 0)),
            content=str(getattr(message, 'content', '')),
            message_type=str(getattr(message, 'message_type', 'text'))
        )
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        
        # 返回响应
        response = ChatMessageResponse(
            id=int(getattr(db_message, 'id', 0)),
            trip_id=int(getattr(db_message, 'trip_id', 0)),
            sender_id=int(getattr(db_message, 'sender_id', 0)),
            content=str(getattr(db_message, 'content', '')),
            message_type=str(getattr(db_message, 'message_type', 'text')),
            timestamp=getattr(db_message, 'timestamp', datetime.utcnow()),
            sender_username=str(getattr(current_user, 'username', ''))
        )
        
        # 向聊天室广播消息
        room_id = f"trip_{getattr(message, 'trip_id', 0)}"
        await manager.broadcast_to_room(
            {
                "type": "message",
                "data": response.dict()
            },
            room_id
        )
        
        return response
    except OperationalError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="数据库连接失败，请稍后重试"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"发送消息失败: {str(e)}"
        )

# 获取聊天历史记录
@router.get("/messages/{trip_id}", response_model=List[ChatMessageResponse])
async def get_chat_history(
    trip_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(verify_token)
):
    try:
        # 验证行程是否存在
        trip = db.query(TripModel).filter(TripModel.id == trip_id).first()
        if not trip:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="行程不存在"
            )
        
        # 验证用户是否有权限查看聊天记录（必须是行程的发布者或预订者）
        has_permission = _check_user_permission(db, int(trip_id), int(getattr(current_user, 'id', 0)))
        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="您没有权限查看此行程的聊天记录"
            )
        
        # 获取聊天历史记录
        messages = db.query(ChatMessageModel).filter(
            ChatMessageModel.trip_id == trip_id
        ).join(UserModel).order_by(
            ChatMessageModel.timestamp.asc()
        ).offset(skip).limit(limit).all()
        
        # 转换为响应模型
        response = []
        for message in messages:
            response.append(ChatMessageResponse(
                id=int(getattr(message, 'id', 0)),
                trip_id=int(getattr(message, 'trip_id', 0)),
                sender_id=int(getattr(message, 'sender_id', 0)),
                content=str(getattr(message, 'content', '')),
                message_type=str(getattr(message, 'message_type', 'text')),
                timestamp=getattr(message, 'timestamp', datetime.utcnow()),
                sender_username=str(getattr(message.sender, 'username', '')) if message.sender else "未知用户"
            ))
        
        return response
    except OperationalError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="数据库连接失败，请稍后重试"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取聊天记录失败: {str(e)}"
        )

# WebSocket端点
@router.websocket("/ws/{trip_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    trip_id: int,
    db: Session = Depends(get_db)
):
    current_user = None
    try:
        # 验证行程是否存在
        trip = db.query(TripModel).filter(TripModel.id == trip_id).first()
        if not trip:
            await websocket.close(code=4004)
            return
        
        # 验证用户身份（通过查询参数传递token）
        token = websocket.query_params.get("token")
        if not token:
            await websocket.close(code=4001)
            return
        
        # 验证用户身份
        current_user = verify_token(token, db)
        if not current_user:
            await websocket.close(code=4002)
            return
        
        # 验证用户是否有权限加入聊天室（必须是行程的发布者或预订者）
        has_permission = _check_user_permission(db, int(trip_id), int(getattr(current_user, 'id', 0)))
        if not has_permission:
            await websocket.close(code=4003)
            return
        
        # 连接WebSocket
        await manager.connect(websocket, int(trip_id), int(getattr(current_user, 'id', 0)))
        
        # 发送欢迎消息
        await manager.send_personal_message(
            json.dumps({
                "type": "welcome",
                "data": {
                    "message": f"欢迎加入行程 {trip_id} 的聊天室",
                    "participants": manager.get_room_participants(f"trip_{trip_id}")
                }
            }, ensure_ascii=False),
            websocket
        )
        
        # 监听消息
        while True:
            data = await websocket.receive_text()
            # 解析消息
            try:
                message_data = json.loads(data)
                if message_data.get("type") == "message":
                    content = message_data.get("content", "")
                    if content:
                        # 创建聊天消息
                        db_message = ChatMessageModel(
                            trip_id=int(trip_id),
                            sender_id=int(getattr(current_user, 'id', 0)),
                            content=str(content),
                            message_type="text"
                        )
                        db.add(db_message)
                        db.commit()
                        db.refresh(db_message)
                        
                        # 返回响应
                        response = ChatMessageResponse(
                            id=int(getattr(db_message, 'id', 0)),
                            trip_id=int(getattr(db_message, 'trip_id', 0)),
                            sender_id=int(getattr(db_message, 'sender_id', 0)),
                            content=str(getattr(db_message, 'content', '')),
                            message_type=str(getattr(db_message, 'message_type', 'text')),
                            timestamp=getattr(db_message, 'timestamp', datetime.utcnow()),
                            sender_username=str(getattr(current_user, 'username', ''))
                        )
                        
                        # 向聊天室广播消息
                        room_id = f"trip_{trip_id}"
                        await manager.broadcast_to_room(
                            {
                                "type": "message",
                                "data": response.dict()
                            },
                            room_id,
                            websocket  # 排除发送者
                        )
            except json.JSONDecodeError:
                # 忽略无效的JSON消息
                pass
            except Exception as e:
                print(f"处理消息时出错: {e}")
                continue
                
    except WebSocketDisconnect:
        user_id = int(getattr(current_user, 'id', 0)) if current_user else 0
        manager.disconnect(websocket, user_id)
    except Exception as e:
        print(f"WebSocket连接错误: {e}")
        user_id = int(getattr(current_user, 'id', 0)) if current_user else 0
        manager.disconnect(websocket, user_id)
        await websocket.close(code=4000)