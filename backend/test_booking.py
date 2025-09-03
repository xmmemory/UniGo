import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from database import get_db
from models import Booking

# 获取数据库会话
db_gen = get_db()
db: Session = next(db_gen)

try:
    # 创建测试预订
    booking = Booking(
        user_id=7,  # testuser2的ID
        trip_id=1   # 我们之前创建的行程ID
    )
    
    db.add(booking)
    db.commit()
    db.refresh(booking)
    
    print(f"Booking created successfully: ID {booking.id}")
    
except Exception as e:
    print(f"Error creating booking: {str(e)}")
    import traceback
    traceback.print_exc()
    db.rollback()
finally:
    db.close()