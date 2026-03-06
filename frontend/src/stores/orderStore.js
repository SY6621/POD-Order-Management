import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import supabase from '../utils/supabase'

/**
 * 订单状态管理
 * 
 * 订单状态 (status):
 *   - new: 新订单
 *   - pending: 待确认
 *   - confirmed: 已确认
 *   - producing: 生产中
 *   - completed: 已完成
 *   - shipped: 已发货
 *   - delivered: 已送达
 *   - cancelled: 已取消
 * 
 * 优先级 (priority):
 *   - normal: 普通
 *   - high: 高优先级
 *   - urgent: 紧急
 */
export const useOrderStore = defineStore('order', () => {
  // 状态
  const orders = ref([])
  const allOrders = ref([]) // 所有订单（用于远程协作页面）
  const loading = ref(false)
  const error = ref(null)

  // 状态映射（与数据库 orders_status_check 约束一致）
  const statusMap = {
    pending: '待确认',
    effect_sent: '效果图已发',
    producing: '生产中',
    delivered: '已送达'
  }

  const priorityMap = {
    normal: '普通',
    high: '高优先',
    urgent: '紧急'
  }

  // 获取所有订单（直接查询 orders 表，不依赖外键关联）
  const fetchOrders = async () => {
    loading.value = true
    error.value = null
    
    try {
      const { data, error: fetchError } = await supabase
        .from('orders')
        .select('*')
        .order('created_at', { ascending: false })
      
      if (fetchError) throw fetchError
      
      orders.value = data || []
      console.log('✅ 订单数据加载成功:', data?.length, '条')
      // debug: 检查第一条订单是否有背面字段
      if (data?.length > 0) {
        console.log('🔍 第一条订单字段检查:', {
          id: data[0].etsy_order_id,
          front: data[0].effect_image_url ? '有' : '无',
          back: data[0].effect_image_back_url ? '有' : '无'
        })
      }
      return data
    } catch (err) {
      error.value = err.message
      console.error('❌ 订单数据加载失败:', err)
      return []
    } finally {
      loading.value = false
    }
  }

  // 根据状态获取订单
  const getOrdersByStatus = async (status) => {
    loading.value = true
    error.value = null
    
    try {
      const { data, error: fetchError } = await supabase
        .from('orders')
        .select(`
          *,
          sku_mapping (*),
          logistics (*),
          production_documents (*)
        `)
        .eq('status', status)
        .order('created_at', { ascending: false })
      
      if (fetchError) throw fetchError
      
      console.log(`✅ ${status} 订单加载成功:`, data?.length, '条')
      return data || []
    } catch (err) {
      error.value = err.message
      console.error('❌ 订单数据加载失败:', err)
      return []
    } finally {
      loading.value = false
    }
  }

  // 获取待确认订单（pending + effect_sent）
  // 统一调用 fetchOrders 写入 store.orders，让各页面 computed 过滤生效
  const getPendingOrders = async () => {
    return await fetchOrders()
  }

  // 获取生产中订单
  // 统一调用 fetchOrders 写入 store.orders，让各页面 computed 过滤生效
  const getProducingOrders = async () => {
    return await fetchOrders()
  }

  // 获取已完成订单（30天内）
  const getCompletedOrders = async () => {
    loading.value = true
    error.value = null
    
    try {
      const { data, error: fetchError } = await supabase
        .from('orders')
        .select('*')
        .eq('status', 'delivered')
        .order('created_at', { ascending: false })
      
      if (fetchError) throw fetchError
      console.log('✅ 已完成订单:', data?.length)
      return data || []
    } catch (err) {
      error.value = err.message
      console.error('❌ 已完成订单查询失败:', err)
      return []
    } finally {
      loading.value = false
    }
  }

  // 获取订单统计
  const getOrderStats = async () => {
    try {
      const { data, error: fetchError } = await supabase
        .from('orders')
        .select('status')
      
      if (fetchError) throw fetchError
      
      const stats = {
        total: data?.length || 0,
        pending: data?.filter(o => ['pending', 'effect_sent'].includes(o.status)).length || 0,
        producing: data?.filter(o => o.status === 'producing').length || 0,
        completed: data?.filter(o => o.status === 'delivered').length || 0
      }
      
      console.log('✅ 订单统计:', stats)
      return stats
    } catch (err) {
      console.error('❌ 统计数据获取失败:', err)
      return { total: 0, pending: 0, producing: 0, completed: 0 }
    }
  }

  // 更新订单状态
  const updateOrderStatus = async (orderId, newStatus) => {
    loading.value = true
    error.value = null
    
    try {
      const updateData = { status: newStatus }
      
      // 根据状态自动填充时间字段
      if (['completed', 'shipped', 'delivered'].includes(newStatus)) {
        updateData.completed_at = new Date().toISOString()
        updateData.progress = 100
      }
      
      const { data, error: updateError } = await supabase
        .from('orders')
        .update(updateData)
        .eq('id', orderId)
        .select()
      
      if (updateError) throw updateError
      
      // 更新本地数据
      const index = orders.value.findIndex(o => o.id === orderId)
      if (index !== -1) {
        orders.value[index] = { ...orders.value[index], ...updateData }
      }
      
      console.log('✅ 订单状态更新成功')
      return data
    } catch (err) {
      error.value = err.message
      console.error('❌ 订单状态更新失败:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  // 更新订单进度
  const updateOrderProgress = async (orderId, progress) => {
    try {
      const { data, error: updateError } = await supabase
        .from('orders')
        .update({ progress })
        .eq('id', orderId)
        .select()
      
      if (updateError) throw updateError
      
      const index = orders.value.findIndex(o => o.id === orderId)
      if (index !== -1) {
        orders.value[index].progress = progress
      }
      
      return data
    } catch (err) {
      console.error('❌ 进度更新失败:', err)
      throw err
    }
  }

  // 获取订单物流信息
  const getOrderLogistics = async (orderId) => {
    try {
      const { data, error: fetchError } = await supabase
        .from('logistics')
        .select('*')
        .eq('order_id', orderId)
        .single()
      
      if (fetchError && fetchError.code !== 'PGRST116') throw fetchError
      return data
    } catch (err) {
      console.error('❌ 物流信息获取失败:', err)
      return null
    }
  }

  // 获取订单生产文档
  const getOrderDocuments = async (orderId) => {
    try {
      const { data, error: fetchError } = await supabase
        .from('production_documents')
        .select('*')
        .eq('order_id', orderId)
        .single()
      
      if (fetchError && fetchError.code !== 'PGRST116') throw fetchError
      return data
    } catch (err) {
      console.error('❌ 生产文档获取失败:', err)
      return null
    }
  }

  // 获取订单邮件记录
  const getOrderEmailLogs = async (orderId) => {
    try {
      const { data, error: fetchError } = await supabase
        .from('email_logs')
        .select('*')
        .eq('order_id', orderId)
        .order('sent_at', { ascending: false })
      
      if (fetchError) throw fetchError
      return data || []
    } catch (err) {
      console.error('❌ 邮件记录获取失败:', err)
      return []
    }
  }

  // 后端 API 地址
  const API_BASE = 'http://localhost:8000'

  // 一键生成效果图并上传（调用后端 API）
  const generateEffectImage = async (orderId) => {
    try {
      const res = await fetch(`${API_BASE}/api/effect-image/generate-and-upload`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ order_id: orderId })
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || '生成失败')
      // 更新本地 orders 缓存
      const idx = orders.value.findIndex(o => o.id === orderId)
      if (idx !== -1) {
        orders.value[idx] = { ...orders.value[idx], ...data }
      }
      return data
    } catch (err) {
      console.error('❌ 效果图生成失败:', err)
      throw err
    }
  }

  // 一键生成生产文档 PDF 并上传（调用后端 API）
  const generateProductionPdf = async (orderId) => {
    try {
      const res = await fetch(`${API_BASE}/api/pdf/generate-and-upload`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ order_id: orderId })
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || 'PDF生成失败')
      // 更新本地 orders 缓存
      const idx = orders.value.findIndex(o => o.id === orderId)
      if (idx !== -1) {
        orders.value[idx] = { ...orders.value[idx], production_pdf_url: data.production_pdf_url }
      }
      return data
    } catch (err) {
      console.error('❌ PDF生成失败:', err)
      throw err
    }
  }

  // 获取所有订单（用于远程协作页面）
  const fetchAllOrders = async () => {
    loading.value = true
    try {
      const { data, error: fetchError } = await supabase
        .from('orders')
        .select('*')
        .order('created_at', { ascending: false })
      
      if (fetchError) throw fetchError
      allOrders.value = data || []
      console.log('✅ 所有订单加载成功:', allOrders.value.length, '条')
    } catch (err) {
      error.value = err.message
      console.error('❌ 订单加载失败:', err)
    } finally {
      loading.value = false
    }
  }

  return {
    // 状态
    orders,
    allOrders,
    loading,
    error,
    
    // 映射
    statusMap,
    priorityMap,
    
    // 方法
    fetchOrders,
    fetchAllOrders,
    getOrdersByStatus,
    getPendingOrders,
    getProducingOrders,
    getCompletedOrders,
    getOrderStats,
    updateOrderStatus,
    updateOrderProgress,
    getOrderLogistics,
    getOrderDocuments,
    getOrderEmailLogs,
    generateEffectImage,
    generateProductionPdf
  }
})
