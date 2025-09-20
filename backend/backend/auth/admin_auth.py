import os
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from ..models import Admin as AdminModel
from ..database import get_db_with_retry
from ..config import Config
from ..utils.security import get_password_hash
from ..admin_model import Admin

# 从配置中获取参数
ADMIN_SECRET_KEY = Config.ADMIN_SECRET_KEY
ADMIN_ALGORITHM = Config.ADMIN_ALGORITHM
ADMIN_ACCESS_TOKEN_EXPIRE_MINUTES = Config.ADMIN_ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/admin/login/")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_admin(username: str, password: str, db: Session):
    """
    认证管理员
    """
    try:
        admin = db.query(AdminModel).filter(AdminModel.username == username).first()
        if not admin:
            return False
        if not getattr(admin, 'is_active', True):
            return False
        if not verify_password(password, admin.password_hash):
            return False
        return admin
    except Exception as e:
        print(f"认证管理员时发生错误: {str(e)}")
        return False

def create_admin_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, ADMIN_SECRET_KEY, algorithm=ADMIN_ALGORITHM)
    return encoded_jwt

async def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_with_retry)):
    """
    获取当前管理员
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, ADMIN_SECRET_KEY, algorithms=[ADMIN_ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception
    
    try:
        admin = db.query(AdminModel).filter(AdminModel.username == username).first()
        if admin is None:
            raise credentials_exception
        if not getattr(admin, 'is_active', True):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin account is disabled",
            )
        # 返回Admin Pydantic模型而不是SQLAlchemy模型
        return Admin(
            id=getattr(admin, 'id'),
            username=getattr(admin, 'username'),
            email=getattr(admin, 'email'),
            role=getattr(admin, 'role'),
            created_at=getattr(admin, 'created_at'),
            last_login=getattr(admin, 'last_login'),
            is_active=getattr(admin, 'is_active')
        )
    except OperationalError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="数据库连接失败，请稍后重试"
        )