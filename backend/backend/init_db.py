from backend.database import init_db
from backend.models import Base, User, Trip, Booking, Admin, SecondHandItem, ErrandTask, ErrandResponse, ChatMessage, ReputationRecord

if __name__ == "__main__":
    init_db()
    print("Database tables created successfully.")