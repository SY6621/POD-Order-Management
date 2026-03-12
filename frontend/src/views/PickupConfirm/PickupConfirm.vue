<template>
  <div class="bg-slate-200 min-h-screen flex items-center justify-center p-4">
    <div class="w-full max-w-3xl bg-white shadow-2xl rounded-2xl overflow-hidden">
      
      <!-- 顶部标题 -->
      <div class="bg-blue-600 px-6 py-5">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-white/20 rounded-xl flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l2-1.14"/><path d="m7.5 4.27 9 5.15"/><polyline points="3.29 7 12 12 20.71 7"/><line x1="12" x2="12" y1="22" y2="12"/><circle cx="18.5" cy="15.5" r="2.5"/><path d="M20.27 17.27 22 19"/></svg>
          </div>
          <div>
            <h1 class="text-xl font-bold text-white">揽件确认</h1>
            <p class="text-sm text-blue-100">4PX物流 · 工厂专用</p>
          </div>
        </div>
      </div>

      <!-- 主体内容 -->
      <div class="p-6">
        
        <!-- 搜索订单 -->
        <div class="mb-6">
          <label class="text-sm font-semibold text-slate-700 mb-2 block">搜索订单</label>
          <div class="flex items-center gap-2 bg-slate-50 border border-slate-200 rounded-xl px-4 py-3">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="输入订单号或扫描条码..." 
              class="flex-1 bg-transparent text-base text-slate-700 placeholder-slate-400 outline-none"
              @keyup.enter="searchOrder"
            />
            <button 
              @click="searchOrder"
              :disabled="searching"
              class="px-4 py-1.5 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
            >
              {{ searching ? '搜索中...' : '搜索' }}
            </button>
          </div>
        </div>

        <!-- 订单信息卡片 -->
        <div v-if="formattedOrder" class="mb-6 space-y-4">
          
          <!-- 订单基本信息 + 揽件码 -->
          <div class="bg-slate-50 rounded-xl border border-slate-200 p-5">
            <div class="flex items-center justify-between">
              <div>
                <span class="text-xs text-slate-500">订单号</span>
                <p class="text-xl font-bold text-slate-800">{{ formattedOrder.etsy_order_id || formattedOrder.id }}</p>
              </div>
              <div class="flex items-center gap-4">
                <!-- 揽件码二维码 -->
                <div class="text-center">
                  <p class="text-[10px] text-slate-400 mb-1">揽件码</p>
                  <img 
                    :src="pickupQrCodeUrl" 
                    alt="揽件码"
                    class="w-16 h-16 rounded-lg border border-slate-200"
                  />
                </div>
                <span class="px-3 py-1.5 bg-orange-100 text-orange-700 text-sm font-bold rounded-full">待发货</span>
              </div>
            </div>
          </div>

          <!-- 产品图片区域 -->
          <div class="grid grid-cols-2 gap-4">
            <!-- 产品实拍图 -->
            <div class="bg-slate-50 rounded-xl border border-slate-200 p-4">
              <div class="flex items-center gap-2 mb-3">
                <span class="w-1.5 h-4 bg-blue-500 rounded-full"></span>
                <h3 class="text-sm font-bold text-slate-700">产品实拍图</h3>
              </div>
              <div class="aspect-square bg-slate-100 rounded-lg overflow-hidden flex items-center justify-center">
                <img 
                  v-if="formattedOrder.product_photo" 
                  :src="formattedOrder.product_photo" 
                  alt="产品实拍图"
                  class="w-full h-full object-cover"
                />
                <div v-else class="text-center text-slate-400">
                  <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="mx-auto mb-2"><rect width="18" height="18" x="3" y="3" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg>
                  <p class="text-xs">暂无实拍图</p>
                </div>
              </div>
              <p class="text-xs text-slate-500 mt-2 text-center">外观与颜色参考</p>
            </div>

            <!-- 定制内容效果图 -->
            <div class="bg-slate-50 rounded-xl border border-slate-200 p-4">
              <div class="flex items-center gap-2 mb-3">
                <span class="w-1.5 h-4 bg-green-500 rounded-full"></span>
                <h3 class="text-sm font-bold text-slate-700">定制内容效果图</h3>
              </div>
              <div class="aspect-square bg-slate-100 rounded-lg overflow-hidden flex items-center justify-center">
                <img 
                  v-if="formattedOrder.effect_image" 
                  :src="formattedOrder.effect_image" 
                  alt="定制效果图"
                  class="w-full h-full object-cover"
                />
                <div v-else class="text-center text-slate-400">
                  <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="mx-auto mb-2"><path d="M12 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.375 2.625a2.121 2.121 0 1 3 3L12 15l-4 1 1-4Z"/></svg>
                  <p class="text-xs">暂无效果图</p>
                </div>
              </div>
              <p class="text-xs text-slate-500 mt-2 text-center">定制内容: {{ formattedOrder.custom_text || '-' }}</p>
            </div>
          </div>

          <!-- 产品规格信息 -->
          <div class="bg-slate-50 rounded-xl border border-slate-200 p-5">
            <div class="flex items-center gap-2 mb-4">
              <span class="w-1.5 h-4 bg-purple-500 rounded-full"></span>
              <h3 class="text-sm font-bold text-slate-700">产品规格</h3>
            </div>
            <div class="grid grid-cols-3 gap-4">
              <div class="text-center p-3 bg-white rounded-lg border border-slate-100">
                <p class="text-xs text-slate-500 mb-1">产品名称</p>
                <p class="text-sm font-semibold text-slate-800">{{ formattedOrder.product_name || '宠物ID牌' }}</p>
              </div>
              <div class="text-center p-3 bg-white rounded-lg border border-slate-100">
                <p class="text-xs text-slate-500 mb-1">SKU</p>
                <p class="text-sm font-semibold text-slate-800">{{ formattedOrder.sku || '-' }}</p>
              </div>
              <div class="text-center p-3 bg-white rounded-lg border border-slate-100">
                <p class="text-xs text-slate-500 mb-1">数量</p>
                <p class="text-sm font-semibold text-slate-800">{{ formattedOrder.quantity || 1 }} 件</p>
              </div>
            </div>
          </div>

          <!-- 收件人信息 -->
          <div class="bg-blue-50 rounded-xl border border-blue-200 p-5">
            <div class="flex items-center gap-2 mb-4">
              <span class="w-1.5 h-4 bg-blue-500 rounded-full"></span>
              <h3 class="text-sm font-bold text-slate-700">收件人信息（请核对）</h3>
              <span v-if="!formattedOrder.hasLogistics" class="px-2 py-0.5 bg-orange-100 text-orange-600 text-[10px] rounded-full">待补充物流信息</span>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <p class="text-xs text-slate-500 mb-1">收件人姓名</p>
                <p class="text-base font-semibold text-slate-800">{{ formattedOrder.buyer_name }}</p>
              </div>
              <div>
                <p class="text-xs text-slate-500 mb-1">联系电话</p>
                <p class="text-base font-semibold text-slate-800">{{ formattedOrder.buyer_phone || '-' }}</p>
              </div>
              <div>
                <p class="text-xs text-slate-500 mb-1">国家/地区</p>
                <p class="text-base font-semibold text-slate-800">{{ formattedOrder.shipping_country || 'US' }}</p>
              </div>
              <div>
                <p class="text-xs text-slate-500 mb-1">州/省</p>
                <p class="text-base font-semibold text-slate-800">{{ formattedOrder.shipping_state || '-' }}</p>
              </div>
              <div>
                <p class="text-xs text-slate-500 mb-1">城市</p>
                <p class="text-base font-semibold text-slate-800">{{ formattedOrder.shipping_city || '-' }}</p>
              </div>
              <div>
                <p class="text-xs text-slate-500 mb-1">邮编</p>
                <p class="text-base font-semibold text-slate-800">{{ formattedOrder.shipping_zip || '-' }}</p>
              </div>
              <div class="col-span-2">
                <p class="text-xs text-slate-500 mb-1">详细地址</p>
                <p class="text-base font-semibold text-slate-800">{{ formattedOrder.shipping_address }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 空状态 -->
        <div v-else-if="!searching && searched" class="mb-6 text-center py-8">
          <div class="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-3">
            <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
          </div>
          <p class="text-slate-500">未找到该订单</p>
          <p class="text-xs text-slate-400 mt-1">请检查订单号是否正确</p>
        </div>

        <!-- 提示信息 -->
        <div v-else class="mb-6 text-center py-8">
          <div class="w-16 h-16 bg-blue-50 rounded-full flex items-center justify-center mx-auto mb-3">
            <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l2-1.14"/><path d="m7.5 4.27 9 5.15"/><polyline points="3.29 7 12 12 20.71 7"/><line x1="12" x2="12" y1="22" y2="12"/><circle cx="18.5" cy="15.5" r="2.5"/><path d="M20.27 17.27 22 19"/></svg>
          </div>
          <p class="text-slate-500">请输入订单号或扫描条码</p>
          <p class="text-xs text-slate-400 mt-1">核对产品信息与地址无误后确认揽件</p>
        </div>

        <!-- 确认按钮 -->
        <button 
          @click="confirmPickup"
          :disabled="!formattedOrder || confirming || !formattedOrder.hasLogistics"
          class="w-full py-4 rounded-xl text-lg font-bold transition-all flex items-center justify-center gap-2"
          :class="formattedOrder && !confirming && formattedOrder.hasLogistics
            ? 'bg-green-600 text-white hover:bg-green-700 shadow-lg shadow-green-200'
            : 'bg-slate-100 text-slate-400 cursor-not-allowed'"
        >
          <svg v-if="!confirming" xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/></svg>
          <svg v-else class="animate-spin" xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>
          {{ confirming ? '确认中...' : (formattedOrder?.hasLogistics ? '确认已揽件，发货' : '请先补充物流信息') }}
        </button>

        <!-- 底部说明 -->
        <div class="mt-4 text-center">
          <p class="text-xs text-slate-400">
            {{ formattedOrder?.hasLogistics 
              ? '请核对以上信息无误后点击确认，订单状态将更新为「已发货」' 
              : '该订单缺少物流信息，请先在「物流下单」页面创建物流订单' }}
          </p>
        </div>
      </div>
    </div>

    <!-- 成功弹窗 -->
    <div v-if="showSuccess" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-sm text-center">
        <div class="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/></svg>
        </div>
        <h3 class="text-xl font-bold text-slate-800 mb-2">揽件确认成功</h3>
        <p class="text-sm text-slate-500 mb-6">订单 {{ formattedOrder?.etsy_order_id || formattedOrder?.id }} 已标记为已发货</p>
        <button @click="resetPage" class="w-full py-3 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700 transition-colors">
          确认下一个订单
        </button>
      </div>
    </div>

    <!-- 错误提示 -->
    <div v-if="errorMsg" class="fixed bottom-6 left-1/2 -translate-x-1/2 bg-red-50 border border-red-200 rounded-xl px-5 py-4 shadow-lg flex items-center gap-3 z-50">
      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="m15 9-6 6"/><path d="m9 9 6 6"/></svg>
      <span class="text-sm text-red-700">{{ errorMsg }}</span>
      <button @click="errorMsg = ''" class="text-red-400 hover:text-red-600 ml-2">
        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useOrderStore } from '../../stores/orderStore'

const store = useOrderStore()

// ── 状态 ──
const searchQuery = ref('')
const searching = ref(false)
const searched = ref(false)
const confirming = ref(false)
const showSuccess = ref(false)
const errorMsg = ref('')
const currentOrder = ref(null)

// ── 计算属性：格式化订单数据 ──
const formattedOrder = computed(() => {
  if (!currentOrder.value) return null
  
  const order = currentOrder.value
  
  // 优先使用关联表数据，如果没有则使用订单表直接字段
  const logistics = order.logistics || {}
  const skuMapping = order.sku_mapping || {}
  const productionDocs = order.production_documents || {}
  
  // 解析实拍图 URLs（JSON 数组格式）
  let productPhoto = null
  if (productionDocs.real_photo_urls) {
    try {
      const photos = JSON.parse(productionDocs.real_photo_urls)
      productPhoto = photos && photos.length > 0 ? photos[0] : null
    } catch (e) {
      productPhoto = productionDocs.real_photo_urls
    }
  }
  
  // 获取效果图 URL（优先使用关联表，否则使用订单表字段）
  const effectImage = productionDocs.effect_jpg_url 
    || order.effect_image_url 
    || order.effect_image 
    || null
  
  // 获取收件人信息（优先使用 logistics 表，否则使用订单表字段）
  const buyerName = logistics.recipient_name 
    || order.customer_name 
    || '-'
  
  // 判断是否有完整的物流信息
  const hasLogistics = logistics && logistics.recipient_name
  
  return {
    id: order.id,
    etsy_order_id: order.etsy_order_id,
    // 收件人信息（优先从 logistics 表获取，否则使用订单表字段）
    buyer_name: buyerName,
    buyer_phone: logistics.phone || order.buyer_phone || '-',
    shipping_country: logistics.country || order.shipping_country || '-',
    shipping_state: logistics.state || order.shipping_state || '-',
    shipping_city: logistics.city || order.shipping_city || '-',
    shipping_zip: logistics.postal_code || order.shipping_zip || '-',
    shipping_address: logistics.street_address || order.shipping_address || '-',
    // 产品信息（优先从 sku_mapping 获取，否则使用订单表字段）
    product_name: skuMapping.product_name 
      || (order.product_shape ? `宠物ID牌 - ${order.product_shape}` : '宠物ID牌'),
    sku: skuMapping.sku_code || order.matched_sku_id || order.sku_id || '-',
    custom_text: order.front_text || '-',
    quantity: order.quantity || 1,
    // 图片信息
    product_photo: productPhoto,
    effect_image: effectImage,
    // 状态
    status: order.status,
    // 标记是否有物流信息
    hasLogistics
  }
})

// ── 计算属性：揽件码二维码 URL ──
const pickupQrCodeUrl = computed(() => {
  if (!formattedOrder.value) return ''
  
  // 生成揽件码内容：包含订单ID和验证信息
  const pickupCode = JSON.stringify({
    orderId: formattedOrder.value.id,
    etsyOrderId: formattedOrder.value.etsy_order_id,
    type: 'pickup_confirm',
    timestamp: Date.now()
  })
  
  // 使用 Google Chart API 生成二维码
  const encodedData = encodeURIComponent(pickupCode)
  return `https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=${encodedData}`
})

// ── 方法 ──
async function searchOrder() {
  if (!searchQuery.value.trim()) return
  
  searching.value = true
  searched.value = true
  currentOrder.value = null
  errorMsg.value = ''
  
  try {
    // 调用 Store 方法搜索订单
    const order = await store.searchOrderById(searchQuery.value.trim())
    
    if (order) {
      currentOrder.value = order
    } else {
      errorMsg.value = '未找到该订单，请检查订单号是否正确'
    }
  } catch (e) {
    errorMsg.value = '搜索失败，请重试'
    console.error('搜索订单失败:', e)
  } finally {
    searching.value = false
  }
}

async function confirmPickup() {
  if (!currentOrder.value) return
  
  confirming.value = true
  errorMsg.value = ''
  
  try {
    // 调用 Store 方法更新订单状态为已发货
    await store.updateOrderStatus(currentOrder.value.id, 'shipped')
    
    showSuccess.value = true
  } catch (e) {
    errorMsg.value = '确认失败，请重试: ' + (e.message || '未知错误')
    console.error('确认发货失败:', e)
  } finally {
    confirming.value = false
  }
}

function resetPage() {
  searchQuery.value = ''
  currentOrder.value = null
  searched.value = false
  showSuccess.value = false
  errorMsg.value = ''
}
</script>
