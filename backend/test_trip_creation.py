import sys
import os
import datetime
sys.path.append(os.path.join(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from database import get_db
from models import Trip

# 获取数据库会话
db_gen = get_db()
db: Session = next(db_gen)

try:
    # 创建测试行程
    departure_time = datetime.datetime.now() + datetime.timedelta(days=1)
    
    trip = Trip(
        departure="北京",
        destination="上海",
        departure_time=departure_time,
        price_per_person=100.0,
        available_seats=4,
        owner_id=7  # testuser2的ID
    )
    
    db.add(trip)
    db.commit()
    db.refresh(trip)
    
    print(f"Trip created successfully: ID {trip.id}, from {trip.departure} to {trip.destination}")
    
except Exception as e:
    print(f"Error creating trip: {str(e)}")
    db.rollback()
finally:
    db.close()