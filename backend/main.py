from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import database
from routers import users, trips, bookings, payments

app = FastAPI(
    title="UniGo Student Ride Sharing API",
    description="API for student ride sharing platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await database.connect()

@app.on_event("shutdown")
async def shutdown_event():
    await database.disconnect()

app.include_router(users.router, prefix="/api")
app.include_router(trips.router, prefix="/api")
app.include_router(bookings.router, prefix="/api")
app.include_router(payments.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to UniGo Student Ride Sharing API"}