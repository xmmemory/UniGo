from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from ..database import get_db
from ..models import Booking as BookingModel, User, Trip as TripModel
from ..schemas import BookingCreate, Booking, TripInBooking
from ..auth.middleware import verify_token
from ..cache import cache_manager
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/bookings/", response_model=Booking)
async def create_booking(
    booking: BookingCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(verify_token)
):
    # 检查行程是否存在且有可用座位
    trip = db.query(TripModel).filter(TripModel.id == booking.trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="行程不存在")
    
    if getattr(trip, 'available_seats', 0) <= 0:
        raise HTTPException(status_code=400, detail="该行程已无可用座位")
    
    # 检查用户是否已经预订了该行程
    existing_booking = db.query(BookingModel).filter(
        BookingModel.trip_id == booking.trip_id,
        BookingModel.user_id == current_user.id
    ).first()
    
    if existing_booking:
        raise HTTPException(status_code=400, detail="您已经预订了该行程")
    
    # 创建预订记录
    db_booking = BookingModel(
        trip_id=booking.trip_id,
        user_id=current_user.id
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    
    # 减少行程的可用座位数
    setattr(trip, 'available_seats', getattr(trip, 'available_seats', 0) - 1)
    db.commit()
    
    # 获取关联的行程信息
    trip = db.query(TripModel).filter(TripModel.id == db_booking.trip_id).first()
    
    # 清除相关缓存
    cache_manager.delete(f"trip_{booking.trip_id}")
    cache_manager.delete("trips_all")
    cache_manager.delete("trips_public_all")
    cache_manager.delete(f"user_bookings_{current_user.id}")
    
    # 返回Pydantic模型而不是SQLAlchemy模型
    return Booking(
        id=getattr(db_booking, 'id', 0),
        trip_id=getattr(db_booking, 'trip_id', 0),
        user_id=getattr(db_booking, 'user_id', 0),
        booked_at=getattr(db_booking, 'booked_at', datetime.utcnow()),
        trip=TripInBooking(
            id=getattr(trip, 'id', 0) if trip else 0,
            departure=getattr(trip, 'departure', '') if trip else '',
            destination=getattr(trip, 'destination', '') if trip else '',
            departure_time=getattr(trip, 'departure_time', datetime.utcnow()) if trip else datetime.utcnow(),
            price_per_person=getattr(trip, 'price_per_person', 0.0) if trip else 0.0,
            available_seats=getattr(trip, 'available_seats', 0) if trip else 0,
            owner_name=trip.owner.username if trip and trip.owner else None
        ) if trip else None,
        status="confirmed"
    )

@router.get("/bookings/{booking_id}", response_model=Booking)
def read_booking(
    booking_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_token)
):
    # 尝试从缓存获取数据
    cache_key = f"booking_{booking_id}_{current_user.id}"
    cached_booking = cache_manager.get(cache_key)
    
    if cached_booking:
        print(f"Returning cached booking {booking_id}")
        return cached_booking
    
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
    result = Booking(
        id=getattr(db_booking, 'id', 0),
        trip_id=getattr(db_booking, 'trip_id', 0),
        user_id=getattr(db_booking, 'user_id', 0),
        booked_at=getattr(db_booking, 'booked_at', datetime.utcnow()),
        trip=TripInBooking(
            id=getattr(db_booking.trip, 'id', 0) if db_booking.trip else 0,
            departure=getattr(db_booking.trip, 'departure', '') if db_booking.trip else '',
            destination=getattr(db_booking.trip, 'destination', '') if db_booking.trip else '',
            departure_time=getattr(db_booking.trip, 'departure_time', datetime.utcnow()) if db_booking.trip else datetime.utcnow(),
            price_per_person=getattr(db_booking.trip, 'price_per_person', 0.0) if db_booking.trip else 0.0,
            available_seats=getattr(db_booking.trip, 'available_seats', 0) if db_booking.trip else 0,
            owner_name=db_booking.trip.owner.username if db_booking.trip and db_booking.trip.owner else None
        ) if db_booking.trip else None,
        status="confirmed"
    )
    
    # 缓存结果10分钟
    cache_manager.set(cache_key, result, timedelta(minutes=10))
    
    return result

# 优化：添加分页参数以减少不必要的数据传输（带缓存）
@router.get("/bookings/", response_model=list[Booking])
def read_user_bookings(
    skip: int = 0, 
    limit: int = 50,  # 默认限制为50条记录
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_token)
):
    # 尝试从缓存获取数据
    cache_key = f"user_bookings_{current_user.id}_{skip}_{limit}"
    cached_bookings = cache_manager.get(cache_key)
    
    if cached_bookings:
        print(f"Returning cached bookings for user {current_user.id}")
        return cached_bookings
    
    # 查询当前用户的所有预订记录及关联的行程信息，添加分页支持
    bookings = db.query(BookingModel).options(
        joinedload(BookingModel.trip).joinedload(TripModel.owner)
    ).filter(BookingModel.user_id == current_user.id).offset(skip).limit(limit).all()
    
    # 返回Pydantic模型列表而不是SQLAlchemy模型列表
    result = [
        Booking(
            id=getattr(booking, 'id', 0),
            trip_id=getattr(booking, 'trip_id', 0),
            user_id=getattr(booking, 'user_id', 0),
            booked_at=getattr(booking, 'booked_at', datetime.utcnow()),
            trip=TripInBooking(
                id=getattr(booking.trip, 'id', 0) if booking.trip else 0,
                departure=getattr(booking.trip, 'departure', '') if booking.trip else '',
                destination=getattr(booking.trip, 'destination', '') if booking.trip else '',
                departure_time=getattr(booking.trip, 'departure_time', datetime.utcnow()) if booking.trip else datetime.utcnow(),
                price_per_person=getattr(booking.trip, 'price_per_person', 0.0) if booking.trip else 0.0,
                available_seats=getattr(booking.trip, 'available_seats', 0) if booking.trip else 0,
                owner_name=booking.trip.owner.username if booking.trip and booking.trip.owner else None
            ) if booking.trip else None,
            status="confirmed"
        )
        for booking in bookings
    ]
    
    # 缓存结果5分钟
    cache_manager.set(cache_key, result, timedelta(minutes=5))
    
    return result

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
    
    # 获取行程信息用于后续检查
    trip = db_booking.trip
    
    # 保存行程信息用于返回（在删除之前）
    trip_info = None
    if trip:
        trip_info = TripInBooking(
            id=getattr(trip, 'id', 0),
            departure=getattr(trip, 'departure', ''),
            destination=getattr(trip, 'destination', ''),
            departure_time=getattr(trip, 'departure_time', datetime.utcnow()),
            price_per_person=getattr(trip, 'price_per_person', 0.0),
            available_seats=getattr(trip, 'available_seats', 0),
            owner_name=trip.owner.username if trip.owner else None
        )
    
    # 删除预订记录
    db.delete(db_booking)
    db.commit()
    
    # 增加行程的可用座位数
    if trip:
        setattr(trip, 'available_seats', getattr(trip, 'available_seats', 0) + 1)
        db.commit()
    
    # 检查该行程是否还有其他预订
    remaining_bookings = db.query(BookingModel).filter(BookingModel.trip_id == getattr(trip, 'id', 0)).count()
    
    # 如果该行程没有其他预订且发布者也是预订者（即发布者取消了自己的预订）
    # 则删除该行程
    if remaining_bookings == 0:
        # 检查发布者是否也是预订者
        publisher_booking = db.query(BookingModel).filter(
            BookingModel.trip_id == getattr(trip, 'id', 0),
            BookingModel.user_id == getattr(trip, 'owner_id', 0)
        ).first()
        
        if publisher_booking:
            # 删除行程
            db.delete(trip)
            db.commit()
    
    # 清除相关缓存
    cache_manager.delete(f"booking_{booking_id}_{current_user.id}")
    cache_manager.delete(f"user_bookings_{current_user.id}")
    if trip:
        cache_manager.delete(f"trip_{getattr(trip, 'id', 0)}")
        cache_manager.delete("trips_all")
        cache_manager.delete("trips_public_all")
    
    # 返回已删除的预订记录（Pydantic模型）
    return Booking(
        id=getattr(db_booking, 'id', 0),
        trip_id=getattr(db_booking, 'trip_id', 0),
        user_id=getattr(db_booking, 'user_id', 0),
        booked_at=getattr(db_booking, 'booked_at', datetime.utcnow()),
        trip=trip_info,
        status="cancelled"
    )