<template>
  <div class="h-full overflow-auto bg-slate-50 p-4">
    <!-- 页面标题 -->
    <div class="mb-4 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-slate-800">工厂生产总览</h1>
        <p class="text-sm text-slate-500 mt-1">实时监控各工厂生产进度与订单状态</p>
      </div>
      <div class="flex items-center gap-2">
        <button class="bg-white border border-slate-200 hover:bg-slate-50 text-slate-600 px-4 py-2 rounded-lg text-sm font-medium flex items-center gap-2 transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8"/>
            <path d="M21 3v5h-5"/>
          </svg>
          刷新
        </button>
        <button class="bg-white border border-slate-200 hover:bg-slate-50 text-slate-600 px-4 py-2 rounded-lg text-sm font-medium flex items-center gap-2 transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="7 10 12 15 17 10"/>
            <line x1="12" x2="12" y1="15" y2="3"/>
          </svg>
          导出
        </button>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="grid grid-cols-4 gap-4 mb-4">
      <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-4">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2">
              <path d="m15 12-9.373 9.373a1 1 0 0 1-3.001-3L12 9"/>
              <path d="M18 15l4-4"/>
              <path d="m21.5 11.5-1.914-1.914A2 2 0 0 1 19 8.172v-.344a2 2 0 0 0-.586-1.414l-1.657-1.657A6 6 0 0 0 12.516 3H9l1.243 1.243A6 6 0 0 1 12 8.485V10l2 2h1.172a2 2 0 0 1 1.414.586L18.5 14.5"/>
            </svg>
          </div>
          <div>
            <p class="text-2xl font-bold text-slate-800">{{ stats.producing }}</p>
            <p class="text-xs text-slate-500">生产中</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-4">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2">
              <path d="M21.801 10A10 10 0 1 1 17 3.335"/>
              <path d="m9 11 3 3L22 4"/>
            </svg>
          </div>
          <div>
            <p class="text-2xl font-bold text-slate-800">{{ stats.todayCompleted }}</p>
            <p class="text-xs text-slate-500">今日完成</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-4">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#dc2626" stroke-width="2">
              <path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
              <line x1="12" x2="12" y1="9" y2="13"/>
              <line x1="12" x2="12.01" y1="17" y2="17"/>
            </svg>
          </div>
          <div>
            <p class="text-2xl font-bold text-red-600">{{ stats.overdue }}</p>
            <p class="text-xs text-slate-500">⚠️ 逾期</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-4">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-orange-100 rounded-lg flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ea580c" stroke-width="2">
              <path d="M5 18H3c-.6 0-1-.4-1-1V7c0-.6.4-1 1-1h10c.6 0 1 .4 1 1v11"/>
              <path d="M14 9h4l4 4v6h-4"/>
              <circle cx="7" cy="18" r="2"/>
              <circle cx="17" cy="18" r="2"/>
            </svg>
          </div>
          <div>
            <p class="text-2xl font-bold text-slate-800">{{ stats.waitingPickup }}</p>
            <p class="text-xs text-slate-500">待揽件</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 筛选栏 -->
    <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-4 mb-4">
      <div class="flex items-center gap-4">
        <div class="flex items-center gap-2">
          <span class="text-sm text-slate-500">工厂:</span>
          <select v-model="filters.factory" class="px-3 py-1.5 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500">
            <option value="all">全部</option>
            <option value="工厂A">工厂A</option>
            <option value="工厂B">工厂B</option>
          </select>
        </div>
        <div class="flex items-center gap-2">
          <span class="text-sm text-slate-500">状态:</span>
          <select v-model="filters.status" class="px-3 py-1.5 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500">
            <option value="all">全部</option>
            <option value="生产中">生产中</option>
            <option value="已完成">已完成</option>
            <option value="逾期">逾期</option>
            <option value="待揽件">待揽件</option>
          </select>
        </div>
        <div class="flex items-center gap-2">
          <span class="text-sm text-slate-500">日期范围:</span>
          <input v-model="filters.startDate" type="date" class="px-3 py-1.5 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500" />
          <span class="text-slate-400">~</span>
          <input v-model="filters.endDate" type="date" class="px-3 py-1.5 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500" />
        </div>
      </div>
    </div>

    <!-- 生产订单列表 -->
    <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden mb-4">
      <div class="px-4 py-3 border-b border-slate-100 flex items-center justify-between">
        <h2 class="text-base font-bold text-slate-800">生产订单列表</h2>
        <span class="bg-blue-100 text-blue-600 px-2 py-0.5 rounded-full text-xs font-bold">{{ filteredOrders.length }}条</span>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-xs text-left">
          <thead class="bg-slate-50 text-slate-500 font-medium border-b border-slate-200">
            <tr class="h-[40px]">
              <th class="px-4 whitespace-nowrap font-medium">订单号</th>
              <th class="px-4 whitespace-nowrap font-medium">SKU</th>
              <th class="px-4 whitespace-nowrap font-medium">形状</th>
              <th class="px-4 whitespace-nowrap font-medium">尺寸</th>
              <th class="px-4 whitespace-nowrap font-medium">工艺</th>
              <th class="px-4 whitespace-nowrap font-medium">工厂</th>
              <th class="px-4 whitespace-nowrap font-medium">下单时间</th>
              <th class="px-4 whitespace-nowrap font-medium">交货时间</th>
              <th class="px-4 whitespace-nowrap font-medium">状态</th>
              <th class="px-4 whitespace-nowrap font-medium">生产文档</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr 
              v-for="order in filteredOrders" 
              :key="order.id" 
              :class="[
                'h-[48px] transition-colors',
                order.status === '逾期' ? 'bg-red-50 border-l-4 border-red-500' : 'hover:bg-slate-50'
              ]"
            >
              <td class="px-4 whitespace-nowrap font-medium text-slate-700">{{ order.etsy_order_id }}</td>
              <td class="px-4 whitespace-nowrap font-mono text-slate-500">{{ order.sku_mappings?.sku_code || '-' }}</td>
              <td class="px-4 whitespace-nowrap text-slate-600">{{ order.sku_mappings?.shape || order.product_shape || '-' }}</td>
              <td class="px-4 whitespace-nowrap text-slate-600">{{ order.sku_mappings?.size || order.product_size || '-' }}</td>
              <td class="px-4 whitespace-nowrap text-slate-600">{{ order.sku_mappings?.craft || '-' }}</td>
              <td class="px-4 whitespace-nowrap text-slate-600">-</td>
              <td class="px-4 whitespace-nowrap text-slate-500">{{ formatDate(order.created_at) }}</td>
              <td class="px-4 whitespace-nowrap text-slate-500">-</td>
              <td class="px-4 whitespace-nowrap">
                <span :class="getStatusClass('生产中')">生产中</span>
              </td>
              <td class="px-4 whitespace-nowrap">
                <button v-if="order.production_pdf_url" @click="viewPdf(order)" class="text-blue-600 hover:text-blue-800 font-medium flex items-center gap-1 text-xs">
                  <span>📄</span>PDF
                </button>
                <button v-else @click="generatePdf(order)" :disabled="generatingId === order.id" class="text-orange-500 hover:text-orange-700 font-medium flex items-center gap-1 text-xs disabled:opacity-50">
                  <span>{{ generatingId === order.id ? '生成中...' : '生成PDF' }}</span>
                </button>
              </td>
            </tr>
            <tr v-if="filteredOrders.length === 0" class="h-[60px]">
              <td colspan="10" class="px-4 text-center text-slate-400 text-sm">暂无订单数据</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 工厂工作量汇总 -->
    <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-4">
      <h2 class="text-base font-bold text-slate-800 mb-3">工厂工作量汇总</h2>
      <div class="space-y-2">
        <div v-for="factory in factorySummary" :key="factory.name" class="flex items-center gap-6 py-2 px-4 bg-slate-50 rounded-lg">
          <span class="font-bold text-slate-700 w-20">{{ factory.name }}:</span>
          <span class="text-sm">
            <span class="text-blue-600 font-medium">生产中 {{ factory.producing }}</span>
            <span class="mx-2 text-slate-300">|</span>
            <span class="text-green-600 font-medium">完成 {{ factory.completed }}</span>
            <span class="mx-2 text-slate-300">|</span>
            <span class="text-red-600 font-medium">逾期 {{ factory.overdue }}</span>
            <span class="mx-2 text-slate-300">|</span>
            <span class="text-orange-600 font-medium">待揽件 {{ factory.waitingPickup }}</span>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted } from 'vue'
import supabase from '../../utils/supabase'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const realOrders = ref([])
const loading = ref(false)
const generatingId = ref(null)

onMounted(() => loadOrders())

async function loadOrders() {
  loading.value = true
  try {
    const { data, error } = await supabase
      .from('orders')
      .select(`*, sku_mappings:sku_mapping(*), logistics(*)`)
      .eq('status', 'producing')
      .order('created_at', { ascending: false })
    if (error) throw error
    realOrders.value = data || []
    console.log(`✅ 工厂生产总览加载: ${realOrders.value.length} 条`)
  } catch (e) {
    console.error('❌ 加载失败:', e)
  } finally {
    loading.value = false
  }
}

// 筛选条件
const filters = reactive({
  factory: 'all',
  status: 'all',
  startDate: '',
  endDate: '',
})

// 统计数据
const stats = computed(() => ({
  producing: realOrders.value.length,
  todayCompleted: 0,
  overdue: 0,
  waitingPickup: 0,
}))

// 展示订单列表
const filteredOrders = computed(() => realOrders.value)

// 工厂汇总（未分配工厂时不展示）
const factorySummary = computed(() => [])

async function generatePdf(order) {
  generatingId.value = order.id
  try {
    const res = await fetch(`${API_BASE_URL}/api/pdf/generate-and-upload`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ order_id: order.id })
    })
    const data = await res.json()
    if (data.success) {
      const idx = realOrders.value.findIndex(o => o.id === order.id)
      if (idx !== -1) realOrders.value[idx] = { ...realOrders.value[idx], production_pdf_url: data.production_pdf_url }
    } else {
      alert('❌ 生成失败: ' + (data.detail || data.message || '未知错误'))
    }
  } catch (e) {
    alert('❌ 网络错误: ' + e.message)
  } finally {
    generatingId.value = null
  }
}

function viewPdf(order) {
  if (order.production_pdf_url) window.open(order.production_pdf_url, '_blank')
}

function formatDate(str) {
  if (!str) return '-'
  const d = new Date(str)
  return `${d.getMonth() + 1}/${d.getDate()} ${d.getHours()}:${String(d.getMinutes()).padStart(2, '0')}`
}

// 状态样式
const getStatusClass = (status) => {
  const classes = {
    '生产中': 'bg-blue-100 text-blue-600 px-2 py-0.5 rounded text-[10px] font-bold',
    '已完成': 'bg-green-100 text-green-600 px-2 py-0.5 rounded text-[10px] font-bold',
    '逾期': 'bg-red-100 text-red-600 px-2 py-0.5 rounded text-[10px] font-bold',
    '待揓件': 'bg-orange-100 text-orange-600 px-2 py-0.5 rounded text-[10px] font-bold',
  }
  return classes[status] || 'bg-slate-100 text-slate-600 px-2 py-0.5 rounded text-[10px] font-bold'
}

const getStatusText = (status) => {
  if (status === '逾期') return '🔴逾期-须跟进'
  return status
}
</script>

