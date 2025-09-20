<template>
  <div class="trip-management">
    <h1>拼车管理</h1>
    
    <div class="toolbar">
      <div class="search-box">
        <input 
          type="text" 
          placeholder="搜索行程..." 
          v-model="searchQuery"
          @input="handleSearch"
        />
        <button @click="searchTrips">搜索</button>
      </div>
      <button class="btn-primary" @click="showCreateTripModal">创建行程</button>
    </div>
    
    <div class="table-container">
      <table class="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>出发地</th>
            <th>目的地</th>
            <th>出发时间</th>
            <th>司机</th>
            <th>空位</th>
            <th>费用</th>
            <th>状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="trip in trips" :key="trip.id">
            <td>{{ trip.id }}</td>
            <td>{{ trip.departure }}</td>
            <td>{{ trip.destination }}</td>
            <td>{{ formatDateTime(trip.departure_time) }}</td>
            <td>{{ trip.owner_name }}</td>
            <td>{{ trip.available_seats }}</td>
            <td>¥{{ trip.price_per_person }}</td>
            <td>
              <span :class="['status', getTripStatusClass(trip.status)]">
                {{ getTripStatusText(trip.status) }}
              </span>
            </td>
            <td>
              <button class="btn-small" @click="viewTrip(trip)">查看</button>
              <button class="btn-small" @click="editTrip(trip)">编辑</button>
              <button 
                :class="['btn-small', trip.status === 'open' ? 'btn-warning' : 'btn-success']"
                @click="toggleTripStatus(trip)"
              >
                {{ trip.status === 'open' ? '关闭' : '开启' }}
              </button>
              <button class="btn-small btn-danger" @click="deleteTrip(trip)">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <div class="pagination">
      <button 
        :disabled="currentPage === 1" 
        @click="changePage(currentPage - 1)"
      >
        上一页
      </button>
      <span>第 {{ currentPage }} 页，共 {{ totalPages }} 页</span>
      <button 
        :disabled="currentPage === totalPages" 
        @click="changePage(currentPage + 1)"
      >
        下一页
      </button>
    </div>
    
    <!-- 创建/编辑行程模态框 -->
    <div class="modal" v-if="showModal">
      <div class="modal-content">
        <h2>{{ editingTrip ? '编辑行程' : '创建行程' }}</h2>
        <form @submit.prevent="saveTrip">
          <div class="form-row">
            <div class="form-group">
              <label for="departure">出发地</label>
              <input 
                type="text" 
                id="departure" 
                v-model="tripForm.departure" 
                required 
              />
            </div>
            <div class="form-group">
              <label for="destination">目的地</label>
              <input 
                type="text" 
                id="destination" 
                v-model="tripForm.destination" 
                required 
              />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="departure_time">出发时间</label>
              <input 
                type="datetime-local" 
                id="departure_time" 
                v-model="tripForm.departure_time" 
                required 
              />
            </div>
            <div class="form-group">
              <label for="available_seats">空位</label>
              <input 
                type="number" 
                id="available_seats" 
                v-model="tripForm.available_seats" 
                min="1" 
                required 
              />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="price_per_person">费用(元)</label>
              <input 
                type="number" 
                id="price_per_person" 
                v-model="tripForm.price_per_person" 
                min="0" 
                step="0.01" 
                required 
              />
            </div>
            <div class="form-group">
              <label for="status">状态</label>
              <select id="status" v-model="tripForm.status">
                <option value="open">开放中</option>
                <option value="closed">已关闭</option>
                <option value="completed">已完成</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label for="description">描述</label>
            <textarea 
              id="description" 
              v-model="tripForm.description" 
              rows="3"
            ></textarea>
          </div>
          <div class="form-actions">
            <button type="button" @click="closeModal" class="btn-secondary">取消</button>
            <button type="submit" class="btn-primary">保存</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getAdminTrips } from '../api/adminService'
import { useAdminStore } from '../stores/admin'

const adminStore = useAdminStore()
const trips = ref<any[]>([])
const loading = ref(false)
const currentPage = ref(1)
const totalPages = ref(1)
const totalItems = ref(0)
const searchQuery = ref('')
const showModal = ref(false)
const editingTrip = ref(null)
const tripForm = ref({
  departure: '',
  destination: '',
  departure_time: '',
  available_seats: 1,
  price_per_person: 0,
  description: '',
  status: 'open'
})

// 获取行程列表
const fetchTrips = async (page = 1) => {
  loading.value = true
  try {
    const response = await getAdminTrips((page - 1) * 10, 10)
    trips.value = response
    totalItems.value = response.length
    totalPages.value = Math.ceil(totalItems.value / 10)
    currentPage.value = page
  } catch (error) {
    console.error('获取行程列表失败:', error)
    alert('获取行程列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索行程
const searchTrips = () => {
  // 这里可以实现搜索逻辑
  console.log('搜索行程:', searchQuery.value)
  fetchTrips(1)
}

// 处理搜索输入
const handleSearch = () => {
  // 可以实现防抖搜索
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

// 获取行程状态类名
const getTripStatusClass = (status: string) => {
  const classMap: Record<string, string> = {
    'open': 'open',
    'closed': 'closed',
    'completed': 'completed'
  }
  return classMap[status] || status
}

// 改变页面
const changePage = (page: number) => {
  fetchTrips(page)
}

// 显示创建行程模态框
const showCreateTripModal = () => {
  editingTrip.value = null
  tripForm.value = {
    departure: '',
    destination: '',
    departure_time: '',
    available_seats: 1,
    price_per_person: 0,
    description: '',
    status: 'open'
  }
  showModal.value = true
}

// 查看行程
const viewTrip = (trip: any) => {
  // 这里可以实现查看行程详情的逻辑
  console.log('查看行程:', trip)
}

// 编辑行程
const editTrip = (trip: any) => {
  editingTrip.value = trip
  tripForm.value = {
    departure: trip.departure,
    destination: trip.destination,
    departure_time: trip.departure_time,
    available_seats: trip.available_seats,
    price_per_person: trip.price_per_person,
    description: trip.description,
    status: trip.status
  }
  showModal.value = true
}

// 切换行程状态
const toggleTripStatus = (trip: any) => {
  const newStatus = trip.status === 'open' ? 'closed' : 'open'
  const action = trip.status === 'open' ? '关闭' : '开启'
  if (confirm(`确定要${action}行程 ${trip.departure} → ${trip.destination} 吗？`)) {
    // 这里可以实现切换行程状态的逻辑
    console.log(`切换行程状态为 ${newStatus}`)
  }
}

// 删除行程
const deleteTrip = (trip: any) => {
  if (confirm(`确定要删除行程 ${trip.departure} → ${trip.destination} 吗？此操作不可恢复！`)) {
    // 这里可以实现删除行程的逻辑
    console.log(`删除行程`)
  }
}

// 保存行程
const saveTrip = () => {
  if (editingTrip.value) {
    // 编辑行程逻辑
    console.log('编辑行程:', tripForm.value)
  } else {
    // 创建行程逻辑
    console.log('创建行程:', tripForm.value)
  }
  closeModal()
  fetchTrips(currentPage.value)
}

// 关闭模态框
const closeModal = () => {
  showModal.value = false
  editingTrip.value = null
}

// 组件挂载时获取行程列表
onMounted(() => {
  fetchTrips(1)
})
</script>

<style scoped>
.trip-management {
  padding: 2rem;
}

.trip-management h1 {
  color: #333;
  margin-bottom: 2rem;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.search-box {
  display: flex;
  gap: 0.5rem;
}

.search-box input {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.search-box button,
.toolbar .btn-primary {
  padding: 0.5rem 1rem;
  background-color: #42b883;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.toolbar .btn-primary:hover,
.search-box button:hover {
  background-color: #359c6d;
}

.table-container {
  overflow-x: auto;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.5rem;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th,
.data-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.data-table th {
  background-color: #f8f9fa;
  font-weight: 600;
  color: #333;
}

.status {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
}

.status.open {
  background-color: #d4edda;
  color: #155724;
}

.status.closed {
  background-color: #f8d7da;
  color: #721c24;
}

.status.completed {
  background-color: #d1ecf1;
  color: #0c5460;
}

.btn-small {
  padding: 0.25rem 0.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
  margin-right: 0.25rem;
}

.btn-small:hover {
  opacity: 0.9;
}

.btn-primary {
  background-color: #42b883;
  color: white;
}

.btn-warning {
  background-color: #ffc107;
  color: #212529;
}

.btn-success {
  background-color: #28a745;
  color: white;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 1.5rem;
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

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-content h2 {
  margin-top: 0;
  color: #333;
}

.form-row {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.form-group {
  flex: 1;
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}

.btn-secondary {
  padding: 0.5rem 1rem;
  background-color: #6c757d;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

@media (max-width: 768px) {
  .toolbar {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-box {
    order: 2;
  }
  
  .toolbar .btn-primary {
    order: 1;
    width: fit-content;
    align-self: flex-end;
  }
  
  .form-row {
    flex-direction: column;
    gap: 0;
  }
  
  .data-table {
    font-size: 0.9rem;
  }
  
  .data-table th,
  .data-table td {
    padding: 0.5rem;
  }
  
  .modal-content {
    margin: 1rem;
    padding: 1rem;
  }
}
</style>