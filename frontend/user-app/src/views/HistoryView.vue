<template>
  <div class="history-container">
    <h1>历史记录</h1>
    
    <div class="history-tabs">
      <button
        :class="{ active: activeTab === 'as-driver' }"
        @click="activeTab = 'as-driver'"
      >
        作为司机
      </button>
      <button
        :class="{ active: activeTab === 'as-passenger' }"
        @click="activeTab = 'as-passenger'"
      >
        作为乘客
      </button>
    </div>
    
    <div class="history-content">
      <div v-if="activeTab === 'as-driver' ? loadingDriverTrips : loadingPassengerBookings" class="loading">加载中...</div>
      <div v-else-if="activeTab === 'as-driver'">
        <div v-if="driverTrips.length === 0" class="no-history">暂无作为司机的历史记录</div>
        <div v-else class="history-list">
          <div
            v-for="trip in driverTrips"
            :key="trip.id"
            class="history-item"
          >
            <div class="history-header">
              <h3>{{ trip.departure }} → {{ trip.destination }}</h3>
              <span class="trip-date">{{ formatDate(trip.departure_time) }}</span>
            </div>
            
            <div class="history-details">
              <p><strong>出发时间:</strong> {{ formatTime(trip.departure_time) }}</p>
              <p><strong>空位:</strong> {{ trip.available_seats }} 个</p>
              <p><strong>费用:</strong> ¥{{ trip.price }}</p>
              <p><strong>状态:</strong> 
                <span class="trip-status" :class="trip.status">
                  {{ getTripStatusText(trip.status) }}
                </span>
              </p>
              <p v-if="trip.passengers && trip.passengers.length > 0">
                <strong>乘客:</strong> 
                <span v-for="passenger in trip.passengers" :key="passenger.id" class="passenger">
                  {{ passenger.name }}
                </span>
              </p>
            </div>
          </div>
        </div>
      </div>
      
      <div v-else-if="activeTab === 'as-passenger'">
        <div v-if="passengerBookings.length === 0" class="no-history">暂无作为乘客的历史记录</div>
        <div v-else class="history-list">
          <div
            v-for="booking in passengerBookings"
            :key="booking.id"
            class="history-item"
          >
            <div class="history-header">
              <h3>{{ booking.trip.departure }} → {{ booking.trip.destination }}</h3>
              <span class="trip-date">{{ formatDate(booking.trip.departure_time) }}</span>
            </div>
            
            <div class="history-details">
              <p><strong>出发时间:</strong> {{ formatTime(booking.trip.departure_time) }}</p>
              <p><strong>司机:</strong> {{ booking.trip.driver_name }}</p>
              <p><strong>费用:</strong> ¥{{ booking.trip.price }}</p>
              <p><strong>预订时间:</strong> {{ formatDateTime(booking.created_at) }}</p>
              <p><strong>状态:</strong> 
                <span class="booking-status" :class="booking.status">
                  {{ getBookingStatusText(booking.status) }}
                </span>
              </p>
            </div>
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
import { useAuthStore } from '../stores/auth'
import { getDriverTrips, getPassengerBookings } from '../api/tripService'

const authStore = useAuthStore()

// 活动标签页
const activeTab = ref('as-driver')

// 司机行程数据
const driverTrips = ref<any[]>([])
const loadingDriverTrips = ref(false)

// 乘客预订数据
const passengerBookings = ref<any[]>([])
const loadingPassengerBookings = ref(false)

// 分页数据
const currentPage = ref(1)
const totalPages = ref(1)
const totalItems = ref(0)

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

// 获取行程状态文本
const getTripStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    'open': '开放中',
    'closed': '已关闭',
    'completed': '已完成'
  }
  return statusMap[status] || status
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

// 获取作为司机的行程
const fetchDriverTrips = async (page = 1) => {
  if (!authStore.isAuthenticated) {
    return
  }
  
  loadingDriverTrips.value = true
  try {
    const response = await getDriverTrips({
      page,
      limit: 10
    })
    
    driverTrips.value = response.trips
    currentPage.value = response.page
    totalPages.value = response.total_pages
    totalItems.value = response.total
  } catch (error) {
    console.error('获取司机行程失败:', error)
    alert('获取司机行程失败')
  } finally {
    loadingDriverTrips.value = false
  }
}

// 获取作为乘客的预订
const fetchPassengerBookings = async (page = 1) => {
  if (!authStore.isAuthenticated) {
    return
  }
  
  loadingPassengerBookings.value = true
  try {
    const response = await getPassengerBookings({
      page,
      limit: 10
    })
    
    passengerBookings.value = response.bookings
    currentPage.value = response.page
    totalPages.value = response.total_pages
    totalItems.value = response.total
  } catch (error) {
    console.error('获取乘客预订失败:', error)
    alert('获取乘客预订失败')
  } finally {
    loadingPassengerBookings.value = false
  }
}

// 切换页面
const changePage = (page: number) => {
  if (page >= 1 && page <= totalPages.value) {
    if (activeTab.value === 'as-driver') {
      fetchDriverTrips(page)
    } else {
      fetchPassengerBookings(page)
    }
  }
}

// 组件挂载时获取数据
onMounted(() => {
  fetchDriverTrips(1)
})
</script>

<style scoped>
.history-container {
  padding: 2rem;
}

.history-container h1 {
  color: #42b883;
  margin-bottom: 1.5rem;
}

.history-tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid #eee;
}

.history-tabs button {
  padding: 0.75rem 1.5rem;
  background: none;
  border: none;
  border-bottom: 3px solid transparent;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  color: #666;
}

.history-tabs button.active {
  color: #42b883;
  border-bottom-color: #42b883;
}

.history-content {
  margin-bottom: 2rem;
}

.loading, .no-history {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.history-item {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1.5rem;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
}

.history-header h3 {
  margin: 0;
  color: #42b883;
}

.trip-date {
  color: #666;
  font-size: 0.9rem;
}

.history-details p {
  margin: 0.5rem 0;
  color: #333;
}

.trip-status, .booking-status {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
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

.passenger {
  display: inline-block;
  margin-right: 0.5rem;
  padding: 0.25rem 0.5rem;
  background-color: #f8f9fa;
  border-radius: 4px;
  font-size: 0.8rem;
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