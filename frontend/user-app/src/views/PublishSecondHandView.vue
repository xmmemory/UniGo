<template>
  <div class="publish-secondhand-container">
    <h1>发布二手物品</h1>
    
    <form @submit.prevent="publishItem" class="publish-form">
      <div class="form-section">
        <h2>物品信息</h2>
        
        <div class="form-group">
          <label for="title">物品名称 *</label>
          <input
            id="title"
            v-model="itemForm.title"
            type="text"
            placeholder="请输入物品名称"
            required
          />
        </div>
        
        <div class="form-group">
          <label for="category">分类 *</label>
          <select
            id="category"
            v-model="itemForm.category"
            required
          >
            <option value="">请选择分类</option>
            <option value="书籍">书籍</option>
            <option value="电子产品">电子产品</option>
            <option value="生活用品">生活用品</option>
            <option value="服装">服装</option>
            <option value="其他">其他</option>
          </select>
        </div>
        
        <div class="form-group">
          <label for="price">价格 (¥) *</label>
          <input
            id="price"
            v-model.number="itemForm.price"
            type="number"
            min="0"
            step="0.01"
            placeholder="请输入价格"
            required
          />
        </div>
        
        <div class="form-group">
          <label for="description">物品描述 *</label>
          <textarea
            id="description"
            v-model="itemForm.description"
            rows="4"
            placeholder="请输入物品描述"
            required
          ></textarea>
        </div>
      </div>
      
      <div class="form-section">
        <h2>物品图片</h2>
        
        <div class="form-group">
          <label for="image">上传图片</label>
          <input
            id="image"
            type="file"
            accept="image/*"
            @change="handleImageUpload"
          />
          <div v-if="itemForm.imagePreview" class="image-preview">
            <img :src="itemForm.imagePreview" alt="预览图片" />
          </div>
        </div>
      </div>
      
      <div class="form-actions">
        <button type="submit" class="btn-publish" :disabled="publishing">
          {{ publishing ? '发布中...' : '发布物品' }}
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
import { createSecondHandItem } from '../services/secondhandService'

const router = useRouter()
const authStore = useAuthStore()

const publishing = ref(false)

const itemForm = reactive({
  title: '',
  category: '',
  price: 0,
  description: '',
  image: null as File | null,
  imagePreview: ''
})

// 处理图片上传
const handleImageUpload = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  
  if (file) {
    itemForm.image = file
    // 生成预览图片
    const reader = new FileReader()
    reader.onload = (e) => {
      itemForm.imagePreview = e.target?.result as string
    }
    reader.readAsDataURL(file)
  }
}

// 发布物品
const publishItem = async () => {
  if (!authStore.isAuthenticated) {
    alert('请先登录')
    router.push('/login')
    return
  }
  
  // 基本验证
  if (!itemForm.title) {
    alert('请输入物品名称')
    return
  }
  
  if (!itemForm.category) {
    alert('请选择分类')
    return
  }
  
  if (itemForm.price <= 0) {
    alert('请输入有效价格')
    return
  }
  
  if (!itemForm.description) {
    alert('请输入物品描述')
    return
  }
  
  publishing.value = true
  try {
    const formData = new FormData()
    formData.append('title', itemForm.title)
    formData.append('category', itemForm.category)
    formData.append('price', itemForm.price.toString())
    formData.append('description', itemForm.description)
    
    if (itemForm.image) {
      formData.append('image', itemForm.image)
    }
    
    await createSecondHandItem(formData)
    
    alert('物品发布成功！')
    router.push('/secondhand')
  } catch (error: any) {
    alert(error.message || '发布物品失败')
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
.publish-secondhand-container {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.publish-secondhand-container h1 {
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

.form-group input[type="file"] {
  padding: 0.5rem;
}

.image-preview {
  margin-top: 1rem;
}

.image-preview img {
  max-width: 200px;
  max-height: 200px;
  object-fit: cover;
  border-radius: 4px;
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
  .publish-secondhand-container {
    padding: 1rem;
  }
  
  .publish-form {
    padding: 1rem;
  }
}
</style>