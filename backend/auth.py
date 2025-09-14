import os
import traceback
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from models import User as UserModel
from database import get_db_with_retry
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 从环境变量获取配置，如果没有则使用默认值
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

print(f"Auth SECRET_KEY: {SECRET_KEY}")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login/")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str):
    """
    认证用户，带数据库连接重试机制
    """
    try:
        # 使用带重试机制的数据库连接
        db = get_db_with_retry()
        try:
            user = db.query(UserModel).filter(UserModel.username == username).first()
            if not user:
                return False
            if not verify_password(password, user.hashed_password):
                return False
            return user
        finally:
            db.close()
    except OperationalError as e:
        # 数据库连接失败
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="数据库连接失败，请稍后重试"
        )
    except Exception as e:
        # 打印详细的错误信息
        print(f"认证用户时发生错误: {str(e)}")
        print(f"错误追踪: {traceback.format_exc()}")
        # 其他异常
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="服务器内部错误"
        )

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    print(f"Creating token with SECRET_KEY: {SECRET_KEY}")
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    获取当前用户，带数据库连接重试机制
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        print(f"Decoding token with SECRET_KEY: {SECRET_KEY}")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        print(f"Decoded username: {username}")
        if username is None:
            raise credentials_exception
    except JWTError as e:
        print(f"JWTError: {e}")
        raise credentials_exception
    
    try:
        # 使用带重试机制的数据库连接
        db = get_db_with_retry()
        try:
            user = db.query(UserModel).filter(UserModel.username == username).first()
            print(f"Found user: {user}")
            if user is None:
                raise credentials_exception
            return user
        finally:
            db.close()
    except OperationalError as e:
        # 数据库连接失败
        print(f"OperationalError: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="数据库连接失败，请稍后重试"
        )
    except Exception as e:
        # 其他异常
        print(f"Exception: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="服务器内部错误"
        )