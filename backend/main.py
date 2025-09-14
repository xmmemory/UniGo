import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Comment out database related imports and code for now
# from database import database
from routers import users, trips, bookings, payments, reputation

# 从环境变量获取配置
host = os.getenv("HOST", "0.0.0.0")
port = int(os.getenv("PORT", 8001))

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

# Comment out database connection for now
# @app.on_event("startup")
# async def startup_event():
#     await database.connect()

# @app.on_event("shutdown")
# async def shutdown_event():
#     await database.disconnect()

app.include_router(users.router, prefix="/api")
app.include_router(trips.router, prefix="/api")
app.include_router(bookings.router, prefix="/api")
app.include_router(payments.router, prefix="/api")
app.include_router(reputation.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to UniGo Student Ride Sharing API"}

# Health check endpoint for deployment
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=host, port=port)