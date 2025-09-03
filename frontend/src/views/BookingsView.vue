<template>
  <div class="bookings">
    <h1>我的预订</h1>
    
    <div class="bookings-list">
      <div class="booking-card" v-for="booking in bookings" :key="booking.id">
        <div class="booking-header">
          <h3>{{ booking.trip.departure }} → {{ booking.trip.destination }}</h3>
          <span class="status" :class="booking.status">{{ booking.status }}</span>
        </div>
        <div class="booking-details">
          <p><strong>预订时间:</strong> {{ formatDate(booking.booked_at) }}</p>
          <p><strong>出发时间:</strong> {{ formatDate(booking.trip.departure_time) }}</p>
          <p><strong>价格:</strong> ¥{{ booking.trip.price_per_person }}</p>
          <p><strong>发布者:</strong> {{ booking.trip.owner_name }}</p>
        </div>
        <div class="booking-actions">
          <button class="btn btn-secondary" @click="cancelBooking(booking.id)">取消预订</button>
        </div>
      </div>
    </div>
    
    <div v-if="bookings.length === 0" class="no-bookings">
      <p>您还没有任何预订。</p>
      <router-link to="/trips" class="btn btn-primary">查找行程</router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

// 定义预订数据结构
interface Booking {
  id: number
  booked_at: string
  status: string
  trip: {
    id: number
    departure: string
    destination: string
    departure_time: string
    price_per_person: number
    owner_name: string
  }
}

// 状态管理
const bookings = ref<Booking[]>([])

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

// 取消预订
const cancelBooking = (bookingId: number) => {
  console.log('取消预订:', bookingId)
  // 这里应该调用API取消预订
  alert(`已取消预订 ${bookingId}`)
  // 重新加载预订列表
  loadBookings()
}

// 加载预订数据
const loadBookings = () => {
  // 这里应该调用API获取预订数据
  // 暂时使用模拟数据
  bookings.value = [
    {
      id: 1,
      booked_at: '2025-09-03T10:30:00',
      status: 'confirmed',
      trip: {
        id: 1,
        departure: '北京',
        destination: '上海',
        departure_time: '2025-09-05T08:00:00',
        price_per_person: 150,
        owner_name: '张三'
      }
    },
    {
      id: 2,
      booked_at: '2025-09-02T14:20:00',
      status: 'pending',
      trip: {
        id: 2,
        departure: '上海',
        destination: '广州',
        departure_time: '2025-09-06T14:30:00',
        price_per_person: 120,
        owner_name: '李四'
      }
    }
  ]
}

// 组件挂载时加载数据
onMounted(() => {
  loadBookings()
})
</script>

<style scoped>
.bookings {
  padding: 1rem 0;
}

.bookings-list {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

.booking-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.booking-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.8rem;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.booking-header h3 {
  margin: 0;
  color: #42b883;
  font-size: 1.1rem;
}

.status {
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: bold;
}

.status.confirmed {
  background-color: #d4edda;
  color: #155724;
}

.status.pending {
  background-color: #fff3cd;
  color: #856404;
}

.status.cancelled {
  background-color: #f8d7da;
  color: #721c24;
}

.booking-details p {
  margin: 0.4rem 0;
  font-size: 0.9rem;
}

.booking-actions {
  margin-top: 1rem;
  text-align: right;
}

.no-bookings {
  text-align: center;
  padding: 2rem 0;
}

.no-bookings p {
  font-size: 1rem;
  margin-bottom: 1.5rem;
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
  .bookings {
    padding: 2rem 0;
  }
  
  .bookings-list {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 2rem;
  }
  
  .booking-card {
    padding: 1.5rem;
  }
  
  .booking-header h3 {
    font-size: 1.3rem;
  }
  
  .booking-header {
    flex-wrap: nowrap;
  }
  
  .status {
    font-size: 0.8rem;
  }
  
  .booking-details p {
    margin: 0.5rem 0;
    font-size: 1rem;
  }
  
  .no-bookings {
    padding: 3rem 0;
  }
  
  .no-bookings p {
    font-size: 1.2rem;
    margin-bottom: 2rem;
  }
  
  .btn {
    padding: 0.8rem 1.5rem;
  }
}
</style>