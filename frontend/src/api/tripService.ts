import API_BASE_URL from './config';

// 获取所有行程
export const getTrips = async (token: string) => {
  const response = await fetch(`${API_BASE_URL}/trips/`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });
  
  if (!response.ok) {
    throw new Error('获取行程失败');
  }
  
  return await response.json();
};

// 创建新行程
export const createTrip = async (tripData: any, token: string) => {
  const response = await fetch(`${API_BASE_URL}/trips/`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(tripData),
  });
  
  if (!response.ok) {
    throw new Error('创建行程失败');
  }
  
  return await response.json();
};

// 获取特定行程
export const getTrip = async (tripId: number, token: string) => {
  const response = await fetch(`${API_BASE_URL}/trips/${tripId}`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });
  
  if (!response.ok) {
    throw new Error('获取行程详情失败');
  }
  
  return await response.json();
};