import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import Config
from .routers import users, trips, bookings, reputation, admin, chat, secondhand, errands

# 配置日志
log_level = getattr(logging, Config.LOG_LEVEL.upper(), logging.DEBUG)
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 创建logger
logger = logging.getLogger(__name__)

app = FastAPI(
    title="CampusGo Student Ride Sharing API",
    description="API for student ride sharing platform",
    version="1.0.0"
)

# 添加请求日志中间件
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    logger.info(f"Headers: {dict(request.headers)}")
    if request.method in ["POST", "PUT", "PATCH"]:
        body = await request.body()
        logger.info(f"Request body: {body.decode()}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/api/v1")
app.include_router(trips.router, prefix="/api/v1")
app.include_router(bookings.router, prefix="/api/v1")
# 移除支付路由，因为我们不再需要支付功能
# app.include_router(payments.router, prefix="/api/v1")
app.include_router(reputation.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")
app.include_router(secondhand.router, prefix="/api/v1")
app.include_router(errands.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to CampusGo Student Ride Sharing API"}

# Health check endpoint for deployment
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=Config.HOST, port=Config.PORT, reload=Config.DEBUG)