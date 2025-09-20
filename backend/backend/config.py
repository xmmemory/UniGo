import os
from dotenv import load_dotenv

# 根据环境变量加载不同的配置文件
env = os.getenv('APP_ENV', 'development')
if env == 'production':
    load_dotenv('.env.production')
else:
    load_dotenv('.env.development')

class Config:
    # Database configuration
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://app_user:199311@101.32.244.111:5432/campusgo")
    
    # JWT configuration
    SECRET_KEY = os.getenv("SECRET_KEY", "Mn4OteEHchuv6Al5WK7ly7YrZ2FNLkqloEipCVysk1M")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    
    # Admin JWT configuration
    ADMIN_SECRET_KEY = os.getenv("ADMIN_SECRET_KEY", "your-admin-secret-key-here")
    ADMIN_ALGORITHM = os.getenv("ADMIN_ALGORITHM", "HS256")
    ADMIN_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ADMIN_ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    
    # Redis configuration
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB = int(os.getenv("REDIS_DB", 0))
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
    
    # Server configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8001))
    
    # Debug configuration
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")