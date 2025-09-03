import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from database import get_db
from auth import authenticate_user, create_access_token

# 获取数据库会话
db_gen = get_db()
db: Session = next(db_gen)

try:
    # 测试用户认证
    user = authenticate_user(db, "testuser2", "testpass")
    if user:
        print(f"User authenticated: {user.username}")
        
        # 生成访问令牌
        access_token = create_access_token(data={"sub": user.username})
        print(f"Access token: {access_token}")
    else:
        print("Authentication failed")
        
except Exception as e:
    print(f"Error during authentication: {str(e)}")
finally:
    db.close()