<template>
  <div class="h-full overflow-auto bg-slate-50 p-4">
    <!-- 页面标题 -->
    <div class="mb-4 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-slate-800">已完成订单</h1>
        <p class="text-sm text-slate-500 mt-1">管理已完成订单、追踪物流并发送追评邮件</p>
      </div>
      <div class="text-sm text-slate-600">
        总计: <span class="font-bold text-slate-800">{{ totalCount }} 笔</span>
      </div>
    </div>

    <!-- 搜索/筛选栏 -->
    <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-4 mb-4">
      <div class="flex flex-wrap items-center gap-3">
        <!-- 搜索框 -->
        <div class="flex-1 min-w-[200px]">
          <input 
            v-model="searchText" 
            type="text" 
            placeholder="搜索订单号/客户名..."
            class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
          />
        </div>
        <!-- 日期范围 -->
        <div class="flex items-center gap-2">
          <input 
            v-model="dateStart" 
            type="date" 
            class="px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
          />
          <span class="text-slate-400">至</span>
          <input 
            v-model="dateEnd" 
            type="date" 
            class="px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
          />
        </div>
        <!-- 店铺筛选 -->
        <select v-model="shopFilter" class="px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500">
          <option value="">全部店铺</option>
          <option value="us">美国店铺</option>
          <option value="eu">欧洲店铺</option>
          <option value="asia">亚洲店铺</option>
        </select>
        <!-- 产品筛选 -->
        <select v-model="productFilter" class="px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500">
          <option value="">全部产品</option>
          <option value="HC">心形</option>
          <option value="BO">骨头形</option>
          <option value="CI">圆形</option>
        </select>
        <!-- 按钮 -->
        <button @click="handleSearch" class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium transition-colors">
          搜索
        </button>
        <button @click="handleReset" class="px-4 py-2 bg-white border border-slate-200 hover:bg-slate-50 text-slate-600 rounded-lg text-sm font-medium transition-colors">
          重置
        </button>
      </div>
    </div>

    <!-- 订单列表表格 -->
    <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm text-left">
          <thead class="bg-slate-50 text-slate-600 font-medium border-b border-slate-200">
            <tr class="h-[44px]">
              <th class="px-4 whitespace-nowrap font-medium">订单号</th>
              <th class="px-4 whitespace-nowrap font-medium">客户</th>
              <th class="px-4 whitespace-nowrap font-medium">SKU</th>
              <th class="px-4 whitespace-nowrap font-medium">完成日期</th>
              <th class="px-4 whitespace-nowrap font-medium">发货日期</th>
              <th class="px-4 whitespace-nowrap font-medium">物流单号</th>
              <th class="px-4 whitespace-nowrap font-medium">已交货天数</th>
              <th class="px-4 whitespace-nowrap font-medium">生产文档</th>
              <th class="px-4 whitespace-nowrap font-medium">追评状态</th>
              <th class="px-4 whitespace-nowrap font-medium">操作</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <template v-for="order in paginatedOrders" :key="order.id">
              <!-- 主行 -->
              <tr 
                @click="toggleExpand(order.id)"
                :class="[
                  'transition-colors cursor-pointer',
                  expandedId === order.id ? 'bg-slate-50' : 'hover:bg-slate-50',
                  getRowBorderClass(order)
                ]"
              >
                <td class="px-4 py-3 whitespace-nowrap font-medium text-slate-700">{{ order.etsy_order_id || order.id }}</td>
                <td class="px-4 py-3 whitespace-nowrap text-slate-600">{{ order.customer_name }}</td>
                <td class="px-4 py-3 whitespace-nowrap font-mono text-slate-500 text-xs">{{ order.sku_mapping?.sku_code || '-' }}</td>
                <td class="px-4 py-3 whitespace-nowrap text-slate-500">{{ formatDate(order.completed_at || order.created_at) }}</td>
                <td class="px-4 py-3 whitespace-nowrap text-slate-500">{{ formatDate(order.shipped_at) || '-' }}</td>
                <td class="px-4 py-3 whitespace-nowrap font-mono text-xs text-slate-500">{{ order.tracking_number || '-' }}</td>
                <td class="px-4 py-3 whitespace-nowrap">
                  <span class="text-slate-600">-</span>
                </td>
                <td class="px-4 py-3 whitespace-nowrap">
                  <a v-if="order.production_pdf_url" href="#" @click.stop.prevent="viewPdf(order)" class="text-blue-600 hover:text-blue-700 flex items-center gap-1">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                    查看PDF
                  </a>
                  <span v-else class="text-red-500 flex items-center gap-1">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" x2="12" y1="9" y2="13"/><line x1="12" x2="12.01" y1="17" y2="17"/></svg>
                    生产文档缺失
                  </span>
                </td>
                <td class="px-4 py-3 whitespace-nowrap">
                  <span :class="getReviewStatusClass(order)">{{ getReviewStatusText(order) }}</span>
                </td>
                <td class="px-4 py-3 whitespace-nowrap">
                  <button 
                    v-if="!order.reviewSent && order.deliveredDays >= 8"
                    @click.stop="sendReviewEmail(order)"
                    class="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded text-xs font-medium transition-colors"
                  >
                    发送追评邮件
                  </button>
                  <button 
                    v-else-if="order.reviewSent"
                    disabled
                    class="px-3 py-1.5 bg-slate-100 text-slate-400 rounded text-xs font-medium cursor-not-allowed"
                  >
                    已发送 ✓
                  </button>
                  <button 
                    v-else
                    disabled
                    class="px-3 py-1.5 bg-slate-100 text-slate-400 rounded text-xs font-medium cursor-not-allowed"
                  >
                    发送追评邮件
                  </button>
                </td>
              </tr>
              <!-- 展开详情行 -->
              <tr v-if="expandedId === order.id">
                <td colspan="10" class="p-0">
                  <div class="bg-slate-50 p-4 border-t border-slate-200 transition-all">
                    <div class="grid grid-cols-2 gap-6">
                      <!-- 左侧：订单详情 -->
                      <div>
                        <h4 class="font-bold text-slate-700 mb-3 text-sm">完整订单信息</h4>
                        <div class="grid grid-cols-2 gap-3 text-sm">
                          <div class="flex justify-between bg-white rounded-lg p-2">
                            <span class="text-slate-400">正面文字:</span>
                            <span class="text-slate-700 font-medium">{{ order.frontText }}</span>
                          </div>
                          <div class="flex justify-between bg-white rounded-lg p-2">
                            <span class="text-slate-400">字体:</span>
                            <span class="text-slate-700 font-medium">{{ order.font }}</span>
                          </div>
                          <div class="flex justify-between bg-white rounded-lg p-2">
                            <span class="text-slate-400">背面文字:</span>
                            <span class="text-slate-700 font-medium">{{ order.backText }}</span>
                          </div>
                          <div class="flex justify-between bg-white rounded-lg p-2">
                            <span class="text-slate-400">形状:</span>
                            <span class="text-slate-700 font-medium">{{ order.shape }}</span>
                          </div>
                          <div class="flex justify-between bg-white rounded-lg p-2">
                            <span class="text-slate-400">颜色:</span>
                            <span class="text-slate-700 font-medium">{{ order.color }}</span>
                          </div>
                          <div class="flex justify-between bg-white rounded-lg p-2">
                            <span class="text-slate-400">尺寸:</span>
                            <span class="text-slate-700 font-medium">{{ order.size }}</span>
                          </div>
                          <div class="flex justify-between bg-white rounded-lg p-2">
                            <span class="text-slate-400">工艺:</span>
                            <span class="text-slate-700 font-medium">{{ order.craft }}</span>
                          </div>
                        </div>
                      </div>
                      <!-- 右侧：生产文档预览 -->
                      <div>
                        <h4 class="font-bold text-slate-700 mb-3 text-sm">生产文档预览</h4>
                        <div v-if="order.production_pdf_url" class="bg-white rounded-lg border border-slate-200 p-4">
                          <div class="bg-slate-100 rounded-lg h-32 flex items-center justify-center mb-3">
                            <div class="text-center text-slate-500">
                              <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="mx-auto mb-2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                              <p class="text-xs">POD_{{ order.etsy_order_id || order.id }}.pdf</p>
                            </div>
                          </div>
                          <div class="flex gap-2">
                            <button @click.stop="viewPdf(order)" class="flex-1 px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded text-xs font-medium flex items-center justify-center gap-1 transition-colors">
                              <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                              查看
                            </button>
                            <button @click.stop="downloadPdf(order)" class="flex-1 px-3 py-1.5 bg-slate-700 hover:bg-slate-800 text-white rounded text-xs font-medium flex items-center justify-center gap-1 transition-colors">
                              <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>
                              下载
                            </button>
                            <button @click.stop="printPdf(order)" class="flex-1 px-3 py-1.5 bg-white border border-slate-200 hover:bg-slate-50 text-slate-600 rounded text-xs font-medium flex items-center justify-center gap-1 transition-colors">
                              <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect width="12" height="8" x="6" y="14"/></svg>
                              打印
                            </button>
                          </div>
                        </div>
                        <div v-else class="bg-red-50 rounded-lg border border-red-200 p-4 text-center">
                          <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="1.5" class="mx-auto mb-2"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" x2="12" y1="9" y2="13"/><line x1="12" x2="12.01" y1="17" y2="17"/></svg>
                          <p class="text-red-600 font-medium text-sm">生产文档缺失</p>
                          <p class="text-red-500 text-xs mt-1">请联系生产部门补充文档</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </td>
              </tr>
            </template>
            <tr v-if="paginatedOrders.length === 0" class="h-[100px]">
              <td colspan="10" class="px-4 text-center text-slate-400">暂无已完成订单</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 分页 -->
      <div class="px-4 py-3 border-t border-slate-200 flex items-center justify-between">
        <div class="text-sm text-slate-500">
          显示 {{ (currentPage - 1) * pageSize + 1 }} - {{ Math.min(currentPage * pageSize, filteredOrders.length) }} 条，共 {{ filteredOrders.length }} 条
        </div>
        <div class="flex items-center gap-2">
          <button 
            @click="currentPage = currentPage - 1" 
            :disabled="currentPage === 1"
            class="px-3 py-1.5 border border-slate-200 rounded text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-slate-50 transition-colors"
          >
            上一页
          </button>
          <span class="text-sm text-slate-600">{{ currentPage }} / {{ totalPages }}</span>
          <button 
            @click="currentPage = currentPage + 1" 
            :disabled="currentPage >= totalPages"
            class="px-3 py-1.5 border border-slate-200 rounded text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-slate-50 transition-colors"
          >
            下一页
          </button>
          <select v-model="pageSize" class="px-2 py-1.5 border border-slate-200 rounded text-sm">
            <option :value="10">10条/页</option>
            <option :value="20">20条/页</option>
            <option :value="50">50条/页</option>
          </select>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useOrderStore } from '../../stores/orderStore'
import axios from 'axios'

const router = useRouter()
const store = useOrderStore()

// API基础URL
const API_BASE_URL = 'http://localhost:8000'

// 筛选条件
const searchText = ref('')
const dateStart = ref('')
const dateEnd = ref('')
const shopFilter = ref('')
const productFilter = ref('')

// 分页
const currentPage = ref(1)
const pageSize = ref(20)

// 展开行
const expandedId = ref(null)

// 正在生成PDF的订单ID
const generatingOrderId = ref(null)

// 页面加载时获取真实数据
onMounted(async () => {
  await store.getCompletedOrders()
  console.log('✅ 已完成订单页面加载，订单数:', store.orders.length)
})

// 刷新订单列表
const refreshOrders = async () => {
  await store.getCompletedOrders()
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

// 总计数量 - 使用真实数据
const totalCount = computed(() => store.orders.length)

// 筛选后的订单 - 使用真实数据
const filteredOrders = computed(() => {
  let result = [...store.orders]
  
  // 搜索文本筛选
  if (searchText.value) {
    const search = searchText.value.toLowerCase()
    result = result.filter(o => 
      (o.etsy_order_id || o.id || '').toLowerCase().includes(search) || 
      (o.customer_name || '').toLowerCase().includes(search)
    )
  }
  
  // 产品筛选
  if (productFilter.value) {
    result = result.filter(o => (o.sku_mapping?.sku_code || '').includes(productFilter.value))
  }
  
  return result
})

// 分页后的订单
const paginatedOrders = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredOrders.value.slice(start, end)
})

// 总页数
const totalPages = computed(() => Math.ceil(filteredOrders.value.length / pageSize.value) || 1)

// 获取行边框样式
const getRowBorderClass = (order) => {
  if (order.review_sent) {
    return 'border-l-4 border-green-400'
  }
  return ''
}

// 获取天数样式
const getDaysClass = (days) => {
  if (days >= 8) return 'text-orange-600 font-medium'
  return 'text-slate-600'
}

// 获取追评状态文字
const getReviewStatusText = (order) => {
  if (order.review_sent) return '已发送'
  return '未发送'
}

// 获取追评状态样式
const getReviewStatusClass = (order) => {
  if (order.review_sent) {
    return 'inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-700'
  }
  return 'inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-slate-100 text-slate-500'
}

// 展开/收起
const toggleExpand = (id) => {
  expandedId.value = expandedId.value === id ? null : id
}

// 搜索
const handleSearch = () => {
  currentPage.value = 1
}

// 重置
const handleReset = () => {
  searchText.value = ''
  dateStart.value = ''
  dateEnd.value = ''
  shopFilter.value = ''
  productFilter.value = ''
  currentPage.value = 1
}

// 生成PDF
const generatePdf = async (order) => {
  generatingOrderId.value = order.id
  try {
    const response = await axios.post(`${API_BASE_URL}/api/pdf/generate-and-upload`, {
      order_id: order.id
    })
    
    if (response.data.success) {
      alert('✅ 生产文档生成成功！')
      // 刷新订单列表
      await store.getCompletedOrders()
    } else {
      alert('❌ 生成失败: ' + (response.data.detail || '未知错误'))
    }
  } catch (err) {
    console.error('生成PDF出错:', err)
    alert('❌ 生成失败: ' + (err.response?.data?.detail || err.message || 'Network Error'))
  } finally {
    generatingOrderId.value = null
  }
}

// 查看PDF
const viewPdf = (order) => {
  if (order.production_pdf_url) {
    window.open(order.production_pdf_url, '_blank')
  } else {
    alert('PDF尚未生成，请先点击"生成"按钮')
  }
}

// 下载PDF
const downloadPdf = (order) => {
  if (order.production_pdf_url) {
    const link = document.createElement('a')
    link.href = order.production_pdf_url
    link.download = `POD_${order.etsy_order_id || order.id}.pdf`
    link.click()
  } else {
    alert('PDF尚未生成，请先点击"生成"按钮')
  }
}

// 打印PDF
const printPdf = (order) => {
  if (order.production_pdf_url) {
    const printWindow = window.open(order.production_pdf_url, '_blank')
    printWindow.onload = () => {
      printWindow.print()
    }
  } else {
    alert('PDF尚未生成，请先点击"生成"按钮')
  }
}

// 发送追评邮件
const sendReviewEmail = (order) => {
  router.push({
    path: '/admin/effects',
    query: {
      orderId: order.etsy_order_id || order.id,
      action: 'review'
    }
  })
}
</script>

<style scoped>
/* 追评建议状态闪烁动画 */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.6;
  }
}
.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>
