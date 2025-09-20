import API_BASE_URL from '../api/config'

// 管理员登录
export const adminLogin = async (credentials: { username: string; password: string }) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/admin/login/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(credentials),
  })
  
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}))
    throw new Error(errorData.detail || `管理员登录失败: ${response.status} ${response.statusText}`)
  }
  
  return await response.json()
}