from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Booking as BookingModel, User
from schemas import BookingCreate, Booking
from middleware.auth import verify_token

router = APIRouter()

@router.post("/bookings/", response_model=Booking)
async def create_booking(
    booking: BookingCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(verify_token)
):
    # 创建预订记录
    db_booking = BookingModel(
        trip_id=booking.trip_id,
        user_id=current_user.id
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

@router.get("/bookings/{booking_id}", response_model=Booking)
def read_booking(
    booking_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_token)
):
    # 查询预订记录
    db_booking = db.query(BookingModel).filter(
        BookingModel.id == booking_id,
        BookingModel.user_id == current_user.id
    ).first()
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_booking

@router.get("/bookings/", response_model=list[Booking])
def read_user_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_token)
):
    # 查询当前用户的所有预订记录
    bookings = db.query(BookingModel).filter(BookingModel.user_id == current_user.id).all()
    return bookings