from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, OperationalError
from pydantic import ValidationError
from ..database import get_db
from ..models import User as UserModel
from ..schemas import UserCreate, User, UserLogin
from ..auth.user_auth import get_password_hash, create_access_token, authenticate_user, get_current_user, get_current_user_from_refresh_token
from ..config import Config
from ..utils.security import create_refresh_token
from datetime import timedelta
import os

router = APIRouter()

# 从配置中获取参数
ACCESS_TOKEN_EXPIRE_MINUTES = Config.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = 7

@router.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        print(f"=== 创建用户开始 ===")
        print(f"用户数据: {user.dict()}")
        
        # 验证密码强度
        try:
            print(f"验证密码强度: {user.password}")
            user.validate_password_strength(user.password)
            print("密码强度验证通过")
        except ValueError as e:
            print(f"密码强度验证失败: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        
        print("生成密码哈希")
        hashed_password = get_password_hash(user.password)
        print("创建用户对象")
        db_user = UserModel(username=user.username, email=user.email, hashed_password=hashed_password)
        print("添加用户到数据库")
        db.add(db_user)
        print("提交事务")
        db.commit()
        print("刷新用户对象")
        db.refresh(db_user)
        print("返回用户信息")
        # 返回Pydantic模型而不是SQLAlchemy模型
        result = User(
            id=getattr(db_user, 'id'),
            username=getattr(db_user, 'username'),
            email=getattr(db_user, 'email'),
            created_at=getattr(db_user, 'created_at')
        )
        print(f"返回结果: {result}")
        return result
    except IntegrityError as e:
        print(f"完整性错误: {str(e)}")
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
        print(f"数据库操作错误: {str(e)}")
        # 数据库连接失败
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="数据库连接失败，请稍后重试"
        )
    except ValidationError as e:
        print(f"验证错误: {e.errors()}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.errors()[0]['msg']
        )
    except Exception as e:
        print(f"创建用户时发生未知错误: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建用户时发生错误"
        )

@router.post("/login/")
def login(user: UserLogin):
    try:
        print(f"Login attempt for username: {user.username}")
        # 使用带重试机制的认证函数
        db_user = authenticate_user(user.username, user.password)
        print(f"Authentication result: {db_user}")
        if not db_user:
            print(f"Authentication failed for user: {user.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        
        access_token = create_access_token(
            data={"sub": db_user.username}, expires_delta=access_token_expires
        )
        
        refresh_token = create_refresh_token(
            data={"sub": db_user.username}, expires_delta=refresh_token_expires
        )
        
        print(f"Login successful for user: {user.username}")
        return {
            "access_token": access_token, 
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
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
        print(f"Unexpected error during login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="登录过程中发生错误，请稍后重试"
        )

# 添加刷新token的API端点
@router.post("/refresh-token/")
def refresh_token(current_user: UserModel = Depends(get_current_user_from_refresh_token)):
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