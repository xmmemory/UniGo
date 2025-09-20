from sqlalchemy.orm import Session
from ..models import Booking as BookingModel

class BookingService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_bookings(self, skip: int = 0, limit: int = 100):
        return self.db.query(BookingModel).offset(skip).limit(limit).all()
    
    def get_booking_by_id(self, booking_id: int):
        return self.db.query(BookingModel).filter(BookingModel.id == booking_id).first()