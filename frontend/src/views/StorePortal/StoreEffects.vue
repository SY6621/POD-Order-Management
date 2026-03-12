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
            @click="shopStore.logout(); $router.push('/store/login')"
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

      <!-- 待下载效果图订单 -->
      <div class="bg-white rounded-xl border border-slate-200 overflow-hidden mb-6">
        <div class="px-6 py-4 border-b border-slate-200">
          <h2 class="font-bold text-slate-800">待下载效果图 ({{ pendingOrders.length }})</h2>
        </div>
        
        <div v-if="pendingOrders.length === 0" class="p-8 text-center text-slate-500">
          暂无待下载的效果图
        </div>
        
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-6">
          <div v-for="order in pendingOrders" :key="order.id" class="border border-slate-200 rounded-xl overflow-hidden hover:shadow-md transition-shadow">
            <!-- 效果图预览 -->
            <div class="aspect-square bg-slate-100 flex items-center justify-center">
              <img v-if="order.effect_image_url" :src="order.effect_image_url" class="w-full h-full object-contain" alt="效果图">
              <div v-else class="text-center text-slate-400">
                <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="mx-auto mb-2">
                  <rect width="18" height="18" x="3" y="3" rx="2"/>
                  <circle cx="9" cy="9" r="2"/>
                  <path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>
                </svg>
                <p class="text-sm">效果图生成中</p>
              </div>
            </div>
            
            <!-- 订单信息 -->
            <div class="p-4">
              <div class="flex items-center justify-between mb-2">
                <span class="font-mono font-semibold text-slate-800">{{ order.etsy_order_id }}</span>
                <span class="px-2 py-0.5 bg-orange-100 text-orange-700 text-xs rounded-full">待确认</span>
              </div>
              <p class="text-sm text-slate-600 mb-1">{{ order.product_shape }} - {{ order.product_color }}</p>
              <p class="text-sm text-slate-600 mb-3">正面: {{ order.front_text }}</p>
              
              <!-- 下载按钮 -->
              <div class="flex gap-2">
                <button 
                  @click="downloadEffect(order)"
                  :disabled="!order.effect_image_url"
                  class="flex-1 py-2 bg-blue-50 text-blue-600 rounded-lg text-sm font-medium hover:bg-blue-100 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  下载效果图
                </button>
                <button 
                  @click="downloadEmailTemplate(order)"
                  class="flex-1 py-2 bg-slate-50 text-slate-600 rounded-lg text-sm font-medium hover:bg-slate-100"
                >
                  邮件模板
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 已确认订单 -->
      <div class="bg-white rounded-xl border border-slate-200 overflow-hidden">
        <div class="px-6 py-4 border-b border-slate-200">
          <h2 class="font-bold text-slate-800">已确认订单 ({{ confirmedOrders.length }})</h2>
        </div>
        
        <div v-if="confirmedOrders.length === 0" class="p-8 text-center text-slate-500">
          暂无已确认订单
        </div>
        
        <div v-else class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-slate-50">
              <tr>
                <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">订单号</th>
                <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">产品</th>
                <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">定制内容</th>
                <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">状态</th>
                <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">操作</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              <tr v-for="order in confirmedOrders" :key="order.id" class="hover:bg-slate-50">
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
                </td>
                <td class="py-4 px-4">
                  <span class="px-2 py-1 bg-green-100 text-green-700 rounded-full text-xs font-medium">
                    {{ getStatusText(order.status) }}
                  </span>
                </td>
                <td class="py-4 px-4">
                  <button 
                    @click="downloadEffect(order)"
                    class="text-sm text-blue-600 hover:underline"
                  >
                    下载
                  </button>
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
const pendingOrders = computed(() => orders.value.filter(o => o.status === 'pending' || o.status === 'confirmed'))
const confirmedOrders = computed(() => orders.value.filter(o => ['producing', 'shipped', 'delivered'].includes(o.status)))

// 加载订单
onMounted(async () => {
  orders.value = await shopStore.fetchShopOrders()
})

// 下载效果图
function downloadEffect(order) {
  if (!order.effect_image_url) return
  
  const link = document.createElement('a')
  link.href = order.effect_image_url
  link.download = `effect_${order.etsy_order_id}.svg`
  link.target = '_blank'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

// 下载邮件模板
function downloadEmailTemplate(order) {
  const template = `
尊敬的客户您好，

您的订单 #${order.etsy_order_id} 设计效果图已完成，请查阅附件。

产品信息：
- 形状：${order.product_shape}
- 颜色：${order.product_color}
- 尺寸：${order.product_size}
- 正面刻字：${order.front_text}
- 背面刻字：${order.back_text}

如您对效果图满意，请回复确认，我们将立即安排生产。
如有修改需求，请随时告知。

感谢您的订购！
  `
  
  const blob = new Blob([template], { type: 'text/plain' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `email_template_${order.etsy_order_id}.txt`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}

// 辅助函数
function getColorClass(color) {
  const map = { '金色': 'bg-yellow-400', '银色': 'bg-gray-300', '玫瑰金': 'bg-amber-700' }
  return map[color] || 'bg-gray-400'
}

function getStatusText(status) {
  const map = {
    'producing': '生产中',
    'shipped': '已发货',
    'delivered': '已送达'
  }
  return map[status] || status
}
</script>