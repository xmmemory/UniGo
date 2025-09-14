from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, OperationalError
from database import get_db
from models import User as UserModel
from schemas import UserCreate, User, UserLogin
from auth import get_password_hash, create_access_token, authenticate_user, get_current_user
from datetime import timedelta
import os

router = APIRouter()

# 从环境变量获取配置
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

@router.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        hashed_password = get_password_hash(user.password)
        db_user = UserModel(username=user.username, email=user.email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        # 返回Pydantic模型而不是SQLAlchemy模型
        return User(
            id=getattr(db_user, 'id'),
            username=getattr(db_user, 'username'),
            email=getattr(db_user, 'email'),
            created_at=getattr(db_user, 'created_at')
        )
    except IntegrityError as e:
        db.rollback()
        # 检查是用户名还是邮箱重复
        if "users_username_key" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已存在"
            )
        elif "users_email_key" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已存在"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户创建失败"
            )
    except OperationalError as e:
        # 数据库连接失败
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="数据库连接失败，请稍后重试"
        )

@router.post("/login/")
def login(user: UserLogin):
    try:
        # 使用带重试机制的认证函数
        db_user = authenticate_user(user.username, user.password)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": db_user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        # 重新抛出已知的HTTP异常
        raise
    except OperationalError as e:
        # 数据库连接失败
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="数据库连接失败，请稍后重试"
        )
    except Exception as e:
        # 捕获其他所有异常，返回友好的错误信息
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="登录过程中发生错误，请稍后重试"
        )

# 添加刷新token的API端点
@router.post("/refresh-token/")
def refresh_token(current_user: UserModel = Depends(get_current_user)):
    try:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": current_user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="刷新token失败，请稍后重试"
        )

# 添加获取当前用户信息的API端点
@router.get("/users/me", response_model=User)
def read_users_me(current_user: UserModel = Depends(get_current_user)):
    print(f"Current user: {current_user}")
    # 返回Pydantic模型而不是SQLAlchemy模型
    return User(
        id=getattr(current_user, 'id'),
        username=getattr(current_user, 'username'),
        email=getattr(current_user, 'email'),
        created_at=getattr(current_user, 'created_at')
    )

# 添加根据ID获取用户信息的API端点
@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    try:
        db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        # 返回Pydantic模型而不是SQLAlchemy模型
        return User(
            id=getattr(db_user, 'id'),
            username=getattr(db_user, 'username'),
            email=getattr(db_user, 'email'),
            created_at=getattr(db_user, 'created_at')
        )
    except OperationalError as e:
        # 数据库连接失败
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="数据库连接失败，请稍后重试"
        )