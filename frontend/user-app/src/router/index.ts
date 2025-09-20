import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import { useAuthStore } from '../stores/auth'

// 创建路由前守卫
const requireAuth = async (_to: any, _from: any, next: any) => {
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

// 管理员路由守卫
const requireAdminAuth = async (_to: any, _from: any, next: any) => {
  // 检查是否存在管理员token
  const adminToken = localStorage.getItem('admin_token')
  
  if (adminToken) {
    // 如果存在管理员token，允许访问
    next()
  } else {
    // 如果不存在管理员token，重定向到管理员登录页面
    next('/admin/login')
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
      path: '/trips/:id',
      name: 'trip-detail',
      component: () => import('../views/TripDetailView.vue'),
      beforeEnter: requireAuth
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
      path: '/secondhand',
      name: 'secondhand',
      component: () => import('../views/SecondHandView.vue'),
    },
    {
      path: '/secondhand/:id',
      name: 'secondhand-detail',
      component: () => import('../views/SecondHandDetailView.vue'),
      beforeEnter: requireAuth
    },
    {
      path: '/publish-secondhand',
      name: 'publish-secondhand',
      component: () => import('../views/PublishSecondHandView.vue'),
      beforeEnter: requireAuth
    },
    {
      path: '/errands',
      name: 'errands',
      component: () => import('../views/ErrandsView.vue'),
    },
    {
      path: '/errands/:id',
      name: 'errand-detail',
      component: () => import('../views/ErrandDetailView.vue'),
      beforeEnter: requireAuth
    },
    {
      path: '/publish-errand',
      name: 'publish-errand',
      component: () => import('../views/PublishErrandView.vue'),
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
    // 管理员路由
    {
      path: '/admin/login',
      name: 'admin-login',
      component: () => import('../views/admin/AdminLoginView.vue'),
    },
    {
      path: '/admin/dashboard',
      name: 'admin-dashboard',
      component: () => import('../views/admin/AdminDashboardView.vue'),
      beforeEnter: requireAdminAuth
    },
  ],
})

export default router