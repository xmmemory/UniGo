import API_BASE_URL from '../api/config'
import { fetchWithAuth } from '../utils/apiErrorHandler'

// 获取预订列表
export const getBookings = async (params: {
  page?: number
  limit?: number
}) => {
  const queryParams = new URLSearchParams()
  if (params.page) queryParams.append('page', params.page.toString())
  if (params.limit) queryParams.append('limit', params.limit.toString())
  
  // 获取认证token
  const token = localStorage.getItem('token')
  
  const response = await fetchWithAuth(
    `${API_BASE_URL}/api/v1/bookings/?${queryParams}`,
    token || '',
    {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    }
  )
  
  if (!response.ok) {
    throw new Error(`获取预订信息失败: ${response.status} ${response.statusText}`)
  }
  
  return await response.json()
}

// 取消预订
export const cancelBooking = async (bookingId: number) => {
  // 获取认证token
  const token = localStorage.getItem('token')
  
  const response = await fetchWithAuth(
    `${API_BASE_URL}/api/v1/bookings/${bookingId}/cancel`,
    token || '',
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    }
  )
  
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}))
    throw new Error(errorData.detail || `取消预订失败: ${response.status} ${response.statusText}`)
  }
  
  return await response.json()
}