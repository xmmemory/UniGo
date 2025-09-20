import API_BASE_URL from '../api/config'
import { fetchWithAuth } from '../utils/apiErrorHandler'

// 获取跑腿任务列表
export const getErrandTasks = async (params: {
  page?: number
  limit?: number
  keyword?: string
  status?: string
  reward_range?: string
}) => {
  const queryParams = new URLSearchParams()
  // 将page转换为skip参数
  if (params.page) queryParams.append('skip', ((params.page - 1) * (params.limit || 10)).toString())
  if (params.limit) queryParams.append('limit', params.limit.toString())
  if (params.keyword) queryParams.append('keyword', params.keyword)
  if (params.status) queryParams.append('status', params.status)
  if (params.reward_range) queryParams.append('reward_range', params.reward_range)
  
  const response = await fetch(`${API_BASE_URL}/api/v1/errands/?${queryParams}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  })
  
  if (!response.ok) {
    throw new Error(`获取跑腿任务失败: ${response.status} ${response.statusText}`)
  }
  
  return await response.json()
}

// 获取跑腿任务详情
export const getErrandTaskDetail = async (taskId: number) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/errands/${taskId}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  })
  
  if (!response.ok) {
    throw new Error(`获取任务详情失败: ${response.status} ${response.statusText}`)
  }
  
  return await response.json()
}

// 创建跑腿任务
export const createErrandTask = async (taskData: {
  title: string
  description: string
  reward: number
  deadline: string
  location: string
}) => {
  // 获取认证token
  const token = localStorage.getItem('token')
  
  const response = await fetchWithAuth(
    `${API_BASE_URL}/api/v1/errands/`,
    token || '',
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(taskData),
    }
  )
  
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}))
    throw new Error(errorData.detail || `发布任务失败: ${response.status} ${response.statusText}`)
  }
  
  return await response.json()
}

// 接取跑腿任务
export const acceptErrandTask = async (taskId: number) => {
  // 获取认证token
  const token = localStorage.getItem('token')
  
  const response = await fetchWithAuth(
    `${API_BASE_URL}/api/v1/errands/${taskId}/accept`,
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
    throw new Error(errorData.detail || `接取任务失败: ${response.status} ${response.statusText}`)
  }
  
  return await response.json()
}

// 完成跑腿任务
export const completeErrandTask = async (taskId: number) => {
  // 获取认证token
  const token = localStorage.getItem('token')
  
  const response = await fetchWithAuth(
    `${API_BASE_URL}/api/v1/errands/${taskId}/complete`,
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
    throw new Error(errorData.detail || `完成任务失败: ${response.status} ${response.statusText}`)
  }
  
  return await response.json()
}

// 取消跑腿任务
export const cancelErrandTask = async (taskId: number) => {
  // 获取认证token
  const token = localStorage.getItem('token')
  
  const response = await fetchWithAuth(
    `${API_BASE_URL}/api/v1/errands/${taskId}/cancel`,
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
    throw new Error(errorData.detail || `取消任务失败: ${response.status} ${response.statusText}`)
  }
  
  return await response.json()
}