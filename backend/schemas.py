from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    # 添加信誉度字段
    reputation_score: Optional[int] = 100

    class Config:
        from_attributes = True

class TripBase(BaseModel):
    departure: str
    destination: str
    departure_time: datetime
    price_per_person: float
    available_seats: int

class TripCreate(TripBase):
    pass

class Trip(TripBase):
    id: int
    owner_id: int
    owner_name: Optional[str] = None  # 添加发布者姓名字段

    class Config:
        from_attributes = True

# 添加一个用于预订中包含的行程信息的简化模型
class TripInBooking(TripBase):
    id: int
    owner_name: Optional[str] = None

    class Config:
        from_attributes = True

class BookingBase(BaseModel):
    trip_id: int

class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    id: Optional[int] = None
    user_id: Optional[int] = None
    booked_at: Optional[datetime] = None
    # 添加关联的行程信息
    trip: Optional[TripInBooking] = None
    # 添加状态字段，默认为"confirmed"
    status: Optional[str] = "confirmed"

    class Config:
        from_attributes = True

class PaymentBase(BaseModel):
    user_id: int
    amount: float
    status: str

class PaymentCreate(PaymentBase):
    pass

class Payment(PaymentBase):
    id: Optional[int] = None
    payment_date: Optional[datetime] = None

    class Config:
        from_attributes = True

# 添加信誉度记录模型
class ReputationRecordBase(BaseModel):
    score_change: int
    reason: str

class ReputationRecordCreate(ReputationRecordBase):
    user_id: int

class ReputationRecord(ReputationRecordBase):
    id: int
    user_id: int
    recorded_at: datetime

    class Config:
        from_attributes = True