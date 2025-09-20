// Utility functions for API error handling
import { fetchWithAuth, fetchWithAdminAuth } from '@campusgo/shared/utils/apiErrorHandler';
import API_BASE_URL from '../api/config';
import router from '../router';

// 检查响应是否为401 Unauthorized错误
export const isUnauthorizedError = (response: Response): boolean => {
  return response.status === 401;
};

// 处理API错误，如果是401错误则登出并跳转到登录页面
export const handleApiError = async (response: Response, error: any): Promise<void> => {
  // 检查是否为401 Unauthorized错误
  if (isUnauthorizedError(response)) {
    // 清除本地存储的token
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('user');
    
    // 跳转到登录页面
    if (router) {
      router.push('/login');
    }
    
    // 抛出自定义错误信息
    throw new Error('您的登录已过期，请重新登录');
  }
  
  // 其他错误处理
  throw error;
};

// 刷新token的函数（需要后端支持）
export const refreshToken = async (): Promise<string | null> => {
  try {
    // 检查是否有当前token
    const token = localStorage.getItem('token');
    if (!token) {
      return null;
    }
    
    // 调用后端的刷新token接口
    const response = await fetch(`${API_BASE_URL}/api/v1/refresh-token/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });
    
    if (!response.ok) {
      throw new Error('Token refresh failed');
    }
    
    const data = await response.json();
    return data.access_token;
  } catch (error) {
    console.error('Token refresh failed:', error);
    return null;
  }
};

export { fetchWithAuth, fetchWithAdminAuth };