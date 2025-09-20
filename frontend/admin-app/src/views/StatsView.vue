<template>
  <div class="stats-view">
    <h1>数据统计与报表</h1>
    
    <div class="stats-cards">
      <div class="stat-card">
        <h3>总览</h3>
        <div class="stat-grid">
          <div class="stat-item">
            <span class="label">总用户数</span>
            <span class="value">{{ stats.overview?.total_users || 0 }}</span>
          </div>
          <div class="stat-item">
            <span class="label">总行程数</span>
            <span class="value">{{ stats.overview?.total_trips || 0 }}</span>
          </div>
          <div class="stat-item">
            <span class="label">总预订数</span>
            <span class="value">{{ stats.overview?.total_bookings || 0 }}</span>
          </div>
          <div class="stat-item">
            <span class="label">确认率</span>
            <span class="value">{{ stats.overview?.confirmation_rate || 0 }}%</span>
          </div>
          <div class="stat-item">
            <span class="label">取消率</span>
            <span class="value">{{ stats.overview?.cancellation_rate || 0 }}%</span>
          </div>
          <div class="stat-item">
            <span class="label">活跃用户</span>
            <span class="value">{{ stats.overview?.active_users || 0 }}</span>
          </div>
        </div>
      </div>
      
      <div class="stat-card">
        <h3>今日数据</h3>
        <div class="stat-grid">
          <div class="stat-item">
            <span class="label">新增用户</span>
            <span class="value">{{ stats.today?.users || 0 }}</span>
          </div>
          <div class="stat-item">
            <span class="label">新增行程</span>
            <span class="value">{{ stats.today?.trips || 0 }}</span>
          </div>
          <div class="stat-item">
            <span class="label">新增预订</span>
            <span class="value">{{ stats.today?.bookings || 0 }}</span>
          </div>
        </div>
      </div>
      
      <div class="stat-card">
        <h3>本周数据</h3>
        <div class="stat-grid">
          <div class="stat-item">
            <span class="label">新增用户</span>
            <span class="value">{{ stats.week?.users || 0 }}</span>
          </div>
          <div class="stat-item">
            <span class="label">新增行程</span>
            <span class="value">{{ stats.week?.trips || 0 }}</span>
          </div>
          <div class="stat-item">
            <span class="label">新增预订</span>
            <span class="value">{{ stats.week?.bookings || 0 }}</span>
          </div>
        </div>
      </div>
      
      <div class="stat-card">
        <h3>本月数据</h3>
        <div class="stat-grid">
          <div class="stat-item">
            <span class="label">新增用户</span>
            <span class="value">{{ stats.month?.users || 0 }}</span>
          </div>
          <div class="stat-item">
            <span class="label">新增行程</span>
            <span class="value">{{ stats.month?.trips || 0 }}</span>
          </div>
          <div class="stat-item">
            <span class="label">新增预订</span>
            <span class="value">{{ stats.month?.bookings || 0 }}</span>
          </div>
        </div>
      </div>
    </div>
    
    <div class="charts-container">
      <div class="chart-card">
        <h3>预订趋势</h3>
        <div ref="bookingChartRef" class="chart-container"></div>
      </div>
      <div class="chart-card">
        <h3>用户增长</h3>
        <div ref="userGrowthChartRef" class="chart-container"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { getAdminStats, getBookingTrends, getUserGrowth } from '../api/adminService'
import { useAdminStore } from '../stores/admin'
import * as echarts from 'echarts'

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

// 图表引用
const bookingChartRef = ref<HTMLElement | null>(null)
const userGrowthChartRef = ref<HTMLElement | null>(null)
let bookingChart: echarts.ECharts | null = null
let userGrowthChart: echarts.ECharts | null = null

// 获取统计数据
const fetchStats = async () => {
  try {
    const data = await getAdminStats()
    stats.value = data
  } catch (error) {
    console.error('获取统计数据失败:', error)
    alert('获取统计数据失败')
  }
}

// 获取预订趋势数据并绘制图表
const fetchBookingTrends = async () => {
  try {
    const data = await getBookingTrends(30)
    if (bookingChartRef.value) {
      // 初始化图表
      if (!bookingChart) {
        bookingChart = echarts.init(bookingChartRef.value)
      }
      
      // 配置图表选项
      const option = {
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: data.map((item: any) => item.date)
        },
        yAxis: {
          type: 'value',
          name: '预订数'
        },
        series: [{
          data: data.map((item: any) => item.bookings),
          type: 'line',
          smooth: true,
          itemStyle: {
            color: '#42b883'
          },
          areaStyle: {
            color: '#42b883',
            opacity: 0.3
          }
        }],
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        }
      }
      
      // 设置图表选项
      bookingChart.setOption(option, true)
    }
  } catch (error) {
    console.error('获取预订趋势数据失败:', error)
    alert('获取预订趋势数据失败')
  }
}

// 获取用户增长数据并绘制图表
const fetchUserGrowth = async () => {
  try {
    const data = await getUserGrowth(30)
    if (userGrowthChartRef.value) {
      // 初始化图表
      if (!userGrowthChart) {
        userGrowthChart = echarts.init(userGrowthChartRef.value)
      }
      
      // 配置图表选项
      const option = {
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: data.map((item: any) => item.date)
        },
        yAxis: {
          type: 'value',
          name: '用户数'
        },
        series: [{
          data: data.map((item: any) => item.users),
          type: 'line',
          smooth: true,
          itemStyle: {
            color: '#3498db'
          },
          areaStyle: {
            color: '#3498db',
            opacity: 0.3
          }
        }],
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        }
      }
      
      // 设置图表选项
      userGrowthChart.setOption(option, true)
    }
  } catch (error) {
    console.error('获取用户增长数据失败:', error)
    alert('获取用户增长数据失败')
  }
}

// 初始化所有图表
const initCharts = async () => {
  await nextTick()
  await fetchBookingTrends()
  await fetchUserGrowth()
}

// 窗口大小改变时重绘图表
const handleResize = () => {
  if (bookingChart) {
    bookingChart.resize()
  }
  if (userGrowthChart) {
    userGrowthChart.resize()
  }
}

// 组件挂载时获取数据
onMounted(() => {
  fetchStats()
  initCharts()
  
  // 添加窗口大小改变监听器
  window.addEventListener('resize', handleResize)
})

// 组件卸载时清理资源
onUnmounted(() => {
  // 移除窗口大小改变监听器
  window.removeEventListener('resize', handleResize)
  
  // 销毁图表实例
  if (bookingChart) {
    bookingChart.dispose()
    bookingChart = null
  }
  if (userGrowthChart) {
    userGrowthChart.dispose()
    userGrowthChart = null
  }
})
</script>

<style scoped>
.stats-view {
  padding: 2rem;
}

.stats-view h1 {
  color: #333;
  margin-bottom: 2rem;
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.stat-card h3 {
  margin: 0 0 1rem 0;
  color: #333;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.5rem;
}

.stat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 1rem;
}

.stat-item {
  display: flex;
  flex-direction: column;
}

.stat-item .label {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.25rem;
}

.stat-item .value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #42b883;
}

.charts-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.chart-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.chart-card h3 {
  margin: 0 0 1rem 0;
  color: #333;
}

.chart-container {
  height: 300px;
  width: 100%;
}

@media (max-width: 768px) {
  .stats-cards {
    grid-template-columns: 1fr;
  }
  
  .stat-grid {
    grid-template-columns: repeat(3, 1fr);
  }
  
  .charts-container {
    grid-template-columns: 1fr;
  }
  
  .chart-container {
    height: 200px;
  }
}
</style>