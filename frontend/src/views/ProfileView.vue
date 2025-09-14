<template>
  <div class="profile">
    <h1>个人中心</h1>
    
    <div class="profile-content">
      <div class="profile-info">
        <div class="avatar">
          <img src="@/assets/logo.svg" alt="头像">
        </div>
        <div class="user-details">
          <h2>{{ user?.username || '加载中...' }}</h2>
          <p>{{ user?.email || '加载中...' }}</p>
          <p>注册时间: {{ user ? formatDate(user.created_at) : '加载中...' }}</p>
        </div>
      </div>
      
      <div class="profile-actions">
        <button class="btn btn-primary" @click="showEditForm = true">编辑资料</button>
        <button class="btn btn-secondary" @click="logout">退出登录</button>
      </div>
    </div>
    
    <div class="profile-sections">
      <div class="section">
        <h3>我的支付记录</h3>
        <div class="payments-list">
          <div class="payment-card" v-for="payment in payments" :key="payment.id">
            <div class="payment-header">
              <span class="payment-amount">¥{{ payment.amount }}</span>
              <span class="payment-status" :class="payment.status">{{ payment.status }}</span>
            </div>
            <div class="payment-details">
              <p><strong>支付时间:</strong> {{ formatDate(payment.payment_date) }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="history-link">
      <router-link to="/history" class="btn btn-primary">查看历史订单</router-link>
    </div>
    
    <!-- 编辑资料表单 -->
    <div class="modal" v-if="showEditForm">
      <div class="modal-content">
        <span class="close" @click="showEditForm = false">&times;</span>
        <h2>编辑个人资料</h2>
        <form @submit.prevent="updateProfile">
          <div class="form-group">
            <label for="username">用户名</label>
            <input type="text" id="username" v-model="editUser.username" required>
          </div>
          <div class="form-group">
            <label for="email">邮箱</label>
            <input type="email" id="email" v-model="editUser.email" required>
          </div>
          <div class="form-group">
            <label for="password">新密码 (留空则不修改)</label>
            <input type="password" id="password" v-model="editUser.password">
          </div>
          <button type="submit" class="btn btn-primary">保存</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getUserById } from '@/api/userService'
import { useAuthStore } from '@/stores/auth'

// 状态管理
const user = ref<any>(null)
const editUser = ref({
  username: '',
  email: '',
  password: ''
})
const payments = ref<any[]>([])
const showEditForm = ref(false)
const router = useRouter()
const authStore = useAuthStore()

// 格式化日期
const formatDate = (dateString: string) => {
  try {
    const date = new Date(dateString)
    return date.toLocaleString('zh-CN')
  } catch (e) {
    console.error('日期格式化错误:', e)
    return '无效日期'
  }
}

// 更新用户资料
const updateProfile = async () => {
  try {
    // 这里应该调用API更新用户信息
    // 暂时只更新本地状态
    if (user.value) {
      user.value.username = editUser.value.username
      user.value.email = editUser.value.email
      authStore.setUser(user.value)
    }
    showEditForm.value = false
    alert('用户信息更新成功')
  } catch (error: any) {
    console.error('更新用户信息失败:', error)
    if (error.message && error.message.includes('登录')) {
      alert(error.message)
      authStore.logout()
      router.push('/login')
    } else {
      alert('更新用户信息失败')
    }
  }
}

// 登出
const logout = () => {
  authStore.logout()
  router.push('/login')
}

// 加载用户数据
const loadUserData = async () => {
  try {
    // 从认证存储中获取当前用户信息
    if (authStore.user) {
      user.value = authStore.user
      editUser.value.username = authStore.user.username
      editUser.value.email = authStore.user.email
    } else if (authStore.token && authStore.user?.id) {
      // 如果认证存储中没有用户信息但有token，从API获取
      const userData = await getUserById(authStore.user.id, authStore.token)
      user.value = userData
      editUser.value.username = userData.username
      editUser.value.email = userData.email
      // 更新authStore中的用户信息
      authStore.setUser(userData)
    } else {
      // 如果没有用户信息且没有token，重定向到登录页面
      console.warn('没有用户信息且没有token，重定向到登录页面')
      authStore.logout()
      router.push('/login')
      return
    }
    
    // 这里应该调用API获取支付记录
    // 暂时使用模拟数据
    payments.value = [
      {
        id: 1,
        amount: 150,
        payment_date: '2025-09-03T10:30:00',
        status: 'paid'
      }
    ]
  } catch (error: any) {
    console.error('加载用户数据失败:', error)
    if (error.message && error.message.includes('登录')) {
      alert(error.message)
      authStore.logout()
      router.push('/login')
    } else {
      alert('加载用户数据失败')
    }
  }
}

// 组件挂载时加载数据
onMounted(() => {
  loadUserData()
})
</script>

<style scoped>
.profile {
  padding: 1rem 0;
}

.profile-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.profile-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.avatar img {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
}

.user-details h2 {
  margin: 0 0 0.3rem 0;
  font-size: 1.3rem;
}

.user-details p {
  margin: 0.3rem 0;
  font-size: 0.9rem;
}

.profile-actions {
  display: flex;
  gap: 1rem;
}

.profile-sections {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.section h3 {
  margin-bottom: 1rem;
  color: #42b883;
  font-size: 1.2rem;
}

.payments-list {
  display: grid;
  gap: 1rem;
}

.payment-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.payment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.payment-amount {
  font-size: 1.1rem;
  font-weight: bold;
  color: #e74c3c;
}

.payment-status {
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: bold;
}

.payment-status.paid {
  background-color: #d4edda;
  color: #155724;
}

.payment-status.pending {
  background-color: #fff3cd;
  color: #856404;
}

.payment-details p {
  margin: 0.3rem 0;
  font-size: 0.9rem;
}

.history-link {
  margin-top: 2rem;
  text-align: center;
}

/* Modal 样式 */
.modal {
  position: fixed;
  z-index: 1000;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem;
}

.modal-content {
  background-color: white;
  padding: 1.5rem;
  border-radius: 8px;
  width: 95%;
  max-width: 500px;
  position: relative;
  max-height: 90vh;
  overflow-y: auto;
}

.close {
  position: absolute;
  right: 1rem;
  top: 1rem;
  font-size: 2rem;
  cursor: pointer;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

.form-group input {
  width: 100%;
  padding: 0.7rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  box-sizing: border-box;
  font-size: 1rem;
}

.btn {
  padding: 0.8rem 1.2rem;
  border-radius: 6px;
  text-decoration: none;
  font-weight: bold;
  transition: opacity 0.3s;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  width: 100%;
  display: inline-block;
  text-align: center;
}

.btn:hover {
  opacity: 0.9;
}

.btn-primary {
  background-color: #42b883;
  color: white;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

/* 平板和桌面端适配 */
@media (min-width: 768px) {
  .profile {
    padding: 2rem 0;
  }
  
  .profile-content {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 3rem;
    gap: 2rem;
  }
  
  .profile-info {
    gap: 2rem;
  }
  
  .avatar img {
    width: 100px;
    height: 100px;
  }
  
  .user-details h2 {
    font-size: 1.5rem;
  }
  
  .user-details p {
    font-size: 1rem;
  }
  
  .profile-actions {
    flex-direction: column;
  }
  
  .profile-sections {
    flex-direction: row;
    gap: 3rem;
  }
  
  .section h3 {
    font-size: 1.5rem;
  }
  
  .payment-header {
    flex-wrap: nowrap;
  }
  
  .payment-status {
    font-size: 0.8rem;
  }
  
  .payment-details p {
    font-size: 1rem;
  }
  
  .modal-content {
    padding: 2rem;
    width: 90%;
  }
  
  .btn {
    width: auto;
    padding: 0.8rem 1.5rem;
  }
}

@media (min-width: 1024px) {
  .profile-sections {
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  }
}
</style>