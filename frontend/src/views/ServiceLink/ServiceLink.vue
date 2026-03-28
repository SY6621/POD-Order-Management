<template>
  <div class="service-link-page">
    <!-- 顶部导航 -->
    <header class="page-header">
      <div class="header-content">
        <div class="shop-info">
          <h1>{{ shopInfo?.name || '店铺订单中心' }}</h1>
          <span class="shop-lang">{{ shopCode?.toUpperCase() || 'US' }}</span>
        </div>
        <div class="header-actions">
          <el-button
            v-if="designLinkEnabled"
            type="warning"
            class="modify-design-btn"
            @click="goToDesignLink"
          >
            <span class="btn-icon">✅</span>修改设计
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
            <h3>订单详情 {{ selectedOrder.etsy_order_id }}</h3>
            <el-tag :type="getEmailStatusType(selectedOrder.email_status)">
              {{ getEmailStatusText(selectedOrder.email_status) }}
            </el-tag>
          </div>

          <!-- 订单详情区域 -->
          <div class="order-detail-section">
            <!-- 效果图预览 - 蓝框：放大到与订单信息块同宽 -->
            <div class="effect-section">
              <h4>📷 效果图预览</h4>
              <div class="effect-preview hero">
                <div class="preview-placeholder">
                  <div class="preview-image hero-image">
                    <svg viewBox="0 0 100 100" class="preview-svg">
                      <path :d="getShapePath(selectedOrder.product_shape)"
                            :fill="getColorHex(selectedOrder.product_color)"
                            :stroke="getColorStroke(selectedOrder.product_color)"
                            stroke-width="2"/>
                      <text x="50" y="50" text-anchor="middle" font-size="16" fill="#374151" dy=".3em">{{ selectedOrder.front_text }}</text>
                    </svg>
                  </div>
                  <el-button size="small" class="download-btn">下载 JPG</el-button>
                </div>
              </div>
            </div>

            <!-- 订单信息块 - 红框：在蓝框下方 -->
            <div class="order-card compact align-left">
              <!-- 绿框：客户信息 - 放在最上面 -->
              <div class="order-card-header">
                <a href="#" class="user-link">{{ selectedOrder.customer_name }}</a>
                <span class="order-id">#{{ selectedOrder.etsy_order_id }}</span>
              </div>
              
              <!-- 内容区域 -->
              <div class="order-card-content">
                <!-- 左侧：图片和标题 -->
                <div class="order-card-left">
                  <div class="product-img-wrapper">
                    <svg viewBox="0 0 24 24" class="product-icon">
                      <path :d="getShapePath(selectedOrder.product_shape)" 
                            :fill="getColorHex(selectedOrder.product_color)" 
                            stroke="#d1d5db" 
                            stroke-width="1"/>
                    </svg>
                  </div>
                  <div class="product-text">
                    <span class="tag-custom">可个性化</span>
                    <h2 class="product-title-zh">定制{{ selectedOrder.product_shape }}宠物身份牌：深雕不锈钢珐琅</h2>
                    <p class="product-title-en">Custom {{ selectedOrder.product_shape }} Pet ID Tag:</p>
                    <p class="product-title-en last">Deep Engraved Stainless Steel with Enamel</p>
                  </div>
                </div>

                <!-- 右侧：规格详情 -->
                <div class="order-card-right">
                  <div class="info-row">
                    <span class="info-label">数量</span>
                    <span class="info-value">{{ selectedOrder.quantity || 1 }}</span>
                  </div>
                  <div class="info-row">
                    <span class="info-label">颜色 + 尺寸:</span>
                    <span class="info-value">{{ selectedOrder.product_color }}{{ selectedOrder.size || '大号' }}</span>
                  </div>
                  <div class="info-row">
                    <span class="info-label">雕刻面:</span>
                    <span class="info-value">{{ selectedOrder.engraving_sides || '双面' }}</span>
                  </div>
                  <div class="info-row last">
                    <span class="info-label">个性化信息</span>
                    <span class="info-value">正面: {{ selectedOrder.front_text }}<br>背面: {{ selectedOrder.back_text }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- 修改设计下拉框 -->
            <div class="design-collapsible">
              <!-- 绿色按钮行 -->
              <div class="design-button-row">
                <el-button 
                  type="success" 
                  size="small"
                  class="design-toggle-btn"
                  @click="toggleDesignPanel"
                >
                  <span class="btn-icon">✏️</span>
                  <span>修改设计</span>
                  <el-icon class="btn-arrow" :class="{ rotate: showDesignPanel }"><ArrowDown /></el-icon>
                </el-button>
              </div>
              <!-- 当前订单信息 - 在按钮下方 -->
              <div class="current-order-info">
                当前订单：{{ selectedOrder.etsy_order_id }} 客户：{{ selectedOrder.customer_name }}
              </div>
              
              <!-- 下拉内容 -->
              <div v-show="showDesignPanel" class="design-content">
                <!-- 客户修改意见 -->
                <div class="customer-feedback">
                  <h4>客户修改意见</h4>
                  <div class="feedback-form">
                    <el-input
                      v-model="customerFeedback"
                      type="textarea"
                      :rows="3"
                      placeholder="将客户的修改要求贴贴/填写至此处..."
                      class="feedback-input"
                    />
                    <div class="reference-upload">
                      <div class="upload-area">
                        <span class="upload-icon">📁</span>
                        <span class="upload-text">点击上传 JPG / PNG • 最大 2MB</span>
                      </div>
                    </div>
                  </div>
                  <div class="design-actions">
                    <el-button type="primary" class="submit-btn" @click="submitDesign">
                      <span>✅</span> 提交设计处理
                    </el-button>
                    <el-button type="success" class="edit-btn" @click="goToDesignLink">
                      <span>🎨</span> 编辑当前设计
                    </el-button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 右侧：邮件与操作 -->
      <aside class="action-panel">
        <!-- 邮件内容 -->
        <div class="panel-section email-section">
          <div class="panel-header">
            <h3>📧 邮件内容</h3>
          </div>
          <div v-if="!selectedOrder" class="empty-state">
            <el-empty description="选择订单查看邮件" :image-size="60" />
          </div>
          <div v-else class="email-preview">
            <div class="email-body">
              <p>Hi {{ selectedOrder.customer_name }}!</p>
              <p>Thank you for your order! Here is the preview of your custom pet tag:</p>
              <p><strong>Front:</strong> {{ selectedOrder.front_text }}</p>
              <p><strong>Back:</strong> {{ selectedOrder.back_text }}</p>
              <p>Please confirm the design looks correct, or let us know if you need any changes.</p>
              <p>Best regards,<br>Customer Support Team</p>
            </div>
            <el-button size="small" class="copy-btn" @click="copyEmail">复制</el-button>
          </div>
        </div>

        <!-- 操作历史 -->
        <div class="panel-section history-section">
          <div class="panel-header">
            <h3>📋 操作历史</h3>
          </div>
          <div v-if="!selectedOrder" class="empty-state">
            <el-empty description="暂无记录" :image-size="60" />
          </div>
          <div v-else class="history-timeline">
            <div v-for="(log, index) in operationLogs" :key="index" class="history-item">
              <span class="history-time">{{ log.time }}</span>
              <span class="history-icon">{{ getLogIcon(log.type) }}</span>
              <div class="history-content">
                <span class="history-label">{{ log.label }}</span>
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
import { Clock, Edit, ArrowDown } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

// 状态
const loading = ref(true)
const shopInfo = ref(null)
const designLinkEnabled = ref(true)
const orders = ref([])
const selectedOrder = ref(null)
const operationLogs = ref([])
const customerFeedback = ref('')
const showDesignPanel = ref(false) // 修改设计面板显示状态

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
        size: '大号',
        quantity: 1,
        engraving_sides: '双面',
        brand_name: 'Marinella Nesso',
        email_status: 'sent',
        etsy_order_time: '2025-03-25T22:30:00Z',
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
        size: '大号',
        quantity: 1,
        engraving_sides: '双面',
        brand_name: 'Marinella Nesso',
        email_status: 'pending',
        etsy_order_time: '2025-03-25T18:15:00Z',
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
        size: '大号',
        quantity: 1,
        engraving_sides: '双面',
        brand_name: 'Marinella Nesso',
        email_status: 'modify',
        etsy_order_time: '2025-03-25T00:45:00Z',
        created_at: '2025-03-25T02:00:00Z'
      }
    ]

    operationLogs.value = [
      { time: '14:32', type: 'email', label: '邮件', text: '客服发送确认邮件给客户' },
      { time: '14:30', type: 'design', label: '设计', text: '设计师生成效果图' },
      { time: '14:15', type: 'order', label: '订单', text: '订单创建，等待处理' }
    ]

    if (orders.value.length > 1) {
      selectedOrder.value = orders.value[1] // 默认选中第二条（草稿状态）
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
  customerFeedback.value = ''
  showDesignPanel.value = false // 切换订单时关闭面板
}

// 切换修改设计面板
function toggleDesignPanel() {
  showDesignPanel.value = !showDesignPanel.value
}

// 前往设计链接
function goToDesignLink() {
  router.push(`/design/${shopCode.value}?token=${token.value}`)
}

// 处理设计下拉操作
function handleDesignAction(command) {
  if (command === 'edit') {
    goToDesignLink()
  } else if (command === 'resend') {
    ElMessage.success('设计已回传系统')
  }
}

// 提交设计处理
function submitDesign() {
  if (!customerFeedback.value.trim()) {
    ElMessage.warning('请填写客户修改意见')
    return
  }
  ElMessage.success('设计处理已提交')
  customerFeedback.value = ''
}

// 复制邮件
function copyEmail() {
  const emailContent = `Hi ${selectedOrder.value.customer_name}!
Thank you for your order! Here is the preview of your custom pet tag:
Front: ${selectedOrder.value.front_text}
Back: ${selectedOrder.value.back_text}
Please confirm the design looks correct, or let us know if you need any changes.
Best regards,
Customer Support Team`
  navigator.clipboard.writeText(emailContent)
  ElMessage.success('邮件内容已复制')
}

// 获取日志图标
function getLogIcon(type) {
  const icons = {
    email: '📧',
    design: '✍️',
    order: '📝'
  }
  return icons[type] || '📋'
}

// 获取形状路径
function getShapePath(shape) {
  const paths = {
    '心形': 'M50 85 C20 55 0 35 15 20 C30 5 45 15 50 25 C55 15 70 5 85 20 C100 35 80 55 50 85Z',
    '圆形': 'M50 10 A40 40 0 1 1 50 90 A40 40 0 1 1 50 10',
    '骨头形': 'M15 50 L25 30 L35 50 L25 70 Z M65 50 L75 30 L85 50 L75 70 Z M30 35 L70 35 L70 65 L30 65 Z',
    '方形': 'M15 15 L85 15 L85 85 L15 85 Z'
  }
  return paths[shape] || paths['圆形']
}

// 获取颜色值
function getColorHex(color) {
  const colors = {
    '金色': '#fbbf24',
    '银色': '#9ca3af',
    '玫瑰金': '#f472b6',
    '黑色': '#374151',
    '蓝色': '#3b82f6'
  }
  return colors[color] || '#fbbf24'
}

function getColorStroke(color) {
  const colors = {
    '金色': '#f59e0b',
    '银色': '#6b7280',
    '玫瑰金': '#ec4899',
    '黑色': '#1f2937',
    '蓝色': '#2563eb'
  }
  return colors[color] || '#f59e0b'
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
/* Notion 风格基础 */
.service-link-page {
  min-height: 100vh;
  background: #f7f7f7;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* 顶部导航 */
.page-header {
  background: #ffffff;
  border-bottom: 1px solid #e5e5e5;
  padding: 12px 32px;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 1600px;
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

.shop-info h1 {
  font-size: 20px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
}

.shop-lang {
  background: #e8f0fe;
  color: #1a73e8;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.modify-design-btn {
  background: #f97316 !important;
  border-color: #f97316 !important;
  color: #ffffff !important;
  border-radius: 6px;
  font-weight: 500;
}

.modify-design-btn:hover {
  background: #ea580c !important;
  border-color: #ea580c !important;
}

.btn-icon {
  margin-right: 6px;
}

/* 统计栏 */
.stats-bar {
  max-width: 1600px;
  margin: 20px auto;
  padding: 0 32px;
  display: flex;
  gap: 12px;
}

.stat-card {
  background: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  padding: 12px 20px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
}

.stat-card.pending { border-left: 4px solid #f97316; }
.stat-card.sent { border-left: 4px solid #3b82f6; }
.stat-card.confirmed { border-left: 4px solid #22c55e; }
.stat-card.modify { border-left: 4px solid #ef4444; }

.stat-label {
  font-size: 13px;
  color: #666666;
}

.stat-value {
  font-size: 28px;
  font-weight: 600;
  color: #1a1a1a;
}

/* 主内容 */
.main-content {
  max-width: 1600px;
  margin: 0 auto;
  padding: 0 32px 32px;
  display: flex;
  gap: 16px;
  height: calc(100vh - 200px);
}

/* 左侧面板 - 订单列表 */
.order-list-panel {
  width: 340px;
  background: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.panel-header {
  padding: 14px 16px;
  border-bottom: 1px solid #f0f0f0;
}

.panel-header h3 {
  font-size: 14px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
}

.panel-hint {
  font-size: 12px;
  color: #999999;
  display: block;
  margin-top: 2px;
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
  margin-bottom: 6px;
}

.order-item:hover {
  background: #f8f8f8;
}

.order-item.active {
  background: #e8f4ff;
  border-color: #b3d7ff;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.order-id {
  font-family: 'SF Mono', Consolas, monospace;
  font-size: 13px;
  font-weight: 600;
  color: #1a1a1a;
}

.order-product {
  display: flex;
  gap: 8px;
  font-size: 12px;
  color: #666666;
  margin-bottom: 4px;
}

.order-text {
  font-size: 11px;
  color: #999999;
  margin-bottom: 4px;
}

.order-time {
  font-size: 11px;
  color: #999999;
  display: flex;
  align-items: center;
  gap: 4px;
}

/* 中间面板 - 订单详情 */
.detail-panel {
  flex: 1;
  background: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.detail-content {
  padding: 20px;
  overflow-y: auto;
  flex: 1;
}

.detail-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.detail-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
}

/* 效果图预览 - 蓝框：增加高度，作为主体 */
.effect-section h4 {
  font-size: 14px;
  font-weight: 600;
  color: #333333;
  margin: 0 0 12px 0;
}

/* 订单详情区域 - 包含蓝框和红框 */
.order-detail-section {
  display: flex;
  flex-direction: column;
}

/* 效果图预览 - 蓝框：放大 */
.effect-section {
  margin-bottom: 12px;
}

.effect-section h4 {
  font-size: 14px;
  font-weight: 600;
  color: #333333;
  margin: 0 0 12px 0;
}

.effect-preview {
  background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%);
  border-radius: 8px;
  padding: 20px;
  text-align: center;
}

/* 效果图主体高度 - 更大 */
.effect-preview.hero {
  padding: 48px 20px;
  min-height: 320px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.preview-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.preview-image {
  width: 140px;
  height: 140px;
  background: #ffffff;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

/* 效果图主体图片更大 */
.preview-image.hero-image {
  width: 220px;
  height: 220px;
  border-radius: 16px;
}

.preview-svg {
  width: 120px;
  height: 120px;
}

.preview-image.hero-image .preview-svg {
  width: 180px;
  height: 180px;
}

.download-btn {
  background: #ffffff !important;
  border: 1px solid #d1d5db !important;
  color: #374151 !important;
  border-radius: 4px;
}

/* 订单信息块样式 - 红框：紧凑版本 */
.order-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  display: flex;
  flex-direction: column;
}

/* 紧凑版本 - 缩小字号和间距 */
.order-card.compact {
  padding: 12px 16px;
}

/* 向左对齐 */
.order-card.align-left {
  align-items: stretch;
}

/* 绿框：客户信息头部 - 放在最上面 */
.order-card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
  padding-bottom: 10px;
  border-bottom: 1px solid #f0f0f0;
}

.order-card-header .user-link {
  color: #6b7280;
  text-decoration: underline;
  font-size: 13px;
  cursor: pointer;
}

.order-card-header .user-link:hover {
  color: #374151;
}

.order-card-header .order-id {
  color: #374151;
  font-size: 13px;
}

/* 旧样式兼容 */
.order-card-footer {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid #f0f0f0;
}

.order-card-footer .user-link {
  color: #6b7280;
  text-decoration: underline;
  font-size: 13px;
  cursor: pointer;
}

.order-card-footer .user-link:hover {
  color: #374151;
}

.order-card-footer .order-id {
  color: #374151;
  font-size: 13px;
}

.order-card-content {
  display: flex;
  gap: 20px;
  align-items: flex-end;
}

.order-card-left {
  display: flex;
  flex: 1;
  gap: 12px;
  align-items: flex-end;
}

.product-img-wrapper {
  width: 120px;
  height: 120px;
  border-radius: 8px;
  background-color: #f3f4f6;
  border: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.product-icon {
  width: 60px;
  height: 60px;
}

.product-text {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}

.tag-custom {
  background-color: #e5e7eb;
  color: #4b5563;
  padding: 2px 6px;
  border-radius: 10px;
  font-size: 11px;
  display: inline-block;
  margin-bottom: 4px;
  width: fit-content;
}

.product-title-zh {
  font-weight: 500;
  color: #111827;
  font-size: 13px;
  margin: 0 0 2px 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.product-title-en {
  color: #6b7280;
  font-size: 12px;
  line-height: 1.3;
  margin: 0;
}

.product-title-en.last {
  margin-top: 2px;
}

.order-card-right {
  width: 240px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}

.info-row {
  margin-bottom: 4px;
  display: flex;
  align-items: flex-start;
  font-size: 12px;
}

.info-row.last {
  margin-bottom: 0;
}

.info-label {
  color: #9ca3af;
  min-width: 70px;
}

.info-value {
  color: #111827;
  font-weight: 500;
}

/* 紧凑版本内容 */
.order-card.compact .order-card-content {
  gap: 16px;
}

.order-card.compact .product-img-wrapper {
  width: 120px;
  height: 120px;
}

.order-card.compact .product-icon {
  width: 60px;
  height: 60px;
}

.order-card.compact .product-title-zh {
  font-size: 12px;
}

.order-card.compact .product-title-en {
  font-size: 11px;
}

.order-card.compact .info-row {
  font-size: 11px;
  margin-bottom: 3px;
}

.order-card.compact .info-label {
  min-width: 60px;
}

/* 旧的产品卡片样式（兼容保留） */
.product-card {
  background: #fafafa;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
}

.product-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.brand-name {
  font-weight: 600;
  color: #1a1a1a;
}

.order-number {
  font-family: monospace;
  color: #666666;
  font-size: 13px;
}

.custom-tag {
  margin-bottom: 8px;
}

.product-desc {
  margin-bottom: 12px;
}

.desc-cn {
  font-size: 13px;
  color: #333333;
  margin: 0 0 4px 0;
}

.desc-en {
  font-size: 12px;
  color: #999999;
  margin: 0;
}

.product-specs {
  border-top: 1px solid #e5e5e5;
  padding-top: 12px;
}

.spec-row {
  display: flex;
  font-size: 13px;
  margin-bottom: 6px;
}

.spec-label {
  color: #666666;
  min-width: 90px;
}

.spec-value {
  color: #1a1a1a;
}

/* 修改设计下拉框 */
.design-collapsible {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  margin-top: 16px;
  overflow: hidden;
}

/* 绿色按钮行 */
.design-button-row {
  padding: 12px 16px;
  display: flex;
  align-items: center;
}

.design-toggle-btn {
  background: #22c55e !important;
  border-color: #22c55e !important;
  color: #ffffff !important;
  font-weight: 500;
}

.design-toggle-btn:hover {
  background: #16a34a !important;
  border-color: #16a34a !important;
}

.btn-icon {
  margin-right: 4px;
}

.btn-arrow {
  margin-left: 4px;
  transition: transform 0.3s;
}

.btn-arrow.rotate {
  transform: rotate(180deg);
}

/* 当前订单信息 - 在按钮下方 */
.current-order-info {
  padding: 0 16px 12px;
  font-size: 12px;
  color: #666666;
  border-bottom: 1px solid #e5e7eb;
}

.design-content {
  padding: 16px;
  background: #ffffff;
}

/* 客户修改意见 */
.customer-feedback h4 {
  font-size: 14px;
  font-weight: 600;
  color: #333333;
  margin: 0 0 12px 0;
}

.feedback-form {
  display: flex;
  gap: 12px;
  margin-bottom: 12px;
}

.feedback-input {
  flex: 1;
}

.reference-upload {
  width: 160px;
}

.upload-area {
  height: 100%;
  min-height: 72px;
  border: 2px dashed #d1d5db;
  border-radius: 6px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.upload-area:hover {
  border-color: #9ca3af;
  background: #f9fafb;
}

.upload-icon {
  font-size: 24px;
  margin-bottom: 4px;
}

.upload-text {
  font-size: 10px;
  color: #9ca3af;
  text-align: center;
}

.design-actions {
  display: flex;
  gap: 12px;
}

.design-actions .submit-btn {
  flex: 1;
  background: #3b82f6 !important;
  border-color: #3b82f6 !important;
}

.design-actions .edit-btn {
  flex: 1;
  background: #10b981 !important;
  border-color: #10b981 !important;
}

/* 右侧面板 */
.action-panel {
  width: 360px;
  background: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.panel-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.panel-section:first-child {
  flex: 0 0 auto;
}

.email-section {
  border-bottom: 1px solid #e0e0e0;
}

.email-preview {
  padding: 16px;
}

.email-body {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 12px;
  font-size: 13px;
  line-height: 1.6;
  color: #374151;
  margin-bottom: 12px;
}

.email-body p {
  margin: 6px 0;
}

.copy-btn {
  width: 100%;
  background: #6b7280 !important;
  border-color: #6b7280 !important;
  color: #ffffff !important;
}

/* 操作历史 */
.history-section .panel-header {
  border-top: none;
}

.history-timeline {
  padding: 12px 16px;
  overflow-y: auto;
  flex: 1;
}

.history-item {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  margin-bottom: 12px;
  font-size: 12px;
}

.history-item:last-child {
  margin-bottom: 0;
}

.history-time {
  color: #999999;
  min-width: 40px;
  font-size: 11px;
}

.history-icon {
  font-size: 14px;
}

.history-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.history-label {
  color: #666666;
  font-weight: 500;
}

.history-text {
  color: #999999;
  font-size: 11px;
}

/* 空状态 */
.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100px;
}

/* 状态标签颜色 */
:deep(.el-tag) {
  border-radius: 4px;
}
</style>
