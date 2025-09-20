from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, OperationalError
from datetime import datetime, timedelta
from sqlalchemy import func, and_, text
import os

from ..database import get_db
from ..models import User as UserModel, Trip as TripModel, Booking as BookingModel, Admin as AdminModel, SecondHandItem as SecondHandItemModel, ErrandTask as ErrandTaskModel
from ..admin_model import AdminCreate, Admin, AdminLogin
from ..auth.admin_auth import get_password_hash, create_admin_access_token, authenticate_admin, get_current_admin
from ..config import Config
from ..cache import cache_manager

router = APIRouter(prefix="/admin")

# 从配置中获取参数
ADMIN_ACCESS_TOKEN_EXPIRE_MINUTES = Config.ADMIN_ACCESS_TOKEN_EXPIRE_MINUTES

@router.post("/login/")
def admin_login(admin: AdminLogin, db: Session = Depends(get_db)):
    try:
        db_admin = authenticate_admin(admin.username, admin.password, db)
        if not db_admin:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="管理员用户名或密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # 更新最后登录时间
        setattr(db_admin, 'last_login', datetime.utcnow())
        db.commit()
        
        access_token_expires = timedelta(minutes=ADMIN_ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_admin_access_token(
            data={"sub": db_admin.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except OperationalError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="数据库连接失败，请稍后重试"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="登录过程中发生错误，请稍后重试"
        )

@router.get("/me", response_model=Admin)
def read_admins_me(current_admin: Admin = Depends(get_current_admin)):
    return Admin(
        id=getattr(current_admin, 'id'),
        username=getattr(current_admin, 'username'),
        email=getattr(current_admin, 'email'),
        role=getattr(current_admin, 'role'),
        created_at=getattr(current_admin, 'created_at'),
        last_login=getattr(current_admin, 'last_login'),
        is_active=getattr(current_admin, 'is_active')
    )

# 管理员用户管理API
@router.get("/users/")
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
    try:
        users = db.query(UserModel).offset(skip).limit(limit).all()
        return users
    except OperationalError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="数据库连接失败，请稍后重试"
        )

# 管理员行程管理API
@router.get("/trips/")
def get_trips(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
    try:
        trips = db.query(TripModel).offset(skip).limit(limit).all()
        return trips
    except OperationalError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="数据库连接失败，请稍后重试"
        )

# 管理员预订管理API
@router.get("/bookings/")
def get_bookings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
    try:
        bookings = db.query(BookingModel).offset(skip).limit(limit).all()
        return bookings
    except OperationalError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="数据库连接失败，请稍后重试"
        )

# 管理员二手交易管理API
@router.get("/secondhand/")
def get_secondhand_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
    try:
        items = db.query(SecondHandItemModel).offset(skip).limit(limit).all()
        return items
    except OperationalError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="数据库连接失败，请稍后重试"
        )

# 管理员跑腿服务管理API
@router.get("/errands/")
def get_errand_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
    try:
        tasks = db.query(ErrandTaskModel).offset(skip).limit(limit).all()
        return tasks
    except OperationalError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="数据库连接失败，请稍后重试"
        )

# 数据统计API（带缓存）
@router.get("/stats/overview")
def get_stats_overview(db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
    # 尝试从缓存获取数据
    cache_key = "admin_stats_overview"
    cached_data = cache_manager.get(cache_key)
    
    if cached_data:
        print("Returning cached stats overview")
        return cached_data
    
    try:
        # 分别查询各项统计数据，避免复杂的联合查询
        
        # 总统计数据
        total_users = db.query(func.count(UserModel.id)).scalar()
        total_trips = db.query(func.count(TripModel.id)).scalar()
        total_bookings = db.query(func.count(BookingModel.id)).scalar()
        total_confirmed = db.query(func.count(BookingModel.id)).filter(BookingModel.status == "confirmed").scalar()
        total_cancelled = db.query(func.count(BookingModel.id)).filter(BookingModel.status == "cancelled").scalar()
        
        # 活跃用户数（30天内有预订的用户）
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        active_users = db.query(func.count(func.distinct(BookingModel.user_id))).filter(
            BookingModel.booked_at >= thirty_days_ago
        ).scalar()
        
        # 今日统计数据
        today = datetime.utcnow().date()
        today_users = db.query(func.count(UserModel.id)).filter(
            func.date(UserModel.created_at) == today
        ).scalar()
        today_trips = db.query(func.count(TripModel.id)).filter(
            func.date(TripModel.departure_time) == today
        ).scalar()
        today_bookings = db.query(func.count(BookingModel.id)).filter(
            func.date(BookingModel.booked_at) == today
        ).scalar()
        
        # 本周统计数据
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        week_users = db.query(func.count(UserModel.id)).filter(
            and_(func.date(UserModel.created_at) >= week_start, func.date(UserModel.created_at) <= week_end)
        ).scalar()
        week_trips = db.query(func.count(TripModel.id)).filter(
            and_(func.date(TripModel.departure_time) >= week_start, func.date(TripModel.departure_time) <= week_end)
        ).scalar()
        week_bookings = db.query(func.count(BookingModel.id)).filter(
            and_(func.date(BookingModel.booked_at) >= week_start, func.date(BookingModel.booked_at) <= week_end)
        ).scalar()
        
        # 本月统计数据
        month_start = today.replace(day=1)
        if today.month == 12:
            month_end = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            month_end = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
            
        month_users = db.query(func.count(UserModel.id)).filter(
            and_(func.date(UserModel.created_at) >= month_start, func.date(UserModel.created_at) <= month_end)
        ).scalar()
        month_trips = db.query(func.count(TripModel.id)).filter(
            and_(func.date(TripModel.departure_time) >= month_start, func.date(TripModel.departure_time) <= month_end)
        ).scalar()
        month_bookings = db.query(func.count(BookingModel.id)).filter(
            and_(func.date(BookingModel.booked_at) >= month_start, func.date(BookingModel.booked_at) <= month_end)
        ).scalar()
        
        # 计算比率
        confirmation_rate = (total_confirmed / total_bookings * 100) if total_bookings and total_bookings > 0 else 0
        cancellation_rate = (total_cancelled / total_bookings * 100) if total_bookings and total_bookings > 0 else 0
        
        result = {
            "overview": {
                "total_users": total_users or 0,
                "total_trips": total_trips or 0,
                "total_bookings": total_bookings or 0,
                "confirmation_rate": round(confirmation_rate, 2),
                "cancellation_rate": round(cancellation_rate, 2),
                "active_users": active_users or 0
            },
            "today": {
                "users": today_users or 0,
                "trips": today_trips or 0,
                "bookings": today_bookings or 0
            },
            "week": {
                "users": week_users or 0,
                "trips": week_trips or 0,
                "bookings": week_bookings or 0
            },
            "month": {
                "users": month_users or 0,
                "trips": month_trips or 0,
                "bookings": month_bookings or 0
            }
        }
        
        # 缓存结果10分钟
        cache_manager.set(cache_key, result, timedelta(minutes=10))
        
        return result
    except OperationalError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="数据库连接失败，请稍后重试"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取统计数据失败: {str(e)}"
        )

# 获取预订趋势数据（用于图表展示，带缓存）
@router.get("/stats/booking-trends")
def get_booking_trends(days: int = 30, db: Session = Depends(get_db), current_admin: AdminModel = Depends(get_current_admin)):
    # 尝试从缓存获取数据
    cache_key = f"admin_booking_trends_{days}"
    cached_data = cache_manager.get(cache_key)
    
    if cached_data:
        print("Returning cached booking trends")
        return cached_data
    
    try:
        # 获取指定天数内的每日预订数据，使用单个查询优化性能
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=days-1)
        
        # 生成日期序列并左连接预订数据
        trends = []
        current_date = start_date
        while current_date <= end_date:
            count = db.query(func.count(BookingModel.id)).filter(
                func.date(BookingModel.booked_at) == current_date
            ).scalar() or 0
            
            trends.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "bookings": count
            })
            current_date += timedelta(days=1)
        
        # 缓存结果5分钟
        cache_manager.set(cache_key, trends, timedelta(minutes=5))
        
        return trends
    except OperationalError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="数据库连接失败，请稍后重试"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取预订趋势数据失败: {str(e)}"
        )

# 获取用户增长趋势数据（带缓存）
@router.get("/stats/user-growth")
def get_user_growth(days: int = 30, db: Session = Depends(get_db), current_admin: AdminModel = Depends(get_current_admin)):
    # 尝试从缓存获取数据
    cache_key = f"admin_user_growth_{days}"
    cached_data = cache_manager.get(cache_key)
    
    if cached_data:
        print("Returning cached user growth")
        return cached_data
    
    try:
        # 获取指定天数内的每日用户增长数据，使用单个查询优化性能
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=days-1)
        
        # 生成日期序列并左连接用户数据
        trends = []
        current_date = start_date
        while current_date <= end_date:
            count = db.query(func.count(UserModel.id)).filter(
                func.date(UserModel.created_at) == current_date
            ).scalar() or 0
            
            trends.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "users": count
            })
            current_date += timedelta(days=1)
        
        # 缓存结果5分钟
        cache_manager.set(cache_key, trends, timedelta(minutes=5))
        
        return trends
    except OperationalError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="数据库连接失败，请稍后重试"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取用户增长数据失败: {str(e)}"
        )