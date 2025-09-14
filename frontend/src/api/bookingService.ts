import API_BASE_URL from './config';
import { handleApiError, fetchWithAuth } from '@/utils/apiErrorHandler';

// 创建预订
export const createBooking = async (bookingData: { trip_id: number }, token: string) => {
  try {
    const response = await fetchWithAuth(`${API_BASE_URL}/bookings/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(bookingData),
    });
    
    if (!response.ok) {
      throw new Error('创建预订失败');
    }
    
    return await response.json();
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('网络连接失败，请确保后端服务正在运行');
    }
    throw error;
  }
};

// 获取用户的所有预订
export const getUserBookings = async (token: string) => {
  try {
    const response = await fetchWithAuth(`${API_BASE_URL}/bookings/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    if (!response.ok) {
      throw new Error('获取预订列表失败');
    }
    
    return await response.json();
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('网络连接失败，请确保后端服务正在运行');
    }
    throw error;
  }
};

// 获取特定预订
export const getBooking = async (bookingId: number, token: string) => {
  try {
    const response = await fetchWithAuth(`${API_BASE_URL}/bookings/${bookingId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    if (!response.ok) {
      throw new Error('获取预订详情失败');
    }
    
    return await response.json();
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('网络连接失败，请确保后端服务正在运行');
    }
    throw error;
  }
};

// 取消预订
export const cancelBooking = async (bookingId: number, token: string) => {
  try {
    const response = await fetchWithAuth(`${API_BASE_URL}/bookings/${bookingId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    if (!response.ok) {
      throw new Error('取消预订失败');
    }
    
    return await response.json();
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('网络连接失败，请确保后端服务正在运行');
    }
    throw error;
  }
};