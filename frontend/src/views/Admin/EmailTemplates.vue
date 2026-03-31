<template>
  <div class="h-full overflow-hidden bg-slate-50 p-4 flex flex-col">
    <!-- 页面标题 -->
    <div class="mb-4 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-slate-800">邮件模板管理</h1>
        <p class="text-sm text-slate-500 mt-1">管理和编辑所有邮件模板内容</p>
      </div>
      <div class="flex items-center gap-2">
        <span v-if="hasUnsavedChanges" class="text-sm text-amber-600 flex items-center gap-1">
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 8v4"/><path d="M12 16h.01"/></svg>
          有未保存的更改
        </span>
        <button
          @click="createNewTemplate"
          class="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg text-sm font-medium flex items-center gap-2 transition-colors"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 5v14"/><path d="M5 12h14"/></svg>
          新建模板
        </button>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="flex-1 flex items-center justify-center">
      <div class="text-center">
        <svg class="animate-spin h-8 w-8 mx-auto mb-3 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <p class="text-slate-500">加载模板数据...</p>
      </div>
    </div>

    <!-- 主体内容 -->
    <div v-else class="flex-1 flex gap-4 min-h-0">
      <!-- 左侧：分类导航 -->
      <div class="w-[200px] bg-gray-800 rounded-xl overflow-hidden flex flex-col">
        <div class="p-3 border-b border-gray-700">
          <h3 class="text-gray-300 text-xs font-medium">模板分类</h3>
        </div>
        <div class="flex-1 overflow-y-auto">
          <div
            v-for="category in categories"
            :key="category.id"
            class="border-b border-gray-700/50 last:border-0"
          >
            <button
              @click="selectCategory(category.id)"
              :class="[
                'w-full px-4 py-3 text-left text-sm flex items-center gap-2 transition-colors',
                activeCategory === category.id
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-300 hover:bg-gray-700'
              ]"
            >
              <span>{{ category.icon }}</span>
              <span>{{ category.name }}</span>
              <span class="ml-auto text-xs opacity-60">{{ getCategoryTemplateCount(category.id) }}</span>
            </button>
            <!-- 选中分类的模板列表 -->
            <div v-if="activeCategory === category.id" class="bg-gray-900/50 px-2 py-2">
              <button
                v-for="template in getCategoryTemplates(category.id)"
                :key="template.id"
                @click="selectTemplate(template)"
                :class="[
                  'w-full px-3 py-2 text-left text-xs rounded transition-colors mb-1 last:mb-0 flex items-center gap-2',
                  selectedTemplate?.id === template.id
                    ? 'bg-blue-500/30 text-blue-200'
                    : 'text-gray-400 hover:bg-gray-700 hover:text-gray-200'
                ]"
              >
                <span v-if="template.icon">{{ template.icon }}</span>
                <span class="flex-1 truncate">{{ template.name }}</span>
                <span v-if="!template.is_active" class="w-2 h-2 rounded-full bg-gray-500" title="已禁用"></span>
              </button>
              <div v-if="getCategoryTemplates(category.id).length === 0" class="px-3 py-2 text-xs text-gray-500">
                暂无模板
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 中间：编辑区 -->
      <div class="flex-1 bg-white rounded-xl shadow-sm border border-slate-200 flex flex-col overflow-hidden">
        <!-- 编辑区标题栏 -->
        <div class="px-4 py-3 border-b border-slate-200 flex items-center justify-between bg-slate-50">
          <div class="flex items-center gap-2">
            <span v-if="selectedTemplate?.icon" class="text-lg">{{ selectedTemplate.icon }}</span>
            <h3 class="font-bold text-slate-800">{{ selectedTemplate?.name || '请选择模板' }}</h3>
            <span v-if="selectedTemplate" class="text-xs px-2 py-0.5 rounded-full" :class="selectedTemplate.is_active ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'">
              {{ selectedTemplate.is_active ? '已启用' : '已禁用' }}
            </span>
          </div>
          <div v-if="selectedTemplate" class="flex items-center gap-2">
            <button
              @click="toggleTemplateActive"
              :class="[
                'px-3 py-1.5 text-sm rounded transition-colors',
                selectedTemplate.is_active
                  ? 'bg-amber-100 hover:bg-amber-200 text-amber-700'
                  : 'bg-green-100 hover:bg-green-200 text-green-700'
              ]"
            >
              {{ selectedTemplate.is_active ? '禁用' : '启用' }}
            </button>
            <button
              @click="deleteTemplate"
              class="px-3 py-1.5 bg-red-100 hover:bg-red-200 text-red-600 text-sm rounded transition-colors"
            >
              删除
            </button>
          </div>
        </div>

        <!-- 编辑区内容 -->
        <div v-if="selectedTemplate" class="flex-1 overflow-y-auto p-4">
          <!-- 基础信息 -->
          <div class="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label class="block text-xs font-medium text-slate-500 mb-1">模板名称</label>
              <input
                v-model="editForm.name"
                type="text"
                class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/30 focus:border-blue-400"
                placeholder="模板名称"
              />
            </div>
            <div>
              <label class="block text-xs font-medium text-slate-500 mb-1">图标 (Emoji)</label>
              <input
                v-model="editForm.icon"
                type="text"
                class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/30 focus:border-blue-400"
                placeholder="📧"
              />
            </div>
          </div>

          <div class="mb-4">
            <label class="block text-xs font-medium text-slate-500 mb-1">描述</label>
            <input
              v-model="editForm.description"
              type="text"
              class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/30 focus:border-blue-400"
              placeholder="模板用途描述"
            />
          </div>

          <!-- 主题编辑 -->
          <div class="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label class="block text-xs font-medium text-slate-500 mb-1">中文主题</label>
              <input
                v-model="editForm.subject_zh"
                type="text"
                class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/30 focus:border-blue-400"
                placeholder="邮件中文主题"
              />
            </div>
            <div>
              <label class="block text-xs font-medium text-slate-500 mb-1">英文主题</label>
              <input
                v-model="editForm.subject_en"
                type="text"
                class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/30 focus:border-blue-400"
                placeholder="Email Subject"
              />
            </div>
          </div>

          <!-- 内容编辑区 -->
          <div class="mb-4">
            <div class="flex items-center justify-between mb-2">
              <label class="text-xs font-medium text-slate-500">邮件内容</label>
              <div class="flex items-center gap-2">
                <!-- 语气选择器 -->
                <div class="flex items-center gap-1">
                  <span class="text-xs text-slate-400 mr-1">语气:</span>
                  <button
                    v-for="tone in toneOptions"
                    :key="tone.value"
                    @click="selectedTone = tone.value"
                    :class="[
                      'px-2 py-1 text-xs rounded transition-colors',
                      selectedTone === tone.value
                        ? 'bg-blue-600 text-white'
                        : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                    ]"
                  >
                    {{ tone.label }}
                  </button>
                </div>
                <!-- 长度选择器 -->
                <div class="flex items-center gap-1">
                  <span class="text-xs text-slate-400 mr-1">长度:</span>
                  <button
                    v-for="length in lengthOptions"
                    :key="length.value"
                    @click="selectedLength = length.value"
                    :class="[
                      'px-2 py-1 text-xs rounded transition-colors',
                      selectedLength === length.value
                        ? 'bg-blue-600 text-white'
                        : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                    ]"
                  >
                    {{ length.label }}
                  </button>
                </div>
              </div>
            </div>

            <!-- 中英文内容切换 -->
            <div class="border border-slate-200 rounded-lg overflow-hidden">
              <div class="flex border-b border-slate-200">
                <button
                  @click="contentLang = 'zh'"
                  :class="[
                    'px-4 py-2 text-sm font-medium transition-colors',
                    contentLang === 'zh'
                      ? 'bg-white text-blue-600 border-b-2 border-blue-600 -mb-px'
                      : 'bg-slate-50 text-slate-500 hover:bg-slate-100'
                  ]"
                >
                  中文内容
                </button>
                <button
                  @click="contentLang = 'en'"
                  :class="[
                    'px-4 py-2 text-sm font-medium transition-colors',
                    contentLang === 'en'
                      ? 'bg-white text-blue-600 border-b-2 border-blue-600 -mb-px'
                      : 'bg-slate-50 text-slate-500 hover:bg-slate-100'
                  ]"
                >
                  英文内容
                </button>
              </div>
              <textarea
                v-model="currentContent"
                rows="10"
                class="w-full px-4 py-3 text-sm focus:outline-none resize-none"
                :placeholder="contentLang === 'zh' ? '输入中文邮件内容...' : 'Enter English email content...'"
              ></textarea>
            </div>
          </div>

          <!-- AI提示词 -->
          <div class="mb-4">
            <label class="block text-xs font-medium text-slate-500 mb-1">AI翻译提示词</label>
            <textarea
              v-model="editForm.ai_prompt"
              rows="3"
              class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/30 focus:border-blue-400 resize-none"
              placeholder="指导AI翻译的提示词..."
            ></textarea>
          </div>

          <!-- 落款名和风格 -->
          <div class="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label class="block text-xs font-medium text-slate-500 mb-1">落款名</label>
              <input
                v-model="editForm.sender_name"
                type="text"
                class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/30 focus:border-blue-400"
                placeholder="Pet Tag Studio"
              />
            </div>
            <div>
              <label class="block text-xs font-medium text-slate-500 mb-1">风格</label>
              <select
                v-model="editForm.style"
                class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/30 focus:border-blue-400"
              >
                <option value="">请选择</option>
                <option v-for="style in styleOptions" :key="style.value" :value="style.value">
                  {{ style.label }}
                </option>
              </select>
            </div>
          </div>

          <!-- 排序 -->
          <div class="mb-4 w-32">
            <label class="block text-xs font-medium text-slate-500 mb-1">排序权重</label>
            <input
              v-model.number="editForm.sort_order"
              type="number"
              min="0"
              class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/30 focus:border-blue-400"
            />
          </div>

          <!-- 底部操作按钮 -->
          <div class="flex items-center gap-3 pt-4 border-t border-slate-200">
            <button
              @click="saveTemplate"
              :disabled="saving"
              class="px-6 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white rounded-lg text-sm font-medium flex items-center gap-2 transition-colors"
            >
              <svg v-if="saving" class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ saving ? '保存中...' : '保存修改' }}
            </button>
            <button
              @click="resetForm"
              class="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-600 rounded-lg text-sm font-medium transition-colors"
            >
              重置
            </button>
          </div>
        </div>

        <!-- 未选择模板时的空状态 -->
        <div v-else class="flex-1 flex items-center justify-center text-slate-400">
          <div class="text-center">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" class="mx-auto mb-3 opacity-50">
              <rect width="20" height="16" x="2" y="4" rx="2"/>
              <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>
            </svg>
            <p>请在左侧选择一个邮件模板</p>
          </div>
        </div>
      </div>

      <!-- 右侧：预览面板 -->
      <div class="w-[350px] bg-white rounded-xl shadow-sm border border-slate-200 flex flex-col overflow-hidden">
        <div class="px-4 py-3 border-b border-slate-200 bg-slate-50">
          <h3 class="font-bold text-slate-800">实时预览</h3>
        </div>

        <!-- 预览语言切换 -->
        <div class="px-4 pt-3 flex gap-2">
          <button
            @click="previewLang = 'zh'"
            :class="[
              'flex-1 py-2 text-sm font-medium rounded-lg transition-colors',
              previewLang === 'zh'
                ? 'bg-blue-600 text-white'
                : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
            ]"
          >
            中文预览
          </button>
          <button
            @click="previewLang = 'en'"
            :class="[
              'flex-1 py-2 text-sm font-medium rounded-lg transition-colors',
              previewLang === 'en'
                ? 'bg-blue-600 text-white'
                : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
            ]"
          >
            English Preview
          </button>
        </div>

        <!-- 预览内容 -->
        <div v-if="selectedTemplate" class="flex-1 p-4 overflow-y-auto">
          <div class="bg-gray-50 rounded-lg p-4 border border-gray-200">
            <!-- 邮件头部 -->
            <div class="mb-4 pb-3 border-b border-gray-200">
              <div class="flex items-center gap-2 text-xs text-gray-500 mb-1">
                <span>收件人:</span>
                <span class="text-gray-700">jessica@example.com</span>
              </div>
              <div class="flex items-center gap-2 text-xs text-gray-500 mb-1">
                <span>主题:</span>
                <span class="text-gray-700 font-medium">{{ previewSubject }}</span>
              </div>
            </div>

            <!-- 邮件正文 -->
            <div class="text-sm text-gray-700 whitespace-pre-wrap leading-relaxed">
              {{ previewContent }}
            </div>

            <!-- 落款 -->
            <div class="mt-4 pt-3 border-t border-gray-200 text-sm text-gray-600">
              <p>Best regards,</p>
              <p class="font-medium">{{ editForm.sender_name || 'Store Team' }}</p>
            </div>
          </div>

          <!-- 变量说明 -->
          <div class="mt-4 p-3 bg-blue-50 rounded-lg">
            <h4 class="text-xs font-medium text-blue-700 mb-2">变量占位符</h4>
            <div class="space-y-1 text-xs">
              <div class="flex justify-between">
                <code class="bg-blue-100 text-blue-700 px-1 rounded">{firstName}</code>
                <span class="text-blue-600">→ Jessica</span>
              </div>
              <div class="flex justify-between">
                <code class="bg-blue-100 text-blue-700 px-1 rounded">{orderId}</code>
                <span class="text-blue-600">→ #4002217518</span>
              </div>
              <div class="flex justify-between">
                <code class="bg-blue-100 text-blue-700 px-1 rounded">{effectImageUrl}</code>
                <span class="text-blue-600">→ [效果图链接]</span>
              </div>
              <div class="flex justify-between">
                <code class="bg-blue-100 text-blue-700 px-1 rounded">{senderName}</code>
                <span class="text-blue-600">→ {{ editForm.sender_name || 'Store Team' }}</span>
              </div>
              <div class="flex justify-between">
                <code class="bg-blue-100 text-blue-700 px-1 rounded">{confirmationDeadline}</code>
                <span class="text-blue-600">→ 24 hours</span>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="flex-1 flex items-center justify-center text-slate-400 text-sm">
          选择模板后显示预览
        </div>
      </div>
    </div>

    <!-- 新建模板弹窗 -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click.self="showCreateModal = false">
      <div class="bg-white rounded-xl shadow-xl w-[500px] max-h-[80vh] overflow-y-auto">
        <div class="px-4 py-3 border-b border-slate-200 flex items-center justify-between">
          <h3 class="font-bold text-slate-800">新建邮件模板</h3>
          <button @click="showCreateModal = false" class="text-slate-400 hover:text-slate-600">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
          </button>
        </div>
        <div class="p-4 space-y-4">
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">模板类型 *</label>
            <select v-model="newTemplate.type" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm">
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.icon }} {{ cat.name }}</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">模板标识 *</label>
            <input v-model="newTemplate.template_key" type="text" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm" placeholder="如: standard, urgent" />
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">模板名称 *</label>
            <input v-model="newTemplate.name" type="text" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm" placeholder="显示名称" />
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">图标</label>
            <input v-model="newTemplate.icon" type="text" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm" placeholder="📧" />
          </div>
          <div class="flex justify-end gap-2 pt-2">
            <button @click="showCreateModal = false" class="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-600 rounded-lg text-sm">取消</button>
            <button @click="submitNewTemplate" :disabled="creating" class="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white rounded-lg text-sm">
              {{ creating ? '创建中...' : '创建' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

// API Base URL
const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

// 分类定义
const categories = [
  { id: 'first_confirm', name: '首封确认', icon: '📧' },
  { id: 'modification', name: '修改确认', icon: '✏️' },
  { id: 'follow_up', name: '追评邮件', icon: '⭐' }
]

// 语气选项
const toneOptions = [
  { value: 'formal', label: '正式' },
  { value: 'casual', label: '随和' },
  { value: 'lively', label: '活泼' }
]

// 长度选项
const lengthOptions = [
  { value: 'short', label: '简短' },
  { value: 'standard', label: '标准' },
  { value: 'detailed', label: '详细' }
]

// 风格选项
const styleOptions = [
  { value: 'professional', label: '专业' },
  { value: 'friendly', label: '友好' },
  { value: 'casual', label: '随和' },
  { value: 'warm', label: '温馨' }
]

// 状态
const loading = ref(true)
const saving = ref(false)
const creating = ref(false)
const showCreateModal = ref(false)
const templates = ref({ first_confirm: [], modification: [], follow_up: [] })
const activeCategory = ref('first_confirm')
const selectedTemplate = ref(null)
const selectedTone = ref('formal')
const selectedLength = ref('standard')
const contentLang = ref('zh')
const previewLang = ref('zh')

// 编辑表单
const editForm = ref({
  name: '',
  icon: '',
  description: '',
  subject_zh: '',
  subject_en: '',
  content: {},
  ai_prompt: '',
  sender_name: '',
  style: '',
  sort_order: 0,
  is_active: true
})

// 新建模板表单
const newTemplate = ref({
  type: 'first_confirm',
  template_key: '',
  name: '',
  icon: '📧'
})

// 原始数据备份（用于检测变更）
const originalForm = ref({})

// 计算是否有未保存的更改
const hasUnsavedChanges = computed(() => {
  if (!selectedTemplate.value) return false
  return JSON.stringify(editForm.value) !== JSON.stringify(originalForm.value)
})

// 获取分类模板数量
const getCategoryTemplateCount = (categoryId) => {
  return templates.value[categoryId]?.length || 0
}

// 获取分类模板列表
const getCategoryTemplates = (categoryId) => {
  return templates.value[categoryId] || []
}

// 选择分类
const selectCategory = (categoryId) => {
  activeCategory.value = categoryId
  const categoryTemplates = getCategoryTemplates(categoryId)
  if (categoryTemplates.length > 0) {
    selectTemplate(categoryTemplates[0])
  } else {
    selectedTemplate.value = null
    resetEditForm()
  }
}

// 选择模板
const selectTemplate = (template) => {
  selectedTemplate.value = template
  // 填充编辑表单
  editForm.value = {
    name: template.name || '',
    icon: template.icon || '',
    description: template.description || '',
    subject_zh: template.subject_zh || '',
    subject_en: template.subject_en || '',
    content: template.content || {},
    ai_prompt: template.ai_prompt || '',
    sender_name: template.sender_name || '',
    style: template.style || '',
    sort_order: template.sort_order || 0,
    is_active: template.is_active !== false
  }
  // 备份原始数据
  originalForm.value = JSON.parse(JSON.stringify(editForm.value))
}

// 重置编辑表单
const resetEditForm = () => {
  editForm.value = {
    name: '',
    icon: '',
    description: '',
    subject_zh: '',
    subject_en: '',
    content: {},
    ai_prompt: '',
    sender_name: '',
    style: '',
    sort_order: 0,
    is_active: true
  }
  originalForm.value = JSON.parse(JSON.stringify(editForm.value))
}

// 当前编辑的内容（根据语气和长度）
const currentContent = computed({
  get() {
    if (!editForm.value.content) return ''
    const tone = selectedTone.value
    const length = selectedLength.value
    const lang = contentLang.value
    try {
      return editForm.value.content?.[tone]?.[length]?.[lang] || ''
    } catch {
      return ''
    }
  },
  set(value) {
    if (!editForm.value.content) {
      editForm.value.content = {}
    }
    const tone = selectedTone.value
    const length = selectedLength.value
    const lang = contentLang.value
    if (!editForm.value.content[tone]) {
      editForm.value.content[tone] = {}
    }
    if (!editForm.value.content[tone][length]) {
      editForm.value.content[tone][length] = {}
    }
    editForm.value.content[tone][length][lang] = value
  }
})

// 预览主题
const previewSubject = computed(() => {
  if (!selectedTemplate.value) return ''
  const subject = previewLang.value === 'zh' ? editForm.value.subject_zh : editForm.value.subject_en
  return replaceVariables(subject || '')
})

// 预览内容
const previewContent = computed(() => {
  if (!selectedTemplate.value) return ''
  const tone = selectedTone.value
  const length = selectedLength.value
  const lang = previewLang.value
  let content = ''
  try {
    content = editForm.value.content?.[tone]?.[length]?.[lang] || ''
  } catch {
    content = ''
  }
  return replaceVariables(content)
})

// 替换变量
const replaceVariables = (text) => {
  if (!text) return ''
  return text
    .replace(/{firstName}/g, 'Jessica')
    .replace(/{orderId}/g, '#4002217518')
    .replace(/{effectImageUrl}/g, '[效果图链接]')
    .replace(/{senderName}/g, editForm.value.sender_name || 'Store Team')
    .replace(/{confirmationDeadline}/g, '24 hours')
}

// 加载模板数据
const loadTemplates = async () => {
  loading.value = true
  try {
    const response = await fetch(`${API_BASE}/api/email-templates`)
    const result = await response.json()
    if (result.success) {
      templates.value = result.data
      // 自动选择第一个模板
      const firstCategory = categories[0].id
      const firstTemplates = templates.value[firstCategory] || []
      if (firstTemplates.length > 0) {
        activeCategory.value = firstCategory
        selectTemplate(firstTemplates[0])
      }
    } else {
      ElMessage.error(result.message || '加载模板失败')
    }
  } catch (error) {
    console.error('加载模板失败:', error)
    ElMessage.error('加载模板失败，请检查网络连接')
  } finally {
    loading.value = false
  }
}

// 保存模板
const saveTemplate = async () => {
  if (!selectedTemplate.value) return
  saving.value = true
  try {
    const response = await fetch(`${API_BASE}/api/email-templates/${selectedTemplate.value.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: editForm.value.name,
        description: editForm.value.description,
        subject_zh: editForm.value.subject_zh,
        subject_en: editForm.value.subject_en,
        content: editForm.value.content,
        ai_prompt: editForm.value.ai_prompt,
        sender_name: editForm.value.sender_name,
        style: editForm.value.style,
        sort_order: editForm.value.sort_order,
        is_active: editForm.value.is_active
      })
    })
    const result = await response.json()
    if (result.success) {
      ElMessage.success('模板保存成功')
      // 更新本地数据
      const tpl = templates.value[selectedTemplate.value.type]?.find(t => t.id === selectedTemplate.value.id)
      if (tpl) {
        Object.assign(tpl, result.data)
      }
      selectedTemplate.value = result.data
      originalForm.value = JSON.parse(JSON.stringify(editForm.value))
    } else {
      ElMessage.error(result.message || '保存失败')
    }
  } catch (error) {
    console.error('保存模板失败:', error)
    ElMessage.error('保存失败，请检查网络连接')
  } finally {
    saving.value = false
  }
}

// 重置表单
const resetForm = () => {
  if (selectedTemplate.value) {
    selectTemplate(selectedTemplate.value)
  }
}

// 切换模板启用状态
const toggleTemplateActive = async () => {
  if (!selectedTemplate.value) return
  editForm.value.is_active = !editForm.value.is_active
  await saveTemplate()
}

// 删除模板
const deleteTemplate = async () => {
  if (!selectedTemplate.value) return
  if (!confirm(`确定要删除模板 "${selectedTemplate.value.name}" 吗？此操作不可恢复。`)) {
    return
  }
  try {
    const response = await fetch(`${API_BASE}/api/email-templates/${selectedTemplate.value.id}`, {
      method: 'DELETE'
    })
    const result = await response.json()
    if (result.success) {
      ElMessage.success('模板已删除')
      // 从本地数据中移除
      const list = templates.value[selectedTemplate.value.type]
      const index = list?.findIndex(t => t.id === selectedTemplate.value.id)
      if (index > -1) {
        list.splice(index, 1)
      }
      // 选择下一个模板
      selectCategory(activeCategory.value)
    } else {
      ElMessage.error(result.message || '删除失败')
    }
  } catch (error) {
    console.error('删除模板失败:', error)
    ElMessage.error('删除失败，请检查网络连接')
  }
}

// 创建新模板
const createNewTemplate = () => {
  newTemplate.value = {
    type: activeCategory.value,
    template_key: '',
    name: '',
    icon: '📧'
  }
  showCreateModal.value = true
}

// 提交新建模板
const submitNewTemplate = async () => {
  if (!newTemplate.value.template_key || !newTemplate.value.name) {
    ElMessage.warning('请填写模板标识和名称')
    return
  }
  creating.value = true
  try {
    const response = await fetch(`${API_BASE}/api/email-templates`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...newTemplate.value,
        content: {
          formal: { short: { zh: '', en: '' }, standard: { zh: '', en: '' }, detailed: { zh: '', en: '' } },
          casual: { short: { zh: '', en: '' }, standard: { zh: '', en: '' }, detailed: { zh: '', en: '' } },
          lively: { short: { zh: '', en: '' }, standard: { zh: '', en: '' }, detailed: { zh: '', en: '' } }
        }
      })
    })
    const result = await response.json()
    if (result.success) {
      ElMessage.success('模板创建成功')
      showCreateModal.value = false
      // 添加到本地数据
      if (!templates.value[result.data.type]) {
        templates.value[result.data.type] = []
      }
      templates.value[result.data.type].push(result.data)
      // 选择新创建的模板
      activeCategory.value = result.data.type
      selectTemplate(result.data)
    } else {
      ElMessage.error(result.message || '创建失败')
    }
  } catch (error) {
    console.error('创建模板失败:', error)
    ElMessage.error('创建失败，请检查网络连接')
  } finally {
    creating.value = false
  }
}

// 初始化
onMounted(() => {
  loadTemplates()
})
</script>

<style scoped>
/* 自定义滚动条 */
::-webkit-scrollbar {
  width: 6px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>
