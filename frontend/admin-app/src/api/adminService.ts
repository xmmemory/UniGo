import API_BASE_URL from './config';
import axios from 'axios';

// 创建axios实例
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

// 请求拦截器，添加认证头
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('admin_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器，处理通用错误
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response) {
      // 服务器返回错误状态码
      const { status, data } = error.response;
      if (status === 401) {
        // 未授权，清除本地存储的token
        localStorage.removeItem('admin_token');
        window.location.href = '/';
      }
      return Promise.reject(new Error(data.detail || `请求失败: ${status}`));
    } else if (error.request) {
      // 网络错误
      return Promise.reject(new Error('网络连接失败，请确保后端服务正在运行'));
    } else {
      // 其他错误
      return Promise.reject(new Error('请求配置错误'));
    }
  }
);

// 管理员登录
export const adminLoginUser = async (credentials: { username: string; password: string }) => {
  try {
    const response = await apiClient.post('/api/v1/admin/login/', credentials);
    return response.data;
  } catch (error) {
    throw error;
  }
};

// 获取当前管理员信息
export const getCurrentAdmin = async () => {
  try {
    const response = await apiClient.get('/api/v1/admin/me');
    return response.data;
  } catch (error) {
    throw error;
  }
};

// 获取用户列表
export const getAdminUsers = async (skip: number = 0, limit: number = 100) => {
  try {
    const response = await apiClient.get(`/api/v1/admin/users/?skip=${skip}&limit=${limit}`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

// 获取行程列表
export const getAdminTrips = async (skip: number = 0, limit: number = 100) => {
  try {
    const response = await apiClient.get(`/api/v1/admin/trips/?skip=${skip}&limit=${limit}`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

// 获取预订列表
export const getAdminBookings = async (skip: number = 0, limit: number = 100) => {
  try {
    const response = await apiClient.get(`/api/v1/admin/bookings/?skip=${skip}&limit=${limit}`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

// 获取二手交易列表
export const getAdminSecondHandItems = async (skip: number = 0, limit: number = 100) => {
  try {
    const response = await apiClient.get(`/api/v1/admin/secondhand/?skip=${skip}&limit=${limit}`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

// 获取跑腿任务列表
export const getAdminErrandTasks = async (skip: number = 0, limit: number = 100) => {
  try {
    const response = await apiClient.get(`/api/v1/admin/errands/?skip=${skip}&limit=${limit}`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

// 获取管理员统计数据
export const getAdminStats = async () => {
  try {
    const response = await apiClient.get('/api/v1/admin/stats/overview');
    return response.data;
  } catch (error) {
    throw error;
  }
};

// 获取预订趋势数据
export const getBookingTrends = async (days: number = 30) => {
  try {
    const response = await apiClient.get(`/api/v1/admin/stats/booking-trends?days=${days}`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

// 获取用户增长数据
export const getUserGrowth = async (days: number = 30) => {
  try {
    const response = await apiClient.get(`/api/v1/admin/stats/user-growth?days=${days}`);
    return response.data;
  } catch (error) {
    throw error;
  }
};