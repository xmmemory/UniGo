from sqlalchemy import create_engine, inspect
from database import Base

# 数据库连接
engine = create_engine("postgresql://postgres:199311@localhost:5432/unigo")

# 检查 users 表结构
inspector = inspect(engine)
columns = inspector.get_columns("users")

print("Users 表结构：")
for column in columns:
    print(column)