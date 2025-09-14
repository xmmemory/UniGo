<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

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
          <RouterLink to="/" @click="closeMenu">UniGo</RouterLink>
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
            <RouterLink to="/bookings" class="nav-link" @click="closeMenu">我的预订</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink to="/profile" class="nav-link" @click="closeMenu">个人中心</RouterLink>
          </li>
        </ul>
      </nav>
    </header>
    
    <main>
      <RouterView />
    </main>
    
    <footer>
      <p>&copy; 2025 UniGo 学生拼车平台. 保留所有权利.</p>
    </footer>
  </div>
</template>

<style scoped>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

header {
  background-color: #42b883;
  color: white;
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 1rem;
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
  max-width: 1200px;
  margin: 1rem auto;
  padding: 0 1rem;
  width: 100%;
}

footer {
  background-color: #f8f9fa;
  padding: 1rem 0;
  text-align: center;
  margin-top: auto;
  border-top: 1px solid #e9ecef;
  font-size: 0.9rem;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .navbar {
    padding: 0 1rem;
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
  
  main {
    margin: 1rem auto;
    padding: 0 0.5rem;
  }
  
  .nav-brand a {
    font-size: 1.3rem;
  }
}

@media (max-width: 480px) {
  .navbar {
    padding: 0 0.5rem;
  }
  
  main {
    padding: 0 0.25rem;
  }
  
  footer {
    font-size: 0.8rem;
    padding: 0.8rem 0;
  }
}
</style>