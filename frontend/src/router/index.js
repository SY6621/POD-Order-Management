import { createRouter, createWebHistory } from 'vue-router'
import { useShopStore } from '../stores/shopStore'
import { useAdminStore } from '../stores/adminStore'

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
  },
  {
    path: '/shipping',
    name: 'ShippingOrder',
    component: () => import('../views/ShippingOrder/ShippingOrder.vue'),
    meta: { title: '物流下单' }
  },
  {
    path: '/pickup-confirm',
    name: 'PickupConfirm',
    component: () => import('../views/PickupConfirm/PickupConfirm.vue'),
    meta: { title: '揽件确认' }
  },
  {
    path: '/factory-workshop',
    name: 'FactoryWorkshop',
    component: () => import('../views/FactoryWorkshop/FactoryWorkshop.vue'),
    meta: { title: '工厂协作平台' }
  },
  // 店铺独立页面
  {
    path: '/store/login',
    name: 'StoreLogin',
    component: () => import('../views/StorePortal/StoreLogin.vue'),
    meta: { title: '店铺登录' }
  },
  {
    path: '/store/:shopCode/login',
    name: 'StoreLoginWithCode',
    component: () => import('../views/StorePortal/StoreLogin.vue'),
    meta: { title: '店铺登录' }
  },
  {
    path: '/store/:shopCode/orders',
    name: 'StoreOrders',
    component: () => import('../views/StorePortal/StoreOrders.vue'),
    meta: { title: '店铺订单', requiresShopAuth: true }
  },
  {
    path: '/store/:shopCode/effects',
    name: 'StoreEffects',
    component: () => import('../views/StorePortal/StoreEffects.vue'),
    meta: { title: '效果图下载', requiresShopAuth: true }
  },
  // 简化版：直接通过链接访问效果图下载（无需登录）
  {
    path: '/download/:orderId',
    name: 'StoreDownload',
    component: () => import('../views/StorePortal/StoreDownload.vue'),
    meta: { title: '效果图下载' }
  },
  // 中央管理系统
  {
    path: '/admin/login',
    name: 'AdminLogin',
    component: () => import('../views/Admin/AdminLogin.vue'),
    meta: { title: '管理员登录' }
  },
  {
    path: '/admin',
    component: () => import('../views/Admin/AdminLayout.vue'),
    meta: { requiresAdminAuth: true },
    children: [
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: () => import('../views/Admin/AdminDashboard.vue'),
        meta: { title: '仪表盘总览' }
      },
      // 订单工作流（7项导航）
      {
        path: 'orders/pending',
        name: 'OrdersPending',
        component: () => import('../views/Admin/OrdersPending.vue'),
        meta: { title: '待确认订单' }
      },
      {
        path: 'orders/shipping',
        name: 'OrdersShipping',
        component: () => import('../views/Admin/AdminOrders.vue'), // 复用现有页面
        meta: { title: '物流下单' }
      },
      {
        path: 'orders/producing',
        name: 'OrdersProducing',
        component: () => import('../views/Admin/AdminOrders.vue'), // 复用现有页面
        meta: { title: '生产中订单' }
      },
      {
        path: 'orders/completed',
        name: 'OrdersCompleted',
        component: () => import('../views/Admin/AdminOrders.vue'), // 复用现有页面
        meta: { title: '已完成订单' }
      },
      {
        path: 'templates',
        name: 'AdminTemplates',
        component: () => import('../views/Admin/AdminEffects.vue'), // 复用现有页面
        meta: { title: '邮件模板' }
      },
      {
        path: 'factory-overview',
        name: 'FactoryOverview',
        component: () => import('../views/Admin/AdminFactories.vue'), // 复用现有页面
        meta: { title: '工厂生产总览' }
      },
      // 系统管理（仅主账号可见）
      {
        path: 'shops',
        name: 'AdminShops',
        component: () => import('../views/Admin/AdminShops.vue'),
        meta: { title: '店铺管理', requiresMainAccount: true }
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: () => import('../views/Admin/AdminUsers.vue'),
        meta: { title: '子账号管理', requiresMainAccount: true }
      },
      {
        path: 'factories',
        name: 'AdminFactories',
        component: () => import('../views/Admin/AdminFactories.vue'),
        meta: { title: '工厂管理', requiresMainAccount: true }
      },
      {
        path: 'settings',
        name: 'AdminSettings',
        component: () => import('../views/Admin/AdminDashboard.vue'), // 临时复用
        meta: { title: '系统设置', requiresMainAccount: true }
      },
      // 保留旧路由兼容
      {
        path: 'orders',
        redirect: '/admin/orders/pending'
      },
      {
        path: 'effects',
        redirect: '/admin/templates'
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  document.title = to.meta.title || 'ETSY订单管理系统'
  
  // 检查是否需要店铺认证
  if (to.meta.requiresShopAuth) {
    const shopStore = useShopStore()
    const isAuth = await shopStore.checkAuth()
    
    if (!isAuth) {
      // 未登录，跳转到店铺登录页
      next(`/store/${to.params.shopCode}/login`)
      return
    }
    
    // 检查店铺代码是否匹配
    if (shopStore.currentShop?.code !== to.params.shopCode) {
      next('/store/login')
      return
    }
  }
  
  // 检查是否需要管理员认证
  if (to.meta.requiresAdminAuth) {
    const adminStore = useAdminStore()
    const isAuth = await adminStore.checkAuth()
    
    if (!isAuth) {
      // 未登录，跳转到管理员登录页
      next('/admin/login')
      return
    }
    
    // 检查是否需要主账号权限
    if (to.meta.requiresMainAccount) {
      const isMain = adminStore.currentUser?.role_type === 'main'
      if (!isMain) {
        // 子账号无权限，跳转到仪表盘
        next('/admin/dashboard')
        return
      }
    }
  }
  
  next()
})

export default router
