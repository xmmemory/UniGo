<template>
  <div class="bookings-container">
    <h1>我的预订</h1>
    
    <div class="bookings-list">
      <div v-if="loading" class="loading">加载中...</div>
      <div v-else-if="bookings.length === 0" class="no-bookings">暂无预订信息</div>
      <div v-else class="booking-cards">
        <div
          v-for="booking in bookings"
          :key="booking.id"
          class="booking-card"
        >
          <div class="booking-header">
            <h3>{{ booking.trip.departure }} → {{ booking.trip.destination }}</h3>
            <span class="booking-date">{{ formatDate(booking.trip.departure_time) }}</span>
          </div>
          
          <div class="booking-details">
            <p><strong>出发时间:</strong> {{ formatTime(booking.trip.departure_time) }}</p>
            <p><strong>司机:</strong> {{ booking.trip.driver_name }}</p>
            <p><strong>联系电话:</strong> {{ booking.trip.driver_phone }}</p>
            <p><strong>费用:</strong> ¥{{ booking.trip.price }}</p>
            <p><strong>预订时间:</strong> {{ formatDateTime(booking.created_at) }}</p>
            <p><strong>状态:</strong> 
              <span class="booking-status" :class="booking.status">
                {{ getBookingStatusText(booking.status) }}
              </span>
            </p>
          </div>
          
          <div class="booking-actions">
            <button 
              v-if="booking.status === 'confirmed'" 
              class="btn-cancel"
              @click="cancelBooking(booking.id)"
              :disabled="cancellingBookingId === booking.id"
            >
              {{ cancellingBookingId === booking.id ? '取消中...' : '取消预订' }}
            </button>
            <button 
              class="btn-detail"
              @click="viewTripDetail(booking.trip.id)"
            >
              查看详情
            </button>
          </div>
        </div>
      </div>
    </div>
    
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
      <router-link to="/profile" class="btn-back">返回个人中心</router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { getBookings, cancelBooking as cancelBookingApi } from '../api/bookingService'

const router = useRouter()
const authStore = useAuthStore()

// 预订数据
const bookings = ref<any[]>([])
const loading = ref(false)
const currentPage = ref(1)
const totalPages = ref(1)
const totalItems = ref(0)
const cancellingBookingId = ref<number | null>(null)

// 获取预订列表
const fetchBookings = async (page = 1) => {
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }
  
  loading.value = true
  try {
    const response = await getBookings({
      page,
      limit: 10
    })
    
    bookings.value = response.bookings
    currentPage.value = response.page
    totalPages.value = response.total_pages
    totalItems.value = response.total
  } catch (error) {
    console.error('获取预订信息失败:', error)
    alert('获取预订信息失败')
  } finally {
    loading.value = false
  }
}

// 取消预订
const cancelBooking = async (bookingId: number) => {
  if (!confirm('确定要取消此预订吗？')) {
    return
  }
  
  cancellingBookingId.value = bookingId
  try {
    await cancelBookingApi(bookingId)
    alert('预订已取消')
    // 重新获取预订列表
    await fetchBookings(currentPage.value)
  } catch (error: any) {
    alert(error.message || '取消预订失败')
  } finally {
    cancellingBookingId.value = null
  }
}

// 查看行程详情
const viewTripDetail = (tripId: number) => {
  router.push(`/trips/${tripId}`)
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

// 格式化日期时间
const formatDateTime = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

// 获取预订状态文本
const getBookingStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    'pending': '待确认',
    'confirmed': '已确认',
    'cancelled': '已取消',
    'completed': '已完成'
  }
  return statusMap[status] || status
}

// 切换页面
const changePage = (page: number) => {
  if (page >= 1 && page <= totalPages.value) {
    fetchBookings(page)
  }
}

// 组件挂载时获取预订列表
onMounted(() => {
  fetchBookings()
})
</script>

<style scoped>
.bookings-container {
  padding: 2rem;
}

.bookings-container h1 {
  color: #42b883;
  margin-bottom: 1.5rem;
}

.bookings-list {
  margin-bottom: 2rem;
}

.loading, .no-bookings {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.booking-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.booking-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1.5rem;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.booking-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
}

.booking-header h3 {
  margin: 0;
  color: #42b883;
}

.booking-date {
  color: #666;
  font-size: 0.9rem;
}

.booking-details p {
  margin: 0.5rem 0;
  color: #333;
}

.booking-status {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
}

.booking-status.pending {
  background-color: #fff3cd;
  color: #856404;
}

.booking-status.confirmed {
  background-color: #d4edda;
  color: #155724;
}

.booking-status.cancelled {
  background-color: #f8d7da;
  color: #721c24;
}

.booking-status.completed {
  background-color: #d1ecf1;
  color: #0c5460;
}

.booking-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.btn-cancel, .btn-detail {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.3s;
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

.btn-detail {
  background-color: #42b883;
  color: white;
}

.btn-detail:hover {
  background-color: #359c6d;
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

.btn-back {
  padding: 0.75rem 1.5rem;
  background-color: #6c757d;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  font-weight: 500;
  transition: background-color 0.3s;
}

.btn-back:hover {
  background-color: #545b62;
}
</style>