<template>
  <div class="p-8">
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-slate-800">订单中心</h1>
      <p class="text-slate-500">查看和管理所有店铺订单</p>
    </div>

    <!-- 筛选器 -->
    <div class="bg-white rounded-xl border border-slate-200 p-4 mb-6">
      <div class="flex gap-4">
        <select v-model="filterShop" class="px-4 py-2 border border-slate-200 rounded-lg">
          <option value="">全部店铺</option>
          <option v-for="shop in shops" :key="shop.id" :value="shop.id">{{ shop.name }}</option>
        </select>
        <select v-model="filterStatus" class="px-4 py-2 border border-slate-200 rounded-lg">
          <option value="">全部状态</option>
          <option value="pending">待确认</option>
          <option value="confirmed">已确认</option>
          <option value="producing">生产中</option>
          <option value="shipped">已发货</option>
          <option value="delivered">已送达</option>
        </select>
        <button @click="loadOrders" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
          筛选
        </button>
      </div>
    </div>

    <!-- 订单列表 -->
    <div class="bg-white rounded-xl border border-slate-200 overflow-hidden">
      <table class="w-full">
        <thead class="bg-slate-50">
          <tr>
            <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">订单号</th>
            <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">店铺</th>
            <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">产品</th>
            <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">状态</th>
            <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">创建时间</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100">
          <tr v-for="order in orders" :key="order.id" class="hover:bg-slate-50">
            <td class="py-4 px-4 font-mono font-semibold">{{ order.etsy_order_id }}</td>
            <td class="py-4 px-4">
              <span class="px-2 py-1 bg-slate-100 rounded text-sm">{{ order.shops?.name || '-' }}</span>
            </td>
            <td class="py-4 px-4">
              {{ order.product_shape }} - {{ order.product_color }}
            </td>
            <td class="py-4 px-4">
              <span :class="getStatusClass(order.status)" class="px-2 py-1 rounded-full text-xs font-medium">
                {{ getStatusText(order.status) }}
              </span>
            </td>
            <td class="py-4 px-4 text-slate-500">{{ formatDate(order.created_at) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAdminStore } from '../../stores/adminStore'

const adminStore = useAdminStore()
const orders = ref([])
const shops = ref([])
const filterShop = ref('')
const filterStatus = ref('')

onMounted(async () => {
  shops.value = await adminStore.fetchShops()
  await loadOrders()
})

async function loadOrders() {
  const filters = {}
  if (filterShop.value) filters.shopId = filterShop.value
  if (filterStatus.value) filters.status = filterStatus.value
  
  orders.value = await adminStore.fetchAllOrders(filters)
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