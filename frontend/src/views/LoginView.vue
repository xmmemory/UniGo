<template>
  <div class="login">
    <div class="login-container">
      <h1>用户登录</h1>
      <form @submit.prevent="login">
        <div class="form-group">
          <label for="username">用户名或邮箱</label>
          <input 
            type="text" 
            id="username" 
            v-model="loginForm.username" 
            required 
            placeholder="请输入用户名或邮箱"
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
      <div class="login-footer">
        <p>还没有账户？<router-link to="/register">立即注册</router-link></p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { loginUser } from '@/api/userService'

// 状态管理
const loginForm = ref({
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
    
    const response = await loginUser(credentials)
    
    // 登录成功，保存token到localStorage
    localStorage.setItem('token', response.access_token)
    
    alert('登录成功！')
    
    // 跳转到首页
    router.push('/')
  } catch (error) {
    console.error('登录失败:', error)
    alert('登录失败，请检查用户名和密码')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 70vh;
  padding: 1rem;
}

.login-container {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.login-container h1 {
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

.login-footer {
  text-align: center;
  margin-top: 1.5rem;
  font-size: 0.9rem;
}

.login-footer a {
  color: #42b883;
  text-decoration: none;
}

.login-footer a:hover {
  text-decoration: underline;
}

/* 平板和桌面端适配 */
@media (min-width: 768px) {
  .login {
    padding: 2rem;
  }
  
  .login-container {
    padding: 2rem;
  }
  
  .login-container h1 {
    font-size: 2rem;
    margin-bottom: 2rem;
  }
  
  .form-group {
    margin-bottom: 1.5rem;
  }
  
  .form-group label {
    font-size: 1rem;
  }
  
  .login-footer {
    font-size: 1rem;
  }
}
</style>