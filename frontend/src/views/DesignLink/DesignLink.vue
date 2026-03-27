<template>
  <div class="design-link-page">
    <!-- Token验证中 -->
    <div v-if="loading" class="loading-state">
      <el-icon class="loading-icon"><Loading /></el-icon>
      <p>验证链接中...</p>
    </div>

    <!-- 验证失败 -->
    <div v-else-if="error" class="error-state">
      <el-icon class="error-icon"><CircleClose /></el-icon>
      <h3>链接无效或已过期</h3>
      <p>{{ errorMessage }}</p>
      <el-button type="primary" @click="goToServiceLink">
        返回沟通链接
      </el-button>
    </div>

    <!-- 主页面内容 -->
    <template v-else>
      <!-- 顶部导航 -->
      <header class="page-header">
        <div class="header-content">
          <div class="shop-info">
            <div class="shop-icon">🎨</div>
            <div class="shop-details">
              <h1>{{ shopInfo?.name || '设计修改中心' }}</h1>
              <p class="shop-code">{{ shopCode?.toUpperCase() }}</p>
            </div>
          </div>
          <div class="header-actions">
            <el-button text @click="goToServiceLink">
              <el-icon><Back /></el-icon>返回沟通链接
            </el-button>
          </div>
        </div>
      </header>

      <!-- 当前订单信息 -->
      <div class="current-order-bar" v-if="selectedOrder">
        <div class="order-label">当前订单：</div>
        <div class="order-info">
          <span class="order-id">{{ selectedOrder.etsy_order_id }}</span>
          <el-tag :type="getStatusType(selectedOrder.status)" size="small">
            {{ getStatusText(selectedOrder.status) }}
          </el-tag>
          <span class="order-customer">{{ selectedOrder.customer_name }}</span>
          <span class="order-product">{{ selectedOrder.product_shape }} · {{ selectedOrder.product_color }}</span>
        </div>
      </div>

      <!-- 主内容区 - 两栏布局：设计器 + 订单详情 -->
      <main class="main-content" v-if="selectedOrder">
        <!-- 左侧：设计器区域 -->
        <section class="designer-section">
          <div class="designer-header">
            <div class="header-left">
              <span class="designer-icon">🎨</span>
              <span class="designer-title">效果图设计器</span>
            </div>
            <span class="auto-load-hint">自动加载订单数据</span>
          </div>
          
          <!-- 设计器 iframe -->
          <div class="designer-wrapper">
            <iframe
              ref="designerFrame"
              src="/designer-standalone.html"
              class="designer-iframe"
              @load="onDesignerLoad"
            ></iframe>
          </div>
        </section>

        <!-- 右侧：订单详情面板 -->
        <aside class="detail-panel">
          <!-- 订单信息 -->
          <div class="panel-section">
            <h3 class="section-title">订单详情</h3>
            
            <!-- 实拍图 -->
            <div class="product-image">
              <img v-if="selectedOrder.product_image_url" :src="selectedOrder.product_image_url" alt="产品实拍图" />
              <div v-else class="image-placeholder">
                <el-icon><Picture /></el-icon>
                <span>产品实拍图</span>
              </div>
            </div>
            
            <!-- 订单信息表格 -->
            <div class="info-grid">
              <div class="info-row">
                <span class="info-label">订单ID:</span>
                <span class="info-value order-id">{{ selectedOrder.etsy_order_id }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">国家:</span>
                <span class="info-value">{{ selectedOrder.country || '美国' }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">客户:</span>
                <span class="info-value">{{ selectedOrder.customer_name }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">颜色:</span>
                <span class="info-value">{{ selectedOrder.product_color }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">形状:</span>
                <span class="info-value">{{ selectedOrder.product_shape }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">尺寸:</span>
                <span class="info-value">{{ selectedOrder.size || 'L' }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">正面:</span>
                <span class="info-value highlight">{{ selectedOrder.front_text }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">字体:</span>
                <span class="info-value">{{ selectedOrder.font_code || 'F-04' }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">背面:</span>
                <span class="info-value">{{ selectedOrder.back_text }}</span>
              </div>
            </div>
          </div>

          <!-- 邮件与回复 -->
          <div class="panel-section">
            <h3 class="section-title">📧 邮件与回复</h3>
            
            <!-- 上次发送的邮件 -->
            <div class="email-box">
              <div class="box-header">
                <span>上次发送的邮件</span>
                <span class="box-badge">只读</span>
              </div>
              <div class="email-content-scroll">
                <p>Hi {{ selectedOrder.customer_name?.split(' ')[0] || 'there' }}!</p>
                <p>Here is the preview of your custom pet tag (Version 1).</p>
                <p>Please check the name, phone number and layout.</p>
                <p>Best,<br>Customer Support Team</p>
              </div>
            </div>

            <!-- 上次发送的效果图 -->
            <div class="effect-box">
              <div class="box-header">
                <span>上次效果图</span>
              </div>
              <div class="effect-preview-area">
                <img v-if="selectedOrder.effect_image_url" :src="selectedOrder.effect_image_url" alt="效果图" />
                <div v-else class="effect-placeholder">
                  <span>效果图预览</span>
                </div>
              </div>
            </div>

            <!-- 客户修改要求 -->
            <div class="modify-request-box" v-if="selectedOrder.modify_request">
              <div class="box-header">
                <span>💬 客户修改要求</span>
                <a href="#" class="store-link">StorePortal</a>
              </div>
              <div class="request-content">
                {{ selectedOrder.modify_request }}
              </div>
            </div>

            <!-- 回复输入框 -->
            <div class="reply-box">
              <div class="box-header">
                <span>📝 回复</span>
                <el-button type="primary" size="small" class="ai-btn">
                  <el-icon><MagicStick /></el-icon> AI生成
                </el-button>
              </div>
              <el-input
                v-model="replyContent"
                type="textarea"
                :rows="4"
                placeholder="在此输入回复内容..."
                class="reply-input"
              />
            </div>

            <!-- 发件人选择 -->
            <div class="sender-select">
              <span class="sender-label">收件人: {{ selectedOrder.customer_name?.split(' ')[0] || 'Customer' }}</span>
              <el-select v-model="replySender" size="small" class="sender-dropdown">
                <el-option label="Customer Support Team" value="Customer Support Team" />
                <el-option label="Pet Tag Studio" value="Pet Tag Studio" />
                <el-option label="Sarah" value="Sarah" />
                <el-option label="Emily" value="Emily" />
              </el-select>
            </div>

            <!-- 历史记录 -->
            <div class="history-box">
              <div class="box-header collapsible" @click="showHistory = !showHistory">
                <span>📜 历史记录</span>
                <el-icon class="collapse-icon" :class="{ rotated: showHistory }">
                  <ArrowDown />
                </el-icon>
              </div>
              <div v-show="showHistory" class="history-list">
                <div v-for="(log, index) in operationLogs" :key="index" class="history-item">
                  <span class="history-time">{{ log.time }}</span>
                  <span class="history-text">{{ log.text }}</span>
                </div>
              </div>
            </div>

            <!-- 操作按钮 -->
            <div class="action-buttons">
              <el-button type="primary" class="action-btn" @click="saveDraft">
                <el-icon><DocumentChecked /></el-icon> 保存草稿
              </el-button>
              <el-button type="success" class="action-btn" @click="markAsProcessed">
                <el-icon><Check /></el-icon> 标记已处理
              </el-button>
            </div>
          </div>
        </aside>
      </main>

      <!-- 未选择订单提示 -->
      <div v-else class="no-order-selected">
        <el-empty description="请从上方选择订单开始设计" />
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  Loading, CircleClose, Back, Picture,
  MagicStick, ArrowDown, DocumentChecked, Check
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

// 状态
const loading = ref(true)
const error = ref(false)
const errorMessage = ref('')
const shopInfo = ref(null)
const orders = ref([])
const selectedOrder = ref(null)
const replyContent = ref('')
const replySender = ref('Customer Support Team')
const showHistory = ref(false)
const operationLogs = ref([])

// 设计器 iframe 引用
const designerFrame = ref(null)

// 从URL获取参数
const shopCode = computed(() => route.params.shopCode)
const token = computed(() => route.query.token)

// 验证Token
async function validateToken() {
  try {
    // 开发模式：如果token是测试值，跳过验证
    if (token.value === 'abc123' || token.value === 'test_token') {
      shopInfo.value = {
        id: 'test-shop-id',
        name: '美国店铺',
        code: shopCode.value
      }
      return true
    }
    
    const response = await fetch('http://localhost:8000/service-link/design-link/validate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        shop_code: shopCode.value,
        token: token.value
      })
    })
    
    const data = await response.json()
    
    if (!data.valid) {
      error.value = true
      errorMessage.value = data.message
      return false
    }
    
    shopInfo.value = {
      id: data.shop_id,
      name: data.shop_name,
      code: shopCode.value
    }
    
    return true
  } catch (e) {
    // 开发模式：API调用失败时也显示页面
    console.log('API验证失败，使用测试模式:', e)
    shopInfo.value = {
      id: 'test-shop-id',
      name: '美国店铺',
      code: shopCode.value
    }
    return true
  }
}

// 获取订单列表
async function fetchOrders() {
  try {
    // 模拟数据
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
        size: 'L',
        country: '美国',
        font_code: 'F-04',
        status: 'pending',
        modify_request: '1. 正面文字由 "Kyla" 改为 "Luna" 2. 背面电话替换为 "+61 4xx xxx xxx" 3. 其它保持不变',
        created_at: '2025-03-25T14:32:00Z'
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
        size: 'M',
        country: '美国',
        font_code: 'F-04',
        status: 'pending',
        created_at: '2025-03-25T10:15:00Z'
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
        size: 'S',
        country: '澳大利亚',
        font_code: 'F-04',
        status: 'pending',
        created_at: '2025-03-24T16:45:00Z'
      }
    ]
    
    operationLogs.value = [
      { time: '2026-03-24 10:15', text: '系统邮件 V1' },
      { time: '2026-03-24 23:01', text: '客户修改：请把名字改成 LUNA' }
    ]
    
    // 默认选中第一个订单
    if (orders.value.length > 0) {
      selectedOrder.value = orders.value[0]
    }
  } catch (e) {
    ElMessage.error('获取订单失败')
  }
}

// 选择订单
function selectOrder(order) {
  selectedOrder.value = order
  // 加载订单数据到设计器
  setTimeout(() => {
    loadOrderToDesigner(order)
  }, 100)
}

// 设计器加载完成
const onDesignerLoad = () => {
  if (selectedOrder.value && designerFrame.value) {
    loadOrderToDesigner(selectedOrder.value)
  }
}

// 加载订单数据到设计器
const loadOrderToDesigner = (order) => {
  if (!designerFrame.value?.contentWindow) return
  
  // 解析背面文字和电话号码
  let backText = order.back_text || ''
  let phone = ''
  
  const phoneMatch = backText.match(/(\d+)/)
  if (phoneMatch) {
    phone = phoneMatch[1]
    backText = backText.replace(/\d+/, '').trim()
  }
  
  // 转换形状和颜色为设计器格式
  const shapeMap = {
    '心形': 'heart',
    '圆形': 'circle',
    '骨头形': 'bone',
    '方形': 'square'
  }
  
  const colorMap = {
    '金色': 'gold',
    '银色': 'silver',
    '玫瑰金': 'rosegold',
    '黑色': 'black'
  }
  
  const shape = shapeMap[order.product_shape] || 'heart'
  const color = colorMap[order.product_color] || 'gold'
  
  designerFrame.value.contentWindow.postMessage({
    type: 'loadOrder',
    data: {
      frontText: order.front_text || '',
      backText: backText,
      phone: phone,
      shape: shape,
      color: color,
      font: order.font_code || 'F-04',
      size: order.size || 'L'
    }
  }, '*')
}

// 返回沟通链接
function goToServiceLink() {
  router.push(`/service/${shopCode.value}?token=${token.value}`)
}

// 保存草稿
function saveDraft() {
  ElMessage.success('草稿已保存')
}

// 标记已处理
function markAsProcessed() {
  ElMessage.success('订单已标记为已处理')
}

// 获取状态类型
function getStatusType(status) {
  const map = {
    pending: 'warning',
    confirmed: 'success',
    modifying: 'danger'
  }
  return map[status] || 'info'
}

// 获取状态文本
function getStatusText(status) {
  const map = {
    pending: '待确认',
    confirmed: '已确认',
    modifying: '修改中'
  }
  return map[status] || status
}

// 初始化
onMounted(async () => {
  const valid = await validateToken()
  if (valid) {
    await fetchOrders()
  }
  loading.value = false
})
</script>

<style scoped>
/* 基础样式 */
.design-link-page {
  min-height: 100vh;
  background: #f5f5f5;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* 加载和错误状态 */
.loading-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  gap: 16px;
}

.loading-icon {
  font-size: 48px;
  color: #3b82f6;
  animation: spin 1s linear infinite;
}

.error-icon {
  font-size: 64px;
  color: #ef4444;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 顶部导航 */
.page-header {
  background: #ffffff;
  border-bottom: 1px solid #e5e5e5;
  padding: 12px 24px;
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

.shop-icon {
  width: 36px;
  height: 36px;
  background: #fef3c7;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
}

.shop-details h1 {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.shop-code {
  font-size: 12px;
  color: #999;
  margin: 2px 0 0 0;
}

/* 当前订单信息栏 */
.current-order-bar {
  max-width: 1600px;
  margin: 16px auto;
  padding: 12px 24px;
  background: #fff;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.order-label {
  font-size: 14px;
  color: #666;
  font-weight: 500;
}

.order-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.order-id {
  font-family: monospace;
  font-size: 14px;
  font-weight: 600;
  color: #3b82f6;
}

.order-customer {
  font-size: 13px;
  color: #333;
}

.order-product {
  font-size: 13px;
  color: #666;
}

/* 主内容区 */
.main-content {
  max-width: 1600px;
  margin: 0 auto;
  padding: 0 24px 24px;
  display: flex;
  gap: 16px;
  height: calc(100vh - 140px);
}

/* 左侧设计器区域 */
.designer-section {
  flex: 1;
  background: #fff;
  border-radius: 8px;
  border: 1px solid #e5e5e5;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.designer-header {
  padding: 12px 16px;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.designer-icon {
  font-size: 18px;
}

.designer-title {
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.auto-load-hint {
  font-size: 12px;
  color: #999;
}

.designer-wrapper {
  flex: 1;
  overflow: hidden;
  background: #f9fafb;
}

.designer-iframe {
  width: 100%;
  height: 100%;
  border: none;
}

/* 右侧详情面板 */
.detail-panel {
  width: 360px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
  overflow-y: auto;
}

.panel-section {
  background: #fff;
  border-radius: 8px;
  border: 1px solid #e5e5e5;
  padding: 16px;
}

.section-title {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin: 0 0 12px 0;
  padding-bottom: 8px;
  border-bottom: 1px solid #f0f0f0;
}

/* 产品图片 */
.product-image {
  width: 100%;
  height: 140px;
  background: #f5f5f5;
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 12px;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #999;
  font-size: 12px;
  gap: 4px;
}

/* 信息网格 */
.info-grid {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.info-row {
  display: flex;
  font-size: 13px;
}

.info-label {
  color: #999;
  min-width: 60px;
}

.info-value {
  color: #333;
  font-weight: 500;
}

.info-value.order-id {
  color: #3b82f6;
  font-family: monospace;
}

.info-value.highlight {
  color: #10b981;
  font-weight: 600;
}

/* 邮件与回复区域 */
.email-box,
.effect-box,
.modify-request-box,
.reply-box,
.history-box {
  background: #fafafa;
  border: 1px solid #e8e8e8;
  border-radius: 6px;
  margin-bottom: 12px;
  overflow: hidden;
}

.box-header {
  padding: 8px 12px;
  background: #f5f5f5;
  border-bottom: 1px solid #e8e8e8;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: #666;
}

.box-header.collapsible {
  cursor: pointer;
}

.box-badge {
  font-size: 10px;
  color: #999;
  background: #e8e8e8;
  padding: 2px 6px;
  border-radius: 3px;
}

.store-link {
  font-size: 11px;
  color: #10b981;
  text-decoration: none;
}

.email-content-scroll {
  padding: 12px;
  font-size: 12px;
  line-height: 1.6;
  color: #555;
  max-height: 120px;
  overflow-y: auto;
}

.email-content-scroll p {
  margin: 4px 0;
}

.effect-preview-area {
  padding: 12px;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.effect-preview-area img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.effect-placeholder {
  color: #999;
  font-size: 12px;
}

.request-content {
  padding: 12px;
  font-size: 12px;
  color: #555;
  line-height: 1.5;
}

.reply-input {
  border: none;
}

.reply-input :deep(.el-textarea__inner) {
  border: none;
  resize: none;
}

.ai-btn {
  font-size: 11px;
}

.sender-select {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 12px 0;
  font-size: 12px;
}

.sender-label {
  color: #666;
}

.sender-dropdown {
  width: 160px;
}

.collapse-icon {
  transition: transform 0.2s;
}

.collapse-icon.rotated {
  transform: rotate(180deg);
}

.history-list {
  padding: 8px 12px;
  font-size: 11px;
}

.history-item {
  display: flex;
  gap: 8px;
  padding: 4px 0;
  color: #666;
}

.history-time {
  color: #999;
  min-width: 100px;
}

/* 操作按钮 */
.action-buttons {
  display: flex;
  gap: 8px;
  margin-top: 12px;
}

.action-btn {
  flex: 1;
  font-size: 13px;
}

/* 未选择订单提示 */
.no-order-selected {
  max-width: 1600px;
  margin: 40px auto;
  padding: 40px;
  background: #fff;
  border-radius: 8px;
  text-align: center;
}
</style>
