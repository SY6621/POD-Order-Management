<template>
  <div class="bg-slate-200 min-h-[964px] min-w-max flex items-center justify-center p-8">
    <div class="flex h-[900px] w-[1480px] bg-white shadow-2xl rounded-2xl overflow-hidden shrink-0">

      <!-- ══ 左侧导航栏 ══ -->
      <div class="w-64 bg-white border-r border-slate-200 flex flex-col h-full overflow-y-auto shrink-0">
        <div class="p-6">
          <h1 class="text-xl font-bold text-slate-800 flex items-center gap-2">
            <span class="w-2 h-6 bg-blue-600 rounded-full"></span>
            仪表盘总览
          </h1>
        </div>
        <nav class="px-4 space-y-1">
          <button @click="$router.push('/')" class="w-full flex items-center justify-between px-4 py-3 rounded-xl text-slate-600 hover:bg-slate-50 transition-colors">
            <div class="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/></svg>
              <span class="font-medium">仪表盘总览</span>
            </div>
          </button>
          <button @click="$router.push('/pending')" class="w-full flex items-center justify-between px-4 py-3 rounded-xl text-slate-600 hover:bg-slate-50 transition-colors">
            <div class="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="8" height="4" x="8" y="2" rx="1" ry="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="M12 11h4"/><path d="M12 16h4"/><path d="M8 11h.01"/><path d="M8 16h.01"/></svg>
              <span class="font-medium">待确认订单</span>
            </div>
            <span class="text-xs font-bold px-2 py-0.5 rounded-full bg-slate-100 text-slate-600">{{ pendingCount }}</span>
          </button>
          <!-- 物流下单 Active -->
          <button class="w-full flex items-center justify-between px-4 py-3 rounded-xl bg-blue-50 text-blue-600">
            <div class="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l2-1.14"/><path d="m7.5 4.27 9 5.15"/><polyline points="3.29 7 12 12 20.71 7"/><line x1="12" x2="12" y1="22" y2="12"/><circle cx="18.5" cy="15.5" r="2.5"/><path d="M20.27 17.27 22 19"/></svg>
              <span class="font-medium">物流下单</span>
            </div>
          </button>
          <button @click="$router.push('/production')" class="w-full flex items-center justify-between px-4 py-3 rounded-xl text-slate-600 hover:bg-slate-50 transition-colors">
            <div class="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 12-8.5 8.5c-.83.83-2.17.83-3 0 0 0 0 0 0 0a2.12 2.12 0 0 1 0-3L12 9"/><path d="M17.64 15 22 10.64"/><path d="m20.91 11.7-1.25-1.25c-.6-.6-.93-1.4-.93-2.25V7.86c0-.55-.45-1-1-1H14.5c-.85 0-1.65-.33-2.25-.93L11 4.71"/><path d="M5.8 5.81a2.2 2.2 0 0 1 3.1 0l1.3 1.3"/></svg>
              <span class="font-medium">生产中订单</span>
            </div>
          </button>
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

        <!-- 说明卡片 -->
        <div class="p-4 mt-4">
          <div class="bg-blue-50 rounded-xl p-4 border border-blue-100">
            <div class="flex items-center gap-2 mb-2">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
              <span class="text-xs font-bold text-blue-700">物流说明</span>
            </div>
            <p class="text-xs text-blue-600 leading-relaxed">从已确认订单中选择，提交至 4PX物流 自动创建面单</p>
            <div class="mt-3 pt-3 border-t border-blue-100">
              <div class="flex items-center gap-1.5">
                <span class="w-2 h-2 rounded-full bg-green-400"></span>
                <span class="text-xs text-slate-600">4PX物流 · PX渠道</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ══ 主内容区 ══ -->
      <div class="flex-1 flex flex-col h-full overflow-hidden">

        <!-- 顶部标题栏 -->
        <div class="border-b border-slate-200 px-8 py-5 flex items-center justify-between shrink-0">
          <div>
            <h2 class="text-xl font-bold text-slate-800 flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l2-1.14"/><path d="m7.5 4.27 9 5.15"/><polyline points="3.29 7 12 12 20.71 7"/><line x1="12" x2="12" y1="22" y2="12"/><circle cx="18.5" cy="15.5" r="2.5"/><path d="M20.27 17.27 22 19"/></svg>
              物流下单
            </h2>
            <p class="text-sm text-slate-500 mt-0.5">从已确认订单中选择，提交 4PX物流 自动下单</p>
          </div>
          <div class="flex items-center gap-3">
            <span class="text-sm text-slate-500">已选择</span>
            <span class="text-lg font-bold text-blue-600">{{ selectedOrders.length }}</span>
            <span class="text-sm text-slate-500">单</span>
            <button
              @click="submitShipping"
              :disabled="selectedOrders.length === 0 || submitting"
              class="flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-semibold transition-all"
              :class="selectedOrders.length > 0 && !submitting
                ? 'bg-blue-600 text-white hover:bg-blue-700 shadow-md shadow-blue-200'
                : 'bg-slate-100 text-slate-400 cursor-not-allowed'"
            >
              <svg v-if="!submitting" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/></svg>
              <svg v-else class="animate-spin" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>
              {{ submitting ? '提交中...' : '提交物流下单' }}
            </button>
          </div>
        </div>

        <!-- 内容主体：左订单列表(40%) + 右表单(60%) -->
        <div class="flex flex-1 overflow-hidden">

          <!-- 左侧：已确认订单列表 40% -->
          <div class="w-[40%] border-r border-slate-200 flex flex-col shrink-0">
            <!-- 搜索栏 -->
            <div class="px-5 py-4 border-b border-slate-100">
              <div class="flex items-center gap-2 bg-slate-50 border border-slate-200 rounded-xl px-3 py-2">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
                <input v-model="searchQuery" type="text" placeholder="搜索订单号 / 买家名称..." class="flex-1 bg-transparent text-sm text-slate-700 placeholder-slate-400 outline-none" />
              </div>
              <div class="flex items-center justify-between mt-3">
                <span class="text-xs text-slate-500">共 <span class="font-semibold text-slate-700">{{ filteredOrders.length }}</span> 条已确认订单</span>
                <button @click="toggleSelectAll" class="text-xs text-blue-600 hover:text-blue-700 font-medium">
                  {{ selectedOrders.length === filteredOrders.length && filteredOrders.length > 0 ? '取消全选' : '全选' }}
                </button>
              </div>
            </div>

            <!-- 订单列表 -->
            <div class="flex-1 overflow-y-auto px-4 py-3 space-y-2">
              <div v-if="loading" class="flex items-center justify-center h-32">
                <div class="flex items-center gap-2 text-slate-400">
                  <svg class="animate-spin" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>
                  <span class="text-sm">加载中...</span>
                </div>
              </div>

              <div v-else-if="filteredOrders.length === 0" class="flex flex-col items-center justify-center h-32 text-slate-400">
                <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#cbd5e1" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="14" x="2" y="7" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>
                <p class="text-sm mt-2">暂无已确认订单</p>
              </div>

              <div
                v-for="order in filteredOrders"
                :key="order.id"
                @click="toggleSelect(order)"
                class="rounded-xl border p-4 cursor-pointer transition-all"
                :class="isSelected(order)
                  ? 'border-blue-400 bg-blue-50 shadow-sm shadow-blue-100'
                  : 'border-slate-200 bg-white hover:border-slate-300 hover:bg-slate-50'"
              >
                <div class="flex items-start gap-3">
                  <!-- 复选框 -->
                  <div class="mt-0.5 w-5 h-5 rounded-md border-2 flex items-center justify-center shrink-0 transition-all"
                    :class="isSelected(order) ? 'bg-blue-600 border-blue-600' : 'border-slate-300'">
                    <svg v-if="isSelected(order)" xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>
                  </div>
                  <!-- 订单信息 -->
                  <div class="flex-1 min-w-0">
                    <div class="flex items-center justify-between mb-1">
                      <span class="text-sm font-bold text-slate-800 truncate">{{ order.etsy_order_id || order.id }}</span>
                      <span class="text-xs px-2 py-0.5 rounded-full bg-green-100 text-green-700 font-medium shrink-0 ml-2">已确认</span>
                    </div>
                    <div class="flex items-center gap-1 mb-1.5">
                      <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                      <span class="text-xs text-slate-500">{{ order.buyer_name || '未知买家' }}</span>
                    </div>
                    <div class="flex items-center justify-between">
                      <div class="flex items-center gap-1">
                        <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
                        <span class="text-xs text-slate-500 truncate max-w-[160px]">{{ order.shipping_address || '地址待填写' }}</span>
                      </div>
                      <span class="text-xs text-slate-400">{{ formatDate(order.created_at) }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 右侧：物流信息填写表单 -->
          <div class="flex-1 flex flex-col overflow-hidden">
            <div class="flex-1 overflow-y-auto px-8 py-6">

              <!-- 物流渠道选择 -->
              <div class="mb-6">
                <h3 class="text-sm font-bold text-slate-700 mb-3 flex items-center gap-2">
                  <span class="w-1 h-4 bg-blue-500 rounded-full"></span>
                  物流渠道
                </h3>
                <div class="grid grid-cols-2 gap-3">
                  <div
                    @click="form.carrier = 'PX'"
                    class="rounded-xl border-2 p-4 cursor-pointer transition-all"
                    :class="form.carrier === 'PX' ? 'border-blue-500 bg-blue-50' : 'border-slate-200 hover:border-slate-300'"
                  >
                    <div class="flex items-center justify-between mb-2">
                      <span class="font-bold text-sm" :class="form.carrier === 'PX' ? 'text-blue-700' : 'text-slate-700'">4PX物流</span>
                      <div class="w-4 h-4 rounded-full border-2 flex items-center justify-center" :class="form.carrier === 'PX' ? 'border-blue-500' : 'border-slate-300'">
                        <div v-if="form.carrier === 'PX'" class="w-2 h-2 rounded-full bg-blue-500"></div>
                      </div>
                    </div>
                    <div class="text-xs text-slate-500">美国联邮通优先挂号</div>
                    <div class="mt-1.5 inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium" :class="form.carrier === 'PX' ? 'bg-blue-100 text-blue-700' : 'bg-slate-100 text-slate-500'">PX 渠道</div>
                  </div>
                  <!-- 预留扩展位 -->
                  <div class="rounded-xl border-2 border-dashed border-slate-200 p-4 flex flex-col items-center justify-center text-slate-300">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 8v8"/><path d="M8 12h8"/></svg>
                    <span class="text-xs mt-1">后续扩展</span>
                  </div>
                </div>
              </div>

              <!-- 已选订单汇总 -->
              <div class="mb-6">
                <h3 class="text-sm font-bold text-slate-700 mb-3 flex items-center gap-2">
                  <span class="w-1 h-4 bg-blue-500 rounded-full"></span>
                  已选订单（{{ selectedOrders.length }}）
                </h3>
                <div v-if="selectedOrders.length === 0" class="rounded-xl border border-dashed border-slate-200 p-6 text-center text-slate-400">
                  <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="mx-auto mb-2"><rect width="8" height="4" x="8" y="2" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/></svg>
                  <p class="text-sm">请从左侧列表选择订单</p>
                </div>
                <div v-else class="space-y-2">
                  <div v-for="order in selectedOrders" :key="order.id" class="flex items-center justify-between bg-slate-50 rounded-xl px-4 py-3 border border-slate-200">
                    <div>
                      <span class="text-sm font-semibold text-slate-800">{{ order.etsy_order_id || order.id }}</span>
                      <span class="text-xs text-slate-500 ml-2">{{ order.buyer_name }}</span>
                    </div>
                    <button @click.stop="toggleSelect(order)" class="text-slate-400 hover:text-red-500 transition-colors">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
                    </button>
                  </div>
                </div>
              </div>

              <!-- 货物信息 -->
              <div class="mb-6">
                <h3 class="text-sm font-bold text-slate-700 mb-3 flex items-center gap-2">
                  <span class="w-1 h-4 bg-blue-500 rounded-full"></span>
                  货物信息
                </h3>
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label class="text-xs font-medium text-slate-600 mb-1.5 block">件数</label>
                    <input v-model.number="form.pieces" type="number" min="1" placeholder="默认 1" class="w-full text-sm border border-slate-200 rounded-xl px-3 py-2.5 outline-none focus:border-blue-400 focus:ring-2 focus:ring-blue-50 text-slate-700" />
                  </div>
                  <div>
                    <label class="text-xs font-medium text-slate-600 mb-1.5 block">重量（克）</label>
                    <select v-model="form.weight" class="w-full text-sm border border-slate-200 rounded-xl px-3 py-2.5 bg-white text-slate-700 outline-none focus:border-blue-400 focus:ring-2 focus:ring-blue-50">
                      <option value="">请选择重量</option>
                      <optgroup label="大号（Large）">
                        <option value="45">大号款1 - 45g</option>
                        <option value="50">大号款2 - 50g</option>
                        <option value="55">大号款3 - 55g</option>
                      </optgroup>
                      <optgroup label="小号（Small）">
                        <option value="25">小号款1 - 25g</option>
                        <option value="30">小号款2 - 30g</option>
                        <option value="35">小号款3 - 35g</option>
                      </optgroup>
                    </select>
                  </div>
                </div>
                <div class="mt-3 p-3 bg-slate-50 rounded-lg border border-slate-100">
                  <div class="flex items-center gap-2 text-xs text-slate-500">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
                    <span>申报信息：Pet ID Tag / 宠物ID牌 / $1.2 / 1件（自动填充）</span>
                  </div>
                </div>
              </div>

              <!-- 发件人信息（固定） -->
              <div class="mb-6">
                <h3 class="text-sm font-bold text-slate-700 mb-3 flex items-center gap-2">
                  <span class="w-1 h-4 bg-slate-400 rounded-full"></span>
                  发件人信息
                  <span class="text-xs font-normal text-slate-400">（固定）</span>
                </h3>
                <div class="bg-slate-50 rounded-xl p-4 border border-slate-200 grid grid-cols-2 gap-3">
                  <div>
                    <span class="text-xs text-slate-400">姓名</span>
                    <p class="text-sm font-medium text-slate-700">Jarvis Schoen</p>
                  </div>
                  <div>
                    <span class="text-xs text-slate-400">电话</span>
                    <p class="text-sm font-medium text-slate-700">13923266621</p>
                  </div>
                  <div>
                    <span class="text-xs text-slate-400">国家</span>
                    <p class="text-sm font-medium text-slate-700">中国（CN）</p>
                  </div>
                  <div>
                    <span class="text-xs text-slate-400">邮编</span>
                    <p class="text-sm font-medium text-slate-700">518000</p>
                  </div>
                  <div class="col-span-2">
                    <span class="text-xs text-slate-400">地址</span>
                    <p class="text-sm font-medium text-slate-700">广东省深圳市</p>
                  </div>
                </div>
              </div>

            </div>

            <!-- 底部操作栏 -->
            <div class="border-t border-slate-200 px-8 py-4 shrink-0 bg-white">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-3">
                  <div class="flex items-center gap-1.5">
                    <div class="w-2 h-2 rounded-full bg-green-400"></div>
                    <span class="text-xs text-slate-500">渠道：4PX物流 · PX</span>
                  </div>
                  <div class="w-px h-4 bg-slate-200"></div>
                  <span class="text-xs text-slate-500">订单：{{ selectedOrders.length }} 单</span>
                  <div class="w-px h-4 bg-slate-200"></div>
                  <span class="text-xs text-slate-500">重量：{{ form.weight ? form.weight + 'g' : '未选择' }}</span>
                </div>
                <div class="flex items-center gap-3">
                  <button @click="resetForm" class="px-4 py-2 text-sm text-slate-500 hover:text-slate-700 font-medium transition-colors">
                    重置
                  </button>
                  <button
                    @click="submitShipping"
                    :disabled="selectedOrders.length === 0 || submitting"
                    class="flex items-center gap-2 px-6 py-2.5 rounded-xl text-sm font-semibold transition-all"
                    :class="selectedOrders.length > 0 && !submitting
                      ? 'bg-blue-600 text-white hover:bg-blue-700 shadow-md shadow-blue-200'
                      : 'bg-slate-100 text-slate-400 cursor-not-allowed'"
                  >
                    <svg v-if="!submitting" xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/></svg>
                    <svg v-else class="animate-spin" xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>
                    {{ submitting ? '提交中...' : '提交物流下单' }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 成功弹窗 -->
    <div v-if="showSuccess" class="fixed inset-0 bg-black/30 flex items-center justify-center z-50">
      <div class="bg-white rounded-2xl shadow-2xl p-8 w-[420px] text-center">
        <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/></svg>
        </div>
        <h3 class="text-lg font-bold text-slate-800 mb-2">下单成功</h3>
        <p class="text-sm text-slate-500 mb-1">已成功提交 <span class="font-semibold text-slate-700">{{ lastSubmitCount }}</span> 个订单至 4PX物流</p>
        <p class="text-sm text-slate-500 mb-6">订单状态已更新为「待发货」</p>
        <button @click="showSuccess = false; $router.push('/logistics')" class="w-full py-2.5 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700 transition-colors">
          查看物流追踪
        </button>
      </div>
    </div>

    <!-- 错误提示 -->
    <div v-if="errorMsg" class="fixed bottom-6 right-6 bg-red-50 border border-red-200 rounded-xl px-5 py-4 shadow-lg flex items-center gap-3 z-50 max-w-sm">
      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="m15 9-6 6"/><path d="m9 9 6 6"/></svg>
      <span class="text-sm text-red-700 flex-1">{{ errorMsg }}</span>
      <button @click="errorMsg = ''" class="text-red-400 hover:text-red-600">
        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useOrderStore } from '../../stores/orderStore'

const store = useOrderStore()

// ── 状态 ──
const loading = ref(false)
const submitting = ref(false)
const showSuccess = ref(false)
const errorMsg = ref('')
const lastSubmitCount = ref(0)
const searchQuery = ref('')
const selectedOrders = ref([])

// 表单
const form = ref({
  pieces: 1,
  weight: '',
})

function resetForm() {
  selectedOrders.value = []
  searchQuery.value = ''
  form.value = { pieces: 1, weight: '' }
}

// ── 已确认订单 ──
const confirmedOrders = ref([])

const pendingCount = computed(() =>
  store.orders.filter(o => o.status === 'pending').length
)

const filteredOrders = computed(() => {
  const q = searchQuery.value.toLowerCase()
  if (!q) return confirmedOrders.value
  return confirmedOrders.value.filter(o =>
    (o.etsy_order_id || '').toLowerCase().includes(q) ||
    (o.buyer_name || '').toLowerCase().includes(q)
  )
})

// ── 方法 ──
function isSelected(order) {
  return selectedOrders.value.some(o => o.id === order.id)
}

function toggleSelect(order) {
  const idx = selectedOrders.value.findIndex(o => o.id === order.id)
  if (idx >= 0) {
    selectedOrders.value.splice(idx, 1)
  } else {
    selectedOrders.value.push(order)
  }
}

function toggleSelectAll() {
  if (selectedOrders.value.length === filteredOrders.value.length && filteredOrders.value.length > 0) {
    selectedOrders.value = []
  } else {
    selectedOrders.value = [...filteredOrders.value]
  }
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return `${d.getMonth() + 1}/${d.getDate()}`
}

async function submitShipping() {
  if (selectedOrders.value.length === 0) return
  submitting.value = true
  errorMsg.value = ''

  try {
    // 模拟提交（4PX签名问题解决后替换为真实API调用）
    await new Promise(resolve => setTimeout(resolve, 1500))

    // 更新订单状态为「待发货」（前端本地模拟）
    lastSubmitCount.value = selectedOrders.value.length
    selectedOrders.value = []
    showSuccess.value = true

  } catch (e) {
    errorMsg.value = '下单失败，请检查网络或联系技术支持'
    setTimeout(() => { errorMsg.value = '' }, 4000)
  } finally {
    submitting.value = false
  }
}

// ── 加载数据 ──
onMounted(async () => {
  loading.value = true
  try {
    await store.fetchOrders()
    // 筛选已确认订单（status === 'confirmed'）
    confirmedOrders.value = store.orders.filter(o => o.status === 'confirmed')
  } catch (e) {
    console.error('加载订单失败:', e)
  } finally {
    loading.value = false
  }
})
</script>
