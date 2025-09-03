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