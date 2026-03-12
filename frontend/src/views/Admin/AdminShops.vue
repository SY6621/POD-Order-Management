<template>
  <div class="p-8">
    <div class="mb-8 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-slate-800">店铺管理</h1>
        <p class="text-slate-500">管理所有店铺信息和访问链接</p>
      </div>
      <button class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
        + 添加店铺
      </button>
    </div>

    <div class="bg-white rounded-xl border border-slate-200 overflow-hidden">
      <table class="w-full">
        <thead class="bg-slate-50">
          <tr>
            <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">店铺</th>
            <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">地区</th>
            <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">访问密码</th>
            <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">状态</th>
            <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">操作</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100">
          <tr v-for="shop in shops" :key="shop.id" class="hover:bg-slate-50">
            <td class="py-4 px-4">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center">
                  <span class="font-bold text-blue-600">{{ shop.code.toUpperCase() }}</span>
                </div>
                <div>
                  <p class="font-medium text-slate-800">{{ shop.name }}</p>
                  <p class="text-sm text-slate-500">{{ shop.code }}</p>
                </div>
              </div>
            </td>
            <td class="py-4 px-4 text-slate-600">{{ shop.region }}</td>
            <td class="py-4 px-4">
              <div class="flex items-center gap-2">
                <span class="font-mono text-sm bg-slate-100 px-2 py-1 rounded">{{ shop.password || '未设置' }}</span>
                <button 
                  @click="editPassword(shop)"
                  class="text-xs text-blue-600 hover:underline"
                >
                  修改
                </button>
              </div>
            </td>
            <td class="py-4 px-4">
              <span class="px-2 py-1 bg-green-100 text-green-700 rounded-full text-xs font-medium">
                {{ shop.status === 'active' ? '正常' : '停用' }}
              </span>
            </td>
            <td class="py-4 px-4">
              <div class="flex items-center gap-3">
                <button 
                  @click="copyAccessLink(shop)"
                  class="text-sm text-blue-600 hover:underline"
                >
                  复制访问链接
                </button>
                <button class="text-sm text-slate-500 hover:underline">编辑</button>
                <button class="text-sm text-slate-500 hover:underline">查看订单</button>
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
        <p class="text-sm text-slate-500 mb-4">店铺：{{ editingShop?.name }}</p>
        
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
        <h3 class="text-lg font-bold text-slate-800 mb-2">店铺访问链接</h3>
        <p class="text-sm text-slate-500 mb-4">将此链接发送给店铺运营人员</p>
        
        <div class="bg-blue-50 rounded-lg p-4 mb-4">
          <p class="text-sm text-blue-800 mb-2">访问地址：</p>
          <div class="flex gap-2">
            <input 
              :value="accessLink"
              readonly
              class="flex-1 px-3 py-2 bg-white border border-blue-200 rounded text-sm font-mono"
            >
            <button 
              @click="copyLinkToClipboard"
              class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm"
            >
              {{ linkCopied ? '已复制' : '复制' }}
            </button>
          </div>
        </div>

        <div class="bg-amber-50 rounded-lg p-4 mb-4">
          <p class="text-sm text-amber-800">
            <strong>访问密码：</strong>{{ selectedShop?.password || '未设置' }}
          </p>
          <p class="text-xs text-amber-600 mt-1">请同时将密码告知店铺运营人员</p>
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
import { ref, onMounted } from 'vue'
import { useAdminStore } from '../../stores/adminStore'

const adminStore = useAdminStore()
const shops = ref([])

// 密码修改相关
const showPasswordModal = ref(false)
const editingShop = ref(null)
const newPassword = ref('')

// 链接相关
const showLinkModal = ref(false)
const selectedShop = ref(null)
const accessLink = ref('')
const linkCopied = ref(false)

onMounted(async () => {
  const data = await adminStore.fetchShops()
  
  // 如果没有数据，使用模拟数据
  if (!data || data.length === 0) {
    shops.value = [
      { id: '1', name: '美国店铺', code: 'us', region: 'North America', password: 'us123', status: 'active' },
      { id: '2', name: '欧洲店铺', code: 'eu', region: 'Europe', password: 'eu123', status: 'active' },
      { id: '3', name: '亚洲店铺', code: 'asia', region: 'Asia', password: 'asia123', status: 'active' }
    ]
  } else {
    shops.value = data
    // 为每个店铺添加默认密码（如果没有）
    shops.value.forEach(shop => {
      if (!shop.password) {
        shop.password = generateDefaultPassword(shop.code)
      }
    })
  }
})

// 生成默认密码
function generateDefaultPassword(code) {
  return `${code.toLowerCase()}123`
}

// 编辑密码
function editPassword(shop) {
  editingShop.value = shop
  newPassword.value = shop.password || ''
  showPasswordModal.value = true
}

// 保存密码
async function savePassword() {
  if (editingShop.value && newPassword.value) {
    editingShop.value.password = newPassword.value
    // TODO: 调用API保存到数据库
    showPasswordModal.value = false
    alert('密码已修改')
  }
}

// 复制访问链接
function copyAccessLink(shop) {
  selectedShop.value = shop
  const baseUrl = window.location.origin
  accessLink.value = `${baseUrl}/store/${shop.code}/login`
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