<template>
  <div class="remote-container">
    <!-- 登录�?-->
    <div v-if="!isLoggedIn" class="login-page">
      <div class="login-box">
        <div class="logo">📦</div>
        <h2>确认生产�?效果�?/h2>
        <p class="subtitle">生产图与邮件</p>
        <input 
          v-model="loginEmail" 
          type="email" 
          placeholder="请输入您的邮�?
          @keyup.enter="handleLogin"
        />
        <button @click="handleLogin">登录</button>
        <p class="tip">提示：密码与邮箱相同</p>
      </div>
    </div>

    <!-- 工作�?-->
    <div v-else class="workspace">
      <!-- 顶部�?-->
      <header class="top-bar">
        <div class="logo-section">
          <div class="logo-icon">📦</div>
          <div>
            <h1>确认生产�?效果�?/h1>
            <p>生产图与邮件</p>
          </div>
        </div>
        <div class="user-info">
          <span>{{ operatorEmail }}</span>
          <button @click="handleLogout">退�?/button>
        </div>
      </header>

      <div class="main-layout">
        <!-- 左侧边栏 -->
        <aside class="left-sidebar">
          <!-- 订单概览 -->
          <div class="stats-card">
            <h3>订单概览</h3>
            <div class="stats-grid">
              <div class="stat-circle">
                <div class="number">{{ totalCount }}</div>
                <div class="label">总订�?/div>
              </div>
              <div class="stat-circle">
                <div class="number">{{ pendingCount }}</div>
                <div class="label">待处�?/div>
              </div>
              <div class="stat-circle">
                <div class="number">{{ producingCount }}</div>
                <div class="label">生产�?/div>
              </div>
              <div class="stat-circle">
                <div class="number">{{ deliveredCount }}</div>
                <div class="label">已交�?/div>
              </div>
            </div>
          </div>

          <!-- 待确认订单列�?-->
          <div class="pending-section">
            <h3>待确认订�?/h3>
            <div class="order-table">
              <div class="table-header">
                <span>订单ID</span>
                <span>客户名称</span>
                <span>产品</span>
              </div>
              <div 
                v-for="order in pendingOrders" 
                :key="order.id"
                :class="['table-row', { 
                  selected: selectedOrder?.id === order.id,
                  timeout: isTimeout(order)
                }]"
                @click="selectOrder(order)"
              >
                <span class="order-id">{{ order.etsy_order_id }}</span>
                <span>{{ order.customer_name || '-' }}</span>
                <span>{{ order.shape || 'B-E01A' }}</span>
              </div>
              <div v-if="pendingOrders.length === 0" class="empty-row">
                暂无待确认订�?
              </div>
            </div>
          </div>

          <!-- 已确认订�?-->
          <div class="confirmed-section">
            <h3>已确认订�?/h3>
            <div class="confirmed-list">
              <div 
                v-for="order in confirmedOrders.slice(0, 3)" 
                :key="order.id"
                class="confirmed-item"
                @click="selectOrder(order)"
              >
                <span>{{ order.etsy_order_id }}</span>
                <span class="status-tag">�?已进入生�?/span>
              </div>
              <div v-if="confirmedOrders.length === 0" class="empty-row">
                暂无已确认订�?
              </div>
            </div>
          </div>
        </aside>

        <!-- 右侧主内容区 -->
        <main class="main-content">
          <div v-if="!selectedOrder" class="empty-state">
            <p>👈 请从左侧选择一个订�?/p>
          </div>
          <div v-else class="order-detail">
            <!-- 订单标题 -->
            <div class="detail-header">
              <h2>{{ selectedOrder.etsy_order_id }}</h2>
              <div class="action-buttons">
                <button 
                  v-if="selectedOrder.remote_status === 'pending'"
                  class="btn-modify"
                >
                  ✏️ 客户要求修改
                </button>
                <button 
                  v-if="selectedOrder.remote_status === 'sent'"
                  @click="markAsConfirmed(selectedOrder)"
                  class="btn-confirm"
                >
                  �?客户已确�?
                </button>
              </div>
            </div>
            
            <p class="detail-meta">
              客户�? {{ selectedOrder.customer_email || 'example@email.com' }} | 
              创建时间: {{ formatDateTime(selectedOrder.created_at) }}
            </p>

            <!-- 效果图预�?-->
            <div class="preview-section">
              <div class="image-preview">
                <img 
                  v-if="selectedOrder.effect_image_url" 
                  :src="selectedOrder.effect_image_url" 
                  alt="效果�?
                  @click="openImageFullscreen"
                />
                <div v-else class="placeholder">
                  <p>600px 宽度效果图预�?/p>
                  <p class="hint">点击放大 / 右键另存�?/p>
                </div>
              </div>
            </div>

            <!-- 邮件内容�?-->
            <div class="email-templates">
              <div 
                v-for="(template, index) in emailTemplates" 
                :key="index"
                :class="['email-card', { active: selectedTemplate === index }]"
                @click="selectedTemplate = index"
              >
                <h4>邮件内容预览: <span class="template-name">模版{{ index + 1 }}</span></h4>
                <p class="email-text">
                  尊敬的客户您好，您的订单 {{ selectedOrder.etsy_order_id }}<br/>
                  {{ template }}
                </p>
                <button @click="copyEmailContent(index)" class="btn-copy">
                  📋 复制邮件
                </button>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useOrderStore } from '../../stores/orderStore'

const orderStore = useOrderStore()

// 登录
const isLoggedIn = ref(false)
const loginEmail = ref('')
const operatorEmail = ref('')

const handleLogin = () => {
  if (loginEmail.value.includes('@')) {
    operatorEmail.value = loginEmail.value
    isLoggedIn.value = true
    localStorage.setItem('operator_email', loginEmail.value)
    loadOrders()
  } else {
    alert('请输入有效的邮箱地址')
  }
}

const handleLogout = () => {
  isLoggedIn.value = false
  operatorEmail.value = ''
  localStorage.removeItem('operator_email')
}

// 加载订单
const loadOrders = async () => {
  await orderStore.fetchAllOrders()
}

// 我的订单
const myOrders = computed(() => {
  return orderStore.allOrders.filter(order => 
    order.operator_email === operatorEmail.value
  )
})

// 统计数据
const totalCount = computed(() => myOrders.value.length)
const pendingCount = computed(() => 
  myOrders.value.filter(o => ['pending', 'sent'].includes(o.remote_status)).length
)
const producingCount = computed(() => 
  myOrders.value.filter(o => o.status === 'producing').length
)
const deliveredCount = computed(() => 
  myOrders.value.filter(o => o.status === 'delivered').length
)

// 待确认订�?
const pendingOrders = computed(() => {
  return myOrders.value.filter(order => 
    ['pending', 'sent'].includes(order.remote_status || 'pending')
  )
})

// 已确认订�?
const confirmedOrders = computed(() => {
  return myOrders.value.filter(order => 
    order.remote_status === 'confirmed' || order.status === 'producing'
  )
})

// 选中订单
const selectedOrder = ref(null)
const selectedTemplate = ref(0)

const selectOrder = (order) => {
  selectedOrder.value = order
  selectedTemplate.value = 0
}

// 超时判断�?12小时�?
const isTimeout = (order) => {
  const created = new Date(order.created_at)
  const now = new Date()
  const hours = (now - created) / (1000 * 60 * 60)
  return hours > 12 && order.remote_status === 'pending'
}

// 时间格式�?
const formatDateTime = (time) => {
  if (!time) return ''
  const date = new Date(time)
  return date.toLocaleString('zh-CN')
}

// 标记为已确认
const markAsConfirmed = async (order) => {
  order.remote_status = 'confirmed'
  order.status = 'producing'
  alert('�?已标记为已确认，订单进入生产')
}

// 邮件模板
const emailTemplates = [
  '设计效果图已完成，请查阅附件�?,
  '您的订单已开始制作，预计3个工作日完成�?,
  '感谢您的订购，如有任何问题请随时联系我们�?
]

// 复制邮件
const copyEmailContent = (index) => {
  const content = `尊敬的客户您好，您的订单 ${selectedOrder.value.etsy_order_id}\n${emailTemplates[index]}`
  navigator.clipboard.writeText(content)
  alert('�?邮件内容已复制！')
}

// 图片全屏
const openImageFullscreen = () => {
  if (selectedOrder.value?.effect_image_url) {
    window.open(selectedOrder.value.effect_image_url, '_blank')
  }
}

// 初始�?
onMounted(() => {
  const saved = localStorage.getItem('operator_email')
  if (saved) {
    loginEmail.value = saved
    handleLogin()
  }
})
</script>

<style scoped>
.remote-container {
  width: 100%;
  min-height: 100vh;
  background: #efefef;
}

/* 登录�?*/
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}

.login-box {
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  width: 400px;
  text-align: center;
}

.login-box .logo {
  font-size: 48px;
  margin-bottom: 15px;
}

.login-box h2 {
  margin: 10px 0 5px;
  font-size: 20px;
}

.login-box .subtitle {
  color: #999;
  font-size: 12px;
  margin-bottom: 25px;
}

.login-box input {
  width: 100%;
  padding: 12px;
  margin-bottom: 15px;
  border: 1px solid #e5e5e5;
  border-radius: 4px;
  font-size: 14px;
  box-sizing: border-box;
}

.login-box button {
  width: 100%;
  padding: 12px;
  background: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.login-box .tip {
  text-align: center;
  color: #999;
  font-size: 12px;
  margin-top: 10px;
}

/* 工作�?*/
.workspace {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  background: white;
  border-bottom: 1px solid #e5e5e5;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  width: 40px;
  height: 40px;
  background: #f0f0f0;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.logo-section h1 {
  font-size: 18px;
  margin: 0;
}

.logo-section p {
  font-size: 11px;
  color: #999;
  margin: 2px 0 0;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.user-info button {
  padding: 6px 15px;
  background: #f0f0f0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

/* 主布局 */
.main-layout {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.left-sidebar {
  width: 288px;
  background: white;
  border-right: 1px solid #e5e5e5;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 0;
}

/* 订单概览 */
.stats-card {
  padding: 20px;
  border-bottom: 1px solid #f0f0f0;
}

.stats-card h3 {
  margin: 0 0 15px;
  font-size: 18px;
  text-align: center;
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.stat-circle {
  aspect-ratio: 1;
  background: white;
  border: 1px solid #e5e5e5;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.stat-circle .number {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 5px;
}

.stat-circle .label {
  font-size: 11px;
  color: #666;
}

/* 待确认订�?*/
.pending-section {
  padding: 20px;
  border-bottom: 1px solid #f0f0f0;
  flex: 1;
}

.pending-section h3 {
  margin: 0 0 15px;
  font-size: 18px;
  text-align: center;
  background: #f0f0f0;
  padding: 12px;
  border-radius: 20px;
}

.order-table {
  font-size: 12px;
}

.table-header {
  display: grid;
  grid-template-columns: 1fr 1fr 0.8fr;
  padding: 8px;
  color: #999;
  border-bottom: 1px solid #f0f0f0;
}

.table-row {
  display: grid;
  grid-template-columns: 1fr 1fr 0.8fr;
  padding: 12px 8px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: background 0.2s;
}

.table-row:hover {
  background: #fafafa;
}

.table-row.selected {
  background: #e6f7ff;
  border-left: 3px solid #1890ff;
}

.table-row.timeout {
  background: #fff1f0;
  border-left: 3px solid #ff4d4f;
}

.order-id {
  font-weight: 500;
}

.empty-row {
  text-align: center;
  padding: 30px;
  color: #999;
  font-size: 13px;
}

/* 已确认订�?*/
.confirmed-section {
  padding: 20px;
}

.confirmed-section h3 {
  margin: 0 0 15px;
  font-size: 18px;
  text-align: center;
  background: #f0f0f0;
  padding: 12px;
  border-radius: 20px;
}

.confirmed-list {
  font-size: 13px;
}

.confirmed-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  background: #efefef;
  margin-bottom: 8px;
  border-radius: 4px;
}

.confirmed-item:hover {
  background: #e5e5e5;
}

.status-tag {
  font-size: 11px;
  color: #52c41a;
}

/* 主内容区 */
.main-content {
  flex: 1;
  background: white;
  overflow-y: auto;
  padding: 20px;
}

.empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  font-size: 18px;
  color: #999;
}

.order-detail {
  max-width: 1100px;
  margin: 0 auto;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.detail-header h2 {
  margin: 0;
  font-size: 24px;
}

.action-buttons {
  display: flex;
  gap: 10px;
}

.btn-modify, .btn-confirm {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.btn-modify {
  background: #232323;
  color: white;
}

.btn-confirm {
  background: #6b6b6b;
  color: white;
}

.detail-meta {
  color: #666;
  font-size: 14px;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #f0f0f0;
}

/* 效果图预�?*/
.preview-section {
  margin-bottom: 30px;
  padding: 20px;
  background: #efefef;
  border-radius: 8px;
}

.image-preview {
  max-width: 600px;
  margin: 0 auto;
}

.image-preview img {
  width: 100%;
  border: 1px solid #e5e5e5;
  border-radius: 4px;
  cursor: pointer;
}

.placeholder {
  background: white;
  border: 1px solid #e5e5e5;
  border-radius: 4px;
  padding: 120px 40px;
  text-align: center;
}

.placeholder p {
  margin: 5px 0;
  color: #999;
}

.placeholder .hint {
  font-size: 12px;
}

/* 邮件模板 */
.email-templates {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.email-card {
  padding: 20px;
  background: #fafafa;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.email-card:hover {
  border-color: #1890ff;
}

.email-card.active {
  background: #e6f7ff;
  border-color: #1890ff;
}

.email-card h4 {
  margin: 0 0 10px;
  font-size: 14px;
  color: #666;
}

.template-name {
  color: #333;
}

.email-text {
  margin: 10px 0 15px;
  line-height: 1.8;
  font-size: 14px;
  color: #666;
}

.btn-copy {
  padding: 8px 16px;
  background: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.btn-copy:hover {
  background: #40a9ff;
}
</style>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useOrderStore } from '../../stores/orderStore'

const orderStore = useOrderStore()

// 登录状�?
const isLoggedIn = ref(false)
const loginEmail = ref('')
const operatorEmail = ref('')

// 订单列表
const activeTab = ref('pending')
const searchQuery = ref('')
const selectedOrder = ref(null)
const copySuccess = ref(false)

// 登录
const handleLogin = () => {
  if (loginEmail.value.includes('@')) {
    operatorEmail.value = loginEmail.value
    isLoggedIn.value = true
    localStorage.setItem('operator_email', loginEmail.value)
    loadOrders()
  } else {
    alert('请输入有效的邮箱地址')
  }
}

// 退�?
const handleLogout = () => {
  isLoggedIn.value = false
  operatorEmail.value = ''
  localStorage.removeItem('operator_email')
}

// 加载订单
const loadOrders = async () => {
  await orderStore.fetchAllOrders()
}

// 按负责人筛选订�?
const myOrders = computed(() => {
  return orderStore.allOrders.filter(order => 
    order.operator_email === operatorEmail.value
  )
})

// 今日订单
const todayOrders = computed(() => {
  const today = new Date().toISOString().split('T')[0]
  return myOrders.value.filter(order => 
    order.created_at?.startsWith(today)
  )
})

// 待确认订�?
const pendingOrders = computed(() => {
  return myOrders.value.filter(order => 
    ['pending', 'sent'].includes(order.remote_status)
  )
})

// 已确认订�?
const confirmedOrders = computed(() => {
  return myOrders.value.filter(order => 
    order.remote_status === 'confirmed'
  )
})

// 当前显示的订�?
const filteredOrders = computed(() => {
  let orders = []
  if (activeTab.value === 'today') orders = todayOrders.value
  else if (activeTab.value === 'pending') orders = pendingOrders.value
  else orders = confirmedOrders.value

  // 搜索过滤
  if (searchQuery.value) {
    orders = orders.filter(order => 
      order.etsy_order_id?.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }

  return orders
})

// 统计
const pendingCount = computed(() => 
  myOrders.value.filter(o => o.remote_status === 'pending').length
)
const sentCount = computed(() => 
  myOrders.value.filter(o => o.remote_status === 'sent').length
)

// 选择订单
const selectOrder = (order) => {
  selectedOrder.value = order
  copySuccess.value = false
}

// 状态映�?
const getStatusClass = (status) => {
  const map = {
    'pending': 'status-pending',
    'sent': 'status-sent',
    'confirmed': 'status-confirmed'
  }
  return map[status] || 'status-pending'
}

const getStatusText = (status) => {
  const map = {
    'pending': '待处�?,
    'sent': '已发�?,
    'confirmed': '已确�?
  }
  return map[status] || '待处�?
}

// 超时判断�?12小时�?
const isTimeout = (order) => {
  const created = new Date(order.created_at)
  const now = new Date()
  const hours = (now - created) / (1000 * 60 * 60)
  return hours > 12 && order.remote_status === 'pending'
}

// 时间格式�?
const formatTime = (time) => {
  if (!time) return ''
  const date = new Date(time)
  const now = new Date()
  const diff = now - date
  const hours = Math.floor(diff / (1000 * 60 * 60))
  if (hours < 1) return '刚刚'
  if (hours < 24) return `${hours}小时前`
  return date.toLocaleDateString('zh-CN')
}

// 标记为已发�?
const markAsSent = async (order) => {
  // TODO: 调用 API 更新状�?
  order.remote_status = 'sent'
  alert('已标记为已发�?)
}

// 标记为已确认
const markAsConfirmed = async (order) => {
  // TODO: 调用 API 更新状�?
  order.remote_status = 'confirmed'
  order.status = 'producing'
  alert('已标记为已确认，订单进入生产')
}

// 邮件内容
const emailContent = computed(() => {
  if (!selectedOrder.value) return ''
  return `Dear ${selectedOrder.value.customer_name},

Thank you for your order!

Order Details:
- Order ID: ${selectedOrder.value.etsy_order_id}
- Product: ${selectedOrder.value.shape} ${selectedOrder.value.color} ${selectedOrder.value.size}

We have received your order and will start production soon.
Please review the attached effect image and let us know if you need any changes.

Best regards,
Your Store Team`
})

// 复制邮件内容
const copyEmailContent = () => {
  navigator.clipboard.writeText(emailContent.value)
  copySuccess.value = true
  setTimeout(() => { copySuccess.value = false }, 2000)
}

// 下载效果�?
const downloadImage = () => {
  if (selectedOrder.value?.effect_image_url) {
    const link = document.createElement('a')
    link.href = selectedOrder.value.effect_image_url
    link.download = `${selectedOrder.value.etsy_order_id}.jpg`
    link.click()
  }
}

// 复制图片链接
const copyImageUrl = () => {
  if (selectedOrder.value?.effect_image_url) {
    navigator.clipboard.writeText(selectedOrder.value.effect_image_url)
    alert('图片链接已复�?)
  }
}

// 图片全屏
const openImageFullscreen = () => {
  if (selectedOrder.value?.effect_image_url) {
    window.open(selectedOrder.value.effect_image_url, '_blank')
  }
}

// 搜索
const handleSearch = () => {
  // 自动触发 computed
}

// 初始�?
onMounted(() => {
  const saved = localStorage.getItem('operator_email')
  if (saved) {
    loginEmail.value = saved
    handleLogin()
  }
})
</script>

<style scoped>
.remote-container {
  width: 100%;
  height: 100vh;
  background: #f5f5f5;
}

/* 登录�?*/
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.login-box {
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  width: 400px;
}

.login-box h2 {
  margin-bottom: 20px;
  text-align: center;
}

.login-box input {
  width: 100%;
  padding: 12px;
  margin-bottom: 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.login-box button {
  width: 100%;
  padding: 12px;
  background: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.login-box button:hover {
  background: #40a9ff;
}

.login-box .tip {
  text-align: center;
  color: #999;
  font-size: 12px;
  margin-top: 10px;
}

/* 工作�?*/
.workspace {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  height: 60px;
  background: white;
  border-bottom: 1px solid #e5e5e5;
}

.top-bar h1 {
  font-size: 20px;
  margin: 0;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.user-info button {
  padding: 6px 15px;
  background: #f0f0f0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.main-content {
  display: flex;
  flex: 1;
  overflow: hidden;
}

/* 左侧 */
.left-sidebar {
  width: 320px;
  background: white;
  border-right: 1px solid #e5e5e5;
  display: flex;
  flex-direction: column;
}

.stats-card {
  padding: 20px;
  border-bottom: 1px solid #f0f0f0;
}

.stats-card h3 {
  margin: 0 0 15px 0;
  font-size: 16px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  font-size: 14px;
}

.stat-item strong {
  color: #1890ff;
  font-size: 18px;
}

.search-box {
  padding: 15px;
  border-bottom: 1px solid #f0f0f0;
}

.search-box input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  font-size: 14px;
}

.order-tabs {
  display: flex;
  border-bottom: 1px solid #f0f0f0;
}

.order-tabs button {
  flex: 1;
  padding: 12px;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 13px;
  color: #666;
  border-bottom: 2px solid transparent;
}

.order-tabs button.active {
  color: #1890ff;
  border-bottom-color: #1890ff;
}

.order-list {
  flex: 1;
  overflow-y: auto;
}

.order-item {
  padding: 15px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: background 0.2s;
}

.order-item:hover {
  background: #fafafa;
}

.order-item.selected {
  background: #e6f7ff;
  border-left: 3px solid #1890ff;
}

.order-item.timeout {
  border-left: 3px solid #ff4d4f;
  background: #fff1f0;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.order-id {
  font-weight: 500;
  font-size: 14px;
}

.status-badge {
  padding: 2px 8px;
  border-radius: 3px;
  font-size: 12px;
}

.status-pending {
  background: #fff7e6;
  color: #fa8c16;
}

.status-sent {
  background: #e6f7ff;
  color: #1890ff;
}

.status-confirmed {
  background: #f6ffed;
  color: #52c41a;
}

.order-info {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  color: #666;
}

.time {
  color: #999;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #999;
}

/* 右侧 */
.right-content {
  flex: 1;
  background: white;
  overflow-y: auto;
  padding: 20px;
}

.empty-detail {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  font-size: 18px;
  color: #999;
}

.order-detail {
  max-width: 900px;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #f0f0f0;
}

.detail-header h2 {
  margin: 0;
  font-size: 24px;
}

.btn-primary, .btn-success {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.btn-primary {
  background: #1890ff;
  color: white;
}

.btn-success {
  background: #52c41a;
  color: white;
}

.detail-info {
  margin-bottom: 30px;
}

.detail-info p {
  margin: 10px 0;
  font-size: 14px;
  line-height: 1.6;
}

.effect-image-section, .email-section {
  margin-bottom: 30px;
  padding: 20px;
  background: #fafafa;
  border-radius: 8px;
}

.effect-image-section h3, .email-section h3 {
  margin: 0 0 15px 0;
  font-size: 16px;
}

.image-container {
  margin-bottom: 15px;
  text-align: center;
}

.image-container img {
  max-width: 600px;
  width: 100%;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  cursor: pointer;
}

.no-image {
  padding: 100px;
  background: white;
  border: 1px dashed #d9d9d9;
  border-radius: 4px;
  color: #999;
  text-align: center;
}

.image-actions {
  display: flex;
  gap: 10px;
}

.image-actions button {
  flex: 1;
  padding: 10px;
  background: white;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  cursor: pointer;
}

.image-actions button:hover {
  border-color: #1890ff;
  color: #1890ff;
}

.email-preview {
  background: white;
  padding: 20px;
  border-radius: 4px;
  margin-bottom: 15px;
  white-space: pre-wrap;
  line-height: 1.8;
  font-size: 14px;
  border: 1px solid #d9d9d9;
}

.btn-copy {
  padding: 10px 20px;
  background: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.btn-copy:hover {
  background: #40a9ff;
}

.copy-tip {
  margin-left: 10px;
  color: #52c41a;
  font-size: 14px;
}
</style>
