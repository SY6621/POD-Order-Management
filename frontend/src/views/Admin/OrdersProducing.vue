<template>
  <div class="producing-page">
    <!-- 页面标题 -->
    <header class="page-header">
      <div class="header-left">
        <h1>生产任务</h1>
        <p class="page-desc">下载生产文档 → 生产 → 确认完成</p>
      </div>
      <div class="header-right">
        <span class="task-count">共 {{ totalCount }} 单待生产</span>
      </div>
    </header>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <span>加载中...</span>
    </div>

    <!-- 任务列表 -->
    <div v-else class="task-groups">
      <!-- 今日任务 -->
      <section class="task-group">
        <div class="group-header" @click="toggleGroup('today')">
          <div class="group-title">
            <span class="group-icon">📅</span>
            <span>今日任务</span>
            <span class="group-count">{{ todayOrders.length }}</span>
          </div>
          <span class="expand-icon" :class="{ expanded: expandedGroups.today }">▼</span>
        </div>
        <div v-show="expandedGroups.today" class="group-content">
          <div v-if="todayOrders.length === 0" class="empty-hint">
            暂无今日任务
          </div>
          <div v-else class="task-list">
            <div v-for="order in todayOrders" :key="order.id" class="task-card">
              <div class="task-main">
                <!-- 产品图 -->
                <div class="product-preview">
                  <svg viewBox="0 0 100 100" class="preview-svg">
                    <path :d="getShapePath(order.product_shape)" 
                          :fill="getColorHex(order.product_color)" 
                          stroke="#d1d5db" stroke-width="2"/>
                  </svg>
                </div>
                <!-- 订单信息 -->
                <div class="task-info">
                  <div class="task-id">#{{ order.etsy_order_id }}</div>
                  <div class="task-product">
                    {{ order.product_shape }} · {{ order.product_color }} · {{ order.product_size || '大号' }}
                  </div>
                  <div class="task-customer">{{ order.customer_name }}</div>
                </div>
              </div>
              <!-- 操作按钮 -->
              <div class="task-actions">
                <button 
                  v-if="order.production_pdf_url"
                  class="btn-download"
                  @click="downloadPdf(order)"
                >
                  <span class="btn-icon">📥</span>
                  下载生产文档
                </button>
                <button v-else class="btn-generate" @click="generatePdf(order)" :disabled="generatingId === order.id">
                  <span class="btn-icon">{{ generatingId === order.id ? '⏳' : '📄' }}</span>
                  {{ generatingId === order.id ? '生成中...' : '生成文档' }}
                </button>
                <button class="btn-complete" @click="confirmComplete(order)">
                  <span class="btn-icon">✅</span>
                  确认完成
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 昨日任务 -->
      <section class="task-group">
        <div class="group-header" @click="toggleGroup('yesterday')">
          <div class="group-title">
            <span class="group-icon">📋</span>
            <span>昨日任务</span>
            <span class="group-count">{{ yesterdayOrders.length }}</span>
          </div>
          <span class="expand-icon" :class="{ expanded: expandedGroups.yesterday }">▼</span>
        </div>
        <div v-show="expandedGroups.yesterday" class="group-content">
          <div v-if="yesterdayOrders.length === 0" class="empty-hint">
            暂无昨日任务
          </div>
          <div v-else class="task-list">
            <div v-for="order in yesterdayOrders" :key="order.id" class="task-card">
              <div class="task-main">
                <div class="product-preview">
                  <svg viewBox="0 0 100 100" class="preview-svg">
                    <path :d="getShapePath(order.product_shape)" 
                          :fill="getColorHex(order.product_color)" 
                          stroke="#d1d5db" stroke-width="2"/>
                  </svg>
                </div>
                <div class="task-info">
                  <div class="task-id">#{{ order.etsy_order_id }}</div>
                  <div class="task-product">
                    {{ order.product_shape }} · {{ order.product_color }} · {{ order.product_size || '大号' }}
                  </div>
                  <div class="task-customer">{{ order.customer_name }}</div>
                </div>
              </div>
              <div class="task-actions">
                <button 
                  v-if="order.production_pdf_url"
                  class="btn-download"
                  @click="downloadPdf(order)"
                >
                  <span class="btn-icon">📥</span>
                  下载生产文档
                </button>
                <button v-else class="btn-generate" @click="generatePdf(order)" :disabled="generatingId === order.id">
                  <span class="btn-icon">{{ generatingId === order.id ? '⏳' : '📄' }}</span>
                  {{ generatingId === order.id ? '生成中...' : '生成文档' }}
                </button>
                <button class="btn-complete" @click="confirmComplete(order)">
                  <span class="btn-icon">✅</span>
                  确认完成
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 更早任务 -->
      <section class="task-group" v-if="olderOrders.length > 0">
        <div class="group-header" @click="toggleGroup('older')">
          <div class="group-title">
            <span class="group-icon">📦</span>
            <span>更早任务</span>
            <span class="group-count">{{ olderOrders.length }}</span>
          </div>
          <span class="expand-icon" :class="{ expanded: expandedGroups.older }">▼</span>
        </div>
        <div v-show="expandedGroups.older" class="group-content">
          <div class="task-list">
            <div v-for="order in olderOrders" :key="order.id" class="task-card overdue">
              <div class="task-main">
                <div class="product-preview">
                  <svg viewBox="0 0 100 100" class="preview-svg">
                    <path :d="getShapePath(order.product_shape)" 
                          :fill="getColorHex(order.product_color)" 
                          stroke="#d1d5db" stroke-width="2"/>
                  </svg>
                </div>
                <div class="task-info">
                  <div class="task-id">#{{ order.etsy_order_id }}</div>
                  <div class="task-product">
                    {{ order.product_shape }} · {{ order.product_color }} · {{ order.product_size || '大号' }}
                  </div>
                  <div class="task-customer">{{ order.customer_name }}</div>
                  <div class="task-date">{{ formatDate(order.created_at) }}</div>
                </div>
              </div>
              <div class="task-actions">
                <button 
                  v-if="order.production_pdf_url"
                  class="btn-download"
                  @click="downloadPdf(order)"
                >
                  <span class="btn-icon">📥</span>
                  下载生产文档
                </button>
                <button v-else class="btn-generate" @click="generatePdf(order)" :disabled="generatingId === order.id">
                  <span class="btn-icon">{{ generatingId === order.id ? '⏳' : '📄' }}</span>
                  {{ generatingId === order.id ? '生成中...' : '生成文档' }}
                </button>
                <button class="btn-complete" @click="confirmComplete(order)">
                  <span class="btn-icon">✅</span>
                  确认完成
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 空状态 -->
      <div v-if="!loading && totalCount === 0" class="empty-state">
        <div class="empty-icon">✅</div>
        <div class="empty-text">暂无生产任务</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import supabase from '../../utils/supabase'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const orders = ref([])
const loading = ref(false)
const generatingId = ref(null)
const expandedGroups = ref({
  today: true,
  yesterday: false,
  older: false
})

onMounted(() => loadOrders())

// 按日期分组
const todayOrders = computed(() => {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  return orders.value.filter(o => {
    const d = new Date(o.created_at)
    d.setHours(0, 0, 0, 0)
    return d.getTime() === today.getTime()
  })
})

const yesterdayOrders = computed(() => {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  const yesterday = new Date(today)
  yesterday.setDate(yesterday.getDate() - 1)
  return orders.value.filter(o => {
    const d = new Date(o.created_at)
    d.setHours(0, 0, 0, 0)
    return d.getTime() === yesterday.getTime()
  })
})

const olderOrders = computed(() => {
  const yesterday = new Date()
  yesterday.setHours(0, 0, 0, 0)
  yesterday.setDate(yesterday.getDate() - 1)
  return orders.value.filter(o => {
    const d = new Date(o.created_at)
    d.setHours(0, 0, 0, 0)
    return d.getTime() < yesterday.getTime()
  })
})

const totalCount = computed(() => orders.value.length)

async function loadOrders() {
  loading.value = true
  try {
    const { data, error } = await supabase
      .from('orders')
      .select(`*, sku_mappings:sku_mapping(*)`)
      .in('status', ['待创建', '生产中'])
      .order('created_at', { ascending: false })

    if (error) throw error
    orders.value = data || []
    console.log(`✅ 生产中订单: ${orders.value.length} 条`)
  } catch (e) {
    console.error('❌ 加载失败:', e)
  } finally {
    loading.value = false
  }
}

function toggleGroup(group) {
  expandedGroups.value[group] = !expandedGroups.value[group]
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
      const idx = orders.value.findIndex(o => o.id === order.id)
      if (idx !== -1) orders.value[idx].production_pdf_url = data.production_pdf_url
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

function downloadPdf(order) {
  if (order.production_pdf_url) {
    const a = document.createElement('a')
    a.href = order.production_pdf_url
    a.download = `POD_${order.etsy_order_id}.pdf`
    a.click()
  }
}

async function confirmComplete(order) {
  if (!confirm(`确认订单 #${order.etsy_order_id} 已完成生产？`)) return
  
  try {
    const { error } = await supabase
      .from('orders')
      .update({ status: '已完成', updated_at: new Date().toISOString() })
      .eq('id', order.id)

    if (error) throw error
    
    // 从列表移除
    orders.value = orders.value.filter(o => o.id !== order.id)
    alert('✅ 已标记为完成！')
  } catch (e) {
    alert('❌ 操作失败: ' + e.message)
  }
}

function formatDate(str) {
  if (!str) return ''
  const d = new Date(str)
  return `${d.getMonth() + 1}/${d.getDate()}`
}

// 产品形状路径映射
function getShapePath(shape) {
  const shapes = {
    '圆形': 'M50,10 A40,40 0 1,1 50,90 A40,40 0 1,1 50,10',
    '心形': 'M50,85 C20,60 5,35 25,20 C40,10 50,25 50,25 C50,25 60,10 75,20 C95,35 80,60 50,85',
    '骨头形': 'M25,35 A15,15 0 1,1 25,65 M75,35 A15,15 0 1,1 75,65 M25,50 L75,50',
    '方形': 'M15,15 L85,15 L85,85 L15,85 Z'
  }
  return shapes[shape] || shapes['圆形']
}

// 颜色映射
function getColorHex(color) {
  const colors = {
    '银色': '#C0C0C0',
    '金色': '#FFD700',
    '玫瑰金': '#B76E79',
    '黑色': '#2D2D2D',
    '蓝色': '#4169E1'
  }
  return colors[color] || '#C0C0C0'
}
</script>

<style scoped>
/* 页面容器 */
.producing-page {
  min-height: 100%;
  background: #fafafa;
  padding: 32px 40px;
}

/* 页面标题 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
}

.header-left h1 {
  font-size: 28px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 8px 0;
}

.page-desc {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}

.task-count {
  font-size: 14px;
  color: #6b7280;
  background: #f3f4f6;
  padding: 8px 16px;
  border-radius: 8px;
}

/* 加载状态 */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 0;
  color: #6b7280;
}

.spinner {
  width: 32px;
  height: 32px;
  border: 3px solid #e5e7eb;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 任务分组 */
.task-groups {
  max-width: 900px;
}

.task-group {
  margin-bottom: 16px;
}

.group-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  cursor: pointer;
  transition: background 0.2s;
}

.group-header:hover {
  background: #f9fafb;
}

.group-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 15px;
  font-weight: 600;
  color: #1a1a1a;
}

.group-icon {
  font-size: 18px;
}

.group-count {
  background: #e5e7eb;
  color: #4b5563;
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 500;
}

.expand-icon {
  color: #9ca3af;
  font-size: 12px;
  transition: transform 0.2s;
}

.expand-icon.expanded {
  transform: rotate(180deg);
}

.group-content {
  margin-top: 8px;
}

.empty-hint {
  padding: 24px;
  text-align: center;
  color: #9ca3af;
  font-size: 14px;
}

/* 任务列表 */
.task-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* 任务卡片 */
.task-card {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 20px;
  transition: box-shadow 0.2s;
}

.task-card:hover {
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.task-card.overdue {
  border-color: #fde68a;
  background: #fffbeb;
}

.task-main {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 16px;
}

/* 产品预览 */
.product-preview {
  width: 64px;
  height: 64px;
  background: #f9fafb;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.preview-svg {
  width: 48px;
  height: 48px;
}

/* 任务信息 */
.task-info {
  flex: 1;
  min-width: 0;
}

.task-id {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 4px;
}

.task-product {
  font-size: 14px;
  color: #4b5563;
  margin-bottom: 2px;
}

.task-customer {
  font-size: 13px;
  color: #6b7280;
}

.task-date {
  font-size: 12px;
  color: #9ca3af;
  margin-top: 4px;
}

/* 操作按钮 */
.task-actions {
  display: flex;
  gap: 12px;
}

.btn-download,
.btn-generate,
.btn-complete {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-download {
  background: #1a1a1a;
  color: #ffffff;
}

.btn-download:hover {
  background: #374151;
}

.btn-generate {
  background: #f59e0b;
  color: #ffffff;
}

.btn-generate:hover:not(:disabled) {
  background: #d97706;
}

.btn-generate:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-complete {
  background: #22c55e;
  color: #ffffff;
}

.btn-complete:hover {
  background: #16a34a;
}

.btn-icon {
  font-size: 16px;
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 0;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.empty-text {
  font-size: 16px;
  color: #6b7280;
}
</style>
