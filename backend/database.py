import os
import time
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 从环境变量中获取数据库配置，如果没有则使用默认值
# 使用云端PostgreSQL数据库，地址为101.32.244.111
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:199311@101.32.244.111:5432/unigo")

# SQLAlchemy engine with connection pooling and retry configuration
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # 验证连接是否有效
    pool_recycle=3600,   # 1小时后回收连接
    connect_args={
        "connect_timeout": 10,
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5,
    }
)

# 创建数据库表
Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)

# 数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_with_retry(max_retries=3, retry_delay=1):
    """
    获取数据库会话，带重试机制
    """
    for attempt in range(max_retries):
        try:
            db = SessionLocal()
            # 测试连接是否有效
            db.execute(text("SELECT 1"))
            return db
        except OperationalError as e:
            if attempt < max_retries - 1:
                print(f"数据库连接失败，{retry_delay}秒后重试... (尝试 {attempt + 1}/{max_retries})")
                time.sleep(retry_delay)
                retry_delay *= 2  # 指数退避
            else:
                raise e
        except Exception as e:
            if 'db' in locals():
                db.close()
            raise e
    
    # 如果所有重试都失败，抛出异常
    raise OperationalError("数据库连接失败，已达到最大重试次数", None, None)