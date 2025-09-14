from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from database import get_db
from models import Booking as BookingModel, User, Trip as TripModel
from schemas import BookingCreate, Booking, TripInBooking
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
    
    # 获取关联的行程信息
    trip = db.query(TripModel).filter(TripModel.id == db_booking.trip_id).first()
    
    # 返回Pydantic模型而不是SQLAlchemy模型
    return Booking(
        id=db_booking.id,
        trip_id=db_booking.trip_id,
        user_id=db_booking.user_id,
        booked_at=db_booking.booked_at,
        trip=TripInBooking(
            id=trip.id,
            departure=trip.departure,
            destination=trip.destination,
            departure_time=trip.departure_time,
            price_per_person=trip.price_per_person,
            available_seats=trip.available_seats,
            owner_name=trip.owner.username if trip.owner else None
        ) if trip else None,
        status="confirmed"
    )

@router.get("/bookings/{booking_id}", response_model=Booking)
def read_booking(
    booking_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_token)
):
    # 查询预订记录及关联的行程信息
    db_booking = db.query(BookingModel).options(
        joinedload(BookingModel.trip).joinedload(TripModel.owner)
    ).filter(
        BookingModel.id == booking_id,
        BookingModel.user_id == current_user.id
    ).first()
    
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # 返回Pydantic模型而不是SQLAlchemy模型
    return Booking(
        id=db_booking.id,
        trip_id=db_booking.trip_id,
        user_id=db_booking.user_id,
        booked_at=db_booking.booked_at,
        trip=TripInBooking(
            id=db_booking.trip.id,
            departure=db_booking.trip.departure,
            destination=db_booking.trip.destination,
            departure_time=db_booking.trip.departure_time,
            price_per_person=db_booking.trip.price_per_person,
            available_seats=db_booking.trip.available_seats,
            owner_name=db_booking.trip.owner.username if db_booking.trip.owner else None
        ) if db_booking.trip else None,
        status="confirmed"
    )

@router.get("/bookings/", response_model=list[Booking])
def read_user_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_token)
):
    # 查询当前用户的所有预订记录及关联的行程信息
    bookings = db.query(BookingModel).options(
        joinedload(BookingModel.trip).joinedload(TripModel.owner)
    ).filter(BookingModel.user_id == current_user.id).all()
    
    # 返回Pydantic模型列表而不是SQLAlchemy模型列表
    return [
        Booking(
            id=booking.id,
            trip_id=booking.trip_id,
            user_id=booking.user_id,
            booked_at=booking.booked_at,
            trip=TripInBooking(
                id=booking.trip.id,
                departure=booking.trip.departure,
                destination=booking.trip.destination,
                departure_time=booking.trip.departure_time,
                price_per_person=booking.trip.price_per_person,
                available_seats=booking.trip.available_seats,
                owner_name=booking.trip.owner.username if booking.trip.owner else None
            ) if booking.trip else None,
            status="confirmed"
        )
        for booking in bookings
    ]

@router.delete("/bookings/{booking_id}", response_model=Booking)
def delete_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_token)
):
    # 查询预订记录及关联的行程信息
    db_booking = db.query(BookingModel).options(
        joinedload(BookingModel.trip).joinedload(TripModel.owner)
    ).filter(
        BookingModel.id == booking_id,
        BookingModel.user_id == current_user.id
    ).first()
    
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # 删除预订记录
    db.delete(db_booking)
    db.commit()
    
    # 返回已删除的预订记录（Pydantic模型）
    return Booking(
        id=db_booking.id,
        trip_id=db_booking.trip_id,
        user_id=db_booking.user_id,
        booked_at=db_booking.booked_at,
        trip=TripInBooking(
            id=db_booking.trip.id,
            departure=db_booking.trip.departure,
            destination=db_booking.trip.destination,
            departure_time=db_booking.trip.departure_time,
            price_per_person=db_booking.trip.price_per_person,
            available_seats=db_booking.trip.available_seats,
            owner_name=db_booking.trip.owner.username if db_booking.trip.owner else None
        ) if db_booking.trip else None,
        status="cancelled"
    )