<template>
  <div class="secondhand-management">
    <h1>二手交易管理</h1>
    
    <div class="toolbar">
      <div class="search-box">
        <input 
          type="text" 
          placeholder="搜索物品..." 
          v-model="searchQuery"
          @input="handleSearch"
        />
        <button @click="searchItems">搜索</button>
      </div>
      <button class="btn-primary" @click="showCreateItemModal">发布物品</button>
    </div>
    
    <div class="table-container">
      <table class="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>标题</th>
            <th>分类</th>
            <th>价格</th>
            <th>发布者</th>
            <th>发布时间</th>
            <th>状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item.id">
            <td>{{ item.id }}</td>
            <td>{{ item.title }}</td>
            <td>{{ item.category }}</td>
            <td>¥{{ item.price }}</td>
            <td>{{ item.owner_name }}</td>
            <td>{{ formatDate(item.created_at) }}</td>
            <td>
              <span :class="['status', getItemStatusClass(item.status)]">
                {{ getItemStatusText(item.status) }}
              </span>
            </td>
            <td>
              <button class="btn-small" @click="viewItem(item)">查看</button>
              <button class="btn-small" @click="editItem(item)">编辑</button>
              <button 
                :class="['btn-small', item.status === 'available' ? 'btn-warning' : 'btn-success']"
                @click="toggleItemStatus(item)"
              >
                {{ item.status === 'available' ? '下架' : '上架' }}
              </button>
              <button class="btn-small btn-danger" @click="deleteItem(item)">删除</button>
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
    
    <!-- 创建/编辑物品模态框 -->
    <div class="modal" v-if="showModal">
      <div class="modal-content">
        <h2>{{ editingItem ? '编辑物品' : '发布物品' }}</h2>
        <form @submit.prevent="saveItem">
          <div class="form-group">
            <label for="title">标题</label>
            <input 
              type="text" 
              id="title" 
              v-model="itemForm.title" 
              required 
            />
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="category">分类</label>
              <select id="category" v-model="itemForm.category" required>
                <option value="书籍">书籍</option>
                <option value="电子产品">电子产品</option>
                <option value="生活用品">生活用品</option>
                <option value="服装">服装</option>
                <option value="其他">其他</option>
              </select>
            </div>
            <div class="form-group">
              <label for="price">价格(元)</label>
              <input 
                type="number" 
                id="price" 
                v-model="itemForm.price" 
                min="0" 
                step="0.01" 
                required 
              />
            </div>
          </div>
          <div class="form-group">
            <label for="description">描述</label>
            <textarea 
              id="description" 
              v-model="itemForm.description" 
              rows="4"
              required
            ></textarea>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="status">状态</label>
              <select id="status" v-model="itemForm.status">
                <option value="available">在售</option>
                <option value="sold">已售</option>
                <option value="removed">已下架</option>
              </select>
            </div>
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
import { getAdminSecondHandItems } from '../api/adminService'
import { useAdminStore } from '../stores/admin'

const adminStore = useAdminStore()
const items = ref<any[]>([])
const loading = ref(false)
const currentPage = ref(1)
const totalPages = ref(1)
const totalItems = ref(0)
const searchQuery = ref('')
const showModal = ref(false)
const editingItem = ref(null)
const itemForm = ref({
  title: '',
  category: '书籍',
  price: 0,
  description: '',
  status: 'available'
})

// 获取二手物品列表
const fetchItems = async (page = 1) => {
  loading.value = true
  try {
    const response = await getAdminSecondHandItems((page - 1) * 10, 10)
    items.value = response
    totalItems.value = response.length
    totalPages.value = Math.ceil(totalItems.value / 10)
    currentPage.value = page
  } catch (error) {
    console.error('获取二手物品列表失败:', error)
    alert('获取二手物品列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索物品
const searchItems = () => {
  // 这里可以实现搜索逻辑
  console.log('搜索物品:', searchQuery.value)
  fetchItems(1)
}

// 处理搜索输入
const handleSearch = () => {
  // 可以实现防抖搜索
}

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN')
}

// 获取物品状态文本
const getItemStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    'available': '在售',
    'sold': '已售',
    'removed': '已下架'
  }
  return statusMap[status] || status
}

// 获取物品状态类名
const getItemStatusClass = (status: string) => {
  const classMap: Record<string, string> = {
    'available': 'available',
    'sold': 'sold',
    'removed': 'removed'
  }
  return classMap[status] || status
}

// 改变页面
const changePage = (page: number) => {
  fetchItems(page)
}

// 显示创建物品模态框
const showCreateItemModal = () => {
  editingItem.value = null
  itemForm.value = {
    title: '',
    category: '书籍',
    price: 0,
    description: '',
    status: 'available'
  }
  showModal.value = true
}

// 查看物品
const viewItem = (item: any) => {
  // 这里可以实现查看物品详情的逻辑
  console.log('查看物品:', item)
}

// 编辑物品
const editItem = (item: any) => {
  editingItem.value = item
  itemForm.value = {
    title: item.title,
    category: item.category,
    price: item.price,
    description: item.description,
    status: item.status
  }
  showModal.value = true
}

// 切换物品状态
const toggleItemStatus = (item: any) => {
  const newStatus = item.status === 'available' ? 'removed' : 'available'
  const action = item.status === 'available' ? '下架' : '上架'
  if (confirm(`确定要${action}物品 "${item.title}" 吗？`)) {
    // 这里可以实现切换物品状态的逻辑
    console.log(`切换物品状态为 ${newStatus}`)
  }
}

// 删除物品
const deleteItem = (item: any) => {
  if (confirm(`确定要删除物品 "${item.title}" 吗？此操作不可恢复！`)) {
    // 这里可以实现删除物品的逻辑
    console.log(`删除物品`)
  }
}

// 保存物品
const saveItem = () => {
  if (editingItem.value) {
    // 编辑物品逻辑
    console.log('编辑物品:', itemForm.value)
  } else {
    // 创建物品逻辑
    console.log('创建物品:', itemForm.value)
  }
  closeModal()
  fetchItems(currentPage.value)
}

// 关闭模态框
const closeModal = () => {
  showModal.value = false
  editingItem.value = null
}

// 组件挂载时获取物品列表
onMounted(() => {
  fetchItems(1)
})
</script>

<style scoped>
.secondhand-management {
  padding: 2rem;
}

.secondhand-management h1 {
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

.status.available {
  background-color: #d4edda;
  color: #155724;
}

.status.sold {
  background-color: #d1ecf1;
  color: #0c5460;
}

.status.removed {
  background-color: #f8d7da;
  color: #721c24;
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