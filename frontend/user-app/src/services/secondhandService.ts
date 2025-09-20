import API_BASE_URL from '../api/config'
import { fetchWithAuth } from '../utils/apiErrorHandler'

// 获取二手物品列表
export const getSecondHandItems = async (params: {
  page?: number
  limit?: number
  keyword?: string
  category?: string
  price_range?: string
}) => {
  const queryParams = new URLSearchParams()
  // 将page转换为skip参数
  if (params.page) queryParams.append('skip', ((params.page - 1) * (params.limit || 10)).toString())
  if (params.limit) queryParams.append('limit', params.limit.toString())
  if (params.keyword) queryParams.append('keyword', params.keyword)
  if (params.category) queryParams.append('category', params.category)
  if (params.price_range) queryParams.append('price_range', params.price_range)
  
  const response = await fetch(`${API_BASE_URL}/api/v1/secondhand/?${queryParams}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  })
  
  if (!response.ok) {
    throw new Error(`获取二手物品失败: ${response.status} ${response.statusText}`)
  }
  
  return await response.json()
}

// 获取二手物品详情
export const getSecondHandItemDetail = async (itemId: number) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/secondhand/${itemId}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  })
  
  if (!response.ok) {
    throw new Error(`获取物品详情失败: ${response.status} ${response.statusText}`)
  }
  
  return await response.json()
}

// 创建二手物品
export const createSecondHandItem = async (formData: FormData) => {
  // 获取认证token
  const token = localStorage.getItem('token')
  
  const response = await fetchWithAuth(
    `${API_BASE_URL}/api/v1/secondhand/`,
    token || '',
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
      body: formData,
    }
  )
  
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}))
    throw new Error(errorData.detail || `发布物品失败: ${response.status} ${response.statusText}`)
  }
  
  return await response.json()
}