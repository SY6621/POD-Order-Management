<template>
  <div class="p-8">
    <div class="mb-8 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-slate-800">工厂管理</h1>
        <p class="text-slate-500">管理工厂账户和访问链接</p>
      </div>
      <button 
        @click="openAddModal"
        class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
      >
        + 添加工厂
      </button>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="flex items-center justify-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      <span class="ml-3 text-slate-500">加载中...</span>
    </div>

    <!-- 工厂列表 -->
    <div v-else class="bg-white rounded-xl border border-slate-200 overflow-hidden">
      <table class="w-full">
        <thead class="bg-slate-50">
          <tr>
            <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">工厂</th>
            <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">工厂代码</th>
            <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">访问密码</th>
            <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">状态</th>
            <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">联系人</th>
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
                  <p class="text-sm text-slate-500">{{ factory.contact_phone || '暂无电话' }}</p>
                </div>
              </div>
            </td>
            <td class="py-4 px-4">
              <span class="font-mono text-sm bg-slate-100 px-2 py-1 rounded">{{ factory.code }}</span>
            </td>
            <td class="py-4 px-4">
              <div class="flex items-center gap-2">
                <span class="font-mono text-sm bg-slate-100 px-2 py-1 rounded">{{ factory.password_hash || '未设置' }}</span>
                <button 
                  @click="editPassword(factory)"
                  class="text-xs text-blue-600 hover:underline"
                >
                  修改
                </button>
              </div>
            </td>
            <td class="py-4 px-4">
              <span 
                :class="[
                  'px-2 py-1 rounded-full text-xs font-medium',
                  factory.status === 'active' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                ]"
              >
                {{ factory.status === 'active' ? '正常' : '停用' }}
              </span>
            </td>
            <td class="py-4 px-4">
              <span class="text-sm text-slate-600">{{ factory.contact_name || '-' }}</span>
            </td>
            <td class="py-4 px-4">
              <div class="flex items-center gap-3">
                <button 
                  @click="copyAccessLink(factory)"
                  class="text-sm text-blue-600 hover:underline"
                >
                  复制访问链接
                </button>
                <button 
                  @click="openEditModal(factory)"
                  class="text-sm text-slate-500 hover:underline"
                >
                  编辑
                </button>
                <button 
                  @click="confirmDelete(factory)"
                  class="text-sm text-red-500 hover:underline"
                >
                  删除
                </button>
              </div>
            </td>
          </tr>
          <tr v-if="factories.length === 0">
            <td colspan="6" class="py-8 text-center text-slate-500">
              暂无工厂数据，点击上方"添加工厂"按钮创建
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 添加/编辑工厂弹窗 -->
    <div v-if="showEditModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl p-6 w-full max-w-lg mx-4 max-h-[90vh] overflow-y-auto">
        <h3 class="text-lg font-bold text-slate-800 mb-4">
          {{ isAddMode ? '添加工厂' : '编辑工厂' }}
        </h3>
        
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">工厂名称 <span class="text-red-500">*</span></label>
            <input 
              v-model="editForm.name"
              type="text"
              placeholder="请输入工厂名称"
              class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none"
            >
          </div>
          
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">工厂代码 <span class="text-red-500">*</span></label>
            <input 
              v-model="editForm.code"
              type="text"
              placeholder="唯一标识，如：main-factory"
              :disabled="!isAddMode"
              class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none disabled:bg-slate-100"
            >
            <p class="text-xs text-slate-500 mt-1">用于生成访问链接，创建后不可修改</p>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">访问密码</label>
            <input 
              v-model="editForm.password_hash"
              type="text"
              placeholder="工厂协作平台登录密码"
              class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none"
            >
          </div>
          
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">状态</label>
            <select 
              v-model="editForm.status"
              class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none"
            >
              <option value="active">正常</option>
              <option value="inactive">停用</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">联系人</label>
            <input 
              v-model="editForm.contact_name"
              type="text"
              placeholder="联系人姓名"
              class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none"
            >
          </div>
          
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">联系电话</label>
            <input 
              v-model="editForm.contact_phone"
              type="text"
              placeholder="联系电话"
              class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none"
            >
          </div>
          
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">工厂地址</label>
            <textarea 
              v-model="editForm.address"
              placeholder="工厂地址"
              rows="2"
              class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none resize-none"
            ></textarea>
          </div>
        </div>

        <div class="flex gap-3 mt-6">
          <button 
            @click="saveFactory"
            :disabled="saving"
            class="flex-1 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {{ saving ? '保存中...' : '保存' }}
          </button>
          <button 
            @click="showEditModal = false"
            class="flex-1 py-2 bg-slate-100 text-slate-700 rounded-lg hover:bg-slate-200"
          >
            取消
          </button>
        </div>
      </div>
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
            :disabled="saving"
            class="flex-1 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {{ saving ? '保存中...' : '保存' }}
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

    <!-- 删除确认弹窗 -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl p-6 w-full max-w-md mx-4">
        <h3 class="text-lg font-bold text-slate-800 mb-4">确认删除</h3>
        <p class="text-sm text-slate-600 mb-4">
          确定要删除工厂 <strong>{{ deletingFactory?.name }}</strong> 吗？此操作不可恢复。
        </p>

        <div class="flex gap-3">
          <button 
            @click="deleteFactory"
            :disabled="saving"
            class="flex-1 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50"
          >
            {{ saving ? '删除中...' : '确认删除' }}
          </button>
          <button 
            @click="showDeleteModal = false"
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
            <strong>访问密码：</strong>{{ selectedFactory?.password_hash || '未设置' }}
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
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

// API Base URL
const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

// 工厂列表
const factories = ref([])
const loading = ref(false)
const saving = ref(false)

// 编辑相关
const showEditModal = ref(false)
const isAddMode = ref(true)
const editForm = ref({
  id: '',
  name: '',
  code: '',
  password_hash: '',
  status: 'active',
  contact_name: '',
  contact_phone: '',
  address: ''
})

// 密码修改相关
const showPasswordModal = ref(false)
const editingFactory = ref(null)
const newPassword = ref('')

// 删除相关
const showDeleteModal = ref(false)
const deletingFactory = ref(null)

// 链接相关
const showLinkModal = ref(false)
const selectedFactory = ref(null)
const accessLink = ref('')
const linkCopied = ref(false)

// 加载工厂列表
async function loadFactories() {
  loading.value = true
  try {
    const response = await fetch(`${API_BASE}/api/factories`)
    const result = await response.json()
    
    if (result.success) {
      factories.value = result.data
    } else {
      ElMessage.error(result.message || '加载工厂列表失败')
    }
  } catch (error) {
    console.error('加载工厂列表失败:', error)
    ElMessage.error('网络错误，请检查后端服务是否启动')
  } finally {
    loading.value = false
  }
}

// 打开添加弹窗
function openAddModal() {
  isAddMode.value = true
  editForm.value = {
    id: '',
    name: '',
    code: '',
    password_hash: '',
    status: 'active',
    contact_name: '',
    contact_phone: '',
    address: ''
  }
  showEditModal.value = true
}

// 打开编辑弹窗
function openEditModal(factory) {
  isAddMode.value = false
  editForm.value = {
    id: factory.id,
    name: factory.name,
    code: factory.code,
    password_hash: factory.password_hash || '',
    status: factory.status || 'active',
    contact_name: factory.contact_name || '',
    contact_phone: factory.contact_phone || '',
    address: factory.address || ''
  }
  showEditModal.value = true
}

// 保存工厂（添加/编辑）
async function saveFactory() {
  // 验证必填字段
  if (!editForm.value.name.trim()) {
    ElMessage.warning('请输入工厂名称')
    return
  }
  if (isAddMode.value && !editForm.value.code.trim()) {
    ElMessage.warning('请输入工厂代码')
    return
  }
  
  saving.value = true
  try {
    const url = isAddMode.value 
      ? `${API_BASE}/api/factories`
      : `${API_BASE}/api/factories/${editForm.value.id}`
    
    const body = isAddMode.value
      ? {
          name: editForm.value.name,
          code: editForm.value.code,
          password_hash: editForm.value.password_hash,
          status: editForm.value.status,
          contact_name: editForm.value.contact_name || null,
          contact_phone: editForm.value.contact_phone || null,
          address: editForm.value.address || null
        }
      : {
          name: editForm.value.name,
          password_hash: editForm.value.password_hash,
          status: editForm.value.status,
          contact_name: editForm.value.contact_name || null,
          contact_phone: editForm.value.contact_phone || null,
          address: editForm.value.address || null
        }
    
    const response = await fetch(url, {
      method: isAddMode.value ? 'POST' : 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    })
    
    const result = await response.json()
    
    if (result.success) {
      ElMessage.success(result.message || (isAddMode.value ? '工厂创建成功' : '工厂更新成功'))
      showEditModal.value = false
      loadFactories()
    } else {
      ElMessage.error(result.message || '操作失败')
    }
  } catch (error) {
    console.error('保存工厂失败:', error)
    ElMessage.error('网络错误，请检查后端服务是否启动')
  } finally {
    saving.value = false
  }
}

// 编辑密码
function editPassword(factory) {
  editingFactory.value = factory
  newPassword.value = factory.password_hash || ''
  showPasswordModal.value = true
}

// 保存密码
async function savePassword() {
  if (!newPassword.value.trim()) {
    ElMessage.warning('请输入新密码')
    return
  }
  
  saving.value = true
  try {
    const response = await fetch(`${API_BASE}/api/factories/${editingFactory.value.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ password_hash: newPassword.value })
    })
    
    const result = await response.json()
    
    if (result.success) {
      ElMessage.success('密码已修改')
      showPasswordModal.value = false
      loadFactories()
    } else {
      ElMessage.error(result.message || '修改失败')
    }
  } catch (error) {
    console.error('修改密码失败:', error)
    ElMessage.error('网络错误，请检查后端服务是否启动')
  } finally {
    saving.value = false
  }
}

// 确认删除
function confirmDelete(factory) {
  deletingFactory.value = factory
  showDeleteModal.value = true
}

// 删除工厂
async function deleteFactory() {
  saving.value = true
  try {
    const response = await fetch(`${API_BASE}/api/factories/${deletingFactory.value.id}`, {
      method: 'DELETE'
    })
    
    const result = await response.json()
    
    if (result.success) {
      ElMessage.success('工厂已删除')
      showDeleteModal.value = false
      loadFactories()
    } else {
      ElMessage.error(result.message || '删除失败')
    }
  } catch (error) {
    console.error('删除工厂失败:', error)
    ElMessage.error('网络错误，请检查后端服务是否启动')
  } finally {
    saving.value = false
  }
}

// 复制访问链接
function copyAccessLink(factory) {
  selectedFactory.value = factory
  const baseUrl = window.location.origin
  accessLink.value = `${baseUrl}/factory-workshop?factory=${factory.code}`
  linkCopied.value = false
  showLinkModal.value = true
}

// 复制链接到剪贴板
async function copyLinkToClipboard() {
  try {
    await navigator.clipboard.writeText(accessLink.value)
    linkCopied.value = true
    ElMessage.success('链接已复制到剪贴板')
    setTimeout(() => linkCopied.value = false, 2000)
  } catch (err) {
    console.error('复制失败:', err)
    ElMessage.error('复制失败，请手动复制')
  }
}

// 初始化加载
onMounted(() => {
  loadFactories()
})
</script>
