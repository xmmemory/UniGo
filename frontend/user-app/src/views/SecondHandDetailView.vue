<template>
  <div class="secondhand-detail-container">
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="item" class="item-detail">
      <div class="item-header">
        <h1>{{ item.title }}</h1>
        <span class="item-category">{{ item.category }}</span>
      </div>
      
      <div class="item-content">
        <div class="item-gallery">
          <div class="main-image">
            <img
              v-if="item.image_url"
              :src="item.image_url"
              :alt="item.title"
            />
            <div v-else class="placeholder-image">📷</div>
          </div>
        </div>
        
        <div class="item-info">
          <div class="price-section">
            <span class="item-price">¥{{ item.price }}</span>
          </div>
          
          <div class="info-section">
            <h2>物品描述</h2>
            <p>{{ item.description || '暂无描述' }}</p>
          </div>
          
          <div class="info-section">
            <h2>卖家信息</h2>
            <div class="seller-info">
              <div class="seller-name">{{ item.owner_name }}</div>
              <div class="seller-contact">
                <button class="btn-contact" @click="contactSeller">联系卖家</button>
              </div>
            </div>
          </div>
          
          <div class="info-section">
            <h2>发布时间</h2>
            <p>{{ formatDateTime(item.created_at) }}</p>
          </div>
          
          <div class="actions" v-if="!isOwner">
            <button class="btn-purchase" @click="purchaseItem">购买</button>
          </div>
        </div>
      </div>
      
      <div class="actions">
        <button class="btn-back" @click="goBack">返回</button>
      </div>
    </div>
    <div v-else class="no-item">未找到物品信息</div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { getSecondHandItemDetail } from '../services/secondhandService'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const itemId = computed(() => parseInt(route.params.id as string))
const item = ref<any>(null)
const loading = ref(true)

// 是否为物品所有者
const isOwner = computed(() => {
  return item.value && authStore.user && item.value.owner_id === authStore.user.id
})

// 获取物品详情
const fetchItemDetail = async () => {
  try {
    const response = await getSecondHandItemDetail(itemId.value)
    item.value = response
  } catch (error) {
    console.error('获取物品详情失败:', error)
    alert('获取物品详情失败')
  } finally {
    loading.value = false
  }
}

// 联系卖家
const contactSeller = () => {
  if (!authStore.isAuthenticated) {
    alert('请先登录')
    router.push('/login')
    return
  }
  
  alert('联系卖家功能待实现')
  // 这里可以实现联系卖家的功能，比如打开聊天窗口
}

// 购买物品
const purchaseItem = () => {
  if (!authStore.isAuthenticated) {
    alert('请先登录')
    router.push('/login')
    return
  }
  
  alert('购买功能待实现')
  // 这里可以实现购买功能
}

// 返回上一页
const goBack = () => {
  router.back()
}

// 格式化日期时间
const formatDateTime = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

// 组件挂载时获取物品详情
onMounted(() => {
  fetchItemDetail()
})
</script>

<style scoped>
.secondhand-detail-container {
  padding: 2rem;
  max-width: 1000px;
  margin: 0 auto;
}

.loading, .no-item {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.item-detail {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.item-header {
  padding: 1.5rem;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.item-header h1 {
  margin: 0;
  color: #333;
}

.item-category {
  background-color: #e9ecef;
  color: #495057;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.9rem;
}

.item-content {
  display: flex;
  flex-wrap: wrap;
  padding: 1.5rem;
}

.item-gallery {
  flex: 1;
  min-width: 300px;
  margin-right: 2rem;
}

.main-image {
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8f9fa;
  border-radius: 8px;
  overflow: hidden;
}

.main-image img {
  max-width: 100%;
  max-height: 100%;
  object-fit: cover;
}

.placeholder-image {
  font-size: 5rem;
  color: #ccc;
}

.item-info {
  flex: 1;
  min-width: 300px;
}

.price-section {
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
}

.item-price {
  font-size: 2rem;
  font-weight: bold;
  color: #42b883;
}

.info-section {
  margin-bottom: 2rem;
}

.info-section h2 {
  color: #42b883;
  margin-bottom: 1rem;
}

.info-section p {
  color: #333;
  line-height: 1.6;
}

.seller-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.seller-name {
  font-size: 1.1rem;
  font-weight: 500;
}

.btn-contact {
  padding: 0.5rem 1rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-contact:hover {
  background-color: #0056b3;
}

.actions {
  padding: 1.5rem;
  text-align: center;
  border-top: 1px solid #eee;
}

.btn-purchase, .btn-back {
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
  margin: 0 0.5rem;
}

.btn-purchase {
  background-color: #42b883;
  color: white;
}

.btn-purchase:hover {
  background-color: #359c6d;
}

.btn-back {
  background-color: #6c757d;
  color: white;
}

.btn-back:hover {
  background-color: #545b62;
}

@media (max-width: 768px) {
  .item-content {
    flex-direction: column;
  }
  
  .item-gallery {
    margin-right: 0;
    margin-bottom: 2rem;
  }
}
</style>