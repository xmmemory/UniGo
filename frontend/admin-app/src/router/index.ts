import { createRouter, createWebHistory } from 'vue-router'
import AdminLoginView from '../views/AdminLoginView.vue'
import AdminLayout from '../components/AdminLayout.vue'
import DashboardView from '../views/DashboardView.vue'
import UserManagementView from '../views/UserManagementView.vue'
import TripManagementView from '../views/TripManagementView.vue'
import SecondHandManagementView from '../views/SecondHandManagementView.vue'
import ErrandManagementView from '../views/ErrandManagementView.vue'
import StatsView from '../views/StatsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'admin-login',
      component: AdminLoginView,
    },
    {
      path: '/admin',
      component: AdminLayout,
      children: [
        {
          path: 'dashboard',
          name: 'admin-dashboard',
          component: DashboardView,
        },
        {
          path: 'users',
          name: 'admin-users',
          component: UserManagementView,
        },
        {
          path: 'trips',
          name: 'admin-trips',
          component: TripManagementView,
        },
        {
          path: 'secondhand',
          name: 'admin-secondhand',
          component: SecondHandManagementView,
        },
        {
          path: 'errands',
          name: 'admin-errands',
          component: ErrandManagementView,
        },
        {
          path: 'stats',
          name: 'admin-stats',
          component: StatsView,
        },
        {
          path: '',
          redirect: 'dashboard',
        },
      ],
    },
  ],
})

export default router