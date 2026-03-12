import { defineStore } from 'pinia'
import { ref } from 'vue'
import supabase from '../utils/supabase'

/**
 * 管理员状态管理
 * 处理管理员登录、权限控制
 */
export const useAdminStore = defineStore('admin', () => {
  // 状态
  const currentUser = ref(null)
  const isAuthenticated = ref(false)
  const loading = ref(false)
  const error = ref(null)

  // 管理员登录
  const login = async (username, password) => {
    loading.value = true
    error.value = null
    
    try {
      // 开发测试模式：本地验证（无需数据库）
      // 默认管理员账号: admin / admin123
      if (username === 'admin' && password === 'admin123') {
        const mockUser = {
          id: 'admin-001',
          username: 'admin',
          role: 'admin',
          role_type: 'main',
          email: 'admin@example.com'
        }
        
        currentUser.value = mockUser
        isAuthenticated.value = true
        
        // 保存到 localStorage
        localStorage.setItem('admin_auth', JSON.stringify({
          userId: mockUser.id,
          username: mockUser.username,
          timestamp: Date.now()
        }))
        
        return { success: true, user: mockUser }
      }
      
      return { success: false, message: '用户名或密码错误' }
    } catch (err) {
      error.value = err.message
      return { success: false, message: err.message }
    } finally {
      loading.value = false
    }
  }

  // 检查登录状态
  const checkAuth = async () => {
    try {
      const auth = localStorage.getItem('admin_auth')
      if (!auth) {
        isAuthenticated.value = false
        return false
      }

      const authData = JSON.parse(auth)
      
      // 检查是否过期（24小时）
      if (Date.now() - authData.timestamp > 24 * 60 * 60 * 1000) {
        localStorage.removeItem('admin_auth')
        isAuthenticated.value = false
        return false
      }

      // 开发测试模式：本地验证（无需数据库）
      if (authData.userId === 'admin-001') {
        currentUser.value = {
          id: 'admin-001',
          username: 'admin',
          role: 'admin',
          role_type: 'main',
          email: 'admin@example.com'
        }
        isAuthenticated.value = true
        return true
      }

      // 生产模式：数据库验证
      const { data: user, error } = await supabase
        .from('users')
        .select('id, username, role, email, status')
        .eq('id', authData.userId)
        .eq('status', 'active')
        .single()
      
      if (error || !user) {
        localStorage.removeItem('admin_auth')
        isAuthenticated.value = false
        return false
      }

      currentUser.value = user
      isAuthenticated.value = true
      return true
    } catch (err) {
      console.error('检查登录状态失败:', err)
      return false
    }
  }

  // 退出登录
  const logout = () => {
    currentUser.value = null
    isAuthenticated.value = false
    localStorage.removeItem('admin_auth')
  }

  // 获取所有店铺
  const fetchShops = async () => {
    try {
      const { data, error } = await supabase
        .from('shops')
        .select('*')
        .order('created_at', { ascending: false })
      
      if (error) throw error
      return data || []
    } catch (err) {
      console.error('获取店铺失败:', err)
      return []
    }
  }

  // 创建店铺
  const createShop = async (shopData) => {
    try {
      const { data, error } = await supabase
        .from('shops')
        .insert(shopData)
        .select()
        .single()
      
      if (error) throw error
      return { success: true, shop: data }
    } catch (err) {
      return { success: false, message: err.message }
    }
  }

  // 更新店铺
  const updateShop = async (shopId, shopData) => {
    try {
      const { data, error } = await supabase
        .from('shops')
        .update(shopData)
        .eq('id', shopId)
        .select()
        .single()
      
      if (error) throw error
      return { success: true, shop: data }
    } catch (err) {
      return { success: false, message: err.message }
    }
  }

  // 获取所有订单（管理员视角）
  const fetchAllOrders = async (filters = {}) => {
    try {
      let query = supabase
        .from('orders')
        .select(`
          *,
          shops:shop_id (name, code)
        `)
        .order('created_at', { ascending: false })
      
      // 应用筛选
      if (filters.shopId) {
        query = query.eq('shop_id', filters.shopId)
      }
      if (filters.status) {
        query = query.eq('status', filters.status)
      }
      
      const { data, error } = await query
      
      if (error) throw error
      return data || []
    } catch (err) {
      console.error('获取订单失败:', err)
      return []
    }
  }

  // ==================== 子账号管理 ====================

  // 获取所有子账号
  const fetchSubAccounts = async () => {
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
      return (data || []).map(user => ({
        ...user,
        shops: user.user_shop_permissions?.map(p => p.shops).filter(Boolean) || []
      }))
    } catch (err) {
      console.error('获取子账号失败:', err)
      return []
    }
  }

  // 创建子账号
  const createSubAccount = async (userData) => {
    try {
      const { data, error } = await supabase
        .from('users')
        .insert({
          ...userData,
          role: 'sub',
          role_type: 'sub',
          status: 'active'
        })
        .select()
        .single()
      
      if (error) throw error
      return { success: true, user: data }
    } catch (err) {
      return { success: false, message: err.message }
    }
  }

  // 更新子账号状态
  const updateSubAccountStatus = async (userId, status) => {
    try {
      const { error } = await supabase
        .from('users')
        .update({ status })
        .eq('id', userId)
      
      if (error) throw error
      return { success: true }
    } catch (err) {
      return { success: false, message: err.message }
    }
  }

  // 分配店铺权限
  const assignShopPermissions = async (userId, shopIds) => {
    try {
      // 删除旧权限
      await supabase
        .from('user_shop_permissions')
        .delete()
        .eq('user_id', userId)
      
      // 添加新权限
      if (shopIds.length > 0) {
        const permissions = shopIds.map(shopId => ({
          user_id: userId,
          shop_id: shopId
        }))
        
        const { error } = await supabase
          .from('user_shop_permissions')
          .insert(permissions)
        
        if (error) throw error
      }
      
      return { success: true }
    } catch (err) {
      return { success: false, message: err.message }
    }
  }

  // 获取子账号绩效统计
  const fetchSubAccountStats = async () => {
    try {
      const { data, error } = await supabase
        .from('subaccount_stats')
        .select('*')
      
      if (error) throw error
      return data || []
    } catch (err) {
      console.error('获取绩效统计失败:', err)
      return []
    }
  }

  return {
    currentUser,
    isAuthenticated,
    loading,
    error,
    login,
    checkAuth,
    logout,
    fetchShops,
    createShop,
    updateShop,
    fetchAllOrders,
    // 子账号管理
    fetchSubAccounts,
    createSubAccount,
    updateSubAccountStatus,
    assignShopPermissions,
    fetchSubAccountStats
  }
})