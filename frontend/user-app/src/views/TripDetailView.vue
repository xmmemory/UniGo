<template>
  <div class="trip-detail-container">
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="trip" class="trip-detail">
      <div class="trip-header">
        <h1>{{ trip.departure }} → {{ trip.destination }}</h1>
        <span class="trip-date">{{ formatDate(trip.departure_time) }}</span>
      </div>
      
      <div class="trip-info">
        <div class="info-section">
          <h2>行程信息</h2>
          <div class="info-grid">
            <div class="info-item">
              <label>出发时间:</label>
              <span>{{ formatTime(trip.departure_time) }}</span>
            </div>
            <div class="info-item">
              <label>司机:</label>
              <span>{{ trip.driver_name }}</span>
            </div>
            <div class="info-item">
              <label>联系电话:</label>
              <span>{{ trip.driver_phone }}</span>
            </div>
            <div class="info-item">
              <label>车型:</label>
              <span>{{ trip.vehicle_type }}</span>
            </div>
            <div class="info-item">
              <label>车牌号:</label>
              <span>{{ trip.license_plate }}</span>
            </div>
            <div class="info-item">
              <label>空位:</label>
              <span>{{ trip.available_seats }} 个</span>
            </div>
            <div class="info-item">
              <label>费用:</label>
              <span>¥{{ trip.price }}</span>
            </div>
            <div class="info-item">
              <label>状态:</label>
              <span class="trip-status" :class="trip.status">{{ getTripStatusText(trip.status) }}</span>
            </div>
          </div>
        </div>
        
        <div class="info-section">
          <h2>行程描述</h2>
          <p>{{ trip.description || '暂无描述' }}</p>
        </div>
        
        <div class="info-section" v-if="trip.passengers && trip.passengers.length > 0">
          <h2>已预订乘客</h2>
          <div class="passengers-list">
            <div
              v-for="passenger in trip.passengers"
              :key="passenger.id"
              class="passenger-item"
            >
              <span>{{ passenger.name }}</span>
              <span>{{ passenger.phone }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <div class="actions">
        <button
          v-if="!isDriver && trip.status === 'open' && trip.available_seats > 0"
          class="btn-book"
          @click="bookTrip"
          :disabled="booking"
        >
          {{ booking ? '预订中...' : '预订座位' }}
        </button>
        <button
          v-else-if="isDriver"
          class="btn-manage"
          @click="manageTrip"
        >
          管理行程
        </button>
        <button
          v-else
          class="btn-disabled"
          disabled
        >
          无法预订
        </button>
        
        <button class="btn-back" @click="goBack">返回</button>
      </div>
      
      <!-- 聊天窗口 -->
      <div class="chat-section" v-if="showChat">
        <h2>行程聊天</h2>
        <ChatWindow :trip-id="tripId" />
      </div>
      
      <div class="chat-toggle" v-if="!showChat">
        <button @click="toggleChat">打开聊天</button>
      </div>
    </div>
    <div v-else class="no-trip">未找到行程信息</div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { getTripDetail, bookTrip as bookTripApi } from '../api/tripService'
import ChatWindow from '../components/ChatWindow.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const tripId = computed(() => parseInt(route.params.id as string))
const trip = ref<any>(null)
const loading = ref(true)
const booking = ref(false)
const showChat = ref(false)

// 是否为司机
const isDriver = computed(() => {
  return trip.value && authStore.user && trip.value.driver_id === authStore.user.id
})

// 获取行程详情
const fetchTripDetail = async () => {
  try {
    const response = await getTripDetail(tripId.value)
    trip.value = response
  } catch (error) {
    console.error('获取行程详情失败:', error)
    alert('获取行程详情失败')
  } finally {
    loading.value = false
  }
}

// 预订行程
const bookTrip = async () => {
  if (!authStore.isAuthenticated) {
    alert('请先登录')
    router.push('/login')
    return
  }
  
  booking.value = true
  try {
    await bookTripApi(tripId.value)
    alert('预订成功！')
    // 重新获取行程详情以更新状态
    await fetchTripDetail()
  } catch (error: any) {
    alert(error.message || '预订失败')
  } finally {
    booking.value = false
  }
}

// 管理行程
const manageTrip = () => {
  // 这里可以跳转到行程管理页面
  alert('跳转到行程管理页面')
}

// 返回上一页
const goBack = () => {
  router.back()
}

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN')
}

// 格式化时间
const formatTime = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

// 获取行程状态文本
const getTripStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    'open': '开放中',
    'closed': '已关闭',
    'completed': '已完成'
  }
  return statusMap[status] || status
}

// 切换聊天窗口
const toggleChat = () => {
  showChat.value = !showChat.value
}

// 组件挂载时获取行程详情
onMounted(() => {
  fetchTripDetail()
})
</script>

<style scoped>
.trip-detail-container {
  padding: 2rem;
}

.loading, .no-trip {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.trip-detail {
  max-width: 800px;
  margin: 0 auto;
}

.trip-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
}

.trip-header h1 {
  margin: 0;
  color: #42b883;
}

.trip-date {
  color: #666;
  font-size: 1.1rem;
}

.trip-info {
  margin-bottom: 2rem;
}

.info-section {
  margin-bottom: 2rem;
}

.info-section h2 {
  color: #42b883;
  margin-bottom: 1rem;
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

.trip-status {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.9rem;
  font-weight: 500;
}

.trip-status.open {
  background-color: #d4edda;
  color: #155724;
}

.trip-status.closed {
  background-color: #f8d7da;
  color: #721c24;
}

.trip-status.completed {
  background-color: #d1ecf1;
  color: #0c5460;
}

.passengers-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.passenger-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem;
  background: #f8f9fa;
  border-radius: 4px;
}

.actions {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.btn-book, .btn-manage, .btn-back, .btn-disabled {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-book {
  background-color: #42b883;
  color: white;
}

.btn-book:hover:not(:disabled) {
  background-color: #359c6d;
}

.btn-book:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-manage {
  background-color: #007bff;
  color: white;
}

.btn-manage:hover {
  background-color: #0056b3;
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

.chat-section {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #eee;
}

.chat-section h2 {
  color: #42b883;
  margin-bottom: 1rem;
}

.chat-toggle {
  text-align: center;
  margin-top: 2rem;
}

.chat-toggle button {
  padding: 0.5rem 1rem;
  background-color: #42b883;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.chat-toggle button:hover {
  background-color: #359c6d;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .trip-detail-container {
    padding: 1rem;
  }
  
  .trip-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
  }
  
  .trip-header h1 {
    font-size: 1.5rem;
  }
  
  .trip-date {
    font-size: 1rem;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }
  
  .info-item {
    flex-direction: column;
    gap: 0.25rem;
    padding: 0.75rem 0;
  }
  
  .info-item label {
    font-size: 0.9rem;
  }
  
  .info-item span {
    font-size: 0.9rem;
  }
  
  .passenger-item {
    flex-direction: column;
    gap: 0.25rem;
    padding: 0.75rem;
  }
  
  .actions {
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .btn-book, .btn-manage, .btn-back, .btn-disabled {
    width: 100%;
    padding: 0.75rem;
  }
  
  .chat-toggle button {
    width: 100%;
    padding: 0.75rem;
  }
}

@media (max-width: 480px) {
  .trip-detail-container {
    padding: 0.5rem;
  }
  
  .trip-header h1 {
    font-size: 1.3rem;
  }
  
  .info-section h2 {
    font-size: 1.1rem;
  }
  
  .info-item {
    padding: 0.5rem 0;
  }
  
  .info-item label, .info-item span {
    font-size: 0.85rem;
  }
  
  .trip-status {
    font-size: 0.8rem;
    padding: 0.2rem 0.4rem;
  }
  
  .passenger-item {
    padding: 0.5rem;
  }
  
  .passenger-item span {
    font-size: 0.85rem;
  }
  
  .btn-book, .btn-manage, .btn-back, .btn-disabled {
    padding: 0.6rem;
    font-size: 0.9rem;
  }
  
  .chat-toggle button {
    padding: 0.6rem;
    font-size: 0.9rem;
  }
}
</style>