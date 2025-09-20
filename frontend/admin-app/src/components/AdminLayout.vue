<template>
  <div class="admin-layout">
    <!-- 侧边栏 -->
    <aside class="sidebar" :class="{ 'sidebar-collapsed': isSidebarCollapsed }">
      <div class="sidebar-header">
        <h2 v-if="!isSidebarCollapsed">CampusGo 管理后台</h2>
        <h2 v-else>CG</h2>
      </div>
      <nav class="sidebar-nav">
        <ul>
          <li>
            <router-link to="/admin/dashboard" class="nav-link" active-class="active">
              <span class="icon">📊</span>
              <span v-if="!isSidebarCollapsed">仪表盘</span>
            </router-link>
          </li>
          <li>
            <router-link to="/admin/users" class="nav-link" active-class="active">
              <span class="icon">👥</span>
              <span v-if="!isSidebarCollapsed">用户管理</span>
            </router-link>
          </li>
          <li>
            <router-link to="/admin/trips" class="nav-link" active-class="active">
              <span class="icon">🚗</span>
              <span v-if="!isSidebarCollapsed">拼车管理</span>
            </router-link>
          </li>
          <li>
            <router-link to="/admin/secondhand" class="nav-link" active-class="active">
              <span class="icon">🛍️</span>
              <span v-if="!isSidebarCollapsed">二手交易</span>
            </router-link>
          </li>
          <li>
            <router-link to="/admin/errands" class="nav-link" active-class="active">
              <span class="icon">📦</span>
              <span v-if="!isSidebarCollapsed">跑腿服务</span>
            </router-link>
          </li>
          <li>
            <router-link to="/admin/stats" class="nav-link" active-class="active">
              <span class="icon">📈</span>
              <span v-if="!isSidebarCollapsed">数据统计</span>
            </router-link>
          </li>
        </ul>
      </nav>
    </aside>

    <!-- 主内容区域 -->
    <div class="main-content">
      <!-- 顶部导航栏 -->
      <header class="topbar">
        <div class="topbar-left">
          <button class="menu-toggle" @click="toggleSidebar">
            <span>☰</span>
          </button>
        </div>
        <div class="topbar-right">
          <div class="user-info">
            <span>管理员: {{ adminStore.admin?.username }}</span>
            <button class="logout-btn" @click="logout">退出</button>
          </div>
        </div>
      </header>

      <!-- 页面内容 -->
      <main class="content">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { RouterView, useRouter } from 'vue-router'
// @ts-ignore
import { useAdminStore } from '../stores/admin'

const adminStore = useAdminStore()
const router = useRouter()

const isSidebarCollapsed = ref(false)

const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
}

const logout = () => {
  adminStore.logout()
  router.push('/')
}
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
}

.sidebar {
  width: 280px;
  background: #2c3e50;
  color: white;
  transition: all 0.3s ease;
  flex-shrink: 0;
  position: fixed;
  height: 100vh;
  z-index: 1000;
  box-shadow: 3px 0 10px rgba(0, 0, 0, 0.1);
  box-sizing: border-box;
}

.sidebar-collapsed {
  width: 80px;
}

.sidebar-header {
  padding: 2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  box-sizing: border-box;
}

.sidebar-header h2 {
  margin: 0;
  font-size: 1.5rem;
  color: #42b883;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sidebar-nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-link {
  display: flex;
  align-items: center;
  padding: 1.25rem 2rem;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: all 0.3s ease;
  white-space: nowrap;
  font-size: 1.1rem;
  box-sizing: border-box;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.nav-link.active {
  background: #42b883;
  color: white;
}

.nav-link .icon {
  margin-right: 1rem;
  font-size: 1.4rem;
  min-width: 1.4rem;
  text-align: center;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-left: 280px;
  width: calc(100% - 280px);
  box-sizing: border-box;
}

.sidebar-collapsed + .main-content {
  margin-left: 80px;
  width: calc(100% - 80px);
}

.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 3rem;
  background: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  z-index: 100;
  position: sticky;
  top: 0;
  width: 100%;
  box-sizing: border-box;
}

.menu-toggle {
  background: none;
  border: none;
  font-size: 1.8rem;
  cursor: pointer;
  color: #333;
  padding: 0.5rem;
  border-radius: 6px;
  transition: background 0.3s ease;
  box-sizing: border-box;
}

.menu-toggle:hover {
  background: #f5f5f5;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  box-sizing: border-box;
}

.logout-btn {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s ease;
  font-size: 1.1rem;
  font-weight: 500;
  box-sizing: border-box;
}

.logout-btn:hover {
  background: #c0392b;
}

.content {
  flex: 1;
  padding: 2rem 3rem;
  background: #f8f9fa;
  overflow-y: auto;
  min-height: calc(100vh - 80px);
  width: 100%;
  box-sizing: border-box;
}

/* 宽屏PC适配 */
@media (min-width: 1200px) {
  .sidebar {
    width: 300px;
  }
  
  .sidebar-collapsed {
    width: 90px;
  }
  
  .sidebar-header {
    padding: 2.5rem;
  }
  
  .sidebar-header h2 {
    font-size: 1.6rem;
  }
  
  .nav-link {
    padding: 1.5rem 2.5rem;
    font-size: 1.2rem;
  }
  
  .nav-link .icon {
    font-size: 1.5rem;
    margin-right: 1.2rem;
  }
  
  .main-content {
    margin-left: 300px;
    width: calc(100% - 300px);
  }
  
  .sidebar-collapsed + .main-content {
    margin-left: 90px;
    width: calc(100% - 90px);
  }
  
  .topbar {
    padding: 1.5rem 4rem;
  }
  
  .content {
    padding: 2.5rem 4rem;
  }
}

/* 大宽屏PC适配 */
@media (min-width: 1600px) {
  .sidebar {
    width: 320px;
  }
  
  .sidebar-collapsed {
    width: 100px;
  }
  
  .sidebar-header {
    padding: 3rem;
  }
  
  .sidebar-header h2 {
    font-size: 1.8rem;
  }
  
  .nav-link {
    padding: 1.75rem 3rem;
    font-size: 1.3rem;
  }
  
  .nav-link .icon {
    font-size: 1.6rem;
    margin-right: 1.5rem;
  }
  
  .main-content {
    margin-left: 320px;
    width: calc(100% - 320px);
  }
  
  .sidebar-collapsed + .main-content {
    margin-left: 100px;
    width: calc(100% - 100px);
  }
  
  .topbar {
    padding: 2rem 5rem;
  }
  
  .content {
    padding: 3rem 5rem;
  }
}

/* 超宽屏PC适配 */
@media (min-width: 2000px) {
  .sidebar {
    width: 350px;
  }
  
  .sidebar-collapsed {
    width: 120px;
  }
  
  .sidebar-header {
    padding: 3.5rem;
  }
  
  .sidebar-header h2 {
    font-size: 2rem;
  }
  
  .nav-link {
    padding: 2rem 3.5rem;
    font-size: 1.4rem;
  }
  
  .nav-link .icon {
    font-size: 1.8rem;
    margin-right: 1.8rem;
  }
  
  .main-content {
    margin-left: 350px;
    width: calc(100% - 350px);
  }
  
  .sidebar-collapsed + .main-content {
    margin-left: 120px;
    width: calc(100% - 120px);
  }
  
  .topbar {
    padding: 2.5rem 6rem;
  }
  
  .content {
    padding: 3.5rem 6rem;
  }
}
</style>