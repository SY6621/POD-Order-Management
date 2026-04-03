<template>
  <div class="service-link-page">
    <!-- 加载中状态 -->
    <div v-if="loading" class="loading-overlay">
      <div class="loading-content">
        <el-icon class="loading-icon" :size="48"><Loading /></el-icon>
        <p class="loading-text">正在验证链接并加载订单数据...</p>
      </div>
    </div>

    <!-- Token无效错误页面 -->
    <div v-else-if="error === 'invalid_token'" class="error-overlay">
      <div class="error-content">
        <el-icon class="error-icon" :size="64" color="#ef4444"><CircleClose /></el-icon>
        <h2 class="error-title">链接无效或已过期</h2>
        <p class="error-desc">该客服外链可能已被禁用、Token已过期或链接地址不正确。</p>
        <p class="error-hint">请联系管理员重新生成有效的客服外链。</p>
      </div>
    </div>

    <!-- 网络错误页面 -->
    <div v-else-if="error === 'network'" class="error-overlay">
      <div class="error-content">
        <el-icon class="error-icon" :size="64" color="#f59e0b"><Warning /></el-icon>
        <h2 class="error-title">网络连接失败</h2>
        <p class="error-desc">无法连接到服务器，请检查网络连接。</p>
        <el-button type="primary" @click="retryLoad">
          <el-icon><RefreshRight /></el-icon>
          重新加载
        </el-button>
      </div>
    </div>

    <!-- 正常页面内容 -->
    <template v-else>
      <!-- 顶部导航 -->
      <header class="page-header">
        <div class="header-content">
          <div class="shop-info">
            <h1>{{ shopInfo?.name || '店铺订单中心' }}</h1>
            <span class="shop-lang">{{ shopCode?.toUpperCase() || 'US' }}</span>
          </div>
          <!-- 移除右上角重复按钮，保留底部修改设计按钮 -->
          <div class="header-actions">
            <!-- 占位，保持布局 -->
          </div>
        </div>
      </header>

      <!-- 统计卡片 -->
      <div class="stats-bar">
        <div class="stat-card">
          <span class="stat-label">全部订单</span>
          <span class="stat-value">{{ orders.length }}</span>
        </div>
        <div class="stat-card pending">
          <span class="stat-label">待确认</span>
          <span class="stat-value">{{ pendingCount }}</span>
        </div>
        <div class="stat-card sent">
          <span class="stat-label">已发送</span>
          <span class="stat-value">{{ sentCount }}</span>
        </div>
        <div class="stat-card confirmed">
          <span class="stat-label">已确认</span>
          <span class="stat-value">{{ confirmedCount }}</span>
        </div>
        <div class="stat-card modify">
          <span class="stat-label">需修改</span>
          <span class="stat-value">{{ modifyCount }}</span>
        </div>
      </div>

    <!-- 主内容 -->
    <main class="main-content">
      <!-- 左侧：订单列表 -->
      <aside class="order-list-panel notion-style">
        <!-- 头部 -->
        <div style="padding: 8px 12px; border-bottom: 1px solid #eee;">
          <span style="font-weight: 600; font-size: 14px; color: #1a1a1a;">订单列表</span>
          <span style="font-size: 11px; color: #999; margin-left: 6px;">点击查看详情</span>
        </div>

        <!-- 新订单分组 -->
        <div class="section-tag tag-new">新订单</div>
        <div class="order-list notion-list">
          <div
            v-for="order in newOrders"
            :key="order.id"
            class="order-card compact-card"
            :class="{ highlight: selectedOrder?.id === order.id }"
            @click="selectOrder(order)"
          >
            <div style="display: flex; align-items: center; gap: 8px;">
              <!-- 产品实拍图（小图） -->
              <img
                v-if="order.product_image"
                :src="order.product_image"
                style="width: 36px; height: 36px; border-radius: 4px; object-fit: cover; flex-shrink: 0; background: #f3f4f6;"
              />
              <div v-else style="width: 36px; height: 36px; border-radius: 4px; background: #f3f4f6; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ccc" stroke-width="1.5">
                  <path :d="getShapeIconPath(order.product_shape)"></path>
                </svg>
              </div>
              <div style="flex: 1; min-width: 0; overflow: hidden;">
                <!-- 客户名 + 状态标签 -->
                <div style="display: flex; align-items: center; justify-content: space-between;">
                  <span style="font-weight: 600; font-size: 13px; color: #1a1a1a; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{{ order.customer_name }}</span>
                  <span class="status-badge-compact badge-red-compact">新订单</span>
                </div>
                <!-- 订单ID（红色粗体） -->
                <div style="font-size: 12px; color: #ef4444; font-weight: 700;"># {{ order.etsy_order_id }}</div>
                <!-- 英文标题（单行截断） -->
                <div style="font-size: 11px; color: #666; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">Custom {{ order.product_shape || 'Heart' }} Pet ID Tag: Deep Engraved Stainless Steel with Enamel</div>
              </div>
            </div>
            <!-- 超时标识（如果有） -->
            <div v-if="isOverdue(order)" style="margin-top: 4px; padding: 1px 6px; background: #fef0f0; border: 1px solid #fde2e2; border-radius: 3px; display: inline-flex; align-items: center;">
              <span style="color: #f56c6c; font-size: 10px; font-weight: 500;">⚠️ 超时 {{ getOverdueHours(order) }}h</span>
            </div>
          </div>
        </div>
        
        <!-- 已发送效果图分组 -->
        <div class="section-tag tag-sent">已发送效果图</div>
        <div class="order-list notion-list">
          <div
            v-for="order in sentOrders"
            :key="order.id"
            class="order-card compact-card"
            :class="{ highlight: selectedOrder?.id === order.id }"
            @click="selectOrder(order)"
          >
            <div style="display: flex; align-items: center; gap: 8px;">
              <!-- 产品实拍图（小图） -->
              <img
                v-if="order.product_image"
                :src="order.product_image"
                style="width: 36px; height: 36px; border-radius: 4px; object-fit: cover; flex-shrink: 0; background: #f3f4f6;"
              />
              <div v-else style="width: 36px; height: 36px; border-radius: 4px; background: #f3f4f6; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ccc" stroke-width="1.5">
                  <path :d="getShapeIconPath(order.product_shape)"></path>
                </svg>
              </div>
              <div style="flex: 1; min-width: 0; overflow: hidden;">
                <!-- 客户名 + 状态标签 -->
                <div style="display: flex; align-items: center; justify-content: space-between;">
                  <span style="font-weight: 600; font-size: 13px; color: #1a1a1a; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{{ order.customer_name }}</span>
                  <span class="status-badge-compact badge-blue-compact">待确认</span>
                </div>
                <!-- 订单ID（红色粗体） -->
                <div style="font-size: 12px; color: #ef4444; font-weight: 700;"># {{ order.etsy_order_id }}</div>
                <!-- 英文标题（单行截断） -->
                <div style="font-size: 11px; color: #666; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">Custom {{ order.product_shape || 'Heart' }} Pet ID Tag: Deep Engraved Stainless Steel with Enamel</div>
              </div>
            </div>
            <!-- 超时标识（如果有） -->
            <div v-if="isOverdue(order)" style="margin-top: 4px; padding: 1px 6px; background: #fef0f0; border: 1px solid #fde2e2; border-radius: 3px; display: inline-flex; align-items: center;">
              <span style="color: #f56c6c; font-size: 10px; font-weight: 500;">⚠️ 超时 {{ getOverdueHours(order) }}h</span>
            </div>
          </div>
        </div>
        
        <!-- 底部留白 -->
        <div class="h-8"></div>
      </aside>

      <!-- 中间：订单详情 -->
      <section class="detail-panel">
        <div v-if="!selectedOrder" class="empty-state">
          <el-empty description="请选择左侧订单查看详情" />
        </div>
        <div v-else class="detail-content">
          <!-- 详情头部 -->
          <div class="detail-header">
            <h3>订单详情 {{ selectedOrder.etsy_order_id }}</h3>
            <div class="detail-header-actions">
              <el-tag :type="getEmailStatusType(selectedOrder.email_status)" class="status-tag">
                {{ getEmailStatusText(selectedOrder.email_status) }}
              </el-tag>
              <!-- 按钮组移到标题行右侧 -->
              <el-button size="small" class="action-btn gray-btn" @click="downloadImage">下载 JPG</el-button>
              <a 
                :href="getDesignLink()" 
                target="_blank"
                class="design-link-btn"
              >修改外链</a>
            </div>
          </div>

          <!-- 订单详情区域 -->
          <div class="order-detail-section">
            <!-- 效果图预览 - 效果图填满整个预览区域 -->
            <div class="effect-section">
              <h4>📷 效果图预览</h4>
              <div class="effect-preview hero">
                <!-- 优先使用effect_image_url展示真实效果图 -->
                <img 
                  v-if="selectedOrder.effect_image_url"
                  :src="selectedOrder.effect_image_url" 
                  :alt="'效果图-' + selectedOrder.etsy_order_id"
                  class="effect-real-image"
                  @error="onEffectImageError"
                />
                <!-- 兜底：使用SVG渲染 -->
                <svg 
                  v-else 
                  viewBox="0 0 100 100" 
                  class="effect-fallback-svg"
                >
                  <path :d="getShapePath(selectedOrder.product_shape)"
                        :fill="getColorHex(selectedOrder.product_color)"
                        :stroke="getColorStroke(selectedOrder.product_color)"
                        stroke-width="2"/>
                  <text x="50" y="50" text-anchor="middle" font-size="12" fill="#374151" dy=".3em">{{ selectedOrder.front_text }}</text>
                  <text x="50" y="70" text-anchor="middle" font-size="10" fill="#6b7280" dy=".3em">{{ selectedOrder.back_text }}</text>
                </svg>
              </div>
            </div>

            <!-- 订单信息块 - 红框：在蓝框下方 -->
            <div class="order-card compact align-left">
              <!-- 绿框：客户信息 - 放在最上面 -->
              <div class="order-card-header">
                <a href="#" class="user-link">{{ selectedOrder.customer_name }}</a>
                <span class="order-id">#{{ selectedOrder.etsy_order_id }}</span>
              </div>
              
              <!-- 内容区域 -->
              <div class="order-card-content">
                <!-- 左侧：图片和标题 -->
                <div class="order-card-left">
                  <div class="product-img-wrapper">
                    <!-- 优先显示产品实拍图 -->
                    <img 
                      v-if="selectedOrder.product_image" 
                      :src="selectedOrder.product_image" 
                      :alt="'产品实拍图-' + selectedOrder.etsy_order_id"
                      class="product-real-img"
                      @error="onDetailProductImageError"
                    />
                    <svg v-else viewBox="0 0 24 24" class="product-icon">
                      <path :d="getShapePath(selectedOrder.product_shape)" 
                            :fill="getColorHex(selectedOrder.product_color)" 
                            stroke="#d1d5db" 
                            stroke-width="1"/>
                    </svg>
                  </div>
                  <div class="product-text">
                    <span class="tag-custom">可个性化</span>
                    <h2 class="product-title-zh">定制{{ selectedOrder.product_shape }}宠物身份牌：深雕不锈钢珐琅</h2>
                    <p class="product-title-en">Custom {{ selectedOrder.product_shape }} Pet ID Tag:</p>
                    <p class="product-title-en last">Deep Engraved Stainless Steel with Enamel</p>
                  </div>
                </div>

                <!-- 右侧：规格详情 -->
                <div class="order-card-right">
                  <div class="info-row">
                    <span class="info-label">数量</span>
                    <span class="info-value">{{ selectedOrder.quantity || 1 }}</span>
                  </div>
                  <div class="info-row">
                    <span class="info-label">颜色 + 尺寸:</span>
                    <span class="info-value">{{ formatColorSize(selectedOrder.product_color, selectedOrder.size) }}</span>
                  </div>
                  <div class="info-row">
                    <span class="info-label">雕刻面:</span>
                    <span class="info-value">{{ selectedOrder.engraving_sides || '双面' }}</span>
                  </div>
                  <div class="info-row last">
                    <span class="info-label">个性化信息</span>
                    <span class="info-value">正面: {{ selectedOrder.front_text }}<br>背面: {{ selectedOrder.back_text }}</span>
                  </div>
                </div>
              </div>
            </div>


          </div>
        </div>
      </section>

      <!-- 右侧：邮件与操作 -->
      <aside class="action-panel">
        <!-- 邮件内容 -->
        <div class="panel-section email-section">
          <div class="panel-header">
            <h3>📧 邮件内容</h3>
          </div>
          <div v-if="!selectedOrder" class="empty-state">
            <el-empty description="选择订单查看邮件" :image-size="60" />
          </div>
          <div v-else class="email-preview">
            <!-- 加载中状态 -->
            <div v-if="isLoadingEmail" class="email-body text-slate-400 text-sm">
              <p>正在加载邮件内容...</p>
            </div>
            <!-- 有邮件记录时显示 -->
            <div v-else-if="latestEmailContent" class="email-body" style="white-space: pre-wrap;">
              {{ latestEmailContent }}
            </div>
            <!-- 无邮件记录时显示提示 -->
            <div v-else class="email-body text-slate-400 text-sm">
              <p>暂无邮件记录</p>
              <p class="text-xs mt-2">发送邮件后将在此显示</p>
            </div>
            <el-button size="small" class="copy-btn" @click="copyEmail">
              <el-icon class="copy-icon"><DocumentCopy /></el-icon>
              复制邮件内容
            </el-button>
          </div>
        </div>

        <!-- 操作按钮区域 -->
        <div v-if="selectedOrder" class="panel-section action-buttons-section">
          <div class="panel-header">
            <h3>⚡ 快捷操作</h3>
          </div>
          <div class="action-buttons">
            <!-- 确认按钮：仅当email_status为sent时显示 -->
            <el-button
              v-if="selectedOrder.email_status === 'sent'"
              type="success"
              class="confirm-btn"
              :loading="confirming"
              @click="confirmOrder"
            >
              <span class="btn-icon">✅</span> 确认订单
            </el-button>
            <!-- 请求修改按钮：仅当email_status为sent时显示 -->
            <el-button
              v-if="selectedOrder.email_status === 'sent'"
              type="warning"
              class="modify-btn"
              :loading="modifying"
              @click="showModifyDialog"
            >
              <span class="btn-icon">✏️</span> 请求修改
            </el-button>
            <!-- 新订单/待确认时显示客户操作按钮 -->
            <template v-if="selectedOrder.email_status === 'pending' || !selectedOrder.email_status || selectedOrder.email_status === 'sent'">
              <el-button
                type="success"
                class="confirm-btn"
                :loading="confirming"
                @click="handleCustomerConfirm"
              >
                <span class="btn-icon">✅</span> 确认设计
              </el-button>
              <el-button
                type="warning"
                class="modify-btn"
                :loading="modifying"
                @click="showModifyDialog"
              >
                <span class="btn-icon">✏️</span> 需要修改
              </el-button>
            </template>
            <!-- 已确认提示 -->
            <div v-if="selectedOrder.email_status === 'confirmed'" class="action-hint success">
              <el-icon><CircleCheckFilled /></el-icon>
              <span>该订单已确认，无需操作</span>
            </div>
            <!-- 需修改提示 -->
            <div v-if="selectedOrder.email_status === 'modify'" class="action-hint warning">
              <el-icon><WarningFilled /></el-icon>
              <span>该订单已提交修改请求，等待处理</span>
            </div>
          </div>
        </div>

        <!-- 操作历史 -->
        <div class="panel-section history-section">
          <div class="panel-header">
            <h3>📋 操作历史</h3>
          </div>
          <div v-if="!selectedOrder" class="empty-state">
            <el-empty description="暂无记录" :image-size="60" />
          </div>
          <div v-else class="history-timeline">
            <!-- 显示当前订单的操作记录 -->
            <div v-if="currentOrderLogs.length > 0">
              <div v-for="(log, index) in currentOrderLogs" :key="index" class="history-item">
                <span class="history-time">{{ log.time }}</span>
                <span class="history-icon">{{ getLogIcon(log.type) }}</span>
                <div class="history-content">
                  <span class="history-label">{{ log.label }}</span>
                  <span class="history-text">{{ log.text }}</span>
                </div>
              </div>
            </div>
            <!-- 无记录时显示订单创建时间 -->
            <div v-else class="history-item">
              <span class="history-time">{{ formatShortTime(selectedOrder.created_at) }}</span>
              <span class="history-icon">📋</span>
              <div class="history-content">
                <span class="history-label">订单创建</span>
                <span class="history-text">订单已入库，等待处理</span>
              </div>
            </div>
          </div>
        </div>
      </aside>
    </main>
    </template>

    <!-- 修改原因对话框 -->
    <el-dialog
      v-model="modifyDialogVisible"
      title="请求修改"
      width="500px"
      :close-on-click-modal="false"
    >
      <div class="modify-dialog-content">
        <p class="dialog-hint">请填写客户要求的修改内容：</p>
        <el-input
          v-model="modifyReason"
          type="textarea"
          :rows="4"
          placeholder="例如：客户希望将正面文字改为 Luna Bell，背面电话改为 123-456-7890"
          maxlength="500"
          show-word-limit
        />
        <!-- 上传参考图片（可选） -->
        <div style="margin-top: 16px;">
          <p class="dialog-hint" style="margin-bottom: 8px;">上传参考图片（可选）：</p>
          <div style="display: flex; align-items: center; gap: 12px;">
            <label 
              style="display: inline-flex; align-items: center; gap: 6px; padding: 8px 16px; border: 1px dashed #d9d9db; border-radius: 6px; cursor: pointer; color: #606266; font-size: 13px; transition: all 0.2s;"
              @mouseenter="$event.target.style.borderColor='#409eff'; $event.target.style.color='#409eff'"
              @mouseleave="$event.target.style.borderColor='#d9d9db'; $event.target.style.color='#606266'"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
              选择图片
              <input type="file" accept="image/*" multiple style="display: none;" @change="handleModifyImageUpload" />
            </label>
            <span v-if="modifyImages.length > 0" style="font-size: 12px; color: #67c23a;">已选择 {{ modifyImages.length }} 张图片</span>
          </div>
          <!-- 图片预览 -->
          <div v-if="modifyImages.length > 0" style="display: flex; gap: 8px; margin-top: 8px; flex-wrap: wrap;">
            <div v-for="(img, idx) in modifyImages" :key="idx" style="position: relative; width: 60px; height: 60px;">
              <img :src="img.preview" style="width: 60px; height: 60px; object-fit: cover; border-radius: 4px; border: 1px solid #eee;" />
              <span 
                @click="modifyImages.splice(idx, 1)" 
                style="position: absolute; top: -6px; right: -6px; width: 18px; height: 18px; background: #f56c6c; color: #fff; border-radius: 50%; font-size: 11px; display: flex; align-items: center; justify-content: center; cursor: pointer;"
              >&times;</span>
            </div>
          </div>
        </div>
      </div>
      <template #footer>
        <el-button @click="modifyDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="modifying" @click="requestModify">
          提交修改请求
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Clock, Edit, ArrowDown, Loading, CircleClose, Warning, RefreshRight, InfoFilled, CircleCheckFilled, WarningFilled, DocumentCopy } from '@element-plus/icons-vue'
import supabase from '@/utils/supabase'
import { useOrderStore } from '@/stores/orderStore'

const store = useOrderStore()

const route = useRoute()
const router = useRouter()

// API基础URL
const API_BASE_URL = 'http://localhost:8000'

// 状态
const loading = ref(true)
const error = ref(null) // 错误状态：null | 'invalid_token' | 'network' | 'no_orders'
const shopInfo = ref(null)
const designLinkEnabled = ref(true)
const orders = ref([])
const selectedOrder = ref(null)
const operationLogs = ref([])
const customerFeedback = ref('')
const showDesignPanel = ref(false) // 修改设计面板显示状态
const confirming = ref(false) // 确认操作loading状态
const modifying = ref(false) // 修改操作loading状态
const modifyDialogVisible = ref(false) // 修改对话框显示状态
const modifyReason = ref('') // 修改原因
const modifyImages = ref([]) // 修改请求附带的图片
const latestEmailContent = ref(null) // 最新邮件内容
const isLoadingEmail = ref(false) // 邮件加载状态

// 从URL获取参数
const shopCode = computed(() => route.params.shopCode)
const token = computed(() => route.query.token)

// 统计
const pendingCount = computed(() => orders.value.filter(o => o.email_status === 'pending' || !o.email_status).length)
const sentCount = computed(() => orders.value.filter(o => o.email_status === 'sent').length)
const confirmedCount = computed(() => orders.value.filter(o => o.email_status === 'confirmed').length)
const modifyCount = computed(() => orders.value.filter(o => o.email_status === 'modify').length)

/**
 * 验证Token并加载数据
 * 1. 调用后端API验证token
 * 2. 验证通过后加载订单数据
 * 3. 加载操作历史
 */
async function validateAndLoad() {
  loading.value = true
  error.value = null
  
  try {
    // 检查必要参数
    if (!shopCode.value || !token.value) {
      error.value = 'invalid_token'
      ElMessage.error('链接无效：缺少必要参数')
      return
    }
    
    console.log('🔐 开始验证Token:', { shopCode: shopCode.value, token: token.value.substring(0, 8) + '...' })
    
    // 1. 调用后端API验证Token
    const validateResponse = await fetch(`${API_BASE_URL}/service-link/validate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        shop_code: shopCode.value,
        token: token.value
      })
    })
    
    if (!validateResponse.ok) {
      throw new Error('验证请求失败')
    }
    
    const validateResult = await validateResponse.json()
    console.log('✅ Token验证结果:', validateResult)
    
    if (!validateResult.valid) {
      error.value = 'invalid_token'
      ElMessage.error(validateResult.message || '链接无效或已过期')
      return
    }
    
    // 验证成功，保存店铺信息（包含两个token供页面跳转使用）
    shopInfo.value = {
      name: validateResult.shop_name || '店铺订单中心',
      code: shopCode.value,
      id: validateResult.shop_id,
      service_token: validateResult.service_token || '',
      design_token: validateResult.design_token || ''
    }
    designLinkEnabled.value = true
    
    // 2. 从Supabase加载该店铺的订单数据
    await loadOrders(validateResult.shop_id)
    
    // 3. 加载操作历史
    await loadOperationLogs(validateResult.shop_id)
    
  } catch (e) {
    console.error('❌ 加载失败:', e)
    error.value = 'network'
    ElMessage.error('网络错误，请检查连接后重试')
  } finally {
    loading.value = false
  }
}

/**
 * 从Supabase加载订单数据
 * 查询条件: shop_id = validated_shop_id AND status IN ('待回复', '待创建')
 */
async function loadOrders(shopId) {
  try {
    console.log('📦 开始加载订单数据，店铺ID:', shopId)
    
    // 查询待确认订单（待回复、待创建状态）
    const { data: ordersData, error: ordersError } = await supabase
      .from('orders')
      .select('*')
      .eq('shop_id', shopId)
      .in('status', ['待回复', '待创建'])
      .order('created_at', { ascending: false })
    
    if (ordersError) {
      console.error('❌ 订单查询错误:', ordersError)
      throw ordersError
    }
    
    console.log('✅ 订单数据加载成功:', ordersData?.length || 0, '条')
    
    if (!ordersData || ordersData.length === 0) {
      orders.value = []
      selectedOrder.value = null
      return
    }
    
    // 获取所有SKU ID用于关联查询（兼容sku_id和sku_mapping_id字段）
    const skuIds = ordersData.map(o => o.sku_id || o.sku_mapping_id).filter(Boolean)
    
    // 并行查询SKU信息和产品图片
    let skuMap = {}
    let photoMap = {}
    
    if (skuIds.length > 0) {
      const [skuResult, photoResult] = await Promise.all([
        supabase.from('sku_mapping').select('id, sku_code, shape, color, size').in('id', skuIds),
        supabase.from('product_photos').select('sku_id, photo_url, photo_type').in('sku_id', skuIds).eq('is_active', true).order('sort_order', { ascending: true })
      ])
      
      // 构建SKU Map
      skuMap = skuResult.data
        ? Object.fromEntries(skuResult.data.map(s => [s.id, s]))
        : {}
      
      // 构建产品实拍图 Map
      if (photoResult.data) {
        const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
        photoResult.data.forEach(p => {
          if (!photoMap[p.sku_id]) {
            // photo_url 可能是完整URL或相对路径
            const photoUrl = p.photo_url.startsWith('http') 
              ? p.photo_url 
              : `${supabaseUrl}/storage/v1/object/public/${p.photo_url}`
            photoMap[p.sku_id] = photoUrl
          }
        })
      }
    }
    
    // 转换订单数据格式，与现有UI兼容
    orders.value = ordersData.map(order => {
      const skuInfo = skuMap[order.sku_id] || {}
      return {
        id: order.id,
        etsy_order_id: order.etsy_order_id,
        customer_name: order.customer_name || '未知客户',
        customer_email: order.customer_email || '',
        product_shape: order.product_shape || skuInfo.shape || '圆形',
        product_color: order.product_color || skuInfo.color || '金色',
        front_text: order.front_text || '',
        back_text: order.back_text || '',
        sku: skuInfo.sku_code || order.sku || '',
        size: order.size || skuInfo.size || '大号',
        quantity: order.quantity || 1,
        engraving_sides: order.engraving_sides || '双面',
        brand_name: order.brand_name || 'Marinella Nesso',
        email_status: order.email_status || 'pending',
        etsy_order_time: order.etsy_order_time,
        created_at: order.created_at,
        // 保留原始数据供后续使用
        sku_mapping: skuInfo,
        product_image: photoMap[order.sku_id || order.sku_mapping_id] || null,
        effect_image_url: order.effect_image_url
      }
    })
    
    // 默认选中第一个订单
    if (orders.value.length > 0) {
      selectedOrder.value = orders.value[0]
      // 【修复】初始加载时也需要获取邮件记录
      await fetchEmailLog()
    }
    
    console.log('✅ 订单数据处理完成')
    
  } catch (e) {
    console.error('❌ 加载订单失败:', e)
    ElMessage.error('加载订单数据失败')
    orders.value = []
  }
}

/**
 * 从Supabase加载操作历史
 * 从service_link_logs表查询该店铺的操作记录
 */
async function loadOperationLogs(shopId) {
  try {
    console.log('📝 开始加载操作历史，店铺ID:', shopId)
    
    const { data: logsData, error: logsError } = await supabase
      .from('service_link_logs')
      .select('*')
      .eq('shop_id', shopId)
      .order('created_at', { ascending: false })
      .limit(20)
    
    if (logsError) {
      console.error('❌ 操作日志查询错误:', logsError)
      // 日志加载失败不影响主流程
      operationLogs.value = []
      return
    }
    
    console.log('✅ 操作历史加载成功:', logsData?.length || 0, '条')
    
    // 转换日志格式与现有UI兼容
    operationLogs.value = (logsData || []).map(log => {
      const createdAt = new Date(log.created_at)
      const timeStr = `${createdAt.getHours().toString().padStart(2, '0')}:${createdAt.getMinutes().toString().padStart(2, '0')}`
      
      // 根据action类型映射显示文本
      const actionMap = {
        'view': { type: 'view', label: '查看', text: '客服查看订单详情' },
        'send_email': { type: 'email', label: '邮件', text: '客服发送确认邮件给客户' },
        'confirm': { type: 'confirm', label: '确认', text: '客户确认设计' },
        'request_modify': { type: 'modify', label: '修改', text: '客户请求修改设计' }
      }
      
      const actionInfo = actionMap[log.action] || { type: 'order', label: '操作', text: log.action }
      
      return {
        time: timeStr,
        type: actionInfo.type,
        label: actionInfo.label,
        text: actionInfo.text,
        raw: log // 保留原始数据
      }
    })
    
  } catch (e) {
    console.error('❌ 加载操作历史失败:', e)
    operationLogs.value = []
  }
}

/**
 * 重试加载
 */
function retryLoad() {
  validateAndLoad()
}

// 选择订单
function selectOrder(order) {
  selectedOrder.value = order
  customerFeedback.value = ''
  showDesignPanel.value = false // 切换订单时关闭面板
  // 获取该订单的邮件记录
  fetchEmailLog()
}

// 获取订单最新邮件记录
async function fetchEmailLog() {
  if (!selectedOrder.value?.id) {
    console.log('⚠️ fetchEmailLog: 无选中订单')
    return
  }
  isLoadingEmail.value = true
  console.log('📧 开始获取邮件记录，订单ID:', selectedOrder.value.id)
  try {
    const emailLog = await store.getEmailLogByOrderId(selectedOrder.value.id)
    console.log('📧 邮件记录查询结果:', emailLog)
    if (emailLog) {
      // 提取英文部分（ServiceLink面向客户）
      const content = emailLog.content || ''
      // 如果content包含 "=== English Version ===" 分隔符，提取英文部分
      const englishMatch = content.split('=== English Version ===')
      if (englishMatch.length > 1) {
        latestEmailContent.value = englishMatch[1].trim()
      } else {
        latestEmailContent.value = content
      }
      console.log('✅ 邮件内容加载成功')
    } else {
      latestEmailContent.value = null
      console.log('ℹ️ 该订单暂无邮件记录')
    }
  } catch (err) {
    console.error('❌ 获取邮件记录失败:', err)
    latestEmailContent.value = null
  } finally {
    isLoadingEmail.value = false
  }
}

// 切换修改设计面板
function toggleDesignPanel() {
  showDesignPanel.value = !showDesignPanel.value
}

// 前往设计链接
function goToDesignLink() {
  // 注意：service_token和design_token是不同的Token
  // 如果shopInfo中有design_token，使用design_token，否则使用当前service_token
  const designToken = shopInfo.value?.design_token || token.value
  router.push(`/design/${shopCode.value}?token=${designToken}`)
}

// 处理设计下拉操作
function handleDesignAction(command) {
  if (command === 'edit') {
    goToDesignLink()
  } else if (command === 'resend') {
    ElMessage.success('设计已回传系统')
  }
}

// 提交设计处理
function submitDesign() {
  if (!customerFeedback.value.trim()) {
    ElMessage.warning('请填写客户修改意见')
    return
  }
  ElMessage.success('设计处理已提交')
  customerFeedback.value = ''
}

/**
 * 确认订单
 * 1. 更新订单email_status为'confirmed'
 * 2. 记录操作日志到service_link_logs表
 * 3. 刷新订单列表
 */
async function confirmOrder() {
  if (!selectedOrder.value || !shopInfo.value) {
    ElMessage.warning('请先选择订单')
    return
  }

  try {
    confirming.value = true
    console.log('✅ 开始确认订单:', selectedOrder.value.etsy_order_id)

    // 1. 更新订单状态
    const { error: updateError } = await supabase
      .from('orders')
      .update({ email_status: 'confirmed' })
      .eq('id', selectedOrder.value.id)

    if (updateError) {
      console.error('❌ 更新订单状态失败:', updateError)
      throw updateError
    }

    // 2. 记录操作日志
    const { error: logError } = await supabase
      .from('service_link_logs')
      .insert({
        order_id: selectedOrder.value.id,
        shop_id: shopInfo.value.id,
        action_type: 'confirm',
        action_detail: '客户确认订单',
        created_at: new Date().toISOString()
      })

    if (logError) {
      console.error('❌ 记录操作日志失败:', logError)
      // 日志失败不影响主流程
    }

    console.log('✅ 订单确认成功')
    ElMessage.success('订单已确认！')

    // 3. 刷新订单列表
    await loadOrders(shopInfo.value.id)
    await loadOperationLogs(shopInfo.value.id)

    // 4. 重新选中新订单列表的第一个（如果有的话）
    if (newOrders.value.length > 0) {
      selectedOrder.value = newOrders.value[0]
    } else if (sentOrders.value.length > 0) {
      selectedOrder.value = sentOrders.value[0]
    } else {
      selectedOrder.value = null
    }

  } catch (e) {
    console.error('❌ 确认订单失败:', e)
    ElMessage.error('确认失败，请重试')
  } finally {
    confirming.value = false
  }
}

/**
 * 显示修改对话框
 */
function showModifyDialog() {
  modifyReason.value = ''
  modifyImages.value = [] // 清空图片
  modifyDialogVisible.value = true
}

// 处理图片上传
function handleModifyImageUpload(e) {
  const files = Array.from(e.target.files)
  files.forEach(file => {
    if (file.size > 5 * 1024 * 1024) {
      ElMessage.warning(`图片 ${file.name} 超过5MB，已跳过`)
      return
    }
    const reader = new FileReader()
    reader.onload = (ev) => {
      modifyImages.value.push({
        file: file,
        preview: ev.target.result,
        name: file.name
      })
    }
    reader.readAsDataURL(file)
  })
  // 重置input以允许重复选择
  e.target.value = ''
}

/**
 * 请求修改
 * 1. 弹出对话框让客服填写修改原因
 * 2. 更新订单email_status为'modify'
 * 3. 记录操作日志到service_link_logs表
 * 4. 刷新订单列表
 */
async function requestModify() {
  if (!selectedOrder.value || !shopInfo.value) {
    ElMessage.warning('请先选择订单')
    return
  }

  if (!modifyReason.value.trim()) {
    ElMessage.warning('请填写修改原因')
    return
  }

  try {
    modifying.value = true
    console.log('✏️ 开始请求修改:', selectedOrder.value.etsy_order_id, '原因:', modifyReason.value)

    // 1. 更新订单状态（同时更新status字段）
    const { error: updateError } = await supabase
      .from('orders')
      .update({ 
        email_status: 'modify',
        status: '客户修改',
        updated_at: new Date().toISOString()
      })
      .eq('id', selectedOrder.value.id)

    if (updateError) {
      console.error('❌ 更新订单状态失败:', updateError)
      throw updateError
    }

    // 2. 记录操作日志（包含修改原因和图片信息）
    let logContent = `修改原因: ${modifyReason.value.trim()}`
    if (modifyImages.value.length > 0) {
      logContent += `\n附带参考图片: ${modifyImages.value.map(img => img.name).join(', ')}`
    }
    const { error: logError } = await supabase
      .from('service_link_logs')
      .insert({
        order_id: selectedOrder.value.id,
        shop_id: shopInfo.value.id,
        action_type: 'request_modify',
        action_detail: logContent,
        created_at: new Date().toISOString()
      })

    if (logError) {
      console.error('❌ 记录操作日志失败:', logError)
      // 日志失败不影响主流程
    }

    console.log('✅ 修改请求已提交')
    ElMessage.success('修改请求已提交！')
    modifyDialogVisible.value = false
    modifyReason.value = ''

    // 3. 刷新订单列表
    await loadOrders(shopInfo.value.id)
    await loadOperationLogs(shopInfo.value.id)

    // 4. 重新选中新订单列表的第一个（如果有的话）
    if (newOrders.value.length > 0) {
      selectedOrder.value = newOrders.value[0]
    } else if (sentOrders.value.length > 0) {
      selectedOrder.value = sentOrders.value[0]
    } else {
      selectedOrder.value = null
    }

  } catch (e) {
    console.error('❌ 请求修改失败:', e)
    ElMessage.error('提交失败，请重试')
  } finally {
    modifying.value = false
  }
}

// 复制邮件
function copyEmail() {
  if (!latestEmailContent.value) {
    ElMessage.warning('暂无邮件内容可复制')
    return
  }
  navigator.clipboard.writeText(latestEmailContent.value)
  ElMessage.success('邮件内容已复制')
}

// 获取日志图标
function getLogIcon(type) {
  const icons = {
    email: '📧',
    design: '✍️',
    order: '📝',
    view: '👁️',
    confirm: '✅',
    modify: '✏️'
  }
  return icons[type] || '📋'
}

// 获取形状路径
function getShapePath(shape) {
  const paths = {
    '心形': 'M50 85 C20 55 0 35 15 20 C30 5 45 15 50 25 C55 15 70 5 85 20 C100 35 80 55 50 85Z',
    '圆形': 'M50 10 A40 40 0 1 1 50 90 A40 40 0 1 1 50 10',
    '骨头形': 'M15 50 L25 30 L35 50 L25 70 Z M65 50 L75 30 L85 50 L75 70 Z M30 35 L70 35 L70 65 L30 65 Z',
    '方形': 'M15 15 L85 15 L85 85 L15 85 Z'
  }
  return paths[shape] || paths['圆形']
}

// 获取颜色值
function getColorHex(color) {
  const colors = {
    '金色': '#fbbf24',
    '银色': '#9ca3af',
    '玫瑰金': '#f472b6',
    '黑色': '#374151',
    '蓝色': '#3b82f6'
  }
  return colors[color] || '#fbbf24'
}

function getColorStroke(color) {
  const colors = {
    '金色': '#f59e0b',
    '银色': '#6b7280',
    '玫瑰金': '#ec4899',
    '黑色': '#1f2937',
    '蓝色': '#2563eb'
  }
  return colors[color] || '#f59e0b'
}

// 订单分组
const newOrders = computed(() => orders.value.filter(o => o.email_status === 'pending' || !o.email_status))
const sentOrders = computed(() => orders.value.filter(o => ['sent', 'confirmed', 'modify'].includes(o.email_status)))

// 超时判断：创建超过24小时且未确认
function isOverdue(order) {
  if (order.email_status === 'confirmed') return false
  const createTime = new Date(order.email_sent_at || order.updated_at || order.created_at)
  const hours = (Date.now() - createTime.getTime()) / (1000 * 60 * 60)
  return hours > 24
}

function getOverdueHours(order) {
  const createTime = new Date(order.email_sent_at || order.updated_at || order.created_at)
  const hours = (Date.now() - createTime.getTime()) / (1000 * 60 * 60)
  return Math.floor(hours)
}

// 当前订单的操作日志
const currentOrderLogs = computed(() => {
  if (!selectedOrder.value) return []
  return operationLogs.value.filter(log => log.raw?.order_id === selectedOrder.value.id)
})

// 格式化颜色+尺寸
function formatColorSize(color, size) {
  const colorText = color || ''
  const sizeText = size || ''
  if (!colorText && !sizeText) return '-'
  if (!colorText) return sizeText
  if (!sizeText) return colorText
  return `${colorText} · ${sizeText}`
}

// 产品图片加载失败处理
function onProductImageError(event, order) {
  console.warn('产品图片加载失败:', order.etsy_order_id)
  order.product_image = null // 清除失败的URL，显示SVG兜底
}

// 效果图加载失败处理
function onEffectImageError() {
  console.warn('效果图加载失败，切换到SVG兜底')
  if (selectedOrder.value) {
    selectedOrder.value.effect_image_url = null
  }
}

// 订单详情区产品图片加载失败处理
function onDetailProductImageError() {
  console.warn('订单详情区产品实拍图加载失败:', selectedOrder.value?.etsy_order_id)
  if (selectedOrder.value) {
    selectedOrder.value.product_image = null
  }
}

// 获取设计链接
function getDesignLink() {
  const designToken = shopInfo.value?.design_token || token.value
  return `/design/${shopCode.value}?token=${designToken}`
}

// 下载JPG图片
function downloadImage() {
  if (!selectedOrder.value) return
  
  // 如果有效果图URL，下载效果图
  if (selectedOrder.value.effect_image_url) {
    const link = document.createElement('a')
    link.href = selectedOrder.value.effect_image_url
    link.download = `effect_${selectedOrder.value.etsy_order_id}.jpg`
    link.target = '_blank'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  } else {
    ElMessage.warning('暂无效果图可下载')
  }
}

// 格式化短时间（用于操作历史）
function formatShortTime(timeStr) {
  if (!timeStr) return '--'
  const date = new Date(timeStr)
  return `${date.getMonth() + 1}/${date.getDate()} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
}

// 客户确认设计（区别于运营确认）
async function handleCustomerConfirm() {
  if (!selectedOrder.value || !shopInfo.value) {
    ElMessage.warning('请先选择订单')
    return
  }

  try {
    const confirmed = await ElMessageBox.confirm(
      '确认该设计效果符合预期？确认后将提交生产。',
      '确认设计',
      {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'success'
      }
    ).catch(() => false)

    if (!confirmed) return

    confirming.value = true
    console.log('✅ 客户确认设计:', selectedOrder.value.etsy_order_id)

    // 1. 更新订单状态（同时更新status字段）
    const { error: updateError } = await supabase
      .from('orders')
      .update({ 
        email_status: 'confirmed',
        status: '待创建',
        updated_at: new Date().toISOString()
      })
      .eq('id', selectedOrder.value.id)

    if (updateError) {
      console.error('❌ 更新订单状态失败:', updateError)
      throw updateError
    }

    // 2. 记录操作日志
    await supabase
      .from('service_link_logs')
      .insert({
        order_id: selectedOrder.value.id,
        shop_id: shopInfo.value.id,
        action_type: 'customer_confirm',
        action_detail: '客户确认设计',
        created_at: new Date().toISOString()
      })

    console.log('✅ 设计确认成功')
    ElMessage.success('设计已确认！感谢您的确认。')

    // 3. 刷新数据
    await loadOrders(shopInfo.value.id)
    await loadOperationLogs(shopInfo.value.id)

    // 4. 重新选中订单
    if (newOrders.value.length > 0) {
      selectedOrder.value = newOrders.value[0]
    } else if (sentOrders.value.length > 0) {
      selectedOrder.value = sentOrders.value[0]
    } else {
      selectedOrder.value = null
    }

  } catch (e) {
    console.error('❌ 确认失败:', e)
    ElMessage.error('确认失败，请重试')
  } finally {
    confirming.value = false
  }
}

// 获取图标路径（用于小图标）
function getShapeIconPath(shape) {
  const paths = {
    '心形': 'M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l8.84-8.84 1.06-1.06a5.5 5.5 0 0 0 0-7.78z',
    '圆形': 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z',
    '骨头形': 'M7 10c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm10 0c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm-5 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z',
    '方形': 'M3 3h18v18H3z'
  }
  return paths[shape] || paths['圆形']
}

// 获取邮件状态类型
function getEmailStatusType(status) {
  const map = {
    pending: 'info',
    sent: 'primary',
    confirmed: 'success',
    modify: 'danger'
  }
  return map[status] || 'info'
}

// 获取状态角标样式类
function getStatusBadgeClass(status) {
  const map = {
    pending: 'badge-red',
    sent: 'badge-blue',
    confirmed: 'badge-green',
    modify: 'badge-orange'
  }
  return map[status] || 'badge-red'
}

// 获取邮件状态文本
function getEmailStatusText(status) {
  const map = {
    pending: '草稿',
    sent: '已发送',
    confirmed: '已确认',
    modify: '需修改'
  }
  return map[status] || status
}

// 格式化时间
function formatTime(timeStr) {
  if (!timeStr) return '--'
  const date = new Date(timeStr)
  return `${date.getFullYear()}/${(date.getMonth() + 1).toString().padStart(2, '0')}/${date.getDate().toString().padStart(2, '0')} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
}

// 初始化
onMounted(() => {
  validateAndLoad()
})
</script>

<style scoped>
/* Notion 风格基础 */
.service-link-page {
  min-height: 100vh;
  background: #f7f7f7;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* 顶部导航 */
.page-header {
  background: #ffffff;
  border-bottom: 1px solid #e5e5e5;
  padding: 12px 32px;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 1600px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.shop-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.shop-info h1 {
  font-size: 20px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
}

.shop-lang {
  background: #e8f0fe;
  color: #1a73e8;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.modify-design-btn {
  background: #f97316 !important;
  border-color: #f97316 !important;
  color: #ffffff !important;
  border-radius: 6px;
  font-weight: 500;
}

.modify-design-btn:hover {
  background: #ea580c !important;
  border-color: #ea580c !important;
}

.btn-icon {
  margin-right: 6px;
}

/* 统计栏 */
.stats-bar {
  max-width: 1600px;
  margin: 20px auto;
  padding: 0 32px;
  display: flex;
  gap: 12px;
}

.stat-card {
  background: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  padding: 12px 20px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
}

.stat-card.pending { border-left: 4px solid #f97316; }
.stat-card.sent { border-left: 4px solid #3b82f6; }
.stat-card.confirmed { border-left: 4px solid #22c55e; }
.stat-card.modify { border-left: 4px solid #ef4444; }

.stat-label {
  font-size: 13px;
  color: #666666;
}

.stat-value {
  font-size: 28px;
  font-weight: 600;
  color: #1a1a1a;
}

/* 主内容 */
.main-content {
  max-width: 1600px;
  margin: 0 auto;
  padding: 0 32px 32px;
  display: flex;
  gap: 16px;
  height: calc(100vh - 200px);
}

/* 左侧面板 - 订单列表 */
.order-list-panel {
  width: 340px;
  background: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.panel-header {
  padding: 14px 16px;
  border-bottom: 1px solid #f0f0f0;
}

.panel-header h3 {
  font-size: 14px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
}

.panel-hint {
  font-size: 12px;
  color: #999999;
  display: block;
  margin-top: 2px;
}

.order-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.order-item {
  padding: 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.15s ease;
  border: 1px solid transparent;
  margin-bottom: 6px;
}

.order-item:hover {
  background: #f8f8f8;
}

.order-item.active {
  background: #e8f4ff;
  border-color: #b3d7ff;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.order-id {
  font-family: 'SF Mono', Consolas, monospace;
  font-size: 13px;
  font-weight: 600;
  color: #1a1a1a;
}

.order-product {
  display: flex;
  gap: 8px;
  font-size: 12px;
  color: #666666;
  margin-bottom: 4px;
}

.order-text {
  font-size: 11px;
  color: #999999;
  margin-bottom: 4px;
}

.order-time {
  font-size: 11px;
  color: #999999;
  display: flex;
  align-items: center;
  gap: 4px;
}

/* ========== Notion风格左侧栏样式（原封不动来自客服外链左侧栏.html） ========== */
.order-list-panel.notion-style {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.order-list-panel.notion-style .header {
  padding: 24px 20px;
  border-bottom: 1px solid #f3f4f6;
}

.order-list-panel.notion-style .header h1 {
  font-size: 20px;
  font-weight: 700;
  color: #111827;
  margin: 0;
}

.order-list-panel.notion-style .header p {
  font-size: 14px;
  color: #9ca3af;
  margin-top: 4px;
  margin-bottom: 0;
}

/* 分类装饰标签 */
.order-list-panel.notion-style .section-tag {
  display: inline-block;
  padding: 3px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  line-height: 1.2;
  margin: 8px 12px 4px;
}

.order-list-panel.notion-style .tag-new {
  background-color: #dcc296;
  color: white;
}

.order-list-panel.notion-style .tag-sent {
  background-color: #c0c0c0;
  color: white;
}

/* 订单列表 */
.order-list-panel.notion-style .notion-list {
  padding: 4px 8px;
}

/* 订单卡片 */
.order-list-panel.notion-style .order-card {
  margin-bottom: 12px;
  padding: 16px;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  position: relative;
  transition: all 0.2s;
  cursor: pointer;
  background: white;
}

.order-list-panel.notion-style .order-card:hover {
  border-color: #d1d5db;
  background-color: #fafafa;
}

/* 紧凑版订单卡片 */
.order-list-panel.notion-style .compact-card {
  padding: 6px 10px;
  border: 1px solid #f0f0f0;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.15s;
  margin-bottom: 4px;
}

.order-list-panel.notion-style .compact-card:hover {
  background: #f8f9fa;
  border-color: #e0e0e0;
}

.order-list-panel.notion-style .compact-card.highlight {
  background: #eff6ff;
  border-color: #93c5fd;
}

/* 紧凑版状态标签 */
.status-badge-compact {
  font-size: 10px;
  padding: 1px 6px;
  border-radius: 8px;
  font-weight: 500;
}

.badge-red-compact {
  background-color: #ef4444;
  color: white;
}

.badge-blue-compact {
  background-color: #3b82f6;
  color: white;
}

.order-list-panel.notion-style .order-card.highlight {
  background-color: #f0f7ff;
  border-color: #bfdbfe;
}

/* 状态角标 */
.order-list-panel.notion-style .status-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 10px;
  font-weight: bold;
}

.order-list-panel.notion-style .badge-red {
  background-color: #ef4444;
  color: white;
}

.order-list-panel.notion-style .badge-blue {
  background-color: #3b82f6;
  color: white;
}

.order-list-panel.notion-style .user-link {
  font-size: 14px;
  color: #374151;
  text-decoration: underline;
  font-weight: 500;
}

.order-list-panel.notion-style .order-number {
  font-size: 16px;
  color: #dc2626;
  font-weight: 600;
  margin: 2px 0 10px;
}

.order-list-panel.notion-style .product-img {
  width: 80px;
  height: 80px;
  border-radius: 6px;
  object-fit: cover;
  background-color: #f3f4f6;
}

.order-list-panel.notion-style .item-tag {
  background-color: #e5e7eb;
  color: #6b7280;
  font-size: 11px;
  padding: 1px 6px;
  border-radius: 4px;
  display: inline-block;
  margin-bottom: 4px;
}

/* 核心修改：缩窄行高 */
.order-list-panel.notion-style .item-desc {
  font-size: 13px;
  color: #4b5563;
  line-height: 1.2;
  margin-bottom: 4px;
}

.order-list-panel.notion-style .item-meta {
  font-size: 12px;
  color: #6b7280;
  line-height: 1.2;
  margin-top: 2px;
}

.order-list-panel.notion-style .meta-bold {
  color: #111827;
  font-weight: 600;
}

.order-list-panel.notion-style .h-8 {
  height: 32px;
}

/* flex工具类 */
.order-list-panel.notion-style .flex {
  display: flex;
}

.order-list-panel.notion-style .gap-3 {
  gap: 12px;
}

.order-list-panel.notion-style .flex-shrink-0 {
  flex-shrink: 0;
}

.order-list-panel.notion-style .flex-1 {
  flex: 1;
}

.order-list-panel.notion-style .items-center {
  align-items: center;
}

.order-list-panel.notion-style .justify-center {
  justify-content: center;
}

.order-list-panel.notion-style .border {
  border-width: 1px;
}

.order-list-panel.notion-style .border-gray-100 {
  border-color: #f3f4f6;
}

.order-list-panel.notion-style .text-gray-300 {
  color: #d1d5db;
}

/* ========== 新版左侧订单列表样式 ========== */
.order-list-panel-new {
  width: 380px;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.panel-header-new {
  padding: 20px;
  border-bottom: 1px solid #f3f4f6;
}

.panel-header-new h3 {
  font-size: 18px;
  font-weight: 700;
  color: #111827;
  margin: 0;
}

.panel-header-new p {
  font-size: 14px;
  color: #9ca3af;
  margin: 4px 0 0 0;
}

/* 分类装饰标签 */
.section-tag {
  display: inline-block;
  padding: 3px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  line-height: 1.2;
  margin: 8px 12px 4px;
}

.tag-new {
  background-color: #dcc296;
  color: white;
}

.tag-sent {
  background-color: #c0c0c0;
  color: white;
}

/* 订单列表 */
.order-list-new {
  flex: 1;
  overflow-y: auto;
  padding: 0 12px;
}

/* 订单卡片 */
.order-card-new {
  margin-bottom: 12px;
  padding: 16px;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  position: relative;
  transition: all 0.2s;
  cursor: pointer;
  background: #ffffff;
}

.order-card-new:hover {
  border-color: #d1d5db;
  background-color: #fafafa;
}

.order-card-new.highlight {
  background-color: #f0f7ff;
  border-color: #bfdbfe;
}

/* 状态角标 */
.status-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 10px;
  font-weight: bold;
}

.badge-red {
  background-color: #ef4444;
  color: white;
}

.badge-blue {
  background-color: #3b82f6;
  color: white;
}

.user-link {
  font-size: 14px;
  color: #374151;
  text-decoration: underline;
  font-weight: 500;
}

.order-number {
  font-size: 16px;
  color: #dc2626;
  font-weight: 600;
  margin: 2px 0 10px;
}

.order-card-content {
  display: flex;
  gap: 12px;
}

.product-img-wrapper-new {
  width: 80px;
  height: 80px;
  border-radius: 6px;
  background-color: #f3f4f6;
  border: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.product-svg-new {
  width: 50px;
  height: 50px;
}

.order-info-new {
  flex: 1;
  min-width: 0;
}

.item-tag {
  background-color: #e5e7eb;
  color: #6b7280;
  font-size: 11px;
  padding: 1px 6px;
  border-radius: 4px;
  display: inline-block;
  margin-bottom: 4px;
}

.item-desc {
  font-size: 13px;
  color: #4b5563;
  line-height: 1.2;
  margin-bottom: 4px;
}

.item-meta {
  font-size: 12px;
  color: #6b7280;
  line-height: 1.2;
  margin-top: 2px;
}

.meta-bold {
  color: #111827;
  font-weight: 600;
}

/* 中间面板 - 订单详情 */
.detail-panel {
  width: 68%;
  background: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.detail-content {
  padding: 20px;
  overflow-y: auto;
  flex: 1;
}

.detail-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 16px;
}

.detail-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
}

.detail-header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.detail-header-actions .status-tag {
  margin-right: 8px;
}

/* 效果图预览 - 蓝框：增加高度，作为主体 */
.effect-section h4 {
  font-size: 14px;
  font-weight: 600;
  color: #333333;
  margin: 0 0 12px 0;
}

/* 订单详情区域 - 包含蓝框和红框 */
.order-detail-section {
  display: flex;
  flex-direction: column;
}

/* 效果图预览区域 */
.effect-section {
  margin-bottom: 12px;
}

.effect-section h4 {
  font-size: 14px;
  font-weight: 600;
  color: #333333;
  margin: 0 0 12px 0;
}

.effect-preview {
  background: #ffffff;
  border-radius: 8px;
  padding: 0;
  text-align: center;
  width: 100%;
  box-sizing: border-box;
  overflow: hidden;
}

/* 效果图主体 - 填满容器 */
.effect-preview.hero {
  padding: 0;
  min-height: 320px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 修改外链按钮样式 - 标题行版本 */
.design-link-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 5px 11px;
  font-size: 12px;
  background: #6b7280;
  color: #ffffff;
  border-radius: 4px;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.2s;
  height: 24px;
  box-sizing: border-box;
}

.design-link-btn:hover {
  background: #4b5563;
  color: #ffffff;
}

/* 灰色按钮样式 - 标题行版本 */
.gray-btn {
  background: #6b7280 !important;
  border-color: #6b7280 !important;
  color: #ffffff !important;
  font-size: 12px !important;
  padding: 5px 11px !important;
  height: 24px;
}

.gray-btn:hover {
  background: #4b5563 !important;
  border-color: #4b5563 !important;
}

.gray-btn .btn-arrow {
  margin-left: 4px;
  transition: transform 0.3s;
}

.gray-btn .btn-arrow.rotate {
  transform: rotate(180deg);
}

/* 效果图真实图片 - 填满容器 */
.effect-real-image {
  width: 100%;
  height: auto;
  max-height: 100%;
  object-fit: contain;
  display: block;
}

/* SVG兜底效果图 - 填满容器 */
.effect-fallback-svg {
  width: 100%;
  height: auto;
  max-width: 100%;
  max-height: 100%;
  display: block;
}

/* 订单信息块样式 - 红框：紧凑版本 */
.order-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  display: flex;
  flex-direction: column;
}

/* 紧凑版本 - 缩小字号和间距 */
.order-card.compact {
  padding: 12px 16px;
}

/* 向左对齐 */
.order-card.align-left {
  align-items: stretch;
}

/* 绿框：客户信息头部 - 放在最上面 */
.order-card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
  padding-bottom: 10px;
  border-bottom: 1px solid #f0f0f0;
}

.order-card-header .user-link {
  color: #6b7280;
  text-decoration: underline;
  font-size: 13px;
  cursor: pointer;
}

.order-card-header .user-link:hover {
  color: #374151;
}

.order-card-header .order-id {
  color: #374151;
  font-size: 13px;
}

/* 旧样式兼容 */
.order-card-footer {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid #f0f0f0;
}

.order-card-footer .user-link {
  color: #6b7280;
  text-decoration: underline;
  font-size: 13px;
  cursor: pointer;
}

.order-card-footer .user-link:hover {
  color: #374151;
}

.order-card-footer .order-id {
  color: #374151;
  font-size: 13px;
}

.order-card-content {
  display: flex;
  gap: 20px;
  align-items: flex-end;
}

.order-card-left {
  display: flex;
  flex: 1;
  gap: 12px;
  align-items: flex-end;
}

.product-img-wrapper {
  width: 120px;
  height: 120px;
  border-radius: 8px;
  background-color: #f3f4f6;
  border: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.product-icon {
  width: 60px;
  height: 60px;
}

.product-text {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}

.tag-custom {
  background-color: #e5e7eb;
  color: #4b5563;
  padding: 2px 6px;
  border-radius: 10px;
  font-size: 11px;
  display: inline-block;
  margin-bottom: 4px;
  width: fit-content;
}

.product-title-zh {
  font-weight: 500;
  color: #111827;
  font-size: 13px;
  margin: 0 0 2px 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.product-title-en {
  color: #6b7280;
  font-size: 12px;
  line-height: 1.3;
  margin: 0;
}

.product-title-en.last {
  margin-top: 2px;
}

.order-card-right {
  width: 240px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}

.info-row {
  margin-bottom: 4px;
  display: flex;
  align-items: flex-start;
  font-size: 12px;
}

.info-row.last {
  margin-bottom: 0;
}

.info-label {
  color: #9ca3af;
  min-width: 70px;
}

.info-value {
  color: #111827;
  font-weight: 500;
}

/* 紧凑版本内容 */
.order-card.compact .order-card-content {
  gap: 16px;
}

.order-card.compact .product-img-wrapper {
  width: 120px;
  height: 120px;
}

.order-card.compact .product-icon {
  width: 60px;
  height: 60px;
}

.order-card.compact .product-title-zh {
  font-size: 12px;
}

.order-card.compact .product-title-en {
  font-size: 11px;
}

.order-card.compact .info-row {
  font-size: 11px;
  margin-bottom: 3px;
}

.order-card.compact .info-label {
  min-width: 60px;
}

/* 旧的产品卡片样式（兼容保留） */
.product-card {
  background: #fafafa;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
}

.product-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.brand-name {
  font-weight: 600;
  color: #1a1a1a;
}

.order-number {
  font-family: monospace;
  color: #666666;
  font-size: 13px;
}

.custom-tag {
  margin-bottom: 8px;
}

.product-desc {
  margin-bottom: 12px;
}

.desc-cn {
  font-size: 13px;
  color: #333333;
  margin: 0 0 4px 0;
}

.desc-en {
  font-size: 12px;
  color: #999999;
  margin: 0;
}

.product-specs {
  border-top: 1px solid #e5e5e5;
  padding-top: 12px;
}

.spec-row {
  display: flex;
  font-size: 13px;
  margin-bottom: 6px;
}

.spec-label {
  color: #666666;
  min-width: 90px;
}

.spec-value {
  color: #1a1a1a;
}

/* 修改设计下拉框 */
.design-collapsible {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  margin-top: 16px;
  overflow: hidden;
}

/* 绿色按钮行 */
.design-button-row {
  padding: 12px 16px;
  display: flex;
  align-items: center;
}

/* 当前订单信息 */
.current-order-info {
  padding: 0 16px 12px;
  font-size: 12px;
  color: #666666;
  border-bottom: 1px solid #e5e7eb;
}

/* 绿色按钮行 */
.design-button-row {
  padding: 12px 16px;
  display: flex;
  align-items: center;
}

.design-toggle-btn {
  background: #22c55e !important;
  border-color: #22c55e !important;
  color: #ffffff !important;
  font-weight: 500;
}

.design-toggle-btn:hover {
  background: #16a34a !important;
  border-color: #16a34a !important;
}

.btn-icon {
  margin-right: 4px;
}

.btn-arrow {
  margin-left: 4px;
  transition: transform 0.3s;
}

.btn-arrow.rotate {
  transform: rotate(180deg);
}

.design-content {
  padding: 16px;
  background: #ffffff;
}

/* 客户修改意见 */
.customer-feedback h4 {
  font-size: 14px;
  font-weight: 600;
  color: #333333;
  margin: 0 0 12px 0;
}

.feedback-form {
  display: flex;
  gap: 12px;
  margin-bottom: 12px;
}

.feedback-input {
  flex: 1;
}

.reference-upload {
  width: 160px;
}

.upload-area {
  height: 100%;
  min-height: 72px;
  border: 2px dashed #d1d5db;
  border-radius: 6px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.upload-area:hover {
  border-color: #9ca3af;
  background: #f9fafb;
}

.upload-icon {
  font-size: 24px;
  margin-bottom: 4px;
}

.upload-text {
  font-size: 10px;
  color: #9ca3af;
  text-align: center;
}

.design-actions {
  display: flex;
  gap: 12px;
}

.design-actions .submit-btn {
  flex: 1;
  background: #3b82f6 !important;
  border-color: #3b82f6 !important;
}

.design-actions .edit-btn {
  flex: 1;
  background: #10b981 !important;
  border-color: #10b981 !important;
}

/* 右侧面板 */
.action-panel {
  width: 32%;
  background: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.panel-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.panel-section:first-child {
  flex: 0 0 auto;
}

.email-section {
  border-bottom: 1px solid #e0e0e0;
}

.email-preview {
  padding: 16px;
}

.email-body {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 12px;
  font-size: 13px;
  line-height: 1.6;
  color: #374151;
  margin-bottom: 12px;
}

.email-body p {
  margin: 6px 0;
}

.copy-btn {
  width: 33% !important;
  margin: 0 auto !important;
  display: block !important;
  background: #e5e7eb !important;
  border-color: #d1d5db !important;
  color: #6b7280 !important;
}
.copy-btn:hover {
  background: #d1d5db !important;
  border-color: #c0c4cc !important;
  color: #4b5563 !important;
}

/* 操作历史 */
.history-section .panel-header {
  border-top: none;
}

.history-timeline {
  padding: 12px 16px;
  overflow-y: auto;
  flex: 1;
}

.history-item {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  margin-bottom: 12px;
  font-size: 12px;
}

.history-item:last-child {
  margin-bottom: 0;
}

.history-time {
  color: #999999;
  min-width: 40px;
  font-size: 11px;
}

.history-icon {
  font-size: 14px;
}

.history-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.history-label {
  color: #666666;
  font-weight: 500;
}

.history-text {
  color: #999999;
  font-size: 11px;
}

/* 空状态 */
.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100px;
}

/* 状态标签颜色 */
:deep(.el-tag) {
  border-radius: 4px;
}

/* ========== 加载和错误状态样式 ========== */

/* 加载中遮罩 */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.loading-content {
  text-align: center;
}

.loading-icon {
  color: #3b82f6;
  animation: rotate 1s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.loading-text {
  margin-top: 16px;
  color: #6b7280;
  font-size: 14px;
}

/* 错误页面 */
.error-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: #f9fafb;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.error-content {
  text-align: center;
  max-width: 400px;
  padding: 40px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.error-icon {
  margin-bottom: 20px;
}

.error-title {
  font-size: 20px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 12px 0;
}

.error-desc {
  font-size: 14px;
  color: #6b7280;
  margin: 0 0 8px 0;
  line-height: 1.5;
}

.error-hint {
  font-size: 13px;
  color: #9ca3af;
  margin: 0 0 24px 0;
}

/* 操作按钮区域样式 */
.action-buttons-section {
  border-bottom: 1px solid #e0e0e0;
}

.action-buttons {
  padding: 16px;
  display: flex;
  flex-direction: row;
  justify-content: center;
  gap: 8px;
}

.confirm-btn {
  width: 33%;
  background: #22c55e !important;
  border-color: #22c55e !important;
  color: #ffffff !important;
  font-weight: 500;
  font-size: 13px !important;
  padding: 10px 0 !important;
  height: auto !important;
}

.confirm-btn:hover {
  background: #16a34a !important;
  border-color: #16a34a !important;
}

.modify-btn {
  width: 33%;
  background: #f97316 !important;
  border-color: #f97316 !important;
  color: #ffffff !important;
  font-weight: 500;
  font-size: 13px !important;
  padding: 10px 0 !important;
  height: auto !important;
}

.modify-btn:hover {
  background: #ea580c !important;
  border-color: #ea580c !important;
}

.action-hint {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: #f3f4f6;
  border-radius: 6px;
  font-size: 13px;
  color: #6b7280;
}

.action-hint.success {
  background: #ecfdf5;
  color: #059669;
}

.action-hint.warning {
  background: #fffbeb;
  color: #d97706;
}

/* 修改对话框样式 */
.modify-dialog-content {
  padding: 8px 0;
}

.dialog-hint {
  font-size: 14px;
  color: #374151;
  margin: 0 0 12px 0;
}

/* 产品实拍图样式 */
.product-real-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 6px;
}



/* 复制按钮样式 - 蓝色背景 */
.copy-btn {
  width: 100%;
  background: #3b82f6 !important;
  border-color: #3b82f6 !important;
  color: #ffffff !important;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.copy-btn:hover {
  background: #2563eb !important;
  border-color: #2563eb !important;
}

.copy-icon {
  font-size: 16px;
}
</style>
