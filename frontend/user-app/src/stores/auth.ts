import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getCurrentUser } from '../api/userService'
import API_BASE_URL from '../api/config'

// 从localStorage获取存储的令牌
const getStoredToken = () => {
  return localStorage.getItem('token')
}

const getStoredRefreshToken = () => {
  return localStorage.getItem('refreshToken')
}

export const useAuthStore = defineStore('auth', () => {
  // 状态
  const user = ref<any>(null)
  const token = ref<string | null>(getStoredToken())
  const refreshToken = ref<string | null>(getStoredRefreshToken())
  const tokenExpiry = ref<number | null>(parseInt(localStorage.getItem('tokenExpiry') || '0'))
  
  // 计算属性
  const isAuthenticated = computed(() => !!token.value)
  
  // 检查令牌是否即将过期（5分钟内）
  const isTokenExpiringSoon = computed(() => {
    if (!tokenExpiry.value) return true
    const now = Date.now()
    const fiveMinutes = 5 * 60 * 1000
    return (tokenExpiry.value - now) < fiveMinutes
  })
  
  // 动作
  const setToken = (newToken: string | null) => {
    token.value = newToken
    if (newToken) {
      localStorage.setItem('token', newToken)
      
      // 解析JWT令牌获取过期时间
      try {
        const payload = JSON.parse(atob(newToken.split('.')[1]))
        tokenExpiry.value = payload.exp * 1000 // 转换为毫秒
        localStorage.setItem('tokenExpiry', tokenExpiry.value.toString())
      } catch (e) {
        console.error('Failed to parse token', e)
        tokenExpiry.value = null
        localStorage.removeItem('tokenExpiry')
      }
    } else {
      localStorage.removeItem('token')
      localStorage.removeItem('tokenExpiry')
      tokenExpiry.value = null
    }
  }
  
  const setRefreshToken = (newRefreshToken: string | null) => {
    refreshToken.value = newRefreshToken
    if (newRefreshToken) {
      localStorage.setItem('refreshToken', newRefreshToken)
    } else {
      localStorage.removeItem('refreshToken')
    }
  }
  
  const setUser = (newUser: any | null) => {
    user.value = newUser
    if (newUser) {
      localStorage.setItem('user', JSON.stringify(newUser))
    } else {
      localStorage.removeItem('user')
    }
  }
  
  const login = (newToken: string, newRefreshToken: string, newUser: any) => {
    setToken(newToken)
    setRefreshToken(newRefreshToken)
    setUser(newUser)
  }
  
  const logout = () => {
    setToken(null)
    setRefreshToken(null)
    setUser(null)
  }
  
  const initializeAuth = async () => {
    // 从localStorage恢复认证状态
    const savedToken = getStoredToken()
    const savedRefreshToken = getStoredRefreshToken()
    const savedUser = localStorage.getItem('user')
    
    if (savedToken) {
      token.value = savedToken
      // 解析JWT令牌获取过期时间
      try {
        const payload = JSON.parse(atob(savedToken.split('.')[1]))
        tokenExpiry.value = payload.exp * 1000 // 转换为毫秒
      } catch (e) {
        console.error('Failed to parse token', e)
        tokenExpiry.value = null
      }
    }
    
    if (savedRefreshToken) {
      refreshToken.value = savedRefreshToken
    }
    
    if (savedUser) {
      try {
        user.value = JSON.parse(savedUser)
      } catch (e) {
        console.error('Failed to parse user from localStorage', e)
        localStorage.removeItem('user')
      }
    }
    
    // 如果有token但没有用户信息，尝试获取用户信息
    if (token.value && !user.value) {
      try {
        const currentUser = await getCurrentUser(token.value)
        setUser(currentUser)
      } catch (e) {
        console.error('Failed to fetch user info', e)
        logout()
      }
    }
  }
  
  const refreshUser = async () => {
    if (token.value) {
      try {
        const currentUser = await getCurrentUser(token.value)
        setUser(currentUser)
        return currentUser
      } catch (e) {
        console.error('Failed to refresh user info', e)
        logout()
        throw e
      }
    }
  }
  
  // 刷新访问令牌
  const refreshAccessToken = async (): Promise<string | null> => {
    if (!refreshToken.value) {
      logout()
      return null
    }
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/refresh-token/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${refreshToken.value}`
        }
      })
      
      if (!response.ok) {
        throw new Error('Failed to refresh token')
      }
      
      const data = await response.json()
      setToken(data.access_token)
      return data.access_token
    } catch (e) {
      console.error('Failed to refresh access token', e)
      logout()
      return null
    }
  }
  
  return {
    // 状态
    user,
    token,
    refreshToken,
    isAuthenticated,
    isTokenExpiringSoon,
    
    // 动作
    setToken,
    setRefreshToken,
    setUser,
    login,
    logout,
    initializeAuth,
    refreshUser,
    refreshAccessToken
  }
})