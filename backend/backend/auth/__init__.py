# Authentication package initializer

# 从admin_auth模块导出管理员认证相关函数
from .admin_auth import (
    get_password_hash as get_admin_password_hash,
    create_admin_access_token,
    authenticate_admin,
    get_current_admin
)

# 从user_auth模块导出用户认证相关函数
from .user_auth import (
    get_password_hash,
    create_access_token,
    authenticate_user,
    get_current_user
)

# 从middleware模块导出中间件函数
from .middleware import verify_token

__all__ = [
    "get_admin_password_hash",
    "create_admin_access_token",
    "authenticate_admin",
    "get_current_admin",
    "get_password_hash",
    "create_access_token",
    "authenticate_user",
    "get_current_user",
    "verify_token"
]