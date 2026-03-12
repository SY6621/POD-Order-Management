<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <!-- Logo区域 -->
      <div class="text-center mb-8">
        <div class="w-16 h-16 bg-blue-600 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg">
          <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
            <polyline points="9 22 9 12 15 12 15 22"/>
          </svg>
        </div>
        <h1 class="text-2xl font-bold text-slate-800">店铺协作平台</h1>
        <p class="text-slate-500 mt-1">Store Collaboration Portal</p>
      </div>

      <!-- 店铺选择 -->
      <div v-if="!selectedShop" class="bg-white rounded-2xl shadow-xl p-6">
        <h2 class="text-lg font-semibold text-slate-800 mb-4">选择您的店铺</h2>
        <div class="space-y-3">
          <button 
            v-for="shop in shops" 
            :key="shop.code"
            @click="selectShop(shop)"
            class="w-full flex items-center gap-4 p-4 rounded-xl border-2 border-slate-100 hover:border-blue-500 hover:bg-blue-50 transition-all group"
          >
            <div class="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center group-hover:bg-blue-100">
              <span class="text-xl font-bold text-slate-600 group-hover:text-blue-600">{{ shop.code.toUpperCase() }}</span>
            </div>
            <div class="text-left">
              <p class="font-semibold text-slate-800">{{ shop.name }}</p>
              <p class="text-sm text-slate-500">{{ shop.region }}</p>
            </div>
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="ml-auto text-slate-400 group-hover:text-blue-500">
              <path d="m9 18 6-6-6-6"/>
            </svg>
          </button>
        </div>
      </div>

      <!-- 密码输入 -->
      <div v-else class="bg-white rounded-2xl shadow-xl p-6">
        <button 
          @click="selectedShop = null"
          class="text-sm text-slate-500 hover:text-slate-700 flex items-center gap-1 mb-4"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="m15 18-6-6 6-6"/>
          </svg>
          返回选择
        </button>

        <div class="text-center mb-6">
          <div class="w-16 h-16 rounded-full bg-blue-100 flex items-center justify-center mx-auto mb-3">
            <span class="text-2xl font-bold text-blue-600">{{ selectedShop.code.toUpperCase() }}</span>
          </div>
          <h2 class="text-lg font-semibold text-slate-800">{{ selectedShop.name }}</h2>
          <p class="text-sm text-slate-500">请输入访问密码</p>
        </div>

        <form @submit.prevent="handleLogin">
          <div class="mb-4">
            <input 
              v-model="password"
              type="password"
              placeholder="输入密码"
              class="w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition-all text-center text-lg tracking-widest"
              :class="{ 'border-red-500': error }"
            >
            <p v-if="error" class="text-red-500 text-sm mt-2 text-center">{{ error }}</p>
          </div>

          <button 
            type="submit"
            :disabled="!password || loading"
            class="w-full py-3 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          >
            {{ loading ? '验证中...' : '进入店铺' }}
          </button>
        </form>

        <p class="text-xs text-slate-400 text-center mt-4">
          忘记密码请联系系统管理员
        </p>
      </div>

      <!-- 底部信息 -->
      <div class="text-center mt-8">
        <p class="text-sm text-slate-500">
          中央管理系统 
          <a href="/" class="text-blue-600 hover:underline">返回后台</a>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useShopStore } from '../../stores/shopStore'

const route = useRoute()
const router = useRouter()
const shopStore = useShopStore()

// 状态
const shops = ref([])
const selectedShop = ref(null)
const password = ref('')
const loading = ref(false)
const error = ref('')

// 加载店铺列表
onMounted(async () => {
  try {
    shops.value = await shopStore.fetchShops()
    
    // 如果URL中有店铺代码，自动选择
    const shopCode = route.params.shopCode
    if (shopCode) {
      const shop = shops.value.find(s => s.code === shopCode)
      if (shop) {
        selectedShop.value = shop
      }
    }
  } catch (err) {
    console.error('加载店铺失败:', err)
  }
})

// 选择店铺
function selectShop(shop) {
  selectedShop.value = shop
  error.value = ''
  password.value = ''
}

// 登录处理
async function handleLogin() {
  if (!password.value) return
  
  loading.value = true
  error.value = ''
  
  try {
    const result = await shopStore.login(selectedShop.value.code, password.value)
    
    if (result.success) {
      // 登录成功，跳转到店铺首页
      router.push(`/store/${selectedShop.value.code}/orders`)
    } else {
      error.value = '密码错误，请重试'
    }
  } catch (err) {
    error.value = '登录失败，请稍后重试'
    console.error('登录错误:', err)
  } finally {
    loading.value = false
  }
}
</script>