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
          <!-- 仪表盘（激活） -->
          <button class="w-full flex items-center justify-between px-4 py-3 rounded-xl bg-blue-50 text-blue-600">
            <div class="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/></svg>
              <span class="font-medium">仪表盘总览</span>
            </div>
          </button>
          <!-- 待确认订单-->
          <button @click="$router.push('/pending')" class="w-full flex items-center justify-between px-4 py-3 rounded-xl text-slate-600 hover:bg-slate-50 transition-colors">
            <div class="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="8" height="4" x="8" y="2" rx="1" ry="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="M12 11h4"/><path d="M12 16h4"/><path d="M8 11h.01"/><path d="M8 16h.01"/></svg>
              <span class="font-medium">待确认订单</span>
            </div>
            <span class="text-xs font-bold px-2 py-0.5 rounded-full bg-slate-100 text-slate-600">{{ navCounts.pending || 0 }}</span>
          </button>
          <!-- 生产中订单-->
          <button @click="$router.push('/production')" class="w-full flex items-center justify-between px-4 py-3 rounded-xl text-slate-600 hover:bg-slate-50 transition-colors">
            <div class="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 12-8.5 8.5c-.83.83-2.17.83-3 0 0 0 0 0 0 0a2.12 2.12 0 0 1 0-3L12 9"/><path d="M17.64 15 22 10.64"/><path d="m20.91 11.7-1.25-1.25c-.6-.6-.93-1.4-.93-2.25V7.86c0-.55-.45-1-1-1H14.5c-.85 0-1.65-.33-2.25-.93L11 4.71"/><path d="M5.8 5.81a2.2 2.2 0 0 1 3.1 0l1.3 1.3"/></svg>
              <span class="font-medium">生产中订单</span>
            </div>
            <span class="text-xs font-bold px-2 py-0.5 rounded-full bg-slate-100 text-slate-600">{{ navCounts.producing || 0 }}</span>
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
        </nav>

        <!-- 2×2 圆弧统计卡片 -->
        <div class="p-4 mt-4">
          <div class="grid grid-cols-2 gap-3">
            <div class="bg-white border border-slate-200 rounded-xl p-3 shadow-sm flex flex-col items-center justify-center text-center relative overflow-hidden">
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
            <div class="bg-white border border-slate-200 rounded-xl p-3 shadow-sm flex flex-col items-center justify-center text-center relative overflow-hidden">
              <div class="relative w-20 h-20 flex items-center justify-center mb-1">
                <svg width="80" height="80" viewBox="0 0 80 80" class="absolute transform -rotate-90">
                  <circle cx="40" cy="40" r="28" stroke="#e2e8f0" stroke-width="5" fill="transparent"/>
                  <circle cx="40" cy="40" r="28" stroke="#f97316" stroke-width="5" fill="transparent" stroke-dasharray="175.93" stroke-dashoffset="168.89" stroke-linecap="round"/>
                </svg>
                <span class="text-lg font-bold z-10 text-orange-600">{{ navCounts.pending }}</span>
              </div>
              <span class="text-xs font-medium text-slate-600">新订单</span>
              <span class="text-[10px] text-slate-400">需确认</span>
            </div>
            <div class="bg-white border border-slate-200 rounded-xl p-3 shadow-sm flex flex-col items-center justify-center text-center relative overflow-hidden">
              <div class="relative w-20 h-20 flex items-center justify-center mb-1">
                <svg width="80" height="80" viewBox="0 0 80 80" class="absolute transform -rotate-90">
                  <circle cx="40" cy="40" r="28" stroke="#e2e8f0" stroke-width="5" fill="transparent"/>
                  <circle cx="40" cy="40" r="28" stroke="#a855f7" stroke-width="5" fill="transparent" stroke-dasharray="175.93" stroke-dashoffset="144.26" stroke-linecap="round"/>
                </svg>
                <span class="text-lg font-bold z-10 text-purple-600">{{ navCounts.producing }}</span>
              </div>
              <span class="text-xs font-medium text-slate-600">生产作业</span>
              <span class="text-[10px] text-slate-400">进行中</span>
            </div>
            <div class="bg-white border border-slate-200 rounded-xl p-3 shadow-sm flex flex-col items-center justify-center text-center relative overflow-hidden">
              <div class="relative w-20 h-20 flex items-center justify-center mb-1">
                <svg width="80" height="80" viewBox="0 0 80 80" class="absolute transform -rotate-90">
                  <circle cx="40" cy="40" r="28" stroke="#e2e8f0" stroke-width="5" fill="transparent"/>
                  <circle cx="40" cy="40" r="28" stroke="#22c55e" stroke-width="5" fill="transparent" stroke-dasharray="175.93" stroke-dashoffset="87.96" stroke-linecap="round"/>
                </svg>
                <span class="text-lg font-bold z-10 text-green-600">{{ navCounts.completed }}</span>
              </div>
              <span class="text-xs font-medium text-slate-600">已交付</span>
              <span class="text-[10px] text-slate-400">物流送达</span>
            </div>
          </div>
        </div>

        <!-- 新订单列表-->
        <div class="p-4 mt-auto">
          <div class="flex items-center justify-between mb-3">
            <h3 class="text-sm font-bold text-slate-700">新订单列表</h3>
            <span class="bg-orange-100 text-orange-600 text-xs px-2 py-0.5 rounded-full">5</span>
          </div>
          <div class="space-y-3">
            <div v-for="item in newOrders" :key="item.id" class="bg-slate-50 p-3 rounded-lg border border-slate-100">
              <div class="flex justify-between items-start mb-1">
                <span class="text-xs font-bold text-slate-800">{{ item.id }}</span>
                <span :class="['text-[10px] font-semibold', item.timeColor]">{{ item.time }}</span>
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

      <!-- ══ 右侧主内容 ══ -->
      <div class="flex-1 bg-slate-50 p-6 overflow-y-auto h-full">
        <!-- 页面标题 -->
        <div class="mb-6 flex items-center justify-between">
          <div class="flex items-center gap-3">
            <h2 class="text-2xl font-bold text-slate-800">仪表盘总览</h2>
            <span class="bg-blue-100 text-blue-600 px-3 py-1 rounded-full text-xs font-bold">全局</span>
          </div>
          <span class="text-xs text-slate-400">数据更新：2026-02-03 09:30</span>
        </div>

        <!-- KPI 卡片行（5张） -->
        <div class="grid grid-cols-5 gap-4 mb-6">
          <div class="bg-white border border-slate-200 rounded-xl p-4 shadow-sm">
            <div class="text-xs text-slate-400 mb-1">总订单</div>
            <div class="text-2xl font-bold text-slate-800 mb-1">{{ stats.total || 0 }}</div>
            <div class="text-xs text-slate-400 mb-2">本月累计</div>
            <span class="text-[10px] bg-slate-100 text-slate-500 px-2 py-0.5 rounded-full">全部</span>
          </div>
          <div class="bg-white border border-orange-200 rounded-xl p-4 shadow-sm">
            <div class="text-xs text-orange-500 font-medium mb-1">新订单</div>
            <div class="text-2xl font-bold text-orange-500 mb-1">{{ stats.pending || 0 }}</div>
            <div class="text-xs text-slate-400 mb-2">须24小时内回复</div>
            <span class="text-[10px] bg-orange-100 text-orange-600 px-2 py-0.5 rounded-full">需处理</span>
          </div>
          <div class="bg-white border border-slate-200 rounded-xl p-4 shadow-sm">
            <div class="text-xs text-slate-400 mb-1">待确认</div>
            <div class="text-2xl font-bold text-slate-800 mb-1">{{ stats.pending || 0 }}</div>
            <div class="text-xs text-slate-400 mb-2">需跟进处理</div>
            <span class="text-[10px] bg-orange-100 text-orange-600 px-2 py-0.5 rounded-full">需跟进</span>
          </div>
          <div class="bg-white border border-slate-200 rounded-xl p-4 shadow-sm">
            <div class="text-xs text-slate-400 mb-1">生产中</div>
            <div class="text-2xl font-bold text-slate-800 mb-1">{{ stats.producing || 0 }}</div>
            <div class="text-xs text-slate-400 mb-2">进行中</div>
            <span class="text-[10px] bg-slate-100 text-slate-500 px-2 py-0.5 rounded-full">正常</span>
          </div>
          <div class="bg-white border border-slate-200 rounded-xl p-4 shadow-sm">
            <div class="text-xs text-slate-400 mb-1">已完成</div>
            <div class="text-2xl font-bold text-slate-800 mb-1">{{ stats.completed || 0 }}</div>
            <div class="text-xs text-slate-400 mb-2">本月交付</div>
            <span class="text-[10px] bg-green-100 text-green-600 px-2 py-0.5 rounded-full">50%</span>
          </div>
        </div>

        <!-- 图表表-->
        <div class="grid grid-cols-2 gap-4 mb-6">
          <!-- 订单状态分布 -->
          <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-sm">
            <h3 class="text-sm font-bold text-slate-700 mb-4">订单状态分布</h3>
            <div class="flex items-center gap-6">
              <div class="relative flex-shrink-0" style="width:130px;height:130px;">
                <svg width="130" height="130" viewBox="0 0 130 130">
                  <circle cx="65" cy="65" r="52" fill="none" stroke="#f1f5f9" stroke-width="14"/>
                  <circle cx="65" cy="65" r="52" fill="none" stroke="#334155" stroke-width="14" stroke-dasharray="163.4 326.7" stroke-dashoffset="81.7" transform="rotate(-90 65 65)"/>
                  <circle cx="65" cy="65" r="52" fill="none" stroke="#64748b" stroke-width="14" stroke-dasharray="58.8 326.7" stroke-dashoffset="-81.7" transform="rotate(-90 65 65)"/>
                  <circle cx="65" cy="65" r="52" fill="none" stroke="#94a3b8" stroke-width="14" stroke-dasharray="81.7 326.7" stroke-dashoffset="-140.5" transform="rotate(-90 65 65)"/>
                  <circle cx="65" cy="65" r="52" fill="none" stroke="#e2e8f0" stroke-width="14" stroke-dasharray="22.9 326.7" stroke-dashoffset="-222.2" transform="rotate(-90 65 65)"/>
                  <text x="65" y="61" text-anchor="middle" font-size="18" font-weight="700" fill="#1e293b">128</text>
                  <text x="65" y="76" text-anchor="middle" font-size="10" fill="#94a3b8">总订单</text>
                </svg>
              </div>
              <div class="space-y-2.5 text-sm flex-1">
                <div class="flex items-center gap-2"><div class="w-3 h-3 rounded-full bg-slate-700 flex-shrink-0"></div><span class="text-slate-600 flex-1">已完成</span><span class="font-bold text-slate-700">64</span><span class="text-slate-400 text-xs w-8 text-right">50%</span></div>
                <div class="flex items-center gap-2"><div class="w-3 h-3 rounded-full bg-slate-500 flex-shrink-0"></div><span class="text-slate-600 flex-1">生产中</span><span class="font-bold text-slate-700">23</span><span class="text-slate-400 text-xs w-8 text-right">18%</span></div>
                <div class="flex items-center gap-2"><div class="w-3 h-3 rounded-full bg-slate-300 flex-shrink-0"></div><span class="text-slate-600 flex-1">待确认</span><span class="font-bold text-slate-700">32</span><span class="text-slate-400 text-xs w-8 text-right">25%</span></div>
                <div class="flex items-center gap-2"><div class="w-3 h-3 rounded-full bg-slate-200 flex-shrink-0"></div><span class="text-slate-600 flex-1">其他</span><span class="font-bold text-slate-700">9</span><span class="text-slate-400 text-xs w-8 text-right">7%</span></div>
              </div>
            </div>
          </div>
          <!-- 本周下单趋势 -->
          <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-sm">
            <h3 class="text-sm font-bold text-slate-700 mb-4">本周下单趋势（件）</h3>
            <div class="flex items-end gap-2" style="height:110px;">
              <div v-for="bar in weekBars" :key="bar.day" class="flex flex-col items-center gap-1 flex-1">
                <span :class="['text-[10px]', bar.today ? 'text-slate-800 font-bold' : 'text-slate-400']">{{ bar.val }}</span>
                <div :class="['w-full rounded-t', bar.today ? 'bg-slate-700' : (bar.light ? 'bg-slate-100' : 'bg-slate-200')]" :style="{ height: bar.height }"></div>
                <span :class="['text-[10px]', bar.today ? 'text-slate-800 font-bold' : 'text-slate-400']">{{ bar.day }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 待确认订单mini 表格 -->
        <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden mb-4">
          <div class="px-5 py-3 flex items-center justify-between border-b border-slate-100">
            <div class="flex items-center gap-2">
              <h3 class="text-sm font-bold text-slate-800">待确认订单</h3>
              <span class="bg-orange-100 text-orange-600 text-xs px-2 py-0.5 rounded-full font-bold">{{ navCounts.pending || 0 }}</span>
            </div>
            <p class="text-xs text-slate-400">最新生产订单· 需尽快确认效果图并发送邮件</p>
            <button @click="$router.push('/pending')" class="text-xs text-slate-400 hover:text-slate-600">查看全部 →</button>
          </div>
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
                <tr v-for="order in pendingOrdersList" :key="order.id" class="hover:bg-slate-50 transition-colors h-[28px]">
                  <td class="px-3 whitespace-nowrap font-medium text-slate-700">{{ order.etsy_order_id || order.id }}</td>
                  <td class="px-3 whitespace-nowrap text-slate-600">{{ order.customer_name }}</td>
                  <td class="px-3 whitespace-nowrap font-mono text-slate-500">{{ order.sku_mapping?.sku_code || order.sku_id }}</td>
                  <td class="px-3 whitespace-nowrap text-slate-600">{{ order.front_text ? '已录入' : '待录入' }}</td>
                  <td class="px-3 whitespace-nowrap text-slate-600">{{ order.email_logs?.length > 0 ? '已发送' : '待发送' }}</td>
                  <td class="px-3 whitespace-nowrap text-slate-600">{{ order.quantity }}</td>
                  <td class="px-3 whitespace-nowrap"><span class="bg-orange-100 text-orange-600 px-1.5 py-0.5 rounded text-[10px] font-bold">{{ store.statusMap[order.status] || '待确认' }}</span></td>
                  <td class="px-3 whitespace-nowrap text-slate-500">{{ new Date(order.created_at).toLocaleDateString('zh-CN') }}</td>
                  <td class="px-3 whitespace-nowrap"><button class="bg-slate-800 hover:bg-slate-900 text-white px-2 py-0.5 rounded text-[10px] transition-colors">创建订单</button></td>
                </tr>
                <tr v-if="pendingOrdersList.length === 0" class="h-[28px]">
                  <td colspan="9" class="px-3 text-center text-slate-400 text-xs">暂无待确认订单</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- 生产中订单mini 表格 -->
        <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
          <div class="px-5 py-3 flex items-center justify-between border-b border-slate-100">
            <div class="flex items-center gap-2">
              <h3 class="text-sm font-bold text-slate-800">生产中订单</h3>
              <span class="bg-slate-100 text-slate-600 text-xs px-2 py-0.5 rounded-full font-bold">{{ navCounts.producing || 0 }}</span>
            </div>
            <p class="text-xs text-slate-400">订单确认后流转至此，跟踪生产进度</p>
            <button @click="$router.push('/production')" class="text-xs text-slate-400 hover:text-slate-600">查看全部 →</button>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-xs text-left">
              <thead class="bg-slate-50 text-slate-500 font-medium border-b border-slate-200">
                <tr class="h-[32px]">
                  <th class="px-3 whitespace-nowrap font-medium">订单ID</th>
                  <th class="px-3 whitespace-nowrap font-medium">客户名称</th>
                  <th class="px-3 whitespace-nowrap font-medium">产品</th>
                  <th class="px-3 whitespace-nowrap font-medium">生产进度</th>
                  <th class="px-3 whitespace-nowrap font-medium">交货期</th>
                  <th class="px-3 whitespace-nowrap font-medium">状态</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                <tr v-for="order in producingOrdersList" :key="order.id" class="hover:bg-slate-50 transition-colors h-[28px]">
                  <td class="px-3 whitespace-nowrap font-medium text-slate-700">{{ order.etsy_order_id || order.id }}</td>
                  <td class="px-3 whitespace-nowrap text-slate-600">{{ order.customer_name }}</td>
                  <td class="px-3 whitespace-nowrap font-mono text-slate-500">{{ order.sku_mapping?.sku_code || order.sku_id }}</td>
                  <td class="px-3 whitespace-nowrap">
                    <div class="flex items-center gap-2">
                      <div class="w-20 bg-slate-200 rounded-full h-1.5">
                        <div :class="['h-1.5 rounded-full', order.progress < 30 ? 'bg-orange-500' : 'bg-blue-500']" :style="{ width: (order.progress || 0) + '%' }"></div>
                      </div>
                      <span :class="order.progress < 30 ? 'text-orange-600 font-medium' : 'text-slate-600'">{{ order.progress || 0 }}%</span>
                    </div>
                  </td>
                  <td :class="['px-3 whitespace-nowrap', order.progress < 30 ? 'text-orange-600 font-medium' : 'text-slate-500']">{{ order.estimated_delivery ? new Date(order.estimated_delivery).toLocaleDateString('zh-CN', {month:'2-digit', day:'2-digit'}) : '--' }}</td>
                  <td class="px-3 whitespace-nowrap">
                    <span :class="['px-1.5 py-0.5 rounded text-[10px] font-bold', order.progress < 30 ? 'bg-orange-100 text-orange-600' : 'bg-slate-100 text-slate-600']">{{ order.progress < 30 ? '须跟进' : '生产中' }}</span>
                  </td>
                </tr>
                <tr v-if="producingOrdersList.length === 0" class="h-[28px]">
                  <td colspan="6" class="px-3 text-center text-slate-400 text-xs">暂无生产中订单</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <!-- ══ /右侧主内容 ══ -->

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useOrderStore } from '../../stores/orderStore'

const store = useOrderStore()

// 统计数据（通过 ref 存储，onMounted 时异步获取）
const stats = ref({ total: 0, pending: 0, producing: 0, completed: 0 })

// 计算属性：各状态订单数量
// 基于 store.orders 动态计算，无需额外请求
const navCounts = computed(() => ({
  pending: store.orders.filter(o => ['pending', 'effect_sent'].includes(o.status)).length,
  producing: store.orders.filter(o => o.status === 'producing').length,
  completed: store.orders.filter(o => o.status === 'delivered').length
}))

// 计算属性：待确认订单（取前3条）
const pendingOrdersList = computed(() => 
  store.orders.filter(o => ['pending', 'effect_sent'].includes(o.status)).slice(0, 3)
)

// 计算属性：生产中订单（取前3条）
const producingOrdersList = computed(() => 
  store.orders.filter(o => o.status === 'producing').slice(0, 3)
)

// 页面加载时获取数据
onMounted(async () => {
  await store.fetchOrders()
  // 基于 store.orders 计算统计数据，无需额外请求
  stats.value = {
    total: store.orders.length,
    pending: store.orders.filter(o => ['pending', 'effect_sent'].includes(o.status)).length,
    producing: store.orders.filter(o => o.status === 'producing').length,
    completed: store.orders.filter(o => o.status === 'delivered').length
  }
})

// 保留的假数据（新订单列表和趋势图）
const newOrders = [
  { id: '#PO-2602-009', time: '18分钟前', timeColor: 'text-orange-500', customer: 'Sophie Turner', sku: 'B-E01A' },
  { id: '#PO-2602-010', time: '1小时前',  timeColor: 'text-orange-500', customer: 'James Wilson',  sku: 'B-G01B' },
  { id: '#PO-2602-011', time: '5小时前',  timeColor: 'text-orange-400', customer: 'Mark Davis',    sku: 'B-E01C' },
  { id: '#PO-2602-012', time: '8小时前',  timeColor: 'text-slate-400',  customer: 'Anna Smith',    sku: 'B-H01A' },
]

const weekBars = [
  { day: '一', val: 12, height: '40px', today: false },
  { day: '二', val: 18, height: '60px', today: false },
  { day: '三', val: 15, height: '50px', today: false },
  { day: '四', val: 22, height: '73px', today: false },
  { day: '五', val: 30, height: '100px', today: true },
  { day: '六', val: 8,  height: '27px', today: false },
  { day: '日', val: 3,  height: '10px', today: false, light: true },
]
</script>
