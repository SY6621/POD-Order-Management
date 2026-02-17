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
          <button :class="['nav-item', { active: currentTab === 'dashboard' }]" @click="switchTab('dashboard')">
            <el-icon><Grid /></el-icon>
            <span>仪表盘总览</span>
          </button>
          <button :class="['nav-item', { active: currentTab === 'pending' }]" @click="switchTab('pending')">
            <el-icon><Clock /></el-icon>
            <span>待确认订单</span>
            <el-tag v-if="stats.pending > 0" size="small" class="badge">{{ stats.pending }}</el-tag>
          </button>
          <button :class="['nav-item', { active: currentTab === 'producing' }]" @click="switchTab('producing')">
            <el-icon><Setting /></el-icon>
            <span>生产中订单</span>
            <el-tag v-if="stats.producing > 0" size="small" type="primary" class="badge">{{ stats.producing }}</el-tag>
          </button>
          <button :class="['nav-item', { active: currentTab === 'completed' }]" @click="switchTab('completed')">
            <el-icon><CircleCheck /></el-icon>
            <span>已完成订单</span>
          </button>
          <button :class="['nav-item', { active: currentTab === 'templates' }]" @click="switchTab('templates')">
            <el-icon><Message /></el-icon>
            <span>邮件模板</span>
          </button>
        </nav>

        <!-- 统计圆形仪表盘 -->
        <div class="stats-grid">
          <div class="stat-card">
            <div class="circular-progress">
              <svg><circle class="bg-ring" cx="40" cy="40" r="35"></circle><circle class="progress-ring" cx="40" cy="40" r="35" :style="getProgressStyle(100, '#2080f0')"></circle></svg>
              <div class="circular-content"><span class="stat-number">{{ stats.total }}</span></div>
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
        <!-- 仪表盘总览 -->
        <div v-show="currentTab === 'dashboard'" class="content-panel">
          <!-- 最近订单/待确认订单 -->
          <section class="orders-section">
            <div class="section-header">
              <div>
                <h2 class="section-title">最近订单 / 待确认订单</h2>
                <p class="section-subtitle">最新的生产订单，需要生成效果图或发送确认邮件。</p>
              </div>
            </div>
            <div class="search-bar">
              <el-input v-model="searchText" placeholder="搜索订单号、客户名称或产品..." prefix-icon="Search" clearable />
            </div>
            <el-table :data="recentOrders" stripe style="width: 100%">
              <el-table-column prop="orderId" label="订单ID" width="120" />
              <el-table-column prop="customerName" label="客户名称" width="120" />
              <el-table-column prop="product" label="产品" width="90" />
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
              <el-table-column prop="quantity" label="数量" width="70" />
              <el-table-column label="状态" width="90">
                <template #default="scope">
                  <el-tag :type="scope.row.statusType" size="small">{{ scope.row.status }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="createDate" label="创建日期" width="100" />
              <el-table-column label="操作" width="120" fixed="right">
                <template #default="scope">
                  <el-dropdown trigger="click">
                    <el-button type="primary" size="small">
                      操作 <el-icon class="el-icon--right"><ArrowDown /></el-icon>
                    </el-button>
                    <template #dropdown>
                      <el-dropdown-menu>
                        <el-dropdown-item>创建订单</el-dropdown-item>
                        <el-dropdown-item>更多订单</el-dropdown-item>
                      </el-dropdown-menu>
                    </template>
                  </el-dropdown>
                </template>
              </el-table-column>
            </el-table>
          </section>

          <!-- 生产中订单 -->
          <section class="orders-section">
            <div class="section-header">
              <div>
                <h2 class="section-title">生产中订单</h2>
                <p class="section-subtitle">订单已进入生产流程，监控生产进度与物流安排。</p>
              </div>
            </div>
            <el-table :data="producingOrders" stripe style="width: 100%">
              <el-table-column prop="customerName" label="客户名称" width="120" />
              <el-table-column prop="product" label="产品" width="90" />
              <el-table-column label="生产表单" width="110">
                <template #default="scope">
                  <el-button v-if="!scope.row.hasForm" size="small" plain><el-icon><Document /></el-icon> 生成表单</el-button>
                  <el-link v-else type="primary" :underline="false"><el-icon><Document /></el-icon> {{ scope.row.formFile }}</el-link>
                </template>
              </el-table-column>
              <el-table-column label="进度" width="150">
                <template #default="scope">
                  <div class="progress-cell">
                    <el-progress :percentage="scope.row.progress" :stroke-width="6" />
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop="quantity" label="数量" width="70" />
              <el-table-column label="状态" width="90">
                <template #default="scope">
                  <el-tag :type="scope.row.statusType" size="small">{{ scope.row.status }}</el-tag>
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
                  <el-button size="small" plain>当日下单</el-button>
                </template>
              </el-table-column>
              <el-table-column prop="createDate" label="创建日期" width="100" />
              <el-table-column label="操作" width="120" fixed="right">
                <template #default="scope">
                  <el-dropdown trigger="click">
                    <el-button size="small">
                      操作 <el-icon class="el-icon--right"><ArrowDown /></el-icon>
                    </el-button>
                    <template #dropdown>
                      <el-dropdown-menu>
                        <el-dropdown-item>物流取货</el-dropdown-item>
                        <el-dropdown-item>更多订单</el-dropdown-item>
                      </el-dropdown-menu>
                    </template>
                  </el-dropdown>
                </template>
              </el-table-column>
            </el-table>
          </section>

          <!-- 已完成订单 -->
          <section class="orders-section">
            <div class="section-header">
              <div>
                <h2 class="section-title">已完成订单</h2>
                <p class="section-subtitle">发货日起 30 天内订单；集成客户订单信息、效果图、往来邮件。</p>
              </div>
            </div>
            <el-table :data="completedOrders" stripe style="width: 100%">
              <el-table-column prop="orderId" label="订单ID" width="120" />
              <el-table-column prop="customerName" label="客户名称" width="120" />
              <el-table-column prop="product" label="产品" width="90" />
              <el-table-column prop="quantity" label="数量" width="70" />
              <el-table-column prop="address" label="国家地址" width="130" />
              <el-table-column prop="shipDate" label="发货日期" width="100" />
              <el-table-column prop="receiveDate" label="收货日期" width="100" />
              <el-table-column label="物流送达" width="90">
                <template #default="scope">
                  <span class="delivered-status">{{ scope.row.deliveryStatus }}</span>
                </template>
              </el-table-column>
              <el-table-column label="追评邮件" width="90">
                <template #default="scope">
                  <el-button size="small" plain><el-icon><Message /></el-icon> 查看</el-button>
                </template>
              </el-table-column>
              <el-table-column label="处理详情" width="120" fixed="right">
                <template #default="scope">
                  <el-dropdown trigger="click">
                    <el-button size="small">
                      详情 <el-icon class="el-icon--right"><ArrowDown /></el-icon>
                    </el-button>
                    <template #dropdown>
                      <el-dropdown-menu>
                        <el-dropdown-item>查看详情</el-dropdown-item>
                        <el-dropdown-item>更多订单</el-dropdown-item>
                      </el-dropdown-menu>
                    </template>
                  </el-dropdown>
                </template>
              </el-table-column>
            </el-table>
          </section>
        </div>

        <!-- 待确认订单 -->
        <div v-show="currentTab === 'pending'" class="content-panel"><h2>待确认订单</h2><p>处理新订单，确认客户需求。</p></div>

        <!-- 生产中订单 -->
        <div v-show="currentTab === 'producing'" class="content-panel"><h2>生产中订单</h2><p>查看正在生产线上的订单。</p></div>

        <!-- 已完成订单 -->
        <div v-show="currentTab === 'completed'" class="content-panel"><h2>已完成订单</h2><p>历史订单记录与详情。</p></div>

        <!-- 邮件模板 -->
        <div v-show="currentTab === 'templates'" class="content-panel"><h2>邮件模板</h2><p>管理客户沟通的自动化邮件模板。</p></div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useOrderStore } from '../../stores/orderStore'
import { Box, Bell, Grid, Clock, Setting, CircleCheck, Message, Picture, View, Download, Document, InfoFilled, ArrowDown } from '@element-plus/icons-vue'
import dayjs from 'dayjs'

const orderStore = useOrderStore()
const stats = ref({ total: 128, pending: 41, producing: 23, completed: 64 })
const searchText = ref('')
const currentTab = ref('dashboard')

// 最近订单数据（模拟）
const recentOrders = ref([
  { orderId: '#PO-2602-001', customerName: 'Maura McHale', product: 'B-E01A', hasDesign: false, emailSent: false, quantity: 200, status: '新订单', statusType: 'info', createDate: '2026-02-03' },
  { orderId: '#PO-2602-002', customerName: 'Kim Alison', product: 'B-G01B', hasDesign: true, emailSent: true, quantity: 1, status: '待确认', statusType: 'warning', createDate: '2026-02-01' }
])

// 生产中订单数据（模拟）
const producingOrders = ref([
  { customerName: 'Maura McHale', product: 'B-E01A', hasForm: false, progress: 60, quantity: 200, status: '生产中', statusType: 'primary', createDate: '2026-02-01' },
  { customerName: 'Laura Alcarria', product: 'B-C01B', hasForm: true, formFile: '38723.pdf', progress: 100, quantity: 2, status: '已完成', statusType: 'success', createDate: '2026-01-10' }
])

// 已完成订单数据（模拟）
const completedOrders = ref([
  { orderId: '#PO-2601-088', customerName: 'Maura McHale', product: 'B-E01A', quantity: 1, address: 'US, California', shipDate: '2026-01-25', receiveDate: '2026-02-01', deliveryStatus: '已送达' },
  { orderId: '#PO-2601-089', customerName: 'Laura Alcarria', product: 'B-C01B', quantity: 2, address: 'UK, London', shipDate: '2026-01-20', receiveDate: '2026-01-29', deliveryStatus: '已送达' }
])

const pendingPercent = computed(() => stats.value.total === 0 ? 0 : Math.round((stats.value.pending / stats.value.total) * 100))
const producingPercent = computed(() => stats.value.total === 0 ? 0 : Math.round((stats.value.producing / stats.value.total) * 100))
const completedPercent = computed(() => stats.value.total === 0 ? 0 : Math.round((stats.value.completed / stats.value.total) * 100))

const getProgressStyle = (percent, color) => {
  const circumference = 220
  const offset = circumference - (percent / 100) * circumference
  return { stroke: color, strokeDasharray: circumference, strokeDashoffset: offset }
}

const switchTab = (tab) => { currentTab.value = tab }

const loadData = async () => {
  try {
    // 尝试从store获取真实数据
    const storeStats = await orderStore.getOrderStats()
    if (storeStats && storeStats.total > 0) {
      stats.value = storeStats
    }
    console.log('✅ Dashboard 数据加载成功')
  } catch (error) {
    console.log('ℹ️ 使用模拟数据')
  }
}

onMounted(() => { loadData() })
</script>

<style scoped>
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
.progress-cell { padding-right: 10px; }
.delivered-status { color: #18a058; font-weight: 500; font-size: 12px; }
</style>
