# UniGo 学生拼车平台

## 项目简介

UniGo是一个专为大学生设计的拼车平台，旨在解决校园内外的出行需求。通过该平台，学生可以发布自己的行程信息或预订他人的行程，实现资源共享和成本分摊。

## 功能特性

### 用户管理
- **用户注册**：新用户可以通过填写用户名、邮箱和密码进行注册
- **用户登录**：支持用户名/密码登录，采用JWT Token进行身份验证
- **个人信息管理**：用户可以查看和编辑个人资料
- **退出登录**：安全退出系统

### 行程管理
- **发布行程**：用户可以发布自己的出行计划，包括出发地、目的地、出发时间、价格和座位数
- **搜索行程**：可以根据出发地、目的地、日期和时间筛选行程
- **行程预订**：用户可以预订符合条件的行程
- **行程查看**：用户可以查看自己发布的行程和预订的行程

### 地址选择
- **地图地址选择器**：集成地图服务，方便用户选择准确的出发地和目的地
- **地址输入清除**：输入框末尾提供清除按钮，方便用户快速清空内容

### 订单管理
- **我的预订**：查看当前用户作为乘客预订的所有行程
- **我发布的行程**：查看当前用户作为发布者发布的所有行程
- **历史订单**：查看已完成的历史订单

## 技术架构

### 后端技术栈
- **框架**：FastAPI (Python 3.9+)
- **数据库**：PostgreSQL (云端数据库)
- **认证**：JWT (JSON Web Tokens)
- **ORM**：SQLAlchemy
- **依赖管理**：pip

### 前端技术栈
- **框架**：Vue 3 + TypeScript
- **状态管理**：Pinia
- **路由**：Vue Router
- **构建工具**：Vite
- **样式**：原生CSS

### 项目结构
```
UniGo/
├── backend/                 # 后端代码
│   ├── routers/            # API路由
│   ├── models/             # 数据模型
│   ├── schemas/            # 数据验证模式
│   ├── database.py         # 数据库配置
│   ├── auth.py             # 认证模块
│   ├── main.py             # 应用入口
│   └── requirements.txt    # 后端依赖
├── frontend/               # 前端代码
│   ├── src/
│   │   ├── views/          # 页面组件
│   │   ├── components/     # 可复用组件
│   │   ├── api/            # API调用封装
│   │   ├── stores/         # 状态管理
│   │   ├── utils/          # 工具函数
│   │   ├── router/         # 路由配置
│   │   └── assets/         # 静态资源
│   ├── public/             # 公共文件
│   └── package.json        # 前端依赖
├── start.sh                # 项目启动脚本
└── README.md               # 项目说明文档
```

## 环境配置

### 后端环境
1. **Python版本**：3.9或更高版本
2. **依赖安装**：
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
3. **环境变量**：
   - DATABASE_URL：数据库连接字符串
   - SECRET_KEY：JWT密钥
   - ALGORITHM：JWT算法
   - ACCESS_TOKEN_EXPIRE_MINUTES：访问令牌过期时间

### 前端环境
1. **Node.js版本**：14或更高版本
2. **依赖安装**：
   ```bash
   cd frontend
   npm install
   ```

## 启动项目

### 启动后端服务
```bash
cd backend
python main.py
```
默认运行在 http://localhost:8001

### 启动前端服务
```bash
cd frontend
npm run dev
```
默认运行在 http://localhost:5181

### 一键启动脚本
项目根目录下的[start.sh](file:///d:/Users/xmmem/Documents/_coding_project/UniGo/start.sh)脚本可以同时启动前后端服务：
```bash
./start.sh
```

## API接口文档

后端使用FastAPI自动生成API文档，可通过以下地址访问：
- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

### 主要API端点

#### 用户相关
- `POST /api/users/` - 注册用户
- `POST /api/login/` - 用户登录
- `GET /api/users/me` - 获取当前用户信息
- `GET /api/users/{user_id}` - 根据ID获取用户信息

#### 行程相关
- `GET /api/trips/all/` - 获取所有行程（需要认证）
- `GET /api/trips/public/` - 获取公开行程（无需认证）
- `POST /api/trips/` - 创建新行程
- `GET /api/trips/{trip_id}` - 获取特定行程

#### 预订相关
- `GET /api/bookings/` - 获取用户的所有预订
- `POST /api/bookings/` - 创建新预订
- `DELETE /api/bookings/{booking_id}` - 取消预订

## 数据模型

### 用户(User)
- id: Integer (主键)
- username: String (唯一)
- email: String (唯一)
- hashed_password: String
- created_at: DateTime
- reputation_score: Integer (信誉度分数)

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

### 信誉度记录(ReputationRecord)
- id: Integer (主键)
- user_id: Integer (外键，关联用户)
- score_change: Integer (分数变化)
- reason: String (变化原因)
- recorded_at: DateTime (记录时间)

## 安全性

### 认证与授权
- 使用JWT Token进行用户身份验证
- 敏感操作需要相应的权限验证
- 密码使用bcrypt进行哈希存储

### 数据安全
- 数据库连接使用SSL加密
- 敏感信息不直接暴露给前端
- API接口有适当的输入验证

## 错误处理

### 前端错误处理
- 网络错误：提示用户检查网络连接
- 认证错误：自动跳转到登录页面
- 业务错误：显示具体的错误信息

### 后端错误处理
- 400：请求参数错误
- 401：未认证或认证失败
- 403：权限不足
- 404：资源不存在
- 500：服务器内部错误

## 测试账号

- 用户名：18810871613
- 密码：112233123

## 开发规范

### 代码规范
- 后端遵循PEP 8 Python编码规范
- 前端遵循Vue.js风格指南
- 变量命名清晰且具有描述性

### 提交规范
- 使用语义化提交信息
- 每次提交只包含一个功能或修复
- 提交前进行代码审查

## 待开发功能

### 核心功能
1. **微信登录**：集成微信开放平台，支持微信授权登录
2. **支付系统**：集成第三方支付平台，实现在线支付功能
3. **消息通知**：实现站内信和邮件通知功能
4. **评价系统**：用户可以对行程进行评价和反馈

### 增强功能
1. **信誉度系统**：完善用户信誉度评分机制
2. **智能推荐**：基于用户历史行为推荐行程
3. **实时聊天**：发布者和预订者之间可以实时沟通
4. **行程分享**：支持将行程分享到社交媒体

## 常见问题

### 启动问题
1. **端口被占用**：修改配置文件中的端口或终止占用进程
2. **依赖安装失败**：检查网络连接或更换pip源
3. **数据库连接失败**：检查数据库配置和网络连接

### 使用问题
1. **登录失败**：检查用户名和密码是否正确
2. **数据加载失败**：检查网络连接和认证状态
3. **页面显示异常**：清除浏览器缓存或使用无痕模式

### 开发问题
1. **API调用失败**：检查接口地址和参数是否正确
2. **组件不显示**：检查组件导入和注册是否正确
3. **样式错乱**：检查CSS选择器优先级和作用域

## 贡献指南

### 提交Issue
- 使用清晰的标题描述问题
- 提供详细的复现步骤
- 附上相关的错误信息和截图

### 提交Pull Request
- Fork项目到自己的仓库
- 创建功能分支进行开发
- 编写清晰的提交信息
- 确保代码通过所有测试

## 许可证

本项目采用MIT许可证，详情请查看LICENSE文件。

## 联系方式

如有任何问题或建议，请通过以下方式联系我们：
- 邮箱：[your-email@example.com](mailto:your-email@example.com)
- GitHub Issues：[项目Issues页面](https://github.com/your-username/unigo/issues)