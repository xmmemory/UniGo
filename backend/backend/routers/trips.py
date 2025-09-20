from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from ..database import get_db
from ..models import Trip as TripModel, User
from ..schemas import TripCreate, Trip
from ..auth.middleware import verify_token
from ..cache import cache_manager
from datetime import datetime, timedelta
import traceback

router = APIRouter()

@router.post("/trips/", response_model=Trip)
async def create_trip(
    trip: TripCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(verify_token)
):
    try:
        print(f"Creating trip with data: {trip.dict()}")
        db_trip = TripModel(**trip.dict(), owner_id=current_user.id)
        db.add(db_trip)
        db.commit()
        db.refresh(db_trip)
        print(f"Trip created with ID: {db_trip.id}")
        # 重新查询以确保关联的用户信息被加载
        db_trip = db.query(TripModel).options(joinedload(TripModel.owner)).filter(TripModel.id == db_trip.id).first()
        print(f"Trip reloaded: {db_trip}")
        # 返回Pydantic模型而不是SQLAlchemy模型
        result = Trip(
            id=getattr(db_trip, 'id', 0),
            departure=getattr(db_trip, 'departure', ''),
            destination=getattr(db_trip, 'destination', ''),
            departure_time=getattr(db_trip, 'departure_time', datetime.utcnow()),
            price_per_person=getattr(db_trip, 'price_per_person', 0.0),
            available_seats=getattr(db_trip, 'available_seats', 0),
            owner_id=getattr(db_trip, 'owner_id', 0),
            owner_name=db_trip.owner.username if db_trip and db_trip.owner else None
        )
        print(f"Returning trip: {result}")
        
        # 清除相关缓存
        cache_manager.delete("trips_all")
        cache_manager.delete("trips_public_all")
        
        return result
    except Exception as e:
        print(f"Error creating trip: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"创建行程失败: {str(e)}"
        )

@router.get("/trips/{trip_id}", response_model=Trip)
def read_trip(
    trip_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_token)
):
    # 尝试从缓存获取数据
    cache_key = f"trip_{trip_id}"
    cached_trip = cache_manager.get(cache_key)
    
    if cached_trip:
        print(f"Returning cached trip {trip_id}")
        return cached_trip
    
    db_trip = db.query(TripModel).options(joinedload(TripModel.owner)).filter(TripModel.id == trip_id).first()
    if db_trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    # 返回Pydantic模型而不是SQLAlchemy模型
    result = Trip(
        id=getattr(db_trip, 'id', 0),
        departure=getattr(db_trip, 'departure', ''),
        destination=getattr(db_trip, 'destination', ''),
        departure_time=getattr(db_trip, 'departure_time', datetime.utcnow()),
        price_per_person=getattr(db_trip, 'price_per_person', 0.0),
        available_seats=getattr(db_trip, 'available_seats', 0),
        owner_id=getattr(db_trip, 'owner_id', 0),
        owner_name=db_trip.owner.username if db_trip and db_trip.owner else None
    )
    
    # 缓存结果10分钟
    cache_manager.set(cache_key, result, timedelta(minutes=10))
    
    return result

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
            id=getattr(trip, 'id', 0),
            departure=getattr(trip, 'departure', ''),
            destination=getattr(trip, 'destination', ''),
            departure_time=getattr(trip, 'departure_time', datetime.utcnow()),
            price_per_person=getattr(trip, 'price_per_person', 0.0),
            available_seats=getattr(trip, 'available_seats', 0),
            owner_id=getattr(trip, 'owner_id', 0),
            owner_name=trip.owner.username if trip and trip.owner else None
        )
        for trip in trips
    ]

# 新增：公开获取所有行程的端点（无需认证，带缓存）
@router.get("/trips/public/all/")
def read_public_trips(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    try:
        # 查询所有行程总数
        total = db.query(TripModel).count()
        
        # 查询所有行程，并预加载用户信息，添加分页支持
        trips = db.query(TripModel).options(joinedload(TripModel.owner)).offset(skip).limit(limit).all()
        
        # 返回Pydantic模型列表而不是SQLAlchemy模型列表
        result = []
        for trip in trips:
            trip_dict = {
                "id": getattr(trip, 'id', 0),
                "departure": getattr(trip, 'departure', ''),
                "destination": getattr(trip, 'destination', ''),
                "departure_time": getattr(trip, 'departure_time', datetime.utcnow()),
                "price_per_person": getattr(trip, 'price_per_person', 0.0),
                "available_seats": getattr(trip, 'available_seats', 0),
                "owner_id": getattr(trip, 'owner_id', 0),
                "owner_name": trip.owner.username if trip and trip.owner else None
            }
            result.append(trip_dict)
        
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
    except Exception as e:
        print(f"Error in read_public_trips: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# 优化：添加分页参数以减少不必要的数据传输（带缓存）
@router.get("/trips/all/")
def read_all_trips(
    skip: int = 0, 
    limit: int = 50,  # 默认限制为50条记录
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_token)
):
    try:
        # 查询所有行程总数
        total = db.query(TripModel).count()
        
        # 查询所有行程，并预加载用户信息，添加分页支持
        trips = db.query(TripModel).options(joinedload(TripModel.owner)).offset(skip).limit(limit).all()
        
        # 返回Pydantic模型列表而不是SQLAlchemy模型列表
        result = []
        for trip in trips:
            trip_dict = {
                "id": getattr(trip, 'id', 0),
                "departure": getattr(trip, 'departure', ''),
                "destination": getattr(trip, 'destination', ''),
                "departure_time": getattr(trip, 'departure_time', datetime.utcnow()),
                "price_per_person": getattr(trip, 'price_per_person', 0.0),
                "available_seats": getattr(trip, 'available_seats', 0),
                "owner_id": getattr(trip, 'owner_id', 0),
                "owner_name": trip.owner.username if trip and trip.owner else None
            }
            result.append(trip_dict)
        
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
    except Exception as e:
        print(f"Error in read_all_trips: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
