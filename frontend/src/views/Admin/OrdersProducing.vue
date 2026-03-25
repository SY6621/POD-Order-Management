<template>
  <div class="h-full overflow-auto bg-slate-50 p-4">
    <!-- 页面标题 -->
    <div class="mb-4 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-slate-800">生产中订单</h1>
        <p class="text-sm text-slate-500 mt-1">按【生产文档】进行生产，点击查看或下载PDF</p>
      </div>
      <div class="flex items-center gap-2">
        <button @click="loadOrders" class="bg-white border border-slate-200 hover:bg-slate-50 text-slate-600 px-4 py-2 rounded-lg text-sm font-medium flex items-center gap-2 transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/></svg>
          刷新
        </button>
        <span class="text-sm text-slate-500">共 <span class="font-bold text-slate-700">{{ orders.length }}</span> 单</span>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="bg-white rounded-xl shadow-sm border border-slate-200 p-12 text-center">
      <div class="w-8 h-8 border-2 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-3"></div>
      <p class="text-slate-500 text-sm">加载中...</p>
    </div>

    <!-- 订单列表 -->
    <div v-else class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
      <table class="w-full text-sm text-left">
        <thead class="bg-slate-50 text-slate-500 font-medium border-b border-slate-200">
          <tr class="h-[44px]">
            <th class="px-4 whitespace-nowrap font-medium">订单号</th>
            <th class="px-4 whitespace-nowrap font-medium">客户</th>
            <th class="px-4 whitespace-nowrap font-medium">产品</th>
            <th class="px-4 whitespace-nowrap font-medium">SKU</th>
            <th class="px-4 whitespace-nowrap font-medium">物流单号</th>
            <th class="px-4 whitespace-nowrap font-medium">下单时间</th>
            <th class="px-4 whitespace-nowrap font-medium text-center">生产文档</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100">
          <template v-for="order in orders" :key="order.id">
            <!-- 主行 -->
            <tr
              @click="toggleExpand(order.id)"
              class="h-[52px] hover:bg-slate-50 transition-colors cursor-pointer"
            >
              <td class="px-4 whitespace-nowrap font-mono font-semibold text-blue-600">{{ order.etsy_order_id }}</td>
              <td class="px-4 whitespace-nowrap text-slate-700">{{ order.customer_name || '-' }}</td>
              <td class="px-4 whitespace-nowrap text-slate-600">
                {{ order.sku_mappings?.shape || order.product_shape || '-' }} -
                {{ order.sku_mappings?.color || order.product_color || '-' }}
              </td>
              <td class="px-4 whitespace-nowrap font-mono text-xs text-slate-500">{{ order.sku_mappings?.sku_code || '-' }}</td>
              <td class="px-4 whitespace-nowrap font-mono text-xs text-slate-500">
                {{ order.logistics?.[0]?.tracking_number || '-' }}
              </td>
              <td class="px-4 whitespace-nowrap text-slate-500">{{ formatDate(order.created_at) }}</td>
              <td class="px-4 whitespace-nowrap text-center">
                <div v-if="order.production_pdf_url" class="flex items-center justify-center gap-1">
                  <button
                    @click.stop="viewPdf(order)"
                    class="px-2.5 py-1 bg-blue-600 hover:bg-blue-700 text-white rounded text-xs font-medium flex items-center gap-1 transition-colors"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                    查看PDF
                  </button>
                  <button
                    @click.stop="downloadPdf(order)"
                    class="px-2.5 py-1 bg-slate-700 hover:bg-slate-800 text-white rounded text-xs font-medium flex items-center gap-1 transition-colors"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>
                    下载
                  </button>
                </div>
                <div v-else class="flex items-center justify-center gap-1">
                  <button
                    @click.stop="generatePdf(order)"
                    :disabled="generatingId === order.id"
                    class="px-2.5 py-1 bg-orange-500 hover:bg-orange-600 disabled:opacity-50 text-white rounded text-xs font-medium flex items-center gap-1 transition-colors"
                  >
                    <svg v-if="generatingId === order.id" class="animate-spin" xmlns="http://www.w3.org/2000/svg" width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12a9 9 0 1 1-9-9"/></svg>
                    <svg v-else xmlns="http://www.w3.org/2000/svg" width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/></svg>
                    {{ generatingId === order.id ? '生成中...' : '生成PDF' }}
                  </button>
                </div>
              </td>
            </tr>

            <!-- 展开详情行 -->
            <tr v-if="expandedId === order.id" class="bg-slate-50/80">
              <td colspan="7" class="px-4 py-4">
                <div class="grid grid-cols-3 gap-4">
                  <!-- 左：订单信息 -->
                  <div>
                    <p class="text-xs font-semibold text-slate-500 mb-2 uppercase tracking-wider">订单信息</p>
                    <div class="space-y-1 text-xs text-slate-600">
                      <div class="flex gap-2"><span class="text-slate-400 w-16">形状</span><span>{{ order.sku_mappings?.shape || order.product_shape || '-' }}</span></div>
                      <div class="flex gap-2"><span class="text-slate-400 w-16">颜色</span><span>{{ order.sku_mappings?.color || order.product_color || '-' }}</span></div>
                      <div class="flex gap-2"><span class="text-slate-400 w-16">尺寸</span><span>{{ order.sku_mappings?.size || order.product_size || '-' }}</span></div>
                      <div class="flex gap-2"><span class="text-slate-400 w-16">工艺</span><span>{{ order.sku_mappings?.craft || '-' }}</span></div>
                      <div class="flex gap-2"><span class="text-slate-400 w-16">数量</span><span>{{ order.quantity || 1 }}</span></div>
                    </div>
                  </div>
                  <!-- 中：物流信息 -->
                  <div>
                    <p class="text-xs font-semibold text-slate-500 mb-2 uppercase tracking-wider">物流信息</p>
                    <div class="space-y-1 text-xs text-slate-600">
                      <div class="flex gap-2"><span class="text-slate-400 w-16">物流单号</span><span class="font-mono">{{ order.logistics?.[0]?.tracking_number || '-' }}</span></div>
                      <div class="flex gap-2"><span class="text-slate-400 w-16">收件人</span><span>{{ order.logistics?.[0]?.recipient_name || order.shipping_name || '-' }}</span></div>
                      <div class="flex gap-2"><span class="text-slate-400 w-16">地址</span><span>{{ order.logistics?.[0]?.street_address || order.shipping_address_line1 || '-' }}</span></div>
                      <div class="flex gap-2"><span class="text-slate-400 w-16">城市</span><span>{{ order.logistics?.[0]?.city || order.shipping_city || '-' }}</span></div>
                      <div class="flex gap-2"><span class="text-slate-400 w-16">国家</span><span>{{ order.logistics?.[0]?.country || order.shipping_country || '-' }}</span></div>
                    </div>
                  </div>
                  <!-- 右：生产文档预览 -->
                  <div>
                    <p class="text-xs font-semibold text-slate-500 mb-2 uppercase tracking-wider">生产文档</p>
                    <div v-if="order.production_pdf_url" class="bg-white rounded-lg border border-slate-200 p-3">
                      <div class="bg-slate-100 rounded h-20 flex items-center justify-center mb-2">
                        <div class="text-center">
                          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="1.5" class="mx-auto mb-1"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                          <p class="text-xs text-slate-400">POD_{{ order.etsy_order_id }}.pdf</p>
                        </div>
                      </div>
                      <div class="flex gap-1.5">
                        <button @click="viewPdf(order)" class="flex-1 px-2 py-1 bg-blue-600 hover:bg-blue-700 text-white rounded text-xs font-medium transition-colors">查看</button>
                        <button @click="downloadPdf(order)" class="flex-1 px-2 py-1 bg-slate-700 hover:bg-slate-800 text-white rounded text-xs font-medium transition-colors">下载</button>
                        <button @click="printPdf(order)" class="flex-1 px-2 py-1 bg-white border border-slate-200 hover:bg-slate-50 text-slate-600 rounded text-xs font-medium transition-colors">打印</button>
                      </div>
                    </div>
                    <div v-else class="bg-orange-50 rounded-lg border border-orange-200 p-3 text-center">
                      <p class="text-orange-600 text-xs font-medium mb-2">尚未生成生产文档</p>
                      <button
                        @click="generatePdf(order)"
                        :disabled="generatingId === order.id"
                        class="px-3 py-1.5 bg-orange-500 hover:bg-orange-600 disabled:opacity-50 text-white rounded text-xs font-medium transition-colors"
                      >
                        {{ generatingId === order.id ? '生成中...' : '立即生成PDF' }}
                      </button>
                    </div>
                  </div>
                </div>
              </td>
            </tr>
          </template>

          <tr v-if="!loading && orders.length === 0">
            <td colspan="7" class="px-4 py-12 text-center text-slate-400">
              <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" class="mx-auto mb-3 opacity-30"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
              <p class="text-sm">暂无生产中订单</p>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import supabase from '../../utils/supabase'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const orders = ref([])
const loading = ref(false)
const expandedId = ref(null)
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
    orders.value = data || []
    console.log(`✅ 生产中订单加载: ${orders.value.length} 条`)
  } catch (e) {
    console.error('❌ 加载失败:', e)
  } finally {
    loading.value = false
  }
}

function toggleExpand(id) {
  expandedId.value = expandedId.value === id ? null : id
}

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
      // 更新本地数据
      const idx = orders.value.findIndex(o => o.id === order.id)
      if (idx !== -1) orders.value[idx] = { ...orders.value[idx], production_pdf_url: data.production_pdf_url }
      alert('✅ 生产文档生成成功！')
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

function downloadPdf(order) {
  if (order.production_pdf_url) {
    const a = document.createElement('a')
    a.href = order.production_pdf_url
    a.download = `POD_${order.etsy_order_id}.pdf`
    a.click()
  }
}

function printPdf(order) {
  if (order.production_pdf_url) {
    const w = window.open(order.production_pdf_url, '_blank')
    w.onload = () => w.print()
  }
}

function formatDate(str) {
  if (!str) return '-'
  const d = new Date(str)
  return `${d.getMonth() + 1}/${d.getDate()} ${d.getHours()}:${String(d.getMinutes()).padStart(2, '0')}`
}
</script>
