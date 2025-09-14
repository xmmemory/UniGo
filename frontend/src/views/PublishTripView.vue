<template>
  <div class="publish-trip">
    <div class="publish-trip-header">
      <h1>发布行程</h1>
      <router-link to="/trips" class="btn btn-secondary">返回搜索</router-link>
    </div>

    <div class="publish-trip-content">
      <form @submit.prevent="createNewTrip" class="publish-trip-form">
        <div class="form-group">
          <label for="departure">出发地</label>
          <input 
            type="text" 
            id="departure" 
            v-model="newTrip.departure" 
            required 
            placeholder="请输入出发地"
          >
        </div>
        <div class="form-group">
          <label for="destination">目的地</label>
          <input 
            type="text" 
            id="destination" 
            v-model="newTrip.destination" 
            required 
            placeholder="请输入目的地"
          >
        </div>
        <div class="form-group">
          <label for="departureTime">出发时间</label>
          <input type="datetime-local" id="departureTime" v-model="newTrip.departure_time" required>
        </div>
        <div class="form-group">
          <label for="price">每人价格 (¥)</label>
          <input type="number" id="price" v-model="newTrip.price_per_person" required min="0" step="0.01">
        </div>
        <div class="form-group">
          <label for="seats">座位数量</label>
          <input type="number" id="seats" v-model="newTrip.available_seats" required min="1">
        </div>
        <button type="submit" class="btn btn-primary">发布行程</button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { createTrip } from '@/api/tripService'

// 状态管理
const newTrip = ref({
  departure: '',
  destination: '',
  departure_time: '',
  price_per_person: 0,
  available_seats: 1
})

const router = useRouter()

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
    // 重置表单
    newTrip.value = {
      departure: '',
      destination: '',
      departure_time: '',
      price_per_person: 0,
      available_seats: 1
    }
    // 跳转到行程搜索页面
    router.push('/trips')
  } catch (error) {
    console.error('创建行程失败:', error)
    alert('创建行程失败，请稍后重试')
  }
}
</script>

<style scoped>
.publish-trip {
  padding: 1rem 0;
}

.publish-trip-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.publish-trip-header h1 {
  margin: 0;
  font-size: 1.5rem;
}

.publish-trip-content {
  max-width: 600px;
  margin: 0 auto;
}

.publish-trip-form {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
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
  display: inline-block;
  text-align: center;
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
  .publish-trip {
    padding: 2rem 0;
  }
  
  .publish-trip-header h1 {
    font-size: 2rem;
  }
  
  .publish-trip-content {
    padding: 0 1rem;
  }
  
  .publish-trip-form {
    padding: 2rem;
  }
  
  .btn {
    width: auto;
    padding: 0.8rem 1.5rem;
  }
}
</style>