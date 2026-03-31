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
            <p class="text-sm text-slate-500">效果图下载中心</p>
          </div>
        </div>
        <div class="flex items-center gap-3">
          <button 
            @click="$router.push(`/store/${shopStore.currentShop?.code}/orders`)"
            class="text-sm text-slate-500 hover:text-slate-700"
          >
            返回订单
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
      <!-- 说明卡片 -->
      <div class="bg-blue-50 border border-blue-200 rounded-xl p-4 mb-6">
        <div class="flex items-start gap-3">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" class="mt-0.5">
            <circle cx="12" cy="12" r="10"/>
            <path d="M12 16v-4"/>
            <path d="M12 8h.01"/>
          </svg>
          <div>
            <p class="text-sm text-blue-800 font-medium">使用说明</p>
            <p class="text-sm text-blue-600 mt-1">
              1. 下载效果图后，登录您的ETSY店铺后台<br>
              2. 找到对应订单，通过消息将效果图发送给客户确认<br>
              3. 客户确认后，订单将自动进入生产环节
            </p>
          </div>
        </div>
      </div>

      <!-- 搜索栏 -->
      <div class="bg-white rounded-xl border border-slate-200 p-4 mb-6">
        <div class="flex gap-4 items-center flex-wrap">
          <div class="relative flex-1 min-w-[300px]">
            <input 
              v-model="searchQuery"
              type="text"
              placeholder="搜索订单号或客户名"
              class="pl-10 pr-4 py-2 border border-slate-200 rounded-lg text-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none w-full"
              @input="handleSearch"
            >
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400">
              <circle cx="11" cy="11" r="8"/>
              <path d="m21 21-4.3-4.3"/>
            </svg>
          </div>
          <button 
            @click="refreshEffects"
            class="px-4 py-2 bg-slate-100 text-slate-600 rounded-lg text-sm font-medium hover:bg-slate-200 flex items-center gap-2"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>
              <path d="M3 3v5h5"/>
              <path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"/>
              <path d="M16 16h5v5"/>
            </svg>
            刷新
          </button>
        </div>
      </div>

      <!-- 效果图列表 -->
      <div class="bg-white rounded-xl border border-slate-200 overflow-hidden">
        <div class="px-6 py-4 border-b border-slate-200 flex items-center justify-between">
          <h2 class="font-bold text-slate-800">效果图列表 ({{ filteredOrders.length }})</h2>
          <div class="flex gap-2">
            <button 
              @click="downloadAll"
              :disabled="filteredOrders.length === 0"
              class="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              批量下载
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
            <rect width="18" height="18" x="3" y="3" rx="2"/>
            <circle cx="9" cy="9" r="2"/>
            <path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>
          </svg>
          <p>暂无效果图</p>
          <p class="text-sm text-slate-400 mt-1">该店铺下没有生成效果图的订单</p>
        </div>
        
        <!-- 效果图网格 -->
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 p-6">
          <div v-for="order in paginatedOrders" :key="order.id" class="border border-slate-200 rounded-xl overflow-hidden hover:shadow-md transition-shadow group">
            <!-- 效果图预览 -->
            <div class="aspect-square bg-slate-100 flex items-center justify-center cursor-pointer relative" @click="previewImage(order)">
              <img 
                v-if="order.effect_image_url" 
                :src="order.effect_image_url" 
                class="w-full h-full object-contain" 
                alt="效果图"
                @error="handleImageError"
              >
              <div v-else class="text-center text-slate-400">
                <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="mx-auto mb-2">
                  <rect width="18" height="18" x="3" y="3" rx="2"/>
                  <circle cx="9" cy="9" r="2"/>
                  <path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>
                </svg>
                <p class="text-sm">无效果图</p>
              </div>
              <!-- 悬停遮罩 -->
              <div class="absolute inset-0 bg-black/50 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                <span class="text-white text-sm font-medium">点击查看大图</span>
              </div>
            </div>
            
            <!-- 订单信息 -->
            <div class="p-4">
              <div class="flex items-center justify-between mb-2">
                <span class="font-mono font-semibold text-slate-800 text-sm">{{ order.order_number }}</span>
                <span :class="getStatusClass(order.status)" class="px-2 py-0.5 text-xs rounded-full">
                  {{ getStatusText(order.status) }}
                </span>
              </div>
              <p class="text-sm text-slate-600 mb-1 truncate">{{ order.customer_name || '未知客户' }}</p>
              <p class="text-xs text-slate-400">{{ formatDate(order.created_at) }}</p>
              
              <!-- 操作按钮 -->
              <div class="flex gap-2 mt-3">
                <button 
                  @click="downloadEffect(order)"
                  :disabled="!order.effect_image_url"
                  class="flex-1 py-1.5 bg-blue-50 text-blue-600 rounded-lg text-xs font-medium hover:bg-blue-100 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-1"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="7 10 12 15 17 10"/>
                    <line x1="12" x2="12" y1="15" y2="3"/>
                  </svg>
                  下载
                </button>
                <button 
                  @click="copyOrderNumber(order.order_number)"
                  class="px-3 py-1.5 bg-slate-50 text-slate-600 rounded-lg text-xs font-medium hover:bg-slate-100"
                  title="复制订单号"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect width="14" height="14" x="8" y="8" rx="2" ry="2"/>
                    <path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 分页 -->
        <div v-if="filteredOrders.length > 0" class="px-6 py-4 border-t border-slate-200 flex items-center justify-between">
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
    </main>
    
    <!-- 图片预览弹窗 -->
    <div v-if="previewModal.show" class="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4" @click="previewModal.show = false">
      <div class="relative max-w-4xl max-h-[90vh] w-full">
        <button 
          @click="previewModal.show = false"
          class="absolute -top-10 right-0 text-white hover:text-slate-300"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M18 6 6 18"/>
            <path d="m6 6 12 12"/>
          </svg>
        </button>
        <img 
          v-if="previewModal.url" 
          :src="previewModal.url" 
          class="max-w-full max-h-[85vh] mx-auto rounded-lg"
          @click.stop
        >
      </div>
    </div>
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
const currentPage = ref(1)
const pageSize = 12
const previewModal = ref({ show: false, url: '' })

// 计算属性 - 筛选后的订单
const filteredOrders = computed(() => {
  let result = orders.value
  
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
watch([searchQuery], () => {
  currentPage.value = 1
})

// 加载效果图订单
const loadEffectOrders = async () => {
  loading.value = true
  try {
    orders.value = await shopStore.fetchShopEffectOrders(searchQuery.value)
  } catch (err) {
    console.error('加载效果图订单失败:', err)
    ElMessage.error('加载效果图失败')
  } finally {
    loading.value = false
  }
}

// 刷新
const refreshEffects = () => {
  loadEffectOrders()
  ElMessage.success('刷新成功')
}

// 搜索处理（防抖）
let searchTimeout = null
const handleSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    currentPage.value = 1
    loadEffectOrders()
  }, 500)
}

// 退出登录
const handleLogout = () => {
  shopStore.logout()
  router.push('/store/login')
  ElMessage.success('已退出登录')
}

// 预览图片
const previewImage = (order) => {
  if (order.effect_image_url) {
    previewModal.value = { show: true, url: order.effect_image_url }
  }
}

// 处理图片加载错误
const handleImageError = (e) => {
  e.target.style.display = 'none'
  e.target.nextElementSibling.style.display = 'flex'
}

// 下载效果图
function downloadEffect(order) {
  if (!order.effect_image_url) {
    ElMessage.warning('该订单暂无效果图')
    return
  }
  
  const link = document.createElement('a')
  link.href = order.effect_image_url
  // 根据URL后缀判断文件类型
  const ext = order.effect_image_url.split('.').pop() || 'svg'
  link.download = `effect_${order.order_number}.${ext}`
  link.target = '_blank'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  
  ElMessage.success('开始下载效果图')
}

// 批量下载
async function downloadAll() {
  if (filteredOrders.value.length === 0) return
  
  const ordersWithEffect = filteredOrders.value.filter(o => o.effect_image_url)
  if (ordersWithEffect.length === 0) {
    ElMessage.warning('没有可下载的效果图')
    return
  }
  
  ElMessage.info(`开始批量下载 ${ordersWithEffect.length} 个效果图`)
  
  // 逐个下载，添加延迟避免浏览器阻止
  for (let i = 0; i < ordersWithEffect.length; i++) {
    const order = ordersWithEffect[i]
    setTimeout(() => {
      downloadEffect(order)
    }, i * 500)
  }
}

// 复制订单号
const copyOrderNumber = (orderNumber) => {
  navigator.clipboard.writeText(orderNumber).then(() => {
    ElMessage.success('订单号已复制')
  }).catch(() => {
    ElMessage.error('复制失败')
  })
}

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
  return `${date.getFullYear()}/${(date.getMonth() + 1).toString().padStart(2, '0')}/${date.getDate().toString().padStart(2, '0')}`
}

// 初始化
onMounted(() => {
  loadEffectOrders()
})
</script>