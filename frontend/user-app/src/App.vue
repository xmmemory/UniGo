<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { ref, onMounted } from 'vue'
import { useAuthStore } from './stores/auth'

// 初始化认证存储
const authStore = useAuthStore()

// 移动端菜单控制
const isMenuOpen = ref(false)

// 切换菜单
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

// 关闭菜单
const closeMenu = () => {
  isMenuOpen.value = false
}

// 在应用启动时初始化认证状态
onMounted(() => {
  authStore.initializeAuth()
})
</script>

<template>
  <div id="app">
    <header>
      <nav class="navbar">
        <div class="nav-brand">
          <RouterLink to="/" @click="closeMenu">CampusGo</RouterLink>
        </div>
        
        <!-- 移动端菜单按钮 -->
        <div class="menu-toggle" @click="toggleMenu">
          <span></span>
          <span></span>
          <span></span>
        </div>
        
        <!-- 导航菜单 -->
        <ul class="nav-menu" :class="{ 'mobile-menu': isMenuOpen }">
          <li class="nav-item">
            <RouterLink to="/" class="nav-link" @click="closeMenu">首页</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink to="/trips" class="nav-link" @click="closeMenu">行程</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink to="/secondhand" class="nav-link" @click="closeMenu">二手交易</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink to="/errands" class="nav-link" @click="closeMenu">跑腿服务</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink to="/profile" class="nav-link" @click="closeMenu">个人中心</RouterLink>
          </li>
        </ul>
      </nav>
    </header>
    
    <main class="main-container">
      <RouterView />
    </main>
    
    <footer>
      <p>&copy; 2025 CampusGo 校园生活平台. 保留所有权利.</p>
    </footer>
  </div>
</template>

<style scoped>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  width: 100%;
}

header {
  background-color: #42b883;
  color: white;
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  position: sticky;
  top: 0;
  z-index: 100;
  width: 100%;
}

.navbar {
  width: 100%;
  max-width: 100%;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 1rem;
  box-sizing: border-box;
}

.nav-brand a {
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
  text-decoration: none;
}

/* 移动端菜单按钮 */
.menu-toggle {
  display: none;
  flex-direction: column;
  cursor: pointer;
}

.menu-toggle span {
  width: 25px;
  height: 3px;
  background-color: white;
  margin: 3px 0;
  transition: 0.3s;
}

.nav-menu {
  display: flex;
  list-style: none;
}

.nav-item {
  margin: 0 0.5rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  font-weight: 500;
  transition: opacity 0.3s;
  padding: 0.5rem;
  border-radius: 4px;
}

.nav-link:hover {
  opacity: 0.8;
  background-color: rgba(255, 255, 255, 0.1);
}

.nav-link.router-link-exact-active {
  background-color: rgba(255, 255, 255, 0.2);
}

main {
  flex: 1;
  width: 100%;
}

.main-container {
  width: 100%;
  max-width: 100%;
  margin: 1rem auto;
  padding: 0 1rem;
  box-sizing: border-box;
}

footer {
  background-color: #f8f9fa;
  padding: 1rem 0;
  text-align: center;
  margin-top: auto;
  border-top: 1px solid #e9ecef;
  font-size: 0.9rem;
  width: 100%;
}

/* 响应式断点优化 */
/* 超小屏幕 (手机, 小于576px) */
@media (max-width: 575.98px) {
  .navbar {
    padding: 0 0.5rem;
  }
  
  .menu-toggle {
    display: flex;
  }
  
  .nav-menu {
    position: fixed;
    left: -100%;
    top: 70px;
    flex-direction: column;
    background-color: #42b883;
    width: 100%;
    text-align: center;
    transition: 0.3s;
    box-shadow: 0 10px 27px rgba(0,0,0,0.05);
    padding: 2rem 0;
  }
  
  .nav-menu.mobile-menu {
    left: 0;
  }
  
  .nav-item {
    margin: 0.5rem 0;
  }
  
  .nav-link {
    padding: 1rem;
    display: block;
    font-size: 1.1rem;
  }
  
  .main-container {
    margin: 0.5rem auto;
    padding: 0 0.5rem;
  }
  
  .nav-brand a {
    font-size: 1.3rem;
  }
  
  footer {
    font-size: 0.85rem;
    padding: 0.8rem 0;
  }
}

/* 小屏幕 (手机横屏, 576px及以上) */
@media (min-width: 576px) {
  .navbar {
    padding: 0 1rem;
  }
  
  .main-container {
    margin: 1rem auto;
    padding: 0 1rem;
  }
}

/* 中等屏幕 (平板, 768px及以上) */
@media (min-width: 768px) {
  .navbar {
    padding: 0 1.5rem;
  }
  
  .main-container {
    margin: 1.5rem auto;
    padding: 0 1.5rem;
  }
  
  .nav-brand a {
    font-size: 1.6rem;
  }
}

/* 大屏幕 (桌面, 992px及以上) */
@media (min-width: 992px) {
  .navbar {
    padding: 0 2rem;
  }
  
  .main-container {
    margin: 2rem auto;
    padding: 0 2rem;
  }
}

/* 超大屏幕 (大桌面, 1200px及以上) */
@media (min-width: 1200px) {
  .navbar {
    padding: 0 2.5rem;
  }
  
  .main-container {
    margin: 2.5rem auto;
    padding: 0 2.5rem;
    max-width: 1400px;
  }
  
  .nav-brand a {
    font-size: 1.8rem;
  }
}

/* 超宽屏 (1600px及以上) */
@media (min-width: 1600px) {
  .navbar {
    padding: 0 3rem;
  }
  
  .main-container {
    margin: 3rem auto;
    padding: 0 3rem;
    max-width: 1600px;
  }
}

/* 超宽屏 (2000px及以上) */
@media (min-width: 2000px) {
  .navbar {
    padding: 0 4rem;
  }
  
  .main-container {
    margin: 4rem auto;
    padding: 0 4rem;
    max-width: 1800px;
  }
  
  .nav-brand a {
    font-size: 2rem;
  }
}
</style>