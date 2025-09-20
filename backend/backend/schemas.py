from pydantic import BaseModel, validator, Field
from typing import Optional, List, TypeVar, Generic
from datetime import datetime
import re

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: str = Field(..., regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

    @validator('username')
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('用户名只能包含字母、数字和下划线')
        return v

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

    @validator('password')
    def validate_password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('密码长度至少为8个字符')
        if not re.search(r'[A-Z]', v):
            raise ValueError('密码必须包含至少一个大写字母')
        if not re.search(r'[a-z]', v):
            raise ValueError('密码必须包含至少一个小写字母')
        if not re.search(r'\d', v):
            raise ValueError('密码必须包含至少一个数字')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('密码必须包含至少一个特殊字符')
        return v

class UserLogin(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)

class User(UserBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    # 添加信誉度字段
    reputation_score: Optional[int] = 100

    class Config:
        orm_mode = True

class TripBase(BaseModel):
    departure: str = Field(..., min_length=1, max_length=100)
    destination: str = Field(..., min_length=1, max_length=100)
    departure_time: datetime
    price_per_person: float = Field(..., gt=0)
    available_seats: int = Field(..., gt=0, le=10)

    @validator('departure', 'destination')
    def validate_location(cls, v):
        if not re.match(r'^[\u4e00-\u9fa5a-zA-Z0-9\s\-]+$', v):
            raise ValueError('地点只能包含中文、英文字母、数字、空格和连字符')
        return v

class TripCreate(TripBase):
    pass

class Trip(TripBase):
    id: int
    owner_id: int
    owner_name: Optional[str] = None  # 添加发布者姓名字段

    class Config:
        orm_mode = True

# 添加一个用于预订中包含的行程信息的简化模型
class TripInBooking(TripBase):
    id: int
    owner_name: Optional[str] = None

    class Config:
        orm_mode = True

class BookingBase(BaseModel):
    trip_id: int = Field(..., gt=0)

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
        orm_mode = True

# 移除Payment相关的模型，因为我们不再需要支付功能

# 添加信誉度记录模型
class ReputationRecordBase(BaseModel):
    score_change: int = Field(..., ge=-100, le=100)
    reason: str = Field(..., min_length=1, max_length=200)

class ReputationRecordCreate(ReputationRecordBase):
    user_id: int = Field(..., gt=0)

class ReputationRecord(ReputationRecordBase):
    id: int
    user_id: int
    recorded_at: datetime

    class Config:
        orm_mode = True

# 聊天消息模型
class ChatMessageBase(BaseModel):
    trip_id: int = Field(..., gt=0)
    content: str = Field(..., min_length=1, max_length=1000)
    message_type: str = Field("text", regex=r'^(text|image|file)$')

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessage(ChatMessageBase):
    id: int
    sender_id: int
    timestamp: datetime

    class Config:
        orm_mode = True

class ChatMessageResponse(BaseModel):
    id: int
    trip_id: int
    sender_id: int
    content: str
    timestamp: datetime
    message_type: str
    sender_username: str

    class Config:
        orm_mode = True

# 二手交易模型
class SecondHandItemBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=1000)
    price: float = Field(..., ge=0)
    category: str = Field(..., min_length=1, max_length=50)  # 商品分类
    condition: str = Field(..., min_length=1, max_length=20)  # 商品状态

class SecondHandItemCreate(SecondHandItemBase):
    pass

class SecondHandItem(SecondHandItemBase):
    id: int
    owner_id: int
    owner_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

# 跑腿任务模型
class ErrandTaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=1000)
    reward: float = Field(..., ge=0)  # 酬劳
    location: str = Field(..., min_length=1, max_length=100)  # 任务地点
    deadline: datetime  # 截止时间

class ErrandTaskCreate(ErrandTaskBase):
    pass

class ErrandTask(ErrandTaskBase):
    id: int
    owner_id: int
    owner_name: Optional[str] = None
    assignee_id: Optional[int] = None
    assignee_name: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    status: str = "open"  # 任务状态

    class Config:
        orm_mode = True

# 跑腿任务响应模型
class ErrandResponseBase(BaseModel):
    task_id: int = Field(..., gt=0)
    message: Optional[str] = Field(None, max_length=500)  # 响应消息

class ErrandResponseCreate(ErrandResponseBase):
    pass

class ErrandResponse(ErrandResponseBase):
    id: int
    user_id: int
    user_name: Optional[str] = None
    created_at: datetime
    is_accepted: bool

    class Config:
        orm_mode = True

# 添加用于返回任务列表和总数的模型
class ErrandTaskListResponse(BaseModel):
    tasks: list[ErrandTask]
    total: int
    page: int
    total_pages: int
    limit: int

    class Config:
        orm_mode = True

# 分页响应模型
T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    total_pages: int
    limit: int
