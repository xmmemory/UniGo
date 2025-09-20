# CampusGo Backend - 重构后的目录结构

## 目录结构说明

```
backend/                        # 项目根目录
├── backend/                    # 真正的 Python 包
│   ├── __init__.py
│   ├── main.py                 # 应用主入口（FastAPI/Flask app）
│   ├── config.py               # 配置管理（加载 .env）
│   ├── database.py             # 数据库连接
│   ├── models.py               # ORM 模型
│   ├── schemas.py              # Pydantic 模型
│   ├── auth/                   # 认证与鉴权
│   │   ├── __init__.py
│   │   ├── admin_auth.py       # 管理员认证逻辑
│   │   ├── user_auth.py        # 用户认证逻辑
│   │   └── middleware.py       # 认证中间件
│   ├── routers/                # 路由层
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── bookings.py
│   │   ├── payments.py
│   │   ├── reputation.py
│   │   ├── trips.py
│   │   └── users.py
│   ├── migrations/             # 数据库迁移脚本
│   │   ├── __init__.py
│   │   ├── add_booking_status.py
│   │   └── add_reputation_score.py
│   ├── services/               # 业务逻辑
│   │   ├── __init__.py
│   │   └── booking_service.py  # 示例
│   └── utils/                  # 工具模块
│       ├── __init__.py
│       ├── security.py         # JWT/密码哈希函数
│       └── logger.py           # （可选：日志配置）
├── tests/                      # 单元测试
│   ├── __init__.py
│   └── test_users.py
├── .env
├── .env.example
├── requirements.txt
├── run.py                      # 启动脚本，调用 uvicorn backend.main:app
└── start.sh
```

## 重构说明

### 1. 双层 backend/ 结构
- 外层 backend/：项目根目录，放配置文件、依赖文件、脚本
- 内层 backend/：真正的 Python 包

### 2. 分层设计
- `routers/`：只负责 HTTP 路由和请求响应
- `services/`：封装业务逻辑，便于测试和复用
- `models.py` + `schemas.py`：一个负责数据库 ORM，一个负责数据验证
- `auth/`：认证和权限相关逻辑单独放置
- `utils/`：工具类函数，如加密、日志、配置

### 3. 配置管理
- 用 `config.py` 统一读取 .env，避免在多个文件重复解析环境变量

### 4. 测试目录
- `tests/` 目录存放单元测试文件，方便 CI/CD 集成

## 启动应用

```bash
# 使用 run.py 启动
python run.py

# 或者直接使用 uvicorn 启动
uvicorn backend.main:app --host 0.0.0.0 --port 8001 --reload
```

## 数据库初始化

```bash
# 初始化数据库
python -m backend.init_db

# 创建初始管理员账号
python -m backend.init_admin
```