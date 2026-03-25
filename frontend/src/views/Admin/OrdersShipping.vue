<template>
  <div class="h-full overflow-auto bg-slate-50 p-4">
    <!-- 页面标题 -->
    <div class="mb-4 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-slate-800">物流下单</h1>
        <p class="text-sm text-slate-500 mt-1">选择订单并创建物流运单</p>
      </div>
      <div class="flex items-center gap-2 text-sm">
        <span class="text-xs text-slate-400">运营:</span>
        <button class="px-2 py-1 rounded text-xs font-medium" :class="activeAccount === 'all' ? 'bg-blue-600 text-white' : 'bg-white text-slate-600 border border-slate-200'" @click="activeAccount = 'all'">全部</button>
        <button class="px-2 py-1 rounded text-xs font-medium" :class="activeAccount === 'A' ? 'bg-blue-600 text-white' : 'bg-white text-slate-600 border border-slate-200'" @click="activeAccount = 'A'">A运营</button>
        <button class="px-2 py-1 rounded text-xs font-medium" :class="activeAccount === 'B' ? 'bg-blue-600 text-white' : 'bg-white text-slate-600 border border-slate-200'" @click="activeAccount = 'B'">B运营</button>
        <button class="px-2 py-1 rounded text-xs font-medium" :class="activeAccount === 'C' ? 'bg-blue-600 text-white' : 'bg-white text-slate-600 border border-slate-200'" @click="activeAccount = 'C'">C运营</button>
      </div>
    </div>

    <!-- 物流公司Tab页 -->
    <div class="flex border-b border-slate-200 mb-4 items-end gap-1">
      <button 
        @click="activeTab = '4px'" 
        :class="['px-6 py-3 text-sm font-medium transition-colors', activeTab === '4px' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-slate-500 hover:text-slate-700']"
      >
        4PX全球直发
      </button>
      <button 
        @click="activeTab = 'yanwen'" 
        :class="['px-6 py-3 text-sm font-medium transition-colors flex items-center gap-1', activeTab === 'yanwen' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-slate-400']"
        title="暂未接入"
      >
        燕文物流
        <span class="text-[10px] bg-slate-100 text-slate-400 px-1.5 py-0.5 rounded-full">未接入</span>
      </button>
      <button 
        @click="activeTab = 'yuntu'" 
        :class="['px-6 py-3 text-sm font-medium transition-colors flex items-center gap-1', activeTab === 'yuntu' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-slate-400']"
        title="暂未接入"
      >
        云途物流
        <span class="text-[10px] bg-slate-100 text-slate-400 px-1.5 py-0.5 rounded-full">未接入</span>
      </button>
    </div>

    <!-- 燕文/云途占位提示 -->
    <div v-if="activeTab !== '4px'" class="flex items-center justify-center h-48 bg-white rounded-xl border border-dashed border-slate-200 mb-4">
      <div class="text-center text-slate-400">
        <div class="text-2xl mb-2">🔜</div>
        <div class="font-medium">{{ activeTab === 'yanwen' ? '燕文物流' : '云途物流' }} 暂未接入</div>
        <div class="text-sm mt-1">接口对接中，敬请期待</div>
      </div>
    </div>

    <!-- 4PX Tab内容 -->
    <div v-if="activeTab === '4px'" class="flex gap-4">
      <!-- 左侧：下单详情 (60%) -->
      <div class="w-[60%] shrink-0">
        <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
          <div class="px-4 py-3 border-b border-slate-100 bg-slate-50 flex items-center justify-between">
            <h2 class="text-base font-bold text-slate-800">
              {{ isBatchMode ? `批量下单确认（已选 ${selectedOrders.length} 单）` : '物流下单表单' }}
            </h2>
            <!-- 批量模式：物流渠道统一选择器 -->
            <div v-if="isBatchMode" class="flex items-center gap-2">
              <span class="text-xs text-slate-500">统一渠道:</span>
              <select v-model="form.channel_code" class="px-2 py-1 border border-slate-200 rounded text-xs focus:outline-none focus:ring-1 focus:ring-blue-500/20">
                <option v-for="channel in channels" :key="channel.code" :value="channel.code">
                  {{ channel.code }} - {{ channel.name }}
                </option>
              </select>
            </div>
          </div>

          <!-- ══ 批量模式：批量下单确认列表 ══ -->
          <div v-if="isBatchMode" class="p-4 space-y-3">
            <!-- 迷你订单卡片列表（订单详情） -->
            <div class="bg-slate-50 rounded-lg p-3">
              <h3 class="text-xs font-bold text-slate-500 mb-2">📋 已选订单汇总</h3>
              <div class="space-y-2 max-h-[320px] overflow-y-auto">
                <div 
                  v-for="order in selectedOrders" 
                  :key="order.id"
                  class="bg-white border border-slate-200 rounded-lg overflow-hidden"
                >
                  <!-- 主行：点击展开订单详情 -->
                  <div 
                    class="px-3 py-2 flex items-center gap-3 text-[11px] cursor-pointer hover:bg-slate-50 transition-colors select-none"
                    @click="toggleBatchExpand(order.id)"
                  >
                    <!-- 展开箭头 -->
                    <svg :class="['w-3 h-3 text-slate-400 shrink-0 transition-transform', expandedBatchOrderId === order.id ? 'rotate-90' : '']" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <polyline points="9 18 15 12 9 6"></polyline>
                    </svg>
                    <!-- 状态图标 -->
                    <div class="shrink-0">
                      <span v-if="batchAddressMap[order.id]?.ready" class="text-green-500">✅</span>
                      <span v-else class="text-amber-400">⏳</span>
                    </div>
                    <!-- 订单信息 -->
                    <div class="flex-1 grid grid-cols-4 gap-x-3">
                      <span class="text-red-500 font-medium">{{ order.etsy_order_id }}</span>
                      <span class="text-slate-600">{{ order.customer_name }}</span>
                      <span class="text-slate-500 font-mono">{{ order.sku_mapping?.sku_code || order.sku_id || '-' }}</span>
                      <span class="text-slate-500">{{ order.country || '-' }}</span>
                    </div>
                    <!-- 地址状态 -->
                    <div class="shrink-0 text-right">
                      <span v-if="batchAddressMap[order.id]?.ready" class="text-green-600 text-[10px]">地址已就绪</span>
                      <span v-else class="text-amber-500 text-[10px]">地址加载中...</span>
                    </div>
                    <!-- 移除按钮 -->
                    <button 
                      @click.stop="removeFromBatch(order)"
                      class="shrink-0 text-slate-300 hover:text-red-400 transition-colors text-base leading-none"
                      title="从批量列表移除"
                    >×</button>
                  </div>
                  <!-- 展开详情区 -->
                  <div v-if="expandedBatchOrderId === order.id" class="border-t border-slate-100 bg-slate-50 px-4 py-3">
                    <div class="flex gap-3">
                      <!-- 实拍图 -->
                      <div class="w-16 h-16 shrink-0 bg-white rounded border border-slate-200 overflow-hidden">
                        <img v-if="order.real_photo_urls" :src="JSON.parse(order.real_photo_urls)[0]" class="w-full h-full object-contain"/>
                        <img v-else-if="order.effect_image_url" :src="order.effect_image_url" class="w-full h-full object-contain"/>
                        <img v-else-if="order.sku_mapping?.image_url" :src="order.sku_mapping.image_url" class="w-full h-full object-contain"/>
                        <div v-else class="w-full h-full flex items-center justify-center text-slate-400 text-[9px]">暂无图片</div>
                      </div>
                      <!-- 详情字段 -->
                      <div class="flex-1 text-[11px] space-y-1">
                        <div class="grid grid-cols-2 gap-x-4 gap-y-1">
                          <div><span class="text-slate-400">订单ID: </span><span class="text-red-500 font-medium">{{ order.etsy_order_id }}</span></div>
                          <div><span class="text-slate-400">国家: </span><span class="text-slate-700">{{ order.country || order.shipping_country || '-' }}</span></div>
                          <div><span class="text-slate-400">客户: </span><span class="text-slate-700">{{ order.customer_name }}</span></div>
                          <div><span class="text-slate-400">SKU: </span><span class="text-slate-700 font-mono">{{ order.sku_mapping?.sku_code || order.sku_id || '-' }}</span></div>
                          <div><span class="text-slate-400">形状: </span><span class="text-slate-700">{{ order.product_shape || order.sku_mapping?.shape || '-' }}</span></div>
                          <div><span class="text-slate-400">颜色: </span><span class="text-slate-700">{{ order.product_color || order.sku_mapping?.color || '-' }}</span></div>
                          <div><span class="text-slate-400">尺寸: </span><span class="text-slate-700">{{ order.product_size || order.sku_mapping?.size || '-' }}</span></div>
                          <div><span class="text-slate-400">数量: </span><span class="text-slate-700">{{ order.quantity || 1 }}</span></div>
                          <div><span class="text-slate-400">重量: </span><span class="text-slate-700">{{ order.weight_g || order.sku_mapping?.weight_g || '-' }}g</span></div>
                        </div>
                        <!-- 地址 -->
                        <div v-if="batchAddressMap[order.id]?.ready" class="mt-1 pt-1 border-t border-slate-200">
                          <span class="text-slate-400">收件地址: </span>
                          <span class="text-slate-600">{{ batchAddressMap[order.id].name }} · {{ batchAddressMap[order.id].street }}, {{ batchAddressMap[order.id].city }} {{ batchAddressMap[order.id].zip }} {{ batchAddressMap[order.id].country }}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div v-if="selectedOrders.length === 0" class="text-center text-slate-400 py-4 text-xs">
                  请从右侧勾选订单
                </div>
              </div>
            </div>

            <!-- 批量确认统计 -->
            <div class="flex items-center justify-between text-xs text-slate-500 px-1">
              <span>地址就绪: <span class="text-green-600 font-bold">{{ batchReadyCount }}</span> / {{ selectedOrders.length }} 单</span>
              <span v-if="batchReadyCount < selectedOrders.length" class="text-amber-500">⚠ 部分订单地址未完整，仍可提交（将跳过不完整订单）</span>
            </div>

            <!-- 批量提交按钮 + 取消按钮 -->
            <div class="flex gap-2 justify-center">
              <button 
                @click="cancelBatch"
                class="w-24 py-2 border border-slate-300 text-slate-600 hover:bg-slate-50 rounded-lg font-medium text-sm transition-colors"
              >取消</button>
              <button 
                @click="createBatchOrder" 
                :disabled="submittingBatch || selectedOrders.length === 0" 
                class="w-48 bg-purple-600 hover:bg-purple-700 disabled:bg-purple-400 text-white py-2 rounded-lg font-medium text-sm flex items-center justify-center gap-2 transition-colors"
              >
                <svg v-if="submittingBatch" class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                {{ submittingBatch ? `批量下单中 (${batchProgress}/${selectedOrders.length})...` : `🚀 确认批量下单 (${selectedOrders.length}单)` }}
              </button>
            </div>

            <!-- 批量结果 -->
            <div v-if="showResult && batchResults.length > 0" class="bg-slate-50 border border-slate-200 rounded-lg p-3">
              <h3 class="text-sm font-bold text-slate-700 mb-2 flex items-center gap-1">
                📋 批量下单结果
                <span class="text-xs font-normal text-slate-500">(成功 {{ batchResults.filter(r => r.success).length }} / {{ batchResults.length }})</span>
              </h3>
              <div class="max-h-[160px] overflow-y-auto space-y-1.5 mb-3">
                <div 
                  v-for="result in batchResults" 
                  :key="result.orderId"
                  :class="['text-xs p-2 rounded flex items-center justify-between', result.success ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-600']"
                >
                  <div class="flex items-center gap-2">
                    <span>{{ result.success ? '✅' : '❌' }}</span>
                    <span class="font-medium">{{ result.etsyOrderId }}</span>
                    <span v-if="result.success" class="font-mono text-[10px]">{{ result.trackingNumber }}</span>
                    <span v-else class="text-[10px]">{{ result.error }}</span>
                  </div>
                  <a v-if="result.success && result.labelUrl" :href="result.labelUrl" target="_blank" class="text-blue-600 hover:underline text-[10px]">面单</a>
                </div>
              </div>
              <div class="flex gap-2">
                <button @click="downloadAllLabels" :disabled="!batchResults.some(r => r.success && r.labelUrl)" class="flex-1 bg-white border border-slate-300 text-slate-700 hover:bg-slate-100 disabled:text-slate-400 py-2 rounded-lg text-xs font-medium flex items-center justify-center gap-1 transition-colors">
                  📄 下载全部面单
                </button>
                <button @click="continueOrder" class="flex-1 bg-white border border-slate-300 text-slate-700 hover:bg-slate-100 py-2 rounded-lg text-xs font-medium flex items-center justify-center gap-1 transition-colors">
                  ← 继续下单
                </button>
              </div>
            </div>
          </div>

          <!-- ══ 单选模式：原有表单 ══ -->
          <div v-else>
          <!-- 未选择订单时的引导 -->
          <div v-if="!selectedOrder" class="p-8 text-center">
            <div class="text-slate-400 text-lg">→ 请从右侧选择一个订单</div>
            <p class="text-slate-300 text-sm mt-2">选择订单后可填写物流信息并创建运单</p>
          </div>

          <!-- 选中订单后显示表单 -->
          <div v-else class="p-4 space-y-4">
            <!-- Section A: 订单详情（三块并排：实拍图 | 订单详情 | 物流地址） -->
            <div class="bg-slate-50 rounded-lg p-3">
              <h3 class="text-xs font-bold text-slate-600 mb-2 flex items-center gap-1">
                <span>📦</span> 订单详情
              </h3>
              <div class="flex gap-3 items-stretch">

                <!-- 块1：实拍图/效果图（正方形） -->
                <div class="w-32 h-32 shrink-0 bg-white rounded-lg overflow-hidden border border-blue-200">
                  <img v-if="selectedOrder.real_photo_urls" :src="JSON.parse(selectedOrder.real_photo_urls)[0]" class="w-full h-full object-contain"/>
                  <img v-else-if="selectedOrder.effect_image_url && selectedOrder.effect_image_url.trim()" :src="selectedOrder.effect_image_url" class="w-full h-full object-contain"/>
                  <img v-else-if="selectedOrder.sku_mapping?.image_url" :src="selectedOrder.sku_mapping.image_url" class="w-full h-full object-contain"/>
                  <div v-else class="w-full h-full flex items-center justify-center text-slate-400 text-[10px]">暂无图片</div>
                </div>

                <!-- 块2：订单详情（严格按位置编排） -->
                <div class="flex-1 h-32 bg-white border border-blue-200 rounded-lg p-2 text-[11px] overflow-hidden">
                  <!-- 第1行：订单ID -->
                  <div class="mb-1.5">
                    <span class="text-slate-400">订单ID: </span>
                    <span class="text-red-500 font-medium">{{ selectedOrder.etsy_order_id }}</span>
                  </div>
                  <!-- 第2行：国家 | 客户 -->
                  <div class="flex gap-3 mb-1.5">
                    <span><span class="text-slate-400">国家: </span><span class="text-slate-700">{{ selectedOrder.country || selectedOrder.shipping_country || '-' }}</span></span>
                    <span><span class="text-slate-400">客户: </span><span class="text-slate-700">{{ selectedOrder.customer_name }}</span></span>
                  </div>
                  <!-- 第3行：SKU -->
                  <div class="mb-1.5">
                    <span class="text-slate-400">SKU: </span>
                    <span class="text-slate-700 font-mono">{{ selectedOrder.sku_mapping?.sku_code || selectedOrder.sku_id || '-' }}</span>
                  </div>
                  <!-- 第4行：形状 | 颜色 | 尺寸 -->
                  <div class="flex gap-3 mb-1.5">
                    <span><span class="text-slate-400">形状: </span><span class="text-slate-700">{{ selectedOrder.product_shape || selectedOrder.sku_mapping?.shape || '-' }}</span></span>
                    <span><span class="text-slate-400">颜色: </span><span class="text-slate-700">{{ selectedOrder.product_color || selectedOrder.sku_mapping?.color || '-' }}</span></span>
                    <span><span class="text-slate-400">尺寸: </span><span class="text-slate-700">{{ selectedOrder.product_size || selectedOrder.sku_mapping?.size || '-' }}</span></span>
                  </div>
                  <!-- 第5行：数量 | 重量 -->
                  <div class="flex gap-3">
                    <span><span class="text-slate-400">数量: </span><span class="text-slate-700">{{ selectedOrder.quantity || 1 }}</span></span>
                    <span><span class="text-slate-400">重量: </span><span class="text-slate-700">{{ selectedOrder.weight_g || selectedOrder.sku_mapping?.weight_g || '-' }}g</span></span>
                  </div>
                </div>

                <!-- 块3：物流地址（自动填充，与块2等宽） -->
                <div class="flex-1 h-32 bg-white border border-blue-200 rounded-lg p-3 text-[11px] relative flex flex-col overflow-hidden">
                  <div class="text-slate-400 mb-1 font-medium">地址:</div>
                  <div v-if="form.recipient_street || form.recipient_city" class="text-slate-700 space-y-0.5 flex-1">
                    <div v-if="form.recipient_name" class="font-medium text-slate-800">{{ form.recipient_name }}</div>
                    <div v-if="form.recipient_street">{{ form.recipient_street }}</div>
                    <div v-if="form.recipient_city || form.recipient_state">
                      {{ [form.recipient_city, form.recipient_state].filter(Boolean).join(', ') }}
                    </div>
                    <div v-if="form.recipient_postcode || form.recipient_country">
                      {{ [form.recipient_postcode, form.recipient_country].filter(Boolean).join(' ') }}
                    </div>
                    <div v-if="form.recipient_phone" class="text-slate-500">{{ form.recipient_phone }}</div>
                  </div>
                  <div v-else class="flex-1 flex items-center justify-center text-slate-300 text-[10px]">地址数据加载中...</div>
                  <div class="text-right text-[10px] text-slate-400 mt-1">自动填充</div>
                </div>

              </div>
            </div>

            <!-- Section BCD：左右紧凑布局（左=收件人信息，右上=包裹信息，右下=物流渠道） -->
            <div class="flex gap-3">

              <!-- ══ 左列：收件人信息 ══ -->
              <div class="flex-1 border border-blue-200 rounded-lg p-3 bg-white">
                <h3 class="text-xs font-bold text-slate-600 mb-2 flex items-center gap-1">
                  <span>📮</span> 收件人信息
                </h3>
                <div class="space-y-2">
                  <!-- 行1：姓名 | 电话 -->
                  <div class="grid grid-cols-2 gap-2">
                    <div>
                      <label class="block text-[10px] text-slate-400 mb-0.5">姓名 <span class="text-red-400">*</span></label>
                      <input v-model="form.recipient_name" type="text" class="w-full px-2 py-1.5 border border-slate-200 rounded text-xs focus:outline-none focus:ring-1 focus:ring-blue-500/20 focus:border-blue-500" />
                    </div>
                    <div>
                      <label class="block text-[10px] text-slate-400 mb-0.5">电话</label>
                      <input v-model="form.recipient_phone" type="text" class="w-full px-2 py-1.5 border border-slate-200 rounded text-xs focus:outline-none focus:ring-1 focus:ring-blue-500/20 focus:border-blue-500" />
                    </div>
                  </div>
                  <!-- 行2：邮编 | 国家（邮编移至此处，邮箱移至最后） -->
                  <div class="grid grid-cols-2 gap-2">
                    <div>
                      <label class="block text-[10px] text-slate-400 mb-0.5">邮编 <span class="text-red-400">*</span></label>
                      <input v-model="form.recipient_postcode" type="text" class="w-full px-2 py-1.5 border border-slate-200 rounded text-xs focus:outline-none focus:ring-1 focus:ring-blue-500/20 focus:border-blue-500" />
                    </div>
                    <div>
                      <label class="block text-[10px] text-slate-400 mb-0.5">国家 <span class="text-red-400">*</span></label>
                      <input v-model="form.recipient_country" type="text" readonly class="w-full px-2 py-1.5 border border-slate-200 rounded text-xs bg-slate-50 text-slate-700" />
                    </div>
                  </div>
                  <!-- 行3：详细地址（全宽，双行高度） -->
                  <div>
                    <label class="block text-[10px] text-slate-400 mb-0.5">详细地址 <span class="text-red-400">*</span></label>
                    <textarea v-model="form.recipient_street" rows="2" class="w-full px-2 py-1.5 border border-slate-200 rounded text-xs focus:outline-none focus:ring-1 focus:ring-blue-500/20 focus:border-blue-500 resize-none"></textarea>
                  </div>
                  <!-- 行4：城市 | 州/省 -->
                  <div class="grid grid-cols-2 gap-2">
                    <div>
                      <label class="block text-[10px] text-slate-400 mb-0.5">城市 <span class="text-red-400">*</span></label>
                      <input v-model="form.recipient_city" type="text" class="w-full px-2 py-1.5 border border-slate-200 rounded text-xs focus:outline-none focus:ring-1 focus:ring-blue-500/20 focus:border-blue-500" />
                    </div>
                    <div>
                      <label class="block text-[10px] text-slate-400 mb-0.5">州/省</label>
                      <input v-model="form.recipient_state" type="text" class="w-full px-2 py-1.5 border border-slate-200 rounded text-xs focus:outline-none focus:ring-1 focus:ring-blue-500/20 focus:border-blue-500" />
                    </div>
                  </div>
                  <!-- 行5：邮箱（移至最后，半宽） -->
                  <div class="grid grid-cols-2 gap-2">
                    <div>
                      <label class="block text-[10px] text-slate-400 mb-0.5">邮箱</label>
                      <input v-model="form.recipient_email" type="email" class="w-full px-2 py-1.5 border border-slate-200 rounded text-xs focus:outline-none focus:ring-1 focus:ring-blue-500/20 focus:border-blue-500" />
                    </div>
                  </div>
                </div>
              </div>

              <!-- ══ 右列：上=包裹信息，下=物流渠道 ══ -->
              <div class="w-[44%] shrink-0 flex flex-col gap-2">

                <!-- 右上：包裹信息 -->
                <div class="border border-slate-200 rounded-lg p-3 bg-white">
                  <h3 class="text-xs font-bold text-slate-600 mb-2 flex items-center gap-1">
                    <span>📐</span> 包裹信息
                  </h3>
                  <!-- 重量/长/宽/高 一行四格 -->
                  <div class="grid grid-cols-4 gap-2 mb-2">
                    <div>
                      <label class="block text-[10px] text-slate-400 mb-0.5">重量(g)</label>
                      <input v-model.number="form.weight" type="number" class="w-full px-2 py-1.5 border border-slate-200 rounded text-xs focus:outline-none focus:ring-1 focus:ring-blue-500/20 focus:border-blue-500" />
                    </div>
                    <div>
                      <label class="block text-[10px] text-slate-400 mb-0.5">长(cm)</label>
                      <input v-model.number="form.length" type="number" class="w-full px-2 py-1.5 border border-slate-200 rounded text-xs focus:outline-none focus:ring-1 focus:ring-blue-500/20 focus:border-blue-500" />
                    </div>
                    <div>
                      <label class="block text-[10px] text-slate-400 mb-0.5">宽(cm)</label>
                      <input v-model.number="form.width" type="number" class="w-full px-2 py-1.5 border border-slate-200 rounded text-xs focus:outline-none focus:ring-1 focus:ring-blue-500/20 focus:border-blue-500" />
                    </div>
                    <div>
                      <label class="block text-[10px] text-slate-400 mb-0.5">高(cm)</label>
                      <input v-model.number="form.height" type="number" class="w-full px-2 py-1.5 border border-slate-200 rounded text-xs focus:outline-none focus:ring-1 focus:ring-blue-500/20 focus:border-blue-500" />
                    </div>
                  </div>
                  <!-- 申报品名中/英：各独占一行（全宽，名字可完整显示） -->
                  <div class="mb-2">
                    <label class="block text-[10px] text-slate-400 mb-0.5">申报品名(中)</label>
                    <input v-model="form.declare_name_cn" type="text" class="w-full px-2 py-1.5 border border-slate-200 rounded text-xs focus:outline-none focus:ring-1 focus:ring-blue-500/20 focus:border-blue-500" />
                  </div>
                  <div class="mb-2">
                    <label class="block text-[10px] text-slate-400 mb-0.5">申报品名(英)</label>
                    <input v-model="form.declare_name_en" type="text" class="w-full px-2 py-1.5 border border-slate-200 rounded text-xs focus:outline-none focus:ring-1 focus:ring-blue-500/20 focus:border-blue-500" />
                  </div>
                  <div class="grid grid-cols-2 gap-2">
                    <div>
                      <label class="block text-[10px] text-slate-400 mb-0.5">申报价值(USD)</label>
                      <input v-model.number="form.declare_value" type="number" step="0.01" class="w-full px-2 py-1.5 border border-slate-200 rounded text-xs focus:outline-none focus:ring-1 focus:ring-blue-500/20 focus:border-blue-500" />
                    </div>
                    <div>
                      <label class="block text-[10px] text-slate-400 mb-0.5">是否带电</label>
                      <div class="flex gap-3 mt-1.5">
                        <label class="flex items-center gap-1 text-xs text-slate-600 cursor-pointer">
                          <input type="radio" v-model="form.has_battery" :value="false" class="text-blue-600" /> 否
                        </label>
                        <label class="flex items-center gap-1 text-xs text-slate-600 cursor-pointer">
                          <input type="radio" v-model="form.has_battery" :value="true" class="text-blue-600" /> 是
                        </label>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- 右下：物流渠道 -->
                <div class="border border-slate-200 rounded-lg p-3 bg-white">
                  <h3 class="text-xs font-bold text-slate-600 mb-2 flex items-center gap-1">
                    <span>🚚</span> 物流渠道
                    <span v-if="loadingChannels" class="text-[10px] text-slate-400 font-normal ml-1">
                      <svg class="animate-spin h-3 w-3 inline" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      查询中...
                    </span>
                  </h3>
                  <select v-model="form.channel_code" class="w-full px-2 py-1.5 border border-slate-200 rounded text-xs focus:outline-none focus:ring-1 focus:ring-blue-500/20 focus:border-blue-500">
                    <option v-for="channel in channels" :key="channel.code" :value="channel.code">
                      {{ channel.code }} - {{ channel.name }}
                    </option>
                  </select>
                </div>

              </div>
            </div>

            <!-- 操作按钮 -->
            <div class="flex gap-3 mt-4 justify-center">
              <!-- 单订单模式 -->
              <button 
                v-if="selectedOrders.length <= 1"
                @click="createOrder" 
                :disabled="submitting || !selectedOrder" 
                class="w-48 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white py-2 rounded-lg font-medium text-sm flex items-center justify-center gap-2 transition-colors"
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
              <!-- 批量模式 -->
              <button 
                v-else
                @click="createBatchOrder" 
                :disabled="submittingBatch || selectedOrders.length === 0" 
                class="flex-1 bg-purple-600 hover:bg-purple-700 disabled:bg-purple-400 text-white py-2.5 rounded-lg font-medium text-sm flex items-center justify-center gap-2 transition-colors"
              >
                <svg v-if="submittingBatch" class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M5 18H3c-.6 0-1-.4-1-1V7c0-.6.4-1 1-1h10c.6 0 1 .4 1 1v11"/>
                  <path d="M14 9h4l4 4v6h-4"/>
                  <circle cx="7" cy="18" r="2"/>
                  <circle cx="17" cy="18" r="2"/>
                </svg>
                {{ submittingBatch ? `正在批量下单 (${batchProgress}/${selectedOrders.length})` : `批量下单 (${selectedOrders.length}单)` }}
              </button>
            </div>

            <!-- 单订单结果区 -->
            <div v-if="showResult && orderResult && selectedOrders.length <= 1" class="bg-green-50 border border-green-200 rounded-lg p-4">
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

            <!-- 批量下单结果区 -->
            <div v-if="showResult && batchResults.length > 0 && selectedOrders.length > 1" class="bg-slate-50 border border-slate-200 rounded-lg p-4">
              <h3 class="text-sm font-bold text-slate-700 mb-3 flex items-center gap-2">
                <span>📋</span> 批量下单结果
                <span class="text-xs font-normal text-slate-500">
                  (成功 {{ batchResults.filter(r => r.success).length }} / {{ batchResults.length }})
                </span>
              </h3>
              <div class="max-h-[200px] overflow-y-auto space-y-2 mb-3">
                <div 
                  v-for="result in batchResults" 
                  :key="result.orderId"
                  :class="['text-xs p-2 rounded flex items-center justify-between', result.success ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-600']"
                >
                  <div class="flex items-center gap-2">
                    <span>{{ result.success ? '✅' : '❌' }}</span>
                    <span class="font-medium">{{ result.etsyOrderId }}</span>
                    <span v-if="result.success" class="font-mono text-[10px]">{{ result.trackingNumber }}</span>
                    <span v-else class="text-[10px]">{{ result.error }}</span>
                  </div>
                  <a 
                    v-if="result.success && result.labelUrl" 
                    :href="result.labelUrl" 
                    target="_blank"
                    class="text-blue-600 hover:underline text-[10px]"
                  >
                    面单
                  </a>
                </div>
              </div>
              <div class="flex gap-2">
                <button 
                  @click="downloadAllLabels" 
                  :disabled="!batchResults.some(r => r.success && r.labelUrl)"
                  class="flex-1 bg-white border border-slate-300 text-slate-700 hover:bg-slate-100 disabled:text-slate-400 py-2 rounded-lg text-sm font-medium flex items-center justify-center gap-2 transition-colors"
                >
                  <span>📄</span> 下载全部面单
                </button>
                <button @click="continueOrder" class="flex-1 bg-white border border-slate-300 text-slate-700 hover:bg-slate-100 py-2 rounded-lg text-sm font-medium flex items-center justify-center gap-2 transition-colors">
                  <span>←</span> 继续下单
                </button>
              </div>
            </div>
          </div>
          <!-- 结束单选模式 v-else -->
          </div>
        </div>
      </div>

      <!-- 右侧：订单列表 (40%) -->
      <div class="flex-1">
        <div class="bg-gray-50 rounded-xl border border-slate-200 overflow-hidden h-full">
          <div class="px-4 py-3 border-b border-slate-200 bg-white">
            <!-- Tab 切换：待下单 / 已下单 -->
            <div class="flex items-center gap-2 mb-3">
              <button
                @click="orderListTab = 'pending'"
                :class="['px-4 py-1.5 rounded-full text-sm font-medium transition-colors', orderListTab === 'pending' ? 'bg-blue-600 text-white' : 'bg-slate-100 text-slate-600 hover:bg-slate-200']"
              >待下单订单</button>
              <button
                @click="orderListTab = 'shipped'"
                :class="['px-4 py-1.5 rounded-full text-sm font-medium transition-colors', orderListTab === 'shipped' ? 'bg-blue-600 text-white' : 'bg-slate-100 text-slate-600 hover:bg-slate-200']"
              >已下单订单</button>
              <div class="ml-auto flex items-center gap-2">
                <span v-if="loading" class="text-xs text-slate-400">
                  <svg class="animate-spin h-4 w-4 inline mr-1" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  加载中...
                </span>
                <span class="bg-blue-100 text-blue-600 px-2 py-0.5 rounded-full text-xs font-bold">{{ currentTabOrders.length }}条</span>
              </div>
            </div>
            <input 
              v-model="searchKeyword" 
              type="text" 
              placeholder="搜索订单号/客户名" 
              class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
            />
          </div>

          <!-- 批量操作栏（仅待下单Tab显示） -->
          <div v-if="orderListTab === 'pending'" class="px-4 py-2 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
            <label class="flex items-center gap-2 text-sm text-slate-600 cursor-pointer">
              <input 
                type="checkbox" 
                :checked="selectedOrders.length === filteredOrders.length && filteredOrders.length > 0"
                @change="toggleSelectAll"
                class="rounded border-slate-300 text-blue-600 focus:ring-blue-500"
              />
              <span>全选</span>
            </label>
            <span class="text-xs text-slate-500">
              已选 <span class="font-bold text-blue-600">{{ selectedOrders.length }}</span> / {{ filteredOrders.length }} 单
            </span>
          </div>

          <!-- 待下单订单列表 -->
          <div v-if="orderListTab === 'pending'" class="overflow-x-auto" style="max-height: 480px;">
            <table class="w-full text-xs text-left">
              <thead class="bg-slate-100 text-slate-500 font-medium border-b border-slate-200 sticky top-0 z-10">
                <tr class="h-[36px]">
                  <th class="px-2 whitespace-nowrap font-medium w-8"></th>
                  <th class="px-3 whitespace-nowrap font-medium">订单号</th>
                  <th class="px-3 whitespace-nowrap font-medium">客户</th>
                  <th class="px-3 whitespace-nowrap font-medium">店铺</th>
                  <th class="px-3 whitespace-nowrap font-medium">运营</th>
                  <th class="px-3 whitespace-nowrap font-medium">国家</th>
                  <th class="px-3 whitespace-nowrap font-medium">操作</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100 bg-white">
                <tr 
                  v-for="order in filteredOrders" 
                  :key="order.id" 
                  @click="selectOrder(order)"
                  :class="['hover:bg-slate-50 transition-colors h-[44px] cursor-pointer', selectedOrder?.id === order.id ? 'bg-blue-50' : '']"
                >
                  <td class="px-2 whitespace-nowrap" @click.stop>
                    <input 
                      type="checkbox" 
                      :checked="isSelected(order.id)"
                      @change="toggleSelect(order)"
                      class="rounded border-slate-300 text-blue-600 focus:ring-blue-500"
                    />
                  </td>
                  <td class="px-3 whitespace-nowrap font-medium text-slate-700">{{ order.etsy_order_id || order.id }}</td>
                  <td class="px-3 whitespace-nowrap text-slate-600">{{ order.customer_name }}</td>
                  <td class="px-3 whitespace-nowrap text-slate-500 text-[11px]">{{ order.shops?.code || order.shop_code || '-' }}</td>
                  <td class="px-3 whitespace-nowrap text-slate-500 text-[11px]">{{ order.shops?.operator || order.operator || '-' }}</td>
                  <td class="px-3 whitespace-nowrap text-slate-600">{{ order.country || '-' }}</td>
                  <td class="px-3 whitespace-nowrap">
                    <button 
                      @click.stop="selectOrder(order)" 
                      :class="['px-3 py-1 rounded text-[10px] transition-colors', selectedOrder?.id === order.id ? 'bg-blue-600 text-white' : 'bg-slate-100 text-slate-600 hover:bg-slate-200']"
                    >
                      {{ selectedOrder?.id === order.id ? '当前' : '选择' }}
                    </button>
                  </td>
                </tr>
                <tr v-if="filteredOrders.length === 0" class="h-[60px]">
                  <td colspan="7" class="px-3 text-center text-slate-400 text-sm">暂无待下单订单</td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- 已下单订单列表 -->
          <div v-if="orderListTab === 'shipped'" class="overflow-x-auto" style="max-height: 480px;">
            <table class="w-full text-xs text-left">
              <thead class="bg-slate-100 text-slate-500 font-medium border-b border-slate-200 sticky top-0 z-10">
                <tr class="h-[36px]">
                  <th class="px-3 whitespace-nowrap font-medium">订单号</th>
                  <th class="px-3 whitespace-nowrap font-medium">客户</th>
                  <th class="px-3 whitespace-nowrap font-medium">店铺</th>
                  <th class="px-3 whitespace-nowrap font-medium">运营</th>
                  <th class="px-3 whitespace-nowrap font-medium">国家</th>
                  <th class="px-3 whitespace-nowrap font-medium">物流单号</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100 bg-white">
                <tr 
                  v-for="order in filteredShippedOrders" 
                  :key="order.id" 
                  class="hover:bg-slate-50 transition-colors h-[44px]"
                >
                  <td class="px-3 whitespace-nowrap font-medium text-slate-700">{{ order.etsy_order_id || order.id }}</td>
                  <td class="px-3 whitespace-nowrap text-slate-600">{{ order.customer_name }}</td>
                  <td class="px-3 whitespace-nowrap text-slate-500 text-[11px]">{{ order.shops?.code || order.shop_code || '-' }}</td>
                  <td class="px-3 whitespace-nowrap text-slate-500 text-[11px]">{{ order.shops?.operator || order.operator || '-' }}</td>
                  <td class="px-3 whitespace-nowrap text-slate-600">{{ order.country || '-' }}</td>
                  <td class="px-3 whitespace-nowrap font-mono text-green-600 text-[11px]">{{ order.logistics?.[0]?.tracking_number || '-' }}</td>
                </tr>
                <tr v-if="filteredShippedOrders.length === 0" class="h-[60px]">
                  <td colspan="6" class="px-3 text-center text-slate-400 text-sm">暂无已下单记录</td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- 批量下单入口 -->
          <div v-if="selectedOrders.length > 1" class="px-4 py-3 bg-purple-50 border-t border-purple-200">
            <div class="flex items-center justify-between">
              <span class="text-sm text-purple-700 font-medium">
                已选 {{ selectedOrders.length }} 单
              </span>
              <button 
                @click="createBatchOrder" 
                :disabled="submittingBatch"
                class="bg-purple-600 hover:bg-purple-700 disabled:bg-purple-400 text-white px-4 py-1.5 rounded-lg text-sm font-medium flex items-center gap-2 transition-colors"
              >
                <svg v-if="submittingBatch" class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                批量下单 ({{ selectedOrders.length }}单)
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 燕文物流/云途物流Tab内容已隐藏（暂未接入） -->
  </div>
</template>

<script setup>
import { ref, computed, onMounted, reactive, watch } from 'vue'
import { useRoute } from 'vue-router'
import supabase from '../../utils/supabase'

// 路由
const route = useRoute()

// API配置
const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

// 状态
const activeTab = ref('4px')
const orderListTab = ref('pending') // 右侧Tab：pending=待下单 / shipped=已下单
const loading = ref(false)
const demoMode = ref(false)
const orders = ref([])          // 待下单（confirmed）
const shippedOrders = ref([])   // 已下单（shipped）
const selectedOrder = ref(null)
const selectedOrders = ref([]) // 批量选择的订单
const searchKeyword = ref('')
const showAdvanced = ref(false)
// 物流渠道固定为A1（4PX标准直发）
const channels = ref([
  { code: 'A1', name: '4PX标准直发(A1) (7-15天)' }
])
const loadingChannels = ref(false)
const submitting = ref(false)
const submittingBatch = ref(false)
const batchProgress = ref(0)
const showResult = ref(false)
const orderResult = ref(null)
const batchResults = ref([]) // 批量下单结果
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
  channel_code: 'A1',
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

// 批量模式判断：选中2单及以上时进入批量模式
const isBatchMode = computed(() => selectedOrders.value.length >= 2)

// 运营筛选
const activeAccount = ref('all')

// 批量列表中当前展开的订单ID（点击展开订单详情）
const expandedBatchOrderId = ref(null)
const toggleBatchExpand = (orderId) => {
  expandedBatchOrderId.value = expandedBatchOrderId.value === orderId ? null : orderId
}

// 取消批量模式（清空所有勾选）
const cancelBatch = () => {
  selectedOrders.value = []
  selectedOrder.value = null
  expandedBatchOrderId.value = null
  batchAddressMap.value = {}
}

// 批量地址映射表（key=order.id，value={ready,data}）
const batchAddressMap = ref({})

// 批量就绪数量
const batchReadyCount = computed(() => 
  Object.values(batchAddressMap.value).filter(v => v?.ready).length
)

// 当前Tab对应的订单列表
const currentTabOrders = computed(() => 
  orderListTab.value === 'pending' ? orders.value : shippedOrders.value
)

const filteredOrders = computed(() => {
  let list = orders.value
  // 按运营筛选
  if (activeAccount.value !== 'all') {
    list = list.filter(o => o.operator === activeAccount.value || o.shops?.operator === activeAccount.value)
  }
  // 按关键词搜索
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    list = list.filter(order => 
      (order.etsy_order_id || order.id || '').toLowerCase().includes(keyword) || 
      (order.customer_name || '').toLowerCase().includes(keyword)
    )
  }
  return list
})

const filteredShippedOrders = computed(() => {
  let list = shippedOrders.value
  // 按运营筛选
  if (activeAccount.value !== 'all') {
    list = list.filter(o => o.operator === activeAccount.value || o.shops?.operator === activeAccount.value)
  }
  // 按关键词搜索
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    list = list.filter(order => 
      (order.etsy_order_id || order.id || '').toLowerCase().includes(keyword) || 
      (order.customer_name || '').toLowerCase().includes(keyword)
    )
  }
  return list
})

// 生成随机美国电话号码（隐私保护，4PX必填）
const generateFakePhone = () => {
  // 美国格式: +1 (区号3位) (前缀3位) (后缀4位)
  const areaCodes = ['202', '212', '213', '312', '415', '617', '702', '818', '305', '404']
  const areaCode = areaCodes[Math.floor(Math.random() * areaCodes.length)]
  const prefix = Math.floor(Math.random() * 900 + 100).toString() // 100-999
  const suffix = Math.floor(Math.random() * 9000 + 1000).toString() // 1000-9999
  return `+1${areaCode}${prefix}${suffix}`
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
    // 注意：由于orders表有两个外键指向sku_mapping(sku_id和matched_sku_id)，
    // 必须明确指定使用哪个外键关系，否则Supabase会报错
    const { data, error } = await supabase
      .from('orders')
      .select('*, sku_mapping!orders_sku_id_fkey(*)')
      .in('status', ['pending', 'confirmed'])
      .order('created_at', { ascending: false })
    
    if (error) throw error
    
    if (data && data.length > 0) {
      orders.value = data
      console.log('✅ 物流下单订单加载成功:', data.length, '条')
      // 调试：打印第一条订单的所有字段
      console.log('📦 第一条订单数据:', JSON.stringify(data[0], null, 2))
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

// 加载已下单订单列表（status=shipped）
const loadShippedOrders = async () => {
  try {
    const { data, error } = await supabase
      .from('orders')
      .select('*, sku_mapping!orders_sku_id_fkey(*)')
      .eq('status', 'shipped')
      .order('created_at', { ascending: false })
      .limit(100)
    
    if (error) throw error
    shippedOrders.value = data || []
    console.log('✅ 已下单订单加载成功:', shippedOrders.value.length, '条')
  } catch (e) {
    console.error('❌ 已下单订单加载失败:', e)
    shippedOrders.value = []
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
      // 物流表数据只覆盖空值，保留订单表的数据（订单表数据更准确）
      if (!form.recipient_name) form.recipient_name = data.recipient_name || ''
      if (!form.recipient_phone || form.recipient_phone.startsWith('+1')) form.recipient_phone = data.phone || generateFakePhone()
      if (!form.recipient_email) form.recipient_email = data.email || ''
      if (!form.recipient_street) form.recipient_street = data.street_address || ''
      if (!form.recipient_city) form.recipient_city = data.city || ''
      if (!form.recipient_state) form.recipient_state = data.state_code || ''
      if (!form.recipient_postcode) form.recipient_postcode = data.postal_code || ''
      // 国家只在空值时才从物流表读取
      if (!form.recipient_country) {
        const countryMap = {
          'Australia': 'AU', 'AU': 'AU',
          'United States': 'US', 'US': 'US', 'USA': 'US',
          'Canada': 'CA', 'CA': 'CA',
          'United Kingdom': 'GB', 'GB': 'GB', 'UK': 'GB',
          'Germany': 'DE', 'DE': 'DE',
          'France': 'FR', 'FR': 'FR',
          'Japan': 'JP', 'JP': 'JP',
          'Korea': 'KR', 'KR': 'KR', 'South Korea': 'KR',
          'Singapore': 'SG', 'SG': 'SG',
          'New Zealand': 'NZ', 'NZ': 'NZ'
        }
        form.recipient_country = countryMap[data.country] || data.country || ''
      }
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
      form.channel_code = channels.value[0]?.code || 'A1'
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
  batchResults.value = []
  
  // 自动填充收件人信息（从orders表的shipping_*字段）
  // 优先使用 shipping_name，其次使用 customer_name
  form.recipient_name = order.shipping_name || order.customer_name || ''
  form.recipient_phone = generateFakePhone() // 4PX必填，自动生成隐私号码
  form.recipient_email = order.customer_email || ''
  
  // 从orders表的shipping_*字段自动填充地址
  form.recipient_street = order.shipping_address_line1 || ''
  form.recipient_city = order.shipping_city || ''
  form.recipient_state = order.shipping_state || ''
  form.recipient_postcode = order.shipping_zip || ''
  
  // 国家名称转代码（下拉框需要代码值）
  const countryMap = {
    'Australia': 'AU', 'AU': 'AU',
    'United States': 'US', 'US': 'US', 'USA': 'US',
    'Canada': 'CA', 'CA': 'CA',
    'United Kingdom': 'GB', 'GB': 'GB', 'UK': 'GB',
    'Germany': 'DE', 'DE': 'DE',
    'France': 'FR', 'FR': 'FR',
    'Japan': 'JP', 'JP': 'JP',
    'Korea': 'KR', 'KR': 'KR', 'South Korea': 'KR',
    'Singapore': 'SG', 'SG': 'SG',
    'New Zealand': 'NZ', 'NZ': 'NZ'
  }
  const countryValue = order.shipping_country || order.country || ''
  form.recipient_country = countryMap[countryValue] || countryValue
  
  // 申报价值
  form.declare_value = order.total_amount || 9.99
  
  // 重量自动从order.weight_g或sku_mapping.weight_g读取（单位：克）
  if (order.weight_g) {
    form.weight = order.weight_g
  } else if (order.sku_mapping && order.sku_mapping.weight_g) {
    form.weight = order.sku_mapping.weight_g
  } else {
    form.weight = 30 // 默认30g
  }
  
  // 尝试加载物流表数据（可能有已存在的物流信息）
  if (order.id && !demoMode.value) {
    await loadLogistics(order.id)
  }
  
  // 物流渠道固定使用A1（4PX标准直发）
  form.channel_code = 'A1'
}

// 国家变化时（暂不动态查询渠道，固定使用PX）
const onCountryChange = () => {
  // 当前只支持PX渠道，无需动态加载
  console.log('国家切换为:', form.recipient_country)
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
  selectedOrders.value = []
  showResult.value = false
  orderResult.value = null
  batchResults.value = []
}

// ==================== 批量操作 ====================

// 判断是否已选中
const isSelected = (orderId) => {
  return selectedOrders.value.some(o => o.id === orderId)
}

// 切换选择
const toggleSelect = (order) => {
  const index = selectedOrders.value.findIndex(o => o.id === order.id)
  if (index > -1) {
    selectedOrders.value.splice(index, 1)
    // 移除时清理地址映射
    delete batchAddressMap.value[order.id]
  } else {
    selectedOrders.value.push(order)
    // 加入时自动加载地址
    loadBatchAddress(order)
  }
  // 同步更新当前选中订单
  if (selectedOrders.value.length === 1) {
    selectedOrder.value = selectedOrders.value[0]
  } else if (selectedOrders.value.length === 0) {
    selectedOrder.value = null
  }
}

// 全选/取消全选
const toggleSelectAll = () => {
  if (selectedOrders.value.length === filteredOrders.value.length) {
    selectedOrders.value = []
    selectedOrder.value = null
    batchAddressMap.value = {}
  } else {
    selectedOrders.value = [...filteredOrders.value]
    if (selectedOrders.value.length > 0) {
      selectedOrder.value = selectedOrders.value[0]
    }
    // 批量加载所有地址
    selectedOrders.value.forEach(o => loadBatchAddress(o))
  }
}

// 从批量列表移除（红×按钮）
const removeFromBatch = (order) => {
  const index = selectedOrders.value.findIndex(o => o.id === order.id)
  if (index > -1) selectedOrders.value.splice(index, 1)
  delete batchAddressMap.value[order.id]
  if (selectedOrders.value.length === 1) {
    selectedOrder.value = selectedOrders.value[0]
  } else if (selectedOrders.value.length === 0) {
    selectedOrder.value = null
  }
}

// 为批量列表中的每条订单加载地址（从订单本身数据读取）
const loadBatchAddress = (order) => {
  const street = order.shipping_address_line1 || ''
  const city   = order.shipping_city || ''
  const state  = order.shipping_state || ''
  const zip    = order.shipping_zip || ''
  const country = order.shipping_country || order.country || ''
  const name   = order.shipping_name || order.customer_name || ''
  const ready  = !!(street && city && zip && country)
  batchAddressMap.value = {
    ...batchAddressMap.value,
    [order.id]: { ready, name, street, city, state, zip, country }
  }
}

// 获取订单的物流表单数据
const getOrderFormData = (order) => {
  // 国家名称转代码
  const countryMap = {
    'Australia': 'AU', 'AU': 'AU',
    'United States': 'US', 'US': 'US', 'USA': 'US',
    'Canada': 'CA', 'CA': 'CA',
    'United Kingdom': 'GB', 'GB': 'GB', 'UK': 'GB',
    'Germany': 'DE', 'DE': 'DE',
    'France': 'FR', 'FR': 'FR',
    'Japan': 'JP', 'JP': 'JP',
    'Korea': 'KR', 'KR': 'KR', 'South Korea': 'KR',
    'Singapore': 'SG', 'SG': 'SG',
    'New Zealand': 'NZ', 'NZ': 'NZ'
  }
  const countryValue = order.shipping_country || order.country || ''
  
  return {
    order_id: order.id,
    logistics_product_code: 'PX',
    recipient_name: order.shipping_name || order.customer_name || '',
    recipient_phone: generateFakePhone(),
    recipient_email: order.customer_email || '',
    recipient_street: order.shipping_address_line1 || '',
    recipient_city: order.shipping_city || '',
    recipient_state: order.shipping_state || '',
    recipient_postcode: order.shipping_zip || '',
    recipient_country: countryMap[countryValue] || countryValue,
    weight_kg: (order.weight_g || order.sku_mapping?.weight_g || 30) / 1000,
    declare_value: order.total_amount || 9.99,
    declare_currency: 'USD'
  }
}

// 批量创建物流订单
const createBatchOrder = async () => {
  if (selectedOrders.value.length === 0) {
    alert('请先选择订单')
    return
  }
  
  submittingBatch.value = true
  batchProgress.value = 0
  batchResults.value = []
  
  const results = []
  
  for (let i = 0; i < selectedOrders.value.length; i++) {
    const order = selectedOrders.value[i]
    batchProgress.value = i + 1
    
    try {
      const formData = getOrderFormData(order)
      
      const res = await fetch(`${API_BASE}/api/shipping/create-order`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      })
      
      const data = await res.json()
      
      if (data.success) {
        results.push({
          orderId: order.id,
          etsyOrderId: order.etsy_order_id || order.id,
          success: true,
          trackingNumber: data.data?.tracking_number || data.data?.fpx_tracking_no,
          labelUrl: data.data?.label_url
        })
        todayShippedCount.value++
      } else {
        results.push({
          orderId: order.id,
          etsyOrderId: order.etsy_order_id || order.id,
          success: false,
          error: data.message || data.detail || '未知错误'
        })
      }
    } catch (e) {
      results.push({
        orderId: order.id,
        etsyOrderId: order.etsy_order_id || order.id,
        success: false,
        error: e.message
      })
    }
  }
  
  batchResults.value = results
  showResult.value = true
  
  // 从列表中移除成功的订单
  const successIds = results.filter(r => r.success).map(r => r.orderId)
  orders.value = orders.value.filter(o => !successIds.includes(o.id))
  selectedOrders.value = selectedOrders.value.filter(o => !successIds.includes(o.id))
  
  const successCount = results.filter(r => r.success).length
  const failCount = results.filter(r => !r.success).length
  
  if (failCount === 0) {
    alert(`✅ 批量下单完成！成功 ${successCount} 单`)
  } else {
    alert(`⚠️ 批量下单完成：成功 ${successCount} 单，失败 ${failCount} 单`)
  }
  
  submittingBatch.value = false
}

// 下载所有面单（批量）
const downloadAllLabels = () => {
  const successResults = batchResults.value.filter(r => r.success && r.labelUrl)
  successResults.forEach((result, index) => {
    setTimeout(() => {
      window.open(result.labelUrl, '_blank')
    }, index * 500)
  })
}

// 切换Tab时加载对应数据
watch(orderListTab, (newTab) => {
  if (newTab === 'shipped' && shippedOrders.value.length === 0) {
    loadShippedOrders()
  }
})

// 初始化
onMounted(async () => {
  await loadOrders()
  // 同步加载已下单数据
  loadShippedOrders()
  
  // 处理路由参数：从"待确认订单"页面跳转过来时自动选中订单
  const orderId = route.query.orderId
  if (orderId) {
    console.log('📍 从待确认订单跳转，订单ID:', orderId)
    // 等待订单列表加载完成后，查找并选中对应订单
    const order = orders.value.find(o => o.id === orderId || o.etsy_order_id === orderId)
    if (order) {
      console.log('✅ 自动选中订单:', order.etsy_order_id)
      await selectOrder(order)
    } else {
      console.warn('⚠️ 未找到订单:', orderId)
    }
  } else {
    // 默认自动选中第一个待下单订单
    if (filteredOrders.value.length > 0) {
      const firstOrder = filteredOrders.value[0]
      console.log('📍 默认选中第一个待下单订单:', firstOrder.etsy_order_id)
      await selectOrder(firstOrder)
    }
  }
})
</script>
