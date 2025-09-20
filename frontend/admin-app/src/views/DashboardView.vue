<template>
  <div class="dashboard">
    <h1>管理员仪表盘</h1>
    <div class="stats-grid">
      <div class="stat-card">
        <h3>总用户数</h3>
        <p class="stat-value">{{ stats.overview?.total_users || 0 }}</p>
      </div>
      <div class="stat-card">
        <h3>总行程数</h3>
        <p class="stat-value">{{ stats.overview?.total_trips || 0 }}</p>
      </div>
      <div class="stat-card">
        <h3>总预订数</h3>
        <p class="stat-value">{{ stats.overview?.total_bookings || 0 }}</p>
      </div>
      <div class="stat-card">
        <h3>确认率</h3>
        <p class="stat-value">{{ stats.overview?.confirmation_rate || 0 }}%</p>
      </div>
    </div>
    
    <!-- 移除了预订趋势和用户增长图表部分 -->
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getAdminStats } from '../api/adminService'
import { useAdminStore } from '../stores/admin'

const adminStore = useAdminStore()
const stats = ref({
  overview: {
    total_users: 0,
    total_trips: 0,
    total_bookings: 0,
    confirmation_rate: 0,
    cancellation_rate: 0,
    active_users: 0
  },
  today: {
    users: 0,
    trips: 0,
    bookings: 0
  },
  week: {
    users: 0,
    trips: 0,
    bookings: 0
  },
  month: {
    users: 0,
    trips: 0,
    bookings: 0
  }
})

const fetchStats = async () => {
  try {
    const data = await getAdminStats()
    stats.value = data
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

onMounted(() => {
  fetchStats()
})
</script>

<style scoped>
.dashboard {
  padding: 2rem;
  width: 100%;
  max-width: 100%;
  margin: 0 auto;
  box-sizing: border-box;
}

.dashboard h1 {
  color: #333;
  margin-bottom: 2rem;
  font-size: 2.5rem;
  text-align: center;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2rem;
  margin-bottom: 3rem;
  width: 100%;
  box-sizing: border-box;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  width: 100%;
  box-sizing: border-box;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.stat-card h3 {
  margin: 0 0 1.5rem 0;
  color: #666;
  font-size: 1.2rem;
  font-weight: 600;
}

.stat-value {
  font-size: 3rem;
  font-weight: bold;
  color: #42b883;
  margin: 0;
  line-height: 1;
}

/* 宽屏PC适配 */
@media (min-width: 1200px) {
  .dashboard {
    padding: 3rem;
    max-width: 1600px;
  }
  
  .dashboard h1 {
    font-size: 2.8rem;
    margin-bottom: 3rem;
  }
  
  .stats-grid {
    gap: 2.5rem;
    margin-bottom: 3rem;
  }
  
  .stat-card {
    padding: 2.5rem;
  }
  
  .stat-card h3 {
    font-size: 1.3rem;
    margin-bottom: 2rem;
  }
  
  .stat-value {
    font-size: 3.5rem;
  }
}

/* 大宽屏PC适配 */
@media (min-width: 1600px) {
  .dashboard {
    padding: 4rem;
    max-width: 1800px;
  }
  
  .dashboard h1 {
    font-size: 3rem;
    margin-bottom: 4rem;
  }
  
  .stats-grid {
    gap: 3rem;
    margin-bottom: 4rem;
  }
  
  .stat-card {
    padding: 3rem;
  }
  
  .stat-card h3 {
    font-size: 1.5rem;
    margin-bottom: 2.5rem;
  }
  
  .stat-value {
    font-size: 4rem;
  }
}

/* 超宽屏PC适配 */
@media (min-width: 2000px) {
  .dashboard {
    padding: 5rem;
    max-width: 2000px;
  }
  
  .dashboard h1 {
    font-size: 3.5rem;
    margin-bottom: 5rem;
  }
  
  .stats-grid {
    gap: 4rem;
    margin-bottom: 5rem;
  }
  
  .stat-card {
    padding: 4rem;
  }
  
  .stat-card h3 {
    font-size: 1.8rem;
    margin-bottom: 3rem;
  }
  
  .stat-value {
    font-size: 5rem;
  }
}
</style>