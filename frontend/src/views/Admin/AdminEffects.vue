<template>
  <div class="h-full overflow-hidden bg-slate-50 p-4 flex flex-col">
    <!-- 页面标题 -->
    <div class="mb-4 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-slate-800">邮件模板</h1>
        <p class="text-sm text-slate-500 mt-1">运营话术参考知识库</p>
      </div>
      <button 
        @click="showOrderSelector = true"
        class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium flex items-center gap-2 transition-colors"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
        从订单生成邮件
      </button>
    </div>

    <!-- 联动模式提示条 -->
    <div v-if="isOrderMode" class="mb-4 bg-blue-50 border-l-4 border-blue-500 p-4 rounded-r-lg flex items-center justify-between">
      <div class="flex items-center gap-3">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="2"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
        <span class="text-blue-700 font-medium">为订单 #{{ linkedOrder.id }} 生成追评邮件</span>
        <span class="text-blue-600 text-sm">（客户: {{ linkedOrder.customer }}）</span>
      </div>
      <button @click="exitOrderMode" class="text-blue-600 hover:text-blue-700 text-sm">
        ✕ 退出联动模式
      </button>
    </div>

    <!-- 主体内容 -->
    <div class="flex-1 flex gap-4 min-h-0">
      <!-- 左侧：分类Tab -->
      <div class="w-[220px] bg-gray-800 rounded-xl overflow-hidden flex flex-col">
        <div class="p-3 border-b border-gray-700">
          <h3 class="text-gray-300 text-xs font-medium">邮件分类</h3>
        </div>
        <div class="flex-1 overflow-y-auto">
          <div 
            v-for="category in categories" 
            :key="category.id"
            class="border-b border-gray-700/50 last:border-0"
          >
            <button 
              @click="selectCategory(category.id)"
              :class="[
                'w-full px-4 py-3 text-left text-sm flex items-center gap-2 transition-colors',
                activeCategory === category.id 
                  ? 'bg-blue-600 text-white' 
                  : 'text-gray-300 hover:bg-gray-700'
              ]"
            >
              <span>{{ category.icon }}</span>
              <span>{{ category.name }}</span>
            </button>
            <!-- 选中分类的模板列表 -->
            <div v-if="activeCategory === category.id" class="bg-gray-900/50 px-2 py-2">
              <button
                v-for="template in getCategoryTemplates(category.id)"
                :key="template.id"
                @click="selectTemplate(template)"
                :class="[
                  'w-full px-3 py-2 text-left text-xs rounded transition-colors mb-1 last:mb-0',
                  selectedTemplate?.id === template.id
                    ? 'bg-blue-500/30 text-blue-200'
                    : 'text-gray-400 hover:bg-gray-700 hover:text-gray-200'
                ]"
              >
                {{ template.name }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧：模板内容区 -->
      <div class="flex-1 bg-white rounded-xl shadow-sm border border-slate-200 flex flex-col overflow-hidden">
        <!-- 模板标题栏 -->
        <div class="px-4 py-3 border-b border-slate-200 flex items-center justify-between bg-slate-50">
          <div class="flex items-center gap-2">
            <h3 class="font-bold text-slate-800">{{ selectedTemplate?.name || '请选择模板' }}</h3>
            <span v-if="selectedTemplate" class="text-xs text-slate-400">{{ getCategoryName(activeCategory) }}</span>
          </div>
          <div v-if="selectedTemplate && !isOrderMode" class="flex items-center gap-2">
            <button 
              @click="isEditing = !isEditing"
              class="px-3 py-1.5 text-sm flex items-center gap-1 rounded transition-colors"
              :class="isEditing ? 'bg-blue-600 text-white' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/></svg>
              {{ isEditing ? '完成编辑' : '编辑' }}
            </button>
            <button 
              @click="copyTemplate"
              class="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-600 text-sm flex items-center gap-1 rounded transition-colors"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>
              复制
            </button>
          </div>
        </div>

        <!-- 模板内容 -->
        <div v-if="selectedTemplate" class="flex-1 p-4 overflow-y-auto">
          <!-- Subject 行 -->
          <div class="mb-4">
            <label class="block text-xs font-medium text-slate-500 mb-1">Subject（邮件主题）</label>
            <div v-if="isEditing && !isOrderMode" class="relative">
              <input 
                v-model="editSubject"
                type="text"
                class="w-full px-3 py-2 border border-blue-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/30"
              />
            </div>
            <div v-else class="bg-slate-50 rounded-lg px-3 py-2 text-sm text-slate-700">
              <template v-if="isOrderMode">{{ renderedSubject }}</template>
              <template v-else>
                <span v-html="highlightVariables(selectedTemplate.subject)"></span>
              </template>
            </div>
          </div>

          <!-- Body 区域 -->
          <div class="mb-4">
            <label class="block text-xs font-medium text-slate-500 mb-1">Body（邮件正文）</label>
            <div v-if="isEditing && !isOrderMode" class="relative">
              <textarea 
                v-model="editBody"
                rows="12"
                class="w-full px-3 py-2 border border-blue-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/30 resize-none font-mono"
              ></textarea>
            </div>
            <div v-else-if="isOrderMode">
              <textarea 
                v-model="generatedEmail"
                rows="12"
                class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/30 resize-none bg-white"
              ></textarea>
            </div>
            <div v-else class="bg-slate-50 rounded-lg px-3 py-3 text-sm text-slate-700 whitespace-pre-wrap leading-relaxed min-h-[200px]">
              <span v-html="highlightVariables(selectedTemplate.body)"></span>
            </div>
          </div>

          <!-- 联动模式：操作按钮 -->
          <div v-if="isOrderMode" class="flex items-center gap-3 pt-4 border-t border-slate-200">
            <button 
              @click="sendEmail"
              class="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium flex items-center gap-2 transition-colors"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
              发送邮件
            </button>
            <button 
              @click="goBackToOrders"
              class="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-600 rounded-lg text-sm font-medium flex items-center gap-2 transition-colors"
            >
              ← 返回订单列表
            </button>
          </div>

          <!-- 变量说明区（折叠面板） -->
          <div v-if="!isOrderMode" class="mt-4 border-t border-slate-200 pt-4">
            <button 
              @click="showVariables = !showVariables"
              class="flex items-center gap-2 text-sm text-slate-500 hover:text-slate-700"
            >
              <svg 
                xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                :class="['transition-transform', showVariables ? 'rotate-90' : '']"
              >
                <path d="m9 18 6-6-6-6"/>
              </svg>
              变量说明
            </button>
            <div v-if="showVariables" class="mt-3 bg-slate-50 rounded-lg p-4 text-xs">
              <div class="grid grid-cols-2 gap-2">
                <div v-for="(desc, key) in variableDescriptions" :key="key" class="flex items-center gap-2">
                  <span class="inline-block bg-blue-100 text-blue-700 px-2 py-0.5 rounded font-mono">{{ key }}</span>
                  <span class="text-slate-500">= {{ desc }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 未选择模板时的空状态 -->
        <div v-else class="flex-1 flex items-center justify-center text-slate-400">
          <div class="text-center">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" class="mx-auto mb-3 opacity-50"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
            <p>请在左侧选择一个邮件模板</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

// 分类数据
const categories = [
  { id: 'confirm', name: '首封确认邮件', icon: '📧' },
  { id: 'natural', name: '自然语言风格', icon: '💬' },
  { id: 'delay', name: '延迟/异常说明', icon: '⚠️' },
  { id: 'review', name: '追评邮件', icon: '⭐' },
  { id: 'faq', name: '常见问题回复', icon: '❓' },
]

// 模板数据
const templates = ref([
  // 首封确认邮件
  { id: 'confirm_1', category: 'confirm', name: '标准确认邮件', subject: 'Your order #ORDER_ID is confirmed!', body: 'Dear CUSTOMER_NAME,\n\nThank you for your order! We have received your order #ORDER_ID for a custom PRODUCT_NAME in PRODUCT_COLOR.\n\nYour customization details:\n- Front: FRONT_TEXT\n- Back: BACK_TEXT\n\nWe will begin production shortly and keep you updated on the progress.\n\nBest regards,\nSTORE_NAME Team' },
  { id: 'confirm_2', category: 'confirm', name: '带效果图确认', subject: 'Your custom PRODUCT_NAME is ready for production!', body: 'Hi CUSTOMER_NAME,\n\nWe have prepared the design preview for your custom PRODUCT_NAME.\n\nPlease review the attached effect image and let us know if everything looks correct. Once confirmed, we will start production immediately!\n\nOrder Details:\n- Order ID: ORDER_ID\n- Product: PRODUCT_NAME (PRODUCT_COLOR)\n- Front Text: FRONT_TEXT\n- Back Text: BACK_TEXT\n\nLooking forward to your confirmation!\n\nWarm regards,\nSTORE_NAME' },
  
  // 自然语言风格
  { id: 'natural_1', category: 'natural', name: '友好问候', subject: 'Hello from STORE_NAME!', body: 'Hey CUSTOMER_NAME!\n\nJust wanted to reach out and say thanks for choosing us for your custom pet tag!\n\nWe are super excited to create FRONT_TEXT new tag. It is going to look amazing in PRODUCT_COLOR!\n\nIf you have any questions or need anything, just hit reply - we are here to help!\n\nCheers,\nThe STORE_NAME Family' },
  { id: 'natural_2', category: 'natural', name: '温馨提醒', subject: 'Quick update on your order!', body: 'Hi CUSTOMER_NAME,\n\nHope you are having a great day!\n\nJust a quick note to let you know your custom PRODUCT_NAME is coming along beautifully. We are putting extra care into making sure FRONT_TEXT tag is perfect.\n\nWe will send you a tracking number as soon as it ships!\n\nTake care,\nSTORE_NAME' },
  
  // 延迟/异常说明
  { id: 'delay_1', category: 'delay', name: '物流延迟通知', subject: 'Update on your order #ORDER_ID shipping', body: 'Dear CUSTOMER_NAME,\n\nWe wanted to let you know about a slight delay with your order #ORDER_ID.\n\nDue to [reason], your PRODUCT_NAME shipment is experiencing a small delay. We expect it to arrive within [X] additional days.\n\nYour tracking number: TRACKING_NUMBER\n\nWe sincerely apologize for any inconvenience and appreciate your patience.\n\nBest regards,\nSTORE_NAME Customer Support' },
  { id: 'delay_2', category: 'delay', name: '生产问题说明', subject: 'Important update about your custom order', body: 'Dear CUSTOMER_NAME,\n\nThank you for your patience. We wanted to inform you about a small issue we encountered while creating your custom PRODUCT_NAME.\n\n[Describe issue]\n\nTo ensure you receive a perfect product, we need [X] additional days. We hope you understand our commitment to quality.\n\nPlease let us know if you have any questions.\n\nSincerely,\nSTORE_NAME Production Team' },
  
  // 追评邮件
  { id: 'review_1', category: 'review', name: '标准追评', subject: 'How are you enjoying your PRODUCT_NAME?', body: 'Dear CUSTOMER_NAME,\n\nIt has been a while since your custom PRODUCT_NAME was delivered, and we hope you and FRONT_TEXT are loving it!\n\nWe would be so grateful if you could take a moment to share your experience with a review. Your feedback helps other pet lovers find the perfect tag for their furry friends.\n\nThank you for choosing STORE_NAME!\n\nWarm regards,\nThe STORE_NAME Team' },
  { id: 'review_2', category: 'review', name: '个性化追评', subject: 'CUSTOMER_NAME, we would love your feedback!', body: 'Hi CUSTOMER_NAME,\n\nWe hope FRONT_TEXT is proudly wearing their new PRODUCT_COLOR PRODUCT_NAME!\n\nIt has been about DELIVERED_DAYS days since your order arrived, and we are curious - how is the tag holding up? Is the engraving clear? Does FRONT_TEXT love showing it off?\n\nYour honest review would mean the world to us and help other pet parents make their decision.\n\nWith warm regards,\nThe STORE_NAME Team' },
  { id: 'review_3', category: 'review', name: '二次追评', subject: 'A gentle reminder from STORE_NAME', body: 'Dear CUSTOMER_NAME,\n\nWe noticed you have not had a chance to review your recent purchase yet - no worries, we know life gets busy!\n\nIf you have a spare moment, we would love to hear how FRONT_TEXT is enjoying their custom tag. Even a quick star rating helps!\n\nThank you for being part of our pet-loving community.\n\nBest wishes,\nSTORE_NAME' },
  
  // 常见问题回复
  { id: 'faq_1', category: 'faq', name: '修改订单请求', subject: 'Re: Order modification request - #ORDER_ID', body: 'Dear CUSTOMER_NAME,\n\nThank you for reaching out about modifying your order #ORDER_ID.\n\n[If possible]: Great news! We can still make changes since production has not started. Please confirm the updated details:\n- New Front Text: [text]\n- New Back Text: [text]\n\n[If not possible]: Unfortunately, production has already begun on your PRODUCT_NAME. However, we can [offer alternatives].\n\nPlease let us know how you would like to proceed.\n\nBest regards,\nSTORE_NAME Support' },
  { id: 'faq_2', category: 'faq', name: '物流查询回复', subject: 'Re: Tracking information for order #ORDER_ID', body: 'Dear CUSTOMER_NAME,\n\nThank you for your inquiry about your order #ORDER_ID.\n\nYour tracking number is: TRACKING_NUMBER\n\nYou can track your package here: [tracking link]\n\nPlease note that international shipments may take 10-20 business days depending on your location. The tracking may not update until the package reaches your country.\n\nIf you have any other questions, feel free to ask!\n\nBest regards,\nSTORE_NAME Support' },
])

// 状态
const activeCategory = ref('confirm')
const selectedTemplate = ref(null)
const isEditing = ref(false)
const editSubject = ref('')
const editBody = ref('')
const showVariables = ref(false)
const showOrderSelector = ref(false)
const generatedEmail = ref('')

// 变量说明
const variableDescriptions = {
  'CUSTOMER_NAME': '客户名',
  'ORDER_ID': '订单号',
  'PRODUCT_NAME': '产品名称（如 heart-shaped pet tag）',
  'PRODUCT_COLOR': '产品颜色',
  'FRONT_TEXT': '正面定制文字',
  'BACK_TEXT': '背面定制文字',
  'STORE_NAME': '店铺名称',
  'TRACKING_NUMBER': '物流单号',
  'DELIVERED_DAYS': '已交货天数',
}

// 联动订单假数据
const mockLinkedOrder = {
  id: '4002217518',
  customer: 'Luna Parker',
  product: 'heart-shaped pet tag',
  color: 'gold',
  frontText: 'Luna',
  backText: '416.456.3524',
  deliveredDays: 10,
  storeName: 'Pet Tag Studio',
  trackingNo: '4PX1234567890'
}

// 判断是否为联动模式
const isOrderMode = computed(() => route.query.action === 'review')

// 联动订单数据
const linkedOrder = computed(() => {
  if (isOrderMode.value) {
    return {
      ...mockLinkedOrder,
      id: route.query.orderId || mockLinkedOrder.id
    }
  }
  return null
})

// 渲染后的主题
const renderedSubject = computed(() => {
  if (!selectedTemplate.value || !linkedOrder.value) return ''
  return replaceVariables(selectedTemplate.value.subject, linkedOrder.value)
})

// 获取分类的模板
const getCategoryTemplates = (categoryId) => {
  return templates.value.filter(t => t.category === categoryId)
}

// 获取分类名称
const getCategoryName = (categoryId) => {
  return categories.find(c => c.id === categoryId)?.name || ''
}

// 选择分类
const selectCategory = (categoryId) => {
  activeCategory.value = categoryId
  // 自动选择该分类的第一个模板
  const categoryTemplates = getCategoryTemplates(categoryId)
  if (categoryTemplates.length > 0) {
    selectTemplate(categoryTemplates[0])
  }
}

// 选择模板
const selectTemplate = (template) => {
  selectedTemplate.value = template
  editSubject.value = template.subject
  editBody.value = template.body
  isEditing.value = false
  
  // 如果是联动模式，自动生成邮件
  if (isOrderMode.value && linkedOrder.value) {
    generateEmailContent()
  }
}

// 替换变量
const replaceVariables = (text, order) => {
  return text
    .replace(/CUSTOMER_NAME/g, order.customer.split(' ')[0])
    .replace(/ORDER_ID/g, order.id)
    .replace(/PRODUCT_NAME/g, order.product)
    .replace(/PRODUCT_COLOR/g, order.color)
    .replace(/FRONT_TEXT/g, order.frontText)
    .replace(/BACK_TEXT/g, order.backText)
    .replace(/STORE_NAME/g, order.storeName)
    .replace(/TRACKING_NUMBER/g, order.trackingNo)
    .replace(/DELIVERED_DAYS/g, order.deliveredDays.toString())
}

// 生成邮件内容
const generateEmailContent = () => {
  if (!selectedTemplate.value || !linkedOrder.value) return
  generatedEmail.value = replaceVariables(selectedTemplate.value.body, linkedOrder.value)
}

// 高亮变量
const highlightVariables = (text) => {
  const vars = Object.keys(variableDescriptions)
  let result = text
  vars.forEach(v => {
    result = result.replace(new RegExp(v, 'g'), '<span class="inline-block bg-blue-100 text-blue-700 px-1.5 py-0.5 rounded text-xs font-mono mx-0.5">' + v + '</span>')
  })
  // 处理换行
  return result.replace(/\n/g, '<br>')
}

// 复制模板
const copyTemplate = async () => {
  if (!selectedTemplate.value) return
  const content = 'Subject: ' + selectedTemplate.value.subject + '\n\n' + selectedTemplate.value.body
  try {
    await navigator.clipboard.writeText(content)
    alert('模板已复制到剪贴板！')
  } catch (e) {
    alert('复制失败，请手动复制')
  }
}

// 发送邮件
const sendEmail = () => {
  if (!linkedOrder.value) return
  alert('追评邮件已发送给 ' + linkedOrder.value.customer + '！\n\n订单号: ' + linkedOrder.value.id)
  // 返回订单列表
  router.push('/admin/completed')
}

// 返回订单列表
const goBackToOrders = () => {
  router.push('/admin/completed')
}

// 退出联动模式
const exitOrderMode = () => {
  router.replace({ path: '/admin/effects' })
}

// 初始化
onMounted(() => {
  // 如果是联动模式，自动选择追评邮件分类
  if (isOrderMode.value) {
    activeCategory.value = 'review'
    const reviewTemplates = getCategoryTemplates('review')
    if (reviewTemplates.length > 0) {
      selectTemplate(reviewTemplates[1]) // 选择"个性化追评"模板
    }
  } else {
    // 默认选择第一个分类的第一个模板
    const firstCategoryTemplates = getCategoryTemplates('confirm')
    if (firstCategoryTemplates.length > 0) {
      selectTemplate(firstCategoryTemplates[0])
    }
  }
})

// 监听路由变化
watch(() => route.query, () => {
  if (isOrderMode.value) {
    activeCategory.value = 'review'
    const reviewTemplates = getCategoryTemplates('review')
    if (reviewTemplates.length > 0) {
      selectTemplate(reviewTemplates[1])
    }
  }
}, { immediate: true })
</script>

<style scoped>
/* 自定义滚动条 */
::-webkit-scrollbar {
  width: 6px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>
