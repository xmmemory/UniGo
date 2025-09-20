from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List
from datetime import datetime
from ..database import get_db
from ..models import SecondHandItem as SecondHandItemModel, User
from ..schemas import SecondHandItemCreate, SecondHandItem
from ..auth.middleware import verify_token

router = APIRouter()

@router.post("/secondhand/", response_model=SecondHandItem)
def create_secondhand_item(
    item: SecondHandItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_token)
):
    """创建二手商品"""
    db_item = SecondHandItemModel(
        title=item.title,
        description=item.description,
        price=item.price,
        category=item.category,
        condition=item.condition,
        owner_id=current_user.id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        is_active=True
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    # 添加发布者姓名
    db_item.owner_name = current_user.username
    
    return db_item

@router.get("/secondhand/")
def read_secondhand_items(
    skip: int = 0,
    limit: int = 100,
    category: str = Query(None, description="商品分类"),
    search: str = Query(None, description="搜索关键词"),
    db: Session = Depends(get_db)
):
    """获取二手商品列表"""
    query = db.query(SecondHandItemModel).filter(SecondHandItemModel.is_active == True)
    
    # 按分类筛选
    if category:
        query = query.filter(SecondHandItemModel.category == category)
    
    # 搜索关键词
    if search:
        query = query.filter(
            and_(
                SecondHandItemModel.is_active == True,
                SecondHandItemModel.title.contains(search) | 
                SecondHandItemModel.description.contains(search)
            )
        )
    
    # 获取总数
    total = query.count()
    
    # 关联用户信息
    query = query.join(User, SecondHandItemModel.owner_id == User.id)
    
    # 应用分页
    items = query.offset(skip).limit(limit).all()
    
    # 添加发布者姓名
    result = []
    for item_obj in items:
        owner = db.query(User).filter(User.id == item_obj.owner_id).first()
        if owner:
            item_obj.owner_name = owner.username
        result.append(item_obj)
    
    # 计算分页信息
    total_pages = (total + limit - 1) // limit
    page = skip // limit + 1
    
    # 创建分页响应对象
    response = {
        "items": result,
        "total": total,
        "page": page,
        "total_pages": total_pages,
        "limit": limit
    }
    
    return response

@router.get("/secondhand/{item_id}", response_model=SecondHandItem)
def read_secondhand_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    """获取二手商品详情"""
    db_item = db.query(SecondHandItemModel).filter(
        SecondHandItemModel.id == item_id,
        SecondHandItemModel.is_active == True
    ).first()
    
    if db_item is None:
        raise HTTPException(status_code=404, detail="商品未找到")
    
    # 获取发布者信息
    owner = db.query(User).filter(User.id == db_item.owner_id).first()
    if owner:
        db_item.owner_name = owner.username
    
    # 将数据库模型转换为Pydantic模型
    return SecondHandItem.from_orm(db_item)

@router.put("/secondhand/{item_id}", response_model=SecondHandItem)
def update_secondhand_item(
    item_id: int,
    item: SecondHandItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_token)
):
    """更新二手商品"""
    db_item = db.query(SecondHandItemModel).filter(
        SecondHandItemModel.id == item_id,
        SecondHandItemModel.owner_id == current_user.id
    ).first()
    
    if db_item is None:
        raise HTTPException(status_code=404, detail="商品未找到或无权限修改")
    
    # 更新商品信息
    update_data = item.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    db_item.__dict__.update(update_data)
    
    db.commit()
    db.refresh(db_item)
    
    # 添加发布者姓名
    db_item.owner_name = current_user.username
    
    # 将数据库模型转换为Pydantic模型
    return SecondHandItem.from_orm(db_item)

@router.delete("/secondhand/{item_id}")
def delete_secondhand_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_token)
):
    """删除二手商品（软删除）"""
    db_item = db.query(SecondHandItemModel).filter(
        SecondHandItemModel.id == item_id,
        SecondHandItemModel.owner_id == current_user.id
    ).first()
    
    if db_item is None:
        raise HTTPException(status_code=404, detail="商品未找到或无权限删除")
    
    # 软删除
    db_item.__dict__.update({
        "is_active": False,
        "updated_at": datetime.utcnow()
    })
    
    db.commit()
    
    return {"message": "商品已删除"}

@router.get("/secondhand/user/{user_id}", response_model=List[SecondHandItem])
def read_user_secondhand_items(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """获取用户发布的二手商品"""
    items = db.query(SecondHandItemModel).filter(
        SecondHandItemModel.owner_id == user_id,
        SecondHandItemModel.is_active == True
    ).offset(skip).limit(limit).all()
    
    # 获取发布者信息
    if items:
        owner = db.query(User).filter(User.id == user_id).first()
        if owner:
            for item in items:
                item.owner_name = owner.username
    
    # 将数据库模型列表转换为Pydantic模型列表
    return [SecondHandItem.from_orm(item) for item in items]