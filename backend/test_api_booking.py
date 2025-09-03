import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from fastapi import FastAPI
from fastapi.testclient import TestClient
from main import app
from sqlalchemy.orm import Session
from database import get_db
from auth import authenticate_user, create_access_token

# 创建测试客户端
client = TestClient(app)

# 获取数据库会话
db_gen = get_db()
db: Session = next(db_gen)

try:
    # 首先认证用户
    user = authenticate_user(db, "testuser2", "testpass")
    if not user:
        print("Authentication failed")
        exit(1)
        
    # 创建访问令牌
    access_token = create_access_token(data={"sub": user.username})
    print(f"Access token: {access_token}")
    
    # 测试创建预订
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    booking_data = {
        "trip_id": 1
    }
    
    response = client.post("/api/bookings/", json=booking_data, headers=headers)
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.json()}")
    
except Exception as e:
    print(f"Error during API test: {str(e)}")
    import traceback
    traceback.print_exc()
finally:
    db.close()