import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('../views/Dashboard/Dashboard.vue'),
    meta: { title: '仪表盘' }
  },
  {
    path: '/orders',
    name: 'Orders',
    component: () => import('../views/Orders/Orders.vue'),
    meta: { title: '订单管理' }
  },
  {
    path: '/effects',
    name: 'Effects',
    component: () => import('../views/Effects/Effects.vue'),
    meta: { title: '效果图生成' }
  },
  {
    path: '/production',
    name: 'Production',
    component: () => import('../views/Production/Production.vue'),
    meta: { title: '生产文档' }
  },
  {
    path: '/logistics',
    name: 'Logistics',
    component: () => import('../views/Logistics/Logistics.vue'),
    meta: { title: '物流管理' }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('../views/Settings/Settings.vue'),
    meta: { title: '系统设置' }
  },
  {
    path: '/remote',
    name: 'Remote',
    component: () => import('../views/Remote/Remote.vue'),
    meta: { title: '远程协作工作台' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'ETSY订单管理系统'
  next()
})

export default router
