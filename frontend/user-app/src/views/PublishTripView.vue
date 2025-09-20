<template>
  <div class="publish-trip-container">
    <h1>发布行程</h1>
    
    <form @submit.prevent="publishTrip" class="publish-form">
      <div class="form-section">
        <h2>行程信息</h2>
        
        <div class="form-group">
          <label for="departure">出发地 *</label>
          <input
            id="departure"
            v-model="tripForm.departure"
            type="text"
            placeholder="请输入出发地"
            required
          />
        </div>
        
        <div class="form-group">
          <label for="destination">目的地 *</label>
          <input
            id="destination"
            v-model="tripForm.destination"
            type="text"
            placeholder="请输入目的地"
            required
          />
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="departureTime">出发时间 *</label>
            <input
              id="departureTime"
              v-model="tripForm.departureTime"
              type="datetime-local"
              required
            />
          </div>
          
          <div class="form-group">
            <label for="availableSeats">空位数量 *</label>
            <input
              id="availableSeats"
              v-model.number="tripForm.availableSeats"
              type="number"
              min="1"
              max="4"
              required
            />
          </div>
        </div>
        
        <div class="form-group">
          <label for="price">费用 (¥) *</label>
          <input
            id="price"
            v-model.number="tripForm.price"
            type="number"
            min="0"
            step="0.01"
            placeholder="请输入费用"
            required
          />
        </div>
      </div>
      
      <div class="form-section">
        <h2>车辆信息</h2>
        
        <div class="form-group">
          <label for="vehicleType">车型 *</label>
          <select
            id="vehicleType"
            v-model="tripForm.vehicleType"
            required
          >
            <option value="">请选择车型</option>
            <option value="轿车">轿车</option>
            <option value="SUV">SUV</option>
            <option value="MPV">MPV</option>
            <option value="面包车">面包车</option>
          </select>
        </div>
        
        <div class="form-group">
          <label for="licensePlate">车牌号 *</label>
          <input
            id="licensePlate"
            v-model="tripForm.licensePlate"
            type="text"
            placeholder="请输入车牌号"
            required
          />
        </div>
      </div>
      
      <div class="form-section">
        <h2>联系方式</h2>
        
        <div class="form-group">
          <label for="driverPhone">联系电话 *</label>
          <input
            id="driverPhone"
            v-model="tripForm.driverPhone"
            type="tel"
            placeholder="请输入联系电话"
            required
          />
        </div>
      </div>
      
      <div class="form-section">
        <h2>行程描述</h2>
        
        <div class="form-group">
          <label for="description">行程描述</label>
          <textarea
            id="description"
            v-model="tripForm.description"
            rows="4"
            placeholder="请输入行程描述（可选）"
          ></textarea>
        </div>
      </div>
      
      <div class="form-actions">
        <button type="submit" class="btn-publish" :disabled="publishing">
          {{ publishing ? '发布中...' : '发布行程' }}
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
import { createTrip } from '../api/tripService'

const router = useRouter()
const authStore = useAuthStore()

const publishing = ref(false)

const tripForm = reactive({
  departure: '',
  destination: '',
  departureTime: '',
  availableSeats: 1,
  price: 0,
  vehicleType: '',
  licensePlate: '',
  driverPhone: '',
  description: ''
})

const publishTrip = async () => {
  if (!authStore.isAuthenticated) {
    alert('请先登录')
    router.push('/login')
    return
  }
  
  // 基本验证
  if (!tripForm.departure || !tripForm.destination) {
    alert('请填写出发地和目的地')
    return
  }
  
  if (!tripForm.departureTime) {
    alert('请选择出发时间')
    return
  }
  
  if (tripForm.availableSeats < 1 || tripForm.availableSeats > 4) {
    alert('空位数量必须在1-4之间')
    return
  }
  
  if (tripForm.price < 0) {
    alert('费用不能为负数')
    return
  }
  
  if (!tripForm.vehicleType) {
    alert('请选择车型')
    return
  }
  
  if (!tripForm.licensePlate) {
    alert('请输入车牌号')
    return
  }
  
  if (!tripForm.driverPhone) {
    alert('请输入联系电话')
    return
  }
  
  publishing.value = true
  try {
    await createTrip({
      departure: tripForm.departure,
      destination: tripForm.destination,
      departure_time: tripForm.departureTime,
      available_seats: tripForm.availableSeats,
      price: tripForm.price,
      vehicle_type: tripForm.vehicleType,
      license_plate: tripForm.licensePlate,
      driver_phone: tripForm.driverPhone,
      description: tripForm.description
    })
    
    alert('行程发布成功！')
    router.push('/trips')
  } catch (error: any) {
    alert(error.message || '发布行程失败')
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
.publish-trip-container {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.publish-trip-container h1 {
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
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  box-sizing: border-box;
}

.form-group input:focus,
.form-group select:focus,
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
  .publish-trip-container {
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