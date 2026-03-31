<template>
  <div class="h-full overflow-auto bg-slate-50 p-4">
    <!-- 页面标题 -->
    <div class="mb-4 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-slate-800">已完成订单</h1>
        <p class="text-sm text-slate-500 mt-1">管理已完成订单、追踪物流并发送追评邮件</p>
      </div>
      <div class="text-sm text-slate-600">
        总计: <span class="font-bold text-slate-800">{{ totalCount }} 笔</span>
      </div>
    </div>

    <!-- 搜索/筛选栏 -->
    <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-4 mb-4">
      <div class="flex flex-wrap items-center gap-3">
        <!-- 搜索框 -->
        <div class="flex-1 min-w-[200px]">
          <input 
            v-model="searchText" 
            type="text" 
            placeholder="搜索订单号/客户名..."
            class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
          />
        </div>
        <!-- 日期范围 -->
        <div class="flex items-center gap-2">
          <input 
            v-model="dateStart" 
            type="date" 
            class="px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
          />
          <span class="text-slate-400">至</span>
          <input 
            v-model="dateEnd" 
            type="date" 
            class="px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
          />
        </div>
        <!-- 店铺筛选 -->
        <select v-model="shopFilter" class="px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500">
          <option value="">全部店铺</option>
          <option v-for="shop in shopOptions" :key="shop" :value="shop">{{ shop }}</option>
        </select>
        <!-- 产品筛选 -->
        <select v-model="productFilter" class="px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500">
          <option value="">全部产品</option>
          <option value="HC">心形</option>
          <option value="BO">骨头形</option>
          <option value="CI">圆形</option>
        </select>
        <!-- 按钮 -->
        <button @click="handleSearch" class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium transition-colors">
          搜索
        </button>
        <button @click="handleReset" class="px-4 py-2 bg-white border border-slate-200 hover:bg-slate-50 text-slate-600 rounded-lg text-sm font-medium transition-colors">
          重置
        </button>
      </div>
    </div>

    <!-- 订单列表表格 -->
    <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm text-left">
          <thead class="bg-slate-50 text-slate-600 font-medium border-b border-slate-200">
            <tr class="h-[44px]">
              <th class="px-4 whitespace-nowrap font-medium">订单号</th>
              <th class="px-4 whitespace-nowrap font-medium">客户</th>
              <th class="px-4 whitespace-nowrap font-medium">SKU</th>
              <th class="px-4 whitespace-nowrap font-medium">完成日期</th>
              <th class="px-4 whitespace-nowrap font-medium">发货日期</th>
              <th class="px-4 whitespace-nowrap font-medium">物流单号</th>
              <th class="px-4 whitespace-nowrap font-medium">已交货天数</th>
              <th class="px-4 whitespace-nowrap font-medium">生产文档</th>
              <th class="px-4 whitespace-nowrap font-medium">追评状态</th>
              <th class="px-4 whitespace-nowrap font-medium">操作</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <template v-for="order in paginatedOrders" :key="order.id">
              <!-- 主行 -->
              <tr 
                @click="toggleExpand(order.id)"
                :class="[
                  'transition-colors cursor-pointer',
                  expandedId === order.id ? 'bg-slate-50' : 'hover:bg-slate-50',
                  getRowBorderClass(order)
                ]"
              >
                <td class="px-4 py-3 whitespace-nowrap font-medium text-slate-700">{{ order.etsy_order_id || order.id }}</td>
                <td class="px-4 py-3 whitespace-nowrap text-slate-600">{{ order.customer_name }}</td>
                <td class="px-4 py-3 whitespace-nowrap font-mono text-slate-500 text-xs">{{ order.sku_mapping?.sku_code || '-' }}</td>
                <td class="px-4 py-3 whitespace-nowrap text-slate-500">{{ formatDate(order.completed_at || order.created_at) }}</td>
                <td class="px-4 py-3 whitespace-nowrap text-slate-500">{{ formatDate(order.shipped_at) || '-' }}</td>
                <td class="px-4 py-3 whitespace-nowrap font-mono text-xs text-slate-500">{{ order.tracking_number || '-' }}</td>
                <td class="px-4 py-3 whitespace-nowrap">
                  <span :class="getDaysClass(calculateDeliveredDays(order))">{{ formatDeliveredDays(order) }}</span>
                </td>
                <td class="px-4 py-3 whitespace-nowrap">
                  <a v-if="order.production_pdf_url" href="#" @click.stop.prevent="viewPdf(order)" class="text-blue-600 hover:text-blue-700 flex items-center gap-1">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                    查看PDF
                  </a>
                  <span v-else class="text-red-500 flex items-center gap-1">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" x2="12" y1="9" y2="13"/><line x1="12" x2="12.01" y1="17" y2="17"/></svg>
                    生产文档缺失
                  </span>
                </td>
                <td class="px-4 py-3 whitespace-nowrap">
                  <span :class="getReviewStatusClass(order)">{{ getReviewStatusText(order) }}</span>
                </td>
                <td class="px-4 py-3 whitespace-nowrap">
                  <button 
                    v-if="!order.review_sent && calculateDeliveredDays(order) >= 8"
                    @click.stop="sendReviewEmail(order)"
                    class="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded text-xs font-medium transition-colors"
                  >
                    发送追评邮件
                  </button>
                  <button 
                    v-else-if="order.review_sent"
                    disabled
                    class="px-3 py-1.5 bg-slate-100 text-slate-400 rounded text-xs font-medium cursor-not-allowed"
                  >
                    已发送 ✓
                  </button>
                  <button 
                    v-else
                    disabled
                    class="px-3 py-1.5 bg-slate-100 text-slate-400 rounded text-xs font-medium cursor-not-allowed"
                  >
                    发送追评邮件
                  </button>
                </td>
              </tr>
              <!-- 展开详情行 -->
              <tr v-if="expandedId === order.id">
                <td colspan="10" class="p-0">
                  <div class="bg-slate-50 p-4 border-t border-slate-200 transition-all">
                    <div class="grid grid-cols-2 gap-6">
                      <!-- 左侧：订单详情 -->
                      <div>
                        <h4 class="font-bold text-slate-700 mb-3 text-sm">完整订单信息</h4>
                        <div class="grid grid-cols-2 gap-3 text-sm">
                          <div class="flex justify-between bg-white rounded-lg p-2">
                            <span class="text-slate-400">正面文字:</span>
                            <span class="text-slate-700 font-medium">{{ order.frontText }}</span>
                          </div>
                          <div class="flex justify-between bg-white rounded-lg p-2">
                            <span class="text-slate-400">字体:</span>
                            <span class="text-slate-700 font-medium">{{ order.font }}</span>
                          </div>
                          <div class="flex justify-between bg-white rounded-lg p-2">
                            <span class="text-slate-400">背面文字:</span>
                            <span class="text-slate-700 font-medium">{{ order.backText }}</span>
                          </div>
                          <div class="flex justify-between bg-white rounded-lg p-2">
                            <span class="text-slate-400">形状:</span>
                            <span class="text-slate-700 font-medium">{{ order.shape }}</span>
                          </div>
                          <div class="flex justify-between bg-white rounded-lg p-2">
                            <span class="text-slate-400">颜色:</span>
                            <span class="text-slate-700 font-medium">{{ order.color }}</span>
                          </div>
                          <div class="flex justify-between bg-white rounded-lg p-2">
                            <span class="text-slate-400">尺寸:</span>
                            <span class="text-slate-700 font-medium">{{ order.size }}</span>
                          </div>
                          <div class="flex justify-between bg-white rounded-lg p-2">
                            <span class="text-slate-400">工艺:</span>
                            <span class="text-slate-700 font-medium">{{ order.craft }}</span>
                          </div>
                        </div>
                      </div>
                      <!-- 右侧：生产文档预览 -->
                      <div>
                        <h4 class="font-bold text-slate-700 mb-3 text-sm">生产文档预览</h4>
                        <div v-if="order.production_pdf_url" class="bg-white rounded-lg border border-slate-200 p-4">
                          <div class="bg-slate-100 rounded-lg h-32 flex items-center justify-center mb-3">
                            <div class="text-center text-slate-500">
                              <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="mx-auto mb-2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                              <p class="text-xs">POD_{{ order.etsy_order_id || order.id }}.pdf</p>
                            </div>
                          </div>
                          <div class="flex gap-2">
                            <button @click.stop="viewPdf(order)" class="flex-1 px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded text-xs font-medium flex items-center justify-center gap-1 transition-colors">
                              <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                              查看
                            </button>
                            <button @click.stop="downloadPdf(order)" class="flex-1 px-3 py-1.5 bg-slate-700 hover:bg-slate-800 text-white rounded text-xs font-medium flex items-center justify-center gap-1 transition-colors">
                              <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>
                              下载
                            </button>
                            <button @click.stop="printPdf(order)" class="flex-1 px-3 py-1.5 bg-white border border-slate-200 hover:bg-slate-50 text-slate-600 rounded text-xs font-medium flex items-center justify-center gap-1 transition-colors">
                              <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect width="12" height="8" x="6" y="14"/></svg>
                              打印
                            </button>
                          </div>
                        </div>
                        <div v-else class="bg-red-50 rounded-lg border border-red-200 p-4 text-center">
                          <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="1.5" class="mx-auto mb-2"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" x2="12" y1="9" y2="13"/><line x1="12" x2="12.01" y1="17" y2="17"/></svg>
                          <p class="text-red-600 font-medium text-sm">生产文档缺失</p>
                          <p class="text-red-500 text-xs mt-1">请联系生产部门补充文档</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </td>
              </tr>
            </template>
            <tr v-if="paginatedOrders.length === 0" class="h-[100px]">
              <td colspan="10" class="px-4 text-center text-slate-400">暂无已完成订单</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 分页 -->
      <div class="px-4 py-3 border-t border-slate-200 flex items-center justify-between">
        <div class="text-sm text-slate-500">
          显示 {{ (currentPage - 1) * pageSize + 1 }} - {{ Math.min(currentPage * pageSize, filteredOrders.length) }} 条，共 {{ filteredOrders.length }} 条
        </div>
        <div class="flex items-center gap-2">
          <button 
            @click="currentPage = currentPage - 1" 
            :disabled="currentPage === 1"
            class="px-3 py-1.5 border border-slate-200 rounded text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-slate-50 transition-colors"
          >
            上一页
          </button>
          <span class="text-sm text-slate-600">{{ currentPage }} / {{ totalPages }}</span>
          <button 
            @click="currentPage = currentPage + 1" 
            :disabled="currentPage >= totalPages"
            class="px-3 py-1.5 border border-slate-200 rounded text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-slate-50 transition-colors"
          >
            下一页
          </button>
          <select v-model="pageSize" class="px-2 py-1.5 border border-slate-200 rounded text-sm">
            <option :value="10">10条/页</option>
            <option :value="20">20条/页</option>
            <option :value="50">50条/页</option>
          </select>
        </div>
      </div>
    </div>

    <!-- 追评邮件对话框 -->
    <el-dialog 
      v-model="showReviewEmailDialog" 
      title="发送追评邮件" 
      width="700px"
      :close-on-click-modal="false"
    >
      <div v-if="selectedOrderForReview" class="space-y-4">
        <!-- 订单信息 -->
        <div class="bg-slate-50 rounded-lg p-3">
          <div class="flex items-center justify-between">
            <div>
              <span class="text-sm text-slate-500">订单号：</span>
              <span class="font-medium text-slate-700">{{ selectedOrderForReview.etsy_order_id || selectedOrderForReview.id }}</span>
            </div>
            <div>
              <span class="text-sm text-slate-500">客户：</span>
              <span class="font-medium text-slate-700">{{ selectedOrderForReview.customer_name }}</span>
            </div>
            <div>
              <span class="text-sm text-slate-500">已交货：</span>
              <span class="font-medium text-orange-600">{{ formatDeliveredDays(selectedOrderForReview) }}</span>
            </div>
          </div>
        </div>

        <!-- 模板选择 -->
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-2">场景模板</label>
          <select 
            v-model="selectedTemplate" 
            @change="generateReviewEmail"
            class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20"
            :disabled="reviewTemplatesLoading"
          >
            <option v-for="tpl in reviewTemplates" :key="tpl.id" :value="tpl">{{ tpl.name }}</option>
          </select>
        </div>

        <!-- 风格设置 -->
        <div class="grid grid-cols-3 gap-4">
          <!-- 语气 -->
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-2">语气</label>
            <div class="flex gap-1">
              <button 
                v-for="opt in toneOptions" 
                :key="opt.value"
                @click="emailTone = opt.value; generateReviewEmail()"
                :class="[
                  'flex-1 px-2 py-1.5 rounded text-xs font-medium transition-colors',
                  emailTone === opt.value 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                ]"
              >
                {{ opt.label }}
              </button>
            </div>
          </div>
          
          <!-- 长度 -->
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-2">长度</label>
            <div class="flex gap-1">
              <button 
                v-for="opt in lengthOptions" 
                :key="opt.value"
                @click="emailLength = opt.value; generateReviewEmail()"
                :class="[
                  'flex-1 px-2 py-1.5 rounded text-xs font-medium transition-colors',
                  emailLength === opt.value 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                ]"
              >
                {{ opt.label }}
              </button>
            </div>
          </div>
          
          <!-- 落款人 -->
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-2">落款人</label>
            <select 
              v-model="senderName" 
              @change="generateReviewEmail"
              class="w-full px-2 py-1.5 border border-slate-200 rounded text-xs focus:outline-none focus:ring-2 focus:ring-blue-500/20"
            >
              <option v-for="opt in senderOptions" :key="opt" :value="opt">{{ opt }}</option>
            </select>
          </div>
        </div>

        <!-- 邮件预览 -->
        <div class="grid grid-cols-2 gap-4">
          <!-- 英文版本 -->
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-2">English Version</label>
            <textarea 
              v-model="emailContentEnglish"
              rows="8"
              class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 font-mono"
              placeholder="邮件内容..."
            ></textarea>
          </div>
          
          <!-- 中文版本 -->
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-2">中文版本</label>
            <textarea 
              v-model="emailContentChinese"
              rows="8"
              class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 font-mono"
              placeholder="邮件内容..."
            ></textarea>
          </div>
        </div>
      </div>

      <!-- 对话框底部按钮 -->
      <template #footer>
        <div class="flex items-center justify-between">
          <button 
            @click="copyReviewEmail"
            class="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-sm font-medium transition-colors"
          >
            📋 复制内容
          </button>
          <div class="flex gap-2">
            <button 
              @click="showReviewEmailDialog = false"
              class="px-4 py-2 bg-white border border-slate-200 hover:bg-slate-50 text-slate-600 rounded-lg text-sm font-medium transition-colors"
            >
              取消
            </button>
            <button 
              @click="confirmSendReviewEmail"
              :disabled="reviewEmailLoading || (!emailContentEnglish && !emailContentChinese)"
              class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ reviewEmailLoading ? '发送中...' : '确认发送' }}
            </button>
          </div>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useOrderStore } from '../../stores/orderStore'
import { ElMessage, ElDialog } from 'element-plus'
import axios from 'axios'

const router = useRouter()
const store = useOrderStore()

// API基础URL
const API_BASE_URL = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

// 筛选条件
const searchText = ref('')
const dateStart = ref('')
const dateEnd = ref('')
const shopFilter = ref('')
const productFilter = ref('')

// 分页
const currentPage = ref(1)
const pageSize = ref(20)

// 展开行
const expandedId = ref(null)

// 正在生成PDF的订单ID
const generatingOrderId = ref(null)

// ========== 追评邮件功能 ==========
// 邮件对话框
const showReviewEmailDialog = ref(false)
const selectedOrderForReview = ref(null)
const reviewEmailLoading = ref(false)
const reviewTemplatesLoading = ref(false)

// 邮件模板数据
const reviewTemplates = ref([])
const selectedTemplate = ref(null)

// 邮件风格控制
const emailTone = ref('casual') // formal(正式) / casual(随和) / lively(活泼)
const emailLength = ref('standard') // short(简短) / standard(标准) / detailed(详细)
const senderName = ref('Customer Support Team')

// 邮件内容
const emailContentEnglish = ref('')
const emailContentChinese = ref('')

// 风格选项定义
const toneOptions = [
  { value: 'formal', label: '正式', desc: '商务专业', icon: '👔' },
  { value: 'casual', label: '随和', desc: '自然友好', icon: '😊' },
  { value: 'lively', label: '活泼', desc: '轻松有趣', icon: '🎉' }
]

const lengthOptions = [
  { value: 'short', label: '简短', desc: '50字以内', icon: '📝' },
  { value: 'standard', label: '标准', desc: '100字左右', icon: '📄' },
  { value: 'detailed', label: '详细', desc: '200字以上', icon: '📚' }
]

// 预设落款人选项
const senderOptions = [
  'Customer Support Team',
  'Pet Tag Studio',
  'Sarah',
  'Emily'
]

// 页面加载时获取真实数据
onMounted(async () => {
  await store.getCompletedOrders()
  console.log('✅ 已完成订单页面加载，订单数:', store.orders.length)
})

// 刷新订单列表
const refreshOrders = async () => {
  await store.getCompletedOrders()
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

// 计算已交货天数
const calculateDeliveredDays = (order) => {
  const shippedAt = order.shipped_at || order.logistics?.shipped_at
  if (!shippedAt) return null

  const shippedDate = new Date(shippedAt)
  const today = new Date()

  // 重置时间为当天开始，只计算日期差
  shippedDate.setHours(0, 0, 0, 0)
  today.setHours(0, 0, 0, 0)

  const diffTime = today - shippedDate
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24))

  return diffDays >= 0 ? diffDays : null
}

// 格式化显示已交货天数
const formatDeliveredDays = (order) => {
  const days = calculateDeliveredDays(order)
  if (days === null) return '-'
  return `${days} 天`
}

// 总计数量 - 使用真实数据
const totalCount = computed(() => store.orders.length)

// 提取唯一的店铺列表（从订单的 operator 字段）
const shopOptions = computed(() => {
  const operators = new Set()
  store.orders.forEach(order => {
    if (order.operator) {
      operators.add(order.operator)
    }
  })
  return Array.from(operators).sort()
})

// 筛选后的订单 - 使用真实数据
const filteredOrders = computed(() => {
  let result = [...store.orders]
  
  // 搜索文本筛选
  if (searchText.value) {
    const search = searchText.value.toLowerCase()
    result = result.filter(o => 
      (o.etsy_order_id || o.id || '').toLowerCase().includes(search) || 
      (o.customer_name || '').toLowerCase().includes(search)
    )
  }
  
  // 日期范围筛选（基于 completed_at 或 created_at）
  if (dateStart.value || dateEnd.value) {
    result = result.filter(o => {
      const orderDate = new Date(o.completed_at || o.created_at)
      orderDate.setHours(0, 0, 0, 0)
      
      if (dateStart.value) {
        const startDate = new Date(dateStart.value)
        startDate.setHours(0, 0, 0, 0)
        if (orderDate < startDate) return false
      }
      
      if (dateEnd.value) {
        const endDate = new Date(dateEnd.value)
        endDate.setHours(23, 59, 59, 999)
        if (orderDate > endDate) return false
      }
      
      return true
    })
  }
  
  // 店铺筛选（基于 operator 字段）
  if (shopFilter.value) {
    result = result.filter(o => o.operator === shopFilter.value)
  }
  
  // 产品筛选
  if (productFilter.value) {
    result = result.filter(o => (o.sku_mapping?.sku_code || '').includes(productFilter.value))
  }
  
  return result
})

// 分页后的订单
const paginatedOrders = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredOrders.value.slice(start, end)
})

// 总页数
const totalPages = computed(() => Math.ceil(filteredOrders.value.length / pageSize.value) || 1)

// 获取行边框样式
const getRowBorderClass = (order) => {
  if (order.review_sent) {
    return 'border-l-4 border-green-400'
  }
  return ''
}

// 获取天数样式
const getDaysClass = (days) => {
  if (days >= 8) return 'text-orange-600 font-medium'
  return 'text-slate-600'
}

// 获取追评状态文字
const getReviewStatusText = (order) => {
  if (order.review_sent) return '已发送'
  return '未发送'
}

// 获取追评状态样式
const getReviewStatusClass = (order) => {
  if (order.review_sent) {
    return 'inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-700'
  }
  return 'inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-slate-100 text-slate-500'
}

// 展开/收起
const toggleExpand = (id) => {
  expandedId.value = expandedId.value === id ? null : id
}

// 搜索
const handleSearch = () => {
  currentPage.value = 1
}

// 重置
const handleReset = () => {
  searchText.value = ''
  dateStart.value = ''
  dateEnd.value = ''
  shopFilter.value = ''
  productFilter.value = ''
  currentPage.value = 1
}

// 生成PDF
const generatePdf = async (order) => {
  generatingOrderId.value = order.id
  try {
    const response = await axios.post(`${API_BASE_URL}/api/pdf/generate-and-upload`, {
      order_id: order.id
    })
    
    if (response.data.success) {
      alert('✅ 生产文档生成成功！')
      // 刷新订单列表
      await store.getCompletedOrders()
    } else {
      alert('❌ 生成失败: ' + (response.data.detail || '未知错误'))
    }
  } catch (err) {
    console.error('生成PDF出错:', err)
    alert('❌ 生成失败: ' + (err.response?.data?.detail || err.message || 'Network Error'))
  } finally {
    generatingOrderId.value = null
  }
}

// 查看PDF
const viewPdf = (order) => {
  if (order.production_pdf_url) {
    window.open(order.production_pdf_url, '_blank')
  } else {
    alert('PDF尚未生成，请先点击"生成"按钮')
  }
}

// 下载PDF
const downloadPdf = (order) => {
  if (order.production_pdf_url) {
    const link = document.createElement('a')
    link.href = order.production_pdf_url
    link.download = `POD_${order.etsy_order_id || order.id}.pdf`
    link.click()
  } else {
    alert('PDF尚未生成，请先点击"生成"按钮')
  }
}

// 打印PDF
const printPdf = (order) => {
  if (order.production_pdf_url) {
    const printWindow = window.open(order.production_pdf_url, '_blank')
    printWindow.onload = () => {
      printWindow.print()
    }
  } else {
    alert('PDF尚未生成，请先点击"生成"按钮')
  }
}

// 发送追评邮件 - 打开对话框并加载模板
const sendReviewEmail = async (order) => {
  selectedOrderForReview.value = order
  selectedTemplate.value = null
  emailContentEnglish.value = ''
  emailContentChinese.value = ''
  
  // 加载追评邮件模板
  await loadReviewTemplates()
  
  showReviewEmailDialog.value = true
}

// 加载追评邮件模板
const loadReviewTemplates = async () => {
  reviewTemplatesLoading.value = true
  try {
    const response = await axios.get(`${API_BASE_URL}/api/email-templates/follow_up`)
    if (response.data.success) {
      reviewTemplates.value = response.data.data || []
      // 默认选中第一个模板
      if (reviewTemplates.value.length > 0) {
        selectedTemplate.value = reviewTemplates.value[0]
        generateReviewEmail()
      }
    }
  } catch (err) {
    console.error('加载追评邮件模板失败:', err)
    ElMessage.warning('加载邮件模板失败，请检查后端服务')
  } finally {
    reviewTemplatesLoading.value = false
  }
}

// 生成追评邮件内容
const generateReviewEmail = () => {
  if (!selectedOrderForReview.value || !selectedTemplate.value) {
    return
  }
  
  const order = selectedOrderForReview.value
  const firstName = order.customer_name?.split(' ')[0] || 'there'
  const orderId = order.etsy_order_id || order.id
  
  // 获取模板内容
  const tone = emailTone.value
  const length = emailLength.value
  const templateContent = selectedTemplate.value.content?.[tone]?.[length]
  
  if (!templateContent) {
    ElMessage.warning('模板内容不存在，请检查模板配置')
    return
  }
  
  // 替换变量
  const replaceVars = (text) => {
    return text
      .replace(/{firstName}/g, firstName)
      .replace(/{orderId}/g, orderId)
      .replace(/{senderName}/g, senderName.value)
  }
  
  // 称呼映射
  const greetingMap = {
    dear: { en: `Dear ${firstName},`, zh: `${firstName}您好，` },
    hi: { en: `Hi ${firstName}!`, zh: `嗨 ${firstName}！` },
    hey: { en: `Hey ${firstName} 👋`, zh: `嘿 ${firstName}～` }
  }
  
  // 落款映射
  const signMap = {
    formal: { en: `Best regards,\n${senderName.value}`, zh: `此致\n${senderName.value}` },
    casual: { en: `Best,\n${senderName.value}`, zh: `祝好，\n${senderName.value}` },
    lively: { en: `Cheers! 🎉\n${senderName.value}`, zh: `加油！🎉\n${senderName.value}` }
  }
  
  const greeting = greetingMap['hi'] // 追评邮件默认用 hi
  const sign = signMap[tone]
  
  // 生成邮件内容
  emailContentEnglish.value = `${greeting.en}\n\n${replaceVars(templateContent.en)}\n\n${sign.en}`
  emailContentChinese.value = `${greeting.zh}\n\n${replaceVars(templateContent.zh)}\n\n${sign.zh}`
}

// 复制邮件内容到剪贴板
const copyReviewEmail = async () => {
  if (!emailContentChinese.value && !emailContentEnglish.value) {
    ElMessage.warning('请先生成邮件内容')
    return
  }
  
  try {
    const fullContent = `=== 中文版本 Chinese Version ===\n\n${emailContentChinese.value}\n\n=== English Version ===\n\n${emailContentEnglish.value}`
    await navigator.clipboard.writeText(fullContent)
    ElMessage.success('✅ 中英文邮件内容已复制到剪贴板！')
  } catch (e) {
    ElMessage.error('复制失败，请手动复制')
  }
}

// 确认发送追评邮件
const confirmSendReviewEmail = async () => {
  if (!selectedOrderForReview.value) {
    ElMessage.warning('订单信息丢失，请重新选择')
    return
  }
  
  if (!emailContentChinese.value && !emailContentEnglish.value) {
    ElMessage.warning('请先生成邮件内容')
    return
  }
  
  reviewEmailLoading.value = true
  
  try {
    const order = selectedOrderForReview.value
    const fullContent = `=== 中文版本 Chinese Version ===\n\n${emailContentChinese.value}\n\n=== English Version ===\n\n${emailContentEnglish.value}`
    
    // 1. 保存邮件记录到 email_logs 表
    await store.saveEmailLog({
      order_id: order.id,
      email_type: 'follow_up',
      subject: `【追评邮件】Thank you for your order - ${order.etsy_order_id || order.id}`,
      content: fullContent,
      sender_name: senderName.value
    })
    
    // 2. 调用后端API发送邮件（可选）
    try {
      const productInfo = `${order.sku_mapping?.product_name || 'Custom Product'} (${order.sku_mapping?.sku_code || 'N/A'})`
      
      await axios.post(`${API_BASE_URL}/api/email/send-confirmation`, {
        order_id: order.id,
        to_email: order.customer_email || '',
        customer_name: order.customer_name || '',
        product_info: productInfo,
        effect_image_path: ''
      })
      
      ElMessage.success('✅ 追评邮件已发送至客户邮箱')
    } catch (sendError) {
      // 发送失败不阻断，提示用户手动发送
      ElMessage.warning(`自动发送邮件失败: ${sendError.message}，请使用「复制内容」手动发送`)
    }
    
    // 3. 更新订单的追评状态
    await store.updateEmailSentStatus(order.id, true)
    
    // 更新本地订单状态
    const orderIndex = store.orders.findIndex(o => o.id === order.id)
    if (orderIndex !== -1) {
      store.orders[orderIndex].review_sent = true
    }
    
    // 4. 关闭对话框
    showReviewEmailDialog.value = false
    selectedOrderForReview.value = null
    
  } catch (err) {
    console.error('发送追评邮件失败:', err)
    ElMessage.error('发送失败: ' + err.message)
  } finally {
    reviewEmailLoading.value = false
  }
}
</script>

<style scoped>
/* 追评建议状态闪烁动画 */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.6;
  }
}
.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>
