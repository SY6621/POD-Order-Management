<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <!-- Logo区域 -->
      <div class="text-center mb-8">
        <div class="w-20 h-20 bg-white/10 backdrop-blur rounded-2xl flex items-center justify-center mx-auto mb-4 border border-white/20">
          <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect width="7" height="9" x="3" y="3" rx="1"/>
            <rect width="7" height="5" x="14" y="3" rx="1"/>
            <rect width="7" height="9" x="14" y="12" rx="1"/>
            <rect width="7" height="5" x="3" y="16" rx="1"/>
          </svg>
        </div>
        <h1 class="text-3xl font-bold text-white">管理系统</h1>
        <p class="text-blue-200 mt-2">Management System</p>
      </div>

      <!-- 登录表单 -->
      <div class="bg-white/10 backdrop-blur-lg rounded-2xl border border-white/20 p-8">
        <form @submit.prevent="handleLogin">
          <div class="mb-4">
            <label class="block text-sm font-medium text-blue-200 mb-2">用户名</label>
            <input 
              v-model="username"
              type="text"
              placeholder="输入用户名"
              class="w-full px-4 py-3 rounded-xl bg-white/10 border border-white/20 text-white placeholder-blue-300/50 focus:border-blue-400 focus:ring-2 focus:ring-blue-400/20 outline-none transition-all"
              :class="{ 'border-red-400': error }"
            >
          </div>

          <div class="mb-6">
            <label class="block text-sm font-medium text-blue-200 mb-2">密码</label>
            <input 
              v-model="password"
              type="password"
              placeholder="输入密码"
              class="w-full px-4 py-3 rounded-xl bg-white/10 border border-white/20 text-white placeholder-blue-300/50 focus:border-blue-400 focus:ring-2 focus:ring-blue-400/20 outline-none transition-all"
              :class="{ 'border-red-400': error }"
            >
          </div>

          <p v-if="error" class="text-red-400 text-sm mb-4 text-center">{{ error }}</p>

          <button 
            type="submit"
            :disabled="!username || !password || loading"
            class="w-full py-3 bg-blue-600 hover:bg-blue-500 text-white rounded-xl font-semibold transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ loading ? '登录中...' : '登录系统' }}
          </button>
        </form>


      </div>

      <!-- 底部信息 -->
      <div class="text-center mt-8">
        <p class="text-sm text-blue-400">
          ETSY订单自动化系统 v2.0
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAdminStore } from '../../stores/adminStore'

const router = useRouter()
const adminStore = useAdminStore()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  if (!username.value || !password.value) return
  
  loading.value = true
  error.value = ''
  
  try {
    const result = await adminStore.login(username.value, password.value)
    
    if (result.success) {
      router.push('/admin/dashboard')
    } else {
      error.value = result.message || '登录失败'
    }
  } catch (err) {
    error.value = '系统错误，请稍后重试'
    console.error('登录错误:', err)
  } finally {
    loading.value = false
  }
}
</script>