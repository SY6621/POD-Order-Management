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
              <td class="px-4 whitespace-nowrap font-medium text-slate-700">{{ order.id }}</td>
              <td class="px-4 whitespace-nowrap font-mono text-slate-500">{{ order.sku }}</td>
              <td class="px-4 whitespace-nowrap text-slate-600">{{ order.shape }}</td>
              <td class="px-4 whitespace-nowrap text-slate-600">{{ order.size }}</td>
              <td class="px-4 whitespace-nowrap text-slate-600">{{ order.craft }}</td>
              <td class="px-4 whitespace-nowrap text-slate-600">{{ order.factory }}</td>
              <td class="px-4 whitespace-nowrap text-slate-500">{{ order.orderDate }}</td>
              <td class="px-4 whitespace-nowrap text-slate-500">{{ order.dueDate }}</td>
              <td class="px-4 whitespace-nowrap">
                <span :class="getStatusClass(order.status)">
                  {{ getStatusText(order.status) }}
                </span>
              </td>
              <td class="px-4 whitespace-nowrap">
                <button v-if="order.hasPdf" class="text-blue-600 hover:text-blue-800 font-medium flex items-center gap-1">
                  <span>📄</span>PDF
                </button>
                <span v-else class="text-slate-400">-</span>
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
import { ref, computed, reactive } from 'vue'

// 假数据
const mockOrders = ref([
  { id: '4002217518', sku: 'B-HC-G-L', shape: '心形', size: '大号', craft: '金色', factory: '工厂A', orderDate: '03-15', dueDate: '03-18', status: '生产中', hasPdf: true },
  { id: '4002217519', sku: 'B-BO-S-S', shape: '骨头', size: '小号', craft: '银色', factory: '工厂B', orderDate: '03-14', dueDate: '03-17', status: '逾期', hasPdf: true },
  { id: '4002217520', sku: 'B-CI-G-L', shape: '圆形', size: '大号', craft: '金色', factory: '工厂A', orderDate: '03-16', dueDate: '03-19', status: '待揽件', hasPdf: true },
  { id: '4002217521', sku: 'B-HC-S-S', shape: '心形', size: '小号', craft: '银色', factory: '工厂A', orderDate: '03-15', dueDate: '03-18', status: '已完成', hasPdf: true },
  { id: '4002217522', sku: 'B-BO-G-L', shape: '骨头', size: '大号', craft: '金色', factory: '工厂B', orderDate: '03-13', dueDate: '03-16', status: '逾期', hasPdf: true },
  { id: '4002217523', sku: 'B-CI-S-S', shape: '圆形', size: '小号', craft: '银色', factory: '工厂A', orderDate: '03-16', dueDate: '03-19', status: '生产中', hasPdf: true },
  { id: '4002217524', sku: 'B-HC-G-L', shape: '心形', size: '大号', craft: '金色', factory: '工厂B', orderDate: '03-15', dueDate: '03-18', status: '生产中', hasPdf: true },
  { id: '4002217525', sku: 'B-BO-S-S', shape: '骨头', size: '小号', craft: '银色', factory: '工厂A', orderDate: '03-16', dueDate: '03-20', status: '待揽件', hasPdf: true },
  { id: '4002217526', sku: 'B-CI-G-L', shape: '圆形', size: '大号', craft: '金色', factory: '工厂B', orderDate: '03-17', dueDate: '03-20', status: '生产中', hasPdf: false },
  { id: '4002217527', sku: 'B-HC-S-S', shape: '心形', size: '小号', craft: '银色', factory: '工厂A', orderDate: '03-17', dueDate: '03-21', status: '生产中', hasPdf: true },
])

// 筛选条件
const filters = reactive({
  factory: 'all',
  status: 'all',
  startDate: '',
  endDate: '',
})

// 统计数据
const stats = computed(() => ({
  producing: mockOrders.value.filter(o => o.status === '生产中').length,
  todayCompleted: mockOrders.value.filter(o => o.status === '已完成').length,
  overdue: mockOrders.value.filter(o => o.status === '逾期').length,
  waitingPickup: mockOrders.value.filter(o => o.status === '待揽件').length,
}))

// 筛选后的订单
const filteredOrders = computed(() => {
  return mockOrders.value.filter(order => {
    if (filters.factory !== 'all' && order.factory !== filters.factory) return false
    if (filters.status !== 'all' && order.status !== filters.status) return false
    return true
  })
})

// 工厂汇总
const factorySummary = computed(() => {
  const factories = ['工厂A', '工厂B']
  return factories.map(name => {
    const orders = mockOrders.value.filter(o => o.factory === name)
    return {
      name,
      producing: orders.filter(o => o.status === '生产中').length,
      completed: orders.filter(o => o.status === '已完成').length,
      overdue: orders.filter(o => o.status === '逾期').length,
      waitingPickup: orders.filter(o => o.status === '待揽件').length,
    }
  })
})

// 状态样式
const getStatusClass = (status) => {
  const classes = {
    '生产中': 'bg-blue-100 text-blue-600 px-2 py-0.5 rounded text-[10px] font-bold',
    '已完成': 'bg-green-100 text-green-600 px-2 py-0.5 rounded text-[10px] font-bold',
    '逾期': 'bg-red-100 text-red-600 px-2 py-0.5 rounded text-[10px] font-bold',
    '待揽件': 'bg-orange-100 text-orange-600 px-2 py-0.5 rounded text-[10px] font-bold',
  }
  return classes[status] || 'bg-slate-100 text-slate-600 px-2 py-0.5 rounded text-[10px] font-bold'
}

const getStatusText = (status) => {
  if (status === '逾期') return '🔴逾期-须跟进'
  return status
}
</script>
