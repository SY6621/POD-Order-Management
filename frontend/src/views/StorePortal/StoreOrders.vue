<template>
  <div class="min-h-screen bg-slate-50">
    <!-- 顶部导航 -->
    <header class="bg-white border-b border-slate-200 px-6 py-4">
      <div class="max-w-6xl mx-auto flex items-center justify-between">
        <div class="flex items-center gap-4">
          <div class="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center">
            <span class="text-lg">{{ shopStore.currentShop?.flag_emoji || shopStore.currentShop?.code?.toUpperCase() }}</span>
          </div>
          <div>
            <h1 class="font-bold text-slate-800">{{ shopStore.currentShop?.name }}</h1>
            <p class="text-sm text-slate-500">店铺订单中心</p>
          </div>
        </div>
        <div class="flex items-center gap-3">
          <button 
            @click="$router.push(`/store/${shopStore.currentShop?.code}/effects`)"
            class="px-4 py-2 bg-blue-50 text-blue-600 rounded-lg text-sm font-medium hover:bg-blue-100"
          >
            下载效果图
          </button>
          <button 
            @click="handleLogout"
            class="text-sm text-slate-500 hover:text-slate-700"
          >
            退出登录
          </button>
        </div>
      </div>
    </header>

    <main class="max-w-6xl mx-auto p-6">
      <!-- 统计卡片 -->
      <div class="grid grid-cols-5 gap-4 mb-6">
        <div 
          class="bg-white rounded-xl p-4 border-2 cursor-pointer transition-all"
          :class="statusFilter === 'all' ? 'border-blue-500 bg-blue-50' : 'border-slate-200'"
          @click="statusFilter = 'all'"
        >
          <p class="text-sm text-slate-500">全部订单</p>
          <p class="text-2xl font-bold text-slate-800">{{ orders.length }}</p>
        </div>
        <div 
          class="bg-white rounded-xl p-4 border-2 cursor-pointer transition-all"
          :class="statusFilter === 'pending' ? 'border-orange-500 bg-orange-50' : 'border-slate-200'"
          @click="statusFilter = 'pending'"
        >
          <p class="text-sm text-slate-500">待确认</p>
          <p class="text-2xl font-bold text-orange-600">{{ pendingCount }}</p>
        </div>
        <div 
          class="bg-white rounded-xl p-4 border-2 cursor-pointer transition-all"
          :class="statusFilter === 'producing' ? 'border-purple-500 bg-purple-50' : 'border-slate-200'"
          @click="statusFilter = 'producing'"
        >
          <p class="text-sm text-slate-500">生产中</p>
          <p class="text-2xl font-bold text-purple-600">{{ producingCount }}</p>
        </div>
        <div 
          class="bg-white rounded-xl p-4 border-2 cursor-pointer transition-all"
          :class="statusFilter === 'shipped' ? 'border-green-500 bg-green-50' : 'border-slate-200'"
          @click="statusFilter = 'shipped'"
        >
          <p class="text-sm text-slate-500">已发货</p>
          <p class="text-2xl font-bold text-green-600">{{ shippedCount }}</p>
        </div>
        <div 
          class="bg-white rounded-xl p-4 border-2 cursor-pointer transition-all"
          :class="statusFilter === 'delivered' ? 'border-slate-500 bg-slate-100' : 'border-slate-200'"
          @click="statusFilter = 'delivered'"
        >
          <p class="text-sm text-slate-500">已交付</p>
          <p class="text-2xl font-bold text-slate-600">{{ deliveredCount }}</p>
        </div>
      </div>

      <!-- 订单列表 -->
      <div class="bg-white rounded-xl border border-slate-200 overflow-hidden">
        <div class="px-6 py-4 border-b border-slate-200 flex items-center justify-between flex-wrap gap-4">
          <h2 class="font-bold text-slate-800">订单列表</h2>
          <div class="flex gap-2 items-center">
            <!-- 搜索框 -->
            <div class="relative">
              <input 
                v-model="searchQuery"
                type="text"
                placeholder="搜索订单号/客户名"
                class="pl-10 pr-4 py-2 border border-slate-200 rounded-lg text-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none w-64"
                @input="handleSearch"
              >
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400">
                <circle cx="11" cy="11" r="8"/>
                <path d="m21 21-4.3-4.3"/>
              </svg>
            </div>
            <button 
              @click="refreshOrders"
              class="p-2 text-slate-500 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-all"
              title="刷新"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>
                <path d="M3 3v5h5"/>
                <path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"/>
                <path d="M16 16h5v5"/>
              </svg>
            </button>
          </div>
        </div>
        
        <!-- 加载状态 -->
        <div v-if="loading" class="p-12 text-center">
          <div class="inline-block w-8 h-8 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
          <p class="text-slate-500 mt-2">加载中...</p>
        </div>
        
        <!-- 空状态 -->
        <div v-else-if="filteredOrders.length === 0" class="p-12 text-center text-slate-500">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="mx-auto mb-4 text-slate-300">
            <path d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2"/>
            <rect x="9" y="3" width="6" height="4" rx="2"/>
            <path d="M9 14h.01"/>
            <path d="M9 17h.01"/>
            <path d="M12 14h.01"/>
            <path d="M12 17h.01"/>
            <path d="M15 14h.01"/>
            <path d="M15 17h.01"/>
          </svg>
          <p>暂无订单数据</p>
        </div>
        
        <div v-else class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-slate-50">
              <tr>
                <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">订单号</th>
                <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">客户</th>
                <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">产品</th>
                <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">定制内容</th>
                <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">状态</th>
                <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">创建时间</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              <tr v-for="order in paginatedOrders" :key="order.id" class="hover:bg-slate-50">
                <td class="py-4 px-4">
                  <p class="font-mono font-semibold text-slate-800">{{ order.order_number }}</p>
                </td>
                <td class="py-4 px-4">
                  <p class="text-sm font-medium text-slate-700">{{ order.customer_name || '-' }}</p>
                </td>
                <td class="py-4 px-4">
                  <div class="flex items-center gap-2">
                    <span class="w-3 h-3 rounded-full" :class="getColorClass(order.product_color)"></span>
                    <span class="text-sm">{{ order.product_shape || '-' }} - {{ order.product_color || '-' }}</span>
                  </div>
                </td>
                <td class="py-4 px-4">
                  <p class="text-sm">正面: {{ order.front_text || '-' }}</p>
                  <p class="text-sm text-slate-500">背面: {{ order.back_text || '-' }}</p>
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
          
          <!-- 分页 -->
          <div class="px-6 py-4 border-t border-slate-200 flex items-center justify-between">
            <p class="text-sm text-slate-500">
              共 {{ filteredOrders.length }} 条，第 {{ currentPage }} / {{ totalPages }} 页
            </p>
            <div class="flex gap-2">
              <button 
                @click="currentPage--"
                :disabled="currentPage === 1"
                class="px-3 py-1.5 border border-slate-200 rounded-lg text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-slate-50"
              >
                上一页
              </button>
              <button 
                @click="currentPage++"
                :disabled="currentPage === totalPages"
                class="px-3 py-1.5 border border-slate-200 rounded-lg text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-slate-50"
              >
                下一页
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useShopStore } from '../../stores/shopStore'

const router = useRouter()
const shopStore = useShopStore()

// 状态
const orders = ref([])
const loading = ref(false)
const searchQuery = ref('')
const statusFilter = ref('all')
const currentPage = ref(1)
const pageSize = 10

// 计算属性 - 统计
const pendingCount = computed(() => orders.value.filter(o => o.status === 'pending').length)
const producingCount = computed(() => orders.value.filter(o => o.status === 'producing').length)
const shippedCount = computed(() => orders.value.filter(o => o.status === 'shipped').length)
const deliveredCount = computed(() => orders.value.filter(o => o.status === 'delivered').length)

// 计算属性 - 筛选后的订单
const filteredOrders = computed(() => {
  let result = orders.value
  
  // 状态筛选
  if (statusFilter.value !== 'all') {
    result = result.filter(o => o.status === statusFilter.value)
  }
  
  // 搜索筛选
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(o => 
      (o.order_number && o.order_number.toLowerCase().includes(query)) ||
      (o.customer_name && o.customer_name.toLowerCase().includes(query))
    )
  }
  
  return result
})

// 计算属性 - 分页
const totalPages = computed(() => Math.ceil(filteredOrders.value.length / pageSize))
const paginatedOrders = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  const end = start + pageSize
  return filteredOrders.value.slice(start, end)
})

// 重置页码当筛选条件变化
watch([searchQuery, statusFilter], () => {
  currentPage.value = 1
})

// 加载订单
const loadOrders = async () => {
  loading.value = true
  try {
    orders.value = await shopStore.fetchShopOrders()
  } catch (err) {
    console.error('加载订单失败:', err)
    ElMessage.error('加载订单失败')
  } finally {
    loading.value = false
  }
}

// 刷新订单
const refreshOrders = () => {
  loadOrders()
  ElMessage.success('刷新成功')
}

// 搜索处理（防抖）
let searchTimeout = null
const handleSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    currentPage.value = 1
  }, 300)
}

// 退出登录
const handleLogout = () => {
  shopStore.logout()
  router.push('/store/login')
  ElMessage.success('已退出登录')
}

// 初始化
onMounted(() => {
  loadOrders()
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