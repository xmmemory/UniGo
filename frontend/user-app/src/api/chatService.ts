import API_BASE_URL from '../api/config'
import { fetchWithAuth } from '../utils/apiErrorHandler'

// 获取聊天消息
export const getChatMessages = async (tripId: number) => {
  // 获取认证token
  const token = localStorage.getItem('token')
  
  const response = await fetchWithAuth(
    `${API_BASE_URL}/api/v1/chat/trips/${tripId}/messages`,
    token || '',
    {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    }
  )
  
  if (!response.ok) {
    throw new Error(`获取聊天消息失败: ${response.status} ${response.statusText}`)
  }
  
  return await response.json()
}

// 发送聊天消息
export const sendChatMessage = async (tripId: number, content: string) => {
  // 获取认证token
  const token = localStorage.getItem('token')
  
  const response = await fetchWithAuth(
    `${API_BASE_URL}/api/v1/chat/trips/${tripId}/messages`,
    token || '',
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ content }),
    }
  )
  
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}))
    throw new Error(errorData.detail || `发送消息失败: ${response.status} ${response.statusText}`)
  }
  
  return await response.json()
}