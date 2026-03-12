<template>
  <div class="bg-slate-200 min-h-[964px] min-w-max flex items-center justify-center p-8">
    <div class="flex h-[900px] w-[1480px] bg-white shadow-2xl rounded-2xl overflow-hidden shrink-0">

      <!-- ══ 左侧导航栏══ -->
      <div class="w-64 bg-white border-r border-slate-200 flex flex-col h-full overflow-y-auto shrink-0">
        <div class="p-6">
          <h1 class="text-xl font-bold text-slate-800 flex items-center gap-2">
            <span class="w-2 h-6 bg-blue-600 rounded-full"></span>
            仪表盘总览
          </h1>
        </div>

        <nav class="px-4 space-y-1">
          <!-- 仪表盘-->
          <button @click="$router.push('/')" class="w-full flex items-center justify-between px-4 py-3 rounded-xl text-slate-600 hover:bg-slate-50 transition-colors">
            <div class="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/></svg>
              <span class="font-medium">仪表盘总览</span>
            </div>
          </button>
          <!-- 待确认订单（激活） -->
          <button class="w-full flex items-center justify-between px-4 py-3 rounded-xl bg-blue-50 text-blue-600">
            <div class="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="8" height="4" x="8" y="2" rx="1" ry="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="M12 11h4"/><path d="M12 16h4"/><path d="M8 11h.01"/><path d="M8 16h.01"/></svg>
              <span class="font-medium">待确认订单</span>
            </div>
            <span class="text-xs font-bold px-2 py-0.5 rounded-full bg-blue-200 text-blue-700">{{ pendingCount || 0 }}</span>
          </button>
          <!-- 物流下单 -->
          <button @click="$router.push('/shipping')" class="w-full flex items-center justify-between px-4 py-3 rounded-xl text-slate-600 hover:bg-slate-50 transition-colors">
            <div class="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l2-1.14"/><path d="m7.5 4.27 9 5.15"/><polyline points="3.29 7 12 12 20.71 7"/><line x1="12" x2="12" y1="22" y2="12"/><circle cx="18.5" cy="15.5" r="2.5"/><path d="M20.27 17.27 22 19"/></svg>
              <span class="font-medium">物流下单</span>
            </div>
          </button>
          <!-- 生产中订单-->
          <button @click="$router.push('/production')" class="w-full flex items-center justify-between px-4 py-3 rounded-xl text-slate-600 hover:bg-slate-50 transition-colors">
            <div class="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 12-8.5 8.5c-.83.83-2.17.83-3 0 0 0 0 0 0 0a2.12 2.12 0 0 1 0-3L12 9"/><path d="M17.64 15 22 10.64"/><path d="m20.91 11.7-1.25-1.25c-.6-.6-.93-1.4-.93-2.25V7.86c0-.55-.45-1-1-1H14.5c-.85 0-1.65-.33-2.25-.93L11 4.71"/><path d="M5.8 5.81a2.2 2.2 0 0 1 3.1 0l1.3 1.3"/></svg>
              <span class="font-medium">生产中订单</span>
            </div>
            <span class="text-xs font-bold px-2 py-0.5 rounded-full bg-slate-100 text-slate-600">18</span>
          </button>
          <!-- 已完成订单-->
          <button @click="$router.push('/completed')" class="w-full flex items-center justify-between px-4 py-3 rounded-xl text-slate-600 hover:bg-slate-50 transition-colors">
            <div class="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/></svg>
              <span class="font-medium">已完成订单</span>
            </div>
          </button>
          <!-- 物流追踪 -->
          <button @click="$router.push('/logistics')" class="w-full flex items-center justify-between px-4 py-3 rounded-xl text-slate-600 hover:bg-slate-50 transition-colors">
            <div class="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H9"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.624l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/></svg>
              <span class="font-medium">物流追踪</span>
            </div>
          </button>
          <!-- 邮件模板 -->
          <button @click="$router.push('/email')" class="w-full flex items-center justify-between px-4 py-3 rounded-xl text-slate-600 hover:bg-slate-50 transition-colors">
            <div class="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
              <span class="font-medium">邮件模板</span>
            </div>
          </button>
          <!-- 工厂协作 -->
          <button @click="$router.push('/factory-workshop')" class="w-full flex items-center justify-between px-4 py-3 rounded-xl text-slate-600 hover:bg-slate-50 transition-colors">
            <div class="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l2-1.14"/><path d="m7.5 4.27 9 5.15"/><polyline points="3.29 7 12 12 20.71 7"/><line x1="12" x2="12" y1="22" y2="12"/></svg>
              <span class="font-medium">工厂协作</span>
            </div>
            <span class="text-xs font-bold px-2 py-0.5 rounded-full bg-green-100 text-green-600">NEW</span>
          </button>
        </nav>

        <!-- 2×2 统计卡-->
        <div class="p-4 mt-4">
          <div class="grid grid-cols-2 gap-3">
            <div class="bg-white border border-slate-200 rounded-xl p-3 shadow-sm flex flex-col items-center justify-center text-center">
              <div class="relative w-20 h-20 flex items-center justify-center mb-1">
                <svg width="80" height="80" viewBox="0 0 80 80" class="absolute transform -rotate-90">
                  <circle cx="40" cy="40" r="28" stroke="#e2e8f0" stroke-width="5" fill="transparent"/>
                  <circle cx="40" cy="40" r="28" stroke="#3b82f6" stroke-width="5" fill="transparent" stroke-dasharray="175.93" stroke-dashoffset="43.98" stroke-linecap="round"/>
                </svg>
                <span class="text-lg font-bold z-10 text-blue-600">{{ store.orders.length }}</span>
              </div>
              <span class="text-xs font-medium text-slate-600">总订单</span>
              <span class="text-[10px] text-slate-400">本月累计</span>
            </div>
            <div class="bg-white border border-slate-200 rounded-xl p-3 shadow-sm flex flex-col items-center justify-center text-center">
              <div class="relative w-20 h-20 flex items-center justify-center mb-1">
                <svg width="80" height="80" viewBox="0 0 80 80" class="absolute transform -rotate-90">
                  <circle cx="40" cy="40" r="28" stroke="#e2e8f0" stroke-width="5" fill="transparent"/>
                  <circle cx="40" cy="40" r="28" stroke="#f97316" stroke-width="5" fill="transparent" stroke-dasharray="175.93" stroke-dashoffset="131.95" stroke-linecap="round"/>
                </svg>
                <span class="text-lg font-bold z-10 text-orange-600">{{ pendingCount || 0 }}</span>
              </div>
              <span class="text-xs font-medium text-slate-600">新订单</span>
              <span class="text-[10px] text-slate-400">需确认</span>
            </div>
            <div class="bg-white border border-slate-200 rounded-xl p-3 shadow-sm flex flex-col items-center justify-center text-center">
              <div class="relative w-20 h-20 flex items-center justify-center mb-1">
                <svg width="80" height="80" viewBox="0 0 80 80" class="absolute transform -rotate-90">
                  <circle cx="40" cy="40" r="28" stroke="#e2e8f0" stroke-width="5" fill="transparent"/>
                  <circle cx="40" cy="40" r="28" stroke="#a855f7" stroke-width="5" fill="transparent" stroke-dasharray="175.93" stroke-dashoffset="144.26" stroke-linecap="round"/>
                </svg>
                <span class="text-lg font-bold z-10 text-purple-600">{{ store.orders.filter(o => o.status === 'producing').length }}</span>
              </div>
              <span class="text-xs font-medium text-slate-600">生产作业</span>
              <span class="text-[10px] text-slate-400">进行中</span>
            </div>
            <div class="bg-white border border-slate-200 rounded-xl p-3 shadow-sm flex flex-col items-center justify-center text-center">
              <div class="relative w-20 h-20 flex items-center justify-center mb-1">
                <svg width="80" height="80" viewBox="0 0 80 80" class="absolute transform -rotate-90">
                  <circle cx="40" cy="40" r="28" stroke="#e2e8f0" stroke-width="5" fill="transparent"/>
                  <circle cx="40" cy="40" r="28" stroke="#22c55e" stroke-width="5" fill="transparent" stroke-dasharray="175.93" stroke-dashoffset="87.96" stroke-linecap="round"/>
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
            <span class="bg-orange-100 text-orange-600 text-xs px-2 py-0.5 rounded-full">{{ pendingCount || 0 }}</span>
          </div>
          <div class="space-y-3">
            <div v-for="item in sidebarOrders" :key="item.id" class="bg-slate-50 p-3 rounded-lg border border-slate-100">
              <div class="flex justify-between items-start mb-1">
                <span class="text-xs font-bold text-slate-800">{{ item.id }}</span>
                <span class="text-[10px] text-slate-400">{{ item.time }}</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-xs text-slate-600">{{ item.customer }}</span>
                <span class="text-[10px] text-slate-400">{{ item.sku }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- ══ /左侧导航栏══ -->

      <!-- ══ 中间主内容区 ══ -->
      <div class="flex-1 bg-slate-50 p-6 overflow-y-auto h-full">
        <!-- 标题 -->
        <div class="mb-4 flex items-center gap-3">
          <h2 class="text-2xl font-bold text-slate-800">待确认订单</h2>
          <span class="bg-blue-100 text-blue-600 px-3 py-1 rounded-full text-xs font-bold">{{ pendingCount || 0 }} 条</span>
        </div>

        <!-- 子状态筛选栏 -->
        <div class="flex items-center gap-2 mb-5">
          <button class="flex items-center gap-1.5 px-4 py-2 rounded-lg text-xs font-bold bg-slate-800 text-white">
            全部 <span class="bg-white text-slate-800 px-1.5 py-0.5 rounded-full text-[10px] font-bold">{{ pendingCount || 0 }}</span>
          </button>
          <button class="flex items-center gap-1.5 px-4 py-2 rounded-lg text-xs font-bold bg-orange-50 text-orange-600 border border-orange-200 hover:bg-orange-100 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#ea580c" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/></svg>
            新到未处理<span class="bg-orange-500 text-white px-1.5 py-0.5 rounded-full text-[10px] font-bold">{{ pendingCount || 0 }}</span>
          </button>
          <button class="flex items-center gap-1.5 px-4 py-2 rounded-lg text-xs font-bold bg-white text-slate-500 border border-slate-200 hover:bg-slate-50 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            等待客户确认 <span class="bg-slate-100 text-slate-600 px-1.5 py-0.5 rounded-full text-[10px] font-bold">{{ pendingCount || 0 }}</span>
          </button>
          <div class="ml-auto text-xs text-slate-400 flex items-center gap-1">
            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" x2="12" y1="9" y2="13"/><line x1="12" x2="12.01" y1="17" y2="17"/></svg>
            新到订单须24小时内回复
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
                  <th class="px-3 whitespace-nowrap font-medium">设计稿件</th>
                  <th class="px-3 whitespace-nowrap font-medium">确认邮件</th>
                  <th class="px-3 whitespace-nowrap font-medium">数量</th>
                  <th class="px-3 whitespace-nowrap font-medium">状态</th>
                  <th class="px-3 whitespace-nowrap font-medium">创建日期</th>
                  <th class="px-3 whitespace-nowrap font-medium">操作</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                <tr v-for="order in pendingOrders" :key="order.id"
                    @click="selectedOrder = order"
                    :class="['hover:bg-slate-50 transition-colors h-[28px] cursor-pointer', selectedOrder?.id === order.id ? 'bg-blue-50' : '']">
                  <td class="px-3 whitespace-nowrap font-medium text-slate-700">{{ order.etsy_order_id || order.id }}</td>
                  <td class="px-3 whitespace-nowrap text-slate-600">{{ order.customer_name }}</td>
                  <td class="px-3 whitespace-nowrap font-mono text-slate-500">{{ order.sku_mapping?.sku_code || order.sku_id }}</td>
                  <td class="px-3 whitespace-nowrap text-slate-600">{{ order.front_text ? '已录入' : '待录入' }}</td>
                  <td class="px-3 whitespace-nowrap text-slate-600">{{ order.email_logs?.length > 0 ? '已发送' : '待发送' }}</td>
                  <td class="px-3 whitespace-nowrap text-slate-600">{{ order.quantity }}</td>
                  <td class="px-3 whitespace-nowrap"><span class="bg-orange-100 text-orange-600 px-1.5 py-0.5 rounded text-[10px] font-bold">{{ store.statusMap[order.status] || '待确认' }}</span></td>
                  <td class="px-3 whitespace-nowrap text-slate-500">{{ new Date(order.created_at).toLocaleDateString('zh-CN') }}</td>
                  <td class="px-3 whitespace-nowrap"><button @click.stop="confirmOrder(order)" class="bg-slate-800 hover:bg-slate-900 text-white px-2 py-0.5 rounded text-[10px] transition-colors">创建订单</button></td>
                </tr>
                <tr v-if="pendingOrders.length === 0" class="h-[28px]">
                  <td colspan="9" class="px-3 text-center text-slate-400 text-xs">暂无待确认订单</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- 订单详情 & 效果图预览 -->
        <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <div class="flex justify-between items-start mb-6">
            <div class="flex gap-4">
              <div class="w-24 h-24 bg-slate-100 rounded-lg overflow-hidden border border-slate-200 shrink-0 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg>
              </div>
              <div>
                <h3 class="text-lg font-bold text-slate-800 flex items-center gap-2 mb-1">
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/></svg>
                  订单详情
                </h3>
                <div class="text-xs text-slate-400 mb-3">{{ selectedOrder ? new Date(selectedOrder.created_at).toLocaleDateString('zh-CN') : '请选择订单' }}</div>
                <div class="grid grid-cols-2 gap-x-8 gap-y-1 text-sm text-slate-600">
                  <div class="flex"><span class="text-slate-400 w-16">订单ID:</span> {{ selectedOrder?.etsy_order_id || selectedOrder?.id || '--' }}</div>
                  <div class="flex"><span class="text-slate-400 w-16">客户:</span> {{ selectedOrder?.customer_name || '--' }}</div>
                  <div class="flex"><span class="text-slate-400 w-16">产品:</span> {{ selectedOrder?.sku_mapping?.sku_code || selectedOrder?.sku_id || '--' }}</div>
                  <div class="flex"><span class="text-slate-400 w-16">数量:</span> {{ selectedOrder?.quantity || '--' }}</div>
                </div>
              </div>
            </div>
            <div class="flex flex-col items-end gap-2">
              <div class="grid grid-cols-1 gap-y-1 text-sm text-slate-600 text-right">
                <div class="flex justify-end"><span class="text-slate-400 mr-2">订单日期:</span> {{ selectedOrder ? new Date(selectedOrder.created_at).toLocaleDateString('zh-CN') : '--' }}</div>
                <div class="flex justify-end"><span class="text-slate-400 mr-2">发货日期:</span> {{ selectedOrder?.estimated_delivery ? new Date(selectedOrder.estimated_delivery).toLocaleDateString('zh-CN') : '待定' }}</div>
              </div>
              <button class="mt-2 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg text-sm font-medium flex items-center gap-2 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" x2="12" y1="3" y2="15"/></svg>
                本地上传
              </button>
              <span class="text-[10px] text-slate-400">自定义图形 SVG</span>
            </div>
          </div>
          <!-- 效果图预览区：正面+背面并排显示 -->
          <div class="border-2 border-dashed border-slate-200 rounded-xl bg-slate-50 overflow-hidden relative">
            <template v-if="selectedOrder?.effect_image_url || selectedOrder?.effect_image_back_url">
              <span class="absolute top-2 right-2 bg-green-500 text-white text-[10px] px-2 py-0.5 rounded-full z-10">已生成</span>
              <div class="flex gap-2 p-3">
                <!-- 正面 -->
                <div class="flex-1 flex flex-col items-center gap-1">
                  <span class="text-[10px] text-slate-400 font-medium">正面</span>
                  <div class="h-40 w-full flex items-center justify-center bg-white rounded-lg border border-slate-100 overflow-hidden">
                    <img v-if="selectedOrder.effect_image_url"
                      :src="selectedOrder.effect_image_url"
                      alt="正面效果图"
                      class="h-full w-full object-contain cursor-pointer"
                      @click="openImage(selectedOrder.effect_image_url)"
                    />
                    <span v-else class="text-xs text-slate-300">无正面</span>
                  </div>
                </div>
                <!-- 背面 -->
                <div class="flex-1 flex flex-col items-center gap-1">
                  <span class="text-[10px] text-slate-400 font-medium">背面</span>
                  <div class="h-40 w-full flex items-center justify-center bg-white rounded-lg border border-slate-100 overflow-hidden">
                    <img v-if="selectedOrder.effect_image_back_url"
                      :src="selectedOrder.effect_image_back_url"
                      alt="背面效果图"
                      class="h-full w-full object-contain cursor-pointer"
                      @click="openImage(selectedOrder.effect_image_back_url)"
                    />
                    <span v-else class="text-xs text-slate-300">无背面</span>
                  </div>
                </div>
              </div>
            </template>
            <template v-else>
              <div class="h-48 flex flex-col items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg>
                <h3 class="text-base font-bold text-slate-400 mt-3 mb-1">效果图预览</h3>
                <p class="text-sm text-slate-400">尚未生成效果图</p>
              </div>
            </template>
          </div>
          <div class="mt-4 flex justify-center items-center gap-4">
            <button
              :disabled="!selectedOrder?.effect_image_url"
              @click="selectedOrder?.effect_image_url && openImage(selectedOrder.effect_image_url)"
              :class="selectedOrder?.effect_image_url ? 'bg-slate-600 hover:bg-slate-700 text-white' : 'bg-slate-200 text-slate-400 cursor-not-allowed'"
              class="px-6 py-2.5 rounded-lg text-sm font-medium flex items-center gap-2 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>
              下载原图
            </button>
            <button class="text-slate-400 hover:text-slate-600 text-sm flex items-center gap-1">历史版本</button>
          </div>
        </div>
      </div>
      <!-- ══ /中间主内容区 ══ -->

      <!-- ══ 右侧邮件面板 ══ -->
      <div class="w-96 bg-white border-l border-slate-200 flex flex-col h-full shrink-0 overflow-y-auto">
        <!-- 客户信息头部 -->
        <div class="p-6 border-b border-slate-100 flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center font-bold text-sm">
              {{ initials }}
            </div>
            <div>
              <h3 class="font-bold text-slate-800">{{ selectedOrder?.customer_name || '请选择订单' }}</h3>
              <div class="flex items-center gap-1 text-xs text-slate-500">
                <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg>
                英国
              </div>
            </div>
          </div>
        </div>

        <div class="p-6 flex-1 flex flex-col gap-6">
          <!-- 生成的邮件 -->
          <div>
            <h4 class="text-sm font-medium text-slate-500 mb-2">生成的邮件</h4>
            <div class="bg-slate-50 border border-slate-200 rounded-xl p-4 text-sm text-slate-600 leading-relaxed h-[200px] overflow-y-auto whitespace-pre-wrap">
              <template v-if="emailContent">
                {{ emailContent }}
              </template>
              <template v-else>
                <p class="text-slate-400 text-center mt-8">请选择订单并点击「生成邮件」</p>
              </template>
            </div>
          </div>

          <!-- 客户需求 -->
          <div>
            <h4 class="text-sm font-medium text-slate-500 mb-2">客户需求</h4>
            <textarea
              v-model="customerNote"
              class="w-full bg-slate-50 border border-slate-200 rounded-xl p-3 text-sm text-slate-600 h-24 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all"
              placeholder="在此粘贴客户的需求以生成回复...">
            </textarea>
          </div>

          <!-- 风格选择 -->
          <div>
            <h4 class="text-sm font-medium text-slate-500 mb-3">风格选择</h4>
            <div class="grid grid-cols-3 gap-3">
              <button :class="['flex flex-col items-center justify-center gap-2 p-3 rounded-xl border transition-all', selectedStyle === 'natural' ? 'bg-blue-50 border-blue-200 text-blue-600' : 'bg-white border-slate-200 text-slate-400 hover:bg-slate-50']" @click="selectedStyle = 'natural'">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" :stroke="selectedStyle === 'natural' ? '#2563eb' : '#94a3b8'" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2"/><line x1="9" x2="9.01" y1="9" y2="9"/><line x1="15" x2="15.01" y1="9" y2="9"/></svg>
                <span class="text-xs font-medium">自然语言</span>
              </button>
              <button :class="['flex flex-col items-center justify-center gap-2 p-3 rounded-xl border transition-all', selectedStyle === 'cute' ? 'bg-blue-50 border-blue-200 text-blue-600' : 'bg-white border-slate-200 text-slate-400 hover:bg-slate-50']" @click="selectedStyle = 'cute'">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" :stroke="selectedStyle === 'cute' ? '#2563eb' : '#94a3b8'" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>
                <span class="text-xs font-medium">可爱风格</span>
              </button>
              <button :class="['flex flex-col items-center justify-center gap-2 p-3 rounded-xl border transition-all', selectedStyle === 'direct' ? 'bg-blue-50 border-blue-200 text-blue-600' : 'bg-white border-slate-200 text-slate-400 hover:bg-slate-50']" @click="selectedStyle = 'direct'">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" :stroke="selectedStyle === 'direct' ? '#2563eb' : '#94a3b8'" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
                <span class="text-xs font-medium">直接了当</span>
              </button>
            </div>
          </div>

          <!-- 操作按钮 -->
          <div class="mt-auto space-y-3">
            <button @click="generateEmail" class="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-xl font-medium flex items-center justify-center gap-2 shadow-sm transition-all active:scale-[0.98]">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/></svg>
              生成邮件
            </button>
            <button @click="copyEmail" class="w-full bg-white border border-slate-200 hover:bg-slate-50 text-slate-600 py-3 rounded-xl font-medium flex items-center justify-center gap-2 transition-all active:scale-[0.98]">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>
              复制内容
            </button>
          </div>
        </div>
      </div>
      <!-- ══ /右侧邮件面板 ══ -->

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useOrderStore } from '../../stores/orderStore'

const store = useOrderStore()

// 页面加载时获取数据
onMounted(() => {
  store.getPendingOrders()
})

// 计算属性：待确认订单列表
const pendingOrders = computed(() => 
  store.orders.filter(o => ['pending', 'effect_sent'].includes(o.status))
)

// 计算属性：待确认订单数量
const pendingCount = computed(() => pendingOrders.value.length)

// 选中的订单
const selectedOrder = ref(null)
const customerNote = ref('')
const selectedStyle = ref('natural')
const showBackSide = ref(false)  // 正面/背面切换

// 当前显示的效果图 URL（根据正/反面切换）
const currentEffectImageUrl = computed(() => {
  if (!selectedOrder.value) return null
  if (showBackSide.value) return selectedOrder.value.effect_image_back_url || null
  return selectedOrder.value.effect_image_url || null
})

// 安全打开图片新标签页
const openImage = (url) => {
  if (url) window.open(url, '_blank')
}

// 客户姓名首字母
const initials = computed(() => {
  const name = selectedOrder.value?.customer_name || 'M'
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
})

// 徧边栏最新订单（取前4条）
const sidebarOrders = computed(() => 
  pendingOrders.value.slice(0, 4).map(order => ({
    id: order.etsy_order_id || order.id,
    time: new Date(order.created_at).toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }),
    customer: order.customer_name,
    sku: order.sku_mapping?.sku_code || order.sku_id
  }))
)

// 生成的邮件文本
const emailContent = ref('')

// 「创建订单」：将订单状态改为 producing
const confirmOrder = async (order) => {
  if (!confirm(`确认将订单 ${order.etsy_order_id || order.id} 改为生产中？`)) return
  try {
    await store.updateOrderStatus(order.id, 'producing')
    selectedOrder.value = null
    alert('✅ 订单已转入生产中！')
  } catch (e) {
    alert('❌ 操作失败：' + e.message)
  }
}

// 「生成邮件」：根据订单信息和风格生成英文客户确认邮件
const generateEmail = () => {
  if (!selectedOrder.value) {
    alert('请先点击选择一条订单')
    return
  }
  const order = selectedOrder.value
  const firstName = order.customer_name?.split(' ')[0] || 'there'
  const orderId = order.etsy_order_id || order.id
  const frontText = order.front_text || ''
  const backText = order.back_text || ''
  const hasEffectImage = !!order.effect_image_url
  const effectImageLine = hasEffectImage
    ? `\nWe have prepared a preview of your custom tag. You can view it here:\n${order.effect_image_url}\n`
    : '\nWe are currently preparing a preview of your custom tag and will send it to you within 4 hours.\n'
  const customDetails = [frontText, backText].filter(Boolean).join(' / ')
  const detailsLine = customDetails ? `\nYour customization details: ${customDetails}\n` : ''
  const noteSection = customerNote.value ? `\nNote: ${customerNote.value}\n` : ''

  let greeting = ''
  let sign = ''
  if (selectedStyle.value === 'cute') {
    greeting = `Hi ${firstName}! 💕`
    sign = 'With love,\nOur Pet Tag Team 🐾'
  } else if (selectedStyle.value === 'direct') {
    greeting = `Hi ${firstName},`
    sign = 'Best,\nCustomer Support'
  } else {
    greeting = `Dear ${firstName},`
    sign = 'Kind regards,\nCustomer Support Team'
  }

  emailContent.value = `${greeting}\n\nThank you for your order! We have received your customization request for order #${orderId}.${detailsLine}${effectImageLine}${noteSection}\nPlease review and let us know if everything looks good, or if you would like any changes.\n\n${sign}`
}

// 「复制内容」：复制邮件到剪贴板
const copyEmail = async () => {
  if (!emailContent.value) {
    alert('请先点击「生成邮件」')
    return
  }
  try {
    await navigator.clipboard.writeText(emailContent.value)
    alert('✅ 邮件内容已复制到剪贴板！')
  } catch (e) {
    alert('复制失败，请手动复制')
  }
}
</script>
