<template>
  <div class="service-link-page">
    <!-- 顶部导航 -->
    <header class="page-header">
      <div class="header-content">
        <div class="shop-info">
          <div class="shop-icon">📧</div>
          <div class="shop-details">
            <h1>{{ shopInfo?.name || '店铺订单中心' }}</h1>
            <p class="shop-code">{{ shopCode?.toUpperCase() }}</p>
          </div>
        </div>
        <div class="header-actions">
          <el-button 
            v-if="designLinkEnabled" 
            type="warning" 
            @click="goToDesignLink"
          >
            <el-icon><Edit /></el-icon>修改设计
          </el-button>
        </div>
      </div>
    </header>

    <!-- 统计卡片 -->
    <div class="stats-bar">
      <div class="stat-card">
        <span class="stat-label">全部订单</span>
        <span class="stat-value">{{ orders.length }}</span>
      </div>
      <div class="stat-card pending">
        <span class="stat-label">待确认</span>
        <span class="stat-value">{{ pendingCount }}</span>
      </div>
      <div class="stat-card sent">
        <span class="stat-label">已发送</span>
        <span class="stat-value">{{ sentCount }}</span>
      </div>
      <div class="stat-card confirmed">
        <span class="stat-label">已确认</span>
        <span class="stat-value">{{ confirmedCount }}</span>
      </div>
      <div class="stat-card modify">
        <span class="stat-label">需修改</span>
        <span class="stat-value">{{ modifyCount }}</span>
      </div>
    </div>

    <!-- 主内容 -->
    <main class="main-content">
      <!-- 左侧：订单列表 -->
      <aside class="order-list-panel">
        <div class="panel-header">
          <h3>订单列表</h3>
          <span class="panel-hint">点击订单查看详情</span>
        </div>
        <div class="order-list">
          <div
            v-for="order in orders"
            :key="order.id"
            class="order-item"
            :class="{ active: selectedOrder?.id === order.id }"
            @click="selectOrder(order)"
          >
            <div class="order-header">
              <span class="order-id">{{ order.etsy_order_id }}</span>
              <el-tag :type="getEmailStatusType(order.email_status)" size="small">
                {{ getEmailStatusText(order.email_status) }}
              </el-tag>
            </div>
            <div class="order-product">
              <span class="product-shape">{{ order.product_shape }}</span>
              <span class="product-color">{{ order.product_color }}</span>
            </div>
            <div class="order-text">
              正面: {{ order.front_text }} | 背面: {{ order.back_text }}
            </div>
            <div class="order-time">
              <el-icon><Clock /></el-icon>
              下单: {{ formatTime(order.etsy_order_time) }}
            </div>
          </div>
        </div>
      </aside>

      <!-- 中间：订单详情 -->
      <section class="detail-panel">
        <div v-if="!selectedOrder" class="empty-state">
          <el-empty description="请选择左侧订单查看详情" />
        </div>
        <div v-else class="detail-content">
          <!-- 详情头部 -->
          <div class="detail-header">
            <h3>订单详情</h3>
            <span class="order-number">{{ selectedOrder.etsy_order_id }}</span>
            <el-tag :type="getEmailStatusType(selectedOrder.email_status)">
              {{ getEmailStatusText(selectedOrder.email_status) }}
            </el-tag>
          </div>

          <!-- 效果图预览 -->
          <div class="effect-section">
            <h4>📷 效果图预览</h4>
            <div class="effect-preview">
              <div class="preview-placeholder">
                <svg viewBox="0 0 100 100" class="preview-svg">
                  <path d="M50 15 C30 15 15 30 15 50 C15 75 50 90 50 90 C50 90 85 75 85 50 C85 30 70 15 50 15Z" 
                        fill="#fbbf24" stroke="#f59e0b" stroke-width="2"/>
                  <text x="50" y="45" text-anchor="middle" font-size="14" fill="#374151">{{ selectedOrder.front_text }}</text>
                  <circle cx="50" cy="25" r="4" fill="#e5e7eb"/>
                </svg>
                <p class="preview-label">{{ selectedOrder.product_shape }} - {{ selectedOrder.product_color }} · 正面</p>
              </div>
            </div>
            
            <!-- 产品信息 -->
            <div class="product-info">
              <div class="info-row">
                <span class="info-label">客户：</span>
                <span class="info-value">{{ selectedOrder.customer_name }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">产品：</span>
                <span class="info-value">{{ selectedOrder.sku }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">尺寸：</span>
                <span class="info-value">{{ selectedOrder.size }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">下单时间：</span>
                <span class="info-value">{{ formatTime(selectedOrder.etsy_order_time) }}</span>
              </div>
              <div v-if="selectedOrder.created_at" class="info-row">
                <span class="info-label">创建时间：</span>
                <span class="info-value">{{ formatTime(selectedOrder.created_at) }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 右侧：邮件与操作 -->
      <aside class="action-panel">
        <div class="panel-header">
          <h3>📧 邮件内容</h3>
        </div>
        <div v-if="!selectedOrder" class="empty-state">
          <el-empty description="选择订单查看邮件" :image-size="80" />
        </div>
        <div v-else class="action-content">
          <!-- 邮件预览 -->
          <div class="email-preview">
            <div class="email-body">
              <p>Hi {{ selectedOrder.customer_name }}!</p>
              <p>Thank you for your order! Here is the preview of your custom pet tag:</p>
              <p><strong>Front:</strong> {{ selectedOrder.front_text }}</p>
              <p><strong>Back:</strong> {{ selectedOrder.back_text }}</p>
              <p>Please confirm the design looks correct, or let us know if you need any changes.</p>
              <p>Best regards,<br>Customer Support Team</p>
            </div>
          </div>

          <!-- 客服操作 -->
          <div class="action-section">
            <h4>🔘 客服操作</h4>
            
            <!-- 主操作按钮 -->
            <div class="action-buttons">
              <el-button 
                type="primary" 
                size="large"
                :disabled="selectedOrder.email_status === 'sent'"
                @click="sendEmail"
              >
                <el-icon><Message /></el-icon>
                {{ selectedOrder.email_status === 'sent' ? '已发送' : '我已发送邮件' }}
              </el-button>
              <el-button 
                type="success" 
                size="large"
                :disabled="selectedOrder.email_status !== 'sent'"
                @click="confirmOrder"
              >
                <el-icon><Check /></el-icon>客户已确认
              </el-button>
            </div>
            
            <!-- 修改按钮 -->
            <el-button 
              v-if="designLinkEnabled"
              class="modify-btn"
              @click="goToDesignLink"
            >
              <el-icon><Edit /></el-icon>客户需修改 - 前往设计链接
            </el-button>

            <!-- 创建订单按钮（客户确认后显示） -->
            <el-button 
              v-if="selectedOrder.email_status === 'confirmed'"
              type="warning" 
              size="large"
              class="create-order-btn"
              @click="createOrder"
            >
              <el-icon><Plus /></el-icon>创建订单
            </el-button>
          </div>

          <!-- 操作历史 -->
          <div class="history-section">
            <h4>📋 操作历史</h4>
            <div class="history-list">
              <div v-for="(log, index) in operationLogs" :key="index" class="history-item">
                <span class="history-time">{{ log.time }}</span>
                <el-tag :type="log.type" size="small">{{ log.label }}</el-tag>
                <span class="history-text">{{ log.text }}</span>
              </div>
            </div>
          </div>
        </div>
      </aside>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Clock, Edit, Message, Check, Plus } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

// 状态
const loading = ref(true)
const shopInfo = ref(null)
const designLinkEnabled = ref(true)
const orders = ref([])
const selectedOrder = ref(null)
const operationLogs = ref([])

// 从URL获取参数
const shopCode = computed(() => route.params.shopCode)
const token = computed(() => route.query.token)

// 统计
const pendingCount = computed(() => orders.value.filter(o => o.email_status === 'pending').length)
const sentCount = computed(() => orders.value.filter(o => o.email_status === 'sent').length)
const confirmedCount = computed(() => orders.value.filter(o => o.email_status === 'confirmed').length)
const modifyCount = computed(() => orders.value.filter(o => o.email_status === 'modify').length)

// 验证Token并获取店铺信息
async function validateAndLoad() {
  try {
    // TODO: 调用后端API验证token
    // 模拟数据
    shopInfo.value = {
      name: '美国店铺',
      code: shopCode.value
    }
    designLinkEnabled.value = true
    
    // 加载订单
    orders.value = [
      {
        id: '1',
        etsy_order_id: '4002217518',
        customer_name: 'Jessica Head',
        customer_email: 'jessica@example.com',
        product_shape: '心形',
        product_color: '金色',
        front_text: 'KYLA',
        back_text: 'If Lost 13999926688',
        sku: 'B-G01B',
        size: 'L (32mm)',
        email_status: 'sent',
        etsy_order_time: '2025-03-25T14:30:00Z',
        created_at: null
      },
      {
        id: '2',
        etsy_order_id: '3986891868',
        customer_name: 'Tom Smith',
        customer_email: 'tom@example.com',
        product_shape: '圆形',
        product_color: '银色',
        front_text: 'TOM',
        back_text: '13800138000',
        sku: 'B-S02S',
        size: 'M (28mm)',
        email_status: 'pending',
        etsy_order_time: '2025-03-25T10:15:00Z',
        created_at: null
      },
      {
        id: '3',
        etsy_order_id: '4002234567',
        customer_name: 'Luna Wang',
        customer_email: 'luna@example.com',
        product_shape: '骨头形',
        product_color: '玫瑰金',
        front_text: 'LUNA',
        back_text: '13987654321',
        sku: 'B-B03R',
        size: 'S (25mm)',
        email_status: 'modify',
        etsy_order_time: '2025-03-24T16:45:00Z',
        created_at: '2025-03-24T18:00:00Z'
      }
    ]
    
    operationLogs.value = [
      { time: '14:32', type: 'primary', label: '邮件', text: '客服发送确认邮件给客户' },
      { time: '14:30', type: 'success', label: '设计', text: '设计师生成效果图' },
      { time: '14:15', type: 'warning', label: '订单', text: '订单创建，等待处理' }
    ]
    
    if (orders.value.length > 0) {
      selectedOrder.value = orders.value[0]
    }
  } catch (e) {
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

// 选择订单
function selectOrder(order) {
  selectedOrder.value = order
}

// 前往设计链接
function goToDesignLink() {
  router.push(`/design/${shopCode.value}?token=${token.value}`)
}

// 发送邮件
async function sendEmail() {
  try {
    await ElMessageBox.confirm('确认已发送邮件给客户？', '提示', {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'info'
    })
    selectedOrder.value.email_status = 'sent'
    ElMessage.success('邮件状态已更新')
  } catch {
    // 取消
  }
}

// 客户确认
async function confirmOrder() {
  try {
    await ElMessageBox.confirm('客户已确认设计？', '提示', {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'success'
    })
    selectedOrder.value.email_status = 'confirmed'
    ElMessage.success('订单已确认')
  } catch {
    // 取消
  }
}

// 创建订单
async function createOrder() {
  try {
    await ElMessageBox.confirm('确认创建订单？创建后将跳转至物流下单页面。', '提示', {
      confirmButtonText: '确认创建',
      cancelButtonText: '取消',
      type: 'warning'
    })
    // TODO: 调用后端API创建订单
    ElMessage.success('订单创建成功，跳转至物流下单...')
    // 跳转到物流下单页面
    router.push('/admin/orders/shipping')
  } catch {
    // 取消
  }
}

// 获取邮件状态类型
function getEmailStatusType(status) {
  const map = {
    pending: 'info',
    sent: 'primary',
    confirmed: 'success',
    modify: 'danger'
  }
  return map[status] || 'info'
}

// 获取邮件状态文本
function getEmailStatusText(status) {
  const map = {
    pending: '草稿',
    sent: '已发送',
    confirmed: '已确认',
    modify: '需修改'
  }
  return map[status] || status
}

// 格式化时间
function formatTime(timeStr) {
  if (!timeStr) return '--'
  const date = new Date(timeStr)
  return `${date.getFullYear()}/${(date.getMonth() + 1).toString().padStart(2, '0')}/${date.getDate().toString().padStart(2, '0')} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
}

// 初始化
onMounted(() => {
  validateAndLoad()
})
</script>

<style scoped>
/* Notion 风格 */
.service-link-page {
  min-height: 100vh;
  background: #fbfbfa;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* 顶部导航 */
.page-header {
  background: #ffffff;
  border-bottom: 1px solid #e3e2e0;
  padding: 16px 32px;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 1550px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.shop-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.shop-icon {
  width: 40px;
  height: 40px;
  background: #dbeafe;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.shop-details h1 {
  font-size: 18px;
  font-weight: 600;
  color: #37352f;
  margin: 0;
}

.shop-code {
  font-size: 13px;
  color: #6b7280;
  margin: 2px 0 0 0;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

/* 统计栏 */
.stats-bar {
  max-width: 1550px;
  margin: 24px auto;
  padding: 0 32px;
  display: flex;
  gap: 16px;
}

.stat-card {
  background: #ffffff;
  border: 1px solid #e3e2e0;
  border-radius: 8px;
  padding: 16px 24px;
  min-width: 100px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
}

.stat-card.pending { border-left: 4px solid #f59e0b; }
.stat-card.sent { border-left: 4px solid #3b82f6; }
.stat-card.confirmed { border-left: 4px solid #10b981; }
.stat-card.modify { border-left: 4px solid #ef4444; }

.stat-label {
  font-size: 13px;
  color: #6b7280;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #37352f;
}

/* 主内容 - 1550px */
.main-content {
  max-width: 1550px;
  margin: 0 auto;
  padding: 0 32px 32px;
  display: flex;
  gap: 20px;
  height: calc(100vh - 220px);
}

/* 左侧面板 */
.order-list-panel {
  width: 320px;
  background: #ffffff;
  border: 1px solid #e3e2e0;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.panel-header {
  padding: 16px;
  border-bottom: 1px solid #f1f1ef;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.panel-header h3 {
  font-size: 14px;
  font-weight: 600;
  color: #37352f;
  margin: 0;
}

.panel-hint {
  font-size: 12px;
  color: #9ca3af;
}

.order-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.order-item {
  padding: 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.15s ease;
  border: 1px solid transparent;
  margin-bottom: 8px;
}

.order-item:hover {
  background: #f9fafb;
  border-color: #e5e7eb;
}

.order-item.active {
  background: #eff6ff;
  border-color: #3b82f6;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.order-id {
  font-family: monospace;
  font-size: 13px;
  font-weight: 600;
  color: #37352f;
}

.order-product {
  display: flex;
  gap: 8px;
  font-size: 12px;
  color: #6b7280;
  margin-bottom: 4px;
}

.order-text {
  font-size: 11px;
  color: #9ca3af;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 4px;
}

.order-time {
  font-size: 11px;
  color: #9ca3af;
  display: flex;
  align-items: center;
  gap: 4px;
}

/* 中间面板 */
.detail-panel {
  flex: 1;
  background: #ffffff;
  border: 1px solid #e3e2e0;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.detail-content {
  padding: 20px;
}

.detail-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f1f1ef;
}

.detail-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: #37352f;
  margin: 0;
}

.order-number {
  font-family: monospace;
  font-size: 14px;
  color: #6b7280;
}

.effect-section h4 {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
  margin: 0 0 16px 0;
}

.effect-preview {
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 20px;
}

.preview-placeholder {
  text-align: center;
}

.preview-svg {
  width: 120px;
  height: 120px;
  margin: 0 auto 12px;
}

.preview-label {
  font-size: 13px;
  color: #6b7280;
}

.product-info {
  space-y: 8px;
}

.info-row {
  display: flex;
  font-size: 13px;
  margin-bottom: 8px;
}

.info-label {
  color: #9ca3af;
  min-width: 80px;
}

.info-value {
  color: #374151;
  font-weight: 500;
}

/* 右侧面板 */
.action-panel {
  width: 380px;
  background: #ffffff;
  border: 1px solid #e3e2e0;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.action-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.email-preview {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 20px;
  font-size: 13px;
  line-height: 1.6;
  color: #374151;
}

.email-body p {
  margin: 8px 0;
}

.action-section h4 {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
  margin: 0 0 12px 0;
}

.action-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  margin-bottom: 12px;
}

.modify-btn {
  width: 100%;
  margin-bottom: 12px;
  background: #fdf2f8;
  border-color: #f9a8d4;
  color: #db2777;
}

.modify-btn:hover {
  background: #fce7f3;
  border-color: #f472b6;
}

.create-order-btn {
  width: 100%;
  margin-top: 12px;
}

.history-section {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #f1f1ef;
}

.history-section h4 {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
  margin: 0 0 12px 0;
}

.history-list {
  space-y: 8px;
}

.history-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  margin-bottom: 8px;
}

.history-time {
  color: #9ca3af;
  min-width: 40px;
}

.history-text {
  color: #6b7280;
}

/* 空状态 */
.empty-state {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
