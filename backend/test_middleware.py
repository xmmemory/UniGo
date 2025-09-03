import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from database import get_db
from jose import jwt
from auth import SECRET_KEY, ALGORITHM

# 获取数据库会话
db_gen = get_db()
db: Session = next(db_gen)

try:
    # 测试令牌解码
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlcjIiLCJleHAiOjE3NTY4NzI2MTR9.9vPSIb-9DYaPpEown6qyw8nvT5MCXuhZLWUxrq-7yP0"
    
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    print(f"Decoded username: {username}")
    
    # 查询用户
    from models import User
    user = db.query(User).filter(User.username == username).first()
    if user:
        print(f"User found: {user.username}, ID: {user.id}")
    else:
        print("User not found")
        
except Exception as e:
    print(f"Error during token verification: {str(e)}")
finally:
    db.close()