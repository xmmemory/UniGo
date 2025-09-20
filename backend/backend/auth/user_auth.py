import os
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from ..models import User as UserModel
from ..database import get_db_with_retry, get_db
from ..config import Config
from ..utils.security import get_password_hash, create_access_token, create_refresh_token, decode_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login/")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str):
    """
    认证用户
    """
    db = None
    try:
        print(f"Authenticating user: {username}")
        db = get_db_with_retry()
        user = db.query(UserModel).filter(UserModel.username == username).first()
        print(f"User found: {user}")
        if not user:
            print(f"User {username} not found in database")
            return False
        print(f"Verifying password for user: {username}")
        password_verified = verify_password(password, user.hashed_password)
        print(f"Password verification result: {password_verified}")
        if not password_verified:
            return False
        return user
    except Exception as e:
        print(f"认证用户时发生错误: {str(e)}")
        return False
    finally:
        if db:
            db.close()


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    获取当前用户
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        username = payload.get("sub")
        token_type = payload.get("type", "access")
        
        # 检查令牌类型
        if token_type != "access":
            raise credentials_exception
            
        if username is None:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception
    
    try:
        user = db.query(UserModel).filter(UserModel.username == username).first()
        if user is None:
            raise credentials_exception
        return user
    except OperationalError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="数据库连接失败，请稍后重试"
        )


async def get_current_user_from_refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    """
    从刷新令牌获取当前用户
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(refresh_token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        username = payload.get("sub")
        token_type = payload.get("type", "access")
        
        # 检查令牌类型
        if token_type != "refresh":
            raise credentials_exception
            
        if username is None:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception
    
    try:
        user = db.query(UserModel).filter(UserModel.username == username).first()
        if user is None:
            raise credentials_exception
        return user
    except OperationalError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="数据库连接失败，请稍后重试"
        )
