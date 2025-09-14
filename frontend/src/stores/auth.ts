import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getCurrentUser } from '@/api/userService'

export const useAuthStore = defineStore('auth', () => {
  // 状态
  const user = ref<any>(null)
  const token = ref<string | null>(null)
  
  // 计算属性
  const isAuthenticated = computed(() => !!token.value)
  
  // 动作
  const setToken = (newToken: string | null) => {
    token.value = newToken
    if (newToken) {
      localStorage.setItem('token', newToken)
    } else {
      localStorage.removeItem('token')
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
  
  const login = (newToken: string, newUser: any) => {
    setToken(newToken)
    setUser(newUser)
  }
  
  const logout = () => {
    setToken(null)
    setUser(null)
  }
  
  const initializeAuth = async () => {
    // 从localStorage恢复认证状态
    const savedToken = localStorage.getItem('token')
    const savedUser = localStorage.getItem('user')
    
    if (savedToken) {
      token.value = savedToken
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
  
  return {
    // 状态
    user,
    token,
    isAuthenticated,
    
    // 动作
    setToken,
    setUser,
    login,
    logout,
    initializeAuth,
    refreshUser
  }
})