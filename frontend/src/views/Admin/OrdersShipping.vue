<template>
  <div class="h-full overflow-auto bg-slate-50 p-4">
    <!-- 页面标题 -->
    <div class="mb-4 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-slate-800">物流下单</h1>
        <p class="text-sm text-slate-500 mt-1">选择订单并创建物流运单</p>
      </div>
      <div class="flex items-center gap-4 text-sm">
        <span class="bg-amber-100 text-amber-700 px-3 py-1 rounded-full font-medium">待下单: {{ pendingCount }}</span>
        <span class="bg-green-100 text-green-700 px-3 py-1 rounded-full font-medium">今日已下: {{ todayShippedCount }}</span>
        <span v-if="demoMode" class="bg-red-100 text-red-600 px-3 py-1 rounded-full font-medium text-xs">演示模式</span>
      </div>
    </div>

    <!-- 物流公司Tab页 -->
    <div class="flex border-b border-slate-200 mb-4">
      <button 
        @click="activeTab = '4px'" 
        :class="['px-6 py-3 text-sm font-medium transition-colors', activeTab === '4px' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-slate-500 hover:text-slate-700']"
      >
        4PX全球直发
      </button>
      <button 
        @click="activeTab = 'yanwen'" 
        :class="['px-6 py-3 text-sm font-medium transition-colors', activeTab === 'yanwen' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-slate-500 hover:text-slate-700']"
      >
        燕文物流
      </button>
      <button 
        @click="activeTab = 'yuntu'" 
        :class="['px-6 py-3 text-sm font-medium transition-colors', activeTab === 'yuntu' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-slate-500 hover:text-slate-700']"
      >
        云途物流
      </button>
    </div>

    <!-- 4PX Tab内容 -->
    <div v-if="activeTab === '4px'" class="flex gap-4">
      <!-- 左侧：待下单订单列表 -->
      <div class="w-[40%] shrink-0">
        <div class="bg-gray-50 rounded-xl border border-slate-200 overflow-hidden">
          <div class="px-4 py-3 border-b border-slate-200 bg-white">
            <div class="flex items-center justify-between mb-3">
              <h2 class="text-base font-bold text-slate-800">待下单订单</h2>
              <div class="flex items-center gap-2">
                <span v-if="loading" class="text-xs text-slate-400">
                  <svg class="animate-spin h-4 w-4 inline mr-1" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  加载中...
                </span>
                <span class="bg-blue-100 text-blue-600 px-2 py-0.5 rounded-full text-xs font-bold">{{ orders.length }}条</span>
              </div>
            </div>
            <input 
              v-model="searchKeyword" 
              type="text" 
              placeholder="搜索订单号/客户名" 
              class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
            />
          </div>

          <div class="overflow-x-auto" style="max-height: 600px;">
            <table class="w-full text-xs text-left">
              <thead class="bg-slate-100 text-slate-500 font-medium border-b border-slate-200 sticky top-0 z-10">
                <tr class="h-[36px]">
                  <th class="px-3 whitespace-nowrap font-medium">订单号</th>
                  <th class="px-3 whitespace-nowrap font-medium">客户</th>
                  <th class="px-3 whitespace-nowrap font-medium">SKU</th>
                  <th class="px-3 whitespace-nowrap font-medium">国家</th>
                  <th class="px-3 whitespace-nowrap font-medium">操作</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100 bg-white">
                <tr 
                  v-for="order in filteredOrders" 
                  :key="order.id" 
                  :class="['hover:bg-slate-50 transition-colors h-[44px]', selectedOrder?.id === order.id ? 'bg-blue-50' : '']"
                >
                  <td class="px-3 whitespace-nowrap font-medium text-slate-700">{{ order.etsy_order_id || order.id }}</td>
                  <td class="px-3 whitespace-nowrap text-slate-600">{{ order.customer_name }}</td>
                  <td class="px-3 whitespace-nowrap font-mono text-slate-500">{{ order.sku_mapping?.sku_code || order.sku_id || '-' }}</td>
                  <td class="px-3 whitespace-nowrap text-slate-600">{{ order.country || '-' }}</td>
                  <td class="px-3 whitespace-nowrap">
                    <button 
                      @click="selectOrder(order)" 
                      class="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-[10px] transition-colors"
                    >
                      选择
                    </button>
                  </td>
                </tr>
                <tr v-if="filteredOrders.length === 0" class="h-[60px]">
                  <td colspan="5" class="px-3 text-center text-slate-400 text-sm">暂无待下单订单</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- 右侧：物流下单表单 -->
      <div class="flex-1">
        <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
          <div class="px-4 py-3 border-b border-slate-100 bg-slate-50">
            <h2 class="text-base font-bold text-slate-800">物流下单表单</h2>
          </div>

          <!-- 未选择订单时的引导 -->
          <div v-if="!selectedOrder" class="p-8 text-center">
            <div class="text-slate-400 text-lg">← 请从左侧选择一个订单</div>
            <p class="text-slate-300 text-sm mt-2">选择订单后可填写物流信息并创建运单</p>
          </div>

          <!-- 选中订单后显示表单 -->
          <div v-else class="p-4 space-y-4">
            <!-- Section A: 订单信息（只读灰色背景） -->
            <div class="bg-slate-50 rounded-lg p-4">
              <h3 class="text-sm font-bold text-slate-700 mb-3 flex items-center gap-2">
                <span>📦</span> 订单信息
              </h3>
              <div class="grid grid-cols-2 gap-3 text-xs">
                <div class="flex justify-between">
                  <span class="text-slate-400">订单号:</span>
                  <span class="text-slate-700 font-medium">{{ selectedOrder.etsy_order_id || selectedOrder.id }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-slate-400">客户:</span>
                  <span class="text-slate-700">{{ selectedOrder.customer_name }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-slate-400">SKU:</span>
                  <span class="text-slate-700 font-mono">{{ selectedOrder.sku_mapping?.sku_code || selectedOrder.sku_id || '-' }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-slate-400">产品:</span>
                  <span class="text-slate-700">{{ getProductDescription(selectedOrder) }}</span>
                </div>
              </div>
            </div>

            <!-- Section B: 收件人信息（可编辑） -->
            <div class="border border-slate-200 rounded-lg p-4">
              <h3 class="text-sm font-bold text-slate-700 mb-3 flex items-center gap-2">
                <span>📮</span> 收件人信息
              </h3>
              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="block text-xs text-slate-500 mb-1">姓名 <span class="text-red-400">*</span></label>
                  <input v-model="form.recipient_name" type="text" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500" />
                </div>
                <div>
                  <label class="block text-xs text-slate-500 mb-1">电话</label>
                  <input v-model="form.recipient_phone" type="text" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500" />
                </div>
                <div>
                  <label class="block text-xs text-slate-500 mb-1">邮箱</label>
                  <input v-model="form.recipient_email" type="email" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500" />
                </div>
                <div>
                  <label class="block text-xs text-slate-500 mb-1">国家 <span class="text-red-400">*</span></label>
                  <select v-model="form.recipient_country" @change="onCountryChange" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500">
                    <option value="">请选择</option>
                    <option value="US">美国 (US)</option>
                    <option value="CA">加拿大 (CA)</option>
                    <option value="GB">英国 (GB)</option>
                    <option value="AU">澳大利亚 (AU)</option>
                    <option value="DE">德国 (DE)</option>
                    <option value="FR">法国 (FR)</option>
                    <option value="JP">日本 (JP)</option>
                    <option value="KR">韩国 (KR)</option>
                    <option value="SG">新加坡 (SG)</option>
                    <option value="NZ">新西兰 (NZ)</option>
                  </select>
                </div>
                <div class="col-span-2">
                  <label class="block text-xs text-slate-500 mb-1">详细地址 <span class="text-red-400">*</span></label>
                  <input v-model="form.recipient_street" type="text" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500" />
                </div>
                <div>
                  <label class="block text-xs text-slate-500 mb-1">城市 <span class="text-red-400">*</span></label>
                  <input v-model="form.recipient_city" type="text" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500" />
                </div>
                <div>
                  <label class="block text-xs text-slate-500 mb-1">州/省</label>
                  <input v-model="form.recipient_state" type="text" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500" />
                </div>
                <div>
                  <label class="block text-xs text-slate-500 mb-1">邮编 <span class="text-red-400">*</span></label>
                  <input v-model="form.recipient_postcode" type="text" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500" />
                </div>
              </div>
            </div>

            <!-- Section C: 物流渠道 -->
            <div class="border border-slate-200 rounded-lg p-4">
              <h3 class="text-sm font-bold text-slate-700 mb-3 flex items-center gap-2">
                <span>🚚</span> 物流渠道
                <span v-if="loadingChannels" class="text-xs text-slate-400 font-normal">
                  <svg class="animate-spin h-3 w-3 inline mr-1" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  查询中...
                </span>
              </h3>
              <select v-model="form.channel_code" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500">
                <option v-for="channel in channels" :key="channel.code" :value="channel.code">
                  {{ channel.code }} - {{ channel.name }}
                </option>
              </select>
            </div>

            <!-- 高级选项折叠按钮 -->
            <button 
              @click="showAdvanced = !showAdvanced" 
              class="w-full flex items-center justify-center gap-2 py-2 text-sm text-slate-500 hover:text-slate-700 transition-colors"
            >
              <span>{{ showAdvanced ? '收起高级选项' : '展开高级选项' }}</span>
              <svg :class="['w-4 h-4 transition-transform', showAdvanced ? 'rotate-180' : '']" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="6 9 12 15 18 9"></polyline>
              </svg>
            </button>

            <!-- 高级选项区域（折叠） -->
            <div v-show="showAdvanced" class="space-y-4 transition-all">
              <!-- Section D: 包裹信息 -->
              <div class="border border-slate-200 rounded-lg p-4">
                <h3 class="text-sm font-bold text-slate-700 mb-3 flex items-center gap-2">
                  <span>📐</span> 包裹信息
                </h3>
                <div class="grid grid-cols-4 gap-3">
                  <div>
                    <label class="block text-xs text-slate-500 mb-1">重量(g)</label>
                    <input v-model.number="form.weight" type="number" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500" />
                  </div>
                  <div>
                    <label class="block text-xs text-slate-500 mb-1">长(cm)</label>
                    <input v-model.number="form.length" type="number" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500" />
                  </div>
                  <div>
                    <label class="block text-xs text-slate-500 mb-1">宽(cm)</label>
                    <input v-model.number="form.width" type="number" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500" />
                  </div>
                  <div>
                    <label class="block text-xs text-slate-500 mb-1">高(cm)</label>
                    <input v-model.number="form.height" type="number" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500" />
                  </div>
                </div>
                <div class="grid grid-cols-2 gap-3 mt-3">
                  <div>
                    <label class="block text-xs text-slate-500 mb-1">申报品名(中)</label>
                    <input v-model="form.declare_name_cn" type="text" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500" />
                  </div>
                  <div>
                    <label class="block text-xs text-slate-500 mb-1">申报品名(英)</label>
                    <input v-model="form.declare_name_en" type="text" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500" />
                  </div>
                  <div>
                    <label class="block text-xs text-slate-500 mb-1">申报价值(USD)</label>
                    <input v-model.number="form.declare_value" type="number" step="0.01" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500" />
                  </div>
                  <div>
                    <label class="block text-xs text-slate-500 mb-1">是否带电</label>
                    <div class="flex gap-4 mt-2">
                      <label class="flex items-center gap-1 text-sm text-slate-600">
                        <input type="radio" v-model="form.has_battery" :value="false" class="text-blue-600" /> 否
                      </label>
                      <label class="flex items-center gap-1 text-sm text-slate-600">
                        <input type="radio" v-model="form.has_battery" :value="true" class="text-blue-600" /> 是
                      </label>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Section E: 发件人信息（只读灰底） -->
              <div class="bg-slate-50 rounded-lg p-4">
                <h3 class="text-sm font-bold text-slate-700 mb-3 flex items-center gap-2">
                  <span>📋</span> 发件人信息
                </h3>
                <div class="grid grid-cols-2 gap-3 text-xs">
                  <div class="flex justify-between">
                    <span class="text-slate-400">公司:</span>
                    <span class="text-slate-700">PetTag Studio</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-slate-400">城市:</span>
                    <span class="text-slate-700">深圳市</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-slate-400">省份:</span>
                    <span class="text-slate-700">广东省</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-slate-400">国家:</span>
                    <span class="text-slate-700">中国</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- 操作按钮 -->
            <div class="flex gap-3 mt-6">
              <button 
                @click="createOrder" 
                :disabled="submitting" 
                class="flex-1 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white py-2.5 rounded-lg font-medium text-sm flex items-center justify-center gap-2 transition-colors"
              >
                <svg v-if="submitting" class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M5 18H3c-.6 0-1-.4-1-1V7c0-.6.4-1 1-1h10c.6 0 1 .4 1 1v11"/>
                  <path d="M14 9h4l4 4v6h-4"/>
                  <circle cx="7" cy="18" r="2"/>
                  <circle cx="17" cy="18" r="2"/>
                </svg>
                {{ submitting ? '正在创建...' : '创建物流订单' }}
              </button>
              <button 
                disabled 
                title="功能开发中" 
                class="px-6 bg-slate-200 text-slate-400 py-2.5 rounded-lg font-medium text-sm cursor-not-allowed"
              >
                批量下单
              </button>
            </div>

            <!-- 下单结果区（成功后显示） -->
            <div v-if="showResult && orderResult" class="bg-green-50 border border-green-200 rounded-lg p-4">
              <h3 class="text-sm font-bold text-green-700 mb-3 flex items-center gap-2">
                <span>✅</span> 物流订单创建成功！
              </h3>
              <div class="text-sm text-green-600 mb-3">
                物流单号: <span class="font-mono font-bold">{{ orderResult.tracking_number || orderResult.fpx_tracking_no }}</span>
              </div>
              <div class="flex gap-2">
                <button @click="downloadLabel" class="flex-1 bg-white border border-green-300 text-green-700 hover:bg-green-100 py-2 rounded-lg text-sm font-medium flex items-center justify-center gap-2 transition-colors">
                  <span>📄</span> 下载面单PDF
                </button>
                <button @click="printLabel" class="flex-1 bg-white border border-green-300 text-green-700 hover:bg-green-100 py-2 rounded-lg text-sm font-medium flex items-center justify-center gap-2 transition-colors">
                  <span>🖨️</span> 打印面单
                </button>
                <button @click="continueOrder" class="flex-1 bg-white border border-green-300 text-green-700 hover:bg-green-100 py-2 rounded-lg text-sm font-medium flex items-center justify-center gap-2 transition-colors">
                  <span>←</span> 继续下单
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 燕文物流Tab内容 -->
    <div v-else-if="activeTab === 'yanwen'" class="flex items-center justify-center h-[400px]">
      <div class="text-center text-slate-400">
        <div class="text-6xl mb-4">🚧</div>
        <div class="text-xl font-medium">即将接入，敬请期待</div>
        <p class="text-sm mt-2">燕文物流API正在对接中...</p>
      </div>
    </div>

    <!-- 云途物流Tab内容 -->
    <div v-else-if="activeTab === 'yuntu'" class="flex items-center justify-center h-[400px]">
      <div class="text-center text-slate-400">
        <div class="text-6xl mb-4">🚧</div>
        <div class="text-xl font-medium">即将接入，敬请期待</div>
        <p class="text-sm mt-2">云途物流API正在对接中...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, reactive } from 'vue'
import supabase from '../../utils/supabase'

// API配置
const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

// 状态
const activeTab = ref('4px')
const loading = ref(false)
const demoMode = ref(false)
const orders = ref([])
const selectedOrder = ref(null)
const searchKeyword = ref('')
const showAdvanced = ref(false)
const channels = ref([
  { code: 'PX', name: '4PX标准直发 (7-15天)' },
  { code: 'PY', name: '4PX快速直发 (3-7天)' }
])
const loadingChannels = ref(false)
const submitting = ref(false)
const showResult = ref(false)
const orderResult = ref(null)
const todayShippedCount = ref(0)

// 假数据（回退用）
const mockOrders = [
  { id: 'demo-001', etsy_order_id: '4002217518', customer_name: 'Luna Parker', sku_id: 'B-HC-G-L', country: 'AU', total_amount: 29.99 },
  { id: 'demo-002', etsy_order_id: '4002217519', customer_name: 'Mike Johnson', sku_id: 'B-BO-S-S', country: 'US', total_amount: 19.99 },
  { id: 'demo-003', etsy_order_id: '4002217520', customer_name: 'Emma Wilson', sku_id: 'B-CI-G-L', country: 'GB', total_amount: 24.99 },
]

// 表单数据
const form = reactive({
  recipient_name: '',
  recipient_phone: '',
  recipient_email: '',
  recipient_street: '',
  recipient_city: '',
  recipient_state: '',
  recipient_postcode: '',
  recipient_country: '',
  channel_code: 'PX',
  weight: 30,
  length: 10,
  width: 8,
  height: 1,
  declare_name_cn: '不锈钢宠物牌',
  declare_name_en: 'Stainless Steel Pet ID Tag',
  declare_value: 9.99,
  has_battery: false
})

// 计算属性
const pendingCount = computed(() => orders.value.length)

const filteredOrders = computed(() => {
  if (!searchKeyword.value) return orders.value
  const keyword = searchKeyword.value.toLowerCase()
  return orders.value.filter(order => 
    (order.etsy_order_id || order.id || '').toLowerCase().includes(keyword) || 
    (order.customer_name || '').toLowerCase().includes(keyword)
  )
})

// 生成随机电话号码（隐私保护）
const generateFakePhone = () => {
  const prefix = ['138', '139', '158', '159', '188', '189']
  const p = prefix[Math.floor(Math.random() * prefix.length)]
  const suffix = Math.floor(Math.random() * 100000000).toString().padStart(8, '0')
  return p + suffix
}

// 获取产品描述
const getProductDescription = (order) => {
  if (order.sku_mapping) {
    const shape = order.sku_mapping.shape || ''
    const color = order.sku_mapping.color || ''
    const size = order.sku_mapping.size || ''
    return [shape, color, size].filter(Boolean).join('/') || '不锈钢宠物牌'
  }
  return '不锈钢宠物牌'
}

// 加载订单列表
const loadOrders = async () => {
  loading.value = true
  demoMode.value = false
  
  try {
    const { data, error } = await supabase
      .from('orders')
      .select('*, sku_mapping(*)')
      .eq('status', 'confirmed')
      .order('created_at', { ascending: false })
    
    if (error) throw error
    
    if (data && data.length > 0) {
      orders.value = data
      console.log('✅ 物流下单订单加载成功:', data.length, '条')
    } else {
      // 无数据时使用假数据
      orders.value = mockOrders
      demoMode.value = true
      console.log('⚠️ 无确认订单，使用演示数据')
    }
  } catch (e) {
    console.error('❌ 订单加载失败:', e)
    // 回退到假数据
    orders.value = mockOrders
    demoMode.value = true
  } finally {
    loading.value = false
  }
}

// 加载物流信息
const loadLogistics = async (orderId) => {
  try {
    const { data, error } = await supabase
      .from('logistics')
      .select('*')
      .eq('order_id', orderId)
      .single()
    
    if (error && error.code !== 'PGRST116') throw error
    
    if (data) {
      form.recipient_name = data.recipient_name || ''
      form.recipient_phone = data.phone || generateFakePhone()
      form.recipient_email = data.email || ''
      form.recipient_street = data.street_address || ''
      form.recipient_city = data.city || ''
      form.recipient_state = data.state_code || ''
      form.recipient_postcode = data.postal_code || ''
      form.recipient_country = data.country || ''
    }
  } catch (e) {
    console.error('❌ 物流信息加载失败:', e)
  }
}

// 加载可用渠道
const loadChannels = async (countryCode) => {
  if (!countryCode) return
  
  loadingChannels.value = true
  try {
    const res = await fetch(`${API_BASE}/api/shipping/get-products`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ country_code: countryCode })
    })
    const data = await res.json()
    
    if (data.success && data.data?.products?.length > 0) {
      channels.value = data.data.products.slice(0, 5).map(p => ({
        code: p.logistics_product_code || p.code,
        name: p.logistics_product_name || p.name || p.logistics_product_code
      }))
      form.channel_code = channels.value[0]?.code || 'PX'
    }
  } catch (e) {
    console.error('❌ 渠道查询失败，使用默认:', e)
    // 使用默认渠道
    channels.value = [
      { code: 'PX', name: '4PX标准直发 (7-15天)' },
      { code: 'PY', name: '4PX快速直发 (3-7天)' }
    ]
  } finally {
    loadingChannels.value = false
  }
}

// 选择订单
const selectOrder = async (order) => {
  selectedOrder.value = order
  showResult.value = false
  orderResult.value = null
  
  // 重置表单
  form.recipient_name = order.customer_name || ''
  form.recipient_phone = generateFakePhone()
  form.recipient_email = ''
  form.recipient_street = ''
  form.recipient_city = ''
  form.recipient_state = ''
  form.recipient_postcode = ''
  form.recipient_country = order.country || ''
  form.declare_value = order.total_amount || 9.99
  
  // 尝试加载物流表数据
  if (order.id && !demoMode.value) {
    await loadLogistics(order.id)
  }
  
  // 根据国家加载渠道
  if (form.recipient_country) {
    await loadChannels(form.recipient_country)
  }
}

// 国家变化时重新加载渠道
const onCountryChange = () => {
  if (form.recipient_country) {
    loadChannels(form.recipient_country)
  }
}

// 创建物流订单
const createOrder = async () => {
  // 表单验证
  if (!form.recipient_name || !form.recipient_street || !form.recipient_city || !form.recipient_postcode || !form.recipient_country) {
    alert('请填写必填项：姓名、地址、城市、邮编、国家')
    return
  }
  
  submitting.value = true
  
  try {
    const res = await fetch(`${API_BASE}/api/shipping/create-order`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        order_id: selectedOrder.value.id,
        logistics_product_code: form.channel_code,
        recipient_name: form.recipient_name,
        recipient_phone: form.recipient_phone,
        recipient_email: form.recipient_email,
        recipient_street: form.recipient_street,
        recipient_city: form.recipient_city,
        recipient_state: form.recipient_state,
        recipient_postcode: form.recipient_postcode,
        recipient_country: form.recipient_country,
        weight_kg: form.weight / 1000,
        declare_value: form.declare_value,
        declare_currency: 'USD'
      })
    })
    
    const data = await res.json()
    
    if (data.success) {
      orderResult.value = data.data
      showResult.value = true
      todayShippedCount.value++
      
      // 从列表中移除已下单的订单
      orders.value = orders.value.filter(o => o.id !== selectedOrder.value.id)
      
      console.log('✅ 物流订单创建成功:', data.data)
    } else {
      alert('下单失败：' + (data.message || data.detail || '未知错误'))
    }
  } catch (e) {
    console.error('❌ 创建订单失败:', e)
    alert('网络错误：' + e.message)
  } finally {
    submitting.value = false
  }
}

// 下载面单
const downloadLabel = () => {
  if (orderResult.value?.label_url) {
    window.open(orderResult.value.label_url, '_blank')
  } else {
    alert('面单PDF尚未生成，请稍后重试')
  }
}

// 打印面单
const printLabel = () => {
  if (orderResult.value?.label_url) {
    const printWindow = window.open(orderResult.value.label_url, '_blank')
    if (printWindow) {
      printWindow.onload = () => printWindow.print()
    }
  } else {
    alert('面单PDF尚未生成，请稍后重试')
  }
}

// 继续下单
const continueOrder = () => {
  selectedOrder.value = null
  showResult.value = false
  orderResult.value = null
}

// 初始化
onMounted(() => {
  loadOrders()
})
</script>
