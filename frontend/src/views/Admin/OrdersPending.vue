<template>
  <div class="p-8">
    <!-- 页面标题 -->
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-slate-800">待确认订单</h1>
      <p class="text-slate-500">处理新订单，生成效果图和确认邮件</p>
    </div>

    <!-- 统计标签 -->
    <div class="flex gap-3 mb-6">
      <button 
        @click="currentFilter = 'all'"
        :class="[currentFilter === 'all' ? 'bg-slate-800 text-white' : 'bg-white text-slate-700 border border-slate-200']"
        class="px-4 py-2 rounded-lg text-sm font-medium transition-colors"
      >
        全部 {{ orders.length }}
      </button>
      <button 
        @click="currentFilter = 'new'"
        :class="[currentFilter === 'new' ? 'bg-orange-500 text-white' : 'bg-white text-slate-700 border border-slate-200']"
        class="px-4 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-2"
      >
        <span class="w-2 h-2 bg-orange-400 rounded-full"></span>
        新到未处理 {{ newOrdersCount }}
      </button>
      <button 
        @click="currentFilter = 'waiting'"
        :class="[currentFilter === 'waiting' ? 'bg-blue-500 text-white' : 'bg-white text-slate-700 border border-slate-200']"
        class="px-4 py-2 rounded-lg text-sm font-medium transition-colors"
      >
        等待客户确认 {{ waitingOrdersCount }}
      </button>
    </div>

    <!-- 搜索栏 -->
    <div class="bg-white rounded-xl border border-slate-200 p-4 mb-6">
      <div class="flex gap-4">
        <div class="relative flex-1 max-w-md">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400">
            <circle cx="11" cy="11" r="8"/>
            <path d="m21 21-4.34-4.34"/>
          </svg>
          <input 
            v-model="searchQuery"
            type="search" 
            placeholder="搜索订单号、客户名称或产品..."
            class="w-full pl-10 pr-4 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:border-blue-500"
          >
        </div>
        <select v-model="filterShop" class="px-4 py-2 border border-slate-200 rounded-lg text-sm">
          <option value="">全部店铺</option>
          <option v-for="shop in shops" :key="shop.id" :value="shop.id">{{ shop.name }}</option>
        </select>
      </div>
    </div>

    <!-- 订单表格 -->
    <div class="bg-white rounded-xl border border-slate-200 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full min-w-[1000px]">
          <thead class="bg-slate-50">
            <tr>
              <th class="text-left py-3 px-4 text-xs font-medium text-slate-500 uppercase tracking-wider">订单ID</th>
              <th class="text-left py-3 px-4 text-xs font-medium text-slate-500 uppercase tracking-wider">客户名称</th>
              <th class="text-left py-3 px-4 text-xs font-medium text-slate-500 uppercase tracking-wider">产品</th>
              <th class="text-left py-3 px-4 text-xs font-medium text-slate-500 uppercase tracking-wider">设计稿件</th>
              <th class="text-left py-3 px-4 text-xs font-medium text-slate-500 uppercase tracking-wider">确认邮件</th>
              <th class="text-left py-3 px-4 text-xs font-medium text-slate-500 uppercase tracking-wider">数量</th>
              <th class="text-left py-3 px-4 text-xs font-medium text-slate-500 uppercase tracking-wider">状态</th>
              <th class="text-left py-3 px-4 text-xs font-medium text-slate-500 uppercase tracking-wider">创建日期</th>
              <th class="text-left py-3 px-4 text-xs font-medium text-slate-500 uppercase tracking-wider">操作</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr v-for="order in filteredOrders" :key="order.id" class="hover:bg-slate-50">
              <td class="py-4 px-4 font-mono text-sm font-medium">{{ order.etsy_order_id }}</td>
              <td class="py-4 px-4 text-sm text-slate-600">{{ order.customer_name }}</td>
              <td class="py-4 px-4 text-sm text-slate-600">{{ order.sku_code }}</td>
              <td class="py-4 px-4">
                <button 
                  v-if="!order.effect_image_url"
                  @click="generateEffect(order)"
                  class="inline-flex items-center gap-1 px-3 py-1.5 text-xs border border-slate-200 rounded-lg hover:bg-slate-50 transition-colors"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect width="18" height="18" x="3" y="3" rx="2"/>
                    <circle cx="9" cy="9" r="2"/>
                    <path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>
                  </svg>
                  生成效果图
                </button>
                <div v-else class="flex items-center gap-2">
                  <button class="inline-flex items-center gap-1 px-3 py-1.5 text-xs border border-slate-200 rounded-lg hover:bg-slate-50">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0"/>
                      <circle cx="12" cy="12" r="3"/>
                    </svg>
                    查看
                  </button>
                  <button class="inline-flex items-center gap-1 px-2 py-1.5 text-xs text-slate-400 hover:text-slate-600">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M12 15V3"/>
                      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                      <path d="m7 10 5 5 5-5"/>
                    </svg>
                  </button>
                </div>
              </td>
              <td class="py-4 px-4">
                <button 
                  v-if="!order.confirm_email_sent"
                  @click="generateEmail(order)"
                  class="inline-flex items-center gap-1 px-3 py-1.5 text-xs border border-slate-200 rounded-lg hover:bg-slate-50 transition-colors"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="m22 7-8.991 5.727a2 2 0 0 1-2.009 0L2 7"/>
                    <rect x="2" y="4" width="20" height="16" rx="2"/>
                  </svg>
                  生成邮件
                </button>
                <button v-else class="inline-flex items-center gap-1 px-3 py-1.5 text-xs border border-slate-200 rounded-lg hover:bg-slate-50">
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M6 22a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.704.706l3.588 3.588A2.4 2.4 0 0 1 20 8v12a2 2 0 0 1-2 2z"/>
                    <path d="M14 2v5a1 1 0 0 0 1 1h5"/>
                    <path d="M10 9H8"/>
                    <path d="M16 13H8"/>
                    <path d="M16 17H8"/>
                  </svg>
                  查看
                </button>
              </td>
              <td class="py-4 px-4 text-sm">{{ order.quantity }}</td>
              <td class="py-4 px-4">
                <span :class="getStatusClass(order.status)" class="px-2.5 py-1 rounded-full text-xs font-medium">
                  {{ getStatusText(order.status) }}
                </span>
              </td>
              <td class="py-4 px-4 text-sm text-slate-500">{{ formatDate(order.created_at) }}</td>
              <td class="py-4 px-4">
                <button 
                  @click="createOrder(order)"
                  class="px-3 py-1.5 text-xs bg-slate-800 text-white rounded-lg hover:bg-slate-700 transition-colors"
                >
                  创建订单
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAdminStore } from '../../stores/adminStore'

const adminStore = useAdminStore()

// 状态
const orders = ref([])
const shops = ref([])
const searchQuery = ref('')
const filterShop = ref('')
const currentFilter = ref('all')

// 计算属性
const newOrdersCount = computed(() => orders.value.filter(o => o.status === 'new').length)
const waitingOrdersCount = computed(() => orders.value.filter(o => o.status === 'pending').length)

const filteredOrders = computed(() => {
  let result = orders.value
  
  // 状态筛选
  if (currentFilter.value === 'new') {
    result = result.filter(o => o.status === 'new')
  } else if (currentFilter.value === 'waiting') {
    result = result.filter(o => o.status === 'pending')
  }
  
  // 店铺筛选
  if (filterShop.value) {
    result = result.filter(o => o.shop_id === filterShop.value)
  }
  
  // 搜索筛选
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(o => 
      o.etsy_order_id?.toLowerCase().includes(query) ||
      o.customer_name?.toLowerCase().includes(query) ||
      o.sku_code?.toLowerCase().includes(query)
    )
  }
  
  return result
})

// 方法
function getStatusClass(status) {
  const map = {
    'new': 'bg-slate-100 text-slate-700 border border-slate-200',
    'pending': 'bg-orange-100 text-orange-700 border border-orange-200',
    'confirmed': 'bg-blue-100 text-blue-700 border border-blue-200'
  }
  return map[status] || 'bg-slate-100 text-slate-600'
}

function getStatusText(status) {
  const map = {
    'new': '新订单',
    'pending': '待确认',
    'confirmed': '已确认'
  }
  return map[status] || status
}

function formatDate(date) {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('zh-CN')
}

function generateEffect(order) {
  console.log('生成效果图:', order.id)
  // 实际应调用API生成效果图
}

function generateEmail(order) {
  console.log('生成邮件:', order.id)
  // 实际应调用API生成邮件
}

function createOrder(order) {
  console.log('创建订单:', order.id)
  // 实际应调用API创建生产订单
}

// 加载数据
onMounted(async () => {
  // 模拟数据
  orders.value = [
    {
      id: '1',
      etsy_order_id: '#PO-202602-001',
      customer_name: 'Maura McHale',
      sku_code: 'B-E01A',
      quantity: 200,
      status: 'new',
      created_at: '2026-02-03',
      shop_id: '1',
      effect_image_url: null,
      confirm_email_sent: false
    },
    {
      id: '2',
      etsy_order_id: '#PO-202602-002',
      customer_name: 'Kim Alison',
      sku_code: 'B-G01B',
      quantity: 1,
      status: 'pending',
      created_at: '2026-02-01',
      shop_id: '1',
      effect_image_url: '/effects/001.png',
      confirm_email_sent: true
    }
  ]
  
  shops.value = [
    { id: '1', name: '美国店铺' },
    { id: '2', name: '欧洲店铺' },
    { id: '3', name: '亚洲店铺' }
  ]
})
</script>
