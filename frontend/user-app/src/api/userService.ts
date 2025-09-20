import API_BASE_URL from './config';
import { fetchWithAuth } from '../utils/apiErrorHandler';
import { useAuthStore } from '../stores/auth';

// 验证邮箱格式
const validateEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

// 验证用户名格式
const validateUsername = (username: string): boolean => {
  const usernameRegex = /^[a-zA-Z0-9_]+$/;
  return usernameRegex.test(username) && username.length >= 3 && username.length <= 20;
};

// 验证密码强度
const validatePasswordStrength = (password: string): { isValid: boolean; errors: string[] } => {
  const errors: string[] = [];
  
  if (password.length < 8) {
    errors.push('密码长度至少为8个字符');
  }
  
  if (!/[A-Z]/.test(password)) {
    errors.push('密码必须包含至少一个大写字母');
  }
  
  if (!/[a-z]/.test(password)) {
    errors.push('密码必须包含至少一个小写字母');
  }
  
  if (!/\d/.test(password)) {
    errors.push('密码必须包含至少一个数字');
  }
  
  if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
    errors.push('密码必须包含至少一个特殊字符');
  }
  
  return {
    isValid: errors.length === 0,
    errors
  };
};

// 带自动刷新令牌的fetch函数
const fetchWithAutoRefresh = async (url: string, options: RequestInit = {}) => {
  const authStore = useAuthStore();
  
  // 如果令牌即将过期，先刷新
  if (authStore.isTokenExpiringSoon && authStore.refreshToken) {
    const newToken = await authStore.refreshAccessToken();
    if (newToken) {
      // 更新Authorization头
      if (!options.headers) {
        options.headers = {};
      }
      (options.headers as Record<string, string>)['Authorization'] = `Bearer ${newToken}`;
    }
  }
  
  let response = await fetch(url, options);
  
  // 如果是401错误，尝试刷新令牌
  if (response.status === 401 && authStore.refreshToken) {
    const newToken = await authStore.refreshAccessToken();
    if (newToken) {
      // 重新发送请求
      if (!options.headers) {
        options.headers = {};
      }
      (options.headers as Record<string, string>)['Authorization'] = `Bearer ${newToken}`;
      response = await fetch(url, options);
    }
  }
  
  return response;
};

// 用户注册
export const registerUser = async (userData: { username: string; email: string; password: string }) => {
  // 前端输入验证
  if (!validateUsername(userData.username)) {
    throw new Error('用户名格式不正确：只能包含字母、数字和下划线，长度为3-20个字符');
  }
  
  if (!validateEmail(userData.email)) {
    throw new Error('邮箱格式不正确');
  }
  
  const passwordValidation = validatePasswordStrength(userData.password);
  if (!passwordValidation.isValid) {
    throw new Error(`密码强度不足：${passwordValidation.errors.join('，')}`);
  }
  
  try {
    const response = await fetch(`${API_BASE_URL}/api/users/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `注册失败: ${response.status} ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('网络连接失败，请确保后端服务正在运行');
    }
    throw error;
  }
};

// 用户登录
export const loginUser = async (credentials: { username: string; password: string }) => {
  // 基本输入验证
  if (!credentials.username || credentials.username.trim().length === 0) {
    throw new Error('用户名不能为空');
  }
  
  if (!credentials.password || credentials.password.trim().length === 0) {
    throw new Error('密码不能为空');
  }
  
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/login/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `登录失败: ${response.status} ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('网络连接失败，请确保后端服务正在运行');
    }
    throw error;
  }
};

// 获取当前用户信息
export const getCurrentUser = async (token: string) => {
  try {
    const response = await fetchWithAutoRefresh(`${API_BASE_URL}/api/v1/users/me`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `获取用户信息失败: ${response.status} ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('网络连接失败，请确保后端服务正在运行');
    }
    throw error;
  }
};

// 更新用户个人信息
export const updateUserProfile = async (profileData: {
  full_name?: string;
  phone_number?: string;
  student_id?: string;
  university?: string;
}) => {
  const token = localStorage.getItem('token');
  
  if (!token) {
    throw new Error('用户未登录');
  }
  
  try {
    const response = await fetchWithAuth(
      `${API_BASE_URL}/api/v1/users/me`,
      token,
      {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(profileData),
      }
    );
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `更新用户信息失败: ${response.status} ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('网络连接失败，请确保后端服务正在运行');
    }
    throw error;
  }
};

// 根据ID获取用户信息
export const getUserById = async (userId: number, token: string) => {
  // 验证用户ID
  if (!Number.isInteger(userId) || userId <= 0) {
    throw new Error('无效的用户ID');
  }
  
  try {
    const response = await fetchWithAutoRefresh(`${API_BASE_URL}/api/v1/users/${userId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `获取用户信息失败: ${response.status} ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('网络连接失败，请确保后端服务正在运行');
    }
    throw error;
  }
};

// 刷新访问令牌
export const refreshAccessToken = async (refreshToken: string) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/refresh-token/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${refreshToken}`,
      },
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `刷新令牌失败: ${response.status} ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('网络连接失败，请确保后端服务正在运行');
    }
    throw error;
  }
};