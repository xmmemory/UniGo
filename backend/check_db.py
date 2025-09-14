from database import engine
from sqlalchemy import text

# 检查users表的列
with engine.connect() as conn:
    result = conn.execute(text('SELECT column_name FROM information_schema.columns WHERE table_name = \'users\''))
    columns = [row[0] for row in result]
    print("Users table columns:")
    for col in columns:
        print(f"  - {col}")
        
    # 检查reputation_score列是否存在
    if 'reputation_score' in columns:
        print("\n✓ reputation_score column exists")
    else:
        print("\n✗ reputation_score column does not exist")