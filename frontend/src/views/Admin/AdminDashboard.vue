<template>
  <div class="p-8">
    <!-- 页面标题 -->
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-slate-800">仪表盘</h1>
      <p class="text-slate-500">系统概览与数据统计</p>
    </div>

    <!-- 统计卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-xl p-6 border border-slate-200 shadow-sm">
        <div class="flex items-center justify-between mb-4">
          <div class="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2">
              <rect width="8" height="4" x="8" y="2" rx="1" ry="1"/>
              <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/>
            </svg>
          </div>
          <span class="text-sm text-green-600 font-medium">+12%</span>
        </div>
        <p class="text-3xl font-bold text-slate-800">{{ stats.totalOrders }}</p>
        <p class="text-sm text-slate-500">总订单数</p>
      </div>

      <div class="bg-white rounded-xl p-6 border border-slate-200 shadow-sm">
        <div class="flex items-center justify-between mb-4">
          <div class="w-12 h-12 bg-orange-100 rounded-xl flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f97316" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <polyline points="12 6 12 12 16 14"/>
            </svg>
          </div>
          <span class="text-sm text-orange-600 font-medium">待处理</span>
        </div>
        <p class="text-3xl font-bold text-slate-800">{{ stats.pendingOrders }}</p>
        <p class="text-sm text-slate-500">待确认订单</p>
      </div>

      <div class="bg-white rounded-xl p-6 border border-slate-200 shadow-sm">
        <div class="flex items-center justify-between mb-4">
          <div class="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#9333ea" stroke-width="2">
              <path d="m15 12-8.5 8.5c-.83.83-2.17.83-3 0 0 0 0 0 0 0a2.12 2.12 0 0 1 0-3L12 9"/>
            </svg>
          </div>
          <span class="text-sm text-purple-600 font-medium">进行中</span>
        </div>
        <p class="text-3xl font-bold text-slate-800">{{ stats.producingOrders }}</p>
        <p class="text-sm text-slate-500">生产中订单</p>
      </div>

      <div class="bg-white rounded-xl p-6 border border-slate-200 shadow-sm">
        <div class="flex items-center justify-between mb-4">
          <div class="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
              <polyline points="9 11 12 14 22 4"/>
            </svg>
          </div>
          <span class="text-sm text-green-600 font-medium">已完成</span>
        </div>
        <p class="text-3xl font-bold text-slate-800">{{ stats.completedOrders }}</p>
        <p class="text-sm text-slate-500">已完成订单</p>
      </div>
    </div>

    <!-- 店铺统计 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="bg-white rounded-xl border border-slate-200 shadow-sm">
        <div class="px-6 py-4 border-b border-slate-200 flex items-center justify-between">
          <h2 class="font-bold text-slate-800">店铺分布</h2>
          <router-link to="/admin/shops" class="text-sm text-blue-600 hover:underline">管理店铺</router-link>
        </div>
        <div class="p-6">
          <div class="space-y-4">
            <div v-for="shop in shopStats" :key="shop.id" class="flex items-center justify-between">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center">
                  <span class="font-bold text-blue-600">{{ shop.code.toUpperCase() }}</span>
                </div>
                <div>
                  <p class="font-medium text-slate-800">{{ shop.name }}</p>
                  <p class="text-sm text-slate-500">{{ shop.region }}</p>
                </div>
              </div>
              <div class="text-right">
                <p class="font-bold text-slate-800">{{ shop.orderCount }}</p>
                <p class="text-sm text-slate-500">订单</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl border border-slate-200 shadow-sm">
        <div class="px-6 py-4 border-b border-slate-200 flex items-center justify-between">
          <h2 class="font-bold text-slate-800">快捷操作</h2>
        </div>
        <div class="p-6">
          <div class="grid grid-cols-2 gap-4">
            <router-link to="/admin/orders" class="p-4 bg-blue-50 rounded-xl hover:bg-blue-100 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" class="mb-2">
                <rect width="8" height="4" x="8" y="2" rx="1" ry="1"/>
                <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/>
              </svg>
              <p class="font-medium text-slate-800">订单管理</p>
              <p class="text-sm text-slate-500">查看所有订单</p>
            </router-link>

            <router-link to="/admin/effects" class="p-4 bg-purple-50 rounded-xl hover:bg-purple-100 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#9333ea" stroke-width="2" class="mb-2">
                <rect width="18" height="18" x="3" y="3" rx="2" ry="2"/>
                <circle cx="9" cy="9" r="2"/>
                <path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>
              </svg>
              <p class="font-medium text-slate-800">效果图管理</p>
              <p class="text-sm text-slate-500">生成与分发</p>
            </router-link>

            <router-link to="/admin/factories" class="p-4 bg-green-50 rounded-xl hover:bg-green-100 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2" class="mb-2">
                <path d="M21 10V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l2-1.14"/>
                <path d="m7.5 4.27 9 5.15"/>
                <polyline points="3.29 7 12 12 20.71 7"/>
                <line x1="12" x2="12" y1="22" y2="12"/>
              </svg>
              <p class="font-medium text-slate-800">工厂管理</p>
              <p class="text-sm text-slate-500">生产管理平台</p>
            </router-link>

            <router-link to="/admin/shops" class="p-4 bg-orange-50 rounded-xl hover:bg-orange-100 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f97316" stroke-width="2" class="mb-2">
                <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
                <polyline points="9 22 9 12 15 12 15 22"/>
              </svg>
              <p class="font-medium text-slate-800">店铺管理</p>
              <p class="text-sm text-slate-500">店铺访问入口</p>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAdminStore } from '../../stores/adminStore'

const adminStore = useAdminStore()

const stats = ref({
  totalOrders: 0,
  pendingOrders: 0,
  producingOrders: 0,
  completedOrders: 0
})

const shopStats = ref([])

onMounted(async () => {
  // 加载订单统计
  const orders = await adminStore.fetchAllOrders()
  stats.value = {
    totalOrders: orders.length,
    pendingOrders: orders.filter(o => o.status === 'pending').length,
    producingOrders: orders.filter(o => o.status === 'producing').length,
    completedOrders: orders.filter(o => ['shipped', 'delivered'].includes(o.status)).length
  }

  // 加载店铺统计
  const shops = await adminStore.fetchShops()
  shopStats.value = shops.map(shop => ({
    ...shop,
    orderCount: orders.filter(o => o.shop_id === shop.id).length
  }))
})
</script>