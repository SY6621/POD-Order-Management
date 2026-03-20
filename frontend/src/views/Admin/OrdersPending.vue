<template>
  <div class="h-full overflow-auto bg-slate-50 p-4">
    <!-- 页面标题 -->
    <div class="mb-4">
      <h1 class="text-2xl font-bold text-slate-800">待确认订单</h1>
      <p class="text-sm text-slate-500 mt-1">处理客户订单，生成效果图并发送确认邮件</p>
    </div>

    <div class="flex gap-4">
      <!-- ══ 左侧：订单列表 + 设计器 ══ -->
      <div class="flex-1 space-y-3 min-w-0">
        <!-- 版块1：合并订单表格 -->
        <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
          <div class="px-4 py-3 border-b border-slate-100 flex items-center justify-between">
            <div class="flex items-center gap-3">
              <h2 class="text-base font-bold text-slate-800">订单列表</h2>
              <span class="bg-blue-100 text-blue-600 px-2 py-0.5 rounded-full text-xs font-bold">{{ allOrdersCount }}条</span>
            </div>
            <div class="flex items-center gap-2">
              <span class="text-xs text-slate-400">子账号:</span>
              <button class="px-2 py-1 rounded text-xs font-medium" :class="activeAccount === 'all' ? 'bg-blue-600 text-white' : 'bg-white text-slate-600 border border-slate-200'" @click="activeAccount = 'all'">全部</button>
              <button class="px-2 py-1 rounded text-xs font-medium" :class="activeAccount === 'A' ? 'bg-blue-600 text-white' : 'bg-white text-slate-600 border border-slate-200'" @click="activeAccount = 'A'">A</button>
              <button class="px-2 py-1 rounded text-xs font-medium" :class="activeAccount === 'B' ? 'bg-blue-600 text-white' : 'bg-white text-slate-600 border border-slate-200'" @click="activeAccount = 'B'">B</button>
            </div>
          </div>

          <div class="px-4 py-2 border-b border-slate-100 flex items-center gap-3 text-xs">
            <button class="px-3 py-1 rounded-full" :class="orderTab === 'all' ? 'bg-blue-50 text-blue-600 font-medium' : 'text-slate-500'" @click="orderTab = 'all'">全部 {{ allOrdersCount }}</button>
            <button class="px-3 py-1 rounded-full" :class="orderTab === 'new' ? 'bg-amber-50 text-amber-600 font-medium' : 'text-slate-500'" @click="orderTab = 'new'">新订单 {{ newOrdersCount }}</button>
            <button class="px-3 py-1 rounded-full" :class="orderTab === 'pending' ? 'bg-orange-50 text-orange-600 font-medium' : 'text-slate-500'" @click="orderTab = 'pending'">待确认 {{ pendingCount }}</button>
          </div>
          
          <div class="overflow-x-auto" style="max-height: 200px;">
            <table class="w-full text-xs text-left">
              <thead class="bg-slate-50 text-slate-500 font-medium border-b border-slate-200 sticky top-0 z-10">
                <tr class="h-[36px]">
                  <th class="px-3 whitespace-nowrap font-medium">订单ID</th>
                  <th class="px-3 whitespace-nowrap font-medium">客户</th>
                  <th class="px-3 whitespace-nowrap font-medium">产品</th>
                  <th class="px-3 whitespace-nowrap font-medium">国家</th>
                  <th class="px-3 whitespace-nowrap font-medium">数量</th>
                  <th class="px-3 whitespace-nowrap font-medium">状态</th>
                  <th class="px-3 whitespace-nowrap font-medium">操作</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                <tr v-for="order in filteredOrders" :key="order.id" @click="selectOrder(order)" 
                    :class="['hover:bg-slate-50 transition-colors h-[40px] cursor-pointer', selectedOrder?.id === order.id ? 'bg-blue-50' : '']">
                  <td class="px-3 whitespace-nowrap font-medium text-slate-700">{{ order.etsy_order_id || order.id }}</td>
                  <td class="px-3 whitespace-nowrap text-slate-600">{{ order.customer_name }}</td>
                  <td class="px-3 whitespace-nowrap font-mono text-slate-500">{{ order.sku_mapping?.sku_code || order.sku_id }}</td>
                  <td class="px-3 whitespace-nowrap text-slate-600">{{ order.country || '美国' }}</td>
                  <td class="px-3 whitespace-nowrap text-slate-600">{{ order.quantity }}</td>
                  <td class="px-3 whitespace-nowrap">
                    <span v-if="order.status === 'new'" class="bg-amber-100 text-amber-600 px-2 py-0.5 rounded text-[10px] font-bold">新订单</span>
                    <span v-else-if="order.status === 'pending'" class="bg-orange-100 text-orange-600 px-2 py-0.5 rounded text-[10px] font-bold">待确认</span>
                    <span v-else-if="order.status === 'effect_sent'" class="bg-blue-100 text-blue-600 px-2 py-0.5 rounded text-[10px] font-bold">效果图已发</span>
                    <span v-else class="bg-slate-100 text-slate-600 px-2 py-0.5 rounded text-[10px] font-bold">{{ order.status }}</span>
                  </td>
                  <td class="px-3 whitespace-nowrap">
                    <button v-if="order.status === 'new'" @click.stop="moveToPending(order)" class="bg-emerald-500 hover:bg-emerald-600 text-white px-2 py-1 rounded text-[10px] transition-colors">拒绝链接</button>
                    <button v-else @click.stop="confirmOrder(order)" class="bg-slate-800 hover:bg-slate-900 text-white px-2 py-1 rounded text-[10px] transition-colors">创建订单</button>
                  </td>
                </tr>
                <tr v-if="filteredOrders.length === 0" class="h-[60px]">
                  <td colspan="7" class="px-3 text-center text-slate-400 text-sm">暂无订单</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- 版块2：设计器（独占左侧，无滚动条） -->
        <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
          <div class="px-4 py-2 border-b border-slate-100 flex items-center justify-between">
            <div class="flex items-center gap-2">
              <h3 class="font-bold text-slate-800 text-sm">效果图设计器</h3>
              <span class="text-xs text-slate-400">使用本地离线设计器生成正背面效果图</span>
            </div>
            <div class="text-xs text-slate-500" v-if="selectedOrder">当前: {{ selectedOrder.etsy_order_id || selectedOrder.id }}</div>
          </div>
          <div class="bg-slate-50">
            <iframe v-if="designerUrl" ref="designerFrame" :src="designerUrl" class="w-full h-[950px] border-0" @load="onDesignerLoad"></iframe>
            <div v-else class="w-full h-[950px] flex items-center justify-center text-slate-400">设计器加载中...</div>
          </div>
          <div class="px-4 py-2 border-t border-slate-100 flex justify-center gap-2">
            <button @click="saveEffectImage" :disabled="!selectedOrder" class="bg-blue-600 hover:bg-blue-700 disabled:bg-slate-300 text-white px-4 py-1.5 rounded text-sm font-medium flex items-center gap-1 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>
              提交效果图
            </button>
          </div>
        </div>
      </div>

      <!-- ══ 右侧：订单详情 + 邮件面板 ══ -->
      <div class="w-[320px] shrink-0 space-y-3">
        <!-- 订单详情 -->
        <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
          <div class="px-3 py-2 border-b border-slate-100 bg-slate-50">
            <h3 class="font-bold text-slate-800 text-sm">订单详情</h3>
          </div>
          <div v-if="selectedOrder" class="p-3">
            <div class="w-full h-32 bg-slate-100 rounded-lg overflow-hidden mb-3">
              <img v-if="selectedOrder.product_image" :src="selectedOrder.product_image" class="w-full h-full object-cover"/>
              <div v-else class="w-full h-full flex items-center justify-center text-slate-400 text-xs">暂无图片</div>
            </div>
            <div class="space-y-1.5 text-xs">
              <div class="flex justify-between"><span class="text-slate-400">订单ID:</span><span class="text-slate-700 font-medium">{{ selectedOrder.etsy_order_id || selectedOrder.id }}</span></div>
              <div class="flex justify-between"><span class="text-slate-400">客户:</span><span class="text-slate-700">{{ selectedOrder.customer_name }}</span></div>
              <div class="flex justify-between"><span class="text-slate-400">形状:</span><span class="text-slate-700">{{ selectedOrder.shape || '圆形' }}</span></div>
              <div class="flex justify-between"><span class="text-slate-400">颜色:</span><span class="text-slate-700">{{ selectedOrder.color || '古铜金' }}</span></div>
              <div class="flex justify-between"><span class="text-slate-400">尺寸:</span><span class="text-slate-700">{{ selectedOrder.size || '30mm' }}</span></div>
              <div class="pt-2 border-t border-slate-100 mt-2">
                <div class="text-slate-400 mb-1">正面内容:</div>
                <div class="text-slate-700 font-medium">{{ selectedOrder.front_text || '-' }}</div>
              </div>
              <div>
                <div class="text-slate-400 mb-1">背面内容:</div>
                <div class="text-slate-700">{{ selectedOrder.back_text || '-' }}</div>
              </div>
              <div class="pt-2 border-t border-slate-100 mt-2 flex gap-2">
                <button class="flex-1 px-2 py-1.5 rounded text-xs bg-white border border-slate-200 text-slate-600">本地上传</button>
                <button class="flex-1 px-2 py-1.5 rounded text-xs bg-slate-800 text-white">下载SVG</button>
              </div>
            </div>
          </div>
          <div v-else class="p-3 text-center text-sm text-slate-400">请在左侧选择订单</div>
        </div>

        <!-- 邮件面板 -->
        <div class="bg-white rounded-xl shadow-sm border border-slate-200 flex flex-col">
          <div class="p-3 border-b border-slate-100">
            <div class="flex items-center gap-2">
              <div class="w-8 h-8 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center font-bold text-xs">{{ initials }}</div>
              <div>
                <h3 class="font-bold text-slate-800 text-sm">{{ selectedOrder?.customer_name || '请选择订单' }}</h3>
                <div class="flex items-center gap-1 text-xs text-slate-500">
                  <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg>
                  {{ selectedOrder?.country || '美国' }}
                </div>
              </div>
            </div>
          </div>

          <div class="p-3 flex-1 flex flex-col gap-3">
            <div>
              <h4 class="text-xs font-medium text-slate-500 mb-1">生成的邮件</h4>
              <div class="bg-slate-50 border border-slate-200 rounded-lg p-2 text-xs text-slate-600 leading-relaxed h-[500px] overflow-y-auto whitespace-pre-wrap">
                <template v-if="emailContent">{{ emailContent }}</template>
                <template v-else><p class="text-slate-400 text-center mt-48">请选择订单并点击「生成邮件」</p></template>
              </div>
            </div>

            <div>
              <h4 class="text-xs font-medium text-slate-500 mb-1">客户需求</h4>
              <textarea v-model="customerNote" class="w-full bg-slate-50 border border-slate-200 rounded-lg p-2 text-xs text-slate-600 h-16 resize-none focus:outline-none focus:ring-1 focus:ring-blue-500/20 focus:border-blue-500" placeholder="在此粘贴客户的需求..."></textarea>
            </div>

            <div>
              <h4 class="text-xs font-medium text-slate-500 mb-1">风格选择</h4>
              <div class="grid grid-cols-3 gap-1">
                <button :class="['flex flex-col items-center justify-center gap-1 p-1.5 rounded-lg border transition-all text-xs', selectedStyle === 'natural' ? 'bg-blue-50 border-blue-200 text-blue-600' : 'bg-white border-slate-200 text-slate-400']" @click="selectedStyle = 'natural'">
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" :stroke="selectedStyle === 'natural' ? '#2563eb' : '#94a3b8'" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2"/><line x1="9" x2="9.01" y1="9" y2="9"/><line x1="15" x2="15.01" y1="9" y2="9"/></svg>
                  <span>自然</span>
                </button>
                <button :class="['flex flex-col items-center justify-center gap-1 p-1.5 rounded-lg border transition-all text-xs', selectedStyle === 'cute' ? 'bg-blue-50 border-blue-200 text-blue-600' : 'bg-white border-slate-200 text-slate-400']" @click="selectedStyle = 'cute'">
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" :stroke="selectedStyle === 'cute' ? '#2563eb' : '#94a3b8'" stroke-width="2"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>
                  <span>可爱</span>
                </button>
                <button :class="['flex flex-col items-center justify-center gap-1 p-1.5 rounded-lg border transition-all text-xs', selectedStyle === 'direct' ? 'bg-blue-50 border-blue-200 text-blue-600' : 'bg-white border-slate-200 text-slate-400']" @click="selectedStyle = 'direct'">
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" :stroke="selectedStyle === 'direct' ? '#2563eb' : '#94a3b8'" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
                  <span>直接</span>
                </button>
              </div>
            </div>

            <div class="mt-auto space-y-2">
              <button @click="generateEmail" class="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg font-medium text-sm flex items-center justify-center gap-1 shadow-sm transition-all">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/></svg>
                生成邮件
              </button>
              <button @click="copyEmail" class="w-full bg-white border border-slate-200 hover:bg-slate-50 text-slate-600 py-2 rounded-lg font-medium text-sm flex items-center justify-center gap-1 transition-all">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="2"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>
                复制内容
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useOrderStore } from '../../stores/orderStore'

const store = useOrderStore()
const designerFrame = ref(null)
const designerUrl = ref('/designer-offline-vector.html')
const activeAccount = ref('all')
const orderTab = ref('all')
const selectedOrder = ref(null)
const customerNote = ref('')
const selectedStyle = ref('natural')
const emailContent = ref('')

onMounted(() => {
  store.getPendingOrders()
})

const allOrders = computed(() => {
  return store.orders.filter(o => ['new', 'pending', 'effect_sent'].includes(o.status))
})

const filteredOrders = computed(() => {
  if (orderTab.value === 'new') {
    return allOrders.value.filter(o => o.status === 'new')
  } else if (orderTab.value === 'pending') {
    return allOrders.value.filter(o => ['pending', 'effect_sent'].includes(o.status))
  }
  return allOrders.value
})

const allOrdersCount = computed(() => allOrders.value.length)
const newOrdersCount = computed(() => allOrders.value.filter(o => o.status === 'new').length)
const pendingCount = computed(() => allOrders.value.filter(o => ['pending', 'effect_sent'].includes(o.status)).length)

const selectOrder = (order) => {
  selectedOrder.value = order
  if (designerFrame.value && designerFrame.value.contentWindow) {
    // 从 sku_mapping 获取 shape 和 color
    const shape = order.sku_mapping?.shape || 'circle'
    const color = order.sku_mapping?.color || '银色'
    
    designerFrame.value.contentWindow.postMessage({
      type: 'loadOrder',
      data: {
        frontText: order.front_text || '',
        backText: order.back_text || '',
        phone: order.phone || '',
        shape: shape,
        color: color,
        font: order.font_code || 'F-04'
      }
    }, '*')
    
    console.log('📤 发送订单数据到设计器:', {
      orderId: order.etsy_order_id,
      shape: shape,
      color: color,
      frontText: order.front_text,
      backText: order.back_text
    })
  }
}

const onDesignerLoad = () => {
  if (selectedOrder.value && designerFrame.value) {
    selectOrder(selectedOrder.value)
  }
}

const saveEffectImage = async () => {
  if (!selectedOrder.value || !designerFrame.value) {
    alert('请先选择一条订单')
    return
  }
  const handleMessage = (event) => {
    if (event.data && event.data.type === 'svgData') {
      window.removeEventListener('message', handleMessage)
      alert('✅ 已从设计器获取SVG数据')
    }
  }
  window.addEventListener('message', handleMessage)
  designerFrame.value.contentWindow.postMessage({ type: 'getSVG' }, '*')
}

const moveToPending = async (order) => {
  if (!confirm(`确认将新订单 ${order.etsy_order_id || order.id} 转为待确认？`)) return
  try {
    await store.updateOrderStatus(order.id, 'pending')
    alert('✅ 已转为待确认订单')
  } catch (e) {
    alert('❌ 操作失败：' + e.message)
  }
}

const confirmOrder = async (order) => {
  if (!confirm(`确认将订单 ${order.etsy_order_id || order.id} 改为生产中？`)) return
  try {
    await store.updateOrderStatus(order.id, 'producing')
    selectedOrder.value = null
    alert('✅ 订单已转入生产中！')
  } catch (e) {
    alert('❌ 操作失败：' + e.message)
  }
}

const initials = computed(() => {
  const name = selectedOrder.value?.customer_name || 'M'
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
})

const generateEmail = () => {
  if (!selectedOrder.value) {
    alert('请先选择一条订单')
    return
  }
  const order = selectedOrder.value
  const firstName = order.customer_name?.split(' ')[0] || 'there'
  const orderId = order.etsy_order_id || order.id
  const frontText = order.front_text || ''
  const backText = order.back_text || ''
  const hasEffectImage = !!order.effect_image_url
  const effectImageLine = hasEffectImage
    ? `\nWe have prepared a preview of your custom tag. You can view it here:\n${order.effect_image_url}\n`
    : '\nWe are currently preparing a preview of your custom tag and will send it to you within 4 hours.\n'
  const customDetails = [frontText, backText].filter(Boolean).join(' / ')
  const detailsLine = customDetails ? `\nYour customization details: ${customDetails}\n` : ''
  const noteSection = customerNote.value ? `\nNote: ${customerNote.value}\n` : ''
  let greeting = ''
  let sign = ''
  if (selectedStyle.value === 'cute') {
    greeting = `Hi ${firstName}! 💕`
    sign = 'With love,\nOur Pet Tag Team 🐾'
  } else if (selectedStyle.value === 'direct') {
    greeting = `Hi ${firstName},`
    sign = 'Best,\nCustomer Support'
  } else {
    greeting = `Dear ${firstName},`
    sign = 'Kind regards,\nCustomer Support Team'
  }
  emailContent.value = `${greeting}\n\nThank you for your order! We have received your customization request for order #${orderId}.${detailsLine}${effectImageLine}${noteSection}\nPlease review and let us know if everything looks good, or if you would like any changes.\n\n${sign}`
}

const copyEmail = async () => {
  if (!emailContent.value) {
    alert('请先点击「生成邮件」')
    return
  }
  try {
    await navigator.clipboard.writeText(emailContent.value)
    alert('✅ 邮件内容已复制到剪贴板！')
  } catch (e) {
    alert('复制失败，请手动复制')
  }
}
</script>
