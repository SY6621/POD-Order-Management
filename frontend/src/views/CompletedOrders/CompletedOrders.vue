<template>
  <div class="bg-slate-200 min-h-[964px] min-w-max flex items-center justify-center p-8">
    <div class="flex h-[900px] w-[1480px] bg-white shadow-2xl rounded-2xl overflow-hidden shrink-0">

      <!-- 左侧导航栏 -->
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
          <!-- 待确认订单 -->
          <button @click="$router.push('/pending')"
            class="w-full flex items-center justify-between px-4 py-3 rounded-xl transition-colors text-slate-600 hover:bg-slate-50">
            <div class="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="8" height="4" x="8" y="2" rx="1" ry="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="M12 11h4"/><path d="M12 16h4"/><path d="M8 11h.01"/><path d="M8 16h.01"/></svg>
              <span class="font-medium">待确认订单</span>
            </div>
            <span class="text-xs font-bold px-2 py-0.5 rounded-full bg-slate-100 text-slate-600">{{ pendingCount }}</span>
          </button>
          <!-- 生产中订单 -->
          <button @click="$router.push('/production')"
            class="w-full flex items-center justify-between px-4 py-3 rounded-xl transition-colors text-slate-600 hover:bg-slate-50">
            <div class="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 12-8.5 8.5c-.83.83-2.17.83-3 0 0 0 0 0 0 0a2.12 2.12 0 0 1 0-3L12 9"/><path d="M17.64 15 22 10.64"/><path d="m20.91 11.7-1.25-1.25c-.6-.6-.93-1.4-.93-2.25V7.86c0-.55-.45-1-1-1H14.5c-.85 0-1.65-.33-2.25-.93L11 4.71"/><path d="M5.8 5.81a2.2 2.2 0 0 1 3.1 0l1.3 1.3"/></svg>
              <span class="font-medium">生产中订单</span>
            </div>
            <span class="text-xs font-bold px-2 py-0.5 rounded-full bg-slate-100 text-slate-600">{{ producingCount }}</span>
          </button>
          <!-- 已完成订单 Active -->
          <button class="w-full flex items-center justify-between px-4 py-3 rounded-xl transition-colors bg-green-50 text-green-700">
            <div class="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#15803d" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/></svg>
              <span class="font-medium">已完成订单</span>
            </div>
            <span class="text-xs font-bold px-2 py-0.5 rounded-full bg-green-200 text-green-700">{{ completedCount }}</span>
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
                  <circle cx="40" cy="40" r="28" stroke="#3b82f6" stroke-width="5" fill="transparent" stroke-dasharray="175.93" :stroke-dashoffset="totalDashOffset" stroke-linecap="round" />
                </svg>
                <span class="text-lg font-bold z-10 text-blue-600">{{ totalCount }}</span>
              </div>
              <span class="text-xs font-medium text-slate-600">总订单</span>
              <span class="text-[10px] text-slate-400">全部累计</span>
            </div>
            <div class="bg-white border border-slate-200 rounded-xl p-3 shadow-sm flex flex-col items-center justify-center text-center">
              <div class="relative w-20 h-20 flex items-center justify-center mb-1">
                <svg width="80" height="80" viewBox="0 0 80 80" class="absolute transform -rotate-90">
                  <circle cx="40" cy="40" r="28" stroke="#e2e8f0" stroke-width="5" fill="transparent" />
                  <circle cx="40" cy="40" r="28" stroke="#f97316" stroke-width="5" fill="transparent" stroke-dasharray="175.93" :stroke-dashoffset="pendingDashOffset" stroke-linecap="round" />
                </svg>
                <span class="text-lg font-bold z-10 text-orange-600">{{ pendingCount }}</span>
              </div>
              <span class="text-xs font-medium text-slate-600">待确认</span>
              <span class="text-[10px] text-slate-400">须24h回复</span>
            </div>
            <div class="bg-white border border-slate-200 rounded-xl p-3 shadow-sm flex flex-col items-center justify-center text-center">
              <div class="relative w-20 h-20 flex items-center justify-center mb-1">
                <svg width="80" height="80" viewBox="0 0 80 80" class="absolute transform -rotate-90">
                  <circle cx="40" cy="40" r="28" stroke="#e2e8f0" stroke-width="5" fill="transparent" />
                  <circle cx="40" cy="40" r="28" stroke="#a855f7" stroke-width="5" fill="transparent" stroke-dasharray="175.93" :stroke-dashoffset="producingDashOffset" stroke-linecap="round" />
                </svg>
                <span class="text-lg font-bold z-10 text-purple-600">{{ producingCount }}</span>
              </div>
              <span class="text-xs font-medium text-slate-600">生产作业</span>
              <span class="text-[10px] text-slate-400">进行中</span>
            </div>
            <div class="bg-white border border-slate-200 rounded-xl p-3 shadow-sm flex flex-col items-center justify-center text-center">
              <div class="relative w-20 h-20 flex items-center justify-center mb-1">
                <svg width="80" height="80" viewBox="0 0 80 80" class="absolute transform -rotate-90">
                  <circle cx="40" cy="40" r="28" stroke="#e2e8f0" stroke-width="5" fill="transparent" />
                  <circle cx="40" cy="40" r="28" stroke="#22c55e" stroke-width="5" fill="transparent" stroke-dasharray="175.93" :stroke-dashoffset="completedDashOffset" stroke-linecap="round" />
                </svg>
                <span class="text-lg font-bold z-10 text-green-600">{{ completedCount }}</span>
              </div>
              <span class="text-xs font-medium text-slate-600">已交付</span>
              <span class="text-[10px] text-slate-400">物流送达</span>
            </div>
          </div>
        </div>

        <!-- 最近完成列表 -->
        <div class="p-4 mt-auto">
          <div class="flex items-center justify-between mb-3">
            <h3 class="text-sm font-bold text-slate-700">最近完成</h3>
            <span class="bg-green-100 text-green-700 text-xs px-2 py-0.5 rounded-full">共{{ completedCount }}单</span>
          </div>
          <div class="space-y-3">
            <div v-for="item in recentCompleted" :key="item.id"
              class="bg-slate-50 p-3 rounded-lg border border-slate-100">
              <div class="flex justify-between items-start mb-1">
                <span class="text-xs font-bold text-slate-800">#{{ item.etsy_order_id || item.id }}</span>
                <span class="text-green-600 text-[10px] font-medium">已送达</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-xs text-slate-600">{{ item.customer_name || '—' }}</span>
                <span class="text-[10px] text-slate-400">{{ item.sku_mapping?.sku_code || item.sku_id || '—' }}</span>
              </div>
            </div>
            <div v-if="recentCompleted.length === 0" class="text-center text-xs text-slate-400 py-4">暂无完成订单</div>
          </div>
        </div>
      </div>

      <!-- 右侧主内容区 -->
      <div class="flex-1 bg-slate-50 p-6 overflow-y-auto h-full">
        <!-- 标题栏 -->
        <div class="mb-5 flex items-center justify-between">
          <div class="flex items-center gap-3">
            <h2 class="text-2xl font-bold text-slate-800">已完成订单</h2>
            <span class="bg-green-100 text-green-700 px-3 py-1 rounded-full text-xs font-bold">共 {{ completedCount }} 单</span>
          </div>
          <!-- 统计数字行 -->
          <div class="flex items-center gap-4">
            <div class="text-center">
              <div class="text-lg font-bold text-green-600">{{ completedCount }}</div>
              <div class="text-[10px] text-slate-400">已完成</div>
            </div>
            <div class="w-px h-8 bg-slate-200"></div>
            <div class="text-center">
              <div class="text-lg font-bold text-blue-600">{{ deliveredCount }}</div>
              <div class="text-[10px] text-slate-400">已签收</div>
            </div>
            <div class="w-px h-8 bg-slate-200"></div>
            <div class="text-center">
              <div class="text-lg font-bold text-orange-500">{{ shippingCount }}</div>
              <div class="text-[10px] text-slate-400">运输中</div>
            </div>
            <div class="w-px h-8 bg-slate-200"></div>
            <div class="text-center">
              <div class="text-lg font-bold text-slate-600">{{ totalCount }}</div>
              <div class="text-[10px] text-slate-400">总订单</div>
            </div>
          </div>
        </div>

        <!-- 订单表格 -->
        <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden mb-6">
          <div class="overflow-x-auto">
            <table class="w-full text-xs text-left">
              <thead class="bg-slate-50 text-slate-500 font-medium border-b border-slate-200">
                <tr class="h-[32px]">
                  <th class="px-3 whitespace-nowrap font-medium">订单ID</th>
                  <th class="px-3 whitespace-nowrap font-medium">客户名称</th>
                  <th class="px-3 whitespace-nowrap font-medium">产品</th>
                  <th class="px-3 whitespace-nowrap font-medium">数量</th>
                  <th class="px-3 whitespace-nowrap font-medium">完成日期</th>
                  <th class="px-3 whitespace-nowrap font-medium">快递公司</th>
                  <th class="px-3 whitespace-nowrap font-medium">运单号</th>
                  <th class="px-3 whitespace-nowrap font-medium">物流状态</th>
                  <th class="px-3 whitespace-nowrap font-medium">已交货天数</th>
                  <th class="px-3 whitespace-nowrap font-medium">生产文档</th>
                  <th class="px-3 whitespace-nowrap font-medium">邮件追评</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                <tr v-for="order in completedOrders" :key="order.id"
                  @click="selectOrder(order)"
                  :class="[
                    'h-[28px] cursor-pointer transition-colors',
                    selectedOrder?.id === order.id ? 'ring-2 ring-inset ring-green-400 bg-green-50' : 'hover:bg-slate-50'
                  ]">
                  <td class="px-3 whitespace-nowrap font-medium text-slate-700">#{{ order.etsy_order_id || order.id }}</td>
                  <td class="px-3 whitespace-nowrap text-slate-600">{{ order.customer_name || '—' }}</td>
                  <td class="px-3 whitespace-nowrap font-mono text-slate-500">{{ order.sku_mapping?.sku_code || order.sku_id || '—' }}</td>
                  <td class="px-3 whitespace-nowrap text-slate-600">{{ order.quantity || 1 }}</td>
                  <td class="px-3 whitespace-nowrap text-slate-500">{{ formatDate(order.completed_at || order.created_at) }}</td>
                  <td class="px-3 whitespace-nowrap text-slate-500">{{ order.logistics?.carrier || '—' }}</td>
                  <td class="px-3 whitespace-nowrap font-mono text-blue-600">{{ order.logistics?.tracking_number || '—' }}</td>
                  <td class="px-3 whitespace-nowrap">
                    <span class="bg-green-100 text-green-700 px-1.5 py-0.5 rounded text-[10px] font-bold">已送达</span>
                  </td>
                  <td class="px-3 whitespace-nowrap">
                    <span class="text-slate-400 text-[10px]">—</span>
                  </td>
                  <td class="px-3 whitespace-nowrap">
                    <span v-if="order.production_documents?.length"
                      class="flex items-center gap-1 text-blue-600 hover:underline text-[10px] cursor-pointer">
                      <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/></svg>
                      查看
                    </span>
                    <span v-else class="text-[10px] text-slate-400">—</span>
                  </td>
                  <td class="px-3 whitespace-nowrap">
                    <select @click.stop class="text-[10px] border border-slate-200 rounded px-1.5 py-0.5 text-slate-600 bg-white">
                      <option>准备发送</option>
                      <option>无须发送</option>
                    </select>
                  </td>
                </tr>
                <tr v-if="completedOrders.length === 0">
                  <td colspan="11" class="px-3 py-8 text-center text-slate-400 text-xs">暂无已完成订单</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- 订单详情面板 -->
        <div v-if="selectedOrder" class="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <div class="flex justify-between items-start mb-6">
            <div class="flex gap-4">
              <div class="w-24 h-24 bg-green-50 rounded-lg overflow-hidden border border-green-200 shrink-0 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#22c55e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/></svg>
              </div>
              <div>
                <h3 class="text-lg font-bold text-slate-800 flex items-center gap-2">
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#15803d" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/></svg>
                  订单详情 · #{{ selectedOrder.etsy_order_id || selectedOrder.id }}
                </h3>
                <div class="text-xs text-slate-400 mb-3 flex items-center gap-1">
                  <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                  完成时间 {{ formatDate(selectedOrder.completed_at || selectedOrder.created_at) }}
                </div>
                <div class="grid grid-cols-2 gap-x-8 gap-y-1 text-sm text-slate-600">
                  <div class="flex"><span class="text-slate-400 w-16">客户:</span> {{ selectedOrder.customer_name || '—' }}</div>
                  <div class="flex"><span class="text-slate-400 w-16">产品:</span> {{ selectedOrder.sku_mapping?.sku_code || selectedOrder.sku_id || '—' }}</div>
                  <div class="flex"><span class="text-slate-400 w-16">定制:</span> {{ selectedOrder.custom_text || '—' }}</div>
                  <div class="flex"><span class="text-slate-400 w-16">数量:</span> {{ selectedOrder.quantity || 1 }} 件</div>
                </div>
              </div>
            </div>
            <div class="flex flex-col items-end gap-2">
              <span class="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-bold">已送达</span>
              <div class="text-right text-sm text-slate-500">
                <div class="flex justify-end"><span class="text-slate-400 mr-2">快递:</span> {{ selectedOrder.logistics?.carrier || '—' }}</div>
                <div class="flex justify-end font-mono text-xs text-blue-600">{{ selectedOrder.logistics?.tracking_number || '—' }}</div>
              </div>
            </div>
          </div>

          <!-- 物流轨迹 -->
          <div class="border border-slate-100 rounded-xl p-5 bg-slate-50">
            <h4 class="text-sm font-bold text-slate-700 mb-4">物流轨迹</h4>
            <div class="space-y-4">
              <div v-for="(step, index) in timelineDefault" :key="index" class="flex gap-4">
                <div class="flex flex-col items-center">
                  <div :class="step.iconBg" class="w-8 h-8 rounded-full flex items-center justify-center shrink-0" v-html="step.icon"></div>
                  <div v-if="index < timelineDefault.length - 1" class="w-px flex-1 bg-slate-200 mt-1"></div>
                </div>
                <div :class="index < timelineDefault.length - 1 ? 'pb-4' : ''">
                  <div :class="step.textColor" class="text-sm font-semibold">{{ step.title }}</div>
                  <div class="text-xs text-slate-400 mt-0.5">{{ step.desc }}</div>
                </div>
              </div>
            </div>
          </div>

          <!-- 追评邮件 -->
          <div class="border border-slate-200 rounded-xl p-5 bg-white mt-4">
            <div class="flex items-center justify-between mb-3">
              <h4 class="text-sm font-bold text-slate-700 flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
                追评邮件
              </h4>
              <div class="flex items-center gap-2">
                <span class="bg-amber-100 text-amber-700 text-xs px-2.5 py-0.5 rounded-full font-medium">准备发送</span>
                <span class="text-[10px] text-slate-400">创建 {{ formatDate(selectedOrder.created_at) }}</span>
              </div>
            </div>
            <div class="bg-slate-50 rounded-lg p-4 text-sm text-slate-600 leading-relaxed border border-slate-100">
              <p class="font-semibold text-slate-700 mb-2">Hi {{ (selectedOrder.customer_name || 'there').split(' ')[0] }},</p>
              <p class="mb-2">Hope you're doing great! Just wanted to check in — it's been a few days since your order arrived, and we'd love to know how you're liking your personalized piece ✨</p>
              <p class="mb-2">If everything looks perfect and you're happy with it, we'd truly appreciate a quick review — it means the world to small shops like ours 🙏</p>
              <p class="mb-2">Just click the link below to leave a review, it only takes a moment:</p>
              <p class="text-blue-600 underline text-xs mb-3 cursor-pointer">https://www.etsy.com/your_shop/review</p>
              <p>Warm regards,<br><span class="text-slate-500">Your Shop Team</span></p>
            </div>
            <div class="flex justify-end gap-2 mt-3">
              <button class="bg-white border border-slate-200 hover:bg-slate-50 text-slate-600 px-4 py-1.5 rounded-lg text-xs font-medium transition-colors">编辑邮件</button>
              <button class="bg-slate-800 hover:bg-slate-900 text-white px-4 py-1.5 rounded-lg text-xs font-medium transition-colors flex items-center gap-1.5">
                <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/></svg>
                发送追评邮件
              </button>
            </div>
          </div>

          <!-- 底部操作按钮 -->
          <div class="mt-4 flex justify-center gap-4">
            <button class="bg-slate-600 hover:bg-slate-700 text-white px-6 py-2.5 rounded-lg text-sm font-medium flex items-center gap-2 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>
              下载生产文档
            </button>
            <button class="text-slate-400 hover:text-slate-600 text-sm flex items-center gap-1">
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
              发送完成通知
            </button>
          </div>
        </div>

        <!-- 未选中时的提示 -->
        <div v-else class="bg-white rounded-xl shadow-sm border border-slate-200 p-12 flex flex-col items-center justify-center text-slate-400">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#cbd5e1" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="mb-3"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/></svg>
          <p class="text-sm">点击上方订单行查看详情</p>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useOrderStore } from '@/stores/orderStore'

const store = useOrderStore()

onMounted(() => {
  store.fetchOrders()
})

// ── 已完成订单（delivered 状态）
const completedOrders = computed(() =>
  store.orders.filter(o => o.status === 'delivered')
)

// ── 侧边栏各状态数量
const pendingCount = computed(() =>
  store.orders.filter(o => ['pending', 'effect_sent'].includes(o.status)).length
)
const producingCount = computed(() =>
  store.orders.filter(o => o.status === 'producing').length
)
const completedCount = computed(() => completedOrders.value.length)
const totalCount = computed(() => store.orders.length)

// ── 物流状态统计（基于 logistics 关联数据）
const deliveredCount = computed(() => completedOrders.value.length)
const shippingCount = computed(() => 0)  // 已完成订单均为送达状态

// ── 最近完成列表（取前3条）
const recentCompleted = computed(() => completedOrders.value.slice(0, 3))

// ── 圆形进度条 dashOffset 计算（圆周 175.93）
function calcDashOffset(count, total) {
  if (!total) return 175.93
  const ratio = Math.min(count / total, 1)
  return 175.93 * (1 - ratio)
}
const totalDashOffset = computed(() => calcDashOffset(totalCount.value, Math.max(totalCount.value, 1)))
const pendingDashOffset = computed(() => calcDashOffset(pendingCount.value, totalCount.value))
const producingDashOffset = computed(() => calcDashOffset(producingCount.value, totalCount.value))
const completedDashOffset = computed(() => calcDashOffset(completedCount.value, totalCount.value))

// ── 选中订单
const selectedOrder = ref(null)

function selectOrder(order) {
  selectedOrder.value = order
}

// ── 日期格式化
function formatDate(dateStr) {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

// ── 物流时间线（占位展示，待物流 API 接入后替换）
const timelineDefault = [
  {
    iconBg: 'bg-green-500',
    icon: '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m9 11 3 3L22 4"/></svg>',
    title: '包裹已签收', textColor: 'text-green-700',
    desc: '已送达收件地址'
  },
  {
    iconBg: 'bg-slate-300',
    icon: '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>',
    title: '已揽收发出', textColor: 'text-slate-600',
    desc: '快递员取件'
  },
]
</script>
