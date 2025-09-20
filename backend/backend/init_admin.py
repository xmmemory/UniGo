"""
管理员账号初始化脚本
运行此脚本创建初始管理员账号
"""

from .database import get_db_with_retry
from .models import Admin
from .auth.admin_auth import get_password_hash
from .config import Config
import os

def create_admin_user():
    """创建初始管理员账号"""
    # 获取数据库会话
    db = get_db_with_retry()
    
    try:
        # 检查是否已存在管理员账号
        existing_admin = db.query(Admin).filter(Admin.username == "admin").first()
        if existing_admin:
            print("管理员账号已存在")
            return
        
        # 创建管理员账号
        admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
        hashed_password = get_password_hash(admin_password)
        
        admin = Admin(
            username="admin",
            email="admin@unigo.com",
            password_hash=hashed_password,
            role="super_admin"
        )
        
        db.add(admin)
        db.commit()
        db.refresh(admin)
        
        print(f"管理员账号创建成功!")
        print(f"用户名: admin")
        print(f"密码: {admin_password}")
        print("请务必在生产环境中修改默认密码!")
        
    except Exception as e:
        print(f"创建管理员账号时发生错误: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()