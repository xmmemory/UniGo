import API_BASE_URL from '../api/config'
import { fetchWithAdminAuth } from '../utils/apiErrorHandler'

// 获取管理员统计数据
export const getAdminStats = async () => {
  // 从localStorage获取管理员token
  const adminToken = localStorage.getItem('admin_token')
  
  if (!adminToken) {
    throw new Error('管理员未登录')
  }
  
  const response = await fetchWithAdminAuth(
    `${API_BASE_URL}/api/v1/admin/stats/`,
    adminToken || '',
    {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    }
  )
  
  if (!response.ok) {
    throw new Error(`获取统计数据失败: ${response.status} ${response.statusText}`)
  }
  
  return await response.json()
}