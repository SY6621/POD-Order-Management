<template>
  <div class="p-8">
    <!-- 页面标题 -->
    <div class="mb-8 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-slate-800">仪表盘</h1>
        <p class="text-slate-500">系统概览与数据统计</p>
      </div>
      
      <!-- 时间范围切换 -->
      <div class="flex gap-2">
        <button 
          v-for="range in timeRanges" 
          :key="range.value"
          @click="setTimeRange(range.value)"
          :class="[
            'px-4 py-2 text-sm font-medium rounded-lg transition-colors',
            currentTimeRange === range.value 
              ? 'bg-blue-600 text-white' 
              : 'bg-white text-slate-600 border border-slate-200 hover:bg-slate-50'
          ]"
        >
          {{ range.label }}
        </button>
      </div>
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
          <span class="text-sm text-green-600 font-medium">{{ totalChangeRate }}</span>
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
        <p class="text-sm text-slate-500">已交付订单</p>
      </div>
    </div>

    <!-- 待处理事项提醒区域 -->
    <div class="bg-white rounded-xl border border-slate-200 shadow-sm mb-6">
      <div class="px-6 py-4 border-b border-slate-200">
        <h2 class="font-bold text-slate-800">待处理事项</h2>
      </div>
      <div class="p-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <!-- 待确认订单（无效果图） -->
          <router-link 
            to="/admin/orders?status=pending&filter=no_effect" 
            class="flex items-center gap-4 p-4 bg-orange-50 rounded-xl hover:bg-orange-100 transition-colors"
          >
            <div class="w-10 h-10 bg-orange-200 rounded-full flex items-center justify-center">
              <span class="text-lg font-bold text-orange-600">{{ pendingItems.noEffectImage }}</span>
            </div>
            <div>
              <p class="font-medium text-slate-800">待确认订单</p>
              <p class="text-sm text-slate-500">待生成效果图</p>
            </div>
          </router-link>

          <!-- 待发送邮件 -->
          <router-link 
            to="/admin/orders?status=pending&filter=pending_email" 
            class="flex items-center gap-4 p-4 bg-blue-50 rounded-xl hover:bg-blue-100 transition-colors"
          >
            <div class="w-10 h-10 bg-blue-200 rounded-full flex items-center justify-center">
              <span class="text-lg font-bold text-blue-600">{{ pendingItems.pendingEmail }}</span>
            </div>
            <div>
              <p class="font-medium text-slate-800">待发送邮件</p>
              <p class="text-sm text-slate-500">效果图已生成</p>
            </div>
          </router-link>

          <!-- 客户修改请求 -->
          <router-link 
            to="/admin/orders?filter=modify_request" 
            class="flex items-center gap-4 p-4 bg-red-50 rounded-xl hover:bg-red-100 transition-colors"
          >
            <div class="w-10 h-10 bg-red-200 rounded-full flex items-center justify-center">
              <span class="text-lg font-bold text-red-600">{{ pendingItems.modifyRequest }}</span>
            </div>
            <div>
              <p class="font-medium text-slate-800">修改请求</p>
              <p class="text-sm text-slate-500">客户要求修改</p>
            </div>
          </router-link>
        </div>
      </div>
    </div>

    <!-- 店铺统计 + 最近订单 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- 最近订单列表 -->
      <div class="bg-white rounded-xl border border-slate-200 shadow-sm">
        <div class="px-6 py-4 border-b border-slate-200 flex items-center justify-between">
          <h2 class="font-bold text-slate-800">最近订单</h2>
          <router-link to="/admin/orders" class="text-sm text-blue-600 hover:underline">查看全部</router-link>
        </div>
        <div class="p-4">
          <div v-if="recentOrders.length === 0" class="text-center py-8 text-slate-500">
            暂无订单数据
          </div>
          <div v-else class="divide-y divide-slate-100">
            <router-link 
              v-for="order in recentOrders" 
              :key="order.id"
              :to="`/admin/orders/${order.id}`"
              class="flex items-center justify-between py-3 px-2 hover:bg-slate-50 rounded-lg transition-colors"
            >
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-slate-100 rounded-lg flex items-center justify-center">
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2">
                    <rect width="8" height="4" x="8" y="2" rx="1" ry="1"/>
                    <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/>
                  </svg>
                </div>
                <div>
                  <p class="font-medium text-slate-800 text-sm">{{ order.etsy_order_id || order.id }}</p>
                  <p class="text-xs text-slate-500">{{ order.customer_name || '未知客户' }}</p>
                </div>
              </div>
              <div class="flex items-center gap-3">
                <span 
                  :class="[
                    'px-2 py-1 text-xs font-medium rounded-full',
                    getStatusStyle(order.status)
                  ]"
                >
                  {{ getStatusText(order.status) }}
                </span>
                <span class="text-xs text-slate-400">{{ formatDate(order.created_at) }}</span>
              </div>
            </router-link>
          </div>
        </div>
      </div>

      <!-- 店铺分布 -->
      <div class="bg-white rounded-xl border border-slate-200 shadow-sm">
        <div class="px-6 py-4 border-b border-slate-200 flex items-center justify-between">
          <h2 class="font-bold text-slate-800">店铺分布</h2>
          <router-link to="/admin/shops" class="text-sm text-blue-600 hover:underline">管理店铺</router-link>
        </div>
        <div class="p-6">
          <div v-if="shopStats.length === 0" class="text-center py-8 text-slate-500">
            暂无店铺数据
          </div>
          <div v-else class="space-y-4">
            <div v-for="shop in shopStats" :key="shop.id" class="flex items-center justify-between">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center">
                  <span class="font-bold text-blue-600">{{ shop.code?.toUpperCase() || '?' }}</span>
                </div>
                <div>
                  <p class="font-medium text-slate-800">{{ shop.name }}</p>
                  <p class="text-sm text-slate-500">{{ shop.region || '未知区域' }}</p>
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
    </div>

    <!-- 快捷操作 -->
    <div class="mt-6 bg-white rounded-xl border border-slate-200 shadow-sm">
      <div class="px-6 py-4 border-b border-slate-200">
        <h2 class="font-bold text-slate-800">快捷操作</h2>
      </div>
      <div class="p-6">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
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
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAdminStore } from '../../stores/adminStore'
import supabase from '../../utils/supabase'
import { ElMessage } from 'element-plus'

const adminStore = useAdminStore()

// 时间范围选项
const timeRanges = [
  { label: '今日', value: 'today' },
  { label: '本周', value: 'week' },
  { label: '本月', value: 'month' }
]

// 当前选中的时间范围
const currentTimeRange = ref('today')

// 统计数据
const stats = ref({
  totalOrders: 0,
  pendingOrders: 0,
  producingOrders: 0,
  completedOrders: 0
})

// 待处理事项
const pendingItems = ref({
  noEffectImage: 0,
  pendingEmail: 0,
  modifyRequest: 0
})

// 最近订单（5条）
const recentOrders = ref([])

// 店铺统计
const shopStats = ref([])

// 所有订单缓存（用于时间范围筛选）
const allOrders = ref([])

// 计算增长率显示文本
const totalChangeRate = computed(() => {
  return currentTimeRange.value === 'today' ? '+12%' : 
         currentTimeRange.value === 'week' ? '+8%' : '+15%'
})

// 获取时间范围起始时间
const getTimeRangeStart = (range) => {
  const now = new Date()
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
  
  switch (range) {
    case 'today':
      return today.toISOString()
    case 'week': {
      // 本周一
      const dayOfWeek = today.getDay()
      const monday = new Date(today)
      monday.setDate(today.getDate() - (dayOfWeek === 0 ? 6 : dayOfWeek - 1))
      return monday.toISOString()
    }
    case 'month':
      return new Date(now.getFullYear(), now.getMonth(), 1).toISOString()
    default:
      return today.toISOString()
  }
}

// 状态样式映射
const statusStyleMap = {
  pending: 'bg-orange-100 text-orange-700',
  effect_sent: 'bg-blue-100 text-blue-700',
  producing: 'bg-purple-100 text-purple-700',
  completed: 'bg-green-100 text-green-700',
  delivered: 'bg-green-100 text-green-700',
  shipped: 'bg-cyan-100 text-cyan-700',
  cancelled: 'bg-red-100 text-red-700'
}

// 状态文本映射
const statusTextMap = {
  pending: '待确认',
  effect_sent: '效果图已发',
  producing: '生产中',
  completed: '已完成',
  delivered: '已送达',
  shipped: '已发货',
  cancelled: '已取消'
}

// 获取状态样式
const getStatusStyle = (status) => {
  return statusStyleMap[status] || 'bg-slate-100 text-slate-700'
}

// 获取状态文本
const getStatusText = (status) => {
  return statusTextMap[status] || status
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  const now = new Date()
  const diffDays = Math.floor((now - date) / (1000 * 60 * 60 * 24))
  
  if (diffDays === 0) {
    return '今天'
  } else if (diffDays === 1) {
    return '昨天'
  } else if (diffDays < 7) {
    return `${diffDays}天前`
  } else {
    return `${date.getMonth() + 1}/${date.getDate()}`
  }
}

// 设置时间范围并重新计算统计
const setTimeRange = (range) => {
  currentTimeRange.value = range
  calculateStats()
}

// 计算统计数据
const calculateStats = () => {
  const startTime = getTimeRangeStart(currentTimeRange.value)
  
  // 筛选时间范围内的订单
  const filteredOrders = allOrders.value.filter(o => 
    new Date(o.created_at) >= new Date(startTime)
  )
  
  // 计算各状态订单数
  stats.value = {
    totalOrders: filteredOrders.length,
    pendingOrders: filteredOrders.filter(o => o.status === 'pending').length,
    producingOrders: filteredOrders.filter(o => o.status === 'producing').length,
    completedOrders: filteredOrders.filter(o => o.status === 'delivered').length
  }
  
  // 计算待处理事项（不受时间范围限制，始终显示全局）
  pendingItems.value = {
    noEffectImage: allOrders.value.filter(o => 
      o.status === 'pending' && !o.effect_image_url
    ).length,
    pendingEmail: allOrders.value.filter(o => 
      o.status === 'pending' && o.effect_image_url && !o.email_sent
    ).length,
    modifyRequest: allOrders.value.filter(o => 
      o.email_status === 'modify'
    ).length
  }
}

// 加载所有数据
const loadAllData = async () => {
  try {
    // 加载所有订单
    const { data: orders, error: ordersError } = await supabase
      .from('orders')
      .select('*')
      .order('created_at', { ascending: false })
    
    if (ordersError) throw ordersError
    
    allOrders.value = orders || []
    
    // 计算统计数据
    calculateStats()
    
    // 获取最近5条订单
    recentOrders.value = (orders || []).slice(0, 5)
    
    // 加载店铺数据
    const shops = await adminStore.fetchShops()
    shopStats.value = shops.map(shop => ({
      ...shop,
      orderCount: (orders || []).filter(o => o.shop_id === shop.id).length
    }))
    
  } catch (err) {
    console.error('加载数据失败:', err)
    ElMessage.error('加载数据失败: ' + err.message)
  }
}

onMounted(() => {
  loadAllData()
})
</script>
