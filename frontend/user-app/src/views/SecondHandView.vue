<template>
  <div class="secondhand-container">
    <h1>二手交易</h1>
    
    <div class="search-filters">
      <div class="filter-group">
        <label for="keyword">关键词</label>
        <input
          id="keyword"
          v-model="searchFilters.keyword"
          type="text"
          placeholder="请输入商品名称或描述"
        />
      </div>
      
      <div class="filter-group">
        <label for="category">分类</label>
        <select
          id="category"
          v-model="searchFilters.category"
        >
          <option value="">全部分类</option>
          <option value="书籍">书籍</option>
          <option value="电子产品">电子产品</option>
          <option value="生活用品">生活用品</option>
          <option value="服装">服装</option>
          <option value="其他">其他</option>
        </select>
      </div>
      
      <div class="filter-group">
        <label for="priceRange">价格范围</label>
        <select
          id="priceRange"
          v-model="searchFilters.priceRange"
        >
          <option value="">不限</option>
          <option value="0-50">0-50元</option>
          <option value="50-100">50-100元</option>
          <option value="100-200">100-200元</option>
          <option value="200-500">200-500元</option>
          <option value="500+">500元以上</option>
        </select>
      </div>
      
      <button class="btn-search" @click="searchItems">搜索</button>
    </div>
    
    <div class="items-list">
      <div v-if="loading" class="loading">加载中...</div>
      <div v-else-if="items.length === 0" class="no-items">暂无二手物品信息</div>
      <div v-else class="item-cards">
        <div
          v-for="item in items"
          :key="item.id"
          class="item-card"
          @click="viewItemDetail(item.id)"
        >
          <div class="item-image">
            <img
              v-if="item.image_url"
              :src="item.image_url"
              :alt="item.title"
            />
            <div v-else class="placeholder-image">📷</div>
          </div>
          
          <div class="item-info">
            <h3>{{ item.title }}</h3>
            <p class="item-description">{{ item.description }}</p>
            <div class="item-meta">
              <span class="item-price">¥{{ item.price }}</span>
              <span class="item-category">{{ item.category }}</span>
            </div>
            <div class="item-owner">
              <span>{{ item.owner_name }}</span>
              <span>{{ formatDate(item.created_at) }}</span>
            </div>
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
      <router-link to="/publish-secondhand" class="btn-primary">发布物品</router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getSecondHandItems } from '../services/secondhandService'

const router = useRouter()

// 搜索过滤器
const searchFilters = reactive({
  keyword: '',
  category: '',
  priceRange: ''
})

// 物品数据
const items = ref<any[]>([])
const loading = ref(false)
const currentPage = ref(1)
const totalPages = ref(1)
const totalItems = ref(0)

// 获取二手物品列表
const fetchItems = async (page = 1) => {
  loading.value = true
  try {
    const response = await getSecondHandItems({
      page,
      limit: 10, // 每页显示10条数据
      keyword: searchFilters.keyword,
      category: searchFilters.category,
      price_range: searchFilters.priceRange
    })
    
    // 正确处理后端返回的数据格式
    items.value = response.items || []
    totalItems.value = response.total || 0
    currentPage.value = response.page || page
    totalPages.value = response.total_pages || 1
  } catch (error) {
    console.error('获取二手物品失败:', error)
    alert('获取二手物品失败')
  } finally {
    loading.value = false
  }
}

// 搜索物品
const searchItems = () => {
  currentPage.value = 1
  fetchItems(1)
}

// 查看物品详情
const viewItemDetail = (itemId: number) => {
  router.push(`/secondhand/${itemId}`)
}

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN')
}

// 切换页面
const changePage = (page: number) => {
  if (page >= 1 && page <= totalPages.value) {
    fetchItems(page)
  }
}

// 组件挂载时获取物品列表
onMounted(() => {
  fetchItems()
})
</script>

<style scoped>
.secondhand-container {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.secondhand-container h1 {
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
}

.filter-group {
  flex: 1;
  min-width: 200px;
}

.filter-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.filter-group input,
.filter-group select {
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
}

.items-list {
  margin-bottom: 2rem;
}

.loading, .no-items {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.item-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
}

.item-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: box-shadow 0.3s;
}

.item-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.item-image {
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8f9fa;
}

.item-image img {
  max-width: 100%;
  max-height: 100%;
  object-fit: cover;
}

.placeholder-image {
  font-size: 3rem;
  color: #ccc;
}

.item-info {
  padding: 1rem;
}

.item-info h3 {
  margin: 0 0 0.5rem 0;
  color: #333;
}

.item-description {
  margin: 0.5rem 0;
  color: #666;
  font-size: 0.9rem;
  line-height: 1.4;
}

.item-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 0.5rem 0;
}

.item-price {
  font-size: 1.2rem;
  font-weight: bold;
  color: #42b883;
}

.item-category {
  background-color: #e9ecef;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
}

.item-owner {
  display: flex;
  justify-content: space-between;
  margin-top: 0.5rem;
  padding-top: 0.5rem;
  border-top: 1px solid #eee;
  font-size: 0.8rem;
  color: #666;
}

.actions {
  text-align: center;
}

.btn-primary {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background-color: #42b883;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  transition: background-color 0.3s;
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

/* 移动端适配 */
@media (max-width: 767.98px) {
  .secondhand-container {
    padding: 1rem;
  }
  
  .search-filters {
    padding: 0.75rem;
    gap: 0.75rem;
  }
  
  .filter-group {
    min-width: 100%;
  }
  
  .item-cards {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
  
  .item-image {
    height: 150px;
  }
  
  .item-info {
    padding: 0.75rem;
  }
  
  .item-info h3 {
    font-size: 1.1rem;
  }
  
  .item-description {
    font-size: 0.85rem;
  }
  
  .item-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
  }
  
  .item-price {
    font-size: 1.1rem;
  }
  
  .item-owner {
    flex-direction: column;
    gap: 0.25rem;
    align-items: flex-start;
  }
  
  .btn-search {
    width: 100%;
    padding: 0.75rem;
  }
  
  .pagination {
    gap: 0.5rem;
    font-size: 0.9rem;
  }
  
  .pagination button {
    padding: 0.4rem 0.8rem;
  }
}

@media (max-width: 480px) {
  .secondhand-container {
    padding: 0.5rem;
  }
  
  .search-filters {
    padding: 0.5rem;
    gap: 0.5rem;
  }
  
  .item-cards {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.75rem;
  }
  
  .filter-group label {
    font-size: 0.9rem;
  }
  
  .filter-group input,
  .filter-group select {
    padding: 0.4rem;
    font-size: 0.9rem;
  }
  
  .item-image {
    height: 120px;
  }
  
  .item-info {
    padding: 0.5rem;
  }
  
  .item-info h3 {
    font-size: 1rem;
  }
  
  .item-description {
    font-size: 0.8rem;
  }
  
  .item-price {
    font-size: 1rem;
  }
  
  .item-category {
    font-size: 0.7rem;
    padding: 0.2rem 0.4rem;
  }
  
  .item-owner {
    font-size: 0.75rem;
  }
  
  .actions {
    padding: 0 0.5rem;
  }
  
  .btn-primary {
    padding: 0.6rem 1rem;
    font-size: 0.9rem;
  }
  
  .pagination {
    font-size: 0.85rem;
  }
  
  .pagination button {
    padding: 0.3rem 0.6rem;
    font-size: 0.85rem;
  }
}
</style>