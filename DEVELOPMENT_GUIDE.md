# CampusGo 项目开发手册

## 目录
1. [项目概述](#项目概述)
2. [技术架构](#技术架构)
3. [开发环境搭建](#开发环境搭建)
4. [项目结构说明](#项目结构说明)
5. [后端开发指南](#后端开发指南)
6. [前端开发指南](#前端开发指南)
7. [数据库设计](#数据库设计)
8. [API设计规范](#api设计规范)
9. [认证与授权](#认证与授权)
10. [错误处理](#错误处理)
11. [测试指南](#测试指南)
12. [部署指南](#部署指南)
13. [代码规范](#代码规范)
14. [Git工作流](#git工作流)
15. [常见问题与解决方案](#常见问题与解决方案)

## 项目概述

CampusGo是一个校园生活平台，旨在为大学生提供便捷、安全的拼车服务。项目采用前后端分离架构，后端使用FastAPI框架，前端使用Vue 3 + TypeScript。

### 核心功能模块
- 用户管理（注册、登录、个人信息）
- 行程管理（发布、搜索、预订）
- 订单管理（我的预订、历史订单）
- 支付系统（待开发）
- 信誉度系统（待完善）

## 技术架构

### 后端技术栈
- **框架**：FastAPI (Python 3.9+)
- **数据库**：PostgreSQL
- **ORM**：SQLAlchemy
- **认证**：JWT
- **依赖管理**：pip

### 前端技术栈
- **框架**：Vue 3 + TypeScript
- **状态管理**：Pinia
- **路由**：Vue Router
- **构建工具**：Vite
- **样式**：原生CSS

### 部署环境
- **后端**：云服务器 + Gunicorn + Nginx
- **前端**：静态文件部署
- **数据库**：云数据库服务

## 开发环境搭建

### 后端环境配置

1. **安装Python 3.9+**
   ```bash
   # Windows (使用Chocolatey)
   choco install python
   
   # macOS (使用Homebrew)
   brew install python
   
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3 python3-pip
   ```

2. **创建虚拟环境**
   ```bash
   cd backend
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **配置环境变量**
   创建`.env`文件，内容如下：
   ```
   DATABASE_URL=postgresql://username:password@host:port/database
   SECRET_KEY=your-secret-key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **启动后端服务**
   ```bash
   python main.py
   ```

### 前端环境配置

1. **安装Node.js 14+**
   ```bash
   # Windows (使用Chocolatey)
   choco install nodejs
   
   # macOS (使用Homebrew)
   brew install node
   
   # Ubuntu/Debian
   curl -fsSL https://deb.nodesource.com/setup_14.x | sudo -E bash -
   sudo apt-get install -y nodejs
   ```

2. **安装依赖**
   ```bash
   cd frontend
   npm install
   ```

3. **启动前端开发服务器**
   ```bash
   npm run dev
   ```

## 项目结构说明

### 后端项目结构
```
backend/
├── main.py                 # 应用入口
├── database.py             # 数据库配置
├── auth.py                 # 认证模块
├── models.py               # 数据模型
├── schemas.py              # Pydantic模型
├── middleware/             # 中间件
├── routers/                # API路由
│   ├── users.py           # 用户相关API
│   ├── trips.py           # 行程相关API
│   ├── bookings.py        # 预订相关API
│   ├── payments.py        # 支付相关API
│   └── reputation.py      # 信誉度相关API
├── requirements.txt        # 依赖列表
└── .env                   # 环境变量配置
```

### 前端项目结构
```
frontend/
├── src/
│   ├── main.ts            # 应用入口
│   ├── App.vue            # 根组件
│   ├── router/            # 路由配置
│   ├── stores/            # 状态管理
│   ├── views/             # 页面组件
│   ├── components/        # 可复用组件
│   ├── api/               # API调用封装
│   ├── utils/             # 工具函数
│   └── assets/            # 静态资源
├── public/                # 公共文件
├── index.html             # HTML模板
├── vite.config.ts         # Vite配置
├── package.json           # 依赖和脚本
└── tsconfig.json          # TypeScript配置
```

## 后端开发指南

### 创建新的API端点

1. **在routers目录下创建新的路由文件**
   ```python
   from fastapi import APIRouter, Depends
   from sqlalchemy.orm import Session
   from database import get_db
   
   router = APIRouter()
   
   @router.get("/example/")
   def get_example(db: Session = Depends(get_db)):
       return {"message": "Hello World"}
   ```

2. **在main.py中注册路由**
   ```python
   from routers import example
   
   app.include_router(example.router, prefix="/api")
   ```

### 数据库模型定义

```python
from sqlalchemy import Column, Integer, String
from database import Base

class Example(Base):
    __tablename__ = 'examples'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
```

### Pydantic模型定义

```python
from pydantic import BaseModel
from datetime import datetime

class ExampleBase(BaseModel):
    name: str

class ExampleCreate(ExampleBase):
    pass

class Example(ExampleBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True
```

### 错误处理

```python
from fastapi import HTTPException, status

def example_function():
    try:
        # 业务逻辑
        pass
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="操作失败，请稍后重试"
        )
```

## 前端开发指南

### 创建新的页面组件

1. **在views目录下创建Vue组件**
   ```vue
   <template>
     <div class="example">
       <h1>{{ title }}</h1>
     </div>
   </template>
   
   <script setup lang="ts">
   import { ref } from 'vue'
   
   const title = ref('示例页面')
   </script>
   
   <style scoped>
   .example {
     padding: 1rem;
   }
   </style>
   ```

2. **在router/index.ts中添加路由**
   ```typescript
   {
     path: '/example',
     name: 'example',
     component: () => import('../views/ExampleView.vue')
   }
   ```

### API调用封装

```typescript
// api/exampleService.ts
import API_BASE_URL from './config'
import { handleApiError } from '@/utils/apiErrorHandler'

export const getExampleData = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/example/`)
    if (!response.ok) {
      throw new Error('获取数据失败')
    }
    return await response.json()
  } catch (error) {
    handleApiError(error)
  }
}
```

### 状态管理

```typescript
// stores/example.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useExampleStore = defineStore('example', () => {
  const data = ref<any>(null)
  
  const setData = (newData: any) => {
    data.value = newData
  }
  
  return {
    data,
    setData
  }
})
```

## 数据库设计

### 用户表 (users)
| 字段名 | 类型 | 约束 | 描述 |
|-------|------|------|------|
| id | Integer | Primary Key | 用户ID |
| username | String(50) | Unique, Not Null | 用户名 |
| email | String(100) | Unique, Not Null | 邮箱 |
| hashed_password | String(100) | Not Null | 哈希密码 |
| created_at | DateTime | Not Null | 创建时间 |
| reputation_score | Integer | Not Null, Default 100 | 信誉度分数 |

### 行程表 (trips)
| 字段名 | 类型 | 约束 | 描述 |
|-------|------|------|------|
| id | Integer | Primary Key | 行程ID |
| departure | String(100) | Not Null | 出发地 |
| destination | String(100) | Not Null | 目的地 |
| departure_time | DateTime | Not Null | 出发时间 |
| price_per_person | Float | Not Null | 每人价格 |
| available_seats | Integer | Not Null | 可用座位数 |
| owner_id | Integer | Foreign Key | 发布者ID |

### 预订表 (bookings)
| 字段名 | 类型 | 约束 | 描述 |
|-------|------|------|------|
| id | Integer | Primary Key | 预订ID |
| user_id | Integer | Foreign Key | 用户ID |
| trip_id | Integer | Foreign Key | 行程ID |
| booked_at | DateTime | Not Null | 预订时间 |
| status | String(20) | Not Null, Default 'confirmed' | 状态 |

### 信誉度记录表 (reputation_records)
| 字段名 | 类型 | 约束 | 描述 |
|-------|------|------|------|
| id | Integer | Primary Key | 记录ID |
| user_id | Integer | Foreign Key | 用户ID |
| score_change | Integer | Not Null | 分数变化 |
| reason | String(200) | Not Null | 变化原因 |
| recorded_at | DateTime | Not Null | 记录时间 |

## API设计规范

### RESTful API设计原则
1. **资源命名**：使用名词复数形式
2. **HTTP方法**：
   - GET：获取资源
   - POST：创建资源
   - PUT：更新资源
   - DELETE：删除资源
3. **状态码**：
   - 200：成功
   - 201：创建成功
   - 400：请求错误
   - 401：未认证
   - 403：权限不足
   - 404：资源不存在
   - 500：服务器错误

### API端点示例
```
GET    /api/users/          # 获取用户列表
POST   /api/users/          # 创建用户
GET    /api/users/{id}      # 获取特定用户
PUT    /api/users/{id}      # 更新用户
DELETE /api/users/{id}      # 删除用户

GET    /api/trips/          # 获取行程列表
POST   /api/trips/          # 创建行程
GET    /api/trips/{id}      # 获取特定行程
```

### 请求/响应格式
```json
// 请求示例
{
  "username": "example",
  "email": "example@example.com",
  "password": "password123"
}

// 响应示例
{
  "id": 1,
  "username": "example",
  "email": "example@example.com",
  "created_at": "2023-01-01T00:00:00"
}
```

## 认证与授权

### JWT Token机制
1. **登录流程**：
   - 用户提交用户名和密码
   - 服务端验证凭据
   - 生成JWT Token并返回给客户端

2. **Token使用**：
   - 客户端在Authorization头中携带Token
   - 服务端验证Token有效性
   - 根据Token获取用户信息

### 权限控制
```python
# 后端权限验证
from fastapi import Depends
from auth import get_current_user

@router.get("/protected/")
def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": "只有认证用户才能访问"}
```

```typescript
// 前端路由守卫
const requireAuth = async (to: any, from: any, next: any) => {
  const authStore = useAuthStore()
  await authStore.initializeAuth()
  
  if (authStore.isAuthenticated) {
    next()
  } else {
    next('/login')
  }
}
```

## 错误处理

### 后端错误处理
```python
from fastapi import HTTPException, status

# 业务逻辑错误
raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="用户名已存在"
)

# 认证错误
raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="认证失败",
    headers={"WWW-Authenticate": "Bearer"}
)

# 权限错误
raise HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="权限不足"
)
```

### 前端错误处理
```typescript
// API错误处理
export const handleApiError = async (error: any) => {
  if (error.response?.status === 401) {
    // 处理认证错误
    useAuthStore().logout()
    router.push('/login')
    throw new Error('请重新登录')
  }
  throw error
}
```

## 测试指南

### 后端测试
```python
# test_users.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/api/users/", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "id" in response.json()
```

### 前端测试
```typescript
// ExampleView.test.ts
import { mount } from '@vue/test-utils'
import ExampleView from '@/views/ExampleView.vue'

describe('ExampleView', () => {
  it('renders correctly', () => {
    const wrapper = mount(ExampleView)
    expect(wrapper.text()).toContain('示例页面')
  })
})
```

### 运行测试
```bash
# 后端测试
cd backend
pytest

# 前端测试
cd frontend
npm run test
```

## 部署指南

### 后端部署
1. **安装生产环境依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **使用Gunicorn运行**
   ```bash
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
   ```

3. **Nginx配置**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

### 前端部署
1. **构建生产版本**
   ```bash
   npm run build
   ```

2. **部署静态文件**
   将`dist`目录下的文件部署到Web服务器

## 代码规范

### Python代码规范
- 遵循PEP 8规范
- 使用类型注解
- 函数和类添加文档字符串
- 变量命名使用snake_case
- 常量命名使用UPPER_SNAKE_CASE

### TypeScript代码规范
- 遵循TypeScript编码规范
- 使用interface定义数据结构
- 函数和类添加JSDoc注释
- 变量命名使用camelCase
- 常量命名使用UPPER_SNAKE_CASE

### Vue组件规范
- 组件命名使用PascalCase
- 组件文件名使用PascalCase
- 组件属性使用kebab-case
- 组件样式使用scoped

### 地址选择器组件
项目中使用了增强版地图地址选择器组件(EnhancedMapAddressSelector)，提供了自动补全和当前位置获取功能。该组件位于`src/components/EnhancedMapAddressSelector.vue`，相关文档请查看`src/components/EnhancedMapAddressSelector.md`。

## Git工作流

### 分支策略
- `main`：生产环境分支
- `develop`：开发环境分支
- `feature/*`：功能开发分支
- `hotfix/*`：紧急修复分支
- `release/*`：发布准备分支

### 提交规范
```bash
# 功能开发
git checkout -b feature/user-profile
git add .
git commit -m "feat: 添加用户个人资料页面"

# Bug修复
git checkout -b hotfix/login-error
git add .
git commit -m "fix: 修复登录错误处理"

# 文档更新
git add .
git commit -m "docs: 更新开发手册"
```

### 合并流程
1. 功能开发完成后提交Pull Request
2. 代码审查通过后合并到develop分支
3. 发布时从develop合并到main分支

## 常见问题与解决方案

### 后端常见问题

1. **数据库连接失败**
   ```bash
   # 检查数据库服务是否运行
   systemctl status postgresql
   
   # 检查连接字符串
   echo $DATABASE_URL
   ```

2. **JWT Token验证失败**
   ```python
   # 检查SECRET_KEY是否一致
   print(os.getenv("SECRET_KEY"))
   ```

3. **端口被占用**
   ```bash
   # 查找占用端口的进程
   netstat -tulpn | grep :8001
   
   # 终止进程
   kill -9 <PID>
   ```

### 前端常见问题

1. **组件不显示**
   ```bash
   # 检查组件导入
   import ExampleComponent from '@/components/ExampleComponent.vue'
   
   # 检查组件注册
   components: {
     ExampleComponent
   }
   ```

2. **API调用失败**
   ```typescript
   // 检查API地址
   const API_BASE_URL = 'http://localhost:8001/api'
   
   // 检查网络连接
   fetch(API_BASE_URL + '/users/')
   ```

3. **样式错乱**
   ```vue
   <!-- 检查scoped属性 -->
   <style scoped>
   .example {
     color: red;
   }
   </style>
   ```

### 部署常见问题

1. **Nginx配置错误**
   ```nginx
   # 检查配置语法
   nginx -t
   
   # 重新加载配置
   nginx -s reload
   ```

2. **SSL证书问题**
   ```bash
   # 使用Let's Encrypt获取证书
   certbot --nginx -d your-domain.com
   ```

3. **性能优化**
   ```bash
   # 启用Gzip压缩
   gzip on;
   gzip_types text/css application/javascript;
   ```

## 附录

### 常用命令

**后端**
```bash
# 启动开发服务器
python main.py

# 运行测试
pytest

# 查看日志
tail -f app.log
```

**前端**
```bash
# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 运行测试
npm run test
```

### 开发工具推荐

**后端**
- PyCharm/VS Code
- Postman (API测试)
- pgAdmin (数据库管理)

**前端**
- VS Code
- Chrome DevTools
- Vue DevTools

### 学习资源

**FastAPI**
- 官方文档: https://fastapi.tiangolo.com/
- 教程: https://fastapi.tiangolo.com/tutorial/

**Vue 3**
- 官方文档: https://v3.vuejs.org/
- 教程: https://vuejs.org/guide/introduction.html

**TypeScript**
- 官方文档: https://www.typescriptlang.org/
- 教程: https://www.typescriptlang.org/docs/