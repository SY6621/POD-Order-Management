<template>
  <div class="design-link-page">
    <!-- Token验证中 -->
    <div v-if="loading" class="loading-overlay">
      <div class="loading-content">
        <el-icon class="loading-icon is-loading" :size="32"><Loading /></el-icon>
        <p class="loading-text">验证链接中，请稍候...</p>
      </div>
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
        </div>
      </div>

      <!-- 主内容区 - 新布局：左上三卡片+左下设计器 + 右全高邮件区 -->
      <main class="main-content" v-if="selectedOrder">
        <!-- 左列：上方三卡片 + 下方设计器 -->
        <div class="left-column">
          <!-- 上方：三卡片水平排列 -->
          <div class="info-cards-row">
            <!-- 卡片2: 订单详情 -->
            <div class="info-card" v-if="selectedOrder">
              <div class="card-header">订单详情</div>
              <div class="card-body order-detail-card">
                <div class="order-thumb">
                  <img v-if="selectedOrder.product_image_url" :src="selectedOrder.product_image_url" alt="产品图" />
                  <div v-else class="thumb-placeholder">暂无图片</div>
                </div>
                <div class="order-info-compact">
                  <div class="info-row"><span class="label">订单:</span><span class="value order-id">{{ selectedOrder.etsy_order_id }}</span></div>
                  <div class="info-row"><span class="label">客户:</span><span class="value">{{ selectedOrder.customer_name }}</span></div>
                  <div class="info-row"><span class="label">国家:</span><span class="value">{{ selectedOrder.country }}</span></div>
                  <div class="info-row"><span class="label">正面:</span><span class="value">{{ selectedOrder.front_text }}</span></div>
                  <div class="info-row"><span class="label">背面:</span><span class="value">{{ selectedOrder.back_text || '-' }}</span></div>
                  <div class="info-row"><span class="label">颜色:</span><span class="value">{{ selectedOrder.product_color }}</span></div>
                </div>
              </div>
            </div>

            <!-- 卡片3: 第一版效果图 -->
            <div class="info-card">
              <div class="card-header">
                <span>第一版效果图</span>
                <span v-if="selectedOrder?.effect_image_url" class="status-badge generated">✓ 已生成</span>
              </div>
              <div class="card-body effect-thumb-card">
                <img v-if="selectedOrder?.effect_image_url" :src="selectedOrder.effect_image_url" alt="效果图" class="effect-thumb" />
                <div v-else class="thumb-placeholder">暂未生成</div>
              </div>
            </div>

            <!-- 卡片4: 时间信息 -->
            <div class="info-card">
              <div class="card-header">时间信息</div>
              <div class="card-body time-info-card">
                <div class="time-row">
                  <span class="time-label">订单到达:</span>
                  <span class="time-value">{{ selectedOrder ? formatDate(selectedOrder.created_at) : '-' }}</span>
                </div>
                <div class="time-row">
                  <span class="time-label">交货时间:</span>
                  <span class="time-value">{{ selectedOrder ? formatDueDate(selectedOrder.created_at) : '-' }}</span>
                </div>
                <div class="time-row" v-if="selectedOrder && isOverdue(selectedOrder)">
                  <span class="overdue-badge">⚠ 超时 {{ getOverdueHours(selectedOrder) }}h</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 下方：设计器 -->
          <div class="designer-section">
            <div class="designer-header">
              <div class="designer-title">
                <span class="designer-icon">🎨</span>
                <span>效果图设计器</span>
              </div>
              <span class="designer-hint">自动加载订单数据</span>
            </div>
            <div class="designer-container">
              <iframe ref="designerFrame" src="/designer-standalone.html" class="designer-iframe" @load="onDesignerLoad"></iframe>
            </div>
          </div>
        </div>

        <!-- 右列：邮件回复（全高） -->
        <div class="email-panel">
          <!-- Tab 切换 -->
          <div class="email-tabs">
            <button :class="['tab-btn', { active: emailTab === 'history' }]" @click="emailTab = 'history'">过往邮件</button>
            <button :class="['tab-btn', { active: emailTab === 'reply' }]" @click="emailTab = 'reply'">邮件回复</button>
          </div>

          <!-- Tab1: 过往邮件 -->
          <div v-if="emailTab === 'history'" class="tab-content history-tab">
            <div v-if="emailHistory.length" class="email-history-list">
              <div v-for="(log, index) in emailHistory" :key="index" class="history-item">
                <div class="history-meta">
                  <span class="history-type">{{ log.email_type === 'modify_reply' ? '修改回复' : '首封邮件' }}</span>
                  <span class="history-time">{{ formatDateTime(log.created_at) }}</span>
                </div>
                <div class="history-content">{{ log.content }}</div>
              </div>
            </div>
            <div v-else class="empty-hint">
              <span>📭</span>
              <p>暂无历史邮件记录</p>
            </div>
          </div>

          <!-- Tab2: 邮件回复（三分区） -->
          <div v-if="emailTab === 'reply'" class="tab-content reply-tab">
            <!-- 分区3: 预设快捷内容（放在最上面，方便快速选择） -->
            <div class="reply-section preset-section">
              <div class="section-label">快捷内容</div>
              <div class="preset-tags">
                <label v-for="(preset, idx) in presetOptions" :key="idx" :class="['preset-tag', { checked: preset.checked }]">
                  <input type="checkbox" v-model="preset.checked" @change="onPresetToggle(preset)" />
                  {{ preset.label }}
                </label>
              </div>
            </div>

            <!-- 分区1: 客户要求 -->
            <div class="reply-section">
              <div class="section-label">📋 客户要求</div>
              <textarea v-model="customerRequirement" placeholder="填写客户修改要求，或通过上方快捷内容自动填入..." rows="6" class="requirement-input"></textarea>
            </div>

            <!-- 分区2: AI生成回复 -->
            <div class="reply-section ai-section">
              <div class="section-label">
                <span>🤖 AI生成回复</span>
                <button @click="generateAIReply" class="generate-btn" :disabled="!customerRequirement.trim()">生成回复</button>
              </div>
              <div class="ai-reply-box-wrapper">
                <textarea v-model="aiGeneratedReply" class="ai-reply-box" placeholder="点击「生成回复」根据客户要求自动生成邮件内容..." rows="8"></textarea>
              </div>
            </div>

            <!-- 落款选择 -->
            <div class="reply-section sender-section">
              <div class="section-label-inline">
                <span>落款:</span>
                <select v-model="firstEmailSender" class="sender-select">
                  <option value="Sophia">Sophia</option>
                  <option value="Emma">Emma</option>
                  <option value="Olivia">Olivia</option>
                  <option value="custom">自定义...</option>
                </select>
                <input v-if="firstEmailSender === 'custom'" v-model="customSenderName" placeholder="输入落款名" class="custom-sender-input" />
              </div>
            </div>

            <!-- 操作按钮 -->
            <div class="action-btn-row">
              <button class="action-btn secondary" @click="copyReplyEmail" title="复制邮件内容">
                📋 复制
              </button>
              <button v-if="!isEffectConfirmed" class="action-btn primary" @click="confirmEffect" title="确认当前效果图">
                ✓ 确认效果图
              </button>
              <button v-else class="action-btn disabled" disabled>
                ✅ 效果图已确认
              </button>
              <button class="action-btn success" @click="sendReplyEmail" :disabled="isSendingFirstEmail" title="传送效果图和邮件到沟通外链">
                {{ isSendingFirstEmail ? '传送中...' : '📤 传送效果图/邮件' }}
              </button>
            </div>
          </div>
        </div>
      </main>

      <!-- 未选择订单提示 -->
      <div v-else class="no-order-selected">
        <el-empty description="请从上方选择订单开始设计" />
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, reactive, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  Loading, CircleClose, Back
} from '@element-plus/icons-vue'
import supabase from '../../utils/supabase'

const route = useRoute()
const router = useRouter()

// 状态
const loading = ref(true)
const error = ref(false)
const errorMessage = ref('')
const shopInfo = ref(null)
const serviceToken = ref('') // 保存 service_token 用于跳转回 ServiceLink
const orders = ref([])
const selectedOrder = ref(null)
const savingEffect = ref(false)

// ===== 首封邮件区域 =====
const firstEmailTemplate = ref('standard')
const firstEmailSender = ref('Sophia')
const senderSelectValue = ref('Sophia')
const customSenderName = ref('')
const templateSelectValue = ref('standard')
const customTemplateName = ref('')
const isSendingFirstEmail = ref(false)
const isEffectConfirmed = ref(false)
const showTemplateEditor = ref(false)
const templateEditContent = ref('')
const customerModifyRequest = ref('') // 客户修改要求

// ===== 新布局邮件回复区域 =====
const emailTab = ref('reply')
const emailHistory = ref([])
const customerRequirement = ref('')
const aiGeneratedReply = ref('')
const presetOptions = ref([
  { label: '设计稿已修改完成', checked: false },
  { label: '感谢你的耐心等待', checked: false },
  { label: '文字/拼写已修正', checked: false },
  { label: '字体已更换', checked: false },
  { label: '颜色已调整', checked: false },
  { label: '尺寸已修改', checked: false },
  { label: '正反面内容已更新', checked: false },
  { label: '图案已重新设计', checked: false },
])

// 落款下拉联动
watch(senderSelectValue, (val) => {
  if (val !== '__custom__') {
    firstEmailSender.value = val
  } else {
    firstEmailSender.value = customSenderName.value || 'Sophia'
  }
})

// 模板下拉联动
watch(templateSelectValue, (val) => {
  if (val !== '__custom__') {
    firstEmailTemplate.value = val
  }
})

// 硬编码默认模板 - 使用reactive使其响应式
const defaultFirstEmailTemplates = reactive({
  standard: {
    name: '标准确认',
    key: 'standard',
    content: `Hi {firstName},

Thank you so much for your order!
I've finished your design proof for the custom heart pet ID tag.
Please kindly check and confirm the details within 24 hours if you need any changes.
If I don't hear from you within 24 hours, I will proceed with production as requested to avoid delay.
Thank you for your support!

Best regards,
{senderName}`
  },
  urgent: {
    name: '加急确认',
    key: 'urgent',
    content: `Hi {firstName},

Thank you for your order!
Your design proof is ready. Since this is a rush order, please review and confirm within 12 hours so we can start production right away.
If I don't hear back within 12 hours, I'll proceed as requested.
Thank you!

Best regards,
{senderName}`
  },
  custom: {
    name: '定制需求确认',
    key: 'custom',
    content: `Hi {firstName},

Thank you so much for your order!
I've carefully prepared your custom design based on your special requirements. Please take a moment to review everything, especially the personalization details.
Please confirm within 24 hours if everything looks good, or let me know if you'd like any changes.
Looking forward to hearing from you!

Best regards,
{senderName}`
  },
  modify_confirm: {
    name: '修改确认',
    key: 'modify_confirm',
    content: `Hi {firstName},

Thank you for your feedback!
I've updated your custom {shape} pet ID tag based on your request.
Please kindly check the new design proof and confirm within 24 hours.
If you need any further changes, please don't hesitate to let me know.
Thank you for your patience and support!

Best regards,
{senderName}`
  }
})

// 模板选项列表
const firstEmailTemplateOptions = computed(() => {
  return Object.values(defaultFirstEmailTemplates)
})

// 邮件预览（计算属性）
const firstEmailPreview = computed(() => {
  const order = selectedOrder.value
  const firstName = order ? (order.customer_name || '').split(' ')[0] || 'Customer' : 'Customer'
  const sender = firstEmailSender.value
  const shape = order?.product_shape || 'heart'

  const defaultTpl = defaultFirstEmailTemplates[firstEmailTemplate.value]
  const templateText = defaultTpl ? defaultTpl.content : ''

  return templateText
    .replace(/\{firstName\}/g, firstName)
    .replace(/\{senderName\}/g, sender)
    .replace(/\{shape\}/g, shape)
})

// 计算是否可以发送首封邮件
const canSendFirstEmail = computed(() => {
  return isEffectConfirmed.value && firstEmailPreview.value && firstEmailPreview.value.trim() !== ''
})

// 选中订单切换时重置确认状态
watch(selectedOrder, () => {
  isEffectConfirmed.value = false
})

// 从localStorage加载自定义模板
const loadCustomTemplates = () => {
  try {
    const saved = localStorage.getItem('firstEmailCustomTemplates')
    if (saved) {
      const parsed = JSON.parse(saved)
      Object.keys(parsed).forEach(key => {
        if (defaultFirstEmailTemplates[key]) {
          defaultFirstEmailTemplates[key].content = parsed[key]
        }
      })
    }
  } catch (e) {
    console.warn('加载自定义模板失败:', e)
  }
}

// 保存模板到localStorage
const saveTemplate = () => {
  const key = firstEmailTemplate.value
  if (!key) return

  if (defaultFirstEmailTemplates[key]) {
    defaultFirstEmailTemplates[key].content = templateEditContent.value
  }

  try {
    const saved = JSON.parse(localStorage.getItem('firstEmailCustomTemplates') || '{}')
    saved[key] = templateEditContent.value
    localStorage.setItem('firstEmailCustomTemplates', JSON.stringify(saved))
    ElMessage.success('模板已保存')
  } catch (e) {
    ElMessage.error('保存失败')
  }
}

// 切换模板时，同步编辑区内容
watch(firstEmailTemplate, (newVal) => {
  const tpl = defaultFirstEmailTemplates[newVal]
  templateEditContent.value = tpl ? tpl.content : ''
})

// 展开编辑器时，同步当前模板内容
watch(showTemplateEditor, (isOpen) => {
  if (isOpen) {
    const tpl = defaultFirstEmailTemplates[firstEmailTemplate.value]
    templateEditContent.value = tpl ? tpl.content : ''
  }
})

// 复制邮件内容
const copyFirstEmail = async () => {
  if (!firstEmailPreview.value) return
  try {
    await navigator.clipboard.writeText(firstEmailPreview.value)
    ElMessage.success('邮件内容已复制到剪贴板')
  } catch (err) {
    const textarea = document.createElement('textarea')
    textarea.value = firstEmailPreview.value
    document.body.appendChild(textarea)
    textarea.select()
    document.execCommand('copy')
    document.body.removeChild(textarea)
    ElMessage.success('邮件内容已复制到剪贴板')
  }
}

// 效果图确认方法
const confirmEffect = () => {
  if (!selectedOrder.value) return
  if (!selectedOrder.value.effect_image_url) {
    ElMessage.warning('请先生成效果图')
    return
  }
  isEffectConfirmed.value = true
  ElMessage.success('效果图已确认')
}

// 确认并发送首封邮件
const sendFirstEmail = async () => {
  if (!canSendFirstEmail.value || !selectedOrder.value) {
    if (!selectedOrder.value) {
      ElMessage.warning('请先选择一条订单')
    } else if (!isEffectConfirmed.value) {
      ElMessage.warning('请先确认效果图')
    }
    return
  }

  isSendingFirstEmail.value = true
  try {
    // 0. 先保存设计器最新效果图到 Supabase Storage
    try {
      await saveEffectImage()
      console.log('✅ 最新效果图已保存')
    } catch (imgErr) {
      console.warn('⚠️ 效果图保存失败，将使用已有效果图:', imgErr.message)
    }

    // 1. 保存邮件记录到 email_logs 表
    await supabase
      .from('email_logs')
      .insert({
        order_id: selectedOrder.value.id,
        shop_id: shopInfo.value?.id,
        email_type: firstEmailTemplate.value === 'modify_confirm' ? 'modify_reply' : 'first_email',
        subject: `Your Custom Pet Tag Design Preview - Order #${selectedOrder.value.etsy_order_id || selectedOrder.value.id}`,
        content: firstEmailPreview.value,
        effect_image_url: selectedOrder.value.effect_image_url || '',
        sender_name: firstEmailSender.value
      })

    // 2. 更新订单状态为"待回复"
    const { error } = await supabase
      .from('orders')
      .update({
        status: '待回复',
        email_status: 'sent',
        email_sent: true,
        email_sent_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      })
      .eq('id', selectedOrder.value.id)

    if (error) throw error

    // 3. 记录操作日志
    await supabase
      .from('service_link_logs')
      .insert({
        order_id: selectedOrder.value.id,
        shop_id: shopInfo.value?.id,
        action: 'first_email_sent',
        action_details: { text: '首封确认邮件已发送，订单进入待回复状态' },
        operator: 'design_link',
        created_at: new Date().toISOString()
      })

    // 4. 重置确认状态
    isEffectConfirmed.value = false

    ElMessage.success('已发送，订单已移至"待回复"')
  } catch (err) {
    console.error('发送失败:', err)
    ElMessage.error('发送失败：' + (err.message || '未知错误'))
  } finally {
    isSendingFirstEmail.value = false
  }
}

// ===== 新布局辅助函数 =====

// 格式化日期
function formatDate(dateStr) {
  if (!dateStr) return '-'
  const d = new Date(dateStr)
  return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`
}

// 格式化日期时间
function formatDateTime(dateStr) {
  if (!dateStr) return '-'
  const d = new Date(dateStr)
  return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')} ${String(d.getHours()).padStart(2,'0')}:${String(d.getMinutes()).padStart(2,'0')}`
}

// 计算交货时间（created_at + 3天）
function formatDueDate(dateStr) {
  if (!dateStr) return '-'
  const d = new Date(dateStr)
  d.setDate(d.getDate() + 3)
  return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`
}

// 获取邮件历史
async function fetchEmailHistory() {
  if (!selectedOrder.value) return
  try {
    const { data } = await supabase
      .from('email_logs')
      .select('*')
      .eq('order_id', selectedOrder.value.id)
      .order('created_at', { ascending: false })
    emailHistory.value = data || []
  } catch (e) {
    console.error('获取邮件历史失败:', e)
    emailHistory.value = []
  }
}

// 预设选项切换
function onPresetToggle(preset) {
  if (preset.checked) {
    // 追加到客户要求
    if (customerRequirement.value) {
      customerRequirement.value += '；' + preset.label
    } else {
      customerRequirement.value = preset.label
    }
  } else {
    // 从客户要求中移除
    customerRequirement.value = customerRequirement.value
      .split('；')
      .filter(s => s.trim() !== preset.label)
      .join('；')
  }
}

// AI生成回复（本地模板引擎）
function generateAIReply() {
  if (!customerRequirement.value.trim()) return
  
  const customerName = selectedOrder.value?.customer_name?.split(' ')[0] || 'Customer'
  const shape = selectedOrder.value?.product_shape || 'heart'
  const sender = firstEmailSender.value === 'custom' ? customSenderName.value : firstEmailSender.value
  const req = customerRequirement.value
  
  // 根据客户要求关键词匹配生成修改说明段落
  const paragraphs = []
  
  if (req.includes('设计稿已修改完成')) {
    paragraphs.push("I've revised the design based on your request. The updated proof is now ready for your review.")
  }
  if (req.includes('文字') || req.includes('拼写') || req.includes('名字')) {
    paragraphs.push("I've corrected the text/spelling as requested. Please check the updated design.")
  }
  if (req.includes('字体')) {
    paragraphs.push("I've changed the font style as you suggested. Hope you like the new look!")
  }
  if (req.includes('颜色')) {
    paragraphs.push("I've updated the color to match your preference.")
  }
  if (req.includes('尺寸') || req.includes('大小')) {
    paragraphs.push("I've adjusted the size according to your requirements.")
  }
  if (req.includes('正反面')) {
    paragraphs.push("I've updated the content on both sides of the tag as requested.")
  }
  if (req.includes('图案')) {
    paragraphs.push("I've redesigned the pattern based on your feedback.")
  }
  if (req.includes('耐心等待')) {
    paragraphs.push("I sincerely apologize for the wait and appreciate your patience.")
  }
  
  // 如果没有匹配到任何关键词，使用默认段落
  if (paragraphs.length === 0) {
    paragraphs.push("I've made the changes as you requested. The updated design is ready for your review.")
  }
  
  const modifyDetails = paragraphs.join('\n')
  
  aiGeneratedReply.value = `Hi ${customerName},

Thank you for your feedback regarding your custom ${shape} pet ID tag order.

${modifyDetails}

Please kindly review the updated design proof and confirm within 24 hours if everything looks good.
If you need any further adjustments, please don't hesitate to let me know.

Best regards,
${sender || 'Sophia'}`
}

// 复制回复邮件
async function copyReplyEmail() {
  const content = aiGeneratedReply.value || ''
  if (!content) {
    alert('请先生成回复内容')
    return
  }
  try {
    await navigator.clipboard.writeText(content)
    alert('邮件内容已复制到剪贴板')
  } catch (e) {
    console.error('复制失败:', e)
  }
}

// 传送回复邮件（修改版sendFirstEmail）
async function sendReplyEmail() {
  if (!isEffectConfirmed.value) {
    alert('请先确认效果图')
    return
  }
  
  const emailContent = aiGeneratedReply.value
  if (!emailContent || !emailContent.trim()) {
    alert('请先生成回复内容')
    return
  }
  
  isSendingFirstEmail.value = true
  try {
    // 1. 保存最新效果图
    await saveEffectImage()
    
    // 2. 刷新订单数据获取最新effect_image_url
    await fetchOrders()
    
    // 3. 保存邮件记录到 email_logs
    const { error: emailError } = await supabase
      .from('email_logs')
      .insert({
        order_id: selectedOrder.value.id,
        shop_id: shopInfo.value?.id,
        content: emailContent,
        sender_name: firstEmailSender.value === 'custom' ? customSenderName.value : firstEmailSender.value,
        email_type: 'modify_reply',
        created_at: new Date().toISOString()
      })
    if (emailError) console.error('保存邮件记录失败:', emailError)
    
    // 4. 更新订单状态为"待回复"
    const { error: updateError } = await supabase
      .from('orders')
      .update({ 
        status: '待回复',
        email_sent: true,
        email_sent_at: new Date().toISOString()
      })
      .eq('id', selectedOrder.value.id)
    if (updateError) console.error('更新订单状态失败:', updateError)
    
    // 5. 记录操作日志
    await supabase
      .from('service_link_logs')
      .insert({
        order_id: selectedOrder.value.id,
        shop_id: shopInfo.value?.id,
        action: 'modify_reply_sent',
        action_details: { text: '修改回复邮件已发送，订单进入待回复状态' },
        operator: 'design_link',
        created_at: new Date().toISOString()
      })
    
    // 6. 重置状态
    isEffectConfirmed.value = false
    aiGeneratedReply.value = ''
    customerRequirement.value = ''
    presetOptions.value.forEach(p => p.checked = false)
    
    alert('传送成功！效果图和邮件已同步到沟通外链')
    
    // 7. 刷新邮件历史
    await fetchEmailHistory()
    
  } catch (e) {
    console.error('传送失败:', e)
    alert('传送失败: ' + e.message)
  } finally {
    isSendingFirstEmail.value = false
  }
}

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
        code: shopCode.value,
        design_token: token.value
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
      code: shopCode.value,
      design_token: token.value
    }

    // 保存 service_token 用于跳转回 ServiceLink
    serviceToken.value = data.service_token || ''

    return true
  } catch (e) {
    // 后端API不可用，尝试直接查询Supabase验证Token（兜底方案）
    console.log('⚠️ 后端API不可用，尝试Supabase兜底验证:', e)

    try {
      const { data: shop, error: supabaseError } = await supabase
        .from('shops')
        .select('*')
        .eq('code', shopCode.value)
        .single()

      if (supabaseError) {
        console.error('❌ Supabase查询失败:', supabaseError)
        error.value = true
        errorMessage.value = '链接验证失败，请稍后重试'
        return false
      }

      if (!shop) {
        console.error('❌ 店铺不存在:', shopCode.value)
        error.value = true
        errorMessage.value = '链接无效：店铺不存在'
        return false
      }

      // 检查design_token是否匹配
      if (shop.design_token !== token.value) {
        console.error('❌ Token不匹配')
        error.value = true
        errorMessage.value = '链接无效或已过期'
        return false
      }

      // 检查design_link_enabled是否开启
      if (!shop.design_link_enabled) {
        console.error('❌ 设计链接功能未开启')
        error.value = true
        errorMessage.value = '该功能暂未开启'
        return false
      }

      // 验证成功
      console.log('✅ Supabase兜底验证成功:', shop.name)
      shopInfo.value = {
        id: shop.id,
        name: shop.name,
        code: shop.code,
        design_token: shop.design_token
      }
      return true

    } catch (supabaseErr) {
      console.error('❌ Supabase兜底验证异常:', supabaseErr)
      error.value = true
      errorMessage.value = '链接验证失败，请稍后重试'
      return false
    }
  }
}

// 获取订单列表
async function fetchOrders() {
  try {
    // 从Supabase加载真实订单数据
    const { data: ordersData, error: ordersError } = await supabase
      .from('orders')
      .select('*')
      .eq('shop_id', shopInfo.value?.id || 'test-shop-id')
      .in('status', ['客户修改', '待回复'])
      .order('created_at', { ascending: false })
    
    if (ordersError) {
      console.error('❌ 订单查询错误:', ordersError)
      throw ordersError
    }
    
    // 如果没有订单数据，使用模拟数据（开发模式）
    if (!ordersData || ordersData.length === 0) {
      console.log('⚠️ 无真实订单数据，使用模拟数据')
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
          created_at: '2025-03-25T14:32:00Z',
          sku_id: null
        }
      ]
    } else {
      // 获取所有SKU ID用于关联查询产品实拍图
      const skuIds = ordersData.map(o => o.sku_id).filter(Boolean)
      
      // 并行查询SKU信息和产品图片
      let skuMap = {}
      let photoMap = {}
      
      if (skuIds.length > 0) {
        const [skuResult, photoResult] = await Promise.all([
          supabase.from('sku_mapping').select('id, sku_code, shape, color, size').in('id', skuIds),
          supabase.from('product_photos').select('sku_id, photo_url, photo_type').in('sku_id', skuIds).eq('is_active', true).order('sort_order', { ascending: true })
        ])
        
        // 构建SKU Map
        skuMap = skuResult.data
          ? Object.fromEntries(skuResult.data.map(s => [s.id, s]))
          : {}
        
        // 构建产品实拍图 Map
        if (photoResult.data) {
          const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
          photoResult.data.forEach(p => {
            if (!photoMap[p.sku_id]) {
              photoMap[p.sku_id] = `${supabaseUrl}/storage/v1/object/public/${p.photo_url}`
            }
          })
        }
      }
      
      // 转换订单数据格式
      orders.value = ordersData.map(order => {
        const skuInfo = skuMap[order.sku_id] || {}
        return {
          id: order.id,
          etsy_order_id: order.etsy_order_id,
          customer_name: order.customer_name || '未知客户',
          customer_email: order.customer_email || '',
          product_shape: order.product_shape || skuInfo.shape || '圆形',
          product_color: order.product_color || skuInfo.color || '金色',
          front_text: order.front_text || '',
          back_text: order.back_text || '',
          sku: skuInfo.sku_code || order.sku || '',
          size: order.size || skuInfo.size || 'L',
          country: order.country || '美国',
          font_code: order.font_code || 'F-04',
          status: order.status || 'pending',
          modify_request: order.modify_request || '',
          created_at: order.created_at,
          // 产品实拍图URL - 优先使用orders表的product_photo_url，其次查询product_photos表
          product_image_url: order.product_photo_url || photoMap[order.sku_id] || null,
          effect_image_url: order.effect_image_url || null,
          email_status: order.email_status || 'pending'
        }
      })
    }
    
    // 默认选中第一个订单（优先选择URL指定的订单）
    const targetOrderId = route.query.order_id
    if (targetOrderId && orders.value.length > 0) {
      const found = orders.value.find(o => o.id === targetOrderId)
      if (found) {
        await selectOrder(found)
        console.log('✅ 已加载目标订单:', targetOrderId)
      } else {
        // 未找到指定订单，选择第一个
        if (orders.value.length > 0) await selectOrder(orders.value[0])
      }
    } else if (orders.value.length > 0) {
      await selectOrder(orders.value[0])
    }
  } catch (e) {
    console.error('❌ 获取订单失败:', e)
    ElMessage.error('获取订单失败')
  }
}

// 选择订单
async function selectOrder(order) {
  selectedOrder.value = order
  // 重置客户修改要求
  customerModifyRequest.value = ''
  
  // 查询客户修改要求（从 service_link_logs 表）
  let modifyLogs = null
  try {
    const { data } = await supabase
      .from('service_link_logs')
      .select('message')
      .eq('order_id', order.id)
      .eq('type', 'customer_modify')
      .order('created_at', { ascending: false })
      .limit(1)
    modifyLogs = data
    if (modifyLogs && modifyLogs.length > 0) {
      customerModifyRequest.value = modifyLogs[0].message
    }
  } catch (e) {
    // 静默忽略，此功能为 UI 占位
    console.warn('查询客户修改要求失败:', e)
  }
  
  // 加载客户修改要求到 customerRequirement
  if (modifyLogs && modifyLogs.length > 0) {
    customerRequirement.value = modifyLogs[0].message || ''
  } else {
    customerRequirement.value = ''
  }
  
  // 加载邮件历史
  await fetchEmailHistory()
  
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
    '金色': 'Gold',
    '银色': 'Silver',
    '玫瑰金': 'RoseGold',
    '黑色': 'Black'
  }
  
  const shape = shapeMap[order.product_shape] || 'heart'
  const color = colorMap[order.product_color] || 'Silver'
  
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
  // 使用保存的 service_token 而非 design_token (token.value)
  const targetToken = serviceToken.value || token.value
  router.push(`/service/${shopCode.value}?token=${targetToken}`)
}

// 保存效果图到Supabase Storage
async function saveEffectImage() {
  if (!selectedOrder.value || !designerFrame.value) {
    ElMessage.warning('请先选择订单')
    return
  }
  
  savingEffect.value = true
  
  try {
    // 获取设计器生成的SVG数据
    const svgData = await new Promise((resolve, reject) => {
      const handleMessage = (event) => {
        if (event.data && event.data.type === 'svgData') {
          window.removeEventListener('message', handleMessage)
          resolve(event.data.svgData)
        }
      }
      window.addEventListener('message', handleMessage)
      designerFrame.value.contentWindow.postMessage({ type: 'getSVG' }, '*')
      
      // 5秒超时
      setTimeout(() => {
        window.removeEventListener('message', handleMessage)
        reject(new Error('获取SVG数据超时'))
      }, 5000)
    })
    
    // 上传SVG到Supabase Storage
    const fileBlob = new Blob([svgData], { type: 'image/svg+xml' })
    const fileName = `effect_${selectedOrder.value.id}_${Date.now()}.svg`
    
    const { data: uploadData, error: uploadError } = await supabase
      .storage
      .from('effect-images')
      .upload(fileName, fileBlob, {
        contentType: 'image/svg+xml',
        upsert: true
      })
    
    if (uploadError) {
      throw new Error(`Storage上传失败: ${uploadError.message}`)
    }
    
    // 获取公开URL
    const { data: urlData } = supabase
      .storage
      .from('effect-images')
      .getPublicUrl(fileName)
    
    const publicUrl = urlData.publicUrl
    
    // 更新订单记录
    const { error: updateError } = await supabase
      .from('orders')
      .update({
        effect_image_url: publicUrl,
        updated_at: new Date().toISOString()
      })
      .eq('id', selectedOrder.value.id)
    
    if (updateError) {
      throw new Error(`订单更新失败: ${updateError.message}`)
    }
    
    // 更新本地数据
    selectedOrder.value.effect_image_url = publicUrl
    
    ElMessage.success('效果图已保存')
    console.log('✅ 效果图已保存:', publicUrl)
  } catch (e) {
    console.error('❌ 保存效果图失败:', e)
    ElMessage.error('保存失败: ' + e.message)
  } finally {
    savingEffect.value = false
  }
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
    modifying: '修改中',
    '客户修改': '客户修改',
    '待回复': '待回复'
  }
  return map[status] || status
}

// 超时判断：创建超过24小时且未确认
function isOverdue(order) {
  if (!order || !order.created_at) return false
  if (order.email_status === 'confirmed') return false
  const createTime = new Date(order.created_at)
  const hours = (Date.now() - createTime.getTime()) / (1000 * 60 * 60)
  return hours > 24
}

function getOverdueHours(order) {
  if (!order || !order.created_at) return 0
  const createTime = new Date(order.created_at)
  return Math.floor((Date.now() - createTime.getTime()) / (1000 * 60 * 60))
}

// 初始化
onMounted(async () => {
  const valid = await validateToken()
  if (valid) {
    await fetchOrders()
  }
  // 加载自定义模板
  loadCustomTemplates()
  // 初始化编辑区内容
  templateEditContent.value = defaultFirstEmailTemplates[firstEmailTemplate.value]?.content || ''
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
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.loading-content {
  text-align: center;
}

.loading-icon {
  color: #409eff;
}

.loading-text {
  margin-top: 12px;
  color: #666;
  font-size: 14px;
}

.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  gap: 16px;
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
  padding: 12px 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 1900px;
  margin: 0 auto;
  padding: 0 24px;
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
  max-width: 1900px;
  margin: 16px auto;
  padding: 12px 24px;
  background: #fff;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 21px;
  box-sizing: border-box;
}

.order-label {
  font-size: 21px;
  color: #666;
  font-weight: 500;
}

.order-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.order-id {
  font-family: 'Arial Black', sans-serif;
  font-size: 21px;
  font-weight: 900;
  color: #dc2626;
}

.order-customer {
  font-size: 20px;
  color: #333;
}

/* 主内容区 */
.main-content {
  max-width: 1900px;
  margin: 0 auto;
  padding: 0 24px 24px;
  display: flex;
  gap: 16px;
  height: calc(100vh - 140px);
}

/* 左列 */
.left-column {
  width: 68%;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* 三卡片行 */
.info-cards-row {
  display: flex;
  gap: 8px;
}

.info-card {
  flex: 1;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
  min-width: 0;
}

.card-header {
  padding: 4px 8px;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
  font-size: 12px;
  font-weight: 600;
  color: #334155;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.card-body {
  padding: 6px 8px;
}

/* 订单详情卡片 */
.order-detail-card {
  display: flex;
  gap: 10px;
}

.order-thumb {
  width: 100px;
  height: 100px;
  flex-shrink: 0;
  border-radius: 6px;
  overflow: hidden;
  background: #f1f5f9;
}

.order-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.thumb-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  color: #94a3b8;
}

.order-info-compact {
  flex: 1;
  min-width: 0;
  padding-left: 4px;
}

.info-row {
  display: flex;
  font-size: 14px;
  line-height: 1.3;
}

.info-row .label {
  color: #64748b;
  width: 48px;
  flex-shrink: 0;
}

.info-row .value {
  color: #1e293b;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.info-row .order-id {
  color: #dc2626;
  font-weight: 600;
  font-size: 14px;
}

/* 效果图缩略图卡片 */
.effect-thumb-card {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.effect-thumb {
  max-height: 140px;
  width: auto;
  max-width: 100%;
  object-fit: contain;
}

.status-badge.generated {
  font-size: 10px;
  color: #16a34a;
}

/* 时间信息卡片 */
.time-info-card {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.time-row {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 22px;
}

.time-label {
  color: #64748b;
  white-space: nowrap;
}

.time-value {
  color: #1e293b;
  font-weight: 700;
}

.overdue-badge {
  background: #fef2f2;
  color: #dc2626;
  font-size: 22px;
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 600;
}

/* 设计器区域 */
.designer-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
  min-height: 0;
}

.designer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.designer-title {
  font-size: 13px;
  font-weight: 600;
  color: #334155;
  display: flex;
  align-items: center;
  gap: 6px;
}

.designer-icon {
  font-size: 16px;
}

.designer-hint {
  font-size: 11px;
  color: #94a3b8;
}

.designer-container {
  flex: 1;
  min-height: 0;
}

.designer-iframe {
  width: 100%;
  height: 100%;
  border: none;
}

/* 右列：邮件面板 */
.email-panel {
  width: 32%;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
}

/* Tab 切换 */
.email-tabs {
  display: flex;
  border-bottom: 2px solid #e2e8f0;
  background: #f8fafc;
}

.tab-btn {
  flex: 1;
  padding: 10px 0;
  border: none;
  background: none;
  font-size: 13px;
  font-weight: 500;
  color: #64748b;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  margin-bottom: -2px;
  transition: all 0.2s;
}

.tab-btn.active {
  color: #2563eb;
  border-bottom-color: #2563eb;
  background: #fff;
}

.tab-btn:hover:not(.active) {
  color: #334155;
  background: #f1f5f9;
}

/* Tab 内容区 */
.tab-content {
  flex: 1;
  overflow-y: auto;
  padding: 12px;
}

/* 过往邮件 Tab */
.email-history-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.history-item {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  padding: 10px;
}

.history-meta {
  display: flex;
  justify-content: space-between;
  margin-bottom: 6px;
}

.history-type {
  font-size: 11px;
  font-weight: 600;
  color: #2563eb;
  background: #eff6ff;
  padding: 1px 6px;
  border-radius: 3px;
}

.history-time {
  font-size: 11px;
  color: #94a3b8;
}

.history-content {
  font-size: 12px;
  color: #475569;
  line-height: 1.6;
  white-space: pre-wrap;
}

.empty-hint {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  color: #94a3b8;
  font-size: 13px;
}

.empty-hint span {
  font-size: 32px;
  margin-bottom: 8px;
}

/* 邮件回复 Tab */
.reply-tab {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.reply-section {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.section-label {
  font-size: 12px;
  font-weight: 600;
  color: #334155;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.section-label-inline {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #334155;
}

/* 预设快捷内容 */
.preset-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.preset-tag {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 3px 8px;
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  font-size: 11px;
  color: #475569;
  cursor: pointer;
  transition: all 0.2s;
  user-select: none;
}

.preset-tag:hover {
  background: #e2e8f0;
}

.preset-tag.checked {
  background: #eff6ff;
  border-color: #93c5fd;
  color: #2563eb;
}

.preset-tag input[type="checkbox"] {
  width: 12px;
  height: 12px;
  margin: 0;
}

/* 客户要求 */
.requirement-input {
  width: 100%;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  padding: 8px 10px;
  font-size: 12px;
  color: #334155;
  resize: vertical;
  line-height: 1.5;
  box-sizing: border-box;
  min-height: 100px;
}

.requirement-input:focus {
  outline: none;
  border-color: #93c5fd;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
}

/* 生成按钮 */
.generate-btn {
  padding: 3px 10px;
  background: #7c3aed;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 11px;
  cursor: pointer;
  transition: background 0.2s;
}

.generate-btn:hover:not(:disabled) {
  background: #6d28d9;
}

.generate-btn:disabled {
  background: #c4b5fd;
  cursor: not-allowed;
}

/* AI回复框 */
.ai-reply-box {
  width: 100%;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  padding: 10px;
  font-size: 12px;
  color: #334155;
  line-height: 1.6;
  resize: vertical;
  min-height: 320px;
  box-sizing: border-box;
  background: #fefce8;
}

.ai-reply-box:focus {
  outline: none;
  border-color: #a78bfa;
  box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.1);
}

/* 落款选择 */
.sender-select {
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  padding: 3px 8px;
  font-size: 12px;
  color: #334155;
}

.custom-sender-input {
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  padding: 3px 8px;
  font-size: 12px;
  width: 80px;
}

/* 操作按钮行 */
.action-btn-row {
  display: flex;
  gap: 8px;
  padding-top: 8px;
  border-top: 1px solid #f0f0f0;
  flex-wrap: wrap;
}

.action-btn {
  flex: 1;
  min-width: 0;
  padding: 8px 4px;
  border: none;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.action-btn.secondary {
  background: #fff;
  border: 1px solid #cbd5e1;
  color: #475569;
}

.action-btn.secondary:hover {
  background: #f8fafc;
}

.action-btn.primary {
  background: #2563eb;
  color: #fff;
}

.action-btn.primary:hover {
  background: #1d4ed8;
}

.action-btn.success {
  background: #16a34a;
  color: #fff;
}

.action-btn.success:hover:not(:disabled) {
  background: #15803d;
}

.action-btn.disabled {
  background: #e2e8f0;
  color: #94a3b8;
  cursor: not-allowed;
}

/* 未选择订单提示 */
.no-order-selected {
  max-width: 1900px;
  margin: 40px auto;
  padding: 40px;
  background: #fff;
  border-radius: 8px;
  text-align: center;
}
</style>
