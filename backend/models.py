from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, func
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    # 添加信誉度字段，默认为100分
    reputation_score = Column(Integer, nullable=False, default=100)
    
    trips = relationship("Trip", back_populates="owner")
    bookings = relationship("Booking", back_populates="user")
    reputation_records = relationship("ReputationRecord", back_populates="user")

class Trip(Base):
    __tablename__ = 'trips'
    
    id = Column(Integer, primary_key=True)
    departure = Column(String(100), nullable=False)
    destination = Column(String(100), nullable=False)
    departure_time = Column(DateTime, nullable=False)
    price_per_person = Column(Float, nullable=False)
    available_seats = Column(Integer, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    owner = relationship("User", back_populates="trips")
    bookings = relationship("Booking", back_populates="trip")

class Booking(Base):
    __tablename__ = 'bookings'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    trip_id = Column(Integer, ForeignKey('trips.id'), nullable=False)
    booked_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    # 添加状态字段，默认为"confirmed"
    status = Column(String(20), nullable=False, default="confirmed")
    
    user = relationship("User", back_populates="bookings")
    trip = relationship("Trip", back_populates="bookings")

class Payment(Base):
    __tablename__ = 'payments'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    status = Column(String(20), nullable=False)
    
    user = relationship("User")

# 添加信誉度记录模型
class ReputationRecord(Base):
    __tablename__ = 'reputation_records'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    # 变化分数（正数表示加分，负数表示扣分）
    score_change = Column(Integer, nullable=False)
    # 变化原因
    reason = Column(String(200), nullable=False)
    # 记录时间
    recorded_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    user = relationship("User", back_populates="reputation_records")