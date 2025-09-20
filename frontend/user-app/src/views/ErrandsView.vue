<template>
  <div class="errands-container">
    <h1>跑腿服务</h1>
    
    <div class="search-filters">
      <div class="filter-group">
        <label for="keyword">关键词</label>
        <input
          id="keyword"
          v-model="searchFilters.keyword"
          type="text"
          placeholder="请输入任务标题或描述"
        />
      </div>
      
      <div class="filter-group">
        <label for="status">状态</label>
        <select
          id="status"
          v-model="searchFilters.status"
        >
          <option value="">全部状态</option>
          <option value="open">开放中</option>
          <option value="in_progress">进行中</option>
          <option value="completed">已完成</option>
          <option value="cancelled">已取消</option>
        </select>
      </div>
      
      <div class="filter-group">
        <label for="rewardRange">酬金范围</label>
        <select
          id="rewardRange"
          v-model="searchFilters.rewardRange"
        >
          <option value="">不限</option>
          <option value="0-10">0-10元</option>
          <option value="10-20">10-20元</option>
          <option value="20-50">20-50元</option>
          <option value="50-100">50-100元</option>
          <option value="100+">100元以上</option>
        </select>
      </div>
      
      <button class="btn-search" @click="searchTasks">搜索</button>
    </div>
    
    <div class="tasks-list">
      <div v-if="loading" class="loading">加载中...</div>
      <div v-else-if="tasks.length === 0" class="no-tasks">暂无跑腿任务信息</div>
      <div v-else class="task-cards">
        <div
          v-for="task in tasks"
          :key="task.id"
          class="task-card"
          @click="viewTaskDetail(task.id)"
        >
          <div class="task-header">
            <h3>{{ task.title }}</h3>
            <span class="task-reward">¥{{ task.reward }}</span>
          </div>
          
          <div class="task-description">
            <p>{{ task.description }}</p>
          </div>
          
          <div class="task-meta">
            <div class="task-location">
              <i class="location-icon">📍</i>
              <span>{{ task.location }}</span>
            </div>
            <div class="task-deadline">
              <i class="deadline-icon">⏰</i>
              <span>{{ formatDate(task.deadline) }}</span>
            </div>
          </div>
          
          <div class="task-footer">
            <span class="task-status" :class="task.status">{{ getTaskStatusText(task.status) }}</span>
            <span class="task-owner">{{ task.owner_name }}</span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 分页控件 -->
    <div class="pagination" v-if="totalPages > 1">
      <button
        :disabled="currentPage === 1"
        @click="changePage(currentPage - 1)"
      >
        上一页
      </button>
      
      <span>{{ currentPage }} / {{ totalPages }}</span>
      
      <button
        :disabled="currentPage === totalPages"
        @click="changePage(currentPage + 1)"
      >
        下一页
      </button>
    </div>
    
    <div class="actions">
      <router-link to="/publish-errand" class="btn-primary">发布任务</router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getErrandTasks } from '../services/errandService'

const router = useRouter()

// 搜索过滤器
const searchFilters = reactive({
  keyword: '',
  status: '',
  rewardRange: ''
})

// 任务数据
const tasks = ref<any[]>([])
const loading = ref(false)
const currentPage = ref(1)
const totalPages = ref(1)
const totalItems = ref(0)

// 获取跑腿任务列表
const fetchTasks = async (page = 1) => {
  loading.value = true
  try {
    const response = await getErrandTasks({
      page,
      limit: 10,
      keyword: searchFilters.keyword,
      status: searchFilters.status,
      reward_range: searchFilters.rewardRange
    })
    
    // 正确处理后端返回的数据格式
    tasks.value = response.tasks || []
    totalItems.value = response.total || 0
    currentPage.value = response.page || page
    totalPages.value = response.total_pages || 1
  } catch (error) {
    console.error('获取跑腿任务失败:', error)
    alert('获取跑腿任务失败')
  } finally {
    loading.value = false
  }
}

// 搜索任务
const searchTasks = () => {
  currentPage.value = 1
  fetchTasks(1)
}

// 查看任务详情
const viewTaskDetail = (taskId: number) => {
  router.push(`/errands/${taskId}`)
}

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN')
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

// 切换页面
const changePage = (page: number) => {
  if (page >= 1 && page <= totalPages.value) {
    fetchTasks(page)
  }
}

// 组件挂载时获取任务列表
onMounted(() => {
  fetchTasks()
})
</script>

<style scoped>
.errands-container {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.errands-container h1 {
  color: #42b883;
  margin-bottom: 1.5rem;
}

.search-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 2rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.filter-group {
  flex: 1;
  min-width: 200px;
}

.filter-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.filter-group input,
.filter-group select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

.btn-search {
  align-self: flex-end;
  padding: 0.5rem 1rem;
  background-color: #42b883;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  height: fit-content;
}

.btn-search:hover {
  background-color: #359c6d;
}

.tasks-list {
  margin-bottom: 2rem;
}

.loading, .no-tasks {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.task-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.task-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1.5rem;
  cursor: pointer;
  transition: box-shadow 0.3s;
  background: white;
}

.task-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.task-header h3 {
  margin: 0;
  color: #333;
  font-size: 1.1rem;
}

.task-reward {
  font-size: 1.2rem;
  font-weight: bold;
  color: #42b883;
}

.task-description p {
  margin: 0 0 1rem 0;
  color: #666;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.task-meta {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  color: #666;
}

.location-icon, .deadline-icon {
  margin-right: 0.25rem;
}

.task-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid #eee;
  padding-top: 1rem;
}

.task-status {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
}

.task-status.open {
  background-color: #d4edda;
  color: #155724;
}

.task-status.in_progress {
  background-color: #fff3cd;
  color: #856404;
}

.task-status.completed {
  background-color: #d1ecf1;
  color: #0c5460;
}

.task-status.cancelled {
  background-color: #f8d7da;
  color: #721c24;
}

.task-owner {
  font-size: 0.9rem;
  color: #666;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
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

.actions {
  text-align: center;
}

.btn-primary {
  padding: 0.75rem 1.5rem;
  background-color: #42b883;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  font-weight: 500;
  transition: background-color 0.3s;
}

.btn-primary:hover {
  background-color: #359c6d;
}

/* 移动端适配 */
@media (max-width: 767.98px) {
  .errands-container {
    padding: 1rem;
  }
  
  .search-filters {
    padding: 0.75rem;
    gap: 0.75rem;
  }
  
  .filter-group {
    min-width: 100%;
  }
  
  .task-cards {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
  
  .task-card {
    padding: 1rem;
  }
  
  .task-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .task-header h3 {
    font-size: 1rem;
  }
  
  .task-reward {
    font-size: 1.1rem;
  }
  
  .task-meta {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .task-description p {
    font-size: 0.9rem;
    margin-bottom: 0.75rem;
  }
  
  .task-footer {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
    padding-top: 0.75rem;
  }
  
  .btn-search {
    width: 100%;
    padding: 0.75rem;
  }
  
  .pagination {
    gap: 0.5rem;
    font-size: 0.9rem;
  }
  
  .pagination button {
    padding: 0.4rem 0.8rem;
  }
}

@media (max-width: 480px) {
  .errands-container {
    padding: 0.5rem;
  }
  
  .search-filters {
    padding: 0.5rem;
    gap: 0.5rem;
  }
  
  .task-cards {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.75rem;
  }
  
  .filter-group label {
    font-size: 0.9rem;
  }
  
  .filter-group input,
  .filter-group select {
    padding: 0.4rem;
    font-size: 0.9rem;
  }
  
  .task-card {
    padding: 0.75rem;
  }
  
  .task-header h3 {
    font-size: 0.95rem;
  }
  
  .task-reward {
    font-size: 1rem;
  }
  
  .task-description p {
    font-size: 0.85rem;
  }
  
  .task-meta {
    font-size: 0.85rem;
  }
  
  .task-status {
    font-size: 0.75rem;
    padding: 0.2rem 0.4rem;
  }
  
  .task-owner {
    font-size: 0.85rem;
  }
  
  .actions {
    padding: 0 0.5rem;
  }
  
  .btn-primary {
    padding: 0.6rem 1rem;
    font-size: 0.9rem;
  }
  
  .pagination {
    font-size: 0.85rem;
  }
  
  .pagination button {
    padding: 0.3rem 0.6rem;
    font-size: 0.85rem;
  }
}
</style>