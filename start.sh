#!/bin/bash

# 启动后端服务
cd backend
echo "Starting backend service..."
py main.py &
BACKEND_PID=$!

# 等待后端服务启动
sleep 3

# 启动前端服务
cd ../frontend
echo "Starting frontend service..."
npm run dev &
FRONTEND_PID=$!

# 捕获退出信号，确保关闭所有服务
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT TERM

echo "UniGo服务已启动："
echo "- 后端服务 PID: $BACKEND_PID"
echo "- 前端服务 PID: $FRONTEND_PID"
echo "访问 http://localhost:5173 查看前端界面"

# 等待服务运行
wait