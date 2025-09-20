import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import DATABASE_URL

def add_reputation_column():
    # 创建数据库引擎
    engine = create_engine(DATABASE_URL)
    
    # 添加reputation_score列到users表
    with engine.connect() as conn:
        try:
            # 使用ALTER TABLE语句添加列
            conn.execute(text("ALTER TABLE users ADD COLUMN reputation_score INTEGER DEFAULT 100"))
            print("Successfully added reputation_score column to users table")
        except Exception as e:
            if "already exists" in str(e) or "duplicate column" in str(e):
                print("Column reputation_score already exists in users table")
            else:
                print(f"Error adding reputation_score column: {e}")
                raise

if __name__ == "__main__":
    add_reputation_column()