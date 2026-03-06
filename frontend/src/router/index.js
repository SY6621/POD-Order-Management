import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('../views/Dashboard/Dashboard.vue'),
    meta: { title: '仪表盘总览' }
  },
  {
    path: '/pending',
    name: 'PendingOrders',
    component: () => import('../views/PendingOrders/PendingOrders.vue'),
    meta: { title: '待确认订单' }
  },
  {
    path: '/production',
    name: 'Production',
    component: () => import('../views/Production/Production.vue'),
    meta: { title: '生产中订单' }
  },
  {
    path: '/completed',
    name: 'CompletedOrders',
    component: () => import('../views/CompletedOrders/CompletedOrders.vue'),
    meta: { title: '已完成订单' }
  },
  {
    path: '/logistics',
    name: 'Logistics',
    component: () => import('../views/Logistics/Logistics.vue'),
    meta: { title: '物流追踪' }
  },
  {
    path: '/email',
    name: 'EmailTemplates',
    component: () => import('../views/EmailTemplates/EmailTemplates.vue'),
    meta: { title: '邮件模板' }
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
