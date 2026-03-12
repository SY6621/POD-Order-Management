<template>
  <div class="min-h-screen bg-slate-50">
    <!-- 顶部信息栏 -->
    <header class="bg-white border-b border-slate-200 px-6 py-4">
      <div class="max-w-4xl mx-auto flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
              <rect width="18" height="18" x="3" y="3" rx="2" ry="2"/>
              <circle cx="9" cy="9" r="2"/>
              <path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>
            </svg>
          </div>
          <div>
            <h1 class="font-bold text-slate-800">效果图下载</h1>
            <p class="text-sm text-slate-500">{{ currentDate }}</p>
          </div>
        </div>
        <div class="text-right">
          <p class="text-sm font-medium text-slate-800">{{ orderData.customer_name }}</p>
          <p class="text-xs text-slate-500">订单 #{{ orderData.etsy_order_id }}</p>
        </div>
      </div>
    </header>

    <main class="max-w-4xl mx-auto p-6">
      <!-- 订单信息卡片 -->
      <div class="bg-white rounded-xl border border-slate-200 p-6 mb-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="font-bold text-slate-800">订单详情</h2>
          <span class="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-medium">
            效果图已完成
          </span>
        </div>
        
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div>
            <p class="text-slate-500 mb-1">外观</p>
            <p class="font-medium text-slate-800">{{ orderData.product_shape }}</p>
          </div>
          <div>
            <p class="text-slate-500 mb-1">颜色</p>
            <p class="font-medium text-slate-800">{{ orderData.product_color }}</p>
          </div>
          <div>
            <p class="text-slate-500 mb-1">尺寸</p>
            <p class="font-medium text-slate-800">{{ orderData.product_size }}</p>
          </div>
          <div>
            <p class="text-slate-500 mb-1">字体</p>
            <p class="font-medium text-slate-800">{{ orderData.font_code }}</p>
          </div>
        </div>

        <div class="mt-4 pt-4 border-t border-slate-100">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div>
              <p class="text-slate-500 mb-1">正面文字</p>
              <p class="font-medium text-slate-800 font-mono bg-slate-50 px-3 py-2 rounded-lg">{{ orderData.front_text || '-' }}</p>
            </div>
            <div>
              <p class="text-slate-500 mb-1">背面文字</p>
              <p class="font-medium text-slate-800 font-mono bg-slate-50 px-3 py-2 rounded-lg">{{ orderData.back_text || '-' }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 效果图预览 -->
      <div class="bg-white rounded-xl border border-slate-200 p-6 mb-6">
        <h2 class="font-bold text-slate-800 mb-4">效果图预览</h2>
        
        <div v-if="loading" class="text-center py-12">
          <div class="w-8 h-8 border-2 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p class="text-slate-500">加载效果图中...</p>
        </div>

        <div v-else-if="error" class="text-center py-12">
          <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" x2="12" y1="8" y2="12"/>
              <line x1="12" x2="12.01" y1="16" y2="16"/>
            </svg>
          </div>
          <p class="text-red-500">{{ error }}</p>
        </div>

        <div v-else-if="!effectImageUrl" class="text-center py-12">
          <p class="text-slate-500">效果图尚未生成</p>
        </div>

        <div v-else class="space-y-4">
          <!-- 效果图显示 -->
          <div class="bg-slate-50 rounded-xl p-4 flex items-center justify-center min-h-[300px]">
            <img 
              v-if="isImageUrl(effectImageUrl)"
              :src="effectImageUrl" 
              alt="效果图"
              class="max-w-full max-h-[400px] object-contain"
            >
            <div v-else class="text-center">
              <p class="text-slate-500 mb-4">效果图已生成</p>
              <a 
                :href="effectImageUrl" 
                target="_blank"
                class="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                  <polyline points="7 10 12 15 17 10"/>
                  <line x1="12" x2="12" y1="15" y2="3"/>
                </svg>
                查看效果图
              </a>
            </div>
          </div>

          <!-- 下载按钮 -->
          <div class="flex gap-3">
            <button 
              @click="downloadEffect"
              class="flex-1 py-3 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700 flex items-center justify-center gap-2"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="7 10 12 15 17 10"/>
                <line x1="12" x2="12" y1="15" y2="3"/>
              </svg>
              下载效果图
            </button>
          </div>
        </div>
      </div>

      <!-- 邮件内容 -->
      <div class="bg-white rounded-xl border border-slate-200 p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="font-bold text-slate-800">邮件内容</h2>
          <button 
            @click="copyEmailContent"
            class="px-4 py-2 bg-slate-100 text-slate-700 rounded-lg hover:bg-slate-200 flex items-center gap-2 text-sm"
          >
            <svg v-if="!copied" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect width="14" height="14" x="8" y="8" rx="2" ry="2"/>
              <path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="20 6 9 17 4 12"/>
            </svg>
            {{ copied ? '已复制' : '复制内容' }}
          </button>
        </div>

        <div class="bg-slate-50 rounded-xl p-4 font-mono text-sm text-slate-700 whitespace-pre-wrap">{{ emailContent }}</div>

        <div class="mt-4 p-4 bg-blue-50 rounded-xl">
          <p class="text-sm text-blue-800">
            <strong>使用提示：</strong>复制上方内容后，打开 ETSY 消息页面，粘贴发送给客户。
          </p>
        </div>
      </div>
    </main>

    <!-- 底部 -->
    <footer class="max-w-4xl mx-auto px-6 py-8 text-center text-sm text-slate-400">
      <p>ETSY 订单自动化系统 · 效果图下载页面</p>
      <p class="mt-1">生成时间：{{ orderData.created_at }}</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import supabase from '../../utils/supabase'

const route = useRoute()

// 状态
const loading = ref(true)
const error = ref('')
const copied = ref(false)
const effectImageUrl = ref('')

// 订单数据
const orderData = ref({
  etsy_order_id: '',
  customer_name: '',
  product_shape: '',
  product_color: '',
  product_size: '',
  font_code: '',
  front_text: '',
  back_text: '',
  created_at: ''
})

// 当前日期
const currentDate = computed(() => {
  const date = new Date()
  return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`
})

// 邮件内容模板
const emailContent = computed(() => {
  const order = orderData.value
  return `Dear ${order.customer_name},

Thank you for your order!

Your custom pet tag has been designed and is ready for your review:

🎨 Design Details:
• Shape: ${order.product_shape}
• Color: ${order.product_color}
• Size: ${order.product_size}
• Front Text: "${order.front_text || 'N/A'}"
• Back Text: "${order.back_text || 'N/A'}"

📎 Please find the effect image attached. Please review carefully and let us know if you need any changes.

If everything looks good, we'll start production immediately!

Best regards,
Your Store Team

---
Order #: ${order.etsy_order_id}
Date: ${new Date(order.created_at).toLocaleDateString()}`
})

// 判断是否为图片URL
function isImageUrl(url) {
  if (!url) return false
  return url.match(/\.(jpg|jpeg|png|gif|svg|webp)(\?.*)?$/i)
}

// 下载效果图
function downloadEffect() {
  if (!effectImageUrl.value) return
  
  const link = document.createElement('a')
  link.href = effectImageUrl.value
  link.download = `effect_${orderData.value.etsy_order_id}.svg`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

// 复制邮件内容
async function copyEmailContent() {
  try {
    await navigator.clipboard.writeText(emailContent.value)
    copied.value = true
    setTimeout(() => copied.value = false, 2000)
  } catch (err) {
    console.error('复制失败:', err)
  }
}

// 加载订单数据
async function loadOrderData() {
  loading.value = true
  error.value = ''
  
  try {
    // 从 URL 参数获取订单ID
    const orderId = route.params.orderId || route.query.orderId
    
    if (!orderId) {
      error.value = '未找到订单信息'
      loading.value = false
      return
    }

    // 查询订单数据
    const { data, error: dbError } = await supabase
      .from('orders')
      .select('*')
      .eq('id', orderId)
      .single()
    
    if (dbError || !data) {
      error.value = '订单不存在或已过期'
      loading.value = false
      return
    }

    orderData.value = data
    effectImageUrl.value = data.effect_image_url || ''
    loading.value = false
  } catch (err) {
    error.value = '加载失败，请稍后重试'
    loading.value = false
    console.error('加载订单失败:', err)
  }
}

onMounted(() => {
  loadOrderData()
})
</script>