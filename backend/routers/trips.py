from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
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
    return db_trip

@router.get("/trips/{trip_id}", response_model=Trip)
def read_trip(
    trip_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_token)
):
    db_trip = db.query(TripModel).filter(TripModel.id == trip_id).first()
    if db_trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    return db_trip

@router.get("/trips/", response_model=list[Trip])
def read_user_trips(
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_token)
):
    # 查询当前用户创建的所有行程
    trips = db.query(TripModel).filter(TripModel.owner_id == current_user.id).all()
    return trips

@router.get("/trips/all/", response_model=list[Trip])
def read_all_trips(
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_token)
):
    # 查询所有公开的行程
    trips = db.query(TripModel).all()
    return trips