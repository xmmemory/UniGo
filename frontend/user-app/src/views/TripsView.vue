<template>
  <div class="trips-container">
    <h1>行程列表</h1>
    
    <div class="search-filters">
      <div class="filter-group">
        <label for="departure">出发地</label>
        <input
          id="departure"
          v-model="searchFilters.departure"
          type="text"
          placeholder="请输入出发地"
        />
      </div>
      
      <div class="filter-group">
        <label for="destination">目的地</label>
        <input
          id="destination"
          v-model="searchFilters.destination"
          type="text"
          placeholder="请输入目的地"
        />
      </div>
      
      <div class="filter-group">
        <label for="date">出发日期</label>
        <input
          id="date"
          v-model="searchFilters.date"
          type="date"
        />
      </div>
      
      <button class="btn-search" @click="searchTrips">搜索</button>
    </div>
    
    <div class="trips-list">
      <div v-if="loading" class="loading">加载中...</div>
      <div v-else-if="trips.length === 0" class="no-trips">暂无行程信息</div>
      <div v-else class="trip-cards">
        <div
          v-for="trip in trips"
          :key="trip.id"
          class="trip-card"
          @click="viewTripDetail(trip.id)"
        >
          <div class="trip-header">
            <h3>{{ trip.departure }} → {{ trip.destination }}</h3>
            <span class="trip-date">{{ formatDate(trip.departure_time) }}</span>
          </div>
          
          <div class="trip-details">
            <p><strong>出发时间:</strong> {{ formatTime(trip.departure_time) }}</p>
            <p><strong>司机:</strong> {{ trip.owner_name }}</p>
            <p><strong>空位:</strong> {{ trip.available_seats }} 个</p>
            <p><strong>费用:</strong> ¥{{ trip.price_per_person }}</p>
          </div>
          
          <div class="trip-footer">
            <span class="trip-status" :class="trip.status">{{ getTripStatusText(trip.status) }}</span>
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
      <router-link to="/publish-trip" class="btn-primary">发布行程</router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getPublicTrips } from '../api/tripService'

const router = useRouter()

// 搜索过滤器
const searchFilters = reactive({
  departure: '',
  destination: '',
  date: ''
})

// 行程数据
const trips = ref<any[]>([])
const loading = ref(false)
const currentPage = ref(1)
const totalPages = ref(1)
const totalItems = ref(0)

// 获取公开行程列表
const fetchTrips = async (page = 1) => {
  loading.value = true
  try {
    const response = await getPublicTrips({
      page,
      limit: 10, // 每页显示10条数据
      departure: searchFilters.departure,
      destination: searchFilters.destination,
      date: searchFilters.date
    })
    
    // API返回包含分页信息的对象，需要提取items数组
    trips.value = response.items || response
    currentPage.value = response.page || page
    totalPages.value = response.total_pages || 1
    totalItems.value = response.total || trips.value.length
  } catch (error) {
    console.error('获取行程失败:', error)
    alert('获取行程失败')
  } finally {
    loading.value = false
  }
}

// 搜索行程
const searchTrips = () => {
  currentPage.value = 1
  fetchTrips(1)
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

// 获取行程状态文本
const getTripStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    'open': '开放中',
    'closed': '已关闭',
    'completed': '已完成'
  }
  return statusMap[status] || status
}

// 切换页面
const changePage = (page: number) => {
  if (page >= 1 && page <= totalPages.value) {
    fetchTrips(page)
  }
}

// 组件挂载时获取行程列表
onMounted(() => {
  fetchTrips()
})
</script>

<style scoped>
.trips-container {
  padding: 2rem;
  width: 100%;
  max-width: 100%;
  margin: 0 auto;
  box-sizing: border-box;
}

.trips-container h1 {
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
  width: 100%;
  box-sizing: border-box;
}

.filter-group {
  flex: 1;
  min-width: 200px;
  box-sizing: border-box;
}

.filter-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.filter-group input {
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
  box-sizing: border-box;
}

.trip-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  width: 100%;
  box-sizing: border-box;
}

.trip-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  cursor: pointer;
  transition: box-shadow 0.3s;
  width: 100%;
  box-sizing: border-box;
}

.trip-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.trip-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.trip-header h3 {
  margin: 0;
  color: #333;
}

.trip-date {
  font-size: 0.9rem;
  color: #666;
}

.trip-details p {
  margin: 0.5rem 0;
  color: #555;
}

.trip-footer {
  margin-top: 1rem;
  text-align: right;
}

.trip-status {
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

.actions {
  text-align: center;
  width: 100%;
  box-sizing: border-box;
}

.btn-primary {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background-color: #42b883;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  transition: background-color 0.3s;
  box-sizing: border-box;
}

.btn-primary:hover {
  background-color: #359c6d;
}

/* 分页控件样式 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
  width: 100%;
  box-sizing: border-box;
}

.pagination button {
  padding: 0.5rem 1rem;
  background-color: #42b883;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  box-sizing: border-box;
}

.pagination button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

/* 响应式断点优化 */
/* 超小屏幕 (手机, 小于576px) */
@media (max-width: 575.98px) {
  .trips-container {
    padding: 0.75rem 0.5rem;
  }
  
  .trips-container h1 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
  }
  
  .search-filters {
    padding: 0.75rem 0.5rem;
    gap: 0.75rem;
    margin-bottom: 1rem;
  }
  
  .filter-group {
    min-width: 100%;
  }
  
  .filter-group label {
    font-size: 0.9rem;
    margin-bottom: 0.25rem;
  }
  
  .filter-group input {
    padding: 0.5rem;
    font-size: 0.9rem;
  }
  
  .btn-search {
    width: 100%;
    padding: 0.75rem;
    font-size: 0.9rem;
  }
  
  .trip-cards {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.75rem;
  }
  
  .trip-card {
    padding: 0.75rem;
  }
  
  .trip-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
    margin-bottom: 0.75rem;
  }
  
  .trip-header h3 {
    font-size: 1rem;
  }
  
  .trip-date {
    font-size: 0.8rem;
  }
  
  .trip-details p {
    margin: 0.25rem 0;
    font-size: 0.85rem;
  }
  
  .trip-status {
    font-size: 0.7rem;
    padding: 0.15rem 0.3rem;
  }
  
  .pagination {
    gap: 0.5rem;
    font-size: 0.85rem;
    margin-bottom: 1rem;
  }
  
  .pagination button {
    padding: 0.3rem 0.6rem;
    font-size: 0.8rem;
  }
  
  .actions {
    padding: 0 0.25rem;
  }
  
  .btn-primary {
    padding: 0.6rem 1rem;
    font-size: 0.9rem;
  }
}

/* 小屏幕 (手机横屏, 576px及以上) */
@media (min-width: 576px) and (max-width: 767.98px) {
  .filter-group {
    min-width: 150px;
  }
  
  .trip-cards {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
}

/* 中等屏幕 (平板, 768px及以上) */
@media (min-width: 768px) {
  .trips-container {
    padding: 1.5rem;
  }
  
  .search-filters {
    padding: 1rem;
    gap: 1rem;
  }
  
  .filter-group {
    min-width: 180px;
  }
  
  .trip-cards {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
  }
  
  .trip-card {
    padding: 1rem;
  }
  
  .trip-header {
    flex-direction: row;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1rem;
  }
  
  .trip-header h3 {
    font-size: 1.1rem;
  }
  
  .trip-date {
    font-size: 0.9rem;
  }
  
  .trip-details p {
    margin: 0.5rem 0;
    font-size: 0.9rem;
  }
  
  .trip-status {
    font-size: 0.8rem;
    padding: 0.25rem 0.5rem;
  }
  
  .pagination {
    gap: 1rem;
    font-size: 1rem;
    margin-bottom: 2rem;
  }
  
  .pagination button {
    padding: 0.5rem 1rem;
    font-size: 1rem;
  }
  
  .btn-primary {
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
  }
}

/* 大屏幕 (桌面, 992px及以上) */
@media (min-width: 992px) {
  .trips-container {
    padding: 2rem;
  }
  
  .search-filters {
    padding: 1.5rem;
  }
  
  .filter-group {
    min-width: 200px;
  }
  
  .trip-cards {
    gap: 2rem;
  }
  
  .trip-card {
    padding: 1.5rem;
  }
  
  .trip-header h3 {
    font-size: 1.2rem;
  }
  
  .trip-details p {
    font-size: 1rem;
  }
  
  .actions {
    margin-top: 1rem;
  }
}

/* 超大屏幕 (大桌面, 1200px及以上) */
@media (min-width: 1200px) {
  .trips-container {
    padding: 2rem;
    max-width: 1400px;
  }
  
  .trip-cards {
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  }
  
  .trip-card {
    padding: 2rem;
  }
}

/* 超宽屏 (1600px及以上) */
@media (min-width: 1600px) {
  .trips-container {
    padding: 3rem;
    max-width: 1600px;
  }
  
  .search-filters {
    padding: 2rem;
    gap: 1.5rem;
  }
  
  .trip-cards {
    grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
    gap: 2.5rem;
  }
  
  .trip-card {
    padding: 2.5rem;
  }
  
  .trip-header h3 {
    font-size: 1.4rem;
  }
  
  .trip-details p {
    font-size: 1.1rem;
  }
}

/* 超宽屏 (2000px及以上) */
@media (min-width: 2000px) {
  .trips-container {
    padding: 4rem;
    max-width: 1800px;
  }
  
  .search-filters {
    padding: 3rem;
    gap: 2rem;
  }
  
  .trip-cards {
    grid-template-columns: repeat(auto-fill, minmax(450px, 1fr));
    gap: 3rem;
  }
  
  .trip-card {
    padding: 3rem;
  }
  
  .trip-header h3 {
    font-size: 1.6rem;
  }
  
  .trip-details p {
    font-size: 1.2rem;
  }
  
  .pagination {
    gap: 1.5rem;
    font-size: 1.2rem;
    margin-bottom: 3rem;
  }
  
  .pagination button {
    padding: 0.75rem 1.5rem;
    font-size: 1.2rem;
  }
  
  .btn-primary {
    padding: 1rem 2rem;
    font-size: 1.2rem;
  }
}
</style>