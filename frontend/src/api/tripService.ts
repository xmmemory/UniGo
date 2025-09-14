import API_BASE_URL from './config';
import { fetchWithAuth } from '@/utils/apiErrorHandler';

// 获取所有公开行程（无需认证）
export const getPublicTrips = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/trips/public/all/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    if (!response.ok) {
      throw new Error('获取行程失败');
    }
    
    return await response.json();
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('网络连接失败，请确保后端服务正在运行');
    }
    throw error;
  }
};

// 获取所有公开行程（需要认证）
export const getTrips = async (token: string) => {
  try {
    const response = await fetchWithAuth(`${API_BASE_URL}/trips/all/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    if (!response.ok) {
      throw new Error('获取行程失败');
    }
    
    return await response.json();
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('网络连接失败，请确保后端服务正在运行');
    }
    throw error;
  }
};

// 创建新行程
export const createTrip = async (tripData: any, token: string) => {
  try {
    const response = await fetchWithAuth(`${API_BASE_URL}/trips/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(tripData),
    });
    
    if (!response.ok) {
      throw new Error('创建行程失败');
    }
    
    return await response.json();
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('网络连接失败，请确保后端服务正在运行');
    }
    throw error;
  }
};

// 获取特定行程
export const getTrip = async (tripId: number, token: string) => {
  try {
    const response = await fetchWithAuth(`${API_BASE_URL}/trips/${tripId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    if (!response.ok) {
      throw new Error('获取行程详情失败');
    }
    
    return await response.json();
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('网络连接失败，请确保后端服务正在运行');
    }
    throw error;
  }
};