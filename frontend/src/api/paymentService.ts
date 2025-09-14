import API_BASE_URL from './config';
import { fetchWithAuth } from '@/utils/apiErrorHandler';

// 创建支付
export const createPayment = async (paymentData: { user_id: number; amount: number; status: string }, token: string) => {
  try {
    const response = await fetchWithAuth(`${API_BASE_URL}/payments/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(paymentData),
    });
    
    if (!response.ok) {
      throw new Error('创建支付失败');
    }
    
    return await response.json();
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('网络连接失败，请确保后端服务正在运行');
    }
    throw error;
  }
};

// 获取用户的所有支付记录
export const getUserPayments = async (token: string) => {
  try {
    const response = await fetchWithAuth(`${API_BASE_URL}/payments/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    if (!response.ok) {
      throw new Error('获取支付记录失败');
    }
    
    return await response.json();
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('网络连接失败，请确保后端服务正在运行');
    }
    throw error;
  }
};

// 获取特定支付记录
export const getPayment = async (paymentId: number, token: string) => {
  try {
    const response = await fetchWithAuth(`${API_BASE_URL}/payments/${paymentId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    if (!response.ok) {
      throw new Error('获取支付详情失败');
    }
    
    return await response.json();
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('网络连接失败，请确保后端服务正在运行');
    }
    throw error;
  }
};