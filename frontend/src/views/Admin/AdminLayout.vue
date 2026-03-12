<template>
  <div class="min-h-screen bg-slate-50 flex">
    <!-- 侧边导航 -->
    <aside class="w-64 bg-slate-900 text-white flex flex-col">
      <!-- Logo -->
      <div class="p-6 border-b border-slate-800">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
              <rect width="7" height="9" x="3" y="3" rx="1"/>
              <rect width="7" height="5" x="14" y="3" rx="1"/>
              <rect width="7" height="9" x="14" y="12" rx="1"/>
              <rect width="7" height="5" x="3" y="16" rx="1"/>
            </svg>
          </div>
          <div>
            <h1 class="font-bold">管理系统</h1>
            <p class="text-xs text-slate-400">Management Panel</p>
          </div>
        </div>
      </div>

      <!-- 导航菜单 -->
      <nav class="flex-1 p-4 space-y-1 overflow-y-auto">
        <!-- 7项核心工作流导航 -->
        <div class="mb-4">
          <p class="px-4 py-2 text-xs text-slate-500 uppercase tracking-wider">订单工作流</p>
          
          <router-link 
            to="/admin/dashboard"
            :class="[isActive('/admin/dashboard') ? 'bg-blue-600' : 'hover:bg-slate-800']"
            class="flex items-center gap-3 px-4 py-3 rounded-xl transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect width="7" height="9" x="3" y="3" rx="1"/>
              <rect width="7" height="5" x="14" y="3" rx="1"/>
              <rect width="7" height="9" x="14" y="12" rx="1"/>
              <rect width="7" height="5" x="3" y="16" rx="1"/>
            </svg>
            <span>仪表盘总览</span>
          </router-link>

          <router-link 
            to="/admin/orders/pending"
            :class="[isActive('/admin/orders/pending') ? 'bg-blue-600' : 'hover:bg-slate-800']"
            class="flex items-center gap-3 px-4 py-3 rounded-xl transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <path d="M12 6v6l4 2"/>
            </svg>
            <span>待确认订单</span>
            <span v-if="pendingCount > 0" class="ml-auto bg-red-500 text-xs px-2 py-0.5 rounded-full">{{ pendingCount }}</span>
          </router-link>

          <router-link 
            to="/admin/orders/shipping"
            :class="[isActive('/admin/orders/shipping') ? 'bg-blue-600' : 'hover:bg-slate-800']"
            class="flex items-center gap-3 px-4 py-3 rounded-xl transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M5 18H3c-.6 0-1-.4-1-1V7c0-.6.4-1 1-1h10c.6 0 1 .4 1 1v11"/>
              <path d="M14 9h4l4 4v6h-4"/>
              <circle cx="7" cy="18" r="2"/>
              <circle cx="17" cy="18" r="2"/>
            </svg>
            <span>物流下单</span>
          </router-link>

          <router-link 
            to="/admin/orders/producing"
            :class="[isActive('/admin/orders/producing') ? 'bg-blue-600' : 'hover:bg-slate-800']"
            class="flex items-center gap-3 px-4 py-3 rounded-xl transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="m15 12-9.373 9.373a1 1 0 0 1-3.001-3L12 9"/>
              <path d="m18 15 4-4"/>
              <path d="m21.5 11.5-1.914-1.914A2 2 0 0 1 19 8.172v-.344a2 2 0 0 0-.586-1.414l-1.657-1.657A6 6 0 0 0 12.516 3H9l1.243 1.243A6 6 0 0 1 12 8.485V10l2 2h1.172a2 2 0 0 1 1.414.586L18.5 14.5"/>
            </svg>
            <span>生产中订单</span>
          </router-link>

          <router-link 
            to="/admin/orders/completed"
            :class="[isActive('/admin/orders/completed') ? 'bg-blue-600' : 'hover:bg-slate-800']"
            class="flex items-center gap-3 px-4 py-3 rounded-xl transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21.801 10A10 10 0 1 1 17 3.335"/>
              <path d="m9 11 3 3L22 4"/>
            </svg>
            <span>已完成订单</span>
          </router-link>

          <router-link 
            to="/admin/templates"
            :class="[isActive('/admin/templates') ? 'bg-blue-600' : 'hover:bg-slate-800']"
            class="flex items-center gap-3 px-4 py-3 rounded-xl transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="m22 7-8.991 5.727a2 2 0 0 1-2.009 0L2 7"/>
              <rect x="2" y="4" width="20" height="16" rx="2"/>
            </svg>
            <span>邮件模板</span>
          </router-link>

          <router-link 
            to="/admin/factory-overview"
            :class="[isActive('/admin/factory-overview') ? 'bg-blue-600' : 'hover:bg-slate-800']"
            class="flex items-center gap-3 px-4 py-3 rounded-xl transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 10V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l2-1.14"/>
              <path d="m7.5 4.27 9 5.15"/>
              <polyline points="3.29 7 12 12 20.71 7"/>
              <line x1="12" x2="12" y1="22" y2="12"/>
            </svg>
            <span>工厂生产总览</span>
          </router-link>
        </div>

        <!-- 系统管理（仅主账号可见） -->
        <div v-if="isMainAccount" class="mt-6 pt-6 border-t border-slate-800">
          <p class="px-4 py-2 text-xs text-slate-500 uppercase tracking-wider">系统管理</p>
          
          <router-link 
            to="/admin/shops"
            :class="[isActive('/admin/shops') ? 'bg-blue-600' : 'hover:bg-slate-800']"
            class="flex items-center gap-3 px-4 py-3 rounded-xl transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
              <polyline points="9 22 9 12 15 12 15 22"/>
            </svg>
            <span>店铺管理</span>
          </router-link>

          <router-link 
            to="/admin/users"
            :class="[isActive('/admin/users') ? 'bg-blue-600' : 'hover:bg-slate-800']"
            class="flex items-center gap-3 px-4 py-3 rounded-xl transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>
              <circle cx="9" cy="7" r="4"/>
              <path d="M22 21v-2a4 4 0 0 0-3-3.87"/>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
            </svg>
            <span>子账号管理</span>
          </router-link>

          <router-link 
            to="/admin/factories"
            :class="[isActive('/admin/factories') ? 'bg-blue-600' : 'hover:bg-slate-800']"
            class="flex items-center gap-3 px-4 py-3 rounded-xl transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M2 22h20"/>
              <path d="M6 22V10l6-4 6 4v12"/>
              <path d="M10 22v-6h4v6"/>
            </svg>
            <span>工厂管理</span>
          </router-link>

          <router-link 
            to="/admin/settings"
            :class="[isActive('/admin/settings') ? 'bg-blue-600' : 'hover:bg-slate-800']"
            class="flex items-center gap-3 px-4 py-3 rounded-xl transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="3"/>
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
            </svg>
            <span>系统设置</span>
          </router-link>
        </div>
      </nav>

      <!-- 底部用户信息 -->
      <div class="p-4 border-t border-slate-800">
        <div class="flex items-center gap-3 mb-3">
          <div class="w-10 h-10 rounded-full bg-blue-600 flex items-center justify-center">
            <span class="font-bold">{{ adminStore.currentUser?.username?.[0]?.toUpperCase() || 'A' }}</span>
          </div>
          <div class="flex-1 min-w-0">
            <p class="font-medium truncate">{{ adminStore.currentUser?.username || 'Admin' }}</p>
            <p class="text-xs text-slate-400">{{ isMainAccount ? '主账号' : '子账号' }}</p>
          </div>
        </div>
        <button 
          @click="handleLogout"
          class="w-full py-2 bg-slate-800 hover:bg-slate-700 rounded-lg text-sm transition-colors"
        >
          退出登录
        </button>
      </div>
    </aside>

    <!-- 主内容区 -->
    <main class="flex-1 overflow-auto bg-slate-50">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAdminStore } from '../../stores/adminStore'

const route = useRoute()
const router = useRouter()
const adminStore = useAdminStore()

// 判断是否主账号
const isMainAccount = computed(() => {
  return adminStore.currentUser?.role_type === 'main'
})

// 待确认订单数量（示例）
const pendingCount = computed(() => {
  return 5 // 实际应从store获取
})

// 判断当前路由是否激活
function isActive(path) {
  return route.path === path || route.path.startsWith(path + '/')
}

function handleLogout() {
  adminStore.logout()
  router.push('/admin/login')
}
</script>