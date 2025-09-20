<template>
  <div class="profile-container">
    <h1>个人中心</h1>
    
    <div class="profile-content">
      <div class="profile-sidebar">
        <div class="user-info">
          <div class="avatar">
            <i class="avatar-icon">👤</i>
          </div>
          <h2>{{ user?.username }}</h2>
          <p>{{ user?.email }}</p>
        </div>
        
        <nav class="profile-nav">
          <ul>
            <li>
              <router-link to="/profile" exact-active-class="active">个人信息</router-link>
            </li>
            <li>
              <router-link to="/bookings" exact-active-class="active">我的预订</router-link>
            </li>
            <li>
              <router-link to="/history" exact-active-class="active">历史记录</router-link>
            </li>
            <li>
              <router-link to="/publish-trip" exact-active-class="active">发布行程</router-link>
            </li>
            <li>
              <router-link to="/publish-secondhand" exact-active-class="active">发布二手物品</router-link>
            </li>
            <li>
              <router-link to="/publish-errand" exact-active-class="active">发布跑腿任务</router-link>
            </li>
          </ul>
        </nav>
        
        <button class="btn-logout" @click="logout">退出登录</button>
      </div>
      
      <div class="profile-main">
        <div class="profile-section">
          <h2>个人信息</h2>
          
          <form @submit.prevent="updateProfile" class="profile-form">
            <div class="form-row">
              <div class="form-group">
                <label for="fullName">姓名</label>
                <input
                  id="fullName"
                  v-model="profileForm.full_name"
                  type="text"
                  placeholder="请输入姓名"
                />
              </div>
              
              <div class="form-group">
                <label for="phoneNumber">手机号</label>
                <input
                  id="phoneNumber"
                  v-model="profileForm.phone_number"
                  type="tel"
                  placeholder="请输入手机号"
                />
              </div>
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label for="studentId">学号</label>
                <input
                  id="studentId"
                  v-model="profileForm.student_id"
                  type="text"
                  placeholder="请输入学号"
                />
              </div>
              
              <div class="form-group">
                <label for="university">学校</label>
                <input
                  id="university"
                  v-model="profileForm.university"
                  type="text"
                  placeholder="请输入学校名称"
                />
              </div>
            </div>
            
            <div class="form-actions">
              <button type="submit" class="btn-save" :disabled="updating">
                {{ updating ? '保存中...' : '保存信息' }}
              </button>
            </div>
          </form>
        </div>
        
        <div class="profile-section">
          <h2>账户安全</h2>
          
          <div class="security-actions">
            <button class="btn-change-password" @click="changePassword">
              修改密码
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { updateUserProfile } from '../api/userService'

const router = useRouter()
const authStore = useAuthStore()

const user = computed(() => authStore.user)
const updating = ref(false)

const profileForm = ref({
  full_name: '',
  phone_number: '',
  student_id: '',
  university: ''
})

// 更新表单数据
const updateFormFromUser = () => {
  if (user.value) {
    profileForm.value.full_name = user.value.full_name || ''
    profileForm.value.phone_number = user.value.phone_number || ''
    profileForm.value.student_id = user.value.student_id || ''
    profileForm.value.university = user.value.university || ''
  }
}

// 更新个人信息
const updateProfile = async () => {
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }
  
  updating.value = true
  try {
    const response = await updateUserProfile(profileForm.value)
    authStore.setUser(response)
    alert('个人信息更新成功')
  } catch (error: any) {
    alert(error.message || '更新个人信息失败')
  } finally {
    updating.value = false
  }
}

// 修改密码
const changePassword = () => {
  alert('跳转到修改密码页面')
  // 这里可以跳转到修改密码页面
}

// 退出登录
const logout = () => {
  if (confirm('确定要退出登录吗？')) {
    authStore.logout()
    router.push('/')
  }
}

// 组件挂载时初始化表单数据
onMounted(() => {
  updateFormFromUser()
})
</script>

<style scoped>
.profile-container {
  padding: 2rem;
  width: 100%;
  max-width: 100%;
  margin: 0 auto;
  box-sizing: border-box;
}

.profile-container h1 {
  color: #42b883;
  margin-bottom: 1.5rem;
}

.profile-content {
  display: flex;
  gap: 2rem;
  width: 100%;
  box-sizing: border-box;
}

.profile-sidebar {
  flex: 0 0 250px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  height: fit-content;
  box-sizing: border-box;
}

.user-info {
  text-align: center;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #eee;
  box-sizing: border-box;
}

.avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background-color: #f8f9fa;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
  font-size: 2rem;
  box-sizing: border-box;
}

.user-info h2 {
  margin: 0.5rem 0;
  color: #333;
}

.user-info p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
}

.profile-nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.profile-nav li {
  margin-bottom: 0.5rem;
}

.profile-nav a {
  display: block;
  padding: 0.75rem 1rem;
  text-decoration: none;
  color: #333;
  border-radius: 4px;
  transition: all 0.3s;
  box-sizing: border-box;
}

.profile-nav a:hover {
  background-color: #f8f9fa;
}

.profile-nav a.active {
  background-color: #42b883;
  color: white;
}

.btn-logout {
  width: 100%;
  padding: 0.75rem;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
  box-sizing: border-box;
}

.btn-logout:hover {
  background-color: #c82333;
}

.profile-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2rem;
  box-sizing: border-box;
}

.profile-section {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  box-sizing: border-box;
}

.profile-section h2 {
  color: #42b883;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #eee;
}

.profile-form {
  margin-bottom: 1rem;
  box-sizing: border-box;
}

.form-row {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  box-sizing: border-box;
}

.form-group {
  flex: 1;
  box-sizing: border-box;
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

.form-actions {
  text-align: center;
  margin-top: 2rem;
  box-sizing: border-box;
}

.btn-save {
  padding: 0.75rem 2rem;
  background-color: #42b883;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
  box-sizing: border-box;
}

.btn-save:hover:not(:disabled) {
  background-color: #359c6d;
}

.btn-save:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.security-actions {
  text-align: center;
  box-sizing: border-box;
}

.btn-change-password {
  padding: 0.75rem 2rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
  box-sizing: border-box;
}

.btn-change-password:hover {
  background-color: #0056b3;
}

/* 响应式断点优化 */
/* 超小屏幕 (手机, 小于576px) */
@media (max-width: 575.98px) {
  .profile-container {
    padding: 0.75rem 0.5rem;
  }
  
  .profile-container h1 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
  }
  
  .profile-content {
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .profile-sidebar {
    flex: none;
    padding: 1rem;
  }
  
  .user-info {
    margin-bottom: 1rem;
    padding-bottom: 1rem;
  }
  
  .avatar {
    width: 60px;
    height: 60px;
    font-size: 1.5rem;
  }
  
  .user-info h2 {
    font-size: 1.1rem;
    margin: 0.25rem 0;
  }
  
  .user-info p {
    font-size: 0.8rem;
  }
  
  .profile-nav li {
    margin-bottom: 0.25rem;
  }
  
  .profile-nav a {
    padding: 0.5rem;
    font-size: 0.85rem;
  }
  
  .btn-logout {
    padding: 0.5rem;
    font-size: 0.85rem;
  }
  
  .profile-main {
    gap: 0.75rem;
  }
  
  .profile-section {
    padding: 1rem;
  }
  
  .profile-section h2 {
    font-size: 1.2rem;
    margin-bottom: 1rem;
    padding-bottom: 0.25rem;
  }
  
  .form-row {
    flex-direction: column;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
  }
  
  .form-group label {
    font-size: 0.85rem;
    margin-bottom: 0.25rem;
  }
  
  .form-group input {
    padding: 0.5rem;
    font-size: 0.85rem;
  }
  
  .form-actions {
    margin-top: 1rem;
  }
  
  .btn-save {
    padding: 0.5rem 1rem;
    font-size: 0.85rem;
  }
  
  .btn-change-password {
    padding: 0.5rem 1rem;
    font-size: 0.85rem;
  }
}

/* 小屏幕 (手机横屏, 576px及以上) */
@media (min-width: 576px) {
  .profile-container {
    padding: 1rem;
  }
  
  .profile-content {
    gap: 1rem;
  }
  
  .profile-sidebar {
    padding: 1rem;
  }
  
  .profile-main {
    gap: 1rem;
  }
  
  .profile-section {
    padding: 1.25rem;
  }
  
  .form-row {
    gap: 0.75rem;
    margin-bottom: 0.75rem;
  }
  
  .form-group input {
    padding: 0.6rem;
    font-size: 0.9rem;
  }
  
  .btn-save {
    padding: 0.6rem 1.5rem;
    font-size: 0.9rem;
  }
  
  .btn-change-password {
    padding: 0.6rem 1.5rem;
    font-size: 0.9rem;
  }
}

/* 中等屏幕 (平板, 768px及以上) */
@media (min-width: 768px) {
  .profile-container {
    padding: 1.5rem;
  }
  
  .profile-content {
    flex-direction: row;
    gap: 1.5rem;
  }
  
  .profile-sidebar {
    flex: 0 0 200px;
    padding: 1.25rem;
  }
  
  .user-info {
    margin-bottom: 1.5rem;
    padding-bottom: 1.25rem;
  }
  
  .avatar {
    width: 70px;
    height: 70px;
    font-size: 1.75rem;
  }
  
  .user-info h2 {
    font-size: 1.25rem;
  }
  
  .user-info p {
    font-size: 0.85rem;
  }
  
  .profile-nav li {
    margin-bottom: 0.4rem;
  }
  
  .profile-nav a {
    padding: 0.6rem 0.75rem;
    font-size: 0.9rem;
  }
  
  .btn-logout {
    padding: 0.6rem;
    font-size: 0.9rem;
  }
  
  .profile-main {
    gap: 1.5rem;
  }
  
  .profile-section {
    padding: 1.5rem;
  }
  
  .profile-section h2 {
    font-size: 1.3rem;
    margin-bottom: 1.25rem;
  }
  
  .form-row {
    gap: 1rem;
    margin-bottom: 1rem;
  }
  
  .form-group input {
    padding: 0.75rem;
    font-size: 1rem;
  }
  
  .form-actions {
    margin-top: 1.5rem;
  }
  
  .btn-save {
    padding: 0.75rem 1.75rem;
    font-size: 1rem;
  }
  
  .btn-change-password {
    padding: 0.75rem 1.75rem;
    font-size: 1rem;
  }
}

/* 大屏幕 (桌面, 992px及以上) */
@media (min-width: 992px) {
  .profile-container {
    padding: 2rem;
  }
  
  .profile-content {
    gap: 2rem;
  }
  
  .profile-sidebar {
    flex: 0 0 250px;
    padding: 1.5rem;
  }
  
  .user-info {
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
  }
  
  .avatar {
    width: 80px;
    height: 80px;
    font-size: 2rem;
  }
  
  .user-info h2 {
    font-size: 1.4rem;
  }
  
  .user-info p {
    font-size: 0.9rem;
  }
  
  .profile-nav li {
    margin-bottom: 0.5rem;
  }
  
  .profile-nav a {
    padding: 0.75rem 1rem;
    font-size: 1rem;
  }
  
  .btn-logout {
    padding: 0.75rem;
    font-size: 1rem;
  }
  
  .profile-main {
    gap: 2rem;
  }
  
  .profile-section {
    padding: 2rem;
  }
  
  .profile-section h2 {
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
  }
  
  .form-row {
    gap: 1rem;
    margin-bottom: 1rem;
  }
  
  .form-actions {
    margin-top: 2rem;
  }
}

/* 超大屏幕 (大桌面, 1200px及以上) */
@media (min-width: 1200px) {
  .profile-container {
    padding: 2rem;
    max-width: 1400px;
  }
  
  .profile-sidebar {
    flex: 0 0 280px;
  }
  
  .profile-section {
    padding: 2.5rem;
  }
}

/* 超宽屏 (1600px及以上) */
@media (min-width: 1600px) {
  .profile-container {
    padding: 3rem;
    max-width: 1600px;
  }
  
  .profile-content {
    gap: 3rem;
  }
  
  .profile-sidebar {
    flex: 0 0 300px;
    padding: 2rem;
  }
  
  .profile-main {
    gap: 3rem;
  }
  
  .profile-section {
    padding: 3rem;
  }
  
  .profile-section h2 {
    font-size: 1.7rem;
    margin-bottom: 2rem;
  }
  
  .form-row {
    gap: 1.5rem;
    margin-bottom: 1.5rem;
  }
  
  .form-actions {
    margin-top: 3rem;
  }
}

/* 超宽屏 (2000px及以上) */
@media (min-width: 2000px) {
  .profile-container {
    padding: 4rem;
    max-width: 1800px;
  }
  
  .profile-content {
    gap: 4rem;
  }
  
  .profile-sidebar {
    flex: 0 0 320px;
    padding: 2.5rem;
  }
  
  .profile-main {
    gap: 4rem;
  }
  
  .profile-section {
    padding: 4rem;
  }
  
  .profile-section h2 {
    font-size: 2rem;
    margin-bottom: 2.5rem;
  }
  
  .form-row {
    gap: 2rem;
    margin-bottom: 2rem;
  }
  
  .form-group label {
    font-size: 1.2rem;
    margin-bottom: 0.75rem;
  }
  
  .form-group input {
    padding: 1rem;
    font-size: 1.2rem;
  }
  
  .form-actions {
    margin-top: 4rem;
  }
  
  .btn-save {
    padding: 1rem 2.5rem;
    font-size: 1.2rem;
  }
  
  .btn-change-password {
    padding: 1rem 2.5rem;
    font-size: 1.2rem;
  }
  
  .btn-logout {
    padding: 1rem;
    font-size: 1.2rem;
  }
}
</style>