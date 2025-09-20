<template>
  <div class="admin-dashboard">
    <h1>管理员控制台</h1>
    
    <div class="dashboard-stats">
      <div class="stat-card">
        <h3>用户总数</h3>
        <p class="stat-value">{{ stats.total_users }}</p>
      </div>
      
      <div class="stat-card">
        <h3>行程总数</h3>
        <p class="stat-value">{{ stats.total_trips }}</p>
      </div>
      
      <div class="stat-card">
        <h3>预订总数</h3>
        <p class="stat-value">{{ stats.total_bookings }}</p>
      </div>
      
      <div class="stat-card">
        <h3>二手物品</h3>
        <p class="stat-value">{{ stats.total_secondhand_items }}</p>
      </div>
      
      <div class="stat-card">
        <h3>跑腿任务</h3>
        <p class="stat-value">{{ stats.total_errand_tasks }}</p>
      </div>
    </div>
    
    <div class="dashboard-charts">
      <div class="chart-section">
        <h2>用户增长趋势</h2>
        <div class="chart-placeholder">
          <p>用户增长图表</p>
        </div>
      </div>
      
      <div class="chart-section">
        <h2>交易统计</h2>
        <div class="chart-placeholder">
          <p>交易统计图表</p>
        </div>
      </div>
    </div>
    
    <div class="dashboard-actions">
      <button class="btn-primary" @click="refreshStats">刷新数据</button>
      <button class="btn-secondary" @click="logout">退出登录</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getAdminStats } from '../../api/adminStatsService'

const router = useRouter()

const stats = ref({
  total_users: 0,
  total_trips: 0,
  total_bookings: 0,
  total_secondhand_items: 0,
  total_errand_tasks: 0
})

// 获取管理员统计数据
const fetchStats = async () => {
  try {
    const response = await getAdminStats()
    stats.value = response
  } catch (error) {
    console.error('获取统计数据失败:', error)
    alert('获取统计数据失败')
  }
}

// 刷新统计数据
const refreshStats = () => {
  fetchStats()
}

// 退出登录
const logout = () => {
  if (confirm('确定要退出管理员登录吗？')) {
    // 清除管理员token
    localStorage.removeItem('admin_token')
    router.push('/admin/login')
  }
}

// 组件挂载时获取统计数据
onMounted(() => {
  fetchStats()
})
</script>

<style scoped>
.admin-dashboard {
  padding: 2rem;
}

.admin-dashboard h1 {
  color: #42b883;
  margin-bottom: 1.5rem;
}

.dashboard-stats {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.stat-card h3 {
  margin: 0 0 1rem 0;
  color: #666;
  font-size: 1rem;
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  color: #42b883;
  margin: 0;
}

.dashboard-charts {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.chart-section h2 {
  color: #42b883;
  margin-bottom: 1rem;
}

.chart-placeholder {
  height: 300px;
  background: #f8f9fa;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chart-placeholder p {
  color: #666;
  font-size: 1.2rem;
}

.dashboard-actions {
  display: flex;
  gap: 1rem;
}

.btn-primary, .btn-secondary {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-primary {
  background-color: #42b883;
  color: white;
}

.btn-primary:hover {
  background-color: #359c6d;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background-color: #545b62;
}

@media (max-width: 768px) {
  .dashboard-stats {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  }
  
  .dashboard-charts {
    grid-template-columns: 1fr;
  }
}
</style>