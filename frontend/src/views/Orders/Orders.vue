<template>
  <div class="page-wrapper">
    <!-- 顶部Header -->
    <header class="page-header">
      <div class="header-content">
        <div class="header-left">
          <div class="logo-icon">
            <el-icon><Box /></el-icon>
          </div>
          <div>
            <h1 class="header-title">生产订单管理系统</h1>
            <p class="header-subtitle">POD 自动化仪表盘</p>
          </div>
        </div>
        <div class="header-right">
          <el-button circle><el-icon><Bell /></el-icon></el-button>
          <el-avatar src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" />
        </div>
      </div>
    </header>

    <!-- 主体容器 -->
    <div class="main-container">
      <!-- 左侧边栏 -->
      <aside class="sidebar">
        <!-- 导航菜单 -->
        <nav class="nav-menu">
          <button :class="['nav-item']" @click="$router.push('/')">
            <el-icon><Grid /></el-icon>
            <span>仪表盘总览</span>
          </button>
          <button :class="['nav-item', { active: activeTab === 'pending' }]" @click="switchTab('pending')">
            <el-icon><Clock /></el-icon>
            <span>待确认订单</span>
            <el-tag v-if="pendingOrders.length > 0" size="small" class="badge">{{ pendingOrders.length }}</el-tag>
          </button>
          <button :class="['nav-item', { active: activeTab === 'producing' }]" @click="switchTab('producing')">
            <el-icon><Setting /></el-icon>
            <span>生产中订单</span>
            <el-tag v-if="producingOrders.length > 0" size="small" type="primary" class="badge">{{ producingOrders.length }}</el-tag>
          </button>
          <button :class="['nav-item', { active: activeTab === 'completed' }]" @click="switchTab('completed')">
            <el-icon><CircleCheck /></el-icon>
            <span>已完成订单</span>
          </button>
          <button :class="['nav-item']">
            <el-icon><Message /></el-icon>
            <span>邮件模板</span>
          </button>
        </nav>

        <!-- 统计圆形仪表盘 -->
        <div class="stats-grid">
          <div class="stat-card">
            <div class="circular-progress">
              <svg><circle class="bg-ring" cx="40" cy="40" r="35"></circle><circle class="progress-ring" cx="40" cy="40" r="35" :style="getProgressStyle(100, '#2080f0')"></circle></svg>
              <div class="circular-content"><span class="stat-number">{{ totalOrders }}</span></div>
            </div>
            <div class="stat-info"><p class="stat-label">总订单</p><p class="stat-sublabel">本月累计</p></div>
          </div>

          <div class="stat-card">
            <div class="circular-progress">
              <svg><circle class="bg-ring" cx="40" cy="40" r="35"></circle><circle class="progress-ring" cx="40" cy="40" r="35" :style="getProgressStyle(pendingPercent, '#f0a020')"></circle></svg>
              <div class="circular-content"><span class="stat-number">{{ pendingPercent }}<span class="percent">%</span></span></div>
            </div>
            <div class="stat-info"><p class="stat-label">待处理</p><p class="stat-sublabel">需确认</p></div>
          </div>

          <div class="stat-card">
            <div class="circular-progress">
              <svg><circle class="bg-ring" cx="40" cy="40" r="35"></circle><circle class="progress-ring" cx="40" cy="40" r="35" :style="getProgressStyle(producingPercent, '#8a2be2')"></circle></svg>
              <div class="circular-content"><span class="stat-number">{{ producingPercent }}<span class="percent">%</span></span></div>
            </div>
            <div class="stat-info"><p class="stat-label">生产中</p><p class="stat-sublabel">工厂作业</p></div>
          </div>

          <div class="stat-card">
            <div class="circular-progress">
              <svg><circle class="bg-ring" cx="40" cy="40" r="35"></circle><circle class="progress-ring" cx="40" cy="40" r="35" :style="getProgressStyle(completedPercent, '#18a058')"></circle></svg>
              <div class="circular-content"><span class="stat-number">{{ completedPercent }}<span class="percent">%</span></span></div>
            </div>
            <div class="stat-info"><p class="stat-label">已交付</p><p class="stat-sublabel">物流送达</p></div>
          </div>
        </div>
      </aside>

      <!-- 右侧主内容区 -->
      <main class="main-content">
        <!-- 待确认订单 -->
        <div v-show="activeTab === 'pending'" class="content-panel">
          <section class="orders-section">
            <div class="section-header">
              <div>
                <h2 class="section-title">待确认订单</h2>
                <p class="section-subtitle">最新的生产订单，需要生成效果图或发送确认邮件。</p>
              </div>
            </div>
            <div class="search-bar">
              <el-input v-model="searchText" placeholder="搜索订单号、客户名称或产品..." prefix-icon="Search" clearable />
            </div>
            <el-table :data="pendingOrders" v-loading="loading" stripe style="width: 100%">
              <el-table-column prop="etsy_order_id" label="订单ID" width="140" fixed />
              <el-table-column prop="customer_name" label="客户名称" width="120" />
              <el-table-column label="产品" width="100">
                <template #default="scope">
                  <span>{{ scope.row.matched_sku_id || '-' }}</span>
                </template>
              </el-table-column>
              <el-table-column label="设计稿件" width="90">
                <template #default="scope">
                  <div class="action-icons">
                    <el-icon class="action-icon"><View /></el-icon>
                    <el-icon class="action-icon"><Download /></el-icon>
                  </div>
                </template>
              </el-table-column>
              <el-table-column label="确认邮件" width="90">
                <template #default="scope">
                  <div class="action-icons">
                    <el-icon class="action-icon"><View /></el-icon>
                    <el-icon class="action-icon"><Download /></el-icon>
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop="quantity" label="数量" width="80" />
              <el-table-column label="状态" width="100">
                <template #default="scope">
                  <el-tag :type="getStatusType(scope.row.status)" size="small">
                    {{ getStatusText(scope.row.status) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="创建日期" width="110">
                <template #default="scope">
                  {{ formatDate(scope.row.created_at) }}
                </template>
              </el-table-column>
              <el-table-column label="操作" width="180" fixed="right">
                <template #default="scope">
                  <div style="display: flex; gap: 8px; align-items: center;">
                    <el-button type="primary" size="small" @click="handleConfirmOrder(scope.row)">订单确认</el-button>
                    <el-dropdown trigger="click">
                      <el-button size="small">更多</el-button>
                      <template #dropdown>
                        <el-dropdown-menu>
                          <el-dropdown-item @click="handleCancelOrder(scope.row)">取消订单</el-dropdown-item>
                        </el-dropdown-menu>
                      </template>
                    </el-dropdown>
                  </div>
                </template>
              </el-table-column>
            </el-table>
          </section>
        </div>

        <!-- 生产中订单 -->
        <div v-show="activeTab === 'producing'" class="content-panel">
          <section class="orders-section">
            <div class="section-header">
              <div>
                <h2 class="section-title">生产中订单</h2>
                <p class="section-subtitle">订单已进入生产流程，监控生产进度与物流安排。</p>
              </div>
            </div>
            <div class="search-bar">
              <el-input v-model="searchText" placeholder="搜索订单号、客户名称或产品..." prefix-icon="Search" clearable />
            </div>
            <el-table :data="producingOrders" v-loading="loading" stripe style="width: 100%">
              <el-table-column prop="customer_name" label="客户名称" width="120" fixed />
              <el-table-column label="产品" width="100">
                <template #default="scope">
                  <span>{{ scope.row.matched_sku_id || '-' }}</span>
                </template>
              </el-table-column>
              <el-table-column label="生产表单" width="90">
                <template #default="scope">
                  <div class="action-icons">
                    <el-icon class="action-icon"><View /></el-icon>
                    <el-icon class="action-icon"><Download /></el-icon>
                  </div>
                </template>
              </el-table-column>
              <el-table-column label="进度" width="150">
                <template #default="scope">
                  <el-progress :percentage="scope.row.progress || 0" :color="getProgressBarColor(scope.row.progress)" />
                </template>
              </el-table-column>
              <el-table-column prop="quantity" label="数量" width="80" />
              <el-table-column label="状态" width="100">
                <template #default="scope">
                  <el-tag type="warning" size="small">
                    {{ getStatusText(scope.row.status) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="物流面单" width="90">
                <template #default="scope">
                  <div class="action-icons">
                    <el-icon class="action-icon"><View /></el-icon>
                    <el-icon class="action-icon"><Download /></el-icon>
                  </div>
                </template>
              </el-table-column>
              <el-table-column label="下单取货" width="90">
                <template #default="scope">
                  <el-checkbox v-model="scope.row.picked" disabled />
                </template>
              </el-table-column>
              <el-table-column label="创建日期" width="110">
                <template #default="scope">
                  {{ formatDate(scope.row.created_at) }}
                </template>
              </el-table-column>
              <el-table-column label="操作" width="180" fixed="right">
                <template #default="scope">
                  <div style="display: flex; gap: 8px; align-items: center;">
                    <el-button type="primary" size="small" @click="handlePickup(scope.row)">物流取货</el-button>
                    <el-dropdown trigger="click">
                      <el-button size="small">更多</el-button>
                      <template #dropdown>
                        <el-dropdown-menu>
                          <el-dropdown-item @click="handleCancelOrder(scope.row)">取消订单</el-dropdown-item>
                        </el-dropdown-menu>
                      </template>
                    </el-dropdown>
                  </div>
                </template>
              </el-table-column>
            </el-table>
          </section>
        </div>

        <!-- 已完成订单 -->
        <div v-show="activeTab === 'completed'" class="content-panel">
          <section class="orders-section">
            <div class="section-header">
              <div>
                <h2 class="section-title">已完成订单</h2>
                <p class="section-subtitle">发货日起 30 天内订单；集成客户订单信息、效果图、往来邮件。</p>
              </div>
            </div>
            <div class="search-bar">
              <el-input v-model="searchText" placeholder="搜索订单号、客户名称或产品..." prefix-icon="Search" clearable />
            </div>
            <el-table :data="completedOrders" v-loading="loading" stripe style="width: 100%">
              <el-table-column prop="etsy_order_id" label="订单ID" width="140" fixed />
              <el-table-column prop="customer_name" label="客户名称" width="120" />
              <el-table-column label="产品" width="100">
                <template #default="scope">
                  <span>{{ scope.row.matched_sku_id || '-' }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="quantity" label="数量" width="80" />
              <el-table-column label="国家地址" width="150">
                <template #default="scope">
                  <span>{{ getAddress(scope.row) }}</span>
                </template>
              </el-table-column>
              <el-table-column label="发货日期" width="110">
                <template #default="scope">
                  {{ formatDate(scope.row.shipped_at) }}
                </template>
              </el-table-column>
              <el-table-column label="收货日期" width="110">
                <template #default="scope">
                  {{ formatDate(scope.row.completed_at) }}
                </template>
              </el-table-column>
              <el-table-column label="物流送达" width="100">
                <template #default="scope">
                  <span class="delivered-status">已送达</span>
                </template>
              </el-table-column>
              <el-table-column label="追评邮件" width="90">
                <template #default="scope">
                  <el-button size="small" plain><el-icon><Message /></el-icon> 查看</el-button>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="150" fixed="right">
                <template #default="scope">
                  <div style="display: flex; gap: 8px; align-items: center;">
                    <el-button size="small" @click="handleViewDetails(scope.row)">查看详情</el-button>
                    <el-dropdown trigger="click">
                      <el-button size="small">更多</el-button>
                      <template #dropdown>
                        <el-dropdown-menu>
                          <el-dropdown-item @click="handleCancelOrder(scope.row)">取消订单</el-dropdown-item>
                        </el-dropdown-menu>
                      </template>
                    </el-dropdown>
                  </div>
                </template>
              </el-table-column>
            </el-table>
          </section>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useOrderStore } from '../../stores/orderStore'
import { ElMessage } from 'element-plus'
import { Box, Bell, Grid, Clock, Setting, CircleCheck, Message, View, Download } from '@element-plus/icons-vue'

const orderStore = useOrderStore()

// 状态
const activeTab = ref('pending')
const loading = ref(false)
const searchText = ref('')
const pendingOrders = ref([])
const producingOrders = ref([])
const completedOrders = ref([])

// 统计数据
const totalOrders = computed(() => pendingOrders.value.length + producingOrders.value.length + completedOrders.value.length)
const pendingPercent = computed(() => totalOrders.value === 0 ? 0 : Math.round((pendingOrders.value.length / totalOrders.value) * 100))
const producingPercent = computed(() => totalOrders.value === 0 ? 0 : Math.round((producingOrders.value.length / totalOrders.value) * 100))
const completedPercent = computed(() => totalOrders.value === 0 ? 0 : Math.round((completedOrders.value.length / totalOrders.value) * 100))

// 圆形进度条样式
const getProgressStyle = (percent, color) => {
  const circumference = 220
  const offset = circumference - (percent / 100) * circumference
  return { stroke: color, strokeDasharray: circumference, strokeDashoffset: offset }
}

// 切换Tab
const switchTab = (tab) => {
  activeTab.value = tab
  loadOrders()
}

// 加载订单数据
const loadOrders = async () => {
  loading.value = true
  try {
    if (activeTab.value === 'pending') {
      pendingOrders.value = await orderStore.getPendingOrders()
    } else if (activeTab.value === 'producing') {
      producingOrders.value = await orderStore.getProducingOrders()
    } else if (activeTab.value === 'completed') {
      completedOrders.value = await orderStore.getCompletedOrders()
    }
  } catch (error) {
    ElMessage.error('订单数据加载失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

// 状态映射
const getStatusText = (status) => {
  const map = {
    pending: '待确认',
    effect_sent: '效果图已发',
    producing: '生产中',
    delivered: '已送达'
  }
  return map[status] || status
}

const getStatusType = (status) => {
  const map = {
    pending: 'info',
    effect_sent: 'warning',
    producing: 'warning',
    delivered: 'success'
  }
  return map[status] || 'info'
}

// 进度条颜色
const getProgressBarColor = (progress) => {
  if (progress < 30) return '#f56c6c'
  if (progress < 70) return '#e6a23c'
  return '#67c23a'
}

// 日期格式化
const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' })
}

// 获取地址
const getAddress = (order) => {
  // TODO: 从 logistics 表获取地址
  return '-'
}

// 操作处理
const handleConfirmOrder = (order) => {
  ElMessage.info('订单确认功能开发中...')
}

const handleCancelOrder = (order) => {
  ElMessage.warning('取消订单功能开发中...')
}

const handlePickup = (order) => {
  ElMessage.info('物流取货功能开发中...')
}

const handleViewDetails = (order) => {
  ElMessage.info('查看详情功能开发中...')
}

// 初始化加载所有Tab的数据
const loadAllOrders = async () => {
  loading.value = true
  try {
    pendingOrders.value = await orderStore.getPendingOrders()
    producingOrders.value = await orderStore.getProducingOrders()
    completedOrders.value = await orderStore.getCompletedOrders()
  } catch (error) {
    ElMessage.error('订单数据加载失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadAllOrders()
})
</script>

<style scoped>
/* 复用Dashboard样式 */
.page-wrapper { height: 100vh; display: flex; flex-direction: column; overflow: hidden; background: #fafafa; }
.page-header { height: 64px; border-bottom: 1px solid #e5e7eb; display: flex; align-items: center; justify-content: center; z-index: 20; background: #fff; }
.header-content { width: 100%; max-width: 1480px; padding: 0 24px; display: flex; align-items: center; justify-content: space-between; }
.header-left { display: flex; align-items: center; gap: 16px; }
.logo-icon { width: 40px; height: 40px; background: linear-gradient(135deg, #eff6ff 0%, #e0e7ff 100%); border: 1px solid #dbeafe; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #3b82f6; font-size: 20px; }
.header-title { font-size: 18px; font-weight: 600; color: #1f2937; margin: 0; }
.header-subtitle { font-size: 11px; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px; margin: 2px 0 0 0; }
.header-right { display: flex; align-items: center; gap: 16px; }
.main-container { flex: 1; display: flex; overflow: hidden; max-width: 1480px; width: 100%; margin: 0 auto; padding: 24px; gap: 24px; background: #fafafa; }
.sidebar { width: 280px; display: flex; flex-direction: column; gap: 0; flex-shrink: 0; background: #fff; border-radius: 12px; padding: 16px; }
.nav-menu { display: flex; flex-direction: column; gap: 2px; padding: 8px; background: #f9fafb; border-radius: 12px; margin-bottom: 24px; }
.nav-item { display: flex; align-items: center; gap: 12px; padding: 12px 16px; background: transparent; border: none; text-align: left; font-size: 14px; font-weight: 500; color: #6b7280; border-radius: 8px; cursor: pointer; transition: all 0.2s; position: relative; width: 100%; }
.nav-item:hover { background: #fff; color: #1f2937; }
.nav-item.active { background: #fff; color: #1f2937; font-weight: 600; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }
.nav-item .badge { margin-left: auto; }
.stats-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }
.stat-card { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px 16px; border: 1px solid #e5e7eb; border-radius: 12px; background: #fff; box-shadow: 0 1px 2px rgba(0,0,0,0.06); transition: box-shadow 0.2s; }
.stat-card:hover { box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
.circular-progress { position: relative; width: 80px; height: 80px; margin-bottom: 12px; }
.circular-progress svg { width: 100%; height: 100%; transform: rotate(-90deg); }
.circular-progress circle { fill: none; stroke-width: 6; stroke-linecap: round; }
.circular-progress .bg-ring { stroke: #f3f4f6; }
.circular-progress .progress-ring { transition: stroke-dashoffset 1s ease; }
.circular-content { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; }
.stat-number { font-size: 20px; font-weight: bold; color: #1f2937; }
.stat-number .percent { font-size: 12px; color: #6b7280; }
.stat-info { text-align: center; }
.stat-label { font-size: 12px; font-weight: 500; color: #6b7280; margin: 0; }
.stat-sublabel { font-size: 10px; color: #9ca3af; margin: 4px 0 0 0; }
.main-content { flex: 1; background: #fff; border: 1px solid #e5e7eb; border-radius: 12px; box-shadow: 0 1px 2px rgba(0,0,0,0.04); overflow-y: auto; }
.content-panel { padding: 32px; }
.orders-section { margin-bottom: 40px; }
.section-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 20px; }
.section-title { font-size: 18px; font-weight: 600; color: #1f2937; margin: 0; }
.section-subtitle { font-size: 14px; color: #6b7280; margin: 8px 0 0 0; }
.search-bar { margin-bottom: 20px; max-width: 400px; }
.action-icons { display: flex; gap: 4px; align-items: center; }
.action-icon { font-size: 16px; color: #6b7280; cursor: pointer; transition: color 0.2s; }
.action-icon:hover { color: #1f2937; }
.delivered-status { color: #18a058; font-weight: 500; font-size: 12px; }
</style>
