import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import engine
from sqlalchemy import text

# 添加status列到bookings表
try:
    with engine.connect() as conn:
        # 开始事务
        trans = conn.begin()
        try:
            conn.execute(text('ALTER TABLE bookings ADD COLUMN status VARCHAR(20) DEFAULT \'confirmed\''))
            # 提交事务
            trans.commit()
            print('Booking status column added successfully')
        except Exception as e:
            # 回滚事务
            trans.rollback()
            if "already exists" in str(e) or "duplicate column" in str(e):
                print("Column status already exists in bookings table")
            else:
                print(f"Error: {e}")
                raise
except Exception as e:
    print(f"Connection error: {e}")