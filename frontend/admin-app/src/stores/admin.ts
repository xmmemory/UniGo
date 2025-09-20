import { defineStore } from 'pinia'

// 定义管理员信息接口
interface Admin {
  id: number
  username: string
  email: string
  role: string
  created_at: string
  last_login: string | null
  is_active: boolean
}

// 定义状态接口
interface AdminState {
  admin: Admin | null
  token: string | null
  isAuthenticated: boolean
}

export const useAdminStore = defineStore('admin', {
  state: (): AdminState => ({
    admin: null,
    token: localStorage.getItem('admin_token'),
    isAuthenticated: !!localStorage.getItem('admin_token')
  }),
  
  getters: {
    isAdminAuthenticated: (state) => state.isAuthenticated,
    adminToken: (state) => state.token,
    currentAdmin: (state) => state.admin
  },
  
  actions: {
    setAdmin(admin: Admin) {
      this.admin = admin
    },
    
    setToken(token: string) {
      this.token = token
      localStorage.setItem('admin_token', token)
      this.isAuthenticated = true
    },
    
    clearAuth() {
      this.admin = null
      this.token = null
      this.isAuthenticated = false
      localStorage.removeItem('admin_token')
    },
    
    logout() {
      this.clearAuth()
    },
    
    async initializeAuth() {
      const token = localStorage.getItem('admin_token')
      if (token) {
        this.setToken(token)
        // 这里可以添加获取管理员信息的逻辑
      }
    }
  }
})