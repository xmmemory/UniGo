import { useAuthStore } from '@/stores/auth'
import router from '@/router'

// 检查响应是否为401 Unauthorized错误
export const isUnauthorizedError = (response: Response): boolean => {
  return response.status === 401
}

// 处理API错误，如果是401错误则登出并跳转到登录页面
export const handleApiError = async (response: Response, error: any): Promise<void> => {
  const authStore = useAuthStore()
  
  // 检查是否为401 Unauthorized错误
  if (isUnauthorizedError(response)) {
    // 清除本地存储的token
    authStore.logout()
    
    // 跳转到登录页面
    if (router) {
      router.push('/login')
    }
    
    // 抛出自定义错误信息
    throw new Error('您的登录已过期，请重新登录')
  }
  
  // 其他错误处理
  throw error
}

// 刷新token的函数（需要后端支持）
export const refreshToken = async (): Promise<string | null> => {
  try {
    const authStore = useAuthStore()
    
    // 检查是否有当前token
    if (!authStore.token) {
      return null
    }
    
    // 调用后端的刷新token接口
    const response = await fetch('/api/refresh-token/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${authStore.token}`,
        'Content-Type': 'application/json',
      },
    })
    
    if (!response.ok) {
      throw new Error('Token refresh failed')
    }
    
    const data = await response.json()
    return data.access_token
  } catch (error) {
    console.error('Token refresh failed:', error)
    return null
  }
}

// 带自动重试的fetch包装函数
export const fetchWithAuth = async (url: string, options: RequestInit = {}) => {
  const authStore = useAuthStore()
  
  // 添加认证头
  const headers = new Headers(options.headers || {})
  if (authStore.token) {
    headers.set('Authorization', `Bearer ${authStore.token}`)
  }
  
  // 更新options
  const updatedOptions = {
    ...options,
    headers,
  }
  
  try {
    // 发起请求
    const response = await fetch(url, updatedOptions)
    
    // 检查是否为401错误
    if (isUnauthorizedError(response)) {
      // 尝试刷新token
      const newToken = await refreshToken()
      
      if (newToken) {
        // 使用新token重新发起请求
        headers.set('Authorization', `Bearer ${newToken}`)
        const retryResponse = await fetch(url, {
          ...updatedOptions,
          headers,
        })
        
        if (isUnauthorizedError(retryResponse)) {
          // 如果刷新后仍然401，登出用户
          authStore.logout()
          if (router) {
            router.push('/login')
          }
          throw new Error('您的登录已过期，请重新登录')
        }
        
        return retryResponse
      } else {
        // 刷新失败，登出用户
        authStore.logout()
        if (router) {
          router.push('/login')
        }
        throw new Error('您的登录已过期，请重新登录')
      }
    }
    
    return response
  } catch (error) {
    throw error
  }
}