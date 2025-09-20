<template>
  <div class="publish-errand-container">
    <h1>发布跑腿任务</h1>
    
    <form @submit.prevent="publishTask" class="publish-form">
      <div class="form-section">
        <h2>任务信息</h2>
        
        <div class="form-group">
          <label for="title">任务标题 *</label>
          <input
            id="title"
            v-model="taskForm.title"
            type="text"
            placeholder="请输入任务标题"
            required
          />
        </div>
        
        <div class="form-group">
          <label for="description">任务描述 *</label>
          <textarea
            id="description"
            v-model="taskForm.description"
            rows="4"
            placeholder="请输入任务详细描述"
            required
          ></textarea>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="reward">酬金 (¥) *</label>
            <input
              id="reward"
              v-model.number="taskForm.reward"
              type="number"
              min="0"
              step="0.01"
              placeholder="请输入酬金"
              required
            />
          </div>
          
          <div class="form-group">
            <label for="deadline">截止时间 *</label>
            <input
              id="deadline"
              v-model="taskForm.deadline"
              type="datetime-local"
              required
            />
          </div>
        </div>
        
        <div class="form-group">
          <label for="location">位置 *</label>
          <input
            id="location"
            v-model="taskForm.location"
            type="text"
            placeholder="请输入任务位置"
            required
          />
        </div>
      </div>
      
      <div class="form-actions">
        <button type="submit" class="btn-publish" :disabled="publishing">
          {{ publishing ? '发布中...' : '发布任务' }}
        </button>
        <button type="button" class="btn-cancel" @click="cancel">取消</button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { createErrandTask } from '../services/errandService'

const router = useRouter()
const authStore = useAuthStore()

const publishing = ref(false)

const taskForm = reactive({
  title: '',
  description: '',
  reward: 0,
  deadline: '',
  location: ''
})

// 发布任务
const publishTask = async () => {
  if (!authStore.isAuthenticated) {
    alert('请先登录')
    router.push('/login')
    return
  }
  
  // 基本验证
  if (!taskForm.title) {
    alert('请输入任务标题')
    return
  }
  
  if (!taskForm.description) {
    alert('请输入任务描述')
    return
  }
  
  if (taskForm.reward <= 0) {
    alert('请输入有效酬金')
    return
  }
  
  if (!taskForm.deadline) {
    alert('请选择截止时间')
    return
  }
  
  // 检查截止时间是否在将来
  const deadline = new Date(taskForm.deadline)
  const now = new Date()
  if (deadline <= now) {
    alert('截止时间必须在将来')
    return
  }
  
  if (!taskForm.location) {
    alert('请输入任务位置')
    return
  }
  
  publishing.value = true
  try {
    await createErrandTask({
      title: taskForm.title,
      description: taskForm.description,
      reward: taskForm.reward,
      deadline: taskForm.deadline,
      location: taskForm.location
    })
    
    alert('任务发布成功！')
    router.push('/errands')
  } catch (error: any) {
    alert(error.message || '发布任务失败')
  } finally {
    publishing.value = false
  }
}

const cancel = () => {
  if (confirm('确定要取消发布吗？')) {
    router.back()
  }
}
</script>

<style scoped>
.publish-errand-container {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.publish-errand-container h1 {
  color: #42b883;
  margin-bottom: 1.5rem;
  text-align: center;
}

.publish-form {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.form-section {
  margin-bottom: 2rem;
}

.form-section h2 {
  color: #42b883;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #eee;
}

.form-row {
  display: flex;
  gap: 1rem;
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
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  box-sizing: border-box;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #42b883;
}

.form-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 2rem;
}

.btn-publish, .btn-cancel {
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-publish {
  background-color: #42b883;
  color: white;
}

.btn-publish:hover:not(:disabled) {
  background-color: #359c6d;
}

.btn-publish:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-cancel {
  background-color: #6c757d;
  color: white;
}

.btn-cancel:hover {
  background-color: #545b62;
}

@media (max-width: 768px) {
  .publish-errand-container {
    padding: 1rem;
  }
  
  .publish-form {
    padding: 1rem;
  }
  
  .form-row {
    flex-direction: column;
    gap: 0;
  }
}
</style>