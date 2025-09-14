from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from database import get_db
from models import Trip as TripModel, User
from schemas import TripCreate, Trip
from middleware.auth import verify_token

router = APIRouter()

@router.post("/trips/", response_model=Trip)
async def create_trip(
    trip: TripCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(verify_token)
):
    db_trip = TripModel(**trip.dict(), owner_id=current_user.id)
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    # 重新查询以确保关联的用户信息被加载
    db_trip = db.query(TripModel).options(joinedload(TripModel.owner)).filter(TripModel.id == db_trip.id).first()
    # 返回Pydantic模型而不是SQLAlchemy模型
    return Trip(
        id=db_trip.id,
        departure=db_trip.departure,
        destination=db_trip.destination,
        departure_time=db_trip.departure_time,
        price_per_person=db_trip.price_per_person,
        available_seats=db_trip.available_seats,
        owner_id=db_trip.owner_id,
        owner_name=db_trip.owner.username if db_trip.owner else None
    )

@router.get("/trips/{trip_id}", response_model=Trip)
def read_trip(
    trip_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_token)
):
    db_trip = db.query(TripModel).options(joinedload(TripModel.owner)).filter(TripModel.id == trip_id).first()
    if db_trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    # 返回Pydantic模型而不是SQLAlchemy模型
    return Trip(
        id=db_trip.id,
        departure=db_trip.departure,
        destination=db_trip.destination,
        departure_time=db_trip.departure_time,
        price_per_person=db_trip.price_per_person,
        available_seats=db_trip.available_seats,
        owner_id=db_trip.owner_id,
        owner_name=db_trip.owner.username if db_trip.owner else None
    )

@router.get("/trips/", response_model=list[Trip])
def read_user_trips(
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_token)
):
    # 查询当前用户创建的所有行程，并预加载用户信息
    trips = db.query(TripModel).options(joinedload(TripModel.owner)).filter(TripModel.owner_id == current_user.id).all()
    # 返回Pydantic模型列表而不是SQLAlchemy模型列表
    return [
        Trip(
            id=trip.id,
            departure=trip.departure,
            destination=trip.destination,
            departure_time=trip.departure_time,
            price_per_person=trip.price_per_person,
            available_seats=trip.available_seats,
            owner_id=trip.owner_id,
            owner_name=trip.owner.username if trip.owner else None
        )
        for trip in trips
    ]

# 新增：公开获取所有行程的端点（无需认证）
@router.get("/trips/public/all/", response_model=list[Trip])
def read_public_trips(
    db: Session = Depends(get_db)
):
    # 查询所有公开的行程，并预加载用户信息
    trips = db.query(TripModel).options(joinedload(TripModel.owner)).all()
    # 返回Pydantic模型列表而不是SQLAlchemy模型列表
    return [
        Trip(
            id=trip.id,
            departure=trip.departure,
            destination=trip.destination,
            departure_time=trip.departure_time,
            price_per_person=trip.price_per_person,
            available_seats=trip.available_seats,
            owner_id=trip.owner_id,
            owner_name=trip.owner.username if trip.owner else None
        )
        for trip in trips
    ]

@router.get("/trips/all/", response_model=list[Trip])
def read_all_trips(
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_token)
):
    # 查询所有公开的行程，并预加载用户信息
    trips = db.query(TripModel).options(joinedload(TripModel.owner)).all()
    # 返回Pydantic模型列表而不是SQLAlchemy模型列表
    return [
        Trip(
            id=trip.id,
            departure=trip.departure,
            destination=trip.destination,
            departure_time=trip.departure_time,
            price_per_person=trip.price_per_person,
            available_seats=trip.available_seats,
            owner_id=trip.owner_id,
            owner_name=trip.owner.username if trip.owner else None
        )
        for trip in trips
    ]