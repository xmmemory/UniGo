<template>
  <div class="user-management">
    <h1>用户管理</h1>
    
    <div class="toolbar">
      <div class="search-box">
        <input 
          type="text" 
          placeholder="搜索用户..." 
          v-model="searchQuery"
          @input="handleSearch"
        />
        <button @click="searchUsers">搜索</button>
      </div>
      <button class="btn-primary" @click="showCreateUserModal">创建用户</button>
    </div>
    
    <div class="table-container">
      <table class="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>用户名</th>
            <th>邮箱</th>
            <th>注册时间</th>
            <th>状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.username }}</td>
            <td>{{ user.email }}</td>
            <td>{{ formatDate(user.created_at) }}</td>
            <td>
              <span :class="['status', user.is_active ? 'active' : 'inactive']">
                {{ user.is_active ? '活跃' : '禁用' }}
              </span>
            </td>
            <td>
              <button class="btn-small" @click="editUser(user)">编辑</button>
              <button 
                :class="['btn-small', user.is_active ? 'btn-warning' : 'btn-success']"
                @click="toggleUserStatus(user)"
              >
                {{ user.is_active ? '禁用' : '启用' }}
              </button>
              <button class="btn-small btn-danger" @click="deleteUser(user)">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <div class="pagination">
      <button 
        :disabled="currentPage === 1" 
        @click="changePage(currentPage - 1)"
      >
        上一页
      </button>
      <span>第 {{ currentPage }} 页，共 {{ totalPages }} 页</span>
      <button 
        :disabled="currentPage === totalPages" 
        @click="changePage(currentPage + 1)"
      >
        下一页
      </button>
    </div>
    
    <!-- 创建/编辑用户模态框 -->
    <div class="modal" v-if="showModal">
      <div class="modal-content">
        <h2>{{ editingUser ? '编辑用户' : '创建用户' }}</h2>
        <form @submit.prevent="saveUser">
          <div class="form-group">
            <label for="username">用户名</label>
            <input 
              type="text" 
              id="username" 
              v-model="userForm.username" 
              required 
              :disabled="!!editingUser"
            />
          </div>
          <div class="form-group">
            <label for="email">邮箱</label>
            <input 
              type="email" 
              id="email" 
              v-model="userForm.email" 
              required 
            />
          </div>
          <div class="form-group" v-if="!editingUser">
            <label for="password">密码</label>
            <input 
              type="password" 
              id="password" 
              v-model="userForm.password" 
              required 
            />
          </div>
          <div class="form-group">
            <label for="is_active">状态</label>
            <select id="is_active" v-model="userForm.is_active">
              <option :value="true">活跃</option>
              <option :value="false">禁用</option>
            </select>
          </div>
          <div class="form-actions">
            <button type="button" @click="closeModal" class="btn-secondary">取消</button>
            <button type="submit" class="btn-primary">保存</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getAdminUsers } from '../api/adminService'
// @ts-ignore
import { useAdminStore } from '../stores/admin'

const adminStore = useAdminStore()
const users = ref<any[]>([])
const loading = ref(false)
const currentPage = ref(1)
const totalPages = ref(1)
const totalItems = ref(0)
const searchQuery = ref('')
const showModal = ref(false)
const editingUser = ref<any>(null)
const userForm = ref({
  username: '',
  email: '',
  password: '',
  is_active: true
})

// 获取用户列表
const fetchUsers = async (page = 1) => {
  loading.value = true
  try {
    // @ts-ignore
    const response = await getAdminUsers((page - 1) * 10, 10)
    users.value = response
    totalItems.value = response.length
    totalPages.value = Math.ceil(totalItems.value / 10)
    currentPage.value = page
  } catch (error) {
    console.error('获取用户列表失败:', error)
    alert('获取用户列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索用户
const searchUsers = () => {
  // 这里可以实现搜索逻辑
  console.log('搜索用户:', searchQuery.value)
  fetchUsers(1)
}

// 处理搜索输入
const handleSearch = () => {
  // 可以实现防抖搜索
}

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN')
}

// 改变页面
const changePage = (page: number) => {
  fetchUsers(page)
}

// 显示创建用户模态框
const showCreateUserModal = () => {
  editingUser.value = null
  userForm.value = {
    username: '',
    email: '',
    password: '',
    is_active: true
  }
  showModal.value = true
}

// 编辑用户
const editUser = (user: any) => {
  editingUser.value = user
  userForm.value = {
    username: user.username,
    email: user.email,
    password: '',
    is_active: user.is_active
  }
  showModal.value = true
}

// 切换用户状态
const toggleUserStatus = (user: any) => {
  const action = user.is_active ? '禁用' : '启用'
  if (confirm(`确定要${action}用户 ${user.username} 吗？`)) {
    // 这里可以实现切换用户状态的逻辑
    console.log(`切换用户 ${user.username} 状态`)
  }
}

// 删除用户
const deleteUser = (user: any) => {
  if (confirm(`确定要删除用户 ${user.username} 吗？此操作不可恢复！`)) {
    // 这里可以实现删除用户的逻辑
    console.log(`删除用户 ${user.username}`)
  }
}

// 保存用户
const saveUser = () => {
  if (editingUser.value) {
    // 编辑用户逻辑
    console.log('编辑用户:', userForm.value)
  } else {
    // 创建用户逻辑
    console.log('创建用户:', userForm.value)
  }
  closeModal()
  fetchUsers(currentPage.value)
}

// 关闭模态框
const closeModal = () => {
  showModal.value = false
  editingUser.value = null
}

// 组件挂载时获取用户列表
onMounted(() => {
  fetchUsers(1)
})
</script>

<style scoped>
.user-management {
  padding: 2rem;
}

.user-management h1 {
  color: #333;
  margin-bottom: 2rem;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.search-box {
  display: flex;
  gap: 0.5rem;
}

.search-box input {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.search-box button,
.toolbar .btn-primary {
  padding: 0.5rem 1rem;
  background-color: #42b883;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.toolbar .btn-primary:hover,
.search-box button:hover {
  background-color: #359c6d;
}

.table-container {
  overflow-x: auto;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.5rem;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th,
.data-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.data-table th {
  background-color: #f8f9fa;
  font-weight: 600;
  color: #333;
}

.status {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
}

.status.active {
  background-color: #d4edda;
  color: #155724;
}

.status.inactive {
  background-color: #f8d7da;
  color: #721c24;
}

.btn-small {
  padding: 0.25rem 0.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
  margin-right: 0.25rem;
}

.btn-small:hover {
  opacity: 0.9;
}

.btn-primary {
  background-color: #42b883;
  color: white;
}

.btn-warning {
  background-color: #ffc107;
  color: #212529;
}

.btn-success {
  background-color: #28a745;
  color: white;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 1.5rem;
}

.pagination button {
  padding: 0.5rem 1rem;
  background-color: #42b883;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.pagination button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-content h2 {
  margin-top: 0;
  color: #333;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}

.btn-secondary {
  padding: 0.5rem 1rem;
  background-color: #6c757d;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

@media (max-width: 768px) {
  .toolbar {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-box {
    order: 2;
  }
  
  .toolbar .btn-primary {
    order: 1;
    width: fit-content;
    align-self: flex-end;
  }
      
  .modal-content {
    margin: 1rem;
    padding: 1rem;
  }
}

/* 宽屏PC适配 */
@media (min-width: 1200px) {
  .user-management {
    padding: 3rem;
    max-width: 1600px;
  }
  
  .user-management h1 {
    font-size: 2.8rem;
    margin-bottom: 3rem;
  }
  
  .toolbar {
    margin-bottom: 3rem;
    padding: 2rem;
  }
  
  .search-box input {
    padding: 1rem;
    font-size: 1.1rem;
    min-width: 400px;
  }
  
  .search-box button,
  .toolbar .btn-primary {
    padding: 1rem 2rem;
    font-size: 1.1rem;
  }
  
  .table-container {
    padding: 2rem;
    margin-bottom: 3rem;
  }
    
  .pagination {
    margin-top: 3rem;
    padding: 2rem;
  }
  
  .pagination button {
    padding: 1rem 2rem;
    font-size: 1.1rem;
  }
  
  .modal-content {
    padding: 4rem;
    max-width: 700px;
  }
  
  .modal-content h2 {
    font-size: 2rem;
    margin-bottom: 3rem;
  }
  
  .form-group {
    margin-bottom: 2rem;
  }
  
  .form-group label {
    font-size: 1.2rem;
    margin-bottom: 1rem;
  }
  
  .form-group input,
  .form-group select {
    padding: 1.25rem;
    font-size: 1.1rem;
  }
  
  .form-actions {
    margin-top: 3rem;
    gap: 2rem;
  }  
}

/* 大宽屏PC适配 */
@media (min-width: 1600px) {
  .user-management {
    padding: 4rem;
    max-width: 1800px;
  }
  
  .user-management h1 {
    font-size: 3rem;
    margin-bottom: 4rem;
  }
  
  .toolbar {
    margin-bottom: 4rem;
    padding: 2.5rem;
  }
  
  .search-box input {
    min-width: 500px;
  }
  
  .table-container {
    padding: 3rem;
    margin-bottom: 4rem;
  }
    
  .pagination {
    margin-top: 4rem;
    padding: 2.5rem;
  }
  
  .modal-content {
    padding: 5rem;
    max-width: 800px;
  }
  
  .modal-content h2 {
    font-size: 2.5rem;
  }
}

/* 超宽屏PC适配 */
@media (min-width: 2000px) {
  .user-management {
    padding: 5rem;
    max-width: 2000px;
  }
  
  .user-management h1 {
    font-size: 3.5rem;
    margin-bottom: 5rem;
  }
  
  .toolbar {
    margin-bottom: 5rem;
    padding: 3rem;
  }
  
  .search-box input {
    min-width: 600px;
    padding: 1.25rem;
    font-size: 1.2rem;
  }
  
  .search-box button,
  .toolbar .btn-primary {
    padding: 1.25rem 2.5rem;
    font-size: 1.2rem;
  }
  
  .table-container {
    padding: 4rem;
    margin-bottom: 5rem;
  }
    
  .pagination {
    margin-top: 5rem;
    padding: 3rem;
  }
  
  .pagination button {
    padding: 1.25rem 2.5rem;
    font-size: 1.2rem;
  }
  
  .modal-content {
    padding: 6rem;
    max-width: 900px;
  }
  
  .modal-content h2 {
    font-size: 3rem;
    margin-bottom: 4rem;
  }
  
  .form-group label {
    font-size: 1.3rem;
  }
  
  .form-group input,
  .form-group select {
    padding: 1.5rem;
    font-size: 1.2rem;
  }
  
}
</style>