from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User
from auth import get_password_hash

# 数据库连接
engine = create_engine("postgresql://postgres:199311@localhost:5432/unigo")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建用户
db = SessionLocal()
try:
    hashed_password = get_password_hash("testpassword")
    db_user = User(username="testuser", email="test@example.com", hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    print("用户创建成功:", db_user)
except Exception as e:
    print("错误:", e)
finally:
    db.close()