import API_BASE_URL from './config';

// 创建支付
export const createPayment = async (paymentData: { user_id: number; amount: number; status: string }, token: string) => {
  const response = await fetch(`${API_BASE_URL}/payments/`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(paymentData),
  });
  
  if (!response.ok) {
    throw new Error('创建支付失败');
  }
  
  return await response.json();
};

// 获取用户的所有支付记录
export const getUserPayments = async (token: string) => {
  const response = await fetch(`${API_BASE_URL}/payments/`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });
  
  if (!response.ok) {
    throw new Error('获取支付记录失败');
  }
  
  return await response.json();
};

// 获取特定支付记录
export const getPayment = async (paymentId: number, token: string) => {
  const response = await fetch(`${API_BASE_URL}/payments/${paymentId}`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });
  
  if (!response.ok) {
    throw new Error('获取支付详情失败');
  }
  
  return await response.json();
};