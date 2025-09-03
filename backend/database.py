from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from databases import Database

# 从环境变量中获取数据库配置
DATABASE_URL = "postgresql://postgres:199311@localhost:5432/unigo"

# 创建数据库连接
database = Database(DATABASE_URL)

# SQLAlchemy engine
engine = create_engine(DATABASE_URL)

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