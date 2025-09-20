<template>
  <div class="errand-detail-container">
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="task" class="task-detail">
      <div class="task-header">
        <h1>{{ task.title }}</h1>
        <span class="task-reward">¥{{ task.reward }}</span>
      </div>
      
      <div class="task-info">
        <div class="info-section">
          <h2>任务描述</h2>
          <p>{{ task.description || '暂无描述' }}</p>
        </div>
        
        <div class="info-section">
          <h2>任务信息</h2>
          <div class="info-grid">
            <div class="info-item">
              <label>发布者:</label>
              <span>{{ task.owner_name }}</span>
            </div>
            <div class="info-item">
              <label>状态:</label>
              <span class="task-status" :class="task.status">{{ getTaskStatusText(task.status) }}</span>
            </div>
            <div class="info-item">
              <label>位置:</label>
              <span>{{ task.location }}</span>
            </div>
            <div class="info-item">
              <label>截止时间:</label>
              <span>{{ formatDateTime(task.deadline) }}</span>
            </div>
            <div class="info-item" v-if="task.assignee_name">
              <label>接取者:</label>
              <span>{{ task.assignee_name }}</span>
            </div>
            <div class="info-item">
              <label>发布时间:</label>
              <span>{{ formatDateTime(task.created_at) }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <div class="actions">
        <button
          v-if="!isOwner && !isAssignee && task.status === 'open'"
          class="btn-accept"
          @click="acceptTask"
          :disabled="accepting"
        >
          {{ accepting ? '接取中...' : '接取任务' }}
        </button>
        <button
          v-else-if="isAssignee && task.status === 'in_progress'"
          class="btn-complete"
          @click="completeTask"
          :disabled="completing"
        >
          {{ completing ? '完成中...' : '完成任务' }}
        </button>
        <button
          v-else-if="isOwner && task.status === 'open'"
          class="btn-cancel"
          @click="cancelTask"
          :disabled="cancelling"
        >
          {{ cancelling ? '取消中...' : '取消任务' }}
        </button>
        <button
          v-else-if="isOwner && task.status === 'in_progress'"
          class="btn-contact"
          @click="contactAssignee"
        >
          联系接取者
        </button>
        <button
          v-else
          class="btn-disabled"
          disabled
        >
          无法操作
        </button>
        
        <button class="btn-back" @click="goBack">返回</button>
      </div>
    </div>
    <div v-else class="no-task">未找到任务信息</div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { getErrandTaskDetail, acceptErrandTask, completeErrandTask, cancelErrandTask } from '../services/errandService'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const taskId = computed(() => parseInt(route.params.id as string))
const task = ref<any>(null)
const loading = ref(true)
const accepting = ref(false)
const completing = ref(false)
const cancelling = ref(false)

// 是否为任务发布者
const isOwner = computed(() => {
  return task.value && authStore.user && task.value.owner_id === authStore.user.id
})

// 是否为任务接取者
const isAssignee = computed(() => {
  return task.value && authStore.user && task.value.assignee_id === authStore.user.id
})

// 获取任务详情
const fetchTaskDetail = async () => {
  try {
    const response = await getErrandTaskDetail(taskId.value)
    task.value = response
  } catch (error) {
    console.error('获取任务详情失败:', error)
    alert('获取任务详情失败')
  } finally {
    loading.value = false
  }
}

// 接取任务
const acceptTask = async () => {
  if (!authStore.isAuthenticated) {
    alert('请先登录')
    router.push('/login')
    return
  }
  
  accepting.value = true
  try {
    await acceptErrandTask(taskId.value)
    alert('任务接取成功！')
    // 重新获取任务详情以更新状态
    await fetchTaskDetail()
  } catch (error: any) {
    alert(error.message || '接取任务失败')
  } finally {
    accepting.value = false
  }
}

// 完成任务
const completeTask = async () => {
  if (!authStore.isAuthenticated) {
    alert('请先登录')
    router.push('/login')
    return
  }
  
  if (!confirm('确定要完成此任务吗？')) {
    return
  }
  
  completing.value = true
  try {
    await completeErrandTask(taskId.value)
    alert('任务已完成！')
    // 重新获取任务详情以更新状态
    await fetchTaskDetail()
  } catch (error: any) {
    alert(error.message || '完成任务失败')
  } finally {
    completing.value = false
  }
}

// 取消任务
const cancelTask = async () => {
  if (!authStore.isAuthenticated) {
    alert('请先登录')
    router.push('/login')
    return
  }
  
  if (!confirm('确定要取消此任务吗？')) {
    return
  }
  
  cancelling.value = true
  try {
    await cancelErrandTask(taskId.value)
    alert('任务已取消！')
    // 重新获取任务详情以更新状态
    await fetchTaskDetail()
  } catch (error: any) {
    alert(error.message || '取消任务失败')
  } finally {
    cancelling.value = false
  }
}

// 联系接取者
const contactAssignee = () => {
  if (!authStore.isAuthenticated) {
    alert('请先登录')
    router.push('/login')
    return
  }
  
  alert('联系接取者功能待实现')
  // 这里可以实现联系接取者的功能
}

// 返回上一页
const goBack = () => {
  router.back()
}

// 格式化日期时间
const formatDateTime = (dateString: string) => {
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

// 组件挂载时获取任务详情
onMounted(() => {
  fetchTaskDetail()
})
</script>

<style scoped>
.errand-detail-container {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.loading, .no-task {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.task-detail {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.task-header {
  padding: 1.5rem;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.task-header h1 {
  margin: 0;
  color: #333;
}

.task-reward {
  font-size: 1.5rem;
  font-weight: bold;
  color: #42b883;
}

.task-info {
  padding: 1.5rem;
}

.info-section {
  margin-bottom: 2rem;
}

.info-section h2 {
  color: #42b883;
  margin-bottom: 1rem;
}

.info-section p {
  color: #333;
  line-height: 1.6;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid #f0f0f0;
}

.info-item label {
  font-weight: 500;
  color: #333;
}

.task-status {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.9rem;
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

.actions {
  padding: 1.5rem;
  text-align: center;
  border-top: 1px solid #eee;
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;
}

.btn-accept, .btn-complete, .btn-cancel, .btn-contact, .btn-back, .btn-disabled {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-accept {
  background-color: #42b883;
  color: white;
}

.btn-accept:hover:not(:disabled) {
  background-color: #359c6d;
}

.btn-accept:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-complete {
  background-color: #007bff;
  color: white;
}

.btn-complete:hover:not(:disabled) {
  background-color: #0056b3;
}

.btn-complete:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-cancel {
  background-color: #dc3545;
  color: white;
}

.btn-cancel:hover:not(:disabled) {
  background-color: #c82333;
}

.btn-cancel:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-contact {
  background-color: #6f42c1;
  color: white;
}

.btn-contact:hover {
  background-color: #5a32a3;
}

.btn-back {
  background-color: #6c757d;
  color: white;
}

.btn-back:hover {
  background-color: #545b62;
}

.btn-disabled {
  background-color: #ccc;
  color: #666;
  cursor: not-allowed;
}
</style>