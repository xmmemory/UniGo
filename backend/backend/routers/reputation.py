from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import ReputationRecord as ReputationRecordModel, User as UserModel
from ..schemas import ReputationRecordCreate, ReputationRecord
from ..auth.middleware import verify_token

router = APIRouter()

@router.post("/reputation/", response_model=ReputationRecord)
async def create_reputation_record(
    record: ReputationRecordCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(verify_token)
):
    # 创建信誉度记录
    db_record = ReputationRecordModel(
        user_id=record.user_id,
        score_change=record.score_change,
        reason=record.reason
    )
    db.add(db_record)
    
    # 更新用户信誉度分数
    user = db.query(UserModel).filter(UserModel.id == record.user_id).first()
    if user:
        # 获取当前信誉度分数
        current_score = getattr(user, 'reputation_score')
        new_score = current_score + record.score_change
        # 确保信誉度分数在0-100之间
        new_score = max(0, min(100, new_score))
        setattr(user, 'reputation_score', new_score)
    
    db.commit()
    db.refresh(db_record)
    
    return db_record

@router.get("/reputation/user/{user_id}", response_model=list[ReputationRecord])
def get_user_reputation_records(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(verify_token)
):
    # 获取用户的信誉度记录
    records = db.query(ReputationRecordModel).filter(
        ReputationRecordModel.user_id == user_id
    ).all()
    
    return records

@router.get("/reputation/user/{user_id}/score", response_model=int)
def get_user_reputation_score(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(verify_token)
):
    # 获取用户的信誉度分数
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return getattr(user, 'reputation_score')