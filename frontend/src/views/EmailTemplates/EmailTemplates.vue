<template>
  <div class="bg-slate-200 min-h-[964px] min-w-max flex items-center justify-center p-8">
    <div class="flex h-[900px] w-[1480px] bg-white shadow-2xl rounded-2xl overflow-hidden shrink-0">

      <!-- 左侧导航栏 -->
      <div class="w-64 bg-white border-r border-slate-200 flex flex-col h-full overflow-y-auto shrink-0">
        <div class="p-6">
          <h1 class="text-xl font-bold text-slate-800 flex items-center gap-2">
            <span class="w-2 h-6 bg-blue-600 rounded-full"></span>
            仪表盘总览
          </h1>
        </div>
        <nav class="px-4 space-y-1">
          <button @click="$router.push('/')" class="w-full flex items-center justify-between px-4 py-3 rounded-xl transition-colors text-slate-600 hover:bg-slate-50">
            <div class="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/></svg>
              <span class="font-medium">仪表盘总览</span>
            </div>
          </button>
          <button @click="$router.push('/pending')" class="w-full flex items-center justify-between px-4 py-3 rounded-xl transition-colors text-slate-600 hover:bg-slate-50">
            <div class="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="8" height="4" x="8" y="2" rx="1" ry="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="M12 11h4"/><path d="M12 16h4"/><path d="M8 11h.01"/><path d="M8 16h.01"/></svg>
              <span class="font-medium">待确认订单</span>
            </div>
            <span class="text-xs font-bold px-2 py-0.5 rounded-full bg-slate-100 text-slate-600">32</span>
          </button>
          <button @click="$router.push('/production')" class="w-full flex items-center justify-between px-4 py-3 rounded-xl transition-colors text-slate-600 hover:bg-slate-50">
            <div class="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 12-8.5 8.5c-.83.83-2.17.83-3 0 0 0 0 0 0 0a2.12 2.12 0 0 1 0-3L12 9"/><path d="M17.64 15 22 10.64"/><path d="m20.91 11.7-1.25-1.25c-.6-.6-.93-1.4-.93-2.25V7.86c0-.55-.45-1-1-1H14.5c-.85 0-1.65-.33-2.25-.93L11 4.71"/><path d="M5.8 5.81a2.2 2.2 0 0 1 3.1 0l1.3 1.3"/></svg>
              <span class="font-medium">生产中订单</span>
            </div>
            <span class="text-xs font-bold px-2 py-0.5 rounded-full bg-slate-100 text-slate-600">18</span>
          </button>
          <button @click="$router.push('/completed')" class="w-full flex items-center justify-between px-4 py-3 rounded-xl transition-colors text-slate-600 hover:bg-slate-50">
            <div class="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/></svg>
              <span class="font-medium">已完成订单</span>
            </div>
            <span class="text-xs font-bold px-2 py-0.5 rounded-full bg-slate-100 text-slate-600">64</span>
          </button>
          <button @click="$router.push('/logistics')" class="w-full flex items-center justify-between px-4 py-3 rounded-xl transition-colors text-slate-600 hover:bg-slate-50">
            <div class="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H9"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.624l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/></svg>
              <span class="font-medium">物流追踪</span>
            </div>
            <span class="text-xs font-bold px-2 py-0.5 rounded-full bg-slate-100 text-slate-600">8</span>
          </button>
          <!-- 邮件模板 Active -->
          <button class="w-full flex items-center justify-between px-4 py-3 rounded-xl bg-blue-50 text-blue-600">
            <div class="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
              <span class="font-medium">邮件模板</span>
            </div>
          </button>
        </nav>

        <!-- 统计卡片 -->
        <div class="p-4 mt-4">
          <div class="grid grid-cols-2 gap-3">
            <div class="bg-white border border-slate-200 rounded-xl p-3 shadow-sm flex flex-col items-center justify-center text-center">
              <div class="relative w-20 h-20 flex items-center justify-center mb-1">
                <svg width="80" height="80" viewBox="0 0 80 80" class="absolute transform -rotate-90"><circle cx="40" cy="40" r="28" stroke="#e2e8f0" stroke-width="5" fill="transparent"/><circle cx="40" cy="40" r="28" stroke="#3b82f6" stroke-width="5" fill="transparent" stroke-dasharray="175.93" stroke-dashoffset="43.98" stroke-linecap="round"/></svg>
                <span class="text-lg font-bold z-10 text-blue-600">24</span>
              </div>
              <span class="text-xs font-medium text-slate-600">模板总数</span>
              <span class="text-[10px] text-slate-400">运营话术</span>
            </div>
            <div class="bg-white border border-slate-200 rounded-xl p-3 shadow-sm flex flex-col items-center justify-center text-center">
              <div class="relative w-20 h-20 flex items-center justify-center mb-1">
                <svg width="80" height="80" viewBox="0 0 80 80" class="absolute transform -rotate-90"><circle cx="40" cy="40" r="28" stroke="#e2e8f0" stroke-width="5" fill="transparent"/><circle cx="40" cy="40" r="28" stroke="#f97316" stroke-width="5" fill="transparent" stroke-dasharray="175.93" stroke-dashoffset="131.95" stroke-linecap="round"/></svg>
                <span class="text-lg font-bold z-10 text-orange-600">6</span>
              </div>
              <span class="text-xs font-medium text-slate-600">首封确认</span>
              <span class="text-[10px] text-slate-400">下单后第一封</span>
            </div>
            <div class="bg-white border border-slate-200 rounded-xl p-3 shadow-sm flex flex-col items-center justify-center text-center">
              <div class="relative w-20 h-20 flex items-center justify-center mb-1">
                <svg width="80" height="80" viewBox="0 0 80 80" class="absolute transform -rotate-90"><circle cx="40" cy="40" r="28" stroke="#e2e8f0" stroke-width="5" fill="transparent"/><circle cx="40" cy="40" r="28" stroke="#a855f7" stroke-width="5" fill="transparent" stroke-dasharray="175.93" stroke-dashoffset="144.26" stroke-linecap="round"/></svg>
                <span class="text-lg font-bold z-10 text-purple-600">4</span>
              </div>
              <span class="text-xs font-medium text-slate-600">延迟/异常</span>
              <span class="text-[10px] text-slate-400">工厂&物流</span>
            </div>
            <div class="bg-white border border-slate-200 rounded-xl p-3 shadow-sm flex flex-col items-center justify-center text-center">
              <div class="relative w-20 h-20 flex items-center justify-center mb-1">
                <svg width="80" height="80" viewBox="0 0 80 80" class="absolute transform -rotate-90"><circle cx="40" cy="40" r="28" stroke="#e2e8f0" stroke-width="5" fill="transparent"/><circle cx="40" cy="40" r="28" stroke="#22c55e" stroke-width="5" fill="transparent" stroke-dasharray="175.93" stroke-dashoffset="87.96" stroke-linecap="round"/></svg>
                <span class="text-lg font-bold z-10 text-green-600">8</span>
              </div>
              <span class="text-xs font-medium text-slate-600">追评邮件</span>
              <span class="text-[10px] text-slate-400">签收后催评</span>
            </div>
          </div>
        </div>

        <!-- 底部提示 -->
        <div class="px-4 pb-4 mt-auto">
          <div class="bg-slate-50 border border-slate-200 rounded-xl p-3 text-[11px] text-slate-500 leading-relaxed">
            <div class="flex items-center gap-2 mb-1">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
              <span class="font-medium text-slate-700">运营话术知识库</span>
            </div>
            <p>这里的模板不绑定单个订单，提供客服用语参考，可复制到各页面的邮件编辑区使用。</p>
          </div>
        </div>
      </div>

      <!-- 右侧主内容 -->
      <div class="flex-1 bg-slate-50 overflow-hidden flex flex-col h-full">

        <!-- Header + Tab -->
        <div class="px-6 pt-6 pb-4 shrink-0">
          <div class="flex items-center justify-between mb-2">
            <div class="flex items-center gap-3">
              <h2 class="text-2xl font-bold text-slate-800">邮件模板</h2>
              <span class="bg-blue-100 text-blue-600 px-3 py-1 rounded-full text-xs font-bold">运营话术知识库</span>
            </div>
            <span class="text-xs text-slate-400">此页面模板不针对单笔订单，仅作运营参考使用</span>
          </div>
          <div class="flex items-center gap-2 mt-3">
            <button v-for="(sec, i) in sections" :key="i" @click="switchTab(i)"
              :class="currentSection === i
                ? 'bg-slate-800 text-white'
                : 'bg-white border border-slate-200 text-slate-500 hover:bg-slate-50'"
              class="px-4 py-2 rounded-xl text-xs font-bold transition-colors">
              {{ i + 1 }}. {{ sec.tabLabel }}
            </button>
          </div>
        </div>

        <!-- 三列内容 -->
        <div class="flex flex-1 overflow-hidden px-6 pb-6 gap-4">

          <!-- 左列：板块说明 + 分类标签 -->
          <div class="w-[220px] shrink-0 flex flex-col gap-4">
            <div class="bg-white rounded-xl border border-slate-200 p-4 shadow-sm">
              <div class="flex items-center gap-2 mb-2">
                <span :class="currentSec.badge" class="inline-flex items-center justify-center w-6 h-6 rounded-full text-xs font-bold">{{ currentSection + 1 }}</span>
                <span class="text-xs font-bold text-slate-800">{{ currentSec.title }}</span>
              </div>
              <p class="text-[11px] text-slate-500 mb-2">{{ currentSec.subtitle }}</p>
              <div class="text-[11px] space-y-1">
                <div><span class="text-slate-400">目标：</span><span class="text-slate-700">{{ currentSec.goal }}</span></div>
                <div><span class="text-slate-400">位置：</span><span class="text-slate-700">{{ currentSec.usage }}</span></div>
              </div>
            </div>
            <div class="bg-white rounded-xl border border-slate-200 p-4 shadow-sm flex-1">
              <div class="flex items-center justify-between mb-3">
                <span class="text-xs font-semibold text-slate-700">分类标签</span>
                <span class="text-[10px] text-slate-400">选中后筛选列表</span>
              </div>
              <div class="flex flex-wrap gap-2">
                <span v-for="(tag, i) in currentSec.tags" :key="i"
                  :class="currentSec.tagColors[i]"
                  class="px-2 py-0.5 rounded-full text-[11px] font-medium cursor-pointer">
                  {{ tag }}
                </span>
              </div>
            </div>
          </div>

          <!-- 中列：模板列表 -->
          <div class="w-[260px] shrink-0 bg-white rounded-xl border border-slate-200 shadow-sm flex flex-col overflow-hidden">
            <div class="px-4 py-3 border-b border-slate-100 flex items-center justify-between shrink-0">
              <span class="text-xs font-semibold text-slate-700">模板列表</span>
              <span class="text-[10px] text-slate-400">共 {{ currentSec.templates.length }} 个模板</span>
            </div>
            <div class="flex-1 overflow-y-auto p-3 space-y-2">
              <button v-for="(tpl, i) in currentSec.templates" :key="i"
                @click="selectTemplate(i)"
                :class="currentTemplate === i
                  ? 'border-blue-300 bg-blue-50'
                  : 'border-slate-200 hover:bg-slate-50'"
                class="w-full text-left p-3 rounded-xl border transition-all">
                <div class="font-semibold text-xs text-slate-800 mb-0.5">{{ tpl.name }}</div>
                <div class="text-[10px] text-slate-400">{{ tpl.desc }}</div>
              </button>
            </div>
          </div>

          <!-- 右列：预览区 -->
          <div class="flex-1 bg-white rounded-xl border border-slate-200 shadow-sm flex flex-col overflow-hidden">
            <div class="px-5 py-3 border-b border-slate-100 flex items-center justify-between shrink-0">
              <div>
                <div class="text-[10px] text-slate-400 mb-0.5">{{ currentTpl.previewLabel }}</div>
                <div class="text-sm font-semibold text-slate-800">{{ currentTpl.subject }}</div>
              </div>
              <button @click="copyBody"
                class="flex items-center gap-1.5 text-[11px] px-3 py-1.5 rounded-lg bg-slate-50 border border-slate-200 transition-colors"
                :class="copied ? 'text-green-600 border-green-200' : 'text-slate-600 hover:bg-slate-100'">
                <svg v-if="!copied" xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m9 11 3 3L22 4"/></svg>
                {{ copied ? '已复制' : '复制正文' }}
              </button>
            </div>
            <div class="flex-1 overflow-y-auto p-5 text-sm text-slate-600 leading-relaxed" v-html="currentTpl.body"></div>
            <div class="px-5 py-3 border-t border-slate-100 bg-slate-50 text-[11px] text-slate-500 flex items-center gap-2 shrink-0">
              <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 8v4l3 3"/></svg>
              <span>适用场景：{{ currentTpl.footer }}</span>
            </div>
          </div>

        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const currentSection = ref(0)
const currentTemplate = ref(0)
const copied = ref(false)

const sections = [
  {
    tabLabel: '首封确认邮件',
    title: '首封确认邮件模板', subtitle: '下单后第一封',
    badge: 'bg-blue-100 text-blue-600',
    goal: '确认信息 + 建立信任', usage: '待确认订单页 — 邮件生成',
    tags: ['标准确认', '带交期说明', '包含注意事项', '温柔语气', '强调定制不可退'],
    tagColors: ['bg-blue-100 text-blue-600','bg-emerald-100 text-emerald-700','bg-slate-100 text-slate-600','bg-indigo-100 text-indigo-700','bg-amber-100 text-amber-700'],
    templates: [
      {
        name: '标准确认 · 简洁版', desc: '包含订单号 + 预计发货时间',
        subject: 'Subject: Order confirmation for your customized tag',
        previewLabel: '预览 · 标准确认 · 简洁版',
        body: `<p class="mb-3">Hi <span class="font-mono text-slate-800">{{ customer_name }}</span>,</p><p class="mb-3">Thank you so much for your order! This is just a quick note to confirm that we've received your order <span class="font-mono text-slate-800">#{{ order_id }}</span> for a customized tag.</p><p class="mb-3">We'll carefully prepare your design and start production soon. The current estimated ship-out date is <span class="font-semibold text-slate-800">{{ ship_date }}</span>.</p><p class="mb-3">If you'd like to adjust the text, font or any detail, simply reply to this message within 24 hours and we'll be happy to help.</p><p>Warm regards,<br/><span class="text-slate-500">{{ shop_name }}</span></p>`,
        footer: '适用：标准新订单 · 下单后24小时内发送'
      },
      {
        name: '温柔关怀 · 详细版', desc: '适合首次下单的新客户',
        subject: 'Subject: Your custom order is in good hands 💛',
        previewLabel: '预览 · 温柔关怀 · 新客户首单',
        body: `<p class="mb-3">Hi <span class="font-mono text-slate-800">{{ customer_name }}</span>,</p><p class="mb-3">I'm so excited to be working on your order! Welcome to our little shop — it truly means a lot to us that you chose us for your special piece.</p><p class="mb-3">Here's a quick summary: Order <span class="font-mono text-slate-800">#{{ order_id }}</span> · Design: <span class="font-mono text-slate-800">{{ design_detail }}</span> · Font: <span class="font-mono text-slate-800">{{ font_name }}</span> · Est. ship-out: <span class="font-semibold text-slate-800">{{ ship_date }}</span>.</p><p class="mb-3">If anything looks different from what you had in mind, please reply within 24 hours!</p><p>Warmly,<br/><span class="text-slate-500">{{ shop_name }}</span></p>`,
        footer: '适用：新客户首单 · 高单价定制'
      },
      {
        name: '强调定制属性 · 风险提示', desc: '适用于高金额 / 高定制订单',
        subject: 'Subject: Important note about your customized order',
        previewLabel: '预览 · 强调定制属性 · 风险提示版',
        body: `<p class="mb-3">Hi <span class="font-mono text-slate-800">{{ customer_name }}</span>,</p><p class="mb-3">Thank you for placing your order <span class="font-mono text-slate-800">#{{ order_id }}</span>! Before we begin, please confirm: Front: <span class="font-mono text-slate-800">{{ front_text }}</span> · Back: <span class="font-mono text-slate-800">{{ back_text }}</span> · Font: <span class="font-mono text-slate-800">{{ font_name }}</span>.</p><p class="mb-3">Please note: because this is a personalized item, <span class="font-semibold text-slate-800">changes or cancellations will not be possible once production begins</span>. If everything looks correct, no reply is needed!</p><p>Best regards,<br/><span class="text-slate-500">{{ shop_name }}</span></p>`,
        footer: '适用：大批量订单 · 强调不可退改'
      }
    ]
  },
  {
    tabLabel: '自然语言风格',
    title: '自然语言风格话术', subtitle: '如何显得友好自然',
    badge: 'bg-emerald-100 text-emerald-700',
    goal: '像真人在说话，不像机器人', usage: '所有邮件编辑区（可插入片段）',
    tags: ['轻松友好', '真诚感谢', '解释清楚', '不推卸责任', '带一点可爱'],
    tagColors: ['bg-blue-100 text-blue-600','bg-emerald-100 text-emerald-700','bg-amber-100 text-amber-700','bg-slate-100 text-slate-600','bg-pink-100 text-pink-700'],
    templates: [
      {
        name: 'Friendly opening · 友好开头', desc: '用于回复客户问题 / 确认细节',
        subject: '可插入片段 · Friendly opening',
        previewLabel: '示例 · 友好开头段落',
        body: `<p class="mb-3 text-slate-400 text-xs font-medium uppercase tracking-wide">// 开头段落示例</p><p class="mb-3">Hope you're having a wonderful day! Thank you so much for reaching out — I'm always happy to help.</p><p class="mb-3">Also, a huge thank you for choosing our little shop for your special piece. It really means a lot to us!</p><hr class="my-4 border-slate-100"/><p class="mb-3 text-slate-400 text-xs font-medium uppercase tracking-wide">// 回复客户疑问时的开头</p><p class="mb-3">Thank you for your message! Great question — let me explain how this works.</p><p class="text-slate-400 text-xs italic">💡 建议：第一句话不要直接进入正题，先表示感谢和热情。</p>`,
        footer: '适用场景：所有邮件开头'
      },
      {
        name: 'Soft apology · 温和道歉', desc: '适用于轻微延迟或小问题',
        subject: '可插入片段 · Soft apology',
        previewLabel: '示例 · 温和道歉片段',
        body: `<p class="mb-3 text-slate-400 text-xs font-medium uppercase tracking-wide">// 轻微延迟道歉</p><p class="mb-3">I apologize for the slight delay — things have been a little busier than usual at the workshop, but I want to make sure your order gets the care and attention it deserves.</p><p class="mb-3">Thank you so much for your patience and understanding, it really means a lot!</p><hr class="my-4 border-slate-100"/><p class="mb-3 text-slate-400 text-xs font-medium uppercase tracking-wide">// 沟通误解道歉</p><p class="mb-3">I'm sorry for any confusion — that was entirely my fault and I should have explained it more clearly!</p><p class="text-slate-400 text-xs italic">💡 建议：道歉不要过度，点到即止，紧接着给出解决方案。</p>`,
        footer: '适用场景：小延迟、沟通误差'
      },
      {
        name: 'Warm closing · 温暖结尾', desc: '适用于所有场景的收尾',
        subject: '可插入片段 · Warm closing',
        previewLabel: '示例 · 温暖结尾片段',
        body: `<p class="mb-3 text-slate-400 text-xs font-medium uppercase tracking-wide">// 标准温暖结尾</p><p class="mb-3">Thank you again for your support and patience — it truly means the world to a small shop like ours 🙏</p><p class="mb-3">Warm regards,<br/><span class="text-slate-500">{{ shop_name }}</span></p><hr class="my-4 border-slate-100"/><p class="mb-3 text-slate-400 text-xs font-medium uppercase tracking-wide">// 可爱风格结尾</p><p class="mb-3">Thanks again for being so awesome and patient 💛 Can't wait for you to see the final result!</p><p class="text-slate-400 text-xs italic">💡 建议：结尾要温暖有个性，避免千篇一律的『Best regards』。</p>`,
        footer: '适用场景：所有邮件结尾'
      }
    ]
  },
  {
    tabLabel: '延迟/异常说明',
    title: '延迟/异常说明模板', subtitle: '工厂延迟、物流问题',
    badge: 'bg-amber-100 text-amber-700',
    goal: '诚实说明 + 提供解决方案', usage: '生产中订单页 / 物流追踪页',
    tags: ['工厂生产延迟', '物流运输延迟', '地址问题', '天气/不可抗力'],
    tagColors: ['bg-amber-100 text-amber-700','bg-blue-100 text-blue-600','bg-red-100 text-red-600','bg-slate-100 text-slate-600'],
    templates: [
      {
        name: '轻微延迟（1-2天）', desc: '简短说明 + 再次感谢耐心',
        subject: 'Subject: A quick update on your order {{ order_id }}',
        previewLabel: '预览 · 轻微延迟 · 1-2天',
        body: `<p class="mb-3">Hi <span class="font-mono text-slate-800">{{ customer_name }}</span>,</p><p class="mb-3">I wanted to give you a quick heads-up that your order <span class="font-mono text-slate-800">#{{ order_id }}</span> is running just a tiny bit behind schedule — about 1-2 days later than originally planned.</p><p class="mb-3">The updated estimated ship-out date is <span class="font-semibold text-slate-800">{{ new_ship_date }}</span>. Your order is still on track and I'll keep you posted!</p><p class="mb-3">Thank you so much for your patience — it truly means a lot to us.</p><p>Warm regards,<br/><span class="text-slate-500">{{ shop_name }}</span></p>`,
        footer: '适用：工厂轻微延误 · 无需补偿'
      },
      {
        name: '中度延迟（3-5天）', desc: '解释原因 + 提供小补偿',
        subject: 'Subject: Important update — your order {{ order_id }}',
        previewLabel: '预览 · 中度延迟 · 3-5天',
        body: `<p class="mb-3">Hi <span class="font-mono text-slate-800">{{ customer_name }}</span>,</p><p class="mb-3">I wanted to reach out personally about your order <span class="font-mono text-slate-800">#{{ order_id }}</span>. Due to <span class="font-semibold text-slate-800">{{ delay_reason }}</span>, the updated estimated ship-out is <span class="font-semibold text-slate-800">{{ new_ship_date }}</span> — approximately 3-5 days later than planned.</p><p class="mb-3">I sincerely apologize for this. As a small token of appreciation for your patience, I'd love to offer you <span class="font-semibold text-slate-800">a discount on your next order</span>.</p><p>Thank you for your understanding,<br/><span class="text-slate-500">{{ shop_name }}</span></p>`,
        footer: '适用：工厂明显延误 · 建议给小补偿'
      },
      {
        name: '物流异常（久未更新/疑似丢件）', desc: '主动提出重制 / 退款方案',
        subject: 'Subject: Following up on your shipment {{ tracking_number }}',
        previewLabel: '预览 · 物流异常 · 疑似丢件',
        body: `<p class="mb-3">Hi <span class="font-mono text-slate-800">{{ customer_name }}</span>,</p><p class="mb-3">I've been closely monitoring the tracking for your order <span class="font-mono text-slate-800">#{{ order_id }}</span> (tracking: <span class="font-mono text-blue-600">{{ tracking_number }}</span>), and I'm concerned that there hasn't been any update for the past <span class="font-semibold text-slate-800">{{ days_no_update }} days</span>.</p><p class="mb-3">Here are your options: <br/>A: We remake and reship your order right away at no extra cost<br/>B: We issue a full refund if you no longer need the item.</p><p class="mb-3">I'm so sorry this happened. I will make this right for you.</p><p>Sincerely,<br/><span class="text-slate-500">{{ shop_name }}</span></p>`,
        footer: '适用：物流丢失 · 必须主动给出解决方案'
      }
    ]
  },
  {
    tabLabel: '追评邮件',
    title: '追评邮件模板', subtitle: '签收后催评',
    badge: 'bg-indigo-100 text-indigo-700',
    goal: '礼貌催评，不给压力', usage: '已完成订单页 — 追评邮件正文区',
    tags: ['温柔提醒', '强调对小店的重要性', '附上直达链接', '明确无压力'],
    tagColors: ['bg-green-100 text-green-700','bg-blue-100 text-blue-600','bg-amber-100 text-amber-700','bg-slate-100 text-slate-600'],
    templates: [
      {
        name: '签收后 3 天 · 首次提醒', desc: '轻松感谢 + 简单说明',
        subject: 'Subject: How is your order doing? 💌',
        previewLabel: '预览 · 签收后3天 · 首次催评',
        body: `<p class="mb-3">Hi <span class="font-mono text-slate-800">{{ customer_name }}</span>,</p><p class="mb-3">Hope you're doing great! It's been a few days since your order arrived, and I just wanted to check in — I truly hope everything looks perfect 💛</p><p class="mb-3">If you have a moment, it would mean a lot to our little shop if you could leave a quick review. Your feedback really helps other customers feel confident when choosing us.</p><p class="mb-3">You can leave your review here:<br/><span class="text-xs text-blue-600 underline cursor-pointer">https://www.etsy.com/your_shop/review_link</span></p><p class="mb-3">No pressure at all — your happiness with the order comes first!</p><p>Warm regards,<br/><span class="text-slate-500">{{ shop_name }}</span></p>`,
        footer: '适用：签收后3天内 · 未留评且无投诉'
      },
      {
        name: '签收后 10 天 · 温柔二次提醒', desc: '仅适用于未评价且无投诉的订单',
        subject: 'Subject: Just checking in 🙂',
        previewLabel: '预览 · 签收后10天 · 二次催评',
        body: `<p class="mb-3">Hi <span class="font-mono text-slate-800">{{ customer_name }}</span>,</p><p class="mb-3">I hope you're enjoying your personalized piece! I know life gets busy, so I just wanted to send one last gentle reminder — if you ever have a spare moment, we'd truly appreciate a quick review on Etsy.</p><p class="mb-3">It only takes 30 seconds and it makes such a big difference for a small shop like ours 🙏</p><p class="mb-3"><span class="text-xs text-blue-600 underline cursor-pointer">https://www.etsy.com/your_shop/review_link</span></p><p>With gratitude,<br/><span class="text-slate-500">{{ shop_name }}</span></p>`,
        footer: '适用：签收后7-14天 · 二次提醒（最多发1次）'
      }
    ]
  },
  {
    tabLabel: '常见问题回复',
    title: '常见问题回复话术', subtitle: '客户问修改/退款等',
    badge: 'bg-slate-100 text-slate-700',
    goal: '统一口径，兼顾原则和温度', usage: '待确认订单 / 已完成订单',
    tags: ['修改定制内容', '急件/加急', '退款/取消订单', '质量问题', '物流久未更新'],
    tagColors: ['bg-blue-100 text-blue-600','bg-amber-100 text-amber-700','bg-rose-100 text-rose-700','bg-emerald-100 text-emerald-700','bg-slate-100 text-slate-600'],
    templates: [
      {
        name: '修改定制内容（生产前）', desc: '确认尚未生产，表示可以修改',
        subject: 'Subject: Re: Change request for your order {{ order_id }}',
        previewLabel: '预览 · 生产前修改定制内容',
        body: `<p class="mb-3">Hi <span class="font-mono text-slate-800">{{ customer_name }}</span>,</p><p class="mb-3">Thanks a lot for your message and for letting me know in time! The good news is that your order <span class="font-mono text-slate-800">#{{ order_id }}</span> hasn't entered production yet, so we can still update the design for you.</p><p class="mb-3">Change noted: Original: <span class="font-mono text-slate-800">{{ original_text }}</span> → New: <span class="font-mono text-slate-800">{{ new_text }}</span>.</p><p class="mb-3">Please confirm that everything looks correct, and I will update the file before we begin production!</p><p>Thank you and talk soon,<br/><span class="text-slate-500">{{ shop_name }}</span></p>`,
        footer: '适用：客户要求改字/改字体 · 生产前'
      },
      {
        name: '修改定制内容（生产中）', desc: '解释无法修改，给出折中方案',
        subject: 'Subject: Re: Change request for your order {{ order_id }}',
        previewLabel: '预览 · 生产中无法修改',
        body: `<p class="mb-3">Hi <span class="font-mono text-slate-800">{{ customer_name }}</span>,</p><p class="mb-3">Thank you so much for reaching out! Unfortunately, your order <span class="font-mono text-slate-800">#{{ order_id }}</span> has already entered the engraving stage, which means we're unable to make changes to the design at this point.</p><p class="mb-3">Here's what I can offer: We can complete the current order and offer you a <span class="font-semibold text-slate-800">special discount on a second piece</span> with the corrected text.</p><p class="mb-3">I sincerely apologize for any inconvenience.</p><p>Best regards,<br/><span class="text-slate-500">{{ shop_name }}</span></p>`,
        footer: '适用：客户要求改字 · 已进入生产'
      },
      {
        name: '质量问题退款/重做', desc: '优先解决问题 + 主动承担责任',
        subject: 'Subject: Re: Issue with your order {{ order_id }} — We\'ll make it right',
        previewLabel: '预览 · 质量问题 · 主动承担',
        body: `<p class="mb-3">Hi <span class="font-mono text-slate-800">{{ customer_name }}</span>,</p><p class="mb-3">I'm so sorry to hear about the issue with your order <span class="font-mono text-slate-800">#{{ order_id }}</span>. This is absolutely not the standard we hold ourselves to.</p><p class="mb-3">Could you please send me a photo of the issue? Once I see it, I'll arrange one of the following right away:<br/>A: A full replacement shipped ASAP at no cost<br/>B: A full refund if you'd prefer that instead.</p><p class="mb-3">Please don't worry — I will make sure it's sorted out quickly.</p><p>Sincerely,<br/><span class="text-slate-500">{{ shop_name }}</span></p>`,
        footer: '适用：收到质量投诉 · 必须主动解决'
      }
    ]
  }
]

const currentSec = computed(() => sections[currentSection.value])
const currentTpl = computed(() => currentSec.value.templates[currentTemplate.value] || currentSec.value.templates[0])

function switchTab(i) {
  currentSection.value = i
  currentTemplate.value = 0
}

function selectTemplate(i) {
  currentTemplate.value = i
}

function copyBody() {
  const el = document.querySelector('.email-preview-body')
  const text = el ? el.innerText : currentTpl.value.body.replace(/<[^>]+>/g, '')
  navigator.clipboard.writeText(text).then(() => {
    copied.value = true
    setTimeout(() => { copied.value = false }, 2000)
  })
}
</script>
