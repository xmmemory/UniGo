import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import { useAuthStore } from '@/stores/auth'

// 创建路由前守卫
const requireAuth = async (to: any, from: any, next: any) => {
  const authStore = useAuthStore()
  // 初始化认证状态
  await authStore.initializeAuth()
  
  if (authStore.isAuthenticated) {
    // 如果已认证，允许访问
    next()
  } else {
    // 如果未认证，重定向到登录页面
    next('/login')
  }
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/trips',
      name: 'trips',
      component: () => import('../views/TripsView.vue'),
      // 移除认证守卫，允许未登录用户访问行程页面
    },
    {
      path: '/publish-trip',
      name: 'publish-trip',
      component: () => import('../views/PublishTripView.vue'),
      beforeEnter: requireAuth
    },
    {
      path: '/bookings',
      name: 'bookings',
      component: () => import('../views/BookingsView.vue'),
      beforeEnter: requireAuth
    },
    {
      path: '/history',
      name: 'history',
      component: () => import('../views/HistoryView.vue'),
      beforeEnter: requireAuth
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/ProfileView.vue'),
      beforeEnter: requireAuth
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue'),
    },
  ],
})

export default router