from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Payment as PaymentModel, User
from schemas import PaymentCreate, Payment
from middleware.auth import verify_token

router = APIRouter()

@router.post("/payments/", response_model=Payment)
def create_payment(
    payment: PaymentCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_token)
):
    # 确保用户只能为自己创建支付记录
    db_payment = PaymentModel(
        user_id=current_user.id,
        amount=payment.amount,
        status=payment.status
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

@router.get("/payments/{payment_id}", response_model=Payment)
def read_payment(
    payment_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_token)
):
    # 确保用户只能查看自己的支付记录
    db_payment = db.query(PaymentModel).filter(
        PaymentModel.id == payment_id,
        PaymentModel.user_id == current_user.id
    ).first()
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment

@router.get("/payments/", response_model=list[Payment])
def read_user_payments(
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_token)
):
    # 查询当前用户的所有支付记录
    payments = db.query(PaymentModel).filter(PaymentModel.user_id == current_user.id).all()
    return payments