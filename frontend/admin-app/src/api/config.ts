// API配置文件
// 注意：确保后端服务正在运行，且端口配置正确

// 根据环境变量设置API基础URL
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001';

export default API_BASE_URL;