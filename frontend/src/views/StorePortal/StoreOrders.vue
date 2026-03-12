<template>
  <div class="min-h-screen bg-slate-50">
    <!-- 顶部导航 -->
    <header class="bg-white border-b border-slate-200 px-6 py-4">
      <div class="max-w-6xl mx-auto flex items-center justify-between">
        <div class="flex items-center gap-4">
          <div class="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center">
            <span class="font-bold text-blue-600">{{ shopStore.currentShop?.code?.toUpperCase() }}</span>
          </div>
          <div>
            <h1 class="font-bold text-slate-800">{{ shopStore.currentShop?.name }}</h1>
            <p class="text-sm text-slate-500">店铺订单中心</p>
          </div>
        </div>
        <div class="flex items-center gap-3">
          <button 
            @click="shopStore.logout(); $router.push('/store/login')"
            class="text-sm text-slate-500 hover:text-slate-700"
          >
            退出登录
          </button>
        </div>
      </div>
    </header>

    <main class="max-w-6xl mx-auto p-6">
      <!-- 统计卡片 -->
      <div class="grid grid-cols-4 gap-4 mb-6">
        <div class="bg-white rounded-xl p-4 border border-slate-200">
          <p class="text-sm text-slate-500">全部订单</p>
          <p class="text-2xl font-bold text-slate-800">{{ orders.length }}</p>
        </div>
        <div class="bg-white rounded-xl p-4 border border-slate-200">
          <p class="text-sm text-slate-500">待确认</p>
          <p class="text-2xl font-bold text-orange-600">{{ pendingCount }}</p>
        </div>
        <div class="bg-white rounded-xl p-4 border border-slate-200">
          <p class="text-sm text-slate-500">生产中</p>
          <p class="text-2xl font-bold text-purple-600">{{ producingCount }}</p>
        </div>
        <div class="bg-white rounded-xl p-4 border border-slate-200">
          <p class="text-sm text-slate-500">已完成</p>
          <p class="text-2xl font-bold text-green-600">{{ completedCount }}</p>
        </div>
      </div>

      <!-- 订单列表 -->
      <div class="bg-white rounded-xl border border-slate-200 overflow-hidden">
        <div class="px-6 py-4 border-b border-slate-200 flex items-center justify-between">
          <h2 class="font-bold text-slate-800">订单列表</h2>
          <div class="flex gap-2">
            <button 
              @click="$router.push(`/store/${shopStore.currentShop?.code}/effects`)"
              class="px-4 py-2 bg-blue-50 text-blue-600 rounded-lg text-sm font-medium hover:bg-blue-100"
            >
              下载效果图
            </button>
          </div>
        </div>
        
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-slate-50">
              <tr>
                <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">订单号</th>
                <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">产品</th>
                <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">定制内容</th>
                <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">状态</th>
                <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">创建时间</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              <tr v-for="order in orders" :key="order.id" class="hover:bg-slate-50">
                <td class="py-4 px-4">
                  <p class="font-mono font-semibold text-slate-800">{{ order.etsy_order_id }}</p>
                </td>
                <td class="py-4 px-4">
                  <div class="flex items-center gap-2">
                    <span class="w-3 h-3 rounded-full" :class="getColorClass(order.product_color)"></span>
                    <span class="text-sm">{{ order.product_shape }} - {{ order.product_color }}</span>
                  </div>
                </td>
                <td class="py-4 px-4">
                  <p class="text-sm">正面: {{ order.front_text }}</p>
                  <p class="text-sm text-slate-500">背面: {{ order.back_text }}</p>
                </td>
                <td class="py-4 px-4">
                  <span :class="getStatusClass(order.status)" class="px-2 py-1 rounded-full text-xs font-medium">
                    {{ getStatusText(order.status) }}
                  </span>
                </td>
                <td class="py-4 px-4 text-sm text-slate-500">
                  {{ formatDate(order.created_at) }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useShopStore } from '../../stores/shopStore'

const shopStore = useShopStore()
const orders = ref([])

// 计算属性
const pendingCount = computed(() => orders.value.filter(o => o.status === 'pending').length)
const producingCount = computed(() => orders.value.filter(o => o.status === 'producing').length)
const completedCount = computed(() => orders.value.filter(o => ['shipped', 'delivered'].includes(o.status)).length)

// 加载订单
onMounted(async () => {
  orders.value = await shopStore.fetchShopOrders()
})

// 辅助函数
function getColorClass(color) {
  const map = { '金色': 'bg-yellow-400', '银色': 'bg-gray-300', '玫瑰金': 'bg-amber-700' }
  return map[color] || 'bg-gray-400'
}

function getStatusClass(status) {
  const map = {
    'pending': 'bg-orange-100 text-orange-700',
    'confirmed': 'bg-blue-100 text-blue-700',
    'producing': 'bg-purple-100 text-purple-700',
    'shipped': 'bg-green-100 text-green-700',
    'delivered': 'bg-slate-100 text-slate-700'
  }
  return map[status] || 'bg-slate-100 text-slate-600'
}

function getStatusText(status) {
  const map = {
    'pending': '待确认',
    'confirmed': '已确认',
    'producing': '生产中',
    'shipped': '已发货',
    'delivered': '已送达'
  }
  return map[status] || status
}

function formatDate(dateStr) {
  if (!dateStr) return '--'
  const date = new Date(dateStr)
  return `${date.getMonth() + 1}/${date.getDate()} ${date.getHours()}:${date.getMinutes().toString().padStart(2, '0')}`
}
</script>