import json
import asyncio
from typing import Dict, List, Set, Optional
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        # 存储所有活跃的WebSocket连接
        self.active_connections: Dict[str, List[WebSocket]] = {}
        # 存储用户ID到连接的映射
        self.user_connections: Dict[int, List[WebSocket]] = {}
        # 存储聊天室连接
        self.chat_rooms: Dict[str, Set[WebSocket]] = {}
        # 存储用户到聊天室的映射
        self.user_chat_rooms: Dict[int, Set[str]] = {}

    async def connect(self, websocket: WebSocket, trip_id: int, user_id: int):
        """连接到WebSocket并加入聊天室"""
        await websocket.accept()
        
        # 将连接添加到活跃连接列表
        if user_id not in self.user_connections:
            self.user_connections[user_id] = []
        self.user_connections[user_id].append(websocket)
        
        # 创建聊天室标识符
        room_id = f"trip_{trip_id}"
        
        # 将连接添加到聊天室
        if room_id not in self.chat_rooms:
            self.chat_rooms[room_id] = set()
        self.chat_rooms[room_id].add(websocket)
        
        # 记录用户所在的聊天室
        if user_id not in self.user_chat_rooms:
            self.user_chat_rooms[user_id] = set()
        self.user_chat_rooms[user_id].add(room_id)
        
        print(f"用户 {user_id} 连接到聊天室 {room_id}")

    def disconnect(self, websocket: WebSocket, user_id: int):
        """断开WebSocket连接"""
        # 从用户连接中移除
        if user_id in self.user_connections:
            if websocket in self.user_connections[user_id]:
                self.user_connections[user_id].remove(websocket)
            if not self.user_connections[user_id]:
                del self.user_connections[user_id]
        
        # 从所有聊天室中移除连接
        for room_id, connections in self.chat_rooms.items():
            if websocket in connections:
                connections.remove(websocket)
                if not connections:
                    del self.chat_rooms[room_id]
        
        # 从用户聊天室映射中移除
        if user_id in self.user_chat_rooms:
            rooms_to_remove = []
            for room_id in self.user_chat_rooms[user_id]:
                if room_id in self.chat_rooms:
                    if websocket in self.chat_rooms[room_id]:
                        self.chat_rooms[room_id].remove(websocket)
                        if not self.chat_rooms[room_id]:
                            rooms_to_remove.append(room_id)
            
            # 清理空的聊天室
            for room_id in rooms_to_remove:
                if room_id in self.chat_rooms:
                    del self.chat_rooms[room_id]
                self.user_chat_rooms[user_id].discard(room_id)
            
            if not self.user_chat_rooms[user_id]:
                del self.user_chat_rooms[user_id]
        
        print(f"用户 {user_id} 断开连接")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """发送个人消息"""
        try:
            await websocket.send_text(message)
        except WebSocketDisconnect:
            pass

    async def broadcast_to_room(self, message: dict, room_id: str, sender_websocket: Optional[WebSocket] = None):
        """向聊天室广播消息"""
        if room_id in self.chat_rooms:
            # 发送给聊天室中的所有连接（除了发送者）
            for connection in self.chat_rooms[room_id]:
                if connection != sender_websocket:
                    try:
                        await connection.send_text(json.dumps(message, ensure_ascii=False))
                    except WebSocketDisconnect:
                        # 如果连接已断开，从聊天室中移除
                        self.chat_rooms[room_id].discard(connection)

    async def send_to_user(self, message: dict, user_id: int):
        """向特定用户发送消息"""
        if user_id in self.user_connections:
            for connection in self.user_connections[user_id]:
                try:
                    await connection.send_text(json.dumps(message, ensure_ascii=False))
                except WebSocketDisconnect:
                    pass

    def get_room_participants(self, room_id: str) -> int:
        """获取聊天室参与者数量"""
        if room_id in self.chat_rooms:
            return len(self.chat_rooms[room_id])
        return 0

# 创建全局连接管理器实例
manager = ConnectionManager()