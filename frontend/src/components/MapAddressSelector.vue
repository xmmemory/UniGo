<template>
  <div class="map-address-selector">
    <div class="map-container">
      <div class="input-wrapper">
        <input
          type="text"
          :value="searchQuery"
          @input="handleInput"
          placeholder="请输入地址"
          class="address-input"
        >
        <button 
          v-if="searchQuery" 
          @click="clearInput" 
          class="clear-button"
          type="button"
        >
          ×
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';

// 定义props
const props = defineProps<{
  modelValue: string;
}>();

// 定义emits
const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void;
}>();

// 状态管理
const searchQuery = ref(props.modelValue);

// 监听modelValue变化
watch(() => props.modelValue, (newValue) => {
  searchQuery.value = newValue;
});

// 处理输入事件
const handleInput = (event: Event) => {
  const target = event.target as HTMLInputElement;
  searchQuery.value = target.value;
  emit('update:modelValue', target.value);
};

// 清除输入
const clearInput = () => {
  searchQuery.value = '';
  emit('update:modelValue', '');
};

// 获取当前位置
const getCurrentLocation = () => {
  // 模拟获取当前位置
  if (navigator.geolocation) {
    // 模拟定位成功
    setTimeout(() => {
      searchQuery.value = '北京市';
      emit('update:modelValue', '北京市');
    }, 500);
  } else {
    // 如果浏览器不支持地理位置，使用默认位置
    searchQuery.value = '北京市';
    emit('update:modelValue', '北京市');
  }
};

// 组件挂载时初始化
onMounted(() => {
  // 初始化逻辑可以在这里添加
});

// 暴露方法给父组件
defineExpose({
  getCurrentLocation
});
</script>

<style scoped>
.map-address-selector {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.map-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.address-input {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  padding-right: 2.5rem; /* 为清除按钮留出空间 */
}

.clear-button {
  position: absolute;
  right: 0.5rem;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #999;
  width: 1.5rem;
  height: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  padding: 0;
}

.clear-button:hover {
  background-color: #f0f0f0;
  color: #333;
}
</style>