from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, not_
from typing import List
from datetime import datetime
from ..database import get_db
from ..models import ErrandTask as ErrandTaskModel, ErrandResponse as ErrandResponseModel, User
from ..schemas import ErrandTaskCreate, ErrandTask, ErrandResponseCreate, ErrandResponse, ErrandTaskListResponse
from ..auth.middleware import verify_token

router = APIRouter()

@router.post("/errands/", response_model=ErrandTask)
def create_errand_task(
    task: ErrandTaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_token)
):
    """创建跑腿任务"""
    try:
        print(f"=== 创建跑腿任务开始 ===")
        print(f"用户: {current_user.username} (ID: {current_user.id})")
        print(f"任务数据: {task.dict()}")
        
        # 验证数据
        if not task.title or len(task.title.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="任务标题不能为空"
            )
            
        if not task.description or len(task.description.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="任务描述不能为空"
            )
            
        if not task.location or len(task.location.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="任务地点不能为空"
            )
            
        if task.reward < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="酬劳不能为负数"
            )
            
        if task.deadline is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="截止时间不能为空"
            )
            
        # 检查截止时间是否在将来
        # 修复时区比较问题：使用带时区的当前时间
        from datetime import timezone
        if task.deadline <= datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="截止时间必须在将来"
            )
        
        print(f"数据验证通过")
        
        # 创建任务对象
        # 修复时区问题：使用带时区的当前时间
        now = datetime.now(timezone.utc)
        db_task = ErrandTaskModel(
            title=task.title.strip(),
            description=task.description.strip(),
            reward=task.reward,
            location=task.location.strip(),
            deadline=task.deadline,
            owner_id=current_user.id,
            created_at=now,
            updated_at=now,
            status="open"
        )
        
        print(f"创建任务对象完成")
        print(f"Adding task to database")
        db.add(db_task)
        
        print(f"Committing transaction")
        try:
            db.commit()
            print(f"数据库提交成功")
        except Exception as commit_error:
            print(f"Commit error: {str(commit_error)}")
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"数据库提交失败: {str(commit_error)}"
            )
            
        print(f"Refreshing task")
        try:
            db.refresh(db_task)
            print(f"数据库刷新成功")
        except Exception as refresh_error:
            print(f"Refresh error: {str(refresh_error)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"数据库刷新失败: {str(refresh_error)}"
            )
        
        # 添加发布者姓名
        db_task.owner_name = current_user.username
        
        print(f"Task created successfully with ID: {db_task.id}")
        print(f"=== 创建跑腿任务结束 ===")
        
        # 返回Pydantic模型而不是SQLAlchemy模型
        return ErrandTask(
            id=getattr(db_task, 'id'),
            title=getattr(db_task, 'title'),
            description=getattr(db_task, 'description'),
            reward=getattr(db_task, 'reward'),
            location=getattr(db_task, 'location'),
            deadline=getattr(db_task, 'deadline'),
            owner_id=getattr(db_task, 'owner_id'),
            owner_name=getattr(db_task, 'owner_name'),
            assignee_id=getattr(db_task, 'assignee_id'),
            assignee_name=getattr(db_task, 'assignee_name', None),
            created_at=getattr(db_task, 'created_at'),
            updated_at=getattr(db_task, 'updated_at'),
            status=getattr(db_task, 'status')
        )
    except HTTPException:
        # 重新抛出HTTP异常
        raise
    except Exception as e:
        # 回滚事务以防出错
        try:
            db.rollback()
            print(f"数据库回滚完成")
        except Exception as rollback_error:
            print(f"数据库回滚失败: {str(rollback_error)}")
            
        print(f"Error creating errand task: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # 如果是HTTP异常，重新抛出
        if isinstance(e, HTTPException):
            raise e
            
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建跑腿任务失败: {str(e)}"
        )

@router.get("/errands/", response_model=ErrandTaskListResponse)
def read_errand_tasks(
    skip: int = 0,
    limit: int = 100,
    status: str = Query(None, description="任务状态"),
    search: str = Query(None, description="搜索关键词"),
    db: Session = Depends(get_db)
):
    """获取跑腿任务列表"""
    query = db.query(ErrandTaskModel).filter(ErrandTaskModel.status != "cancelled")
    
    # 按状态筛选
    if status:
        query = query.filter(ErrandTaskModel.status == status)
    
    # 搜索关键词
    if search:
        query = query.filter(
            and_(
                ErrandTaskModel.status != "cancelled",
                or_(
                    ErrandTaskModel.title.contains(search),
                    ErrandTaskModel.description.contains(search)
                )
            )
        )
    
    # 关联用户信息
    query = query.join(User, ErrandTaskModel.owner_id == User.id)
    
    # 获取总数
    total = query.count()
    
    # 应用分页
    tasks = query.offset(skip).limit(limit).all()
    
    # 添加发布者和接取者姓名
    result = []
    for task_obj in tasks:
        # 获取发布者信息
        owner = db.query(User).filter(User.id == task_obj.owner_id).first()
        if owner:
            task_obj.owner_name = owner.username
        
        # 获取接取者信息
        if task_obj.assignee_id is not None:
            assignee = db.query(User).filter(User.id == task_obj.assignee_id).first()
            if assignee:
                task_obj.assignee_name = assignee.username
                
        # 转换为Pydantic模型
        result.append(ErrandTask(
            id=getattr(task_obj, 'id'),
            title=getattr(task_obj, 'title'),
            description=getattr(task_obj, 'description'),
            reward=getattr(task_obj, 'reward'),
            location=getattr(task_obj, 'location'),
            deadline=getattr(task_obj, 'deadline'),
            owner_id=getattr(task_obj, 'owner_id'),
            owner_name=getattr(task_obj, 'owner_name'),
            assignee_id=getattr(task_obj, 'assignee_id'),
            assignee_name=getattr(task_obj, 'assignee_name', None),
            created_at=getattr(task_obj, 'created_at'),
            updated_at=getattr(task_obj, 'updated_at'),
            status=getattr(task_obj, 'status')
        ))
    
    # 计算分页信息
    total_pages = (total + limit - 1) // limit
    page = skip // limit + 1
    
    # 返回包含任务列表和分页信息的对象
    return {
        "tasks": result, 
        "total": total,
        "page": page,
        "total_pages": total_pages,
        "limit": limit
    }

@router.get("/errands/{task_id}", response_model=ErrandTask)
def read_errand_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """获取跑腿任务详情"""
    db_task = db.query(ErrandTaskModel).filter(
        and_(
            ErrandTaskModel.id == task_id,
            ErrandTaskModel.status != "cancelled"
        )
    ).first()
    
    if db_task is None:
        raise HTTPException(status_code=404, detail="任务未找到")
    
    # 获取发布者信息
    owner = db.query(User).filter(User.id == db_task.owner_id).first()
    if owner:
        db_task.owner_name = owner.username
    
    # 获取接取者信息（检查assignee_id是否为None）
    if db_task.assignee_id is not None:
        assignee = db.query(User).filter(User.id == db_task.assignee_id).first()
        if assignee:
            db_task.assignee_name = assignee.username
    
    # 返回Pydantic模型而不是SQLAlchemy模型
    return ErrandTask(
        id=getattr(db_task, 'id'),
        title=getattr(db_task, 'title'),
        description=getattr(db_task, 'description'),
        reward=getattr(db_task, 'reward'),
        location=getattr(db_task, 'location'),
        deadline=getattr(db_task, 'deadline'),
        owner_id=getattr(db_task, 'owner_id'),
        owner_name=getattr(db_task, 'owner_name'),
        assignee_id=getattr(db_task, 'assignee_id'),
        assignee_name=getattr(db_task, 'assignee_name', None),
        created_at=getattr(db_task, 'created_at'),
        updated_at=getattr(db_task, 'updated_at'),
        status=getattr(db_task, 'status')
    )

@router.put("/errands/{task_id}", response_model=ErrandTask)
def update_errand_task(
    task_id: int,
    task: ErrandTaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_token)
):
    """更新跑腿任务"""
    db_task = db.query(ErrandTaskModel).filter(
        and_(
            ErrandTaskModel.id == task_id,
            ErrandTaskModel.owner_id == current_user.id
        )
    ).first()
    
    if db_task is None:
        raise HTTPException(status_code=404, detail="任务未找到或无权限修改")
    
    # 检查任务状态，只有开放状态的任务才能修改
    # 先从数据库获取任务的当前状态
    current_status = db.query(ErrandTaskModel.status).filter(ErrandTaskModel.id == task_id).scalar()
    if current_status != "open":
        raise HTTPException(status_code=400, detail="只有开放状态的任务才能修改")
    
    # 更新任务信息
    update_data = task.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    db_task.__dict__.update(update_data)
    
    db.commit()
    db.refresh(db_task)
    
    # 添加发布者姓名
    db_task.owner_name = current_user.username
    
    return db_task

@router.delete("/errands/{task_id}")
def delete_errand_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_token)
):
    """删除跑腿任务（取消任务）"""
    db_task = db.query(ErrandTaskModel).filter(
        and_(
            ErrandTaskModel.id == task_id,
            ErrandTaskModel.owner_id == current_user.id
        )
    ).first()
    
    if db_task is None:
        raise HTTPException(status_code=404, detail="任务未找到或无权限删除")
    
    # 只有开放状态的任务才能取消
    # 先从数据库获取任务的当前状态
    current_status = db.query(ErrandTaskModel.status).filter(ErrandTaskModel.id == task_id).scalar()
    if current_status != "open":
        raise HTTPException(status_code=400, detail="只有开放状态的任务才能取消")
    
    # 取消任务
    db_task.__dict__.update({
        "status": "cancelled",
        "updated_at": datetime.utcnow()
    })
    
    db.commit()
    
    return {"message": "任务已取消"}

@router.post("/errands/{task_id}/responses/", response_model=ErrandResponse)
def create_errand_response(
    task_id: int,
    response: ErrandResponseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_token)
):
    """响应跑腿任务"""
    # 检查任务是否存在且处于开放状态
    db_task = db.query(ErrandTaskModel).filter(
        and_(
            ErrandTaskModel.id == task_id,
            ErrandTaskModel.status == "open"
        )
    ).first()
    
    if db_task is None:
        raise HTTPException(status_code=404, detail="任务未找到或不处于开放状态")
    
    # 检查是否已经响应过该任务
    existing_response = db.query(ErrandResponseModel).filter(
        and_(
            ErrandResponseModel.task_id == task_id,
            ErrandResponseModel.user_id == current_user.id
        )
    ).first()
    
    if existing_response is not None:
        raise HTTPException(status_code=400, detail="您已经响应过该任务")
    
    # 创建响应
    db_response = ErrandResponseModel(
        task_id=task_id,
        user_id=current_user.id,
        message=response.message,
        created_at=datetime.utcnow(),
        is_accepted=False
    )
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    
    # 添加用户姓名
    db_response.user_name = current_user.username
    
    return db_response

@router.get("/errands/{task_id}/responses/", response_model=List[ErrandResponse])
def read_errand_responses(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_token)
):
    """获取跑腿任务的响应列表"""
    # 检查任务是否存在且用户是任务发布者
    db_task = db.query(ErrandTaskModel).filter(
        and_(
            ErrandTaskModel.id == task_id,
            ErrandTaskModel.owner_id == current_user.id
        )
    ).first()
    
    if db_task is None:
        raise HTTPException(status_code=404, detail="任务未找到或无权限查看响应")
    
    # 获取响应列表
    responses = db.query(ErrandResponseModel).filter(
        ErrandResponseModel.task_id == task_id
    ).join(User, ErrandResponseModel.user_id == User.id).all()
    
    # 添加用户姓名
    result = []
    for response_obj in responses:
        user = db.query(User).filter(User.id == response_obj.user_id).first()
        if user:
            response_obj.user_name = user.username
        result.append(response_obj)
    
    return result

@router.post("/errands/{task_id}/accept/{response_id}")
def accept_errand_response(
    task_id: int,
    response_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_token)
):
    """接受跑腿任务响应"""
    # 检查任务是否存在且用户是任务发布者
    db_task = db.query(ErrandTaskModel).filter(
        and_(
            ErrandTaskModel.id == task_id,
            ErrandTaskModel.owner_id == current_user.id,
            ErrandTaskModel.status == "open"
        )
    ).first()
    
    if db_task is None:
        raise HTTPException(status_code=404, detail="任务未找到或无权限操作")
    
    # 检查响应是否存在
    db_response = db.query(ErrandResponseModel).filter(
        and_(
            ErrandResponseModel.id == response_id,
            ErrandResponseModel.task_id == task_id
        )
    ).first()
    
    if db_response is None:
        raise HTTPException(status_code=404, detail="响应未找到")
    
    # 更新响应状态
    db_response.__dict__.update({
        "is_accepted": True
    })
    
    # 更新任务状态和接取者
    db_task.__dict__.update({
        "assignee_id": db_response.user_id,
        "status": "in_progress",
        "updated_at": datetime.utcnow()
    })
    
    db.commit()
    
    return {"message": "已接受响应，任务状态更新为进行中"}

@router.post("/errands/{task_id}/complete")
def complete_errand_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_token)
):
    """完成跑腿任务"""
    # 检查任务是否存在且用户是任务接取者
    db_task = db.query(ErrandTaskModel).filter(
        and_(
            ErrandTaskModel.id == task_id,
            ErrandTaskModel.assignee_id == current_user.id,
            ErrandTaskModel.status == "in_progress"
        )
    ).first()
    
    if db_task is None:
        raise HTTPException(status_code=404, detail="任务未找到或无权限操作")
    
    # 更新任务状态
    db_task.__dict__.update({
        "status": "completed",
        "updated_at": datetime.utcnow()
    })
    
    db.commit()
    
    return {"message": "任务已完成"}

@router.get("/errands/user/tasks/", response_model=List[ErrandTask])
def read_user_errand_tasks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_token)
):
    """获取用户发布的跑腿任务"""
    tasks = db.query(ErrandTaskModel).filter(
        ErrandTaskModel.owner_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    # 获取发布者信息
    if tasks:
        for task in tasks:
            task.owner_name = current_user.username
    
    return tasks

@router.get("/errands/user/assigned/", response_model=List[ErrandTask])
def read_user_assigned_errand_tasks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_token)
):
    """获取用户接取的跑腿任务"""
    tasks = db.query(ErrandTaskModel).filter(
        ErrandTaskModel.assignee_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    # 获取接取者信息
    if tasks:
        for task in tasks:
            task.assignee_name = current_user.username
            
            # 获取发布者信息
            owner = db.query(User).filter(User.id == task.owner_id).first()
            if owner:
                task.owner_name = owner.username
    
    return tasks