<template>
  <div class="admin-login">
    <div class="admin-login-container">
      <h1>管理员登录</h1>
      <form @submit.prevent="login">
        <div class="form-group">
          <label for="username">管理员用户名</label>
          <input 
            type="text" 
            id="username" 
            v-model="loginForm.username" 
            required 
            placeholder="请输入管理员用户名"
          >
        </div>
        <div class="form-group">
          <label for="password">密码</label>
          <input 
            type="password" 
            id="password" 
            v-model="loginForm.password" 
            required 
            placeholder="请输入密码"
          >
        </div>
        <div class="form-group">
          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? '登录中...' : '登录' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { adminLoginUser } from '../api/adminService'

// 定义登录表单数据结构
interface LoginForm {
  username: string
  password: string
}

// 状态管理
const loginForm = ref<LoginForm>({
  username: '',
  password: ''
})
const loading = ref(false)
const router = useRouter()

// 登录函数
const login = async () => {
  loading.value = true
  try {
    // 调用API进行登录
    const credentials = {
      username: loginForm.value.username,
      password: loginForm.value.password
    }
    
    const response = await adminLoginUser(credentials)
    
    // 保存token到localStorage
    localStorage.setItem('admin_token', response.access_token)
    
    // 跳转到管理员后台首页
    router.push('/admin/dashboard')
  } catch (error: any) {
    console.error('管理员登录失败:', error)
    
    // 根据错误类型显示不同的提示信息
    if (error.message.includes('数据库连接失败')) {
      alert('服务器暂时不可用，请稍后重试')
    } else if (error.message.includes('用户名或密码错误')) {
      alert('管理员用户名或密码错误，请检查后重试')
    } else if (error.message.includes('网络连接失败')) {
      alert('网络连接失败，请确保后端服务正在运行')
    } else {
      alert('登录失败，请检查用户名和密码')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.admin-login {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 200px);
  padding: 1rem;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

.admin-login-container {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  margin: auto;
}

.admin-login-container h1 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #42b883;
  font-size: 1.5rem;
}

.form-group {
  margin-bottom: 1.2rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
  font-size: 0.9rem;
}

.form-group input {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  box-sizing: border-box;
  font-size: 1rem;
}

.btn {
  width: 100%;
  padding: 1rem;
  border-radius: 6px;
  text-decoration: none;
  font-weight: bold;
  transition: opacity 0.3s;
  border: none;
  cursor: pointer;
  font-size: 1rem;
}

.btn:hover {
  opacity: 0.9;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background-color: #42b883;
  color: white;
}

/* 平板和桌面端适配 */
@media (min-width: 768px) {
  .admin-login {
    padding: 2rem;
    min-height: calc(100vh - 300px);
  }
  
  .admin-login-container {
    padding: 2rem;
  }
  
  .admin-login-container h1 {
    font-size: 2rem;
    margin-bottom: 2rem;
  }
  
  .form-group {
    margin-bottom: 1.5rem;
  }
  
  .form-group label {
    font-size: 1rem;
  }
}
</style>