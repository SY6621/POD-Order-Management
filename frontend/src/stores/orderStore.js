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

  // 获取所有订单（关联 sku_mapping 获取 shape/color/size，关联 shops 获取店铺信息）
  const fetchOrders = async () => {
    loading.value = true
    error.value = null
    
    try {
      // 简化查询：不使用关联查询，避免权限问题
      const { data, error: fetchError } = await supabase
        .from('orders')
        .select('*')
        .order('created_at', { ascending: false })
      
      if (fetchError) throw fetchError
      
      orders.value = data || []
      console.log('✅ 订单数据加载成功:', data?.length, '条')
      
      // 如果有订单，单独加载 SKU 信息 + 产品实拍图 + 店铺信息
      if (data?.length > 0) {
        const skuIds = data.map(o => o.sku_id).filter(Boolean)
        const shopIds = data.map(o => o.shop_id).filter(Boolean)
        
        // 调试：输出 shop_id 值
        console.log('🔍 shop_id 检查:', {
          shopIds: shopIds,
          shopIdCount: shopIds.length,
          sampleOrderShopIds: data.slice(0, 3).map(o => ({ id: o.etsy_order_id, shop_id: o.shop_id, shop_code: o.shop_code }))
        })
        
        // 并行查询 sku_mapping、product_photos、shops
        const [skuResult, photoResult, shopResult] = await Promise.all([
          skuIds.length > 0
            ? supabase.from('sku_mapping').select('id, sku_code, shape, color, size').in('id', skuIds)
            : { data: [] },
          skuIds.length > 0
            ? supabase.from('product_photos').select('sku_id, photo_url, photo_type').in('sku_id', skuIds).eq('is_active', true).order('sort_order', { ascending: true })
            : { data: [] },
          // 如果 shopIds 为空，查询所有 shops 作为 fallback
          supabase.from('shops').select('id, code, name, operator')
        ])
        
        // 构建 SKU Map
        const skuMap = skuResult.data
          ? Object.fromEntries(skuResult.data.map(s => [s.id, s]))
          : {}
        
        // 构建产品实拍图 Map（每个 sku_id 取第一张）
        const photoMap = {}
        if (photoResult.data) {
          photoResult.data.forEach(p => {
            if (!photoMap[p.sku_id]) {
              // 正确的 Supabase Storage URL: photos bucket，不是 assets
              const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
              photoMap[p.sku_id] = `${supabaseUrl}/storage/v1/object/public/${p.photo_url}`
              console.log('🖼️ 实拍图 URL:', photoMap[p.sku_id])
            }
          })
        }
        
        // 构建 Shop Map
        const shopMap = shopResult.data
          ? Object.fromEntries(shopResult.data.map(s => [s.id, s]))
          : {}
        
        orders.value = data.map(order => {
          // 优先通过 shop_id 匹配，如果为空则尝试通过 shop_code 匹配
          let shop = shopMap[order.shop_id] || null
          if (!shop && order.shop_code) {
            shop = Object.values(shopMap).find(s => s.code === order.shop_code) || null
          }
          // 如果仍然没有店铺信息，创建一个默认值
          if (!shop) {
            shop = { name: order.shop_code || '未分配', code: order.shop_code || 'N/A', operator: '-' }
          }
          
          return {
            ...order,
            sku_mapping: skuMap[order.sku_id] || null,
            product_image: photoMap[order.sku_id] || null,
            shops: shop
          }
        })
        
        const first = orders.value[0]
        console.log('🔍 第一条订单字段检查:', {
          id: first.etsy_order_id,
          sku: first.sku_mapping?.sku_code || '无',
          shape: first.sku_mapping?.shape || '无',
          color: first.sku_mapping?.color || '无',
          product_image: first.product_image ? '有' : '无',
          shop_code: first.shops?.code || first.shop_code || '无',
          shop_name: first.shops?.name || '无',
          operator: first.shops?.operator || '无'
        })
      }
      return orders.value
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
  // 查询状态为 confirmed 或 producing 的订单，关联SKU和物流信息
  const getProducingOrders = async () => {
    loading.value = true
    error.value = null
    
    try {
      // 查询订单（不使用关联，避免权限问题）
      const { data, error: fetchError } = await supabase
        .from('orders')
        .select('*')
        .in('status', ['confirmed', 'producing'])
        .order('created_at', { ascending: false })

      if (fetchError) throw fetchError

      console.log('✅ 生产中订单原始数据:', data?.length)

      if (data && data.length > 0) {
        // 获取所有SKU ID和订单ID
        const skuIds = data.map(o => o.sku_id).filter(Boolean)
        const orderIds = data.map(o => o.id)

        // 并行查询SKU和物流信息
        const [skuResult, logisticsResult] = await Promise.all([
          skuIds.length > 0 
            ? supabase.from('sku_mapping').select('id, sku_code, shape, color, size').in('id', skuIds)
            : { data: [] },
          supabase.from('logistics').select('order_id, tracking_number, carrier').in('order_id', orderIds)
        ])

        // 构建SKU Map
        const skuMap = skuResult.data
          ? Object.fromEntries(skuResult.data.map(s => [s.id, s]))
          : {}

        // 构建物流Map
        const logisticsMap = {}
        if (logisticsResult.data) {
          logisticsResult.data.forEach(l => {
            logisticsMap[l.order_id] = l
          })
        }

        // 组装订单数据
        const ordersWithDetails = data.map(order => ({
          ...order,
          sku_mapping: skuMap[order.sku_id] || null,
          logistics: logisticsMap[order.id] || null
        }))

        orders.value = ordersWithDetails
        console.log('✅ 生产中订单（含SKU和物流）:', ordersWithDetails.length)
        return ordersWithDetails
      }

      orders.value = data || []
      return data || []
    } catch (err) {
      error.value = err.message
      console.error('❌ 生产中订单查询失败:', err)
      return []
    } finally {
      loading.value = false
    }
  }

  // 获取已完成订单（30天内）
  // 关联 sku_mapping 和 logistics 表，获取产品信息和物流发货时间
  const getCompletedOrders = async () => {
    loading.value = true
    error.value = null

    try {
      // 查询订单（不使用关联，避免权限问题）
      const { data, error: fetchError } = await supabase
        .from('orders')
        .select('*')
        .eq('status', 'delivered')
        .order('created_at', { ascending: false })

      if (fetchError) {
        console.error('Supabase 查询错误:', fetchError)
        throw fetchError
      }

      console.log('✅ 已完成订单原始数据:', data?.length)

      if (data && data.length > 0) {
        // 获取所有 SKU ID 和订单 ID
        const skuIds = data.map(o => o.sku_id).filter(Boolean)
        const orderIds = data.map(o => o.id)

        // 并行查询 SKU 和物流信息
        const [skuResult, logisticsResult] = await Promise.all([
          skuIds.length > 0
            ? supabase.from('sku_mapping').select('id, sku_code, shape, color, size').in('id', skuIds)
            : { data: [] },
          supabase.from('logistics').select('order_id, tracking_number, shipped_at, delivered_at, delivery_status').in('order_id', orderIds)
        ])

        // 构建 SKU Map
        const skuMap = skuResult.data
          ? Object.fromEntries(skuResult.data.map(s => [s.id, s]))
          : {}

        // 构建物流 Map
        const logisticsMap = {}
        if (logisticsResult.data) {
          logisticsResult.data.forEach(l => {
            logisticsMap[l.order_id] = l
          })
        }

        // 组装订单数据
        const ordersWithDetails = data.map(order => ({
          ...order,
          sku_mapping: skuMap[order.sku_id] || null,
          logistics: logisticsMap[order.id] || null,
          // 从 logistics 中提取便捷字段
          tracking_number: logisticsMap[order.id]?.tracking_number || null,
          shipped_at: logisticsMap[order.id]?.shipped_at || null
        }))

        orders.value = ordersWithDetails
        console.log('✅ 已完成订单（含SKU和物流）:', ordersWithDetails.length)
        return ordersWithDetails
      }

      orders.value = data || []
      return data || []
    } catch (err) {
      error.value = err.message
      console.error('❌ 已完成订单查询失败:', err)
      console.error('错误详情:', err.message, err.code, err.details)
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

  // 根据订单号搜索订单（支持 Etsy 订单号模糊搜索）
  const searchOrderById = async (query) => {
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
        .ilike('etsy_order_id', `%${query}%`)
        .limit(1)
      
      if (fetchError) throw fetchError
      
      if (data && data.length > 0) {
        console.log('✅ 订单搜索成功:', data[0].etsy_order_id)
        return data[0]
      }
      
      // 如果没找到，尝试用 id 搜索
      const { data: dataById, error: idError } = await supabase
        .from('orders')
        .select(`
          *,
          sku_mapping (*),
          logistics (*),
          production_documents (*)
        `)
        .eq('id', query)
        .single()
      
      if (idError && idError.code !== 'PGRST116') throw idError
      
      if (dataById) {
        console.log('✅ 订单搜索成功(ID):', dataById.etsy_order_id)
        return dataById
      }
      
      return null
    } catch (err) {
      error.value = err.message
      console.error('❌ 订单搜索失败:', err)
      return null
    } finally {
      loading.value = false
    }
  }

  // 获取订单完整信息（包含关联表数据）
  const getOrderWithDetails = async (orderId) => {
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
        .eq('id', orderId)
        .single()
      
      if (fetchError) throw fetchError
      
      console.log('✅ 订单详情加载成功:', data?.etsy_order_id)
      return data
    } catch (err) {
      error.value = err.message
      console.error('❌ 订单详情加载失败:', err)
      return null
    } finally {
      loading.value = false
    }
  }

  // 保存效果图（从设计器获取文字转路径SVG并上传到存储）
  const saveEffectImage = async (orderId, imageData) => {
    loading.value = true
    error.value = null
    
    try {
      // SVG 格式（文字已转路径，无字体依赖）
      const fileBlob = new Blob([imageData], { type: 'image/svg+xml' })
      const fileName = `effect_${orderId}_${Date.now()}.svg`
      const contentType = 'image/svg+xml'
      console.log('📤 开始上传效果图:', fileName)
      
      // 2. 上传到Supabase Storage
      const { data: uploadData, error: uploadError } = await supabase
        .storage
        .from('effect-images')
        .upload(fileName, fileBlob, {
          contentType: contentType,
          upsert: true
        })
      
      if (uploadError) {
        console.error('❌ Storage上传失败:', uploadError)
        throw new Error(`Storage上传失败: ${uploadError.message}`)
      }
      console.log('✅ Storage上传成功:', uploadData)
      
      // 3. 获取公开URL
      const { data: urlData } = supabase
        .storage
        .from('effect-images')
        .getPublicUrl(fileName)
      
      const publicUrl = urlData.publicUrl
      console.log('🔗 获取到公开URL:', publicUrl)
      
      // 4. 更新订单记录
      console.log('📝 开始更新订单记录:', orderId)
      const { data, error: updateError } = await supabase
        .from('orders')
        .update({ 
          effect_image_url: publicUrl,
          updated_at: new Date().toISOString()
        })
        .eq('id', orderId)
        .select()
      
      if (updateError) {
        console.error('❌ 订单更新失败:', updateError)
        throw new Error(`订单更新失败: ${updateError.message}`)
      }
      console.log('✅ 订单更新成功:', data)
      
      // 5. 【可选】同步保存到 production_documents 表（生产文档PDF依赖此表）
      // 注意：此操作可能因RLS策略失败，但不影响主流程
      try {
        const { data: existingDoc } = await supabase
          .from('production_documents')
          .select('id')
          .eq('order_id', orderId)
          .single()
        
        if (existingDoc) {
          // 更新已有记录
          const { error: docUpdateError } = await supabase
            .from('production_documents')
            .update({ 
              effect_svg_url: publicUrl,
              updated_at: new Date().toISOString()
            })
            .eq('order_id', orderId)
          
          if (docUpdateError) {
            console.warn('⚠️ production_documents 更新失败:', docUpdateError)
          } else {
            console.log('✅ production_documents 更新成功')
          }
        } else {
          // 插入新记录
          const { error: docInsertError } = await supabase
            .from('production_documents')
            .insert({
              order_id: orderId,
              effect_svg_url: publicUrl,
              created_at: new Date().toISOString(),
              updated_at: new Date().toISOString()
            })
          
          if (docInsertError) {
            console.warn('⚠️ production_documents 插入失败:', docInsertError)
          } else {
            console.log('✅ production_documents 插入成功')
          }
        }
      } catch (docError) {
        console.warn('⚠️ production_documents 操作失败（可忽略）:', docError.message)
      }
      
      // 6. 更新本地缓存
      const index = orders.value.findIndex(o => o.id === orderId)
      if (index !== -1) {
        orders.value[index].effect_image_url = publicUrl
      }
      
      console.log('✅ 效果图保存成功:', publicUrl)
      return { url: publicUrl, data }
    } catch (err) {
      error.value = err.message
      console.error('❌ 效果图保存失败:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  // 清空效果图（回退编辑）
  const clearEffectImage = async (orderId) => {
    loading.value = true
    error.value = null
    
    try {
      // 1. 更新订单记录，清空 effect_image_url
      const { data, error: updateError } = await supabase
        .from('orders')
        .update({ 
          effect_image_url: null,
          updated_at: new Date().toISOString()
        })
        .eq('id', orderId)
        .select()
      
      if (updateError) throw updateError
      
      // 2. 更新本地缓存
      const index = orders.value.findIndex(o => o.id === orderId)
      if (index !== -1) {
        orders.value[index].effect_image_url = null
      }
      
      console.log('✅ 效果图已清空')
      return data
    } catch (err) {
      error.value = err.message
      console.error('❌ 效果图清空失败:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  // 更新邮件发送状态
  const updateEmailSentStatus = async (orderId, sent) => {
    loading.value = true
    error.value = null
    
    try {
      const { data, error: updateError } = await supabase
        .from('orders')
        .update({ 
          email_sent: sent,
          updated_at: new Date().toISOString()
        })
        .eq('id', orderId)
        .select()
      
      if (updateError) throw updateError
      
      // 更新本地缓存
      const index = orders.value.findIndex(o => o.id === orderId)
      if (index !== -1) {
        orders.value[index].email_sent = sent
      }
      
      console.log('✅ 邮件发送状态已更新:', sent)
      return data
    } catch (err) {
      error.value = err.message
      console.error('❌ 邮件状态更新失败:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  // 保存邮件记录
  const saveEmailLog = async (emailData) => {
    loading.value = true
    error.value = null
    
    try {
      const { data, error: insertError } = await supabase
        .from('email_logs')
        .insert([{
          ...emailData,
          sent_at: new Date().toISOString(),
          status: 'sent'
        }])
        .select()
      
      if (insertError) throw insertError
      
      console.log('✅ 邮件记录已保存:', data)
      return data
    } catch (err) {
      error.value = err.message
      console.error('❌ 邮件记录保存失败:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  // 根据订单ID获取最新的邮件记录
  const getEmailLogByOrderId = async (orderId) => {
    try {
      const { data, error: fetchError } = await supabase
        .from('email_logs')
        .select('*')
        .eq('order_id', orderId)
        .order('sent_at', { ascending: false })
        .limit(1)
        .maybeSingle()
      
      if (fetchError) throw fetchError
      
      return data
    } catch (err) {
      console.error('❌ 邮件记录获取失败:', err)
      return null
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
    generateProductionPdf,
    searchOrderById,
    getOrderWithDetails,
    saveEffectImage,
    clearEffectImage,
    updateEmailSentStatus,
    saveEmailLog,
    getEmailLogByOrderId
  }
})
