<template>
  <div class="admin-users-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="page-title-section">
        <h1 class="page-title">子账号与店铺管理</h1>
        <p class="page-subtitle">管理运营子账号及其负责的店铺，配置客服外链</p>
      </div>
      <el-button type="primary" @click="showCreateModal = true">
        <el-icon><Plus /></el-icon>创建运营账号
      </el-button>
    </div>

    <!-- 运营Tab页 - 只显示A运营 -->
    <div class="operator-tabs">
      <div 
        class="tab-item is-active"
      >
        <span class="tab-name">A运营</span>
        <span class="tab-count">{{ displayShops.length }}</span>
      </div>
    </div>

    <!-- 左右分栏布局 -->
    <div class="main-layout">
      <!-- 左侧：店铺列表 -->
      <div class="shop-list-panel">
        <div class="panel-header">
          <span class="panel-title">店铺列表</span>
          <span class="panel-count">{{ displayShops.length }} 间</span>
        </div>
        <div class="shop-list">
          <!-- 按3个一组分组显示 -->
          <div 
            v-for="(group, groupIndex) in groupedShops" 
            :key="groupIndex"
            class="shop-group"
          >
            <div 
              v-for="shop in group" 
              :key="shop.id"
              class="shop-list-item"
              :class="{ 'is-active': selectedShop?.id === shop.id }"
              @click="selectShop(shop)"
            >
              <div class="item-content">
                <span class="item-flag">{{ getCountryFlag(shop.code) }}</span>
                <span class="item-code">{{ shop.code?.toUpperCase() }}</span>
                <span class="item-name">{{ shop.name }}</span>
                <span 
                  class="item-status"
                  :class="shop.service_link_enabled ? 'enabled' : 'disabled'"
                >
                  {{ shop.service_link_enabled ? '已启用' : '未生成' }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧：店铺详情 -->
      <div class="shop-detail-panel">
        <div v-if="selectedShop" class="detail-content">
          <!-- 详情头部 -->
          <div class="detail-header">
            <div class="detail-icon" :style="{ backgroundColor: getShopColor(selectedShop.code) }">
              <span>{{ getCountryFlag(selectedShop.code) }}</span>
            </div>
            <div class="detail-title">
              <h2>{{ selectedShop.name }}</h2>
              <div class="detail-meta">
                <el-tag :type="getRegionTagType(selectedShop.region)">{{ selectedShop.region }}</el-tag>
                <span class="detail-code">{{ selectedShop.code?.toUpperCase() }}</span>
              </div>
            </div>
          </div>

          <!-- 状态卡片 -->
          <div class="status-cards">
            <div class="status-card" :class="selectedShop.service_link_enabled ? 'active' : 'inactive'">
              <div class="status-icon">
                <el-icon v-if="selectedShop.service_link_enabled"><CircleCheck /></el-icon>
                <el-icon v-else><CircleClose /></el-icon>
              </div>
              <div class="status-info">
                <span class="status-label">外链状态</span>
                <span class="status-value">{{ selectedShop.service_link_enabled ? '已启用' : '未生成' }}</span>
              </div>
            </div>
            <div class="status-card">
              <div class="status-icon password">
                <el-icon><Lock /></el-icon>
              </div>
              <div class="status-info">
                <span class="status-label">访问密码</span>
                <span class="status-value">{{ selectedShop.password || '未设置' }}</span>
              </div>
            </div>
          </div>

          <!-- 客服外链操作区 -->
          <div class="link-section">
            <h3>📧 沟通链接 <span class="link-hint">（仅发邮件、收集反馈）</span></h3>
            <div v-if="selectedShop.service_link_enabled && selectedShop.service_token" class="link-box">
              <a 
                :href="getFullServiceLinkRaw(selectedShop)" 
                target="_blank" 
                class="link-url clickable"
                title="点击打开链接"
              >
                <code>{{ getFullServiceLink(selectedShop) }}</code>
                <el-icon class="link-open-icon"><TopRight /></el-icon>
              </a>
              <div class="link-actions">
                <el-button type="success" size="small" @click="openServiceLink(selectedShop)">
                  <el-icon><TopRight /></el-icon>打开
                </el-button>
                <el-button type="primary" size="small" @click="copyServiceLink(selectedShop)">
                  <el-icon><DocumentCopy /></el-icon>复制
                </el-button>
                <el-button size="small" @click="refreshServiceToken(selectedShop)">
                  <el-icon><Refresh /></el-icon>刷新
                </el-button>
                <el-button 
                  size="small"
                  :type="selectedShop.service_link_enabled ? 'danger' : 'success'"
                  @click="toggleServiceLink(selectedShop)"
                >
                  {{ selectedShop.service_link_enabled ? '禁用' : '启用' }}
                </el-button>
              </div>
            </div>
            <div v-else class="link-box empty">
              <el-empty description="暂无沟通链接" :image-size="60">
                <el-button type="primary" size="small" @click="generateServiceToken(selectedShop)">
                  <el-icon><Link /></el-icon>生成沟通链接
                </el-button>
              </el-empty>
            </div>
          </div>

          <!-- 设计链接操作区 -->
          <div class="link-section design-link">
            <h3>🎨 设计链接 <span class="link-hint">（可修改设计、生成效果图）</span></h3>
            <div v-if="selectedShop.design_link_enabled && selectedShop.design_token" class="link-box">
              <a 
                :href="getFullDesignLinkRaw(selectedShop)" 
                target="_blank" 
                class="link-url design clickable"
                title="点击打开链接"
              >
                <code>{{ getFullDesignLink(selectedShop) }}</code>
                <el-icon class="link-open-icon"><TopRight /></el-icon>
              </a>
              <div class="link-actions">
                <el-button type="success" size="small" @click="openDesignLink(selectedShop)">
                  <el-icon><TopRight /></el-icon>打开
                </el-button>
                <el-button type="primary" size="small" @click="copyDesignLink(selectedShop)">
                  <el-icon><DocumentCopy /></el-icon>复制
                </el-button>
                <el-button size="small" @click="refreshDesignToken(selectedShop)">
                  <el-icon><Refresh /></el-icon>刷新
                </el-button>
                <el-button 
                  size="small"
                  :type="selectedShop.design_link_enabled ? 'danger' : 'success'"
                  @click="toggleDesignLink(selectedShop)"
                >
                  {{ selectedShop.design_link_enabled ? '禁用' : '启用' }}
                </el-button>
              </div>
            </div>
            <div v-else class="link-box empty">
              <el-empty description="暂无设计链接" :image-size="60">
                <el-button type="warning" size="small" @click="generateDesignToken(selectedShop)">
                  <el-icon><Edit /></el-icon>生成设计链接
                </el-button>
              </el-empty>
            </div>
          </div>

          <!-- 时间信息 -->
          <div class="time-section" v-if="selectedShop.updated_at">
            <el-icon><Clock /></el-icon>
            <span>最后更新：{{ formatTime(selectedShop.updated_at) }}</span>
          </div>
        </div>

        <!-- 空状态 -->
        <div v-else class="detail-empty">
          <el-empty description="请选择左侧店铺查看详情" :image-size="120" />
        </div>
      </div>
    </div>

    <!-- 创建运营账号弹窗 -->
    <el-dialog v-model="showCreateModal" title="创建运营账号" width="480px" destroy-on-close>
      <el-form :model="newUser" label-position="top">
        <el-form-item label="用户名"><el-input v-model="newUser.username" placeholder="输入用户名" /></el-form-item>
        <el-form-item label="显示名称"><el-input v-model="newUser.display_name" placeholder="输入显示名称" /></el-form-item>
        <el-form-item label="邮箱"><el-input v-model="newUser.email" placeholder="输入邮箱" /></el-form-item>
        <el-form-item label="初始密码"><el-input v-model="newUser.password" type="password" placeholder="输入初始密码" show-password /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateModal = false">取消</el-button>
        <el-button type="primary" @click="createSubAccount" :disabled="!newUser.username || !newUser.password">创建</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, CircleCheck, CircleClose, DocumentCopy, Link, Refresh, Clock, Lock, Edit, TopRight } from '@element-plus/icons-vue'

// 数据
const subAccounts = ref([])
const allShops = ref([])
const activeTab = ref('')
const selectedShop = ref(null)

// 弹窗
const showCreateModal = ref(false)
const newUser = ref({ username: '', display_name: '', email: '', password: '' })

// 显示店铺
const displayShops = computed(() => {
  if (activeTab.value === 'all') return allShops.value
  const user = subAccounts.value.find(u => u.id === activeTab.value)
  return user?.shops || []
})

// 按3个一组分组
const groupedShops = computed(() => {
  const shops = displayShops.value
  const groups = []
  for (let i = 0; i < shops.length; i += 3) {
    groups.push(shops.slice(i, i + 3))
  }
  return groups
})

// 地区颜色
const regionColors = {
  'North America': '#3b82f6', 'Europe': '#8b5cf6', 'Asia': '#f59e0b',
  'Oceania': '#10b981', 'South America': '#ef4444', 'Africa': '#f97316'
}
const regionTagTypes = {
  'North America': 'primary', 'Europe': 'success', 'Asia': 'warning',
  'Oceania': 'success', 'South America': 'danger', 'Africa': 'warning'
}
const countryFlags = {
  'us': '🇺🇸', 'ca': '🇨🇦', 'mx': '🇲🇽', 'uk': '🇬🇧', 'de': '🇩🇪', 'fr': '🇫🇷',
  'it': '🇮🇹', 'es': '🇪🇸', 'nl': '🇳🇱', 'pl': '🇵🇱', 'se': '🇸🇪', 'ch': '🇨🇭',
  'at': '🇦🇹', 'be': '🇧🇪', 'dk': '🇩🇰', 'no': '🇳🇴', 'fi': '🇫🇮', 'ie': '🇮🇪',
  'pt': '🇵🇹', 'tr': '🇹🇷', 'asia': '🇨🇳', 'jp': '🇯🇵', 'kr': '🇰🇷', 'sg': '🇸🇬',
  'in': '🇮🇳', 'ae': '🇦🇪', 'sa': '🇸🇦', 'au': '🇦🇺', 'br': '🇧🇷', 'default': '🏪'
}

function getRegionColor(region) { return regionColors[region] || '#6b7280' }
function getRegionTagType(region) { return regionTagTypes[region] || 'info' }
function getCountryFlag(code) { return countryFlags[code?.toLowerCase()] || countryFlags.default }
function getShopColor(code) {
  const colors = ['#dbeafe', '#fce7f3', '#d1fae5', '#fef3c7', '#e0e7ff']
  return colors[code?.charCodeAt(0) % colors.length] || colors[0]
}
function formatTime(timeStr) {
  if (!timeStr) return '--'
  const date = new Date(timeStr)
  return `${date.getMonth() + 1}/${date.getDate()} ${date.getHours()}:${date.getMinutes().toString().padStart(2, '0')}`
}

// 沟通链接相关
function getFullServiceLink(shop) {
  // 显示截断版本
  return `${window.location.origin}/service/${shop.code}?token=${shop.service_token?.slice(0, 12)}...`
}
function getFullServiceLinkRaw(shop) {
  // 返回完整链接用于点击
  return `${window.location.origin}/service/${shop.code}?token=${shop.service_token}`
}
function copyServiceLink(shop) {
  const link = `${window.location.origin}/service/${shop.code}?token=${shop.service_token}`
  navigator.clipboard.writeText(link).then(() => ElMessage.success('沟通链接已复制'))
}
function openServiceLink(shop) {
  if (!shop.service_token) return ElMessage.warning('请先生成沟通链接')
  window.open(`${window.location.origin}/service/${shop.code}?token=${shop.service_token}`, '_blank')
}
function openDesignLink(shop) {
  if (!shop.design_token) return ElMessage.warning('请先生成设计链接')
  window.open(`${window.location.origin}/design/${shop.code}?token=${shop.design_token}`, '_blank')
}
async function generateServiceToken(shop) {
  shop.service_token = Math.random().toString(36).substring(2, 34)
  shop.service_link_enabled = true
  ElMessage.success('沟通链接已生成')
}
async function toggleServiceLink(shop) {
  shop.service_link_enabled = !shop.service_link_enabled
  ElMessage.success(shop.service_link_enabled ? '沟通链接已启用' : '沟通链接已禁用')
}
async function refreshServiceToken(shop) {
  shop.service_token = Math.random().toString(36).substring(2, 34)
  ElMessage.success('沟通链接Token已刷新')
}

// 设计链接相关
function getFullDesignLink(shop) {
  // 显示截断版本
  return `${window.location.origin}/design/${shop.code}?token=${shop.design_token?.slice(0, 12)}...`
}
function getFullDesignLinkRaw(shop) {
  // 返回完整链接用于点击
  return `${window.location.origin}/design/${shop.code}?token=${shop.design_token}`
}
function copyDesignLink(shop) {
  const link = `${window.location.origin}/design/${shop.code}?token=${shop.design_token}`
  navigator.clipboard.writeText(link).then(() => ElMessage.success('设计链接已复制'))
}
function openDesignPortal(shop) {
  if (!shop.design_token) return ElMessage.warning('请先生成设计链接')
  window.open(`${window.location.origin}/design/${shop.code}?token=${shop.design_token}`, '_blank')
}
async function generateDesignToken(shop) {
  shop.design_token = Math.random().toString(36).substring(2, 34)
  shop.design_link_enabled = true
  ElMessage.success('设计链接已生成')
}
async function toggleDesignLink(shop) {
  shop.design_link_enabled = !shop.design_link_enabled
  ElMessage.success(shop.design_link_enabled ? '设计链接已启用' : '设计链接已禁用')
}
async function refreshDesignToken(shop) {
  shop.design_token = Math.random().toString(36).substring(2, 34)
  ElMessage.success('设计链接Token已刷新')
}

// 切换运营
function switchOperator(userId) {
  activeTab.value = userId
  selectedShop.value = displayShops.value[0] || null
}

// 选择店铺
function selectShop(shop) {
  selectedShop.value = shop
}
function createSubAccount() {
  const newId = Date.now().toString()
  subAccounts.value.unshift({
    id: newId, username: newUser.value.username,
    display_name: newUser.value.display_name || newUser.value.username,
    email: newUser.value.email, status: 'active', shops: []
  })
  activeTab.value = newId
  showCreateModal.value = false
  newUser.value = { username: '', display_name: '', email: '', password: '' }
  ElMessage.success('运营账号创建成功')
}

// 初始化数据
onMounted(() => {
  // 模拟数据 - 只保留一个店铺（美国店铺）
  subAccounts.value = [
    { id: '1', username: 'operator_a', display_name: 'A运营', email: 'a@example.com', status: 'active',
      shops: [
        { id: '1', name: '美国店铺', code: 'us', region: 'North America', password: 'US2025', status: 'active', service_token: 'abc123xyz789', service_link_enabled: true, design_token: 'dsg_us_001', design_link_enabled: true, updated_at: '2025-03-22T14:30:00Z' }
      ]
    }
  ]
  allShops.value = subAccounts.value.flatMap(u => u.shops)
  activeTab.value = '1'
  selectedShop.value = subAccounts.value[0].shops[0]
})
</script>

<style scoped>
.admin-users-page {
  padding: 24px 32px;
  background-color: #fbfbfa;
  min-height: 100vh;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #37352f;
  margin: 0;
}

.page-subtitle {
  font-size: 14px;
  color: #6b7280;
  margin: 4px 0 0 0;
}

/* Tab */
.operator-tabs {
  display: flex;
  gap: 4px;
  padding: 4px;
  background: #f1f1ef;
  border-radius: 8px;
  margin-bottom: 20px;
}

.tab-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  color: #6b7280;
  transition: all 0.15s ease;
}

.tab-item:hover {
  background: rgba(255, 255, 255, 0.5);
  color: #37352f;
}

.tab-item.is-active {
  background: #ffffff;
  color: #37352f;
  font-weight: 500;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.06);
}

.tab-count {
  font-size: 12px;
  padding: 2px 6px;
  background: #e3e2e0;
  border-radius: 10px;
}

.tab-item.is-active .tab-count {
  background: #3b82f6;
  color: white;
}

/* 主布局 - 左右分栏 */
.main-layout {
  display: flex;
  gap: 20px;
  height: calc(100vh - 200px);
}

/* 左侧面板 - Notion 简洁风格 */
.shop-list-panel {
  width: 280px;
  background: #ffffff;
  border: 1px solid #e3e2e0;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid #f1f1ef;
}

.panel-title {
  font-size: 14px;
  font-weight: 500;
  color: #37352f;
}

.panel-count {
  font-size: 12px;
  color: #9ca3af;
}

.shop-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px 12px;
}

/* 店铺组 - 每3个一组 */
.shop-group {
  margin-bottom: 16px;
}

.shop-group:last-child {
  margin-bottom: 0;
}

.shop-list-item {
  display: flex;
  align-items: center;
  padding: 8px 10px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.12s ease;
  margin-bottom: 4px;
  border: 1px solid #e5e7eb;
  background: #ffffff;
}

.shop-list-item:hover {
  border-color: #d1d5db;
  background: #f9fafb;
}

.shop-list-item.is-active {
  border-color: #3b82f6;
  background: #eff6ff;
}

/* 简化的列表项内容 */
.item-content {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 8px;
}

.item-flag {
  font-size: 14px;
  width: 20px;
  text-align: center;
}

.item-code {
  font-size: 11px;
  font-weight: 600;
  color: #9ca3af;
  width: 24px;
  font-family: monospace;
}

.item-name {
  flex: 1;
  font-size: 13px;
  color: #37352f;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.item-status {
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 10px;
  font-weight: 500;
}

.item-status.enabled {
  background: #d1fae5;
  color: #059669;
}

.item-status.disabled {
  background: #f3f4f6;
  color: #9ca3af;
}

/* 右侧面板 */
.shop-detail-panel {
  flex: 1;
  background: #ffffff;
  border: 1px solid #e3e2e0;
  border-radius: 10px;
  padding: 24px;
  overflow-y: auto;
}

.detail-content {
  max-width: 600px;
}

.detail-header {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px solid #f1f1ef;
}

.detail-icon {
  width: 64px;
  height: 64px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
}

.detail-title h2 {
  font-size: 22px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 8px 0;
}

.detail-meta {
  display: flex;
  align-items: center;
  gap: 12px;
}

.detail-code {
  font-family: monospace;
  font-size: 14px;
  color: #6b7280;
  font-weight: 500;
}

/* 状态卡片 */
.status-cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.status-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border-radius: 10px;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
}

.status-card.active {
  background: #ecfdf5;
  border-color: #a7f3d0;
}

.status-card.inactive {
  background: #f3f4f6;
  border-color: #d1d5db;
}

.status-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  background: #ffffff;
  color: #10b981;
}

.status-card.inactive .status-icon {
  color: #9ca3af;
}

.status-icon.password {
  color: #f59e0b;
}

.status-info {
  display: flex;
  flex-direction: column;
}

.status-label {
  font-size: 12px;
  color: #6b7280;
  margin-bottom: 2px;
}

.status-value {
  font-size: 15px;
  font-weight: 600;
  color: #1f2937;
}

/* 链接区域 */
.link-section {
  margin-bottom: 20px;
}

.link-section h3 {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
  margin: 0 0 10px 0;
  display: flex;
  align-items: center;
  gap: 6px;
}

.link-hint {
  font-size: 12px;
  font-weight: 400;
  color: #9ca3af;
}

.link-box {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 14px;
}

.link-box.empty {
  padding: 24px;
}

.link-url {
  background: #1f2937;
  border-radius: 8px;
  padding: 10px 14px;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  text-decoration: none;
  transition: all 0.2s ease;
}

.link-url.clickable:hover {
  background: #374151;
  cursor: pointer;
}

.link-url code {
  color: #10b981;
  font-family: 'SF Mono', Monaco, monospace;
  font-size: 12px;
  word-break: break-all;
  flex: 1;
}

.link-open-icon {
  color: #10b981;
  font-size: 14px;
  margin-left: 8px;
  opacity: 0.7;
}

.link-url.clickable:hover .link-open-icon {
  opacity: 1;
}

/* 设计链接区分样式 */
.link-section.design-link .link-box {
  background: #fefce8;
  border-color: #fde047;
}

.link-section.design-link .link-url {
  background: #78350f;
}

.link-section.design-link .link-url.design code {
  color: #fde047;
}

.link-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

/* 时间信息 */
.time-section {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: #f0f9ff;
  border: 1px solid #dbeafe;
  border-radius: 8px;
  font-size: 13px;
  color: #3b82f6;
}

/* 空状态 */
.detail-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

/* 响应式 */
@media (max-width: 1024px) {
  .main-layout {
    flex-direction: column;
    height: auto;
  }
  .shop-list-panel {
    width: 100%;
    max-height: 400px;
  }
}
</style>