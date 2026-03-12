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
          <button @click="$router.push('/')" class="w-full flex items-center justify-between px-4 py-3 rounded-xl transition-colors text-slate-600 hover:bg-slate-50">
            <div class="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/></svg>
              <span class="font-medium">仪表盘总览</span>
            </div>
          </button>
          <button @click="$router.push('/pending')" class="w-full flex items-center justify-between px-4 py-3 rounded-xl transition-colors text-slate-600 hover:bg-slate-50">
            <div class="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="8" height="4" x="8" y="2" rx="1" ry="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="M12 11h4"/><path d="M12 16h4"/><path d="M8 11h.01"/><path d="M8 16h.01"/></svg>
              <span class="font-medium">待确认订单</span>
            </div>
            <span class="text-xs font-bold px-2 py-0.5 rounded-full bg-slate-100 text-slate-600">{{ pendingCount }}</span>
          </button>
          <!-- 物流下单 -->
          <button @click="$router.push('/shipping')" class="w-full flex items-center justify-between px-4 py-3 rounded-xl transition-colors text-slate-600 hover:bg-slate-50">
            <div class="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l2-1.14"/><path d="m7.5 4.27 9 5.15"/><polyline points="3.29 7 12 12 20.71 7"/><line x1="12" x2="12" y1="22" y2="12"/><circle cx="18.5" cy="15.5" r="2.5"/><path d="M20.27 17.27 22 19"/></svg>
              <span class="font-medium">物流下单</span>
            </div>
          </button>
          <button @click="$router.push('/production')" class="w-full flex items-center justify-between px-4 py-3 rounded-xl transition-colors text-slate-600 hover:bg-slate-50">
            <div class="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 12-8.5 8.5c-.83.83-2.17.83-3 0 0 0 0 0 0 0a2.12 2.12 0 0 1 0-3L12 9"/><path d="M17.64 15 22 10.64"/><path d="m20.91 11.7-1.25-1.25c-.6-.6-.93-1.4-.93-2.25V7.86c0-.55-.45-1-1-1H14.5c-.85 0-1.65-.33-2.25-.93L11 4.71"/><path d="M5.8 5.81a2.2 2.2 0 0 1 3.1 0l1.3 1.3"/></svg>
              <span class="font-medium">生产中订单</span>
            </div>
            <span class="text-xs font-bold px-2 py-0.5 rounded-full bg-slate-100 text-slate-600">{{ producingCount }}</span>
          </button>
          <button @click="$router.push('/completed')" class="w-full flex items-center justify-between px-4 py-3 rounded-xl transition-colors text-slate-600 hover:bg-slate-50">
            <div class="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/></svg>
              <span class="font-medium">已完成订单</span>
            </div>
          </button>
          <!-- 物流追踪 Active -->
          <button class="w-full flex items-center justify-between px-4 py-3 rounded-xl bg-blue-50 text-blue-600">
            <div class="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H9"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.624l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/></svg>
              <span class="font-medium">物流追踪</span>
            </div>
            <span class="text-xs font-bold px-2 py-0.5 rounded-full bg-blue-200 text-blue-700">8</span>
          </button>
          <button @click="$router.push('/email')" class="w-full flex items-center justify-between px-4 py-3 rounded-xl transition-colors text-slate-600 hover:bg-slate-50">
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
                <span class="text-lg font-bold z-10 text-orange-600">{{ pendingCount }}</span>
              </div>
              <span class="text-xs font-medium text-slate-600">新订单</span>
              <span class="text-[10px] text-slate-400">顲24h回复</span>
            </div>
            <div class="bg-white border border-slate-200 rounded-xl p-3 shadow-sm flex flex-col items-center justify-center text-center">
              <div class="relative w-20 h-20 flex items-center justify-center mb-1">
                <svg width="80" height="80" viewBox="0 0 80 80" class="absolute transform -rotate-90">
                  <circle cx="40" cy="40" r="28" stroke="#e2e8f0" stroke-width="5" fill="transparent"/>
                  <circle cx="40" cy="40" r="28" stroke="#a855f7" stroke-width="5" fill="transparent" stroke-dasharray="175.93" stroke-dashoffset="144.26" stroke-linecap="round"/>
                </svg>
                <span class="text-lg font-bold z-10 text-purple-600">{{ producingCount }}</span>
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
                <span class="text-lg font-bold z-10 text-green-600">50%</span>
              </div>
              <span class="text-xs font-medium text-slate-600">已交付</span>
              <span class="text-[10px] text-slate-400">物流送达</span>
            </div>
          </div>
        </div>

        <!-- 运输中小列表 -->
        <div class="p-4 mt-auto">
          <div class="flex items-center justify-between mb-3">
            <h3 class="text-sm font-bold text-slate-700">运输中</h3>
            <span class="bg-blue-100 text-blue-600 text-xs px-2 py-0.5 rounded-full">8单</span>
          </div>
          <div class="space-y-3">
            <div v-for="item in sidebarShipments" :key="item.id"
              :class="item.overdue ? 'bg-orange-50 border-orange-100' : 'bg-slate-50 border-slate-100'"
              class="p-3 rounded-lg border">
              <div class="flex justify-between items-start mb-1">
                <span class="text-xs font-bold text-slate-800">{{ item.id }}</span>
                <span :class="item.overdue ? 'text-orange-500' : 'text-blue-500'" class="text-[10px] font-medium">{{ item.statusLabel }}</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-xs text-slate-600">{{ item.customer }}</span>
                <span class="text-[10px] text-slate-400">{{ item.carrier }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 中间：运单列表 -->
      <div class="w-[480px] bg-slate-50 border-r border-slate-200 flex flex-col h-full overflow-y-auto shrink-0">
        <div class="p-4 pb-3 border-b border-slate-200 bg-white">
          <div class="flex items-center justify-between mb-1">
            <h2 class="text-base font-bold text-slate-800">物流追踪</h2>
            <span class="bg-blue-100 text-blue-600 px-2 py-0.5 rounded-full text-xs font-bold">8 单在途</span>
          </div>
          <p class="text-[11px] text-slate-400">点击运单查看实时轨迹</p>
        </div>

        <div class="p-4 space-y-3">
          <!-- 详细卡片（前3条） -->
          <div v-for="ship in detailShipments" :key="ship.id"
            @click="selectShipment(ship)"
            :class="[
              'rounded-xl p-3 cursor-pointer transition-colors',
              selectedShipment?.id === ship.id
                ? (ship.overdue ? 'bg-orange-50 border-2 border-orange-400' : 'bg-white border-2 border-blue-500')
                : (ship.overdue ? 'bg-orange-50 border border-orange-200 hover:border-orange-400' : 'bg-white border border-slate-200 hover:border-blue-300')
            ]">
            <div class="flex items-start justify-between mb-2">
              <div>
                <div class="flex items-center gap-2 mb-0.5">
                  <span class="text-xs font-bold text-slate-800">{{ ship.id }}</span>
                  <span :class="ship.overdue ? 'bg-orange-100 text-orange-600' : 'bg-blue-100 text-blue-600'"
                    class="px-1.5 py-0.5 rounded text-[10px] font-bold">{{ ship.statusLabel }}</span>
                </div>
                <div class="text-[11px] text-slate-500">{{ ship.customer }} · {{ ship.carrier }}</div>
              </div>
              <div class="text-right">
                <div :class="ship.overdue ? 'text-orange-600' : 'text-blue-600'" class="text-[11px] font-mono">{{ ship.trackingNo }}</div>
                <div :class="ship.overdue ? 'text-orange-500 font-medium' : 'text-slate-400'" class="text-[10px] mt-0.5">{{ ship.etaLabel }}</div>
              </div>
            </div>
            <div class="flex items-center gap-2">
              <div class="flex-1 rounded-full h-1.5" :class="ship.overdue ? 'bg-orange-100' : 'bg-slate-100'">
                <div :style="{ width: ship.progress + '%' }"
                  :class="ship.overdue ? 'bg-orange-500' : 'bg-blue-500'"
                  class="h-1.5 rounded-full"></div>
              </div>
              <span :class="ship.overdue ? 'text-orange-600' : 'text-blue-600'" class="text-[10px] font-medium">{{ ship.progress }}%</span>
            </div>
            <div class="flex justify-between mt-1">
              <span v-for="(step, i) in ship.steps" :key="i"
                :class="step.active ? (ship.overdue ? 'text-orange-600 font-medium' : 'text-blue-600 font-medium') : (step.done ? 'text-slate-400' : 'text-slate-300')"
                class="text-[10px]">{{ step.label }}</span>
            </div>
          </div>

          <!-- 紧凑卡片（后4条） -->
          <div v-for="ship in compactShipments" :key="ship.id"
            @click="selectShipment(ship)"
            :class="[
              'bg-white border rounded-xl p-4 cursor-pointer transition-colors',
              selectedShipment?.id === ship.id ? 'border-2 border-blue-500' : 'border-slate-200 hover:border-blue-300'
            ]">
            <div class="flex items-center justify-between">
              <div>
                <span class="text-sm font-bold text-slate-800">{{ ship.id }}</span>
                <span :class="ship.delivered ? 'bg-green-100 text-green-700' : 'bg-blue-100 text-blue-600'"
                  class="ml-2 px-1.5 py-0.5 rounded text-[10px] font-bold">{{ ship.statusLabel }}</span>
              </div>
              <div class="text-right">
                <div class="text-xs font-mono text-slate-500">{{ ship.trackingNo }}</div>
                <div :class="ship.delivered ? 'text-green-600' : 'text-slate-400'" class="text-[10px] mt-0.5">{{ ship.etaLabel }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧：物流时间线详情 -->
      <div class="flex-1 bg-white flex flex-col h-full overflow-y-auto">
        <template v-if="selectedShipment">
          <!-- 详情头部 -->
          <div class="p-4 border-b border-slate-100">
            <div class="flex items-start justify-between">
              <div>
                <div class="flex items-center gap-2 mb-1">
                  <h3 class="text-base font-bold text-slate-800">{{ selectedShipment.id }}</h3>
                  <span :class="selectedShipment.overdue ? 'bg-orange-100 text-orange-600' : 'bg-blue-100 text-blue-600'"
                    class="px-2 py-0.5 rounded-full text-xs font-bold">{{ selectedShipment.statusLabel }}</span>
                </div>
                <div class="text-xs text-slate-500">{{ selectedShipment.customer }} · {{ selectedShipment.carrier }}</div>
              </div>
              <div class="text-right">
                <div class="text-[10px] text-slate-400 mb-1">运单号</div>
                <div class="font-mono text-xs text-blue-600 font-bold">{{ selectedShipment.trackingNo }}</div>
                <button class="mt-1 text-[10px] text-slate-400 hover:text-blue-600 flex items-center gap-1 ml-auto">
                  <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>
                  复制运单号
                </button>
              </div>
            </div>
            <div class="mt-3 grid grid-cols-3 gap-3">
              <div class="bg-slate-50 rounded-xl p-2.5 text-center">
                <div class="text-[10px] text-slate-400 mb-0.5">发货日期</div>
                <div class="text-xs font-bold text-slate-700">{{ selectedShipment.shipDate }}</div>
              </div>
              <div class="bg-blue-50 rounded-xl p-2.5 text-center">
                <div class="text-[10px] text-blue-400 mb-0.5">预计送达</div>
                <div class="text-xs font-bold text-blue-700">{{ selectedShipment.eta }}</div>
              </div>
              <div class="bg-slate-50 rounded-xl p-2.5 text-center">
                <div class="text-[10px] text-slate-400 mb-0.5">收件地址</div>
                <div class="text-xs font-bold text-slate-700">{{ selectedShipment.destination }}</div>
              </div>
            </div>
          </div>

          <!-- 物流时间线 -->
          <div class="p-4 flex-1">
            <h4 class="text-xs font-bold text-slate-700 mb-4 flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
              实时轨迹
            </h4>
            <div class="space-y-0">
              <div v-for="(step, index) in selectedShipment.timeline" :key="index" class="flex gap-4">
                <div class="flex flex-col items-center">
                  <div :class="step.iconBg" class="w-8 h-8 rounded-full flex items-center justify-center shrink-0" v-html="step.icon"></div>
                  <div v-if="index < selectedShipment.timeline.length - 1"
                    :class="step.lineColor"
                    class="w-px flex-1 mt-1.5 mb-1.5 min-h-[32px]"></div>
                </div>
                <div :class="index < selectedShipment.timeline.length - 1 ? 'pb-4 pt-0.5' : 'pt-0.5'">
                  <div class="flex items-center gap-2 mb-0.5">
                    <span :class="step.titleColor" class="text-xs font-bold">{{ step.title }}</span>
                    <span v-if="step.current" class="text-[10px] bg-blue-100 text-blue-600 px-2 py-0.5 rounded-full font-bold">当前</span>
                  </div>
                  <div class="text-[11px] text-slate-400 mb-1.5">{{ step.time }}</div>
                  <div v-if="step.detail" :class="step.detailBg" class="rounded-lg p-2.5 text-[11px] text-slate-600">
                    {{ step.detail }}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 操作按钮 -->
          <div class="p-4 border-t border-slate-100">
            <div class="flex gap-3">
              <button class="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2.5 rounded-xl font-medium text-xs flex items-center justify-center gap-2 transition-all">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
                刷新轨迹
              </button>
              <button class="flex-1 bg-white border border-slate-200 hover:bg-slate-50 text-slate-600 py-2.5 rounded-xl font-medium text-xs flex items-center justify-center gap-2 transition-all">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
                通知客户
              </button>
            </div>
          </div>
        </template>

        <!-- 未选中提示 -->
        <div v-else class="flex-1 flex flex-col items-center justify-center text-slate-400">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#cbd5e1" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="mb-3"><path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H9"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.624l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/></svg>
          <p class="text-sm">点击左侧运单查看实时轨迹</p>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useOrderStore } from '../../stores/orderStore'

const store = useOrderStore()

// 页面加载时获取订单数据（用于导航栏统计）
onMounted(() => {
  store.fetchOrders()
})

// 导航栏各状态订单数量
const pendingCount = computed(() =>
  store.orders.filter(o => ['pending', 'effect_sent'].includes(o.status)).length
)
const producingCount = computed(() =>
  store.orders.filter(o => o.status === 'producing').length
)

const iconTruck = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H9"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.624l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/></svg>'
const iconPin  = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>'
const iconArrow = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>'
const iconBox  = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="12" x="2" y="6" rx="2"/><circle cx="12" cy="12" r="2"/><path d="M6 12h.01M18 12h.01"/></svg>'
const iconWrench = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 12-8.5 8.5c-.83.83-2.17.83-3 0a2.12 2.12 0 0 1 0-3L12 9"/><path d="M17.64 15 22 10.64"/></svg>'

const defaultTimeline = [
  { iconBg:'bg-blue-600', icon:iconTruck, lineColor:'bg-blue-200', title:'快递员正在派送', titleColor:'text-blue-700', current:true,  time:'2026-03-03 08:15', detail:'快递员 John M. 已取件，正驶往 235 W 48th St, New York', detailBg:'bg-blue-50 border border-blue-100' },
  { iconBg:'bg-blue-400', icon:iconPin,   lineColor:'bg-slate-200', title:'到达目的城市分拣中心', titleColor:'text-slate-700', current:false, time:'2026-03-02 22:30 · Queens, NY', detail:'包裹已扫描入库，等待次日派送', detailBg:'bg-slate-50' },
  { iconBg:'bg-slate-300', icon:iconArrow,lineColor:'bg-slate-200', title:'离开转运中心', titleColor:'text-slate-600', current:false, time:'2026-03-01 14:20 · Philadelphia, PA', detail:'包裹已装载航班 FX4521，预计当日到达纽约', detailBg:'bg-slate-50' },
  { iconBg:'bg-slate-300', icon:iconBox,  lineColor:'bg-slate-200', title:'到达转运中心', titleColor:'text-slate-600', current:false, time:'2026-02-28 06:45 · Memphis, TN', detail:'经 FedEx World Hub 转运，等待中转', detailBg:'bg-slate-50' },
  { iconBg:'bg-slate-300', icon:iconWrench,lineColor:'', title:'已揽收', titleColor:'text-slate-600', current:false, time:'2026-02-08 16:00 · Los Angeles, CA', detail:'', detailBg:'' },
]

const sidebarShipments = [
  { id:'#PO-2602-003', customer:'Alice Cooper', carrier:'FedEx', statusLabel:'派送中', overdue:false },
  { id:'#PO-2602-005', customer:'Sarah Brooks', carrier:'DHL',   statusLabel:'运输中', overdue:false },
  { id:'#PO-2601-045', customer:'Robert Lee',   carrier:'UPS',   statusLabel:'⚠ 超时', overdue:true  },
]

const detailShipments = ref([
  {
    id:'#PO-2602-003', customer:'Alice Cooper', carrier:'FedEx', trackingNo:'7489876543210',
    statusLabel:'派送中', overdue:false, progress:80, etaLabel:'预计 03-03 送达',
    shipDate:'2026-02-08', eta:'2026-03-03', destination:'New York, NY',
    steps:[
      {label:'已揽收',done:true,active:false},{label:'转运',done:true,active:false},
      {label:'到达',done:true,active:false},{label:'派送中',done:false,active:true},{label:'已签收',done:false,active:false}
    ],
    timeline: defaultTimeline
  },
  {
    id:'#PO-2602-005', customer:'Sarah Brooks', carrier:'DHL', trackingNo:'1234567890',
    statusLabel:'运输中', overdue:false, progress:55, etaLabel:'预计 03-05 送达',
    shipDate:'2026-02-10', eta:'2026-03-05', destination:'Chicago, IL',
    steps:[
      {label:'已揽收',done:true,active:false},{label:'转运',done:true,active:false},
      {label:'到达',done:false,active:true},{label:'派送中',done:false,active:false},{label:'已签收',done:false,active:false}
    ],
    timeline: defaultTimeline
  },
  {
    id:'#PO-2601-045', customer:'Robert Lee', carrier:'UPS', trackingNo:'1Z999AA1087654321',
    statusLabel:'⚠ 超时', overdue:true, progress:40, etaLabel:'超预计 2 天',
    shipDate:'2026-01-28', eta:'2026-03-01', destination:'Houston, TX',
    steps:[
      {label:'已揽收',done:true,active:false},{label:'转运中',done:false,active:true},
      {label:'到达',done:false,active:false},{label:'派送中',done:false,active:false},{label:'已签收',done:false,active:false}
    ],
    timeline: defaultTimeline
  },
])

const compactShipments = ref([
  { id:'#PO-2602-008', trackingNo:'9400111899223456782', statusLabel:'已签收', delivered:true,  etaLabel:'签收于 03-01' },
  { id:'#PO-2602-009', trackingNo:'1Z999AA1012345680',   statusLabel:'已揽收', delivered:false, etaLabel:'预计 03-06' },
  { id:'#PO-2602-010', trackingNo:'7489876543220',       statusLabel:'运输中', delivered:false, etaLabel:'预计 03-07' },
  { id:'#PO-2602-011', trackingNo:'1234567895',          statusLabel:'运输中', delivered:false, etaLabel:'预计 03-08' },
])

const selectedShipment = ref(detailShipments.value[0])

function selectShipment(ship) {
  selectedShipment.value = ship
}
</script>
