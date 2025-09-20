# CampusGo 学生综合服务平台

## 项目简介
CampusGo 是一个专为学生设计的综合服务平台，包含拼车、二手交易和校内跑腿服务，旨在帮助学生更方便、经济地校园生活。

## 功能特性
- 用户注册与登录（支持密码强度验证）
- 行程发布与搜索（拼车服务）
- 行程预订与管理
- 实时聊天功能（行程参与者之间沟通）
- 二手商品交易（发布、搜索、购买）
- 校内跑腿服务（发布任务、接取任务）
- 个人中心管理
- 管理员后台管理（数据统计、用户管理等）
- 会话管理（JWT双令牌机制：访问令牌+刷新令牌）

## 技术栈
- 前端：Vue 3 + TypeScript + Vite
- 后端：FastAPI (Python)
- 数据库：PostgreSQL
- 缓存：Redis
- 实时通信：WebSocket

## 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- PostgreSQL (使用云端数据库，无需本地安装)
- Redis (用于缓存)

### 一键启动（推荐）
```bash
# 使用start.sh脚本同时启动前后端服务（Linux/Mac）
./start.sh

# Windows用户可以分别启动前后端服务
```

### 后端启动
```bash
cd backend
# 创建虚拟环境
python -m venv venv
# 激活虚拟环境
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python init_db.py

# 初始化管理员账号
python init_admin.py

# 启动服务
python run.py
```

### 前端启动
```bash
cd frontend
# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 访问地址
- 前端：http://localhost:5173
- 后端API文档：http://localhost:8001/docs
- 管理员后台：http://localhost:5173/admin/login

## 项目结构

### 后端结构
```
backend/
├── backend/                    # 真正的 Python 包
│   ├── main.py                 # 应用主入口
│   ├── config.py               # 配置管理
│   ├── database.py             # 数据库连接
│   ├── models.py               # ORM 模型
│   ├── schemas.py              # Pydantic 模型
│   ├── auth/                   # 认证与鉴权
│   ├── routers/                # 路由层
│   ├── migrations/             # 数据库迁移脚本
│   ├── services/               # 业务逻辑
│   └── utils/                  # 工具模块
├── tests/                      # 单元测试
├── requirements.txt            # 依赖列表
└── run.py                      # 启动脚本
```

### 前端结构
```
frontend/
├── src/
│   ├── main.ts                 # 应用入口
│   ├── App.vue                 # 根组件
│   ├── router/                 # 路由配置
│   ├── stores/                 # 状态管理
│   ├── views/                  # 页面组件
│   ├── components/             # 可复用组件
│   ├── api/                    # API调用封装
│   ├── services/               # 业务服务
│   ├── utils/                  # 工具函数
│   └── assets/                 # 静态资源
├── public/                     # 公共文件
└── index.html                  # HTML模板
```

## API 端点

### 用户相关
- `POST /api/v1/users/` - 注册用户
- `POST /api/v1/login/` - 用户登录
- `POST /api/v1/refresh-token/` - 刷新访问令牌
- `GET /api/v1/users/me` - 获取当前用户信息
- `GET /api/v1/users/{user_id}` - 根据ID获取用户信息

### 行程相关
- `GET /api/v1/trips/all/` - 获取所有行程（需要认证，带分页）
- `GET /api/v1/trips/public/all/` - 获取公开行程（无需认证）
- `GET /api/v1/trips/{trip_id}` - 获取特定行程详情
- `POST /api/v1/trips/` - 创建新行程

### 预订相关
- `GET /api/v1/bookings/` - 获取用户的所有预订（带分页）
- `GET /api/v1/bookings/{booking_id}` - 获取特定预订详情
- `POST /api/v1/bookings/` - 创建新预订
- `DELETE /api/v1/bookings/{booking_id}` - 取消预订

### 聊天相关
- `GET /api/v1/chat/messages/{trip_id}` - 获取聊天历史记录
- `POST /api/v1/chat/messages/` - 发送聊天消息

### 二手交易相关
- `GET /api/v1/secondhand?page={page}&limit={limit}` - 获取二手商品列表
- `GET /api/v1/secondhand/{id}` - 获取二手商品详情
- `POST /api/v1/secondhand` - 创建二手商品
- `PUT /api/v1/secondhand/{id}` - 更新二手商品
- `DELETE /api/v1/secondhand/{id}` - 删除二手商品
- `GET /api/v1/secondhand/search?keyword={keyword}` - 搜索二手商品

### 跑腿服务相关
- `GET /api/v1/errands?page={page}&limit={limit}` - 获取跑腿任务列表
- `GET /api/v1/errands/{id}` - 获取跑腿任务详情
- `POST /api/v1/errands` - 创建跑腿任务
- `PUT /api/v1/errands/{id}` - 更新跑腿任务
- `DELETE /api/v1/errands/{id}` - 删除跑腿任务
- `POST /api/v1/errands/{id}/accept` - 接取跑腿任务
- `POST /api/v1/errands/{id}/complete` - 完成跑腿任务
- `POST /api/v1/errands/{id}/cancel` - 取消跑腿任务
- `GET /api/v1/errands/search?keyword={keyword}` - 搜索跑腿任务

### 管理员相关
- `POST /api/v1/admin/login/` - 管理员登录
- `GET /api/v1/admin/me` - 获取当前管理员信息
- `GET /api/v1/admin/users/` - 获取用户列表
- `GET /api/v1/admin/trips/` - 获取行程列表
- `GET /api/v1/admin/bookings/` - 获取预订列表
- `GET /api/v1/admin/stats/overview` - 获取统计概览数据
- `GET /api/v1/admin/stats/booking-trends` - 获取预订趋势数据
- `GET /api/v1/admin/stats/user-growth` - 获取用户增长数据

## 管理员后台
系统包含独立的管理员后台，具有以下功能：
- 用户管理：查看、编辑用户信息，调整用户状态和信誉度
- 行程管理：查看所有行程，管理异常行程
- 预订管理：查看所有预订，处理争议
- 数据统计：查看平台运营数据（默认显示页面）
- 系统设置：管理员账号管理，系统参数配置

默认管理员账号：
- 用户名：admin
- 密码：admin123（生产环境请务必修改）

## 数据模型

### 用户(User)
- id: Integer (主键)
- username: String (唯一)
- email: String (唯一)
- hashed_password: String
- created_at: DateTime
- reputation_score: Integer (信誉度分数)

### 管理员(Admin)
- id: Integer (主键)
- username: String (唯一)
- email: String (唯一)
- password_hash: String
- role: String (角色)
- created_at: DateTime
- last_login: DateTime
- is_active: Boolean

### 行程(Trip)
- id: Integer (主键)
- departure: String (出发地)
- destination: String (目的地)
- departure_time: DateTime (出发时间)
- price_per_person: Float (每人价格)
- available_seats: Integer (可用座位数)
- owner_id: Integer (外键，关联用户)

### 预订(Booking)
- id: Integer (主键)
- user_id: Integer (外键，关联用户)
- trip_id: Integer (外键，关联行程)
- booked_at: DateTime (预订时间)
- status: String (状态)

### 聊天消息(ChatMessage)
- id: Integer (主键)
- trip_id: Integer (外键，关联行程)
- sender_id: Integer (外键，关联用户)
- content: Text (消息内容)
- message_type: String (消息类型：text/image)
- timestamp: DateTime (时间戳)

### 信誉度记录(ReputationRecord)
- id: Integer (主键)
- user_id: Integer (外键，关联用户)
- score_change: Integer (分数变化)
- reason: String (变化原因)
- recorded_at: DateTime (记录时间)

### 二手商品(SecondHandItem)
- id: Integer (主键)
- title: String (标题)
- description: Text (描述)
- price: Float (价格)
- category: String (分类)
- image_url: String (图片URL)
- owner_id: Integer (外键，关联用户)
- status: String (状态：available/sold)
- created_at: DateTime

### 跑腿任务(ErrandTask)
- id: Integer (主键)
- title: String (标题)
- description: Text (描述)
- reward: Float (报酬)
- location: String (地点)
- deadline: DateTime (截止时间)
- status: String (状态：open/accepted/completed/cancelled)
- poster_id: Integer (发布者ID，外键关联用户)
- accepter_id: Integer (接取者ID，外键关联用户，可为空)
- created_at: DateTime
- updated_at: DateTime

## 安全性

### 认证与授权
- 使用JWT Token进行用户身份验证（双令牌机制）
- 敏感操作需要相应的权限验证
- 密码使用bcrypt进行哈希存储
- 密码强度验证（至少8位，包含大小写字母、数字和特殊字符）
- 输入验证（前后端双重验证）

### 数据安全
- 数据库连接使用SSL加密
- 敏感信息不直接暴露给前端
- API接口有适当的输入验证
- Redis缓存使用密码保护

## 性能优化

### 数据库优化
- 为常用查询字段添加索引
- 使用分页减少单次查询数据量
- 优化复杂查询逻辑

### API优化
- 实现Redis缓存机制，提高常用数据访问速度
- 减少不必要的数据传输
- 优化API响应速度

### 前端优化
- 代码分割和懒加载
- 组件复用和优化

## 错误处理

### 前端错误处理
- 网络错误：提示用户检查网络连接
- 认证错误：自动跳转到登录页面
- 业务错误：显示具体的错误信息
- 输入验证错误：实时提示用户修正

### 后端错误处理
- 400：请求参数错误
- 401：未认证或认证失败
- 403：权限不足
- 404：资源不存在
- 500：服务器内部错误

## 测试账号

- 用户名：18810871613
- 密码：Test1234!

## 开发规范

### 代码规范
- 后端遵循PEP 8 Python编码规范
- 前端遵循Vue.js风格指南
- 变量命名清晰且具有描述性

### 提交规范
- 使用语义化提交信息
- 每次提交只包含一个功能或修复
- 提交前进行代码审查

## 常见问题