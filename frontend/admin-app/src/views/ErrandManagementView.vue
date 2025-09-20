<template>
  <div class="errand-management">
    <h1>跑腿服务管理</h1>
    
    <div class="toolbar">
      <div class="search-box">
        <input 
          type="text" 
          placeholder="搜索任务..." 
          v-model="searchQuery"
          @input="handleSearch"
        />
        <button @click="searchTasks">搜索</button>
      </div>
      <button class="btn-primary" @click="showCreateTaskModal">发布任务</button>
    </div>
    
    <div class="table-container">
      <table class="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>标题</th>
            <th>酬金</th>
            <th>发布者</th>
            <th>接取者</th>
            <th>发布时间</th>
            <th>截止时间</th>
            <th>状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="task in tasks" :key="task.id">
            <td>{{ task.id }}</td>
            <td>{{ task.title }}</td>
            <td>¥{{ task.reward }}</td>
            <td>{{ task.owner_name }}</td>
            <td>{{ task.taker_name || '-' }}</td>
            <td>{{ formatDate(task.created_at) }}</td>
            <td>{{ formatDate(task.deadline) }}</td>
            <td>
              <span :class="['status', getTaskStatusClass(task.status)]">
                {{ getTaskStatusText(task.status) }}
              </span>
            </td>
            <td>
              <button class="btn-small" @click="viewTask(task)">查看</button>
              <button class="btn-small" @click="editTask(task)">编辑</button>
              <button 
                v-if="task.status === 'open'"
                class="btn-small btn-warning"
                @click="closeTask(task)"
              >
                关闭
              </button>
              <button 
                v-if="task.status === 'completed' || task.status === 'cancelled'"
                class="btn-small btn-success"
                @click="reopenTask(task)"
              >
                重新开启
              </button>
              <button class="btn-small btn-danger" @click="deleteTask(task)">删除</button>
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
    
    <!-- 创建/编辑任务模态框 -->
    <div class="modal" v-if="showModal">
      <div class="modal-content">
        <h2>{{ editingTask ? '编辑任务' : '发布任务' }}</h2>
        <form @submit.prevent="saveTask">
          <div class="form-group">
            <label for="title">标题</label>
            <input 
              type="text" 
              id="title" 
              v-model="taskForm.title" 
              required 
            />
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="reward">酬金(元)</label>
              <input 
                type="number" 
                id="reward" 
                v-model="taskForm.reward" 
                min="0" 
                step="0.01" 
                required 
              />
            </div>
            <div class="form-group">
              <label for="deadline">截止时间</label>
              <input 
                type="datetime-local" 
                id="deadline" 
                v-model="taskForm.deadline" 
                required 
              />
            </div>
          </div>
          <div class="form-group">
            <label for="location">地点</label>
            <input 
              type="text" 
              id="location" 
              v-model="taskForm.location" 
              required 
            />
          </div>
          <div class="form-group">
            <label for="description">描述</label>
            <textarea 
              id="description" 
              v-model="taskForm.description" 
              rows="4"
              required
            ></textarea>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="status">状态</label>
              <select id="status" v-model="taskForm.status">
                <option value="open">开放中</option>
                <option value="in_progress">进行中</option>
                <option value="completed">已完成</option>
                <option value="cancelled">已取消</option>
              </select>
            </div>
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
import { getAdminErrandTasks } from '../api/adminService'
import { useAdminStore } from '../stores/admin'

const adminStore = useAdminStore()
const tasks = ref<any[]>([])
const loading = ref(false)
const currentPage = ref(1)
const totalPages = ref(1)
const totalItems = ref(0)
const searchQuery = ref('')
const showModal = ref(false)
const editingTask = ref(null)
const taskForm = ref({
  title: '',
  reward: 0,
  deadline: '',
  location: '',
  description: '',
  status: 'open'
})

// 获取跑腿任务列表
const fetchTasks = async (page = 1) => {
  loading.value = true
  try {
    const response = await getAdminErrandTasks((page - 1) * 10, 10)
    tasks.value = response
    totalItems.value = response.length
    totalPages.value = Math.ceil(totalItems.value / 10)
    currentPage.value = page
  } catch (error) {
    console.error('获取跑腿任务列表失败:', error)
    alert('获取跑腿任务列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索任务
const searchTasks = () => {
  // 这里可以实现搜索逻辑
  console.log('搜索任务:', searchQuery.value)
  fetchTasks(1)
}

// 处理搜索输入
const handleSearch = () => {
  // 可以实现防抖搜索
}

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

// 获取任务状态文本
const getTaskStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    'open': '开放中',
    'in_progress': '进行中',
    'completed': '已完成',
    'cancelled': '已取消'
  }
  return statusMap[status] || status
}

// 获取任务状态类名
const getTaskStatusClass = (status: string) => {
  const classMap: Record<string, string> = {
    'open': 'open',
    'in_progress': 'in-progress',
    'completed': 'completed',
    'cancelled': 'cancelled'
  }
  return classMap[status] || status
}

// 改变页面
const changePage = (page: number) => {
  fetchTasks(page)
}

// 显示创建任务模态框
const showCreateTaskModal = () => {
  editingTask.value = null
  taskForm.value = {
    title: '',
    reward: 0,
    deadline: '',
    location: '',
    description: '',
    status: 'open'
  }
  showModal.value = true
}

// 查看任务
const viewTask = (task: any) => {
  // 这里可以实现查看任务详情的逻辑
  console.log('查看任务:', task)
}

// 编辑任务
const editTask = (task: any) => {
  editingTask.value = task
  taskForm.value = {
    title: task.title,
    reward: task.reward,
    deadline: task.deadline,
    location: task.location,
    description: task.description,
    status: task.status
  }
  showModal.value = true
}

// 关闭任务
const closeTask = (task: any) => {
  if (confirm(`确定要关闭任务 "${task.title}" 吗？`)) {
    // 这里可以实现关闭任务的逻辑
    console.log(`关闭任务`)
  }
}

// 重新开启任务
const reopenTask = (task: any) => {
  if (confirm(`确定要重新开启任务 "${task.title}" 吗？`)) {
    // 这里可以实现重新开启任务的逻辑
    console.log(`重新开启任务`)
  }
}

// 删除任务
const deleteTask = (task: any) => {
  if (confirm(`确定要删除任务 "${task.title}" 吗？此操作不可恢复！`)) {
    // 这里可以实现删除任务的逻辑
    console.log(`删除任务`)
  }
}

// 保存任务
const saveTask = () => {
  if (editingTask.value) {
    // 编辑任务逻辑
    console.log('编辑任务:', taskForm.value)
  } else {
    // 创建任务逻辑
    console.log('创建任务:', taskForm.value)
  }
  closeModal()
  fetchTasks(currentPage.value)
}

// 关闭模态框
const closeModal = () => {
  showModal.value = false
  editingTask.value = null
}

// 组件挂载时获取任务列表
onMounted(() => {
  fetchTasks(1)
})
</script>

<style scoped>
.errand-management {
  padding: 2rem;
}

.errand-management h1 {
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

.status.open {
  background-color: #d4edda;
  color: #155724;
}

.status.in-progress {
  background-color: #fff3cd;
  color: #856404;
}

.status.completed {
  background-color: #d1ecf1;
  color: #0c5460;
}

.status.cancelled {
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

.form-row {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.form-group {
  flex: 1;
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-group input,
.form-group select,
.form-group textarea {
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
  
  .form-row {
    flex-direction: column;
    gap: 0;
  }
  
  .data-table {
    font-size: 0.9rem;
  }
  
  .data-table th,
  .data-table td {
    padding: 0.5rem;
  }
  
  .modal-content {
    margin: 1rem;
    padding: 1rem;
  }
}
</style>