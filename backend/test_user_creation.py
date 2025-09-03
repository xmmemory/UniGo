import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from database import get_db, init_db
from models import User as UserModel
from auth import get_password_hash
from schemas import UserCreate

# 初始化数据库
init_db()

# 获取数据库会话
db_gen = get_db()
db: Session = next(db_gen)

try:
    # 创建测试用户
    user_data = UserCreate(
        username="testuser2",
        email="test2@example.com",
        password="testpass"
    )
    
    hashed_password = get_password_hash(user_data.password)
    db_user = UserModel(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    print(f"User created successfully: {db_user.username}, ID: {db_user.id}")
    
except Exception as e:
    print(f"Error creating user: {str(e)}")
    db.rollback()
finally:
    db.close()