<template>
  <div class="admin-settings-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="page-title-section">
        <h1 class="page-title">系统设置</h1>
        <p class="page-subtitle">管理系统配置、邮件、物流和安全设置</p>
      </div>
    </div>

    <!-- 主布局：左侧Tab + 右侧内容 -->
    <div class="main-layout">
      <!-- 左侧Tab导航 -->
      <div class="settings-tabs">
        <div
          v-for="(tab, index) in tabs"
          :key="tab.key"
          class="tab-item"
          :class="{ 'is-active': activeTab === tab.key }"
          @click="activeTab = tab.key"
        >
          <span class="tab-icon">{{ tab.icon }}</span>
          <span class="tab-label">{{ tab.label }}</span>
        </div>
      </div>

      <!-- 右侧内容区 -->
      <div class="settings-content">
        <!-- Tab 1: 系统基础配置 -->
        <div v-if="activeTab === 'basic'" class="content-panel">
          <div class="panel-header">
            <h2>系统基础配置</h2>
            <p class="panel-desc">配置系统基本信息，保存在本地浏览器中</p>
          </div>
          
          <div class="config-form">
            <div class="form-group">
              <label>系统名称</label>
              <el-input v-model="basicConfig.systemName" placeholder="输入系统名称" />
            </div>
            
            <div class="form-group">
              <label>默认语言</label>
              <el-select v-model="basicConfig.language" placeholder="选择默认语言">
                <el-option label="中文" value="zh-CN" />
                <el-option label="English" value="en-US" />
              </el-select>
            </div>
            
            <div class="form-group">
              <label>时区设置</label>
              <el-select v-model="basicConfig.timezone" placeholder="选择时区">
                <el-option label="Asia/Shanghai (北京时间)" value="Asia/Shanghai" />
                <el-option label="Asia/Hong_Kong (香港时间)" value="Asia/Hong_Kong" />
                <el-option label="Asia/Tokyo (东京时间)" value="Asia/Tokyo" />
                <el-option label="America/New_York (纽约时间)" value="America/New_York" />
                <el-option label="America/Los_Angeles (洛杉矶时间)" value="America/Los_Angeles" />
                <el-option label="Europe/London (伦敦时间)" value="Europe/London" />
              </el-select>
            </div>
            
            <el-button type="primary" @click="saveBasicConfig">
              <el-icon><Check /></el-icon>保存配置
            </el-button>
          </div>
        </div>

        <!-- Tab 2: 邮件配置 -->
        <div v-if="activeTab === 'email'" class="content-panel">
          <div class="panel-header">
            <h2>邮件服务配置</h2>
            <p class="panel-desc">邮件相关配置在后端 .env 文件中管理</p>
          </div>
          
          <div class="config-form">
            <div class="info-card">
              <div class="info-row">
                <span class="info-label">SMTP服务器</span>
                <span class="info-value">{{ emailConfig.smtpServer || '未配置' }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">SMTP端口</span>
                <span class="info-value">{{ emailConfig.smtpPort || '未配置' }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">发件人邮箱</span>
                <span class="info-value">{{ emailConfig.senderEmail || '未配置' }}</span>
              </div>
            </div>
            
            <div class="status-section">
              <h3>邮件服务状态</h3>
              <div class="status-card" :class="healthStatus.email ? 'active' : 'inactive'">
                <div class="status-indicator">
                  <span class="status-dot" :class="healthStatus.email ? 'online' : 'offline'"></span>
                  <span class="status-text">{{ healthStatus.email ? '服务正常' : '服务异常' }}</span>
                </div>
                <el-button size="small" @click="checkHealth" :loading="healthChecking">
                  <el-icon><Refresh /></el-icon>刷新状态
                </el-button>
              </div>
            </div>
            
            <div class="hint-box">
              <el-icon><InfoFilled /></el-icon>
              <span>邮件SMTP配置请修改后端 <code>.env</code> 文件中的相关参数</span>
            </div>
          </div>
        </div>

        <!-- Tab 3: 物流配置 -->
        <div v-if="activeTab === 'logistics'" class="content-panel">
          <div class="panel-header">
            <h2>物流服务配置</h2>
            <p class="panel-desc">管理物流API连接和默认渠道设置</p>
          </div>
          
          <div class="config-form">
            <div class="status-section">
              <h3>4PX API 连接状态</h3>
              <div class="status-card" :class="healthStatus.logistics ? 'active' : 'inactive'">
                <div class="status-indicator">
                  <span class="status-dot" :class="healthStatus.logistics ? 'online' : 'offline'"></span>
                  <span class="status-text">{{ healthStatus.logistics ? 'API连接正常' : 'API连接异常' }}</span>
                </div>
                <el-button size="small" @click="checkHealth" :loading="healthChecking">
                  <el-icon><Refresh /></el-icon>检测连接
                </el-button>
              </div>
            </div>
            
            <div class="form-group">
              <label>默认物流渠道</label>
              <el-select v-model="logisticsConfig.defaultChannel" placeholder="选择默认物流渠道">
                <el-option label="4PX递四方 - 全球速递" value="4PX_EXPRESS" />
                <el-option label="4PX递四方 - 经济专线" value="4PX_ECONOMY" />
                <el-option label="4PX递四方 - 标准专线" value="4PX_STANDARD" />
              </el-select>
            </div>
            
            <el-button type="primary" @click="saveLogisticsConfig">
              <el-icon><Check /></el-icon>保存配置
            </el-button>
            
            <div class="hint-box">
              <el-icon><InfoFilled /></el-icon>
              <span>物流API密钥配置请修改后端 <code>.env</code> 文件中的 4PX 相关参数</span>
            </div>
          </div>
        </div>

        <!-- Tab 4: 发件人配置 -->
        <div v-if="activeTab === 'sender'" class="content-panel">
          <div class="panel-header">
            <h2>发件人配置</h2>
            <p class="panel-desc">管理邮件落款名列表，用于邮件撰写时选择</p>
          </div>
          
          <div class="config-form">
            <div class="sender-list">
              <div class="list-header">
                <span>落款名列表</span>
                <el-button type="primary" size="small" @click="showAddSender = true">
                  <el-icon><Plus /></el-icon>添加落款名
                </el-button>
              </div>
              
              <div class="list-items">
                <div
                  v-for="(sender, index) in senderConfig.signatures"
                  :key="index"
                  class="list-item"
                >
                  <span class="item-name">{{ sender }}</span>
                  <el-button
                    type="danger"
                    size="small"
                    text
                    @click="removeSender(index)"
                  >
                    <el-icon><Delete /></el-icon>删除
                  </el-button>
                </div>
                
                <div v-if="senderConfig.signatures.length === 0" class="empty-state">
                  <p>暂无落款名，请添加</p>
                </div>
              </div>
            </div>
            
            <!-- 添加落款名弹窗 -->
            <el-dialog v-model="showAddSender" title="添加落款名" width="400px">
              <el-input v-model="newSenderName" placeholder="输入落款名，如：Customer Service Team" />
              <template #footer>
                <el-button @click="showAddSender = false">取消</el-button>
                <el-button type="primary" @click="addSender" :disabled="!newSenderName.trim()">
                  添加
                </el-button>
              </template>
            </el-dialog>
          </div>
        </div>

        <!-- Tab 5: 安全设置 -->
        <div v-if="activeTab === 'security'" class="content-panel">
          <div class="panel-header">
            <h2>安全设置</h2>
            <p class="panel-desc">修改密码和登录安全配置</p>
          </div>
          
          <div class="config-form">
            <div class="section-block">
              <h3>修改密码</h3>
              <div class="form-group">
                <label>当前密码</label>
                <el-input v-model="passwordForm.oldPassword" type="password" placeholder="输入当前密码" show-password />
              </div>
              <div class="form-group">
                <label>新密码</label>
                <el-input v-model="passwordForm.newPassword" type="password" placeholder="输入新密码" show-password />
              </div>
              <div class="form-group">
                <label>确认新密码</label>
                <el-input v-model="passwordForm.confirmPassword" type="password" placeholder="再次输入新密码" show-password />
              </div>
              <el-button type="primary" @click="changePassword" :loading="passwordChanging">
                <el-icon><Key /></el-icon>修改密码
              </el-button>
            </div>
            
            <div class="section-block">
              <h3>登录超时设置</h3>
              <div class="form-group">
                <label>登录有效期</label>
                <el-select v-model="securityConfig.sessionTimeout" placeholder="选择登录有效期">
                  <el-option label="12 小时" value="12" />
                  <el-option label="24 小时（推荐）" value="24" />
                  <el-option label="72 小时（3天）" value="72" />
                </el-select>
              </div>
              <el-button type="primary" @click="saveSecurityConfig">
                <el-icon><Check /></el-icon>保存设置
              </el-button>
            </div>
          </div>
        </div>

        <!-- Tab 6: 关于系统 -->
        <div v-if="activeTab === 'about'" class="content-panel">
          <div class="panel-header">
            <h2>关于系统</h2>
            <p class="panel-desc">系统版本和技术栈信息</p>
          </div>
          
          <div class="config-form">
            <div class="about-card">
              <div class="about-header">
                <div class="system-logo">POD</div>
                <div class="system-info">
                  <h3>ETSY订单自动化管理系统</h3>
                  <p class="version">版本 POD V1.05</p>
                </div>
              </div>
            </div>
            
            <div class="tech-stack">
              <h3>技术栈</h3>
              <div class="tech-grid">
                <div class="tech-item">
                  <span class="tech-label">前端框架</span>
                  <span class="tech-value">Vue 3 + Vite</span>
                </div>
                <div class="tech-item">
                  <span class="tech-label">UI组件</span>
                  <span class="tech-value">Tailwind CSS + Element Plus</span>
                </div>
                <div class="tech-item">
                  <span class="tech-label">后端框架</span>
                  <span class="tech-value">Python + FastAPI</span>
                </div>
                <div class="tech-item">
                  <span class="tech-label">数据库</span>
                  <span class="tech-value">Supabase (PostgreSQL)</span>
                </div>
              </div>
            </div>
            
            <div class="status-section">
              <h3>系统状态</h3>
              <div class="status-card" :class="healthStatus.database ? 'active' : 'inactive'">
                <div class="status-indicator">
                  <span class="status-dot" :class="healthStatus.database ? 'online' : 'offline'"></span>
                  <span class="status-text">{{ healthStatus.database ? '数据库连接正常' : '数据库连接异常' }}</span>
                </div>
                <el-button size="small" @click="checkHealth" :loading="healthChecking">
                  <el-icon><Refresh /></el-icon>检测连接
                </el-button>
              </div>
            </div>
            
            <div class="developer-info">
              <h3>开发者信息</h3>
              <p>本系统为ETSY订单自动化管理解决方案，支持订单处理、效果图生成、生产文档制作和物流跟踪等核心功能。</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { Check, Refresh, Plus, Delete, Key, InfoFilled } from '@element-plus/icons-vue'
import supabase from '../../utils/supabase'
import { useAdminStore } from '../../stores/adminStore'

const adminStore = useAdminStore()

// Tab配置
const tabs = [
  { key: 'basic', label: '基础配置', icon: '⚙️' },
  { key: 'email', label: '邮件配置', icon: '📧' },
  { key: 'logistics', label: '物流配置', icon: '🚚' },
  { key: 'sender', label: '发件人配置', icon: '✍️' },
  { key: 'security', label: '安全设置', icon: '🔒' },
  { key: 'about', label: '关于系统', icon: 'ℹ️' }
]

const activeTab = ref('basic')

// 系统基础配置
const basicConfig = reactive({
  systemName: 'ETSY订单自动化管理系统',
  language: 'zh-CN',
  timezone: 'Asia/Shanghai'
})

// 邮件配置（只读展示）
const emailConfig = reactive({
  smtpServer: 'smtp.qq.com',
  smtpPort: '587',
  senderEmail: '配置于后端.env'
})

// 物流配置
const logisticsConfig = reactive({
  defaultChannel: '4PX_EXPRESS'
})

// 发件人配置
const senderConfig = reactive({
  signatures: []
})
const showAddSender = ref(false)
const newSenderName = ref('')

// 安全配置
const securityConfig = reactive({
  sessionTimeout: '24'
})

// 密码修改表单
const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})
const passwordChanging = ref(false)

// 健康状态
const healthStatus = reactive({
  email: false,
  logistics: false,
  database: false
})
const healthChecking = ref(false)

// 加载本地存储的配置
function loadLocalConfig() {
  const savedBasic = localStorage.getItem('settings_basic')
  if (savedBasic) {
    Object.assign(basicConfig, JSON.parse(savedBasic))
  }
  
  const savedLogistics = localStorage.getItem('settings_logistics')
  if (savedLogistics) {
    Object.assign(logisticsConfig, JSON.parse(savedLogistics))
  }
  
  const savedSender = localStorage.getItem('settings_sender')
  if (savedSender) {
    Object.assign(senderConfig, JSON.parse(savedSender))
  }
  
  const savedSecurity = localStorage.getItem('settings_security')
  if (savedSecurity) {
    Object.assign(securityConfig, JSON.parse(savedSecurity))
  }
}

// 保存基础配置
function saveBasicConfig() {
  localStorage.setItem('settings_basic', JSON.stringify(basicConfig))
  ElMessage.success('基础配置已保存')
}

// 保存物流配置
function saveLogisticsConfig() {
  localStorage.setItem('settings_logistics', JSON.stringify(logisticsConfig))
  ElMessage.success('物流配置已保存')
}

// 添加发件人落款名
function addSender() {
  if (!newSenderName.value.trim()) return
  senderConfig.signatures.push(newSenderName.value.trim())
  localStorage.setItem('settings_sender', JSON.stringify(senderConfig))
  newSenderName.value = ''
  showAddSender.value = false
  ElMessage.success('落款名已添加')
}

// 删除发件人落款名
function removeSender(index) {
  senderConfig.signatures.splice(index, 1)
  localStorage.setItem('settings_sender', JSON.stringify(senderConfig))
  ElMessage.success('落款名已删除')
}

// 保存安全配置
function saveSecurityConfig() {
  localStorage.setItem('settings_security', JSON.stringify(securityConfig))
  ElMessage.success('安全设置已保存')
}

// 修改密码
async function changePassword() {
  if (!passwordForm.oldPassword || !passwordForm.newPassword) {
    ElMessage.warning('请填写完整密码信息')
    return
  }
  
  if (passwordForm.newPassword !== passwordForm.confirmPassword) {
    ElMessage.error('两次输入的新密码不一致')
    return
  }
  
  if (passwordForm.newPassword.length < 6) {
    ElMessage.error('新密码长度不能少于6位')
    return
  }
  
  passwordChanging.value = true
  
  try {
    const currentUser = adminStore.currentUser
    if (!currentUser || !currentUser.id) {
      ElMessage.error('无法获取当前用户信息')
      return
    }
    
    // 更新密码到Supabase
    const { error } = await supabase
      .from('users')
      .update({ password: passwordForm.newPassword })
      .eq('id', currentUser.id)
    
    if (error) throw error
    
    ElMessage.success('密码修改成功')
    passwordForm.oldPassword = ''
    passwordForm.newPassword = ''
    passwordForm.confirmPassword = ''
  } catch (err) {
    console.error('密码修改失败:', err)
    ElMessage.error('密码修改失败: ' + err.message)
  } finally {
    passwordChanging.value = false
  }
}

// 健康检查
async function checkHealth() {
  healthChecking.value = true
  
  try {
    const apiBase = import.meta.env.VITE_API_BASE || 'http://localhost:8000'
    const response = await fetch(`${apiBase}/api/health`)
    
    if (response.ok) {
      const data = await response.json()
      healthStatus.email = data.email_service === true || data.email === true
      healthStatus.logistics = data.logistics_api === true || data.logistics === true
      healthStatus.database = data.database === true || data.status === 'healthy'
    } else {
      // 如果API不可用，尝试直接连接Supabase
      const { error } = await supabase.from('shops').select('id').limit(1)
      healthStatus.database = !error
      healthStatus.email = false
      healthStatus.logistics = false
    }
  } catch (err) {
    console.error('健康检查失败:', err)
    // 尝试直接连接Supabase检查数据库
    try {
      const { error } = await supabase.from('shops').select('id').limit(1)
      healthStatus.database = !error
    } catch {
      healthStatus.database = false
    }
    healthStatus.email = false
    healthStatus.logistics = false
  } finally {
    healthChecking.value = false
  }
}

// 初始化
onMounted(() => {
  loadLocalConfig()
  checkHealth()
})
</script>

<style scoped>
.admin-settings-page {
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

/* 主布局 */
.main-layout {
  display: flex;
  gap: 20px;
  height: calc(100vh - 160px);
  min-height: 600px;
}

/* 左侧Tab导航 */
.settings-tabs {
  width: 200px;
  background: #ffffff;
  border: 1px solid #e3e2e0;
  border-radius: 10px;
  padding: 12px;
  flex-shrink: 0;
}

.tab-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 14px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  color: #6b7280;
  transition: all 0.15s ease;
  margin-bottom: 4px;
}

.tab-item:hover {
  background: #f5f5f4;
  color: #37352f;
}

.tab-item.is-active {
  background: #eff6ff;
  color: #2563eb;
  font-weight: 500;
}

.tab-icon {
  font-size: 16px;
}

.tab-label {
  flex: 1;
}

/* 右侧内容区 */
.settings-content {
  flex: 1;
  background: #ffffff;
  border: 1px solid #e3e2e0;
  border-radius: 10px;
  overflow-y: auto;
}

.content-panel {
  padding: 24px;
}

.panel-header {
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f1f1ef;
}

.panel-header h2 {
  font-size: 18px;
  font-weight: 600;
  color: #37352f;
  margin: 0 0 4px 0;
}

.panel-desc {
  font-size: 13px;
  color: #9ca3af;
  margin: 0;
}

/* 表单样式 */
.config-form {
  max-width: 500px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: #374151;
  margin-bottom: 8px;
}

.form-group .el-input,
.form-group .el-select {
  width: 100%;
}

/* 信息卡片 */
.info-card {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 16px;
  margin-bottom: 24px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #e5e7eb;
}

.info-row:last-child {
  border-bottom: none;
}

.info-label {
  font-size: 13px;
  color: #6b7280;
}

.info-value {
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  font-family: monospace;
}

/* 状态区块 */
.status-section {
  margin-bottom: 24px;
}

.status-section h3 {
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  margin: 0 0 12px 0;
}

.status-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-radius: 10px;
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
}

.status-card.active {
  background: #ecfdf5;
  border-color: #a7f3d0;
}

.status-card.inactive {
  background: #fef2f2;
  border-color: #fecaca;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 10px;
}

.status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.status-dot.online {
  background: #10b981;
  box-shadow: 0 0 8px rgba(16, 185, 129, 0.4);
}

.status-dot.offline {
  background: #ef4444;
}

.status-text {
  font-size: 14px;
  font-weight: 500;
  color: #374151;
}

/* 提示框 */
.hint-box {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: #fefce8;
  border: 1px solid #fde047;
  border-radius: 8px;
  font-size: 13px;
  color: #854d0e;
  margin-top: 20px;
}

.hint-box code {
  background: rgba(0,0,0,0.08);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: monospace;
}

/* 发件人列表 */
.sender-list {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  overflow: hidden;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: #ffffff;
  border-bottom: 1px solid #e5e7eb;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
}

.list-items {
  padding: 8px;
  max-height: 300px;
  overflow-y: auto;
}

.list-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 12px;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  margin-bottom: 8px;
}

.list-item:last-child {
  margin-bottom: 0;
}

.item-name {
  font-size: 14px;
  color: #374151;
}

.empty-state {
  text-align: center;
  padding: 32px;
  color: #9ca3af;
}

/* 安全设置区块 */
.section-block {
  padding: 20px;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  margin-bottom: 20px;
}

.section-block h3 {
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  margin: 0 0 16px 0;
}

/* 关于系统 */
.about-card {
  background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
  border-radius: 12px;
  padding: 24px;
  color: white;
  margin-bottom: 24px;
}

.about-header {
  display: flex;
  align-items: center;
  gap: 16px;
}

.system-logo {
  width: 64px;
  height: 64px;
  background: rgba(255,255,255,0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: 700;
}

.system-info h3 {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 4px 0;
}

.system-info .version {
  font-size: 13px;
  opacity: 0.8;
  margin: 0;
}

.tech-stack {
  margin-bottom: 24px;
}

.tech-stack h3 {
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  margin: 0 0 12px 0;
}

.tech-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.tech-item {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 12px;
}

.tech-label {
  display: block;
  font-size: 12px;
  color: #6b7280;
  margin-bottom: 4px;
}

.tech-value {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
}

.developer-info {
  padding: 16px;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
}

.developer-info h3 {
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  margin: 0 0 8px 0;
}

.developer-info p {
  font-size: 13px;
  color: #6b7280;
  margin: 0;
  line-height: 1.6;
}

/* 响应式 */
@media (max-width: 768px) {
  .main-layout {
    flex-direction: column;
    height: auto;
  }
  
  .settings-tabs {
    width: 100%;
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
  }
  
  .tab-item {
    flex: 1;
    min-width: 120px;
    justify-content: center;
  }
  
  .tech-grid {
    grid-template-columns: 1fr;
  }
}
</style>
