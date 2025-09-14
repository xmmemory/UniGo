<template>
  <div class="trips">
    <div class="trips-header">
      <h1>行程</h1>
      <router-link to="/publish-trip" class="btn btn-primary">发布行程</router-link>
    </div>

    <div class="search-filters">
      <div class="filter-group">
        <label for="departure">出发地</label>
        <!-- 使用地图地址选择器组件 -->
        <MapAddressSelector v-model="filters.departure" ref="departureSelector" />
      </div>
      <div class="filter-group">
        <label for="destination">目的地</label>
        <!-- 使用地图地址选择器组件 -->
        <MapAddressSelector v-model="filters.destination" />
      </div>
      <div class="filter-group">
        <label for="date">出发日期</label>
        <input type="date" id="date" v-model="filters.date">
      </div>
      <div class="filter-group">
        <label for="time">出发时间</label>
        <input type="time" id="time" v-model="filters.time">
      </div>
      <button class="btn btn-secondary" @click="searchTrips">搜索</button>
    </div>

    <div class="trips-list">
      <div class="trip-card" v-for="trip in filteredTrips" :key="trip.id">
        <div class="trip-header">
          <h3>{{ trip.departure }} → {{ trip.destination }}</h3>
          <span class="price">¥{{ trip.price_per_person }}</span>
        </div>
        <div class="trip-details">
          <p><strong>出发时间:</strong> {{ formatDate(trip.departure_time) }}</p>
          <p><strong>剩余座位:</strong> {{ trip.available_seats }}</p>
          <p><strong>发布者:</strong> {{ trip.owner_name || '未知' }}</p>
        </div>
        <div class="trip-actions">
          <button class="btn btn-primary" @click="bookTrip(trip.id)">预订</button>
        </div>
      </div>
    </div>
    
    <div v-if="filteredTrips.length === 0 && !loading" class="no-trips">
      <p>暂无符合条件的行程。</p>
      <!-- 调试信息 -->
      <div v-if="trips.length > 0" class="debug-info">
        <p>总行程数: {{ trips.length }}</p>
        <p>过滤后行程数: {{ filteredTrips.length }}</p>
        <p>过滤条件: {{ JSON.stringify(filters) }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { getPublicTrips, getTrips, createTrip } from '@/api/tripService'
import { createBooking } from '@/api/bookingService'
import { useAuthStore } from '@/stores/auth'
// 引入地图地址选择器组件（仅用于搜索过滤器）
import MapAddressSelector from '@/components/MapAddressSelector.vue'

// 定义行程数据结构
interface Trip {
  id: number
  departure: string
  destination: string
  departure_time: string
  price_per_person: number
  available_seats: number
  owner_name: string | null
  owner_id: number
}

// 定义地图选择器引用
interface MapSelectorInstance {
  getCurrentLocation: () => void
}

// 状态管理
const trips = ref<Trip[]>([])
const loading = ref(false)
const filters = ref({
  departure: '',
  destination: '',
  date: '',
  time: ''
})
const router = useRouter()
const authStore = useAuthStore()

// 地图选择器引用
const departureSelector = ref<MapSelectorInstance | null>(null)

// 根据过滤条件计算显示的行程
const filteredTrips = computed(() => {
  // 获取当前用户ID
  let currentUserId = null;
  let isLoggedIn = false;
  try {
    if (authStore.user) {
      currentUserId = authStore.user.id;
      isLoggedIn = true;
    }
  } catch (e) {
    console.error('解析用户信息失败:', e);
  }
  
  return trips.value.filter(trip => {
    // 只有在用户已登录时才排除当前用户自己发布的行程
    if (isLoggedIn && currentUserId && trip.owner_id === currentUserId) {
      return false;
    }
    
    // 出发地过滤 - 增强匹配逻辑
    if (filters.value.departure) {
      const departureFilter = filters.value.departure.trim().toLowerCase();
      const tripDeparture = trip.departure.trim().toLowerCase();
      
      // 如果过滤条件为空，跳过过滤
      if (!departureFilter) return true;
      
      // 支持多种匹配方式：
      // 1. 精确匹配
      // 2. 包含匹配
      // 3. 城市名称标准化匹配（北京/北京市）
      const isMatch = 
        tripDeparture === departureFilter ||
        tripDeparture.includes(departureFilter) ||
        departureFilter.includes(tripDeparture) ||
        normalizeCityName(tripDeparture).includes(normalizeCityName(departureFilter)) ||
        normalizeCityName(departureFilter).includes(normalizeCityName(tripDeparture));
      
      if (!isMatch) {
        return false;
      }
    }
    
    // 目的地过滤 - 增强匹配逻辑
    if (filters.value.destination) {
      const destinationFilter = filters.value.destination.trim().toLowerCase();
      const tripDestination = trip.destination.trim().toLowerCase();
      
      // 如果过滤条件为空，跳过过滤
      if (!destinationFilter) return true;
      
      // 支持多种匹配方式
      const isMatch = 
        tripDestination === destinationFilter ||
        tripDestination.includes(destinationFilter) ||
        destinationFilter.includes(tripDestination) ||
        normalizeCityName(tripDestination).includes(normalizeCityName(destinationFilter)) ||
        normalizeCityName(destinationFilter).includes(normalizeCityName(tripDestination));
      
      if (!isMatch) {
        return false;
      }
    }
    
    // 日期过滤
    if (filters.value.date) {
      try {
        const tripDate = new Date(trip.departure_time).toISOString().split('T')[0];
        if (tripDate !== filters.value.date) {
          return false;
        }
      } catch (e) {
        console.error('日期解析错误:', e);
        return false;
      }
    }
    
    // 时间过滤
    if (filters.value.time) {
      try {
        const tripTime = new Date(trip.departure_time).toTimeString().slice(0, 5);
        if (tripTime !== filters.value.time) {
          return false;
        }
      } catch (e) {
        console.error('时间解析错误:', e);
        return false;
      }
    }
    
    return true;
  });
});

// 城市名称标准化函数
const normalizeCityName = (cityName: string): string => {
  // 移除"市"字进行标准化匹配
  return cityName.replace(/市$/, '');
};

// 格式化日期
const formatDate = (dateString: string) => {
  try {
    const date = new Date(dateString)
    return date.toLocaleString('zh-CN')
  } catch (e) {
    console.error('日期格式化错误:', e)
    return '无效日期'
  }
}

// 搜索行程
const searchTrips = async () => {
  loading.value = true
  try {
    // 尝试从authStore获取token
    const token = authStore.token
    
    // 如果有token，使用需要认证的API；否则使用公开API
    let data;
    if (token) {
      data = await getTrips(token)
    } else {
      data = await getPublicTrips()
    }
    
    console.log('从API获取的数据:', data)
    trips.value = data
  } catch (error: any) {
    console.error('获取行程失败:', error)
    if (error.message && error.message.includes('登录')) {
      alert(error.message)
      authStore.logout()
      router.push('/login')
    } else {
      alert('获取行程失败，请稍后重试')
    }
  } finally {
    loading.value = false
  }
}

// 预订行程
const bookTrip = async (tripId: number) => {
  try {
    // 从authStore获取token
    const token = authStore.token
    if (!token) {
      alert('请先登录')
      router.push('/login')
      return
    }
    
    // 调用API进行预订
    const bookingData = { trip_id: tripId }
    await createBooking(bookingData, token)
    
    alert(`已预订行程 ${tripId}`)
    // 重新加载行程列表
    searchTrips()
  } catch (error: any) {
    console.error('预订失败:', error)
    if (error.message && error.message.includes('登录')) {
      alert(error.message)
      authStore.logout()
      router.push('/login')
    } else {
      alert('预订失败，请稍后重试')
    }
  }
}

// 组件挂载时加载数据和获取当前位置
onMounted(() => {
  searchTrips()
  
  // 设置默认日期为当前日期
  const today = new Date()
  filters.value.date = today.toISOString().split('T')[0]
  
  // 获取当前位置
  if (departureSelector.value) {
    departureSelector.value.getCurrentLocation()
  }
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

.no-trips {
  text-align: center;
  padding: 2rem 0;
}

.no-trips p {
  font-size: 1rem;
  margin-bottom: 1.5rem;
}

.debug-info {
  margin-top: 1rem;
  padding: 1rem;
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  text-align: left;
}

.debug-info p {
  margin: 0.2rem 0;
  font-size: 0.8rem;
  color: #6c757d;
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