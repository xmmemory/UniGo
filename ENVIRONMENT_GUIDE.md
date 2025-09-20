# CampusGo 环境配置指南

## 环境区分说明

CampusGo 项目支持开发环境和生产环境的区分，通过启动参数来控制不同环境的行为。

## 启动方式

### 开发环境启动（默认）

```bash
# 使用默认开发环境启动
./start.sh

# 或者明确指定开发环境
./start.sh --env development
```

### 生产环境启动

```bash
# 指定生产环境启动
./start.sh --env production
```

### 单独启动服务

```bash
# 只启动前端服务
./start.sh --frontend-only

# 只启动后端服务
./start.sh --backend-only

# 生产环境只启动前端服务
./start.sh --env production --frontend-only
```

## 环境差异

### 开发环境特征

1. **前端**：
   - 启动 Vite 开发服务器
   - 启用 Vue DevTools
   - 显示调试信息
   - API 请求指向开发服务器

2. **后端**：
   - 启用调试模式
   - 详细日志输出
   - 自动重载功能

### 生产环境特征

1. **前端**：
   - 构建优化后的静态文件
   - 禁用 Vue DevTools
   - 隐藏调试信息
   - API 请求指向生产服务器

2. **后端**：
   - 禁用调试模式
   - 简化日志输出
   - 关闭自动重载功能

## 环境配置文件

### 前端环境配置

- `.env.development` - 开发环境配置
- `.env.production` - 生产环境配置

### 后端环境配置

- `.env.development` - 开发环境配置
- `.env.production` - 生产环境配置

## 环境变量说明

### 前端

- `VITE_API_BASE_URL` - API 基础URL
- `NODE_ENV` - Node.js 环境变量

### 后端

- `DATABASE_URL` - 数据库连接URL
- `SECRET_KEY` - JWT 密钥
- `DEBUG` - 调试模式开关
- `LOG_LEVEL` - 日志级别

## 注意事项

1. 在生产环境中，请确保配置了正确的数据库连接和安全密钥
2. 生产环境应关闭调试信息和开发工具以提高性能和安全性
3. 建议在生产环境中使用 HTTPS 和适当的 CORS 配置