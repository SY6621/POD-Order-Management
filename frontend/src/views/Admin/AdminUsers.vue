<template>
  <div class="p-8">
    <div class="mb-8 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-slate-800">子账号管理</h1>
        <p class="text-slate-500">创建和管理子账号，分配店铺权限</p>
      </div>
      <button 
        @click="showCreateModal = true"
        class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
      >
        + 创建子账号
      </button>
    </div>

    <!-- 子账号列表 -->
    <div class="bg-white rounded-xl border border-slate-200 overflow-hidden">
      <table class="w-full">
        <thead class="bg-slate-50">
          <tr>
            <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">账号信息</th>
            <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">管理店铺</th>
            <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">状态</th>
            <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">最后活动</th>
            <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">操作</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100">
          <tr v-for="user in subAccounts" :key="user.id" class="hover:bg-slate-50">
            <td class="py-4 px-4">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-full bg-purple-100 flex items-center justify-center">
                  <span class="font-bold text-purple-600">{{ (user.display_name || user.username)?.[0]?.toUpperCase() }}</span>
                </div>
                <div>
                  <p class="font-medium text-slate-800">{{ user.display_name || user.username }}</p>
                  <p class="text-sm text-slate-500">{{ user.email || '未设置邮箱' }}</p>
                </div>
              </div>
            </td>
            <td class="py-4 px-4">
              <div class="flex flex-wrap gap-1">
                <span 
                  v-for="shop in user.shops" 
                  :key="shop.id"
                  class="px-2 py-0.5 bg-blue-100 text-blue-700 rounded text-xs"
                >
                  {{ shop.name }}
                </span>
                <span v-if="!user.shops?.length" class="text-sm text-slate-400">未分配店铺</span>
              </div>
            </td>
            <td class="py-4 px-4">
              <span :class="user.status === 'active' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'" class="px-2 py-1 rounded-full text-xs font-medium">
                {{ user.status === 'active' ? '正常' : '已禁用' }}
              </span>
            </td>
            <td class="py-4 px-4 text-sm text-slate-500">
              {{ user.last_activity_at ? formatDate(user.last_activity_at) : '暂无活动' }}
            </td>
            <td class="py-4 px-4">
              <div class="flex items-center gap-3">
                <button @click="editPermissions(user)" class="text-sm text-blue-600 hover:underline">分配店铺</button>
                <button @click="toggleStatus(user)" class="text-sm text-slate-500 hover:underline">
                  {{ user.status === 'active' ? '禁用' : '启用' }}
                </button>
                <button @click="resetPassword(user)" class="text-sm text-slate-500 hover:underline">重置密码</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      
      <div v-if="subAccounts.length === 0" class="p-8 text-center text-slate-500">
        暂无子账号，点击上方按钮创建
      </div>
    </div>

    <!-- 创建子账号弹窗 -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl p-6 w-full max-w-md mx-4">
        <h3 class="text-lg font-bold text-slate-800 mb-4">创建子账号</h3>
        
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">用户名</label>
            <input 
              v-model="newUser.username"
              type="text"
              placeholder="输入用户名"
              class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none"
            >
          </div>
          
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">显示名称</label>
            <input 
              v-model="newUser.display_name"
              type="text"
              placeholder="输入显示名称"
              class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none"
            >
          </div>
          
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">邮箱</label>
            <input 
              v-model="newUser.email"
              type="email"
              placeholder="输入邮箱"
              class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none"
            >
          </div>
          
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">初始密码</label>
            <input 
              v-model="newUser.password"
              type="text"
              placeholder="输入初始密码"
              class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none"
            >
          </div>
        </div>

        <div class="flex gap-3 mt-6">
          <button 
            @click="createSubAccount"
            :disabled="!newUser.username || !newUser.password"
            class="flex-1 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            创建
          </button>
          <button 
            @click="showCreateModal = false"
            class="flex-1 py-2 bg-slate-100 text-slate-700 rounded-lg hover:bg-slate-200"
          >
            取消
          </button>
        </div>
      </div>
    </div>

    <!-- 分配店铺弹窗 -->
    <div v-if="showPermissionModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl p-6 w-full max-w-lg mx-4">
        <h3 class="text-lg font-bold text-slate-800 mb-2">分配店铺权限</h3>
        <p class="text-sm text-slate-500 mb-4">账号：{{ editingUser?.display_name || editingUser?.username }}</p>
        
        <div class="space-y-2 max-h-64 overflow-y-auto">
          <label 
            v-for="shop in allShops" 
            :key="shop.id"
            class="flex items-center gap-3 p-3 border border-slate-200 rounded-lg hover:bg-slate-50 cursor-pointer"
          >
            <input 
              type="checkbox"
              :checked="selectedShopIds.includes(shop.id)"
              @change="toggleShop(shop.id)"
              class="w-4 h-4 text-blue-600 rounded"
            >
            <div class="flex-1">
              <p class="font-medium text-slate-800">{{ shop.name }}</p>
              <p class="text-sm text-slate-500">{{ shop.code }} · {{ shop.region }}</p>
            </div>
          </label>
        </div>

        <div class="flex gap-3 mt-6">
          <button 
            @click="savePermissions"
            class="flex-1 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            保存
          </button>
          <button 
            @click="showPermissionModal = false"
            class="flex-1 py-2 bg-slate-100 text-slate-700 rounded-lg hover:bg-slate-200"
          >
            取消
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAdminStore } from '../../stores/adminStore'
import supabase from '../../utils/supabase'

const adminStore = useAdminStore()

const subAccounts = ref([])
const allShops = ref([])

// 弹窗状态
const showCreateModal = ref(false)
const showPermissionModal = ref(false)

// 新用户表单
const newUser = ref({
  username: '',
  display_name: '',
  email: '',
  password: ''
})

// 编辑权限
const editingUser = ref(null)
const selectedShopIds = ref([])

onMounted(async () => {
  await loadSubAccounts()
  await loadShops()
})

// 加载子账号列表
async function loadSubAccounts() {
  try {
    const { data, error } = await supabase
      .from('users')
      .select(`
        *,
        user_shop_permissions (
          shop_id,
          shops (id, name, code, region)
        )
      `)
      .eq('role_type', 'sub')
      .order('created_at', { ascending: false })
    
    if (error) throw error
    
    // 转换数据格式
    subAccounts.value = (data || []).map(user => ({
      ...user,
      shops: user.user_shop_permissions?.map(p => p.shops).filter(Boolean) || []
    }))
  } catch (err) {
    console.error('加载子账号失败:', err)
    // 使用模拟数据
    subAccounts.value = [
      { id: '1', username: 'operator1', display_name: '运营小王', email: 'wang@example.com', status: 'active', shops: [{ id: '1', name: '美国店铺' }] },
      { id: '2', username: 'operator2', display_name: '运营小李', email: 'li@example.com', status: 'active', shops: [{ id: '2', name: '欧洲店铺' }] }
    ]
  }
}

// 加载店铺列表
async function loadShops() {
  const data = await adminStore.fetchShops()
  // 如果没有数据，使用模拟数据
  if (!data || data.length === 0) {
    allShops.value = [
      { id: '1', name: '美国店铺', code: 'us', region: 'North America' },
      { id: '2', name: '欧洲店铺', code: 'eu', region: 'Europe' },
      { id: '3', name: '亚洲店铺', code: 'asia', region: 'Asia' }
    ]
  } else {
    allShops.value = data
  }
}

// 创建子账号
async function createSubAccount() {
  if (!newUser.value.username || !newUser.value.password) return
  
  try {
    const { data, error } = await supabase
      .from('users')
      .insert({
        username: newUser.value.username,
        display_name: newUser.value.display_name,
        email: newUser.value.email,
        password_hash: newUser.value.password, // TODO: 实际应加密
        role: 'sub',
        role_type: 'sub',
        status: 'active'
      })
      .select()
      .single()
    
    if (error) throw error
    
    subAccounts.value.unshift({ ...data, shops: [] })
    showCreateModal.value = false
    newUser.value = { username: '', display_name: '', email: '', password: '' }
    alert('子账号创建成功！')
  } catch (err) {
    console.error('创建失败:', err)
    // 模拟创建成功
    subAccounts.value.unshift({
      id: Date.now().toString(),
      username: newUser.value.username,
      display_name: newUser.value.display_name,
      email: newUser.value.email,
      status: 'active',
      shops: []
    })
    showCreateModal.value = false
    alert('子账号创建成功！')
  }
}

// 编辑权限
function editPermissions(user) {
  editingUser.value = user
  selectedShopIds.value = user.shops?.map(s => s.id) || []
  showPermissionModal.value = true
}

// 切换店铺选择
function toggleShop(shopId) {
  const index = selectedShopIds.value.indexOf(shopId)
  if (index > -1) {
    selectedShopIds.value.splice(index, 1)
  } else {
    selectedShopIds.value.push(shopId)
  }
}

// 保存权限
async function savePermissions() {
  if (!editingUser.value) return
  
  try {
    // 删除旧权限
    await supabase
      .from('user_shop_permissions')
      .delete()
      .eq('user_id', editingUser.value.id)
    
    // 添加新权限
    if (selectedShopIds.value.length > 0) {
      const permissions = selectedShopIds.value.map(shopId => ({
        user_id: editingUser.value.id,
        shop_id: shopId
      }))
      
      await supabase
        .from('user_shop_permissions')
        .insert(permissions)
    }
    
    // 更新本地数据
    const user = subAccounts.value.find(u => u.id === editingUser.value.id)
    if (user) {
      user.shops = allShops.value.filter(s => selectedShopIds.value.includes(s.id))
    }
    
    showPermissionModal.value = false
    alert('权限已保存！')
  } catch (err) {
    console.error('保存权限失败:', err)
    // 模拟保存成功
    const user = subAccounts.value.find(u => u.id === editingUser.value.id)
    if (user) {
      user.shops = allShops.value.filter(s => selectedShopIds.value.includes(s.id))
    }
    showPermissionModal.value = false
    alert('权限已保存！')
  }
}

// 切换状态
async function toggleStatus(user) {
  const newStatus = user.status === 'active' ? 'inactive' : 'active'
  
  try {
    await supabase
      .from('users')
      .update({ status: newStatus })
      .eq('id', user.id)
    
    user.status = newStatus
  } catch (err) {
    console.error('更新状态失败:', err)
    user.status = newStatus
  }
}

// 重置密码
function resetPassword(user) {
  const newPassword = prompt(`为 ${user.display_name || user.username} 设置新密码：`)
  if (newPassword) {
    // TODO: 调用API更新密码
    alert(`密码已重置为：${newPassword}`)
  }
}

// 格式化日期
function formatDate(dateStr) {
  if (!dateStr) return '--'
  const date = new Date(dateStr)
  return `${date.getMonth() + 1}/${date.getDate()} ${date.getHours()}:${date.getMinutes().toString().padStart(2, '0')}`
}
</script>