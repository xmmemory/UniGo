<template>
  <div class="trips">
    <div class="trips-header">
      <h1>行程列表</h1>
      <button class="btn btn-primary" @click="showCreateForm = true">发布行程</button>
    </div>

    <div class="search-filters">
      <div class="filter-group">
        <label for="departure">出发地</label>
        <input type="text" id="departure" v-model="filters.departure" placeholder="请输入出发地">
      </div>
      <div class="filter-group">
        <label for="destination">目的地</label>
        <input type="text" id="destination" v-model="filters.destination" placeholder="请输入目的地">
      </div>
      <div class="filter-group">
        <label for="date">出发日期</label>
        <input type="date" id="date" v-model="filters.date">
      </div>
      <button class="btn btn-secondary" @click="searchTrips">搜索</button>
    </div>

    <div class="trips-list">
      <div class="trip-card" v-for="trip in trips" :key="trip.id">
        <div class="trip-header">
          <h3>{{ trip.departure }} → {{ trip.destination }}</h3>
          <span class="price">¥{{ trip.price_per_person }}</span>
        </div>
        <div class="trip-details">
          <p><strong>出发时间:</strong> {{ formatDate(trip.departure_time) }}</p>
          <p><strong>剩余座位:</strong> {{ trip.available_seats }}</p>
          <p><strong>发布者:</strong> {{ trip.owner_name }}</p>
        </div>
        <div class="trip-actions">
          <button class="btn btn-primary" @click="bookTrip(trip.id)">预订</button>
        </div>
      </div>
    </div>

    <!-- 创建行程表单 -->
    <div class="modal" v-if="showCreateForm">
      <div class="modal-content">
        <span class="close" @click="showCreateForm = false">&times;</span>
        <h2>发布新行程</h2>
        <form @submit.prevent="createNewTrip">
          <div class="form-group">
            <label for="newDeparture">出发地</label>
            <input type="text" id="newDeparture" v-model="newTrip.departure" required>
          </div>
          <div class="form-group">
            <label for="newDestination">目的地</label>
            <input type="text" id="newDestination" v-model="newTrip.destination" required>
          </div>
          <div class="form-group">
            <label for="newDepartureTime">出发时间</label>
            <input type="datetime-local" id="newDepartureTime" v-model="newTrip.departure_time" required>
          </div>
          <div class="form-group">
            <label for="newPrice">每人价格 (¥)</label>
            <input type="number" id="newPrice" v-model="newTrip.price_per_person" required min="0" step="0.01">
          </div>
          <div class="form-group">
            <label for="newSeats">座位数量</label>
            <input type="number" id="newSeats" v-model="newTrip.available_seats" required min="1">
          </div>
          <button type="submit" class="btn btn-primary">发布行程</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getTrips, createTrip } from '@/api/tripService'
import { createBooking } from '@/api/bookingService'

// 定义行程数据结构
interface Trip {
  id: number
  departure: string
  destination: string
  departure_time: string
  price_per_person: number
  available_seats: number
  owner_name: string
}

// 状态管理
const trips = ref<Trip[]>([])
const showCreateForm = ref(false)
const filters = ref({
  departure: '',
  destination: '',
  date: ''
})

const newTrip = ref({
  departure: '',
  destination: '',
  departure_time: '',
  price_per_person: 0,
  available_seats: 1
})

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

// 搜索行程
const searchTrips = async () => {
  try {
    // 从localStorage获取token
    const token = localStorage.getItem('token')
    if (!token) {
      alert('请先登录')
      return
    }
    
    // 调用API获取行程数据
    const data = await getTrips(token)
    trips.value = data
  } catch (error) {
    console.error('获取行程失败:', error)
    // 使用模拟数据作为后备
    trips.value = [
      {
        id: 1,
        departure: '北京',
        destination: '上海',
        departure_time: '2025-09-05T08:00:00',
        price_per_person: 150,
        available_seats: 3,
        owner_name: '张三'
      },
      {
        id: 2,
        departure: '上海',
        destination: '广州',
        departure_time: '2025-09-06T14:30:00',
        price_per_person: 120,
        available_seats: 2,
        owner_name: '李四'
      }
    ]
  }
}

// 预订行程
const bookTrip = async (tripId: number) => {
  try {
    // 从localStorage获取token
    const token = localStorage.getItem('token')
    if (!token) {
      alert('请先登录')
      return
    }
    
    // 调用API进行预订
    const bookingData = { trip_id: tripId }
    await createBooking(bookingData, token)
    
    alert(`已预订行程 ${tripId}`)
    // 重新加载行程列表
    searchTrips()
  } catch (error) {
    console.error('预订失败:', error)
    alert('预订失败，请稍后重试')
  }
}

// 创建行程
const createNewTrip = async () => {
  try {
    // 从localStorage获取token
    const token = localStorage.getItem('token')
    if (!token) {
      alert('请先登录')
      return
    }
    
    // 调用API创建行程
    const tripData = {
      departure: newTrip.value.departure,
      destination: newTrip.value.destination,
      departure_time: newTrip.value.departure_time,
      price_per_person: newTrip.value.price_per_person,
      available_seats: newTrip.value.available_seats
    }
    
    await createTrip(tripData, token)
    
    alert('行程创建成功！')
    showCreateForm.value = false
    // 重置表单
    newTrip.value = {
      departure: '',
      destination: '',
      departure_time: '',
      price_per_person: 0,
      available_seats: 1
    }
    // 重新加载行程列表
    searchTrips()
  } catch (error) {
    console.error('创建行程失败:', error)
    alert('行程创建失败，请稍后重试')
  }
}

// 组件挂载时加载数据
onMounted(() => {
  searchTrips()
})
</script>

<style scoped>
.trips {
  padding: 1rem 0;
}

.trips-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.trips-header h1 {
  margin: 0;
  font-size: 1.5rem;
}

.search-filters {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.filter-group {
  display: flex;
  flex-direction: column;
}

.filter-group label {
  margin-bottom: 0.5rem;
  font-weight: bold;
  font-size: 0.9rem;
}

.filter-group input {
  padding: 0.7rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
}

.trips-list {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

.trip-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.trip-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.8rem;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.trip-header h3 {
  margin: 0;
  color: #42b883;
  font-size: 1.1rem;
}

.price {
  font-size: 1.1rem;
  font-weight: bold;
  color: #e74c3c;
}

.trip-details p {
  margin: 0.4rem 0;
  font-size: 0.9rem;
}

.trip-actions {
  margin-top: 1rem;
  text-align: right;
}

/* Modal 样式 */
.modal {
  position: fixed;
  z-index: 1000;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem;
}

.modal-content {
  background-color: white;
  padding: 1.5rem;
  border-radius: 8px;
  width: 95%;
  max-width: 500px;
  position: relative;
  max-height: 90vh;
  overflow-y: auto;
}

.close {
  position: absolute;
  right: 1rem;
  top: 1rem;
  font-size: 2rem;
  cursor: pointer;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

.form-group input {
  width: 100%;
  padding: 0.7rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  box-sizing: border-box;
  font-size: 1rem;
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
  width: 100%;
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
  .trips {
    padding: 2rem 0;
  }
  
  .trips-header h1 {
    font-size: 2rem;
  }
  
  .search-filters {
    flex-direction: row;
    gap: 1rem;
    align-items: end;
  }
  
  .filter-group label {
    font-size: 1rem;
  }
  
  .trips-list {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 2rem;
  }
  
  .trip-header h3 {
    font-size: 1.3rem;
  }
  
  .trip-header {
    flex-wrap: nowrap;
  }
  
  .modal-content {
    padding: 2rem;
    width: 90%;
  }
  
  .btn {
    width: auto;
    padding: 0.8rem 1.5rem;
  }
}

@media (min-width: 1024px) {
  .search-filters {
    flex-wrap: wrap;
  }
}
</style>