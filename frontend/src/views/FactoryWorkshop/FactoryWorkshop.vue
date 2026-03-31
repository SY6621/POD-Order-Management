<template>
  <div class="bg-slate-50 min-h-screen">
    <!-- 密码验证层 -->
    <div v-if="!isAuthenticated" class="fixed inset-0 bg-slate-900 z-50 flex items-center justify-center">
      <div class="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-md mx-4">
        <div class="text-center mb-6">
          <div class="w-16 h-16 bg-blue-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
              <path d="M21 10V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l2-1.14"/>
              <path d="m7.5 4.27 9 5.15"/>
              <polyline points="3.29 7 12 12 20.71 7"/>
              <line x1="12" x2="12" y1="22" y2="12"/>
            </svg>
          </div>
          <h2 class="text-2xl font-bold text-slate-800">工厂生产协作平台</h2>
          <p class="text-slate-500 mt-1">请输入访问密码</p>
        </div>
        
        <form @submit.prevent="handleLogin">
          <div class="mb-4">
            <input 
              v-model="factoryCode"
              type="text"
              placeholder="工厂代码"
              class="w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition-all text-center text-lg mb-3"
              :class="{ 'border-red-500': loginError }"
            >
            <input 
              v-model="password"
              type="password"
              placeholder="输入密码"
              class="w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition-all text-center text-lg tracking-widest"
              :class="{ 'border-red-500': loginError }"
            >
            <p v-if="loginError" class="text-red-500 text-sm mt-2 text-center">{{ loginError }}</p>
          </div>
          
          <button 
            type="submit"
            :disabled="!factoryCode || !password || loginLoading"
            class="w-full py-3 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          >
            {{ loginLoading ? '验证中...' : '进入系统' }}
          </button>
        </form>
        
        <p class="text-xs text-slate-400 text-center mt-4">
          忘记密码请联系系统管理员
        </p>
      </div>
    </div>

    <!-- 顶部导航 -->
    <header class="bg-slate-900 text-white px-6 py-4">
      <div class="max-w-7xl mx-auto flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 10V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l2-1.14"/>
              <path d="m7.5 4.27 9 5.15"/>
              <polyline points="3.29 7 12 12 20.71 7"/>
              <line x1="12" x2="12" y1="22" y2="12"/>
            </svg>
          </div>
          <div>
            <h1 class="text-xl font-bold">工厂生产协作平台</h1>
            <p class="text-sm text-slate-400">{{ currentDate }}</p>
          </div>
        </div>
        <div class="flex items-center gap-4">
          <span v-if="currentFactory" class="text-sm text-slate-400">
            工厂: {{ currentFactory.name }}
          </span>
          <button 
            @click="logout"
            class="text-sm text-slate-400 hover:text-white transition-colors"
          >
            退出登录
          </button>
        </div>
      </div>
    </header>

    <main class="max-w-7xl mx-auto p-6">
      <!-- Tab 切换 -->
      <div class="flex gap-2 mb-6">
        <button 
          @click="switchTab('production')" 
          :class="activeTab === 'production' ? 'tab-active' : 'tab-inactive'"
          class="px-6 py-3 rounded-xl font-semibold transition-all flex items-center gap-2"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
          </svg>
          生产文档
          <span class="ml-1 px-2 py-0.5 bg-white/20 rounded-full text-sm">{{ productionOrders.length }}</span>
        </button>
        <button 
          @click="switchTab('pickup')" 
          :class="activeTab === 'pickup' ? 'tab-active' : 'tab-inactive'"
          class="px-6 py-3 rounded-xl font-semibold transition-all flex items-center gap-2"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 10V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l2-1.14"/>
            <path d="m7.5 4.27 9 5.15"/>
            <polyline points="3.29 7 12 12 20.71 7"/>
            <line x1="12" x2="12" y1="22" y2="12"/>
            <circle cx="18.5" cy="15.5" r="2.5"/>
            <path d="M20.27 17.27 22 19"/>
          </svg>
          揽件确认
          <span class="ml-1 px-2 py-0.5 bg-slate-200 rounded-full text-sm">{{ pickupOrders.length }}</span>
        </button>
        <button 
          @click="switchTab('completed')" 
          :class="activeTab === 'completed' ? 'tab-active' : 'tab-inactive'"
          class="px-6 py-3 rounded-xl font-semibold transition-all flex items-center gap-2"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
            <polyline points="9 11 12 14 22 4"/>
          </svg>
          已完成
          <span class="ml-1 px-2 py-0.5 bg-slate-200 rounded-full text-sm">{{ completedOrders.length }}</span>
        </button>
      </div>

      <!-- Tab 1: 生产文档 -->
      <div v-if="activeTab === 'production'" class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <div class="bg-slate-50 px-6 py-4 border-b border-slate-200 flex items-center justify-between">
          <h2 class="text-lg font-bold text-slate-800">今日生产任务</h2>
          <div class="flex items-center gap-2">
            <label class="text-sm text-slate-600">日期:</label>
            <input 
              v-model="selectedDate" 
              type="date" 
              class="px-3 py-1.5 border border-slate-300 rounded-lg text-sm"
            >
            <button 
              @click="selectedDate = today" 
              class="px-3 py-1.5 bg-blue-100 text-blue-600 rounded-lg text-sm font-medium"
            >
              今天
            </button>
            <button 
              @click="setYesterday" 
              class="px-3 py-1.5 bg-slate-100 text-slate-600 rounded-lg text-sm"
            >
              昨天
            </button>
          </div>
        </div>
        
        <div class="p-6">
          <table class="w-full">
            <thead>
              <tr class="border-b border-slate-200">
                <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">订单号</th>
                <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">产品信息</th>
                <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">定制内容</th>
                <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">生产文档</th>
                <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">操作</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              <tr v-for="order in productionOrders" :key="order.id" class="hover:bg-slate-50">
                <td class="py-4 px-4">
                  <p class="font-mono font-semibold text-slate-800">{{ order.etsy_order_id }}</p>
                  <p class="text-xs text-slate-400">{{ formatTime(order.created_at) }} 创建</p>
                </td>
                <td class="py-4 px-4">
                  <div class="flex items-center gap-2">
                    <span class="w-3 h-3 rounded-full" :class="getColorClass(order.product_color)"></span>
                    <span class="text-sm">{{ order.product_shape }} - {{ order.product_color }} - {{ order.product_size }}</span>
                  </div>
                  <p class="text-xs text-slate-500 mt-1">{{ order.product_craft }}工艺</p>
                </td>
                <td class="py-4 px-4">
                  <p class="text-sm"><span class="text-slate-500">正面:</span> <span class="font-medium">{{ order.front_text }}</span></p>
                  <p class="text-sm"><span class="text-slate-500">字体:</span> <span class="font-medium">{{ order.font_code }}</span></p>
                  <p class="text-sm"><span class="text-slate-500">背面:</span> <span class="font-medium">{{ order.back_text }}</span></p>
                </td>
                <td class="py-4 px-4">
                  <div class="flex flex-col gap-2">
                    <!-- PDF 下载 -->
                    <button 
                      @click="downloadPdf(order)"
                      class="px-3 py-1.5 bg-blue-50 text-blue-600 text-sm rounded-lg hover:bg-blue-100 flex items-center gap-1"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                        <polyline points="14 2 14 8 20 8"/>
                      </svg>
                      PDF
                    </button>
                    <!-- SVG 下载（生产文件） -->
                    <button 
                      @click="downloadSvg(order)"
                      class="px-3 py-1.5 bg-green-50 text-green-600 text-sm rounded-lg hover:bg-green-100 flex items-center gap-1"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                        <polyline points="14 2 14 8 20 8"/>
                        <path d="M12 12v6"/>
                        <path d="M9 15l3 3 3-3"/>
                      </svg>
                      SVG
                    </button>
                    <!-- 打印 -->
                    <button 
                      @click="printDocument(order)"
                      class="px-3 py-1.5 bg-slate-50 text-slate-600 text-sm rounded-lg hover:bg-slate-100 flex items-center gap-1"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="6 9 6 2 18 2 18 9"/>
                        <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/>
                        <rect x="6" y="14" width="12" height="8"/>
                      </svg>
                      打印
                    </button>
                  </div>
                </td>
                <td class="py-4 px-4">
                  <div class="flex gap-2">
                    <button 
                      @click="startProduction(order)"
                      class="px-4 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700"
                    >
                      开始生产
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Tab 2: 揽件确认 -->
      <div v-if="activeTab === 'pickup'" class="space-y-6">
        <!-- 待发货订单列表 -->
        <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
          <div class="bg-slate-50 px-6 py-4 border-b border-slate-200">
            <h2 class="text-lg font-bold text-slate-800">待发货订单（点击选择）</h2>
          </div>
          <div class="p-6">
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div 
                v-for="order in pickupOrders" 
                :key="order.id"
                @click="selectOrder(order)"
                :class="selectedOrder?.id === order.id ? 'order-selected border-blue-500 bg-blue-50' : 'border-slate-200 hover:border-blue-300'"
                class="border-2 rounded-xl p-4 cursor-pointer transition-all hover:shadow-md"
              >
                <div class="flex items-center justify-between mb-3">
                  <span class="font-mono font-semibold text-slate-800">{{ order.etsy_order_id }}</span>
                  <span class="px-2 py-1 bg-orange-100 text-orange-700 text-xs rounded-full">
                    {{ order.verifyStatus === 'verified' ? '已校验' : '待校验' }}
                  </span>
                </div>
                <div class="flex items-center gap-2 mb-2">
                  <span class="w-3 h-3 rounded-full" :class="getColorClass(order.product_color)"></span>
                  <span class="text-sm">{{ order.product_shape }} - {{ order.product_color }} - {{ order.product_size }}</span>
                </div>
                <p class="text-sm text-slate-600">正面: <span class="font-medium">{{ order.front_text }}</span></p>
                <p class="text-sm text-slate-600">背面: <span class="font-medium">{{ order.back_text }}</span></p>
              </div>
            </div>
          </div>
        </div>

        <!-- 生产文档校验区 -->
        <div v-if="selectedOrder" class="bg-white rounded-xl shadow-sm border-2 border-blue-200 overflow-hidden">
          <div class="bg-blue-50 px-6 py-4 border-b border-blue-200 flex items-center justify-between">
            <h2 class="text-lg font-bold text-slate-800">生产文档校验</h2>
            <span class="text-sm text-slate-500">订单 #{{ selectedOrder.etsy_order_id }}</span>
          </div>
          
          <div class="p-6">
            <div class="grid grid-cols-12 gap-6">
              <!-- 左侧：图片对比 -->
              <div class="col-span-12 lg:col-span-8">
                <div class="grid grid-cols-2 gap-4 mb-4">
                  <!-- 实拍图 -->
                  <div class="bg-slate-50 rounded-xl border-2 border-slate-200 p-4">
                    <div class="flex items-center gap-2 mb-3">
                      <span class="w-2 h-2 bg-blue-500 rounded-full"></span>
                      <h3 class="font-semibold text-slate-700">产品实拍图</h3>
                      <span class="text-xs text-slate-400">工厂拍摄</span>
                    </div>
                    <div class="aspect-square bg-white rounded-lg border border-slate-200 flex items-center justify-center overflow-hidden">
                      <div v-if="!selectedOrder.productPhoto" class="text-center text-slate-400">
                        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="mx-auto mb-2">
                          <rect width="18" height="18" x="3" y="3" rx="2"/>
                          <circle cx="9" cy="9" r="2"/>
                          <path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>
                        </svg>
                        <p class="text-sm">请上传实拍图</p>
                        <button class="mt-2 px-3 py-1.5 bg-blue-50 text-blue-600 text-xs rounded-lg">点击上传</button>
                      </div>
                      <img v-else :src="selectedOrder.productPhoto" class="w-full h-full object-cover" alt="实拍图">
                    </div>
                    <p class="text-xs text-slate-500 mt-2 text-center">核对产品形状、颜色、刻字</p>
                  </div>

                  <!-- 效果图 -->
                  <div class="bg-slate-50 rounded-xl border-2 border-slate-200 p-4">
                    <div class="flex items-center gap-2 mb-3">
                      <span class="w-2 h-2 bg-green-500 rounded-full"></span>
                      <h3 class="font-semibold text-slate-700">设计效果图</h3>
                      <span class="text-xs text-slate-400">系统生成</span>
                    </div>
                    <div class="aspect-square bg-white rounded-lg border border-slate-200 flex items-center justify-center overflow-hidden">
                      <img v-if="selectedOrder.effect_image_url" :src="selectedOrder.effect_image_url" class="w-full h-full object-cover" alt="效果图">
                      <div v-else class="text-center p-4">
                        <div class="w-24 h-24 mx-auto mb-3 rounded-full bg-gradient-to-br from-gray-300 to-gray-400 flex items-center justify-center shadow-lg">
                          <span class="text-white font-bold text-lg">{{ selectedOrder.front_text }}</span>
                        </div>
                        <p class="text-sm font-medium text-slate-700">{{ selectedOrder.product_shape }} - {{ selectedOrder.product_color }}</p>
                        <p class="text-xs text-slate-500">{{ selectedOrder.font_code }} 字体</p>
                      </div>
                    </div>
                    <p class="text-xs text-slate-500 mt-2 text-center">客户确认的设计效果</p>
                  </div>
                </div>
              </div>

              <!-- 右侧：生产文档信息 + 物流面单 -->
              <div class="col-span-12 lg:col-span-4 space-y-4">
                <!-- 生产文档信息 -->
                <div class="bg-slate-50 rounded-xl border border-slate-200 p-5">
                  <h3 class="font-bold text-slate-800 mb-4 flex items-center gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                      <polyline points="14 2 14 8 20 8"/>
                    </svg>
                    生产文档信息
                  </h3>
                  
                  <div class="space-y-3 mb-4">
                    <div class="bg-white rounded-lg p-3 border border-slate-200">
                      <p class="text-xs text-slate-500 mb-1">订单号</p>
                      <p class="font-mono font-semibold text-slate-800">{{ selectedOrder.etsy_order_id }}</p>
                    </div>
                    <div class="bg-white rounded-lg p-3 border border-slate-200">
                      <p class="text-xs text-slate-500 mb-1">物流单号</p>
                      <p class="font-mono font-semibold text-slate-800">{{ selectedOrder.tracking_number || '4PX123456789' }}</p>
                    </div>
                    <div class="bg-white rounded-lg p-3 border border-slate-200">
                      <p class="text-xs text-slate-500 mb-1">定制内容</p>
                      <p class="text-sm"><span class="text-slate-500">正面:</span> <span class="font-medium">{{ selectedOrder.front_text }}</span></p>
                      <p class="text-sm"><span class="text-slate-500">字体:</span> <span class="font-medium">{{ selectedOrder.font_code }}</span></p>
                      <p class="text-sm"><span class="text-slate-500">背面:</span> <span class="font-medium">{{ selectedOrder.back_text }}</span></p>
                    </div>
                    <div class="bg-white rounded-lg p-3 border border-slate-200">
                      <p class="text-xs text-slate-500 mb-1">收货地址</p>
                      <p class="text-sm font-medium text-slate-800">{{ selectedOrder.logistics?.recipient_name || 'Jane Smith' }}</p>
                      <p class="text-sm text-slate-600">{{ selectedOrder.logistics?.street_address || '456 Oak Street, Toronto' }}</p>
                      <p class="text-sm text-slate-600">{{ selectedOrder.logistics?.country || 'Canada' }} {{ selectedOrder.logistics?.postal_code || 'M5V 3A8' }}</p>
                    </div>
                  </div>

                  <button class="w-full py-2 bg-blue-50 text-blue-600 rounded-lg text-sm font-medium hover:bg-blue-100 flex items-center justify-center gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                      <polyline points="14 2 14 8 20 8"/>
                    </svg>
                    查看完整PDF
                  </button>
                </div>

                <!-- 物流面单 -->
                <div class="bg-white rounded-xl border-2 border-slate-300 p-4">
                  <div class="flex items-center justify-between mb-3">
                    <h3 class="font-bold text-slate-800 flex items-center gap-2">
                      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect width="20" height="16" x="2" y="4" rx="2"/>
                        <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>
                      </svg>
                      物流面单
                    </h3>
                    <span class="text-xs text-slate-400">4PX物流</span>
                  </div>
                  
                  <!-- 面单预览 -->
                  <div class="bg-slate-50 rounded-lg border border-slate-200 p-4 space-y-3">
                    <!-- 条码区域 -->
                    <div class="text-center pb-3 border-b border-dashed border-slate-300">
                      <div class="font-mono text-lg font-bold tracking-widest">{{ selectedOrder.tracking_number || '4PX123456789' }}</div>
                      <div class="h-8 bg-slate-800 mt-1 rounded barcode-pattern"></div>
                      <p class="text-xs text-slate-500 mt-1">扫描条码核对单号</p>
                    </div>
                    
                    <!-- 地址信息 -->
                    <div class="space-y-1">
                      <p class="text-xs text-slate-500 uppercase tracking-wider">To / 收件人</p>
                      <p class="font-bold text-slate-800">{{ selectedOrder.logistics?.recipient_name || 'Jane Smith' }}</p>
                      <p class="text-sm text-slate-700">{{ selectedOrder.logistics?.street_address || '456 Oak Street' }}</p>
                      <p class="text-sm text-slate-700">{{ selectedOrder.logistics?.city || 'Toronto' }}, {{ selectedOrder.logistics?.state || 'ON' }} {{ selectedOrder.logistics?.postal_code || 'M5V 3A8' }}</p>
                      <p class="text-sm font-medium text-slate-800">{{ selectedOrder.logistics?.country || 'Canada' }}</p>
                    </div>
                    
                    <!-- 核对提示 -->
                    <div class="bg-amber-50 border border-amber-200 rounded-lg p-2 mt-2">
                      <p class="text-xs text-amber-700 flex items-center gap-1">
                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <circle cx="12" cy="12" r="10"/>
                          <path d="M12 16v-4"/>
                          <path d="M12 8h.01"/>
                        </svg>
                        请核对面单地址与右侧收货地址一致
                      </p>
                    </div>
                  </div>
                  
                  <button class="w-full mt-3 py-2 bg-slate-100 text-slate-600 rounded-lg text-sm font-medium hover:bg-slate-200 flex items-center justify-center gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <polyline points="6 9 6 2 18 2 18 9"/>
                      <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/>
                      <rect x="6" y="14" width="12" height="8"/>
                    </svg>
                    打印面单
                  </button>
                </div>
              </div>
            </div>

            <!-- 底部确认按钮 -->
            <div class="mt-6 flex gap-4 justify-center">
              <button 
                @click="verifyOrder"
                :class="selectedOrder.verifyStatus === 'verified' ? 'verify-btn-active' : 'bg-slate-200 text-slate-400'"
                class="px-8 py-3 rounded-xl font-bold text-lg transition-all"
              >
                {{ selectedOrder.verifyStatus === 'verified' ? '✓ 校验完成' : '校验完成' }}
              </button>
              <button 
                @click="confirmPickup"
                :disabled="selectedOrder.verifyStatus !== 'verified'"
                :class="selectedOrder.verifyStatus === 'verified' ? 'pickup-btn-active' : 'pickup-btn-disabled'"
                class="px-8 py-3 rounded-xl font-bold text-lg transition-all"
              >
                确认揽件
              </button>
            </div>
            
            <!-- 回退操作 -->
            <div class="mt-4 flex gap-3 justify-center">
              <button 
                @click="rollbackToProduction"
                class="px-4 py-2 text-sm text-slate-500 hover:text-orange-600 hover:bg-orange-50 rounded-lg transition-all flex items-center gap-1"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M3 7v6h6"/>
                  <path d="M21 17a9 9 0 0 0-9-9 9 9 0 0 0-6 2.3L3 13"/>
                </svg>
                回退到生产文档
              </button>
              <span class="text-slate-300">|</span>
              <button 
                @click="unselectOrder"
                class="px-4 py-2 text-sm text-slate-500 hover:text-slate-700 rounded-lg transition-all"
              >
                重新选择订单
              </button>
            </div>
            <p class="text-center text-sm text-slate-400 mt-3">
              {{ selectedOrder.verifyStatus === 'verified' ? '请点击「确认揽件」完成发货' : '请先点击「校验完成」确认信息正确' }}
            </p>
          </div>
        </div>

        <!-- 未选择订单提示 -->
        <div v-else class="bg-white rounded-xl shadow-sm border border-slate-200 p-12 text-center">
          <div class="w-20 h-20 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="1.5">
              <path d="M21 10V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l2-1.14"/>
              <path d="m7.5 4.27 9 5.15"/>
              <polyline points="3.29 7 12 12 20.71 7"/>
              <line x1="12" x2="12" y1="22" y2="12"/>
            </svg>
          </div>
          <p class="text-slate-500">请点击上方订单卡片选择要校验的订单</p>
        </div>
      </div>

      <!-- Tab 3: 已完成 -->
      <div v-if="activeTab === 'completed'" class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <div class="bg-slate-50 px-6 py-4 border-b border-slate-200">
          <h2 class="text-lg font-bold text-slate-800">今日已完成订单</h2>
        </div>
        <div class="p-6">
          <table class="w-full">
            <thead>
              <tr class="border-b border-slate-200">
                <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">订单号</th>
                <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">产品信息</th>
                <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">定制内容</th>
                <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">确认时间</th>
                <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">状态</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              <tr v-for="order in completedOrders" :key="order.id" class="hover:bg-slate-50">
                <td class="py-4 px-4">
                  <p class="font-mono font-semibold text-slate-800">{{ order.etsy_order_id }}</p>
                </td>
                <td class="py-4 px-4">
                  <div class="flex items-center gap-2">
                    <span class="w-3 h-3 rounded-full" :class="getColorClass(order.product_color)"></span>
                    <span class="text-sm">{{ order.product_shape }} - {{ order.product_color }} - {{ order.product_size }}</span>
                  </div>
                </td>
                <td class="py-4 px-4">
                  <p class="text-sm"><span class="text-slate-500">正面:</span> <span class="font-medium">{{ order.front_text }}</span></p>
                  <p class="text-sm"><span class="text-slate-500">背面:</span> <span class="font-medium">{{ order.back_text }}</span></p>
                </td>
                <td class="py-4 px-4">
                  <p class="text-sm text-slate-600">{{ formatTime(order.completed_at) }}</p>
                </td>
                <td class="py-4 px-4">
                  <span class="px-2 py-1 bg-green-100 text-green-700 text-xs font-medium rounded-full">已发货</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>

    <!-- 成功弹窗 -->
    <div v-if="showSuccessModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-md text-center">
        <div class="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2.5">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
            <path d="m9 11 3 3L22 4"/>
          </svg>
        </div>
        <h3 class="text-xl font-bold text-slate-800 mb-2">揽件确认成功</h3>
        <p class="text-slate-500 mb-6">订单 <span class="font-mono font-semibold">{{ selectedOrder?.etsy_order_id }}</span> 已完成生产并发货</p>
        <button @click="closeModal" class="w-full py-3 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700">
          继续确认下一单
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useOrderStore } from '../../stores/orderStore'
import supabase from '../../utils/supabase'
import { ElMessage } from 'element-plus'

const store = useOrderStore()
const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

// 状态
const activeTab = ref('production')
const selectedDate = ref(new Date().toISOString().split('T')[0])
const today = new Date().toISOString().split('T')[0]
const selectedOrder = ref(null)
const showSuccessModal = ref(false)

// 订单数据
const productionOrders = ref([])
const pickupOrders = ref([])
const completedOrders = ref([])

// 计算属性
const currentDate = computed(() => {
  const date = new Date()
  return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日 星期${['日', '一', '二', '三', '四', '五', '六'][date.getDay()]}`
})

// 方法
function switchTab(tab) {
  activeTab.value = tab
  if (tab === 'pickup') {
    selectedOrder.value = null
  }
}

function setYesterday() {
  const yesterday = new Date()
  yesterday.setDate(yesterday.getDate() - 1)
  selectedDate.value = yesterday.toISOString().split('T')[0]
}

function getColorClass(color) {
  const colorMap = {
    '金色': 'bg-yellow-400',
    '银色': 'bg-gray-300',
    '玫瑰金': 'bg-amber-700',
    '黑色': 'bg-gray-800',
    '白色': 'bg-white border border-gray-300'
  }
  return colorMap[color] || 'bg-gray-400'
}

function formatTime(timeStr) {
  if (!timeStr) return '--'
  const date = new Date(timeStr)
  return `${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
}

function selectOrder(order) {
  selectedOrder.value = order
}

function verifyOrder() {
  if (selectedOrder.value) {
    selectedOrder.value.verifyStatus = 'verified'
  }
}

async function confirmPickup() {
  if (!selectedOrder.value) return
  
  try {
    // 更新订单状态为 delivered（已发货）
    const { error } = await supabase
      .from('orders')
      .update({
        status: 'delivered',
        confirmed_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      })
      .eq('id', selectedOrder.value.id)
    
    if (error) throw error
    
    showSuccessModal.value = true
  } catch (error) {
    console.error('揽件确认失败:', error)
    ElMessage.error('揽件确认失败：' + error.message)
  }
}

async function closeModal() {
  showSuccessModal.value = false
  // 将订单移到已完成列表
  if (selectedOrder.value) {
    const order = selectedOrder.value
    order.status = 'delivered'
    order.confirmed_at = new Date().toISOString()
    completedOrders.value.unshift(order)
    pickupOrders.value = pickupOrders.value.filter(o => o.id !== order.id)
    selectedOrder.value = null
  }
  activeTab.value = 'completed'
}

// 回退到生产文档
async function rollbackToProduction() {
  if (!selectedOrder.value) return
  
  if (!confirm(`确定将订单 ${selectedOrder.value.etsy_order_id} 回退到「生产文档」阶段吗？\n\n注意：此操作会将订单状态重置为「生产中」`)) {
    return
  }
  
  try {
    // 更新订单状态为 producing
    const { error } = await supabase
      .from('orders')
      .update({
        status: 'producing',
        completed_at: null,
        updated_at: new Date().toISOString()
      })
      .eq('id', selectedOrder.value.id)
    
    if (error) throw error
    
    // 将订单从揽件列表移回生产列表
    const order = selectedOrder.value
    order.status = 'producing'
    order.completed_at = null
    productionOrders.value.push(order)
    pickupOrders.value = pickupOrders.value.filter(o => o.id !== order.id)
    selectedOrder.value = null
    
    ElMessage.success('订单已回退到「生产文档」阶段')
  } catch (error) {
    console.error('回退失败:', error)
    ElMessage.error('回退失败：' + error.message)
  }
}

// 取消选择订单
function unselectOrder() {
  selectedOrder.value = null
}

async function downloadPdf(order) {
  if (order.production_pdf_url) {
    window.open(order.production_pdf_url, '_blank')
    return
  }
  
  // 如果没有PDF，调用后端生成
  try {
    ElMessage.info('正在生成生产文档PDF...')
    const res = await fetch(`${API_BASE}/api/pdf/generate-and-upload`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ order_id: order.id })
    })
    
    const data = await res.json()
    if (data.success && data.production_pdf_url) {
      order.production_pdf_url = data.production_pdf_url
      window.open(data.production_pdf_url, '_blank')
      ElMessage.success('PDF生成成功')
    } else {
      throw new Error(data.message || 'PDF生成失败')
    }
  } catch (error) {
    console.error('PDF生成失败:', error)
    ElMessage.error('PDF生成失败：' + error.message)
  }
}

function downloadSvg(order) {
  // 优先使用效果图SVG URL
  const svgUrl = order.effect_svg_url || order.effect_image_url
  if (svgUrl) {
    // 创建临时链接下载
    const link = document.createElement('a')
    link.href = svgUrl
    link.download = `${order.etsy_order_id}.svg`
    link.target = '_blank'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  } else {
    ElMessage.warning('SVG文件尚未生成')
  }
}

function printDocument(order) {
  if (order.production_pdf_url) {
    // 打开PDF在新窗口，用户可以自行打印
    window.open(order.production_pdf_url, '_blank')
    ElMessage.info('请在打开的PDF页面中使用打印功能')
  } else {
    ElMessage.warning('请先生成PDF文档')
  }
}

async function startProduction(order) {
  try {
    // 更新订单状态为 completed（生产完成，待揽件）
    const { error } = await supabase
      .from('orders')
      .update({
        status: 'completed',
        completed_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      })
      .eq('id', order.id)
    
    if (error) throw error
    
    // 从生产列表移到揽件列表
    order.status = 'completed'
    order.completed_at = new Date().toISOString()
    pickupOrders.value.push({ ...order, verifyStatus: 'pending' })
    productionOrders.value = productionOrders.value.filter(o => o.id !== order.id)
    
    ElMessage.success(`订单 ${order.etsy_order_id} 已标记为生产完成`)
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage.error('操作失败：' + error.message)
  }
}

// 加载订单数据 - 从Supabase获取真实数据
async function loadOrders() {
  try {
    loading.value = true
    
    // 1. 获取生产中订单 (status = 'producing')
    const { data: producingData, error: producingError } = await supabase
      .from('orders')
      .select(`
        *,
        sku_mapping(*)
      `)
      .eq('status', 'producing')
      .order('created_at', { ascending: false })
    
    if (producingError) throw producingError
    
    // 2. 获取待揽件订单 (status = 'completed')
    const { data: completedData, error: completedError } = await supabase
      .from('orders')
      .select(`
        *,
        sku_mapping(*),
        logistics(*)
      `)
      .eq('status', 'completed')
      .order('completed_at', { ascending: false })
    
    if (completedError) throw completedError
    
    // 3. 获取已发货订单 (status = 'delivered')
    const { data: deliveredData, error: deliveredError } = await supabase
      .from('orders')
      .select(`
        *,
        sku_mapping(*)
      `)
      .eq('status', 'delivered')
      .order('completed_at', { ascending: false })
      .limit(50)
    
    if (deliveredError) throw deliveredError
    
    // 处理生产文档订单数据
    productionOrders.value = (producingData || []).map(order => ({
      ...order,
      etsy_order_id: order.order_number,
      product_shape: order.sku_mapping?.shape || '-',
      product_color: order.sku_mapping?.color || '-',
      product_size: order.sku_mapping?.size || '-',
      product_craft: order.sku_mapping?.craft || '抛光',
      front_text: order.custom_text_front || '-',
      back_text: order.custom_text_back || '-',
      font_code: order.font_code || '-'
    }))
    
    // 处理揽件订单数据
    pickupOrders.value = (completedData || []).map(order => ({
      ...order,
      etsy_order_id: order.order_number,
      product_shape: order.sku_mapping?.shape || '-',
      product_color: order.sku_mapping?.color || '-',
      product_size: order.sku_mapping?.size || '-',
      product_craft: order.sku_mapping?.craft || '抛光',
      front_text: order.custom_text_front || '-',
      back_text: order.custom_text_back || '-',
      font_code: order.font_code || '-',
      tracking_number: order.logistics?.tracking_number || '',
      verifyStatus: 'pending'
    }))
    
    // 处理已完成订单数据
    completedOrders.value = (deliveredData || []).map(order => ({
      ...order,
      etsy_order_id: order.order_number,
      product_shape: order.sku_mapping?.shape || '-',
      product_color: order.sku_mapping?.color || '-',
      product_size: order.sku_mapping?.size || '-',
      front_text: order.custom_text_front || '-',
      back_text: order.custom_text_back || '-',
      font_code: order.font_code || '-'
    }))
    
    console.log('✅ 订单数据加载成功:', {
      producing: productionOrders.value.length,
      pickup: pickupOrders.value.length,
      completed: completedOrders.value.length
    })
  } catch (error) {
    console.error('❌ 加载订单失败:', error)
    ElMessage.error('加载订单数据失败: ' + error.message)
  } finally {
    loading.value = false
  }
}

const loading = ref(false)

// ==================== 工厂登录相关 ====================
const isAuthenticated = ref(false)
const password = ref('')
const loginLoading = ref(false)
const loginError = ref('')
const currentFactory = ref(null)
const factoryCode = ref('') // 工厂代码输入

// 检查登录状态
function checkAuth() {
  const auth = localStorage.getItem('factory_auth')
  if (auth) {
    const authData = JSON.parse(auth)
    // 检查是否过期（8小时）
    if (Date.now() - authData.timestamp < 8 * 60 * 60 * 1000) {
      currentFactory.value = authData.factory
      isAuthenticated.value = true
      return true
    }
    localStorage.removeItem('factory_auth')
  }
  return false
}

// 登录处理 - 对接后端API
async function handleLogin() {
  if (!factoryCode.value || !password.value) {
    loginError.value = '请输入工厂代码和密码'
    return
  }
  
  loginLoading.value = true
  loginError.value = ''
  
  try {
    const res = await fetch(`${API_BASE}/api/factories/verify-password`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        code: factoryCode.value,
        password: password.value
      })
    })
    
    const result = await res.json()
    
    if (result.success && result.data?.valid) {
      currentFactory.value = result.data.factory
      isAuthenticated.value = true
      
      // 保存登录状态
      localStorage.setItem('factory_auth', JSON.stringify({
        factory: result.data.factory,
        timestamp: Date.now()
      }))
      
      ElMessage.success('登录成功')
      // 加载订单
      await loadOrders()
    } else {
      loginError.value = result.data?.message || '密码错误或工厂不存在'
    }
  } catch (error) {
    console.error('登录失败:', error)
    loginError.value = '网络错误，请稍后重试'
  } finally {
    loginLoading.value = false
  }
}

// 退出登录
function logout() {
  localStorage.removeItem('factory_auth')
  isAuthenticated.value = false
  currentFactory.value = null
  password.value = ''
}

onMounted(() => {
  // 先检查登录状态
  if (checkAuth()) {
    loadOrders()
  }
})
</script>

<style scoped>
.tab-active {
  background-color: #3b82f6;
  color: white;
}
.tab-inactive {
  background-color: #f1f5f9;
  color: #64748b;
}
.tab-inactive:hover {
  background-color: #e2e8f0;
}
.order-selected {
  border-color: #3b82f6;
  background-color: #eff6ff;
}
.verify-btn-active {
  background-color: #10b981;
  color: white;
}
.pickup-btn-disabled {
  background-color: #e2e8f0;
  color: #94a3b8;
  cursor: not-allowed;
}
.pickup-btn-active {
  background-color: #8b5cf6;
  color: white;
}
.barcode-pattern {
  background: repeating-linear-gradient(90deg, #000 0px, #000 2px, #fff 2px, #fff 4px);
}
</style>