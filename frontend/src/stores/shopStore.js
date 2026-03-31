import { defineStore } from 'pinia'
import { ref } from 'vue'
import supabase from '../utils/supabase'

/**
 * 店铺状态管理
 * 处理店铺登录、数据隔离
 */
export const useShopStore = defineStore('shop', () => {
  // 状态
  const currentShop = ref(null)
  const isAuthenticated = ref(false)
  const loading = ref(false)
  const error = ref(null)

  // 获取店铺列表（公开接口，无需认证）
  const fetchShops = async () => {
    try {
      const { data, error: fetchError } = await supabase
        .from('shops')
        .select('id, name, code, region, status, flag_emoji')
        .eq('status', 'active')
        .order('name')
      
      if (fetchError) throw fetchError
      return data || []
    } catch (err) {
      console.error('获取店铺列表失败:', err)
      return []
    }
  }

  // 店铺登录（密码验证）
  const login = async (shopCode, password) => {
    loading.value = true
    error.value = null
    
    try {
      // 1. 获取店铺信息
      const { data: shop, error: shopError } = await supabase
        .from('shops')
        .select('*')
        .eq('code', shopCode)
        .eq('status', 'active')
        .single()
      
      if (shopError || !shop) {
        return { success: false, message: '店铺不存在' }
      }

      // 2. 验证密码（与数据库中的password_hash字段比较）
      if (password !== shop.password_hash) {
        return { success: false, message: '密码错误' }
      }

      // 3. 登录成功，保存状态
      currentShop.value = {
        id: shop.id,
        name: shop.name,
        code: shop.code,
        region: shop.region,
        flag_emoji: shop.flag_emoji
      }
      isAuthenticated.value = true
      
      // 保存到 localStorage
      localStorage.setItem('shop_auth', JSON.stringify({
        shopId: shop.id,
        shopCode: shop.code,
        shopName: shop.name,
        timestamp: Date.now()
      }))

      // 记录访问日志
      await logAccess(shop.id, 'login')

      return { success: true, shop: currentShop.value }
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
      const auth = localStorage.getItem('shop_auth')
      if (!auth) {
        isAuthenticated.value = false
        return false
      }

      const authData = JSON.parse(auth)
      
      // 检查是否过期（24小时）
      if (Date.now() - authData.timestamp > 24 * 60 * 60 * 1000) {
        localStorage.removeItem('shop_auth')
        isAuthenticated.value = false
        return false
      }

      // 获取店铺信息
      const { data: shop, error } = await supabase
        .from('shops')
        .select('id, name, code, region, flag_emoji')
        .eq('id', authData.shopId)
        .single()
      
      if (error || !shop) {
        localStorage.removeItem('shop_auth')
        isAuthenticated.value = false
        return false
      }

      currentShop.value = shop
      isAuthenticated.value = true
      return true
    } catch (err) {
      console.error('检查登录状态失败:', err)
      return false
    }
  }

  // 退出登录
  const logout = () => {
    currentShop.value = null
    isAuthenticated.value = false
    localStorage.removeItem('shop_auth')
  }

  // 获取当前店铺的订单
  const fetchShopOrders = async (filters = {}) => {
    if (!currentShop.value) return []
    
    try {
      let query = supabase
        .from('orders')
        .select('*')
        .eq('shop_id', currentShop.value.id)
        .order('created_at', { ascending: false })
      
      // 状态筛选
      if (filters.status && filters.status !== 'all') {
        query = query.eq('status', filters.status)
      }
      
      // 搜索功能
      if (filters.search) {
        query = query.or(`order_number.ilike.%${filters.search}%,customer_name.ilike.%${filters.search}%`)
      }

      const { data, error } = await query
      
      if (error) throw error
      return data || []
    } catch (err) {
      console.error('获取店铺订单失败:', err)
      return []
    }
  }

  // 获取店铺的效果图订单（有effect_image_url的订单）
  const fetchShopEffectOrders = async (search = '') => {
    if (!currentShop.value) return []
    
    try {
      let query = supabase
        .from('orders')
        .select('*')
        .eq('shop_id', currentShop.value.id)
        .not('effect_image_url', 'is', null)
        .order('created_at', { ascending: false })
      
      // 搜索功能
      if (search) {
        query = query.or(`order_number.ilike.%${search}%,customer_name.ilike.%${search}%`)
      }

      const { data, error } = await query
      
      if (error) throw error
      return data || []
    } catch (err) {
      console.error('获取店铺效果图订单失败:', err)
      return []
    }
  }

  // 记录访问日志
  const logAccess = async (shopId, action) => {
    try {
      await supabase
        .from('shop_access_logs')
        .insert({
          shop_id: shopId,
          action: action,
          user_agent: navigator.userAgent
        })
    } catch (err) {
      console.error('记录访问日志失败:', err)
    }
  }

  return {
    currentShop,
    isAuthenticated,
    loading,
    error,
    fetchShops,
    login,
    checkAuth,
    logout,
    fetchShopOrders,
    fetchShopEffectOrders,
    logAccess
  }
})