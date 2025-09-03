from database import init_db
from models import Base, User, Trip, Booking, Payment

if __name__ == "__main__":
    init_db()
    print("Database tables created successfully.")