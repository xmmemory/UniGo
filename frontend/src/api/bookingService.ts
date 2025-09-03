import API_BASE_URL from './config';

// 创建预订
export const createBooking = async (bookingData: { trip_id: number }, token: string) => {
  const response = await fetch(`${API_BASE_URL}/bookings/`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(bookingData),
  });
  
  if (!response.ok) {
    throw new Error('创建预订失败');
  }
  
  return await response.json();
};

// 获取用户的所有预订
export const getUserBookings = async (token: string) => {
  const response = await fetch(`${API_BASE_URL}/bookings/`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });
  
  if (!response.ok) {
    throw new Error('获取预订列表失败');
  }
  
  return await response.json();
};

// 获取特定预订
export const getBooking = async (bookingId: number, token: string) => {
  const response = await fetch(`${API_BASE_URL}/bookings/${bookingId}`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });
  
  if (!response.ok) {
    throw new Error('获取预订详情失败');
  }
  
  return await response.json();
};

// 取消预订
export const cancelBooking = async (bookingId: number, token: string) => {
  // 注意：这里需要后端实现DELETE方法
  const response = await fetch(`${API_BASE_URL}/bookings/${bookingId}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });
  
  if (!response.ok) {
    throw new Error('取消预订失败');
  }
  
  return await response.json();
};