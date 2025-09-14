<template>
  <div class="history">
    <div class="history-header">
      <h1>历史订单</h1>
      <router-link to="/profile" class="btn btn-secondary">返回个人中心</router-link>
    </div>
    
    <!-- 作为乘客的历史预订 -->
    <div class="section">
      <h2>我预订的历史行程</h2>
      <div class="bookings-list">
        <div class="booking-card" v-for="booking in passengerHistory" :key="booking.id">
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
        </div>
      </div>
      
      <div v-if="passengerHistory.length === 0" class="no-bookings">
        <p>您还没有历史预订记录。</p>
      </div>
    </div>
    
    <!-- 作为发布者的历史行程 -->
    <div class="section">
      <h2>我发布的历史行程</h2>
      <div class="trips-list">
        <div class="trip-card" v-for="trip in publishedHistory" :key="trip.id">
          <div class="trip-header">
            <h3>{{ trip.departure }} → {{ trip.destination }}</h3>
            <span class="price">¥{{ trip.price_per_person }}</span>
          </div>
          <div class="trip-details">
            <p><strong>出发时间:</strong> {{ formatDate(trip.departure_time) }}</p>
            <p><strong>总座位:</strong> {{ trip.available_seats + (trip.bookings_count || 0) }}</p>
            <p><strong>预订人数:</strong> {{ trip.bookings_count || 0 }}</p>
          </div>
        </div>
      </div>
      
      <div v-if="publishedHistory.length === 0" class="no-trips">
        <p>您还没有历史发布记录。</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getUserBookings } from '@/api/bookingService'
import { getTrips } from '@/api/tripService'

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

// 定义行程数据结构
interface Trip {
  id: number
  departure: string
  destination: string
  departure_time: string
  price_per_person: number
  available_seats: number
  bookings_count: number
}

// 状态管理
const passengerHistory = ref<Booking[]>([])
const publishedHistory = ref<Trip[]>([])

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

// 加载乘客历史预订数据
const loadPassengerHistory = async () => {
  try {
    // 从localStorage获取token
    const token = localStorage.getItem('token')
    if (!token) {
      console.error('未找到认证token')
      return
    }
    
    // 调用API获取预订数据
    const bookingsData = await getUserBookings(token)
    
    // 过滤出已结束的行程（这里简单地假设出发时间在当前时间之前的为已结束）
    const now = new Date()
    passengerHistory.value = bookingsData.filter((booking: Booking) => {
      const departureTime = new Date(booking.trip.departure_time)
      return departureTime < now
    }).map((booking: any) => ({
      ...booking,
      status: booking.status || 'completed' // 如果没有状态字段，设置默认值
    }))
  } catch (error) {
    console.error('加载历史预订数据失败:', error)
    // 使用模拟数据作为后备
    passengerHistory.value = []
  }
}

// 加载发布的历史行程数据
const loadPublishedHistory = async () => {
  try {
    // 从localStorage获取token
    const token = localStorage.getItem('token')
    if (!token) {
      console.error('未找到认证token')
      return
    }
    
    // 调用API获取行程数据
    const tripsData = await getTrips(token)
    
    // 过滤出已结束的行程（这里简单地假设出发时间在当前时间之前的为已结束）
    const now = new Date()
    publishedHistory.value = tripsData.filter((trip: Trip) => {
      const departureTime = new Date(trip.departure_time)
      return departureTime < now
    }).map((trip: any) => ({
      id: trip.id,
      departure: trip.departure,
      destination: trip.destination,
      departure_time: trip.departure_time,
      price_per_person: trip.price_per_person,
      available_seats: trip.available_seats,
      bookings_count: trip.bookings ? trip.bookings.length : 0
    }))
  } catch (error) {
    console.error('加载发布的历史行程数据失败:', error)
    // 使用模拟数据作为后备
    publishedHistory.value = []
  }
}

// 组件挂载时加载数据
onMounted(() => {
  loadPassengerHistory()
  loadPublishedHistory()
})
</script>

<style scoped>
.history {
  padding: 1rem 0;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.history-header h1 {
  margin: 0;
  font-size: 1.5rem;
}

.section {
  margin-bottom: 2rem;
}

.section h2 {
  margin-bottom: 1rem;
  color: #42b883;
  font-size: 1.3rem;
}

.bookings-list, .trips-list {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

.booking-card, .trip-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.booking-header, .trip-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.8rem;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.booking-header h3, .trip-header h3 {
  margin: 0;
  color: #42b883;
  font-size: 1.1rem;
}

.status, .price {
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

.status.completed {
  background-color: #cce5ff;
  color: #004085;
}

.price {
  background-color: #e74c3c;
  color: white;
}

.booking-details p, .trip-details p {
  margin: 0.4rem 0;
  font-size: 0.9rem;
}

.no-bookings, .no-trips {
  text-align: center;
  padding: 2rem 0;
}

.no-bookings p, .no-trips p {
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
  display: inline-block;
  text-align: center;
}

.btn:hover {
  opacity: 0.9;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

/* 平板和桌面端适配 */
@media (min-width: 768px) {
  .history {
    padding: 2rem 0;
  }
  
  .history-header h1 {
    font-size: 2rem;
  }
  
  .section h2 {
    font-size: 1.5rem;
  }
  
  .bookings-list, .trips-list {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 2rem;
  }
  
  .booking-card, .trip-card {
    padding: 1.5rem;
  }
  
  .booking-header h3, .trip-header h3 {
    font-size: 1.3rem;
  }
  
  .booking-header, .trip-header {
    flex-wrap: nowrap;
  }
  
  .status, .price {
    font-size: 0.8rem;
  }
  
  .booking-details p, .trip-details p {
    margin: 0.5rem 0;
    font-size: 1rem;
  }
  
  .no-bookings, .no-trips {
    padding: 3rem 0;
  }
  
  .no-bookings p, .no-trips p {
    font-size: 1.2rem;
    margin-bottom: 2rem;
  }
  
  .btn {
    padding: 0.8rem 1.5rem;
  }
}
</style>