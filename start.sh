#!/bin/bash

# 解析命令行参数
ENVIRONMENT="development"
# ENVIRONMENT="production"
FRONTEND_ONLY=false
BACKEND_ONLY=false

# 定义颜色变量
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# 检查终端是否支持颜色
check_color_support() {
  if [ -t 1 ] && [ -z "$NO_COLOR" ] && [ -z "$CI" ]; then
    return 0
  else
    return 1
  fi
}

# 彩色echo函数
cecho() {
  local color="$1"
  local text="$2"
  if check_color_support; then
    echo -e "${color}${text}${NC}"
  else
    echo "$text"
  fi
}

# 彩色echo函数（不换行）
cecho_n() {
  local color="$1"
  local text="$2"
  if check_color_support; then
    echo -ne "${color}${text}${NC}"
  else
    echo -n "$text"
  fi
}

# 无颜色的echo函数（用于信号处理）
plain_echo() {
  echo "$1"
}

while [[ $# -gt 0 ]]; do
  case $1 in 
    --env)
      ENVIRONMENT="$2"
      shift 2
      ;;
    --frontend-only)
      FRONTEND_ONLY=true
      shift
      ;;
    --backend-only)
      BACKEND_ONLY=true
      shift
      ;;
    *)
      cecho $RED "未知参数: $1"
      cecho $WHITE "用法: $0 [--env development|production] [--frontend-only] [--backend-only]"
      exit 1
      ;;
  esac
done

cecho $CYAN "=========================================="
cecho $CYAN "  CampusGo 启动脚本"
cecho $CYAN "  启动环境: $ENVIRONMENT"
cecho $CYAN "=========================================="

# 设置环境变量
export NODE_ENV=$ENVIRONMENT
export APP_ENV=$ENVIRONMENT

# 定义端口变量
BACKEND_PORT=8001
USER_FRONTEND_PORT_DEVELOPMENT=5173
ADMIN_FRONTEND_PORT_DEVELOPMENT=5174
FRONTEND_PORT_PRODUCTION=4174

# 检查是否在Windows环境下运行
IS_WINDOWS=false
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
  IS_WINDOWS=true
fi

# 启动后端服务（除非指定了--frontend-only）
if [ "$BACKEND_ONLY" = true ] || [ "$FRONTEND_ONLY" = false ]; then
  cd backend
  cecho $YELLOW "启动后端服务..."
  cecho $WHITE "后端服务端口: $BACKEND_PORT"
  
  # 根据环境设置不同的启动参数
  if [ "$ENVIRONMENT" = "production" ]; then
    cecho $PURPLE "生产环境启动后端服务"
    # 根据操作系统选择合适的命令
    if [ "$IS_WINDOWS" = true ]; then
      py run.py --port $BACKEND_PORT > backend.log 2>&1 &
    else
      python run.py --port $BACKEND_PORT > backend.log 2>&1 &
    fi
  else
    cecho $PURPLE "开发环境启动后端服务"
    # 根据操作系统选择合适的命令
    if [ "$IS_WINDOWS" = true ]; then
      py run.py --port $BACKEND_PORT > backend.log 2>&1 &
    else
      python run.py --port $BACKEND_PORT > backend.log 2>&1 &
    fi
  fi
  
  BACKEND_PID=$!
  cecho $WHITE "后端服务 PID: $BACKEND_PID"
  cecho $WHITE "后端服务日志: backend.log"
  
  # 等待后端服务启动
  sleep 5
  
  # 检查后端服务是否成功启动
  if ps -p $BACKEND_PID > /dev/null; then
    cecho $GREEN "✓ 后端服务启动成功"
    cecho $WHITE "  访问地址: http://localhost:$BACKEND_PORT"
    cecho $WHITE "  API文档: http://localhost:$BACKEND_PORT/docs"
  else
    cecho $RED "✗ 后端服务启动失败，请检查 backend.log 文件"
  fi
  
  cd ..
fi

# 启动用户端前端服务（除非指定了--backend-only）
if [ "$FRONTEND_ONLY" = true ] || [ "$BACKEND_ONLY" = false ]; then
  cd frontend/user-app
  cecho $YELLOW "启动用户端前端服务..."
  
  # 根据环境设置不同的启动命令
  if [ "$ENVIRONMENT" = "production" ]; then
    cecho $PURPLE "生产环境构建和启动用户端前端服务"
    cecho $WHITE "用户端前端服务端口: $FRONTEND_PORT_PRODUCTION"
    # 生产环境构建
    cecho $YELLOW "正在构建用户端前端资源..."
    if [ "$IS_WINDOWS" = true ]; then
      npm run build > user-frontend-build.log 2>&1
    else
      npm run build > user-frontend-build.log 2>&1
    fi
    
    if [ $? -eq 0 ]; then
      cecho $GREEN "✓ 用户端前端资源构建成功"
      # 启动生产服务器
      if [ "$IS_WINDOWS" = true ]; then
        npm run preview > user-frontend.log 2>&1 &
      else
        npm run preview > user-frontend.log 2>&1 &
      fi
    else
      cecho $RED "✗ 用户端前端资源构建失败，请检查 user-frontend-build.log 文件"
      cd ../..
      exit 1
    fi
  else
    cecho $PURPLE "开发环境启动用户端前端服务"
    cecho $WHITE "用户端前端服务端口: $USER_FRONTEND_PORT_DEVELOPMENT (如果被占用会自动选择其他端口)"
    # 开发环境启动
    if [ "$IS_WINDOWS" = true ]; then
      npm run dev > user-frontend.log 2>&1 &
    else
      npm run dev > user-frontend.log 2>&1 &
    fi
  fi
  
  USER_FRONTEND_PID=$!
  cecho $WHITE "用户端前端服务 PID: $USER_FRONTEND_PID"
  cecho $WHITE "用户端前端服务日志: user-frontend.log"
  
  # 等待用户端前端服务启动
  sleep 5
  
  # 检查用户端前端服务是否成功启动
  if ps -p $USER_FRONTEND_PID > /dev/null; then
    cecho $GREEN "✓ 用户端前端服务启动成功"
    if [ "$ENVIRONMENT" = "production" ]; then
      cecho $WHITE "  访问地址: http://localhost:$FRONTEND_PORT_PRODUCTION"
    else
      # 尝试从日志中获取实际端口
      ACTUAL_PORT=$(grep -o "http://localhost:[0-9]*" user-frontend.log | head -1 | cut -d':' -f3)
      if [ -n "$ACTUAL_PORT" ]; then
        cecho $WHITE "  访问地址: http://localhost:$ACTUAL_PORT"
      else
        cecho $WHITE "  访问地址: http://localhost:$USER_FRONTEND_PORT_DEVELOPMENT (或自动分配的其他端口)"
      fi
    fi
  else
    cecho $RED "✗ 用户端前端服务启动失败，请检查 user-frontend.log 文件"
  fi
  
  cd ../..
fi

# 启动管理端前端服务（除非指定了--backend-only）
if [ "$FRONTEND_ONLY" = true ] || [ "$BACKEND_ONLY" = false ]; then
  cd frontend/admin-app
  cecho $YELLOW "启动管理端前端服务..."
  
  # 根据环境设置不同的启动命令
  if [ "$ENVIRONMENT" = "production" ]; then
    cecho $PURPLE "生产环境构建和启动管理端前端服务"
    cecho $WHITE "管理端前端服务端口: $FRONTEND_PORT_PRODUCTION"
    # 生产环境构建
    cecho $YELLOW "正在构建管理端前端资源..."
    if [ "$IS_WINDOWS" = true ]; then
      npm run build > admin-frontend-build.log 2>&1
    else
      npm run build > admin-frontend-build.log 2>&1
    fi
    
    if [ $? -eq 0 ]; then
      cecho $GREEN "✓ 管理端前端资源构建成功"
      # 启动生产服务器
      if [ "$IS_WINDOWS" = true ]; then
        npm run preview > admin-frontend.log 2>&1 &
      else
        npm run preview > admin-frontend.log 2>&1 &
      fi
    else
      cecho $RED "✗ 管理端前端资源构建失败，请检查 admin-frontend-build.log 文件"
      cd ../..
      exit 1
    fi
  else
    cecho $PURPLE "开发环境启动管理端前端服务"
    cecho $WHITE "管理端前端服务端口: $ADMIN_FRONTEND_PORT_DEVELOPMENT (如果被占用会自动选择其他端口)"
    # 开发环境启动
    if [ "$IS_WINDOWS" = true ]; then
      npm run dev > admin-frontend.log 2>&1 &
    else
      npm run dev > admin-frontend.log 2>&1 &
    fi
  fi
  
  ADMIN_FRONTEND_PID=$!
  cecho $WHITE "管理端前端服务 PID: $ADMIN_FRONTEND_PID"
  cecho $WHITE "管理端前端服务日志: admin-frontend.log"
  
  # 等待管理端前端服务启动
  sleep 5
  
  # 检查管理端前端服务是否成功启动
  if ps -p $ADMIN_FRONTEND_PID > /dev/null; then
    cecho $GREEN "✓ 管理端前端服务启动成功"
    if [ "$ENVIRONMENT" = "production" ]; then
      cecho $WHITE "  访问地址: http://localhost:$FRONTEND_PORT_PRODUCTION"
    else
      # 尝试从日志中获取实际端口
      ACTUAL_PORT=$(grep -o "http://localhost:[0-9]*" admin-frontend.log | head -1 | cut -d':' -f3)
      if [ -n "$ACTUAL_PORT" ]; then
        cecho $WHITE "  访问地址: http://localhost:$ACTUAL_PORT"
      else
        cecho $WHITE "  访问地址: http://localhost:$ADMIN_FRONTEND_PORT_DEVELOPMENT (或自动分配的其他端口)"
      fi
    fi
  else
    cecho $RED "✗ 管理端前端服务启动失败，请检查 admin-frontend.log 文件"
  fi
  
  cd ../..
fi

# 捕获退出信号，确保关闭所有服务
# 使用printf而不是echo，避免ANSI转义序列问题
trap 'printf "正在关闭服务...\n"; kill $BACKEND_PID $USER_FRONTEND_PID $ADMIN_FRONTEND_PID 2>/dev/null; exit' INT TERM

cecho $CYAN ""
cecho $CYAN "=========================================="
cecho $CYAN "  CampusGo 服务状态"
cecho $CYAN "=========================================="
if [ -n "$BACKEND_PID" ]; then
  if ps -p $BACKEND_PID > /dev/null; then
    cecho $GREEN "✓ 后端服务运行中 (PID: $BACKEND_PID)"
  else
    cecho $RED "✗ 后端服务已停止"
  fi
fi
if [ -n "$USER_FRONTEND_PID" ]; then
  if ps -p $USER_FRONTEND_PID > /dev/null; then
    cecho $GREEN "✓ 用户端前端服务运行中 (PID: $USER_FRONTEND_PID)"
  else
    cecho $RED "✗ 用户端前端服务已停止"
  fi
fi
if [ -n "$ADMIN_FRONTEND_PID" ]; then
  if ps -p $ADMIN_FRONTEND_PID > /dev/null; then
    cecho $GREEN "✓ 管理端前端服务运行中 (PID: $ADMIN_FRONTEND_PID)"
  else
    cecho $RED "✗ 管理端前端服务已停止"
  fi
fi

cecho $CYAN ""
cecho $YELLOW "按 Ctrl+C 停止所有服务"
cecho $CYAN ""

# 等待服务运行
wait