<template>
  <div class="register">
    <div class="register-container">
      <h1>用户注册</h1>
      <form @submit.prevent="register">
        <div class="form-group">
          <label for="username">用户名</label>
          <input 
            type="text" 
            id="username" 
            v-model="registerForm.username" 
            required 
            placeholder="请输入用户名"
            minlength="3"
            maxlength="20"
          >
        </div>
        <div class="form-group">
          <label for="email">邮箱</label>
          <input 
            type="email" 
            id="email" 
            v-model="registerForm.email" 
            required 
            placeholder="请输入邮箱"
          >
        </div>
        <div class="form-group">
          <label for="password">密码</label>
          <input 
            type="password" 
            id="password" 
            v-model="registerForm.password" 
            required 
            placeholder="请输入密码"
            minlength="6"
          >
        </div>
        <div class="form-group">
          <label for="confirmPassword">确认密码</label>
          <input 
            type="password" 
            id="confirmPassword" 
            v-model="registerForm.confirmPassword" 
            required 
            placeholder="请再次输入密码"
          >
        </div>
        <div class="form-group">
          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? '注册中...' : '注册' }}
          </button>
        </div>
      </form>
      <div class="register-footer">
        <p>已有账户？<router-link to="/login">立即登录</router-link></p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { registerUser } from '@/api/userService'

// 状态管理
const registerForm = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const loading = ref(false)
const router = useRouter()

// 监听密码确认字段
watch(() => registerForm.value.confirmPassword, (newVal) => {
  if (newVal && newVal !== registerForm.value.password) {
    // 这里可以显示密码不匹配的提示
    console.log('密码不匹配')
  }
})

// 注册函数
const register = async () => {
  // 验证密码是否匹配
  if (registerForm.value.password !== registerForm.value.confirmPassword) {
    alert('两次输入的密码不一致')
    return
  }
  
  loading.value = true
  try {
    // 调用API进行注册
    const userData = {
      username: registerForm.value.username,
      email: registerForm.value.email,
      password: registerForm.value.password
    }
    
    await registerUser(userData)
    
    // 注册成功
    alert('注册成功！请登录')
    
    // 跳转到登录页
    router.push('/login')
  } catch (error) {
    console.error('注册失败:', error)
    alert('注册失败，请稍后重试')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 70vh;
  padding: 1rem;
}

.register-container {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.register-container h1 {
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

.register-footer {
  text-align: center;
  margin-top: 1.5rem;
  font-size: 0.9rem;
}

.register-footer a {
  color: #42b883;
  text-decoration: none;
}

.register-footer a:hover {
  text-decoration: underline;
}

/* 平板和桌面端适配 */
@media (min-width: 768px) {
  .register {
    padding: 2rem;
  }
  
  .register-container {
    padding: 2rem;
  }
  
  .register-container h1 {
    font-size: 2rem;
    margin-bottom: 2rem;
  }
  
  .form-group {
    margin-bottom: 1.5rem;
  }
  
  .form-group label {
    font-size: 1rem;
  }
  
  .register-footer {
    font-size: 1rem;
  }
}
</style>