import API_BASE_URL from '../api/config'
import { fetchWithAuth } from '../utils/apiErrorHandler'

// 获取公开行程列表（无需认证）
export const getPublicTrips = async (params: {
  page?: number
  limit?: number
  departure?: string
  destination?: string
  date?: string
}) => {
  const queryParams = new URLSearchParams()
  // 将page转换为skip参数
  if (params.page) queryParams.append('skip', ((params.page - 1) * (params.limit || 10)).toString())
  if (params.limit) queryParams.append('limit', params.limit.toString())
  if (params.departure) queryParams.append('departure', params.departure)
  if (params.destination) queryParams.append('destination', params.destination)
  if (params.date) queryParams.append('date', params.date)
  
  const response = await fetch(`${API_BASE_URL}/api/v1/trips/public/all/?${queryParams}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  })
  
  if (!response.ok) {
    throw new Error(`获取行程失败: ${response.status} ${response.statusText}`)
  }
  
  return await response.json()
}

// 获取行程列表（需要认证）
export const getTrips = async (params: {
  page?: number
  limit?: number
  departure?: string
  destination?: string
  date?: string
}) => {
  const queryParams = new URLSearchParams()
  // 将page转换为skip参数
  if (params.page) queryParams.append('skip', ((params.page - 1) * (params.limit || 10)).toString())
  if (params.limit) queryParams.append('limit', params.limit.toString())
  if (params.departure) queryParams.append('departure', params.departure)
  if (params.destination) queryParams.append('destination', params.destination)
  if (params.date) queryParams.append('date', params.date)
  
  // 获取认证token
  const token = localStorage.getItem('token')
  
  const response = await fetchWithAuth(
    `${API_BASE_URL}/api/v1/trips/all/?${queryParams}`,
    token || '',
    {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    }
  )
  
  if (!response.ok) {
    throw new Error(`获取行程失败: ${response.status} ${response.statusText}`)
  }
  
  return await response.json()
}

// 获取行程详情
export const getTripDetail = async (tripId: number) => {
  // 获取认证token
  const token = localStorage.getItem('token')
  
  const response = await fetchWithAuth(
    `${API_BASE_URL}/api/v1/trips/${tripId}`,
    token || '',
    {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    }
  )
  
  if (!response.ok) {
    throw new Error(`获取行程详情失败: ${response.status} ${response.statusText}`)
  }
  
  return await response.json()
}

// 创建行程
export const createTrip = async (tripData: {
  departure: string
  destination: string
  departure_time: string
  available_seats: number
  price: number
  vehicle_type: string
  license_plate: string
  driver_phone: string
  description?: string
}) => {
  // 获取认证token
  const token = localStorage.getItem('token')
  
  const response = await fetchWithAuth(
    `${API_BASE_URL}/api/v1/trips/`,
    token || '',
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(tripData),
    }
  )
  
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}))
    throw new Error(errorData.detail || `创建行程失败: ${response.status} ${response.statusText}`)
  }
  
  return await response.json()
}

// 获取作为司机的行程
export const getDriverTrips = async (params: {
  page?: number
  limit?: number
}) => {
  const queryParams = new URLSearchParams()
  if (params.page) queryParams.append('page', params.page.toString())
  if (params.limit) queryParams.append('limit', params.limit.toString())
  
  // 获取认证token
  const token = localStorage.getItem('token')
  
  const response = await fetchWithAuth(
    `${API_BASE_URL}/api/v1/trips/driver/?${queryParams}`,
    token || '',
    {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    }
  )
  
  if (!response.ok) {
    throw new Error(`获取司机行程失败: ${response.status} ${response.statusText}`)
  }
  
  return await response.json()
}

// 获取作为乘客的预订
export const getPassengerBookings = async (params: {
  page?: number
  limit?: number
}) => {
  const queryParams = new URLSearchParams()
  if (params.page) queryParams.append('page', params.page.toString())
  if (params.limit) queryParams.append('limit', params.limit.toString())
  
  // 获取认证token
  const token = localStorage.getItem('token')
  
  const response = await fetchWithAuth(
    `${API_BASE_URL}/api/v1/bookings/passenger/?${queryParams}`,
    token || '',
    {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    }
  )
  
  if (!response.ok) {
    throw new Error(`获取乘客预订失败: ${response.status} ${response.statusText}`)
  }
  
  return await response.json()
}

// 预订行程
export const bookTrip = async (tripId: number) => {
  // 获取认证token
  const token = localStorage.getItem('token')
  
  const response = await fetchWithAuth(
    `${API_BASE_URL}/api/v1/bookings/`,
    token || '',
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ trip_id: tripId }),
    }
  )
  
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}))
    throw new Error(errorData.detail || `预订行程失败: ${response.status} ${response.statusText}`)
  }
  
  return await response.json()
}

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