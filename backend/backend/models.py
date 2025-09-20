from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, func, Boolean, Index, Text
from sqlalchemy.orm import relationship
from .database import Base
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
    # 添加聊天消息关系
    sent_messages = relationship("ChatMessage", back_populates="sender")
    # 二手交易关系
    items_for_sale = relationship("SecondHandItem", back_populates="owner")
    # 跑腿服务关系
    errand_tasks = relationship("ErrandTask", back_populates="owner", foreign_keys="ErrandTask.owner_id")
    errand_responses = relationship("ErrandResponse", back_populates="user")
    
    # 添加索引
    __table_args__ = (
        Index('ix_users_username', 'username'),
        Index('ix_users_email', 'email'),
        Index('ix_users_created_at', 'created_at'),
    )

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
    
    # 添加索引
    __table_args__ = (
        Index('ix_trips_owner_id', 'owner_id'),
        Index('ix_trips_departure_time', 'departure_time'),
        Index('ix_trips_departure', 'departure'),
        Index('ix_trips_destination', 'destination'),
    )

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
    
    # 添加索引
    __table_args__ = (
        Index('ix_bookings_user_id', 'user_id'),
        Index('ix_bookings_trip_id', 'trip_id'),
        Index('ix_bookings_booked_at', 'booked_at'),
        Index('ix_bookings_status', 'status'),
    )

# 移除Payment类，因为我们不再需要支付功能

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
    
    # 添加索引
    __table_args__ = (
        Index('ix_reputation_records_user_id', 'user_id'),
        Index('ix_reputation_records_recorded_at', 'recorded_at'),
    )

# 管理员模型
class Admin(Base):
    __tablename__ = 'admins'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False, default="admin")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    
    # 添加索引
    __table_args__ = (
        Index('ix_admins_username', 'username'),
        Index('ix_admins_email', 'email'),
        Index('ix_admins_created_at', 'created_at'),
    )

# 聊天消息模型
class ChatMessage(Base):
    __tablename__ = 'chat_messages'
    
    id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, ForeignKey('trips.id'), nullable=False)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    # 消息类型（text, image, etc.）
    message_type = Column(String(20), nullable=False, default="text")
    
    # 关系
    trip = relationship("Trip")
    sender = relationship("User", back_populates="sent_messages")
    
    # 添加索引
    __table_args__ = (
        Index('ix_chat_messages_trip_id', 'trip_id'),
        Index('ix_chat_messages_sender_id', 'sender_id'),
        Index('ix_chat_messages_timestamp', 'timestamp'),
    )

# 二手交易模型
class SecondHandItem(Base):
    __tablename__ = 'second_hand_items'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)  # 商品分类（如：书籍、电子产品、衣物等）
    condition = Column(String(20), nullable=False)  # 商品状态（如：全新、良好、一般等）
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    is_active = Column(Boolean, nullable=False, default=True)  # 是否仍在售卖
    
    # 关系
    owner = relationship("User", back_populates="items_for_sale")
    
    # 添加索引
    __table_args__ = (
        Index('ix_second_hand_items_owner_id', 'owner_id'),
        Index('ix_second_hand_items_category', 'category'),
        Index('ix_second_hand_items_created_at', 'created_at'),
        Index('ix_second_hand_items_is_active', 'is_active'),
    )

# 跑腿任务模型
class ErrandTask(Base):
    __tablename__ = 'errand_tasks'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    reward = Column(Float, nullable=False)  # 酬劳
    location = Column(String(100), nullable=False)  # 任务地点
    deadline = Column(DateTime, nullable=False)  # 截止时间
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    assignee_id = Column(Integer, ForeignKey('users.id'), nullable=True)  # 接取任务的用户
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    status = Column(String(20), nullable=False, default="open")  # 任务状态（open, in_progress, completed, cancelled）
    
    # 关系
    owner = relationship("User", foreign_keys=[owner_id], back_populates="errand_tasks")
    assignee = relationship("User", foreign_keys=[assignee_id])
    responses = relationship("ErrandResponse", back_populates="task")
    
    # 添加索引
    __table_args__ = (
        Index('ix_errand_tasks_owner_id', 'owner_id'),
        Index('ix_errand_tasks_assignee_id', 'assignee_id'),
        Index('ix_errand_tasks_created_at', 'created_at'),
        Index('ix_errand_tasks_status', 'status'),
        Index('ix_errand_tasks_deadline', 'deadline'),
    )

# 跑腿任务响应模型
class ErrandResponse(Base):
    __tablename__ = 'errand_responses'
    
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('errand_tasks.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    message = Column(Text, nullable=True)  # 响应消息
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    is_accepted = Column(Boolean, nullable=False, default=False)  # 是否被接受
    
    # 关系
    task = relationship("ErrandTask", back_populates="responses")
    user = relationship("User", back_populates="errand_responses")
    
    # 添加索引
    __table_args__ = (
        Index('ix_errand_responses_task_id', 'task_id'),
        Index('ix_errand_responses_user_id', 'user_id'),
        Index('ix_errand_responses_created_at', 'created_at'),
        Index('ix_errand_responses_is_accepted', 'is_accepted'),
    )