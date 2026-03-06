<template>
  <div class="bg-slate-200 min-h-[964px] min-w-max flex items-center justify-center p-8">
    <div class="flex h-[900px] w-[1480px] bg-white shadow-2xl rounded-2xl overflow-hidden shrink-0">

      <!-- 左侧导航栏-->
      <div class="w-64 bg-white border-r border-slate-200 flex flex-col h-full overflow-y-auto shrink-0">
        <div class="p-6">
          <h1 class="text-xl font-bold text-slate-800 flex items-center gap-2">
            <span class="w-2 h-6 bg-blue-600 rounded-full"></span>
            仪表盘总览
          </h1>
        </div>

        <nav class="px-4 space-y-1">
          <!-- 仪表盘总览 -->
          <button @click="$router.push('/')"
            class="w-full flex items-center justify-between px-4 py-3 rounded-xl transition-colors text-slate-600 hover:bg-slate-50">
            <div class="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/></svg>
              <span class="font-medium">仪表盘总览</span>
            </div>
          </button>
          <!-- 待确认订单-->
          <button @click="$router.push('/pending')"
            class="w-full flex items-center justify-between px-4 py-3 rounded-xl transition-colors text-slate-600 hover:bg-slate-50">
            <div class="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="8" height="4" x="8" y="2" rx="1" ry="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="M12 11h4"/><path d="M12 16h4"/><path d="M8 11h.01"/><path d="M8 16h.01"/></svg>
              <span class="font-medium">待确认订单</span>
            </div>
            <span class="text-xs font-bold px-2 py-0.5 rounded-full bg-slate-100 text-slate-600">32</span>
          </button>
          <!-- 生产中订单Active -->
          <button class="w-full flex items-center justify-between px-4 py-3 rounded-xl transition-colors bg-blue-50 text-blue-600">
            <div class="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 12-8.5 8.5c-.83.83-2.17.83-3 0 0 0 0 0 0 0a2.12 2.12 0 0 1 0-3L12 9"/><path d="M17.64 15 22 10.64"/><path d="m20.91 11.7-1.25-1.25c-.6-.6-.93-1.4-.93-2.25V7.86c0-.55-.45-1-1-1H14.5c-.85 0-1.65-.33-2.25-.93L11 4.71"/><path d="M5.8 5.81a2.2 2.2 0 0 1 3.1 0l1.3 1.3"/></svg>
              <span class="font-medium">生产中订单</span>
            </div>
            <span class="text-xs font-bold px-2 py-0.5 rounded-full bg-blue-200 text-blue-700">{{ producingCount || 0 }}</span>
          </button>
          <!-- 已完成订单-->
          <button @click="$router.push('/completed')"
            class="w-full flex items-center justify-between px-4 py-3 rounded-xl transition-colors text-slate-600 hover:bg-slate-50">
            <div class="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/></svg>
              <span class="font-medium">已完成订单</span>
            </div>
          </button>
          <!-- 物流追踪 -->
          <button @click="$router.push('/logistics')"
            class="w-full flex items-center justify-between px-4 py-3 rounded-xl transition-colors text-slate-600 hover:bg-slate-50">
            <div class="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H9"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.624l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/></svg>
              <span class="font-medium">物流追踪</span>
            </div>
          </button>
          <!-- 邮件模板 -->
          <button @click="$router.push('/email')"
            class="w-full flex items-center justify-between px-4 py-3 rounded-xl transition-colors text-slate-600 hover:bg-slate-50">
            <div class="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
              <span class="font-medium">邮件模板</span>
            </div>
          </button>
        </nav>

        <!-- 统计卡片 2×2 -->
        <div class="p-4 mt-4">
          <div class="grid grid-cols-2 gap-3">
            <div class="bg-white border border-slate-200 rounded-xl p-3 shadow-sm flex flex-col items-center justify-center text-center">
              <div class="relative w-20 h-20 flex items-center justify-center mb-1">
                <svg width="80" height="80" viewBox="0 0 80 80" class="absolute transform -rotate-90">
                  <circle cx="40" cy="40" r="28" stroke="#e2e8f0" stroke-width="5" fill="transparent" />
                  <circle cx="40" cy="40" r="28" stroke="#3b82f6" stroke-width="5" fill="transparent" stroke-dasharray="175.93" stroke-dashoffset="43.98" stroke-linecap="round" />
                </svg>
                <span class="text-lg font-bold z-10 text-blue-600">{{ store.orders.length }}</span>
              </div>
              <span class="text-xs font-medium text-slate-600">总订单</span>
              <span class="text-[10px] text-slate-400">本月累计</span>
            </div>
            <div class="bg-white border border-slate-200 rounded-xl p-3 shadow-sm flex flex-col items-center justify-center text-center">
              <div class="relative w-20 h-20 flex items-center justify-center mb-1">
                <svg width="80" height="80" viewBox="0 0 80 80" class="absolute transform -rotate-90">
                  <circle cx="40" cy="40" r="28" stroke="#e2e8f0" stroke-width="5" fill="transparent" />
                  <circle cx="40" cy="40" r="28" stroke="#f97316" stroke-width="5" fill="transparent" stroke-dasharray="175.93" stroke-dashoffset="131.95" stroke-linecap="round" />
                </svg>
                <span class="text-lg font-bold z-10 text-orange-600">{{ store.orders.filter(o => ['pending','effect_sent'].includes(o.status)).length }}</span>
              </div>
              <span class="text-xs font-medium text-slate-600">待确认</span>
              <span class="text-[10px] text-slate-400">需处理</span>
            </div>
            <div class="bg-white border border-slate-200 rounded-xl p-3 shadow-sm flex flex-col items-center justify-center text-center">
              <div class="relative w-20 h-20 flex items-center justify-center mb-1">
                <svg width="80" height="80" viewBox="0 0 80 80" class="absolute transform -rotate-90">
                  <circle cx="40" cy="40" r="28" stroke="#e2e8f0" stroke-width="5" fill="transparent" />
                  <circle cx="40" cy="40" r="28" stroke="#a855f7" stroke-width="5" fill="transparent" stroke-dasharray="175.93" stroke-dashoffset="144.26" stroke-linecap="round" />
                </svg>
                <span class="text-lg font-bold z-10 text-purple-600">{{ producingCount || 0 }}</span>
              </div>
              <span class="text-xs font-medium text-slate-600">生产作业</span>
              <span class="text-[10px] text-slate-400">进行中</span>
            </div>
            <div class="bg-white border border-slate-200 rounded-xl p-3 shadow-sm flex flex-col items-center justify-center text-center">
              <div class="relative w-20 h-20 flex items-center justify-center mb-1">
                <svg width="80" height="80" viewBox="0 0 80 80" class="absolute transform -rotate-90">
                  <circle cx="40" cy="40" r="28" stroke="#e2e8f0" stroke-width="5" fill="transparent" />
                  <circle cx="40" cy="40" r="28" stroke="#22c55e" stroke-width="5" fill="transparent" stroke-dasharray="175.93" stroke-dashoffset="87.96" stroke-linecap="round" />
                </svg>
                <span class="text-lg font-bold z-10 text-green-600">{{ store.orders.filter(o => o.status === 'delivered').length }}</span>
              </div>
              <span class="text-xs font-medium text-slate-600">已交付</span>
              <span class="text-[10px] text-slate-400">物流送达</span>
            </div>
          </div>
        </div>

        <!-- 最新订单列表-->
        <div class="p-4 mt-auto">
          <div class="flex items-center justify-between mb-3">
            <h3 class="text-sm font-bold text-slate-700">最新订单列表</h3>
            <span class="bg-orange-100 text-orange-600 text-xs px-2 py-0.5 rounded-full">{{ urgentCount || 0 }} 须跟进</span>
          </div>
          <div class="space-y-3">
            <div v-for="item in recentOrders" :key="item.id"
              class="bg-slate-50 p-3 rounded-lg border border-slate-100">
              <div class="flex justify-between items-start mb-1">
                <span class="text-xs font-bold text-slate-800">{{ item.id }}</span>
                <span :class="item.urgent ? 'text-orange-500' : 'text-purple-500'" class="text-[10px] font-medium">{{ item.statusLabel }}</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-xs text-slate-600">{{ item.customer }}</span>
                <span class="text-[10px] text-slate-400">{{ item.sku }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧主内容区 -->
      <div class="flex-1 bg-slate-50 p-6 overflow-y-auto h-full">
        <!-- 标题表-->
        <div class="mb-5 flex items-center gap-3">
          <h2 class="text-2xl font-bold text-slate-800">生产中订单</h2>
          <span class="bg-blue-100 text-blue-600 px-3 py-1 rounded-full text-xs font-bold">{{ producingCount || 0 }} 卡</span>
          <span v-if="urgentCount > 0" class="bg-orange-100 text-orange-600 px-3 py-1 rounded-full text-xs font-bold">⚠{{ urgentCount }} 单须跟进</span>
        </div>

        <!-- 订单表格 -->
        <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden mb-5">
          <div class="overflow-x-auto">
            <table class="w-full text-xs text-left">
              <thead class="bg-slate-50 text-slate-500 font-medium border-b border-slate-200">
                <tr class="h-[32px]">
                  <th class="px-3 whitespace-nowrap font-medium">优先级</th>
                  <th class="px-3 whitespace-nowrap font-medium">订单ID</th>
                  <th class="px-3 whitespace-nowrap font-medium">客户名称</th>
                  <th class="px-3 whitespace-nowrap font-medium">产品</th>
                  <th class="px-3 whitespace-nowrap font-medium">数量</th>
                  <th class="px-3 whitespace-nowrap font-medium">下单日期</th>
                  <th class="px-3 whitespace-nowrap font-medium">交货日期</th>
                  <th class="px-3 whitespace-nowrap font-medium">进度</th>
                  <th class="px-3 whitespace-nowrap font-medium">生产文档</th>
                  <th class="px-3 whitespace-nowrap font-medium">状态</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                <tr v-for="order in producingOrders" :key="order.id"
                  @click="selectOrder(order)"
                  :class="[
                    'h-[28px] cursor-pointer transition-colors',
                    selectedOrder?.id === order.id ? 'ring-2 ring-inset ring-blue-400 bg-blue-50' : 'hover:bg-slate-50'
                  ]">
                  <td class="px-3 whitespace-nowrap">
                    <span :class="(order.progress || 0) < 30 ? 'bg-orange-500' : 'bg-blue-400'" class="w-2 h-2 rounded-full inline-block"></span>
                  </td>
                  <td class="px-3 whitespace-nowrap font-medium text-slate-700">{{ order.etsy_order_id || order.id }}</td>
                  <td class="px-3 whitespace-nowrap text-slate-600">{{ order.customer_name }}</td>
                  <td class="px-3 whitespace-nowrap font-mono text-slate-500">{{ order.sku_mapping?.sku_code || order.sku_id }}</td>
                  <td class="px-3 whitespace-nowrap text-slate-600">{{ order.quantity }}</td>
                  <td class="px-3 whitespace-nowrap text-slate-400">{{ new Date(order.created_at).toLocaleDateString('zh-CN') }}</td>
                  <td class="px-3 whitespace-nowrap font-medium" :class="isOverdue(order) ? 'text-orange-600' : 'text-slate-500'">
                    {{ order.estimated_delivery ? new Date(order.estimated_delivery).toLocaleDateString('zh-CN', {month:'2-digit', day:'2-digit'}) : '--' }}
                    <span v-if="isOverdue(order)" class="text-orange-500"> ⚠</span>
                  </td>
                  <td class="px-3 whitespace-nowrap">
                    <div class="flex items-center gap-2">
                      <div class="w-16 h-1.5 bg-slate-100 rounded-full">
                        <div :style="{ width: (order.progress || 0) + '%' }" :class="(order.progress || 0) < 30 ? 'bg-orange-500' : 'bg-blue-500'" class="h-1.5 rounded-full"></div>
                      </div>
                      <span class="text-[10px] text-slate-400">{{ order.progress || 0 }}%</span>
                    </div>
                  </td>
                  <td class="px-3 whitespace-nowrap">
                    <span v-if="order.production_documents?.production_pdf_url" class="flex items-center gap-1 text-blue-600 hover:underline text-[10px] cursor-pointer">
                      <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/></svg>
                      查看
                    </span>
                    <span v-else class="text-[10px] text-slate-400">—</span>
                  </td>
                  <td class="px-3 whitespace-nowrap">
                    <span v-if="(order.progress || 0) < 30" class="bg-orange-100 text-orange-600 px-1.5 py-0.5 rounded text-[10px] font-bold">须跟进</span>
                    <span v-else class="bg-blue-100 text-blue-600 px-1.5 py-0.5 rounded text-[10px] font-bold">生产中</span>
                  </td>
                </tr>
                <tr v-if="producingOrders.length === 0" class="h-[28px]">
                  <td colspan="10" class="px-3 text-center text-slate-400 text-xs">暂无生产中订单</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- 订单详情面板（点击表格行展开） -->
        <div v-if="selectedOrder" class="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <div class="flex justify-between items-start mb-5">
            <div class="flex gap-4">
              <div class="w-24 h-24 bg-slate-50 rounded-lg overflow-hidden border border-slate-200 shrink-0 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" x2="12" y1="9" y2="13"/><line x1="12" x2="12.01" y1="17" y2="17"/></svg>
              </div>
              <div>
                <h3 class="text-lg font-bold text-slate-800 flex items-center gap-2">
                  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 12-8.5 8.5c-.83.83-2.17.83-3 0a2.12 2.12 0 0 1 0-3L12 9"/><path d="M17.64 15 22 10.64"/></svg>
                  {{ selectedOrder.etsy_order_id || selectedOrder.id }} · 生产中订单
                </h3>
                <div class="grid grid-cols-2 gap-x-8 gap-y-1 text-sm text-slate-600 mt-2">
                  <div class="flex"><span class="text-slate-400 w-16">客户:</span> {{ selectedOrder.customer_name }}</div>
                  <div class="flex"><span class="text-slate-400 w-16">产品:</span> {{ selectedOrder.sku_mapping?.sku_code || selectedOrder.sku_id }}</div>
                  <div class="flex"><span class="text-slate-400 w-16">工艺:</span> {{ selectedOrder.sku_mapping?.craft || '标准' }}</div>
                  <div class="flex"><span class="text-slate-400 w-16">正面:</span> {{ selectedOrder.front_text || '—' }}</div>
                  <div class="flex"><span class="text-slate-400 w-16">背面:</span> {{ selectedOrder.back_text || '—' }}</div>
                  <div class="flex"><span class="text-slate-400 w-16">数量:</span> {{ selectedOrder.quantity }} 付</div>
                </div>
              </div>
            </div>
            <div class="flex flex-col items-end gap-2">
              <span v-if="(selectedOrder.progress || 0) < 30 || isOverdue(selectedOrder)" class="bg-orange-100 text-orange-600 px-3 py-1.5 rounded-lg text-sm font-bold">⚠ {{ isOverdue(selectedOrder) ? '已逾期' : '须跟进' }}</span>
              <span v-else class="bg-blue-100 text-blue-600 px-3 py-1.5 rounded-lg text-sm font-bold">生产中</span>
              <div class="text-right text-sm">
                <div class="flex justify-end"><span class="text-slate-400 mr-2">下单时间:</span> {{ new Date(selectedOrder.created_at).toLocaleDateString('zh-CN') }}</div>
                <div class="flex justify-end text-slate-500 font-medium">
                  <span class="text-slate-400 mr-2 font-normal">交货时间:</span>
                  {{ selectedOrder.estimated_delivery ? new Date(selectedOrder.estimated_delivery).toLocaleDateString('zh-CN') : '待定' }}
                  <span v-if="isOverdue(selectedOrder)" class="text-orange-600 ml-1">已逾期</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 生产进度条 -->
          <div class="bg-slate-50 border border-slate-200 rounded-xl p-4 mb-4">
            <div class="flex items-center justify-between mb-3">
              <span class="text-sm font-bold text-slate-700">生产进度</span>
              <span class="bg-slate-100 text-slate-600 px-3 py-0.5 rounded-full text-xs font-bold">
                生产中· <span :class="(selectedOrder.progress || 0) < 30 || isOverdue(selectedOrder) ? 'text-orange-600' : 'text-blue-600'">{{ (selectedOrder.progress || 0) < 30 || isOverdue(selectedOrder) ? (isOverdue(selectedOrder) ? '已逾期' : '须跟进') : '正常' }}</span>
              </span>
            </div>
            <div class="w-full h-2 bg-slate-100 rounded-full mb-2">
              <div :style="{ width: (selectedOrder.progress || 0) + '%' }"
                :class="(selectedOrder.progress || 0) < 30 || isOverdue(selectedOrder) ? 'bg-orange-500' : 'bg-blue-500'"
                class="h-2 rounded-full transition-all duration-300"></div>
            </div>
            <div class="flex justify-between text-xs text-slate-400">
              <span>{{ selectedOrder.progress || 0 }}% 已完成</span>
              <span v-if="isOverdue(selectedOrder)">交货时间 {{ new Date(selectedOrder.estimated_delivery).toLocaleDateString('zh-CN', {month:'2-digit', day:'2-digit'}) }} <span class="text-orange-600 font-medium">已逾期</span> — 请立即联系工厂跟进进度</span>
              <span v-else-if="(selectedOrder.progress || 0) < 30">进度较慢，请关注</span>
              <span v-else>预计按时交货</span>
            </div>
          </div>

          <!-- 生产文档 -->
          <div class="border border-slate-200 rounded-xl p-4 mb-4">
            <div class="flex items-center justify-between mb-3">
              <span class="text-sm font-bold text-slate-700 flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/></svg>
                生产文档
              </span>
              <div v-if="selectedOrder.production_documents?.production_pdf_url" class="flex gap-2">
                <button class="bg-slate-800 hover:bg-slate-900 text-white px-3 py-1 rounded-lg text-xs font-medium transition-colors">在新标签页查看</button>
                <button class="bg-white border border-slate-200 hover:bg-slate-50 text-slate-600 px-3 py-1 rounded-lg text-xs font-medium transition-colors">下载 PDF</button>
              </div>
            </div>
            <div class="bg-slate-100 rounded-lg h-[120px] flex items-center justify-center text-slate-400 text-sm">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-2"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/></svg>
              <span v-if="selectedOrder.production_documents?.production_pdf_url">{{ selectedOrder.etsy_order_id || selectedOrder.id }}_生产文档.pdf</span>
              <span v-else class="text-slate-400">暂无生产文档</span>
            </div>
          </div>

          <!-- 操作按钮 -->
          <div class="flex justify-center gap-4 mt-2">
            <button @click="openPdfDoc" :disabled="pdfLoading" :class="pdfLoading ? 'bg-slate-400 cursor-not-allowed' : 'bg-slate-600 hover:bg-slate-700'" class="text-white px-5 py-2.5 rounded-lg text-sm font-medium flex items-center gap-2 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H9"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.624l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/></svg>
              {{ pdfLoading ? '生成中...' : selectedOrder?.production_pdf_url ? '查看生产文档' : '生成生产文档' }}
            </button>
            <button @click="copyShipEmail" class="bg-white border border-slate-200 hover:bg-slate-50 text-slate-600 px-5 py-2.5 rounded-lg text-sm font-medium flex items-center gap-2 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
              发货通知邮件
            </button>
            <button @click="markDelivered" class="bg-green-600 hover:bg-green-700 text-white px-5 py-2.5 rounded-lg text-sm font-medium flex items-center gap-2 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/></svg>
              标记完成
            </button>
          </div>
        </div>

        <!-- 未选中时的提示 -->
        <div v-else class="bg-white rounded-xl shadow-sm border border-slate-200 p-12 flex flex-col items-center justify-center text-slate-400">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#cbd5e1" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="mb-3"><path d="m15 12-8.5 8.5c-.83.83-2.17.83-3 0a2.12 2.12 0 0 1 0-3L12 9"/><path d="M17.64 15 22 10.64"/></svg>
          <p class="text-sm">点击上方订单行查看详情</p>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useOrderStore } from '../../stores/orderStore'

const store = useOrderStore()
const selectedOrder = ref(null)

// 页面加载时获取数据
onMounted(() => {
  store.getProducingOrders()
})

// 计算属性：生产中订单列表
const producingOrders = computed(() => 
  store.orders.filter(o => o.status === 'producing')
)

// 计算属性：生产中订单数量
const producingCount = computed(() => producingOrders.value.length)

// 计算属性：须跟进订单（进度低于30%或逾期）
const urgentCount = computed(() => 
  producingOrders.value.filter(o => (o.progress || 0) < 30).length
)

// 侧边栏最新订单（取前3条生产中订单）
const recentOrders = computed(() => 
  producingOrders.value.slice(0, 3).map(order => ({
    id: order.etsy_order_id || order.id,
    customer: order.customer_name,
    sku: order.sku_mapping?.sku_code || order.sku_id,
    urgent: (order.progress || 0) < 30,
    statusLabel: (order.progress || 0) < 30 ? '⚠须跟进' : '生产中'
  }))
)

// 选择订单
function selectOrder(order) {
  selectedOrder.value = order
}

// 判断是否递期（estimated_delivery < 今天）
function isOverdue(order) {
  if (!order.estimated_delivery) return false
  return new Date(order.estimated_delivery) < new Date()
}

// PDF 生成加载状态
const pdfLoading = ref(false)

// 「生成生产文档」：调用后端 API 生成 PDF 并上传到 Supabase Storage
async function openPdfDoc() {
  if (!selectedOrder.value) {
    alert('请先选择一条订单')
    return
  }

  // 如果已有 PDF URL，直接打开
  const existingUrl = selectedOrder.value.production_pdf_url
  if (existingUrl) {
    window.open(existingUrl, '_blank')
    return
  }

  // 否则调用后端生成并上传
  pdfLoading.value = true
  try {
    const result = await store.generateProductionPdf(selectedOrder.value.id)
    if (result?.production_pdf_url) {
      // 更新当前选中订单的本地缓存
      selectedOrder.value = { ...selectedOrder.value, production_pdf_url: result.production_pdf_url }
      alert('✅ 生产文档已生成！正在打开PDF...')
      window.open(result.production_pdf_url, '_blank')
    } else {
      alert('❌ PDF 生成失败，请确认后端服务已启动')
    }
  } catch (e) {
    alert('❌ 生成失败：' + e.message + '\n请确认后端服务已启动 (uvicorn src.api.main:app --port 8000)')
  } finally {
    pdfLoading.value = false
  }
}

// 「发货通知邮件」：复制发货邮件内容
async function copyShipEmail() {
  if (!selectedOrder.value) return
  const name = selectedOrder.value.customer_name?.split(' ')[0] || '客户'
  const text = `Dear ${name},\n\nYour order has been shipped! We will send you the tracking number shortly.\n\nBest regards,\nCustomer Service`
  try {
    await navigator.clipboard.writeText(text)
    alert('✅ 发货邮件已复制到剪贴板！')
  } catch (e) {
    alert('复制失败，请手动复制')
  }
}

// 「标记完成」：将订单状态改为 delivered
async function markDelivered() {
  if (!selectedOrder.value) return
  if (!confirm(`确认将订单 ${selectedOrder.value.etsy_order_id || selectedOrder.value.id} 标记为已完成？`)) return
  try {
    await store.updateOrderStatus(selectedOrder.value.id, 'delivered')
    selectedOrder.value = null
    alert('✅ 订单已标记为已完成！')
  } catch (e) {
    alert('❌ 操作失败：' + e.message)
  }
}
</script>
