<template>
  <div class="p-8">
    <div class="mb-8 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-slate-800">工厂管理</h1>
        <p class="text-slate-500">管理工厂账户和访问链接</p>
      </div>
      <button class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
        + 添加工厂
      </button>
    </div>

    <div class="bg-white rounded-xl border border-slate-200 overflow-hidden">
      <table class="w-full">
        <thead class="bg-slate-50">
          <tr>
            <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">工厂</th>
            <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">访问密码</th>
            <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">状态</th>
            <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">操作</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100">
          <tr v-for="factory in factories" :key="factory.id" class="hover:bg-slate-50">
            <td class="py-4 px-4">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center">
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2">
                    <path d="M21 10V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l2-1.14"/>
                    <path d="m7.5 4.27 9 5.15"/>
                    <polyline points="3.29 7 12 12 20.71 7"/>
                    <line x1="12" x2="12" y1="22" y2="12"/>
                  </svg>
                </div>
                <div>
                  <p class="font-medium text-slate-800">{{ factory.name }}</p>
                  <p class="text-sm text-slate-500">{{ factory.id }}</p>
                </div>
              </div>
            </td>
            <td class="py-4 px-4">
              <div class="flex items-center gap-2">
                <span class="font-mono text-sm bg-slate-100 px-2 py-1 rounded">{{ factory.password }}</span>
                <button 
                  @click="editPassword(factory)"
                  class="text-xs text-blue-600 hover:underline"
                >
                  修改
                </button>
              </div>
            </td>
            <td class="py-4 px-4">
              <span class="px-2 py-1 bg-green-100 text-green-700 rounded-full text-xs font-medium">
                正常
              </span>
            </td>
            <td class="py-4 px-4">
              <div class="flex items-center gap-3">
                <button 
                  @click="copyAccessLink(factory)"
                  class="text-sm text-blue-600 hover:underline"
                >
                  复制访问链接
                </button>
                <button class="text-sm text-slate-500 hover:underline">编辑</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 修改密码弹窗 -->
    <div v-if="showPasswordModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl p-6 w-full max-w-md mx-4">
        <h3 class="text-lg font-bold text-slate-800 mb-4">修改访问密码</h3>
        <p class="text-sm text-slate-500 mb-4">工厂：{{ editingFactory?.name }}</p>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-slate-700 mb-2">新密码</label>
          <input 
            v-model="newPassword"
            type="text"
            placeholder="输入新密码"
            class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none"
          >
        </div>

        <div class="flex gap-3">
          <button 
            @click="savePassword"
            class="flex-1 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            保存
          </button>
          <button 
            @click="showPasswordModal = false"
            class="flex-1 py-2 bg-slate-100 text-slate-700 rounded-lg hover:bg-slate-200"
          >
            取消
          </button>
        </div>
      </div>
    </div>

    <!-- 访问链接弹窗 -->
    <div v-if="showLinkModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl p-6 w-full max-w-lg mx-4">
        <h3 class="text-lg font-bold text-slate-800 mb-2">工厂访问链接</h3>
        <p class="text-sm text-slate-500 mb-4">将此链接发送给工厂负责人</p>
        
        <div class="bg-green-50 rounded-lg p-4 mb-4">
          <p class="text-sm text-green-800 mb-2">访问地址：</p>
          <div class="flex gap-2">
            <input 
              :value="accessLink"
              readonly
              class="flex-1 px-3 py-2 bg-white border border-green-200 rounded text-sm font-mono"
            >
            <button 
              @click="copyLinkToClipboard"
              class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 text-sm"
            >
              {{ linkCopied ? '已复制' : '复制' }}
            </button>
          </div>
        </div>

        <div class="bg-amber-50 rounded-lg p-4 mb-4">
          <p class="text-sm text-amber-800">
            <strong>访问密码：</strong>{{ selectedFactory?.password }}
          </p>
          <p class="text-xs text-amber-600 mt-1">请同时将密码告知工厂负责人</p>
        </div>

        <button 
          @click="showLinkModal = false"
          class="w-full py-2 bg-slate-100 text-slate-700 rounded-lg hover:bg-slate-200"
        >
          关闭
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const factories = ref([
  { id: 'factory1', name: '主工厂', password: 'factory123' },
  { id: 'factory2', name: '分工厂A', password: 'factory456' }
])

// 密码修改相关
const showPasswordModal = ref(false)
const editingFactory = ref(null)
const newPassword = ref('')

// 链接相关
const showLinkModal = ref(false)
const selectedFactory = ref(null)
const accessLink = ref('')
const linkCopied = ref(false)

// 编辑密码
function editPassword(factory) {
  editingFactory.value = factory
  newPassword.value = factory.password
  showPasswordModal.value = true
}

// 保存密码
function savePassword() {
  if (editingFactory.value && newPassword.value) {
    editingFactory.value.password = newPassword.value
    showPasswordModal.value = false
    alert('密码已修改')
  }
}

// 复制访问链接
function copyAccessLink(factory) {
  selectedFactory.value = factory
  const baseUrl = window.location.origin
  accessLink.value = `${baseUrl}/factory-workshop`
  showLinkModal.value = true
}

// 复制链接到剪贴板
async function copyLinkToClipboard() {
  try {
    await navigator.clipboard.writeText(accessLink.value)
    linkCopied.value = true
    setTimeout(() => linkCopied.value = false, 2000)
  } catch (err) {
    console.error('复制失败:', err)
  }
}
</script>