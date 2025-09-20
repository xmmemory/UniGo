<template>
  <div class="register-container">
    <div class="register-form">
      <h2>用户注册</h2>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="username">用户名</label>
          <input
            id="username"
            v-model="registerForm.username"
            type="text"
            placeholder="请输入用户名"
            required
          />
          <div v-if="usernameError" class="error-message">{{ usernameError }}</div>
        </div>
        
        <div class="form-group">
          <label for="email">邮箱</label>
          <input
            id="email"
            v-model="registerForm.email"
            type="email"
            placeholder="请输入邮箱"
            required
          />
          <div v-if="emailError" class="error-message">{{ emailError }}</div>
        </div>
        
        <div class="form-group">
          <label for="password">密码</label>
          <input
            id="password"
            v-model="registerForm.password"
            type="password"
            placeholder="请输入密码"
            required
            @input="checkPasswordStrength"
          />
          <div class="password-strength" v-if="passwordStrength">
            <div class="strength-bar">
              <div 
                class="strength-fill" 
                :class="passwordStrengthClass"
                :style="{ width: passwordStrengthPercentage + '%' }"
              ></div>
            </div>
            <div class="strength-text">{{ passwordStrengthText }}</div>
          </div>
          <div v-if="passwordError" class="error-message">{{ passwordError }}</div>
        </div>
        
        <div class="form-group">
          <label for="confirmPassword">确认密码</label>
          <input
            id="confirmPassword"
            v-model="registerForm.confirmPassword"
            type="password"
            placeholder="请再次输入密码"
            required
          />
          <div v-if="confirmPasswordError" class="error-message">{{ confirmPasswordError }}</div>
        </div>
        
        <button type="submit" class="btn-register" :disabled="isLoading || !isFormValid">
          {{ isLoading ? '注册中...' : '注册' }}
        </button>
      </form>
      
      <div class="form-footer">
        <p>已有账户？<router-link to="/login">立即登录</router-link></p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { registerUser } from '../api/userService'

const router = useRouter()

const registerForm = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const isLoading = ref(false)
const usernameError = ref('')
const emailError = ref('')
const passwordError = ref('')
const confirmPasswordError = ref('')

// 密码强度相关
const passwordStrength = ref(0)
const passwordStrengthText = ref('')
const passwordStrengthClass = ref('')

// 验证用户名格式
const validateUsername = (username: string): boolean => {
  const usernameRegex = /^[a-zA-Z0-9_]+$/
  return usernameRegex.test(username) && username.length >= 3 && username.length <= 20
}

// 验证邮箱格式
const validateEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

// 验证密码强度
const validatePasswordStrength = (password: string): { score: number; text: string; class: string; errors: string[] } => {
  let score = 0
  const errors: string[] = []
  
  if (password.length >= 8) score += 1
  else errors.push('至少8个字符')
  
  if (/[A-Z]/.test(password)) score += 1
  else errors.push('至少一个大写字母')
  
  if (/[a-z]/.test(password)) score += 1
  else errors.push('至少一个小写字母')
  
  if (/\d/.test(password)) score += 1
  else errors.push('至少一个数字')
  
  if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) score += 1
  else errors.push('至少一个特殊字符')
  
  let text = ''
  let className = ''
  
  switch (score) {
    case 0:
    case 1:
      text = '很弱'
      className = 'very-weak'
      break
    case 2:
      text = '弱'
      className = 'weak'
      break
    case 3:
      text = '一般'
      className = 'medium'
      break
    case 4:
      text = '强'
      className = 'strong'
      break
    case 5:
      text = '很强'
      className = 'very-strong'
      break
    default:
      text = ''
      className = ''
  }
  
  return {
    score,
    text,
    class: className,
    errors
  }
}

// 检查密码强度
const checkPasswordStrength = () => {
  if (registerForm.password) {
    const result = validatePasswordStrength(registerForm.password)
    passwordStrength.value = result.score
    passwordStrengthText.value = result.text
    passwordStrengthClass.value = result.class
  } else {
    passwordStrength.value = 0
    passwordStrengthText.value = ''
    passwordStrengthClass.value = ''
  }
}

// 计算密码强度百分比
const passwordStrengthPercentage = computed(() => {
  return (passwordStrength.value / 5) * 100
})

// 表单验证
const isFormValid = computed(() => {
  return (
    registerForm.username &&
    registerForm.email &&
    registerForm.password &&
    registerForm.confirmPassword &&
    !usernameError.value &&
    !emailError.value &&
    !passwordError.value &&
    !confirmPasswordError.value
  )
})

// 监听表单变化进行实时验证
const validateForm = () => {
  // 验证用户名
  if (registerForm.username) {
    if (!validateUsername(registerForm.username)) {
      usernameError.value = '用户名只能包含字母、数字和下划线，长度为3-20个字符'
    } else {
      usernameError.value = ''
    }
  } else {
    usernameError.value = ''
  }
  
  // 验证邮箱
  if (registerForm.email) {
    if (!validateEmail(registerForm.email)) {
      emailError.value = '请输入有效的邮箱地址'
    } else {
      emailError.value = ''
    }
  } else {
    emailError.value = ''
  }
  
  // 验证密码
  if (registerForm.password) {
    const passwordValidation = validatePasswordStrength(registerForm.password)
    if (passwordValidation.score < 3) {
      passwordError.value = '密码强度不足：' + passwordValidation.errors.join('，')
    } else {
      passwordError.value = ''
    }
  } else {
    passwordError.value = ''
  }
  
  // 验证确认密码
  if (registerForm.confirmPassword) {
    if (registerForm.password !== registerForm.confirmPassword) {
      confirmPasswordError.value = '两次输入的密码不一致'
    } else {
      confirmPasswordError.value = ''
    }
  } else {
    confirmPasswordError.value = ''
  }
}

const handleRegister = async () => {
  // 最终验证
  validateForm()
  
  if (!isFormValid.value) {
    alert('请检查表单填写是否正确')
    return
  }
  
  isLoading.value = true
  try {
    await registerUser({
      username: registerForm.username,
      email: registerForm.email,
      password: registerForm.password
    })
    alert('注册成功！请登录')
    router.push('/login')
  } catch (error: any) {
    alert(error.message || '注册失败')
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 200px);
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.register-form {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.register-form h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #42b883;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  box-sizing: border-box;
}

.form-group input:focus {
  outline: none;
  border-color: #42b883;
}

.error-message {
  color: #e74c3c;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.password-strength {
  margin-top: 0.5rem;
}

.strength-bar {
  width: 100%;
  height: 8px;
  background-color: #eee;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 0.25rem;
}

.strength-fill {
  height: 100%;
  transition: width 0.3s ease;
}

.strength-fill.very-weak {
  background-color: #e74c3c;
}

.strength-fill.weak {
  background-color: #f39c12;
}

.strength-fill.medium {
  background-color: #f1c40f;
}

.strength-fill.strong {
  background-color: #2ecc71;
}

.strength-fill.very-strong {
  background-color: #27ae60;
}

.strength-text {
  font-size: 0.875rem;
  color: #666;
}

.btn-register {
  width: 100%;
  padding: 0.75rem;
  background-color: #42b883;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-top: 1rem;
}

.btn-register:hover:not(:disabled) {
  background-color: #359c6d;
}

.btn-register:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.form-footer {
  text-align: center;
  margin-top: 1.5rem;
}

.form-footer a {
  color: #42b883;
  text-decoration: none;
}

.form-footer a:hover {
  text-decoration: underline;
}
</style>