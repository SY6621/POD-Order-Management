<template>
  <div class="h-full overflow-auto bg-slate-50 p-4">
    <!-- 页面标题 -->
    <div class="mb-4">
      <h1 class="text-2xl font-bold text-slate-800">待确认订单</h1>
      <p class="text-sm text-slate-500 mt-1">处理客户订单，生成效果图并发送确认邮件</p>
    </div>

    <!-- 【所有Tab共用布局】左侧主区域 + 右侧订单详情 -->
    <div class="flex gap-4">
      <!-- ══ 左侧：订单列表 + 设计器/邮件撰写 ══ -->
      <!-- 待创建Tab时左侧缩小，其他Tab时左侧占满 -->
      <div class="flex-1 space-y-3 min-w-0">
        <!-- 版块1：合并订单表格 -->
        <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
          <div class="px-4 py-3 border-b border-slate-100 flex items-center justify-between">
            <div class="flex items-center gap-3">
              <h2 class="text-base font-bold text-slate-800">订单列表</h2>
              <span class="bg-blue-100 text-blue-600 px-2 py-0.5 rounded-full text-xs font-bold">{{ allOrdersCount }}条</span>
            </div>
            <div class="flex items-center gap-2">
              <span class="text-xs text-slate-400">运营:</span>
              <button class="px-2 py-1 rounded text-xs font-medium" :class="activeAccount === 'all' ? 'bg-blue-600 text-white' : 'bg-white text-slate-600 border border-slate-200'" @click="activeAccount = 'all'">全部</button>
              <button class="px-2 py-1 rounded text-xs font-medium" :class="activeAccount === 'A' ? 'bg-blue-600 text-white' : 'bg-white text-slate-600 border border-slate-200'" @click="activeAccount = 'A'">A运营</button>
              <button class="px-2 py-1 rounded text-xs font-medium" :class="activeAccount === 'B' ? 'bg-blue-600 text-white' : 'bg-white text-slate-600 border border-slate-200'" @click="activeAccount = 'B'">B运营</button>
              <button class="px-2 py-1 rounded text-xs font-medium" :class="activeAccount === 'C' ? 'bg-blue-600 text-white' : 'bg-white text-slate-600 border border-slate-200'" @click="activeAccount = 'C'">C运营</button>
            </div>
          </div>

          <div class="px-4 py-2 border-b border-slate-100 flex items-center gap-3 text-xs">
            <button class="px-3 py-1 rounded-full" :class="orderTab === 'new' ? 'bg-amber-50 text-amber-600 font-medium' : 'text-slate-500'" @click="orderTab = 'new'">新订单 {{ newOrdersCount }}</button>
            <button class="px-3 py-1 rounded-full" :class="orderTab === 'email' ? 'bg-purple-50 text-purple-600 font-medium' : 'text-slate-500'" @click="orderTab = 'email'">邮件撰写 {{ emailOrdersCount }}</button>
            <button class="px-3 py-1 rounded-full" :class="orderTab === 'modify' ? 'bg-pink-50 text-pink-600 font-medium' : 'text-slate-500'" @click="orderTab = 'modify'">客户修改 {{ modifyCount }}</button>
            <button class="px-3 py-1 rounded-full" :class="orderTab === 'pending' ? 'bg-orange-50 text-orange-600 font-medium' : 'text-slate-500'" @click="orderTab = 'pending'">待创建 {{ pendingCount }}</button>
            <button class="px-3 py-1 rounded-full" :class="orderTab === 'all' ? 'bg-blue-50 text-blue-600 font-medium' : 'text-slate-500'" @click="orderTab = 'all'">全部 {{ allOrdersCount }}</button>
          </div>
          
          <div class="overflow-x-auto" style="max-height: 200px;">
            <table class="w-full text-xs text-left">
              <thead class="bg-slate-50 text-slate-500 font-medium border-b border-slate-200 sticky top-0 z-10">
                <tr class="h-[36px]">
                  <th class="px-3 whitespace-nowrap font-medium">店铺</th>
                  <th class="px-3 whitespace-nowrap font-medium">订单ID</th>
                  <th class="px-3 whitespace-nowrap font-medium">客户</th>
                  <th class="px-3 whitespace-nowrap font-medium">国家</th>
                  <th class="px-3 whitespace-nowrap font-medium">产品(SKU)</th>
                  <th class="px-3 whitespace-nowrap font-medium">数量</th>
                  <th class="px-3 whitespace-nowrap font-medium">状态</th>
                  <th class="px-3 whitespace-nowrap font-medium">效果图</th>
                  <th class="px-3 whitespace-nowrap font-medium">操作</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                <tr v-for="order in filteredOrders" :key="order.id" @click="selectOrder(order)" 
                    :class="['hover:bg-slate-50 transition-colors h-[40px] cursor-pointer', selectedOrder?.id === order.id ? 'bg-blue-50' : '']">
                  <td class="px-3 whitespace-nowrap font-mono text-slate-600 text-[11px]">{{ order.shop_code || order.shops?.code || '-' }}</td>
                  <td class="px-3 whitespace-nowrap font-medium text-slate-700">{{ order.etsy_order_id || order.id }}</td>
                  <td class="px-3 whitespace-nowrap text-slate-600">{{ order.customer_name }}</td>
                  <td class="px-3 whitespace-nowrap text-slate-600">{{ order.country || '美国' }}</td>
                  <td class="px-3 whitespace-nowrap font-mono text-slate-500 text-[11px]">{{ order.sku_mapping?.sku_code || order.sku_id || '-' }}</td>
                  <td class="px-3 whitespace-nowrap text-slate-600">{{ order.quantity }}</td>
                  <td class="px-3 whitespace-nowrap">
                    <span v-if="order.status === 'pending' && !order.effect_image_url" class="bg-amber-100 text-amber-600 px-2 py-0.5 rounded text-[10px] font-bold">新订单</span>
                    <span v-else-if="order.status === 'pending' && order.effect_image_url && !order.email_sent" class="bg-purple-100 text-purple-600 px-2 py-0.5 rounded text-[10px] font-bold">邮件撰写</span>
                    <span v-else-if="order.status === 'pending' && order.effect_image_url && order.email_sent" class="bg-orange-100 text-orange-600 px-2 py-0.5 rounded text-[10px] font-bold">待创建</span>
                    <span v-else class="bg-slate-100 text-slate-600 px-2 py-0.5 rounded text-[10px] font-bold">{{ order.status }}</span>
                  </td>
                  <td class="px-3 whitespace-nowrap">
                    <span v-if="order.effect_image_url" class="bg-green-100 text-green-700 px-2 py-0.5 rounded text-[10px] font-bold">已出</span>
                    <span v-else class="bg-slate-100 text-slate-400 px-2 py-0.5 rounded text-[10px] font-bold">空</span>
                  </td>
                  <td class="px-3 whitespace-nowrap">
                    <span v-if="order.status === 'pending' && !order.effect_image_url" class="text-slate-400 text-[10px]">-</span>
                    <div v-else-if="order.status === 'pending' && order.effect_image_url && !order.email_sent" class="flex items-center gap-1">
                      <button @click.stop="rollbackToEdit(order)" class="bg-amber-100 hover:bg-amber-200 text-amber-700 px-2 py-1 rounded text-[10px] transition-colors">回退编辑</button>
                      <button @click.stop="goToEmailTab(order)" class="bg-purple-100 hover:bg-purple-200 text-purple-700 px-2 py-1 rounded text-[10px] transition-colors">写邮件</button>
                    </div>
                    <div v-else-if="order.status === 'pending' && order.effect_image_url && order.email_sent" class="flex items-center gap-1">
                      <button @click.stop="rollbackToEmail(order)" class="bg-purple-100 hover:bg-purple-200 text-purple-700 px-2 py-1 rounded text-[10px] transition-colors">回退邮件</button>
                      <button @click.stop="confirmOrder(order)" class="bg-slate-800 hover:bg-slate-900 text-white px-2 py-1 rounded text-[10px] transition-colors">创建订单</button>
                    </div>
                    <span v-else class="text-slate-400 text-[10px]">-</span>
                  </td>
                </tr>
                <tr v-if="filteredOrders.length === 0" class="h-[60px]">
                  <td colspan="9" class="px-3 text-center text-slate-400 text-sm">暂无订单</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

      <!-- 版剗2：设计器（只在新订单Tab显示） -->
        <div v-if="orderTab === 'new'" class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
          <div class="px-4 py-2 border-b border-slate-100 flex items-center justify-between">
            <div class="flex items-center gap-2">
              <h3 class="font-bold text-slate-800 text-sm">效果图设计器</h3>
              <span class="text-xs text-slate-400">使用本地离线设计器生成正背面效果图</span>
            </div>
            <div class="text-xs text-slate-500" v-if="selectedOrder">当前: {{ selectedOrder.etsy_order_id || selectedOrder.id }}</div>
          </div>
          <div class="bg-slate-50">
            <iframe v-if="designerUrl" ref="designerFrame" :src="designerUrl" class="w-full h-[950px] border-0" @load="onDesignerLoad"></iframe>
            <div v-else class="w-full h-[950px] flex items-center justify-center text-slate-400">设计器加载中...</div>
          </div>
        </div>
      
      <!-- 版剗2：客户修改Tab（静态布局，仅用于预览效果） -->
        <div v-if="orderTab === 'modify'" class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
          <div class="px-4 py-2 border-b border-slate-100 flex items-center justify-between">
            <h3 class="font-bold text-slate-800 text-sm">客户修改</h3>
            <span class="text-xs text-slate-500" v-if="selectedOrder">
              <span class="mr-6">订单ID: <span class="text-red-500 font-medium">{{ selectedOrder.etsy_order_id }}</span></span>
              <span class="mr-6">客户: {{ selectedOrder.customer_name }}</span>
              <span>SKU: {{ selectedOrder.sku_mapping?.sku_code || selectedOrder.sku_id || '-' }}</span>
            </span>
          </div>
          <div class="p-3 bg-slate-50" style="height: 950px; overflow-y: auto;">
            <!-- 客户修改Tab：只显示设计器，邮件内容在右侧订单详情区域 -->
            <div class="h-full flex flex-col gap-3">

              <!-- 效果图设计器 -->
              <div class="bg-white rounded-lg border border-slate-200 flex-1 flex flex-col overflow-hidden">
                <div class="px-3 py-2 border-b border-slate-100 flex items-center justify-between">
                  <div class="flex items-center gap-2 text-xs text-slate-500">
                    <span class="text-base">🎨</span>
                    <span>效果图设计器</span>
                  </div>
                  <span class="text-[10px] text-slate-400">自动加载订单数据</span>
                </div>
                <div class="flex-1 bg-slate-50">
                  <iframe 
                    ref="modifyDesignerFrame" 
                    :src="designerUrl" 
                    class="w-full h-full border-0" 
                    @load="onModifyDesignerLoad"
                  ></iframe>
                </div>
              </div>
            </div>
          </div>
        </div>

   108→      <!-- 版剗2：效果图+邮件预览并排（只在待创建Tab显示，与设计器/邮件撰写同位置） -->
        <div v-if="orderTab === 'pending'" class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
          <div class="px-4 py-2 border-b border-slate-100 flex items-center justify-between">
            <div class="flex items-center gap-2">
              <h3 class="font-bold text-slate-800 text-sm">效果图预览 &amp; 邮件预览</h3>
              <span class="text-xs text-slate-400">已发送邀请邮件，待客户确认</span>
            </div>
            <div class="text-xs text-slate-500" v-if="selectedOrder">当前: {{ selectedOrder.etsy_order_id || selectedOrder.id }}</div>
          </div>
          <div class="p-3">
            <div class="grid grid-cols-2 gap-3">
              <!-- 左：效果图 -->
              <div class="flex flex-col">
                <div class="text-[10px] text-slate-400 mb-1 flex items-center gap-1">
                  <span class="w-4 h-4 bg-slate-100 text-slate-600 rounded flex items-center justify-center text-[9px]">&#128444;</span>
                  效果图
                  <span v-if="selectedOrder?.effect_image_url" class="text-green-500 ml-1">✓ 已确认</span>
                </div>
                <div class="aspect-[4/3] flex items-center justify-center bg-slate-50 rounded-lg border border-slate-200 overflow-hidden">
                  <img v-if="selectedOrder?.effect_image_url" :src="selectedOrder.effect_image_url" class="max-h-full max-w-full object-contain" alt="效果图" @error="$event.target.src=''" />
                  <div v-else class="text-slate-400 text-sm flex flex-col items-center gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="text-slate-300"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg>
                    <span class="text-xs">暂无效果图</span>
                  </div>
                </div>
              </div>
              <!-- 右：邮件预览 -->
              <div class="flex flex-col">
                <div class="text-[10px] text-slate-400 mb-1 flex items-center gap-1">
                  <span class="w-4 h-4 bg-blue-50 text-blue-600 rounded flex items-center justify-center text-[9px]">EN</span>
                  邮件预览
                  <span v-if="pendingEmailContent" class="text-green-500 ml-1">✓ 已生成</span>
                </div>
                <div v-if="pendingEmailContent" class="aspect-[4/3] bg-slate-50 border border-slate-200 rounded-lg p-3 text-xs text-slate-700 leading-relaxed overflow-y-auto whitespace-pre-wrap">
                  {{ getEnglishEmailContent(pendingEmailContent) }}
                </div>
                <div v-else class="aspect-[4/3] flex items-center justify-center text-slate-400 text-xs bg-slate-50 rounded-lg border border-slate-200">
                  选择订单后显示邮件内容
                </div>
              </div>
            </div>
            <!-- 操作按钮行：已移至右侧"发送给客户"面板，此处不再重复显示 -->
          </div>
        </div>

        <!-- 版剗2：邮件撰写区域（只在邮件撰写Tab显示，与设计器同位置） -->
        <div v-if="orderTab === 'email'" class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
          <div class="px-4 py-2 border-b border-slate-100 flex items-center justify-between">
            <div class="flex items-center gap-2">
              <h3 class="font-bold text-slate-800 text-sm">邮件撰写</h3>
              <span class="text-xs text-slate-400">编辑邮件并发送给客户确认</span>
            </div>
            <div class="text-xs text-slate-500" v-if="selectedOrder">当前: {{ selectedOrder.etsy_order_id || selectedOrder.id }}</div>
          </div>
          
          <div class="bg-slate-50 p-3" style="height: 950px; overflow-y: auto;">
            <!-- ═══════════════════════════════════════════════════════════════ -->
            <!-- 红框1：邮件编辑区（最显眼位置，占据主体） -->
            <!-- ═══════════════════════════════════════════════════════════════ -->
            <div class="bg-white rounded-lg border border-slate-200 p-3 mb-3">
              <div class="flex items-center justify-between mb-2">
                <h4 class="text-xs font-medium text-slate-700 flex items-center gap-1">
                  <span class="text-base">📝</span>
                  邮件内容（中英文对照）
                </h4>
                <button @click="translateEmail" :disabled="!emailContentChinese || isTranslating" class="text-xs bg-purple-50 text-purple-600 px-2 py-1 rounded hover:bg-purple-100 disabled:opacity-50 flex items-center gap-1">
                  <svg v-if="isTranslating" class="animate-spin w-3 h-3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m5 8 6 6"/><path d="m4 14 6-6 2-3"/><path d="M2 5h12"/><path d="M7 2h1"/><path d="m22 22-5-10-5 10"/><path d="M14 18h6"/></svg>
                  {{ isTranslating ? '翻译中...' : '翻译' }}
                </button>
              </div>
              
              <!-- 中英文左右对照布局 -->
              <div class="grid grid-cols-2 gap-3">
                <!-- 中文版本 -->
                <div class="flex flex-col">
                  <div class="text-[10px] text-slate-400 mb-1 flex items-center gap-1">
                    <span class="w-4 h-4 bg-red-100 text-red-600 rounded flex items-center justify-center text-[9px] font-bold">中</span>
                    中文
                  </div>
                  <textarea v-model="emailContentChinese" class="flex-1 min-h-[320px] bg-slate-50 border border-slate-200 rounded-lg p-2 text-xs text-slate-600 resize-none focus:outline-none focus:ring-1 focus:ring-blue-500/20 focus:border-blue-500" placeholder="编辑中文邮件内容..."></textarea>
                </div>
                
                <!-- 英文版本 -->
                <div class="flex flex-col">
                  <div class="text-[10px] text-slate-400 mb-1 flex items-center gap-1">
                    <span class="w-4 h-4 bg-blue-100 text-blue-600 rounded flex items-center justify-center text-[9px] font-bold">EN</span>
                    English
                  </div>
                  <textarea v-model="emailContentEnglish" class="flex-1 min-h-[320px] bg-slate-50 border border-slate-200 rounded-lg p-2 text-xs text-slate-600 resize-none focus:outline-none focus:ring-1 focus:ring-blue-500/20 focus:border-blue-500" placeholder="Edit English email content..."></textarea>
                </div>
              </div>
            </div>

            <!-- 客户需求（可折叠） -->
            <div class="bg-white rounded-lg border border-slate-200 p-2 mb-3">
              <div class="flex items-center justify-between cursor-pointer" @click="showCustomerNote = !showCustomerNote">
                <h4 class="text-xs font-medium text-slate-500 flex items-center gap-1">
                  <span>💬</span> 客户需求
                  <span v-if="customerNote" class="text-[10px] text-green-500">（已填写）</span>
                </h4>
                <svg :class="['w-4 h-4 text-slate-400 transition-transform', showCustomerNote ? 'rotate-180' : '']" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m6 9 6 6 6-6"/></svg>
              </div>
              <textarea v-if="showCustomerNote" v-model="customerNote" class="w-full bg-slate-50 border border-slate-200 rounded-lg p-2 text-xs text-slate-600 h-16 resize-none mt-2 focus:outline-none focus:ring-1 focus:ring-blue-500/20 focus:border-blue-500" placeholder="在此粘贴客户的需求..."></textarea>
            </div>

            <!-- ═══════════════════════════════════════════════════════════════ -->
            <!-- 红框2：邮件类型Tab + 场景模板（压缩为紧凑布局） -->
            <!-- ═══════════════════════════════════════════════════════════════ -->
            <div class="bg-white rounded-lg border border-slate-200 p-2 mb-3">
              <!-- 邮件类型Tab（紧凑横排） -->
              <div class="flex items-center gap-2 mb-2">
                <span class="text-xs text-slate-500 shrink-0">类型:</span>
                <div class="flex gap-1 flex-1">
                  <button v-for="option in emailTypeOptions" :key="option.value"
                    :class="['flex items-center gap-1 px-2.5 py-1 rounded text-xs border transition-all',
                      emailType === option.value ? 'bg-blue-50 border-blue-200 text-blue-600 font-medium' : 'bg-white border-slate-200 text-slate-500 hover:border-slate-300']"
                    @click="emailType = option.value; selectedTemplate = null">
                    <span>{{ option.icon }}</span>
                    <span>{{ option.label }}</span>
                  </button>
                </div>
              </div>
              
              <!-- 场景模板（紧凑横排） -->
              <div v-if="currentTemplates.length > 0" class="flex items-center gap-2">
                <span class="text-xs text-slate-500 shrink-0">模板:</span>
                <div class="flex gap-1 flex-1 flex-wrap">
                  <button v-for="template in currentTemplates" :key="template.id"
                    :class="['flex items-center gap-1 px-2.5 py-1 rounded text-xs border transition-all',
                      selectedTemplate?.id === template.id ? 'bg-purple-50 border-purple-200 text-purple-600 font-medium' : 'bg-white border-slate-200 text-slate-500 hover:border-slate-300']"
                    @click="selectedTemplate = template">
                    <span>{{ template.icon }}</span>
                    <span>{{ template.name }}</span>
                  </button>
                </div>
              </div>
            </div>

            <!-- ═══════════════════════════════════════════════════════════════ -->
            <!-- 红框3：风格与落款设置（压缩为紧凑布局 + 保存设置功能） -->
            <!-- ═══════════════════════════════════════════════════════════════ -->
            <div class="bg-white rounded-lg border border-slate-200 p-2 mb-3">
              <div class="flex items-center justify-between mb-2">
                <span class="text-xs text-slate-500">风格设置</span>
                <button @click="saveEmailSettings" class="text-xs text-blue-500 hover:text-blue-600 flex items-center gap-0.5">
                  <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
                  {{ settingsSaved ? '已保存' : '保存设置' }}
                </button>
              </div>
              
              <!-- 第一行：语气 + 长度 -->
              <div class="flex items-center gap-4 mb-2">
                <!-- 语气 -->
                <div class="flex items-center gap-2">
                  <span class="text-xs text-slate-500 shrink-0">语气:</span>
                  <div class="flex gap-0.5">
                    <button v-for="option in toneOptions" :key="option.value"
                      :class="['px-2 py-0.5 rounded text-xs border transition-all',
                        emailTone === option.value ? 'bg-indigo-50 border-indigo-200 text-indigo-600' : 'bg-white border-slate-200 text-slate-500 hover:border-slate-300']"
                      @click="emailTone = option.value">
                      {{ option.icon }} {{ option.label }}
                    </button>
                  </div>
                </div>
                
                <!-- 长度 -->
                <div class="flex items-center gap-2">
                  <span class="text-xs text-slate-500 shrink-0">长度:</span>
                  <div class="flex gap-0.5">
                    <button v-for="option in lengthOptions" :key="option.value"
                      :class="['px-2 py-0.5 rounded text-xs border transition-all',
                        emailLength === option.value ? 'bg-emerald-50 border-emerald-200 text-emerald-600' : 'bg-white border-slate-200 text-slate-500 hover:border-slate-300']"
                      @click="emailLength = option.value">
                      {{ option.icon }} {{ option.label }}
                    </button>
                  </div>
                </div>
              </div>
              
              <!-- 第二行：称呼 + 落款人 -->
              <div class="flex items-center gap-4">
                <!-- 称呼 -->
                <div class="flex items-center gap-2">
                  <span class="text-xs text-slate-500 shrink-0">称呼:</span>
                  <div class="flex gap-0.5">
                    <button v-for="option in greetingOptions" :key="option.value"
                      :class="['px-2 py-0.5 rounded text-xs border transition-all',
                        emailGreeting === option.value ? 'bg-amber-50 border-amber-200 text-amber-600' : 'bg-white border-slate-200 text-slate-500 hover:border-slate-300']"
                      @click="emailGreeting = option.value">
                      {{ option.icon }} {{ option.label }}
                    </button>
                  </div>
                </div>
                
                <!-- 落款人 -->
                <div class="flex items-center gap-2 flex-1">
                  <span class="text-xs text-slate-500 shrink-0">落款:</span>
                  <div class="flex gap-0.5 flex-wrap">
                    <button v-for="name in senderOptions.slice(0, 4)" :key="name"
                      :class="['px-2 py-0.5 rounded text-xs border transition-all',
                        senderName === name ? 'bg-blue-50 border-blue-200 text-blue-600' : 'bg-white border-slate-200 text-slate-500 hover:border-slate-300']"
                      @click="senderName = name">
                      {{ name }}
                    </button>
                  </div>
                  <input v-if="!senderOptions.slice(0, 4).includes(senderName)" 
                    v-model="senderName" 
                    type="text" 
                    class="flex-1 min-w-[80px] bg-slate-50 border border-slate-200 rounded px-2 py-0.5 text-xs text-slate-600 focus:outline-none focus:ring-1 focus:ring-blue-500/20 focus:border-blue-500"
                    placeholder="自定义..." />
                </div>
              </div>
            </div>

            <!-- 操作按钮 -->
            <div class="flex gap-2">
              <button @click="generateEmail" class="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg font-medium text-sm flex items-center justify-center gap-1 shadow-sm transition-all">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/></svg>
                ✨ 生成邮件
              </button>
              <button @click="copyEmail" class="bg-white border border-slate-200 hover:bg-slate-50 text-slate-600 px-4 py-2 rounded-lg font-medium text-sm flex items-center justify-center gap-1 transition-all">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="2"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>
                复制
              </button>
              <button @click="submitEmail" class="flex-1 bg-green-600 hover:bg-green-700 text-white py-2 rounded-lg font-medium text-sm flex items-center justify-center gap-1 shadow-sm transition-all">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2"><path d="M20 6 9 17l-5-5"/></svg>
                ✅ 邮件确认
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧：订单详情 + 发送面板（所有Tab右侧宽度一致） -->
      <div class="w-[320px] shrink-0 space-y-3">
        <!-- 订单详情 -->
        <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
          <div class="px-3 py-2 border-b border-slate-100 bg-slate-50">
            <h3 class="font-bold text-slate-800 text-sm">订单详情</h3>
          </div>
          <div v-if="selectedOrder" class="p-3">
            <!-- 实拍图 -->
            <div class="w-full h-28 bg-slate-100 rounded-lg overflow-hidden mb-2">
              <img v-if="selectedOrder.product_image" :src="selectedOrder.product_image" class="w-full h-full object-contain"/>
              <div v-else class="w-full h-full flex items-center justify-center text-slate-400 text-xs">暂无图片</div>
            </div>
            <!-- 订单信息两列布局 -->
            <div class="grid grid-cols-2 gap-x-3 gap-y-1.5 text-[11px] mb-2">
              <div><span class="text-slate-400">订单ID:</span> <span class="text-red-500 font-medium">{{ selectedOrder.etsy_order_id }}</span></div>
              <div><span class="text-slate-400">国家:</span> <span class="text-slate-700">{{ selectedOrder.country || '美国' }}</span></div>
              <div><span class="text-slate-400">客户:</span> <span class="text-slate-700">{{ selectedOrder.customer_name }}</span></div>
              <div><span class="text-slate-400">颜色:</span> <span class="text-slate-700">{{ selectedOrder.sku_mapping?.color || '古铜金' }}</span></div>
              <div><span class="text-slate-400">形状:</span> <span class="text-slate-700">{{ selectedOrder.sku_mapping?.shape || '圆形' }}</span></div>
              <div><span class="text-slate-400">尺寸:</span> <span class="text-slate-700">{{ selectedOrder.sku_mapping?.size || '30mm' }}</span></div>
            </div>
            <!-- 正背面内容 -->
            <div class="bg-slate-50 rounded-lg p-2 text-[11px] space-y-1">
              <div class="flex items-baseline gap-1">
                <span class="text-slate-400 shrink-0">正面:</span>
                <span class="text-slate-800 font-bold">{{ selectedOrder.front_text || '-' }}</span>
              </div>
              <div class="flex items-baseline gap-1">
                <span class="text-slate-400 shrink-0">字体:</span>
                <span class="text-slate-800 font-bold">{{ selectedOrder.font_code || 'F-04' }}</span>
              </div>
              <div class="flex items-baseline gap-1">
                <span class="text-slate-400 shrink-0">背面:</span>
                <span class="text-slate-800 font-bold">{{ selectedOrder.back_text || '-' }}</span>
              </div>
            </div>
          </div>
          <div v-else class="p-3 text-center text-sm text-slate-400">请在左侧选择订单</div>
        </div>

        <!-- 效果图展示框（邮件撰写Tab和待创建Tab显示） -->
        <div v-if="(orderTab === 'email' || orderTab === 'pending') && selectedOrder?.effect_image_url" class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
          <div class="px-3 py-2 border-b border-slate-100 bg-slate-50 flex items-center justify-between">
            <h3 class="font-bold text-slate-800 text-sm">效果图</h3>
            <span class="text-[10px] text-green-500 flex items-center gap-0.5">
              <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 6 9 17l-5-5"/></svg>
              已生成
            </span>
          </div>
          <div class="p-2">
            <div class="w-full rounded-lg overflow-hidden border border-slate-100 bg-slate-50">
              <img :src="selectedOrder.effect_image_url" class="w-full object-contain max-h-[220px]" alt="效果图" @error="(e) => console.error('效果图URL加载失败:', selectedOrder.effect_image_url)" />
            </div>
          </div>
        </div>

        <!-- 客户修改Tab专用：邮件/修改/回复面板 -->
        <div v-if="orderTab === 'modify' && selectedOrder" class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
          <div class="px-3 py-2 border-b border-slate-100 bg-slate-50">
            <h3 class="font-bold text-slate-800 text-sm">📧 邮件与回复</h3>
          </div>
          <div class="p-3 space-y-3 text-[11px]">
            <!-- 上次发送的邮件 -->
            <div class="border border-slate-200 rounded-lg p-2">
              <div class="flex items-center justify-between mb-1">
                <span class="text-slate-500 font-medium">上次发送的邮件</span>
                <span class="text-[10px] text-slate-400">只读</span>
              </div>
              <div class="bg-slate-50 border border-slate-200 rounded p-2 h-24 overflow-y-auto whitespace-pre-wrap text-slate-700">
Hi {{ selectedOrder?.customer_name?.split(' ')[0] || 'there' }}!

Here is the preview of your custom pet tag (Version 1).
Please check the name, phone number and layout.

Best,
Customer Support Team
              </div>
            </div>

            <!-- 上次发送的效果图 -->
            <div class="border border-slate-200 rounded-lg p-2">
              <div class="w-full aspect-[4/3] rounded bg-slate-100 border border-dashed border-slate-200 flex items-center justify-center overflow-hidden">
                <img v-if="selectedOrder?.effect_image_url" :src="selectedOrder.effect_image_url" class="w-full h-full object-contain" />
                <span v-else class="text-[10px] text-slate-400">效果图预览</span>
              </div>
            </div>

            <!-- 客户修改要求 -->
            <div class="border border-slate-200 rounded-lg p-2">
              <div class="flex items-center justify-between mb-1">
                <span class="text-slate-500 font-medium flex items-center gap-1">
                  <span>💬</span> 客户修改要求
                </span>
                <span class="text-[10px] text-green-500">StorePortal</span>
              </div>
              <div class="bg-slate-50 border border-slate-200 rounded p-2 min-h-[60px] text-slate-700 whitespace-pre-wrap">
1. 正面文字由 "Kyla" 改为 "Luna"
2. 背面电话替换为 "+61 4xx xxx xxx"
3. 其它保持不变
              </div>
            </div>

            <!-- 邮件/信息回复 -->
            <div class="border border-slate-200 rounded-lg p-2">
              <div class="flex items-center justify-between mb-1">
                <span class="text-slate-500 font-medium flex items-center gap-1">
                  <span>✉️</span> 回复
                </span>
                <button 
                  @click="generateReplyEmail"
                  class="px-2 py-0.5 rounded text-[10px] font-medium bg-blue-800 text-white hover:bg-blue-900 transition-colors"
                >
                  ✨ AI生成
                </button>
              </div>
              <textarea 
                v-model="replyContent" 
                class="w-full bg-slate-50 border border-slate-200 rounded p-2 min-h-[160px] text-[11px] text-slate-700 resize-none focus:outline-none focus:ring-1 focus:ring-blue-500/20 focus:border-blue-500"
                placeholder="在此输入回复内容..."
              ></textarea>
              <div class="flex items-center justify-between text-[10px] mt-1">
                <span class="text-slate-400">收件人: {{ selectedOrder?.customer_name?.split(' ')[0] || 'Customer' }}</span>
                <div class="flex items-center gap-1">
                  <span class="text-slate-400">落款:</span>
                  <select 
                    v-model="replySenderName" 
                    class="bg-slate-50 border border-slate-200 rounded px-1 py-0.5 text-[10px] text-slate-700"
                  >
                    <option v-for="name in senderOptions" :key="name" :value="name">{{ name }}</option>
                  </select>
                </div>
              </div>
            </div>

            <!-- 历史记录 -->
            <div class="border border-slate-200 rounded-lg">
              <button class="w-full px-2 py-1.5 flex items-center justify-between text-[11px] text-slate-500" @click="showHistory = !showHistory">
                <span class="flex items-center gap-1">
                  <span>📜</span> 历史记录
                </span>
                <svg :class="['w-3 h-3 transition-transform', showHistory ? 'rotate-180' : '']" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m6 9 6 6 6-6"/></svg>
              </button>
              <div v-if="showHistory" class="px-2 pb-2 max-h-32 overflow-y-auto text-[10px] text-slate-600 space-y-1">
                <div>2026-03-24 10:15 · 系统邮件 V1</div>
                <div>2026-03-24 23:01 · 客户修改：请把名字改成 LUNA</div>
              </div>
            </div>

            <!-- 操作按钮 -->
            <div class="flex gap-2 pt-2">
              <button class="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg font-medium text-[11px] shadow-sm">保存草稿</button>
              <button class="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white py-2 rounded-lg font-medium text-[11px] shadow-sm">标记已处理</button>
            </div>
          </div>
        </div>

          <!-- 发送给客户操作面板（待创建Tab显示） -->
          <div v-if="orderTab === 'pending' && selectedOrder" class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
            <div class="px-3 py-2 border-b border-slate-100 bg-slate-50">
              <h3 class="font-bold text-slate-800 text-sm">🚀 发送给客户</h3>
            </div>
            <div class="p-3 space-y-3">
              <p class="text-xs text-slate-500">请复制效果图和邮件内容，通过Etsy后台发送给客户确认。</p>
              
              <!-- 操作按钮 -->
              <div class="flex gap-2">
                <button @click="copyShareLink" class="flex-1 bg-white border border-slate-200 hover:bg-slate-50 text-slate-600 py-2.5 rounded-lg text-xs flex items-center justify-center gap-1 transition-all">
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>
                  🔗 复制链接
                </button>
                <button @click="copyEmailContent" class="flex-1 bg-white border border-slate-200 hover:bg-slate-50 text-slate-600 py-2.5 rounded-lg text-xs flex items-center justify-center gap-1 transition-all">
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>
                  📋 复制邮件
                </button>
              </div>
              <button @click="goToShipping" class="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-medium text-sm flex items-center justify-center gap-2 shadow-sm transition-all">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H9"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.624l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/></svg>
                物流下单 →
              </button>
            </div>
          </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useOrderStore } from '../../stores/orderStore'

const router = useRouter()
const store = useOrderStore()
const designerFrame = ref(null)
const designerUrl = ref('/designer-standalone.html')
const modifyDesignerFrame = ref(null)
const modifyDesignerUrl = ref('') // 客户修改Tab的设计器URL（懒加载）
const activeAccount = ref('all')
const orderTab = ref('new')
const selectedOrder = ref(null)
const customerNote = ref('')
const selectedStyle = ref('natural')
const emailContent = ref('')
const emailContentChinese = ref('')
const emailContentEnglish = ref('')
const confirmedEmailContent = ref('') // 点击"邮件确认"后才显示在右侧栏
const pendingEmailContent = ref('') // 待创建Tab的邮件预览内容（从 email_logs 加载）
const isTranslating = ref(false)
const showCustomerNote = ref(false) // 客户需求折叠状态
const settingsSaved = ref(false) // 设置保存状态
const showHistory = ref(false) // 客户修改Tab：历史记录折叠状态
const replyContent = ref('') // 客户修改Tab：邮件/信息回复内容
const replySenderName = ref('Customer Support Team') // 客户修改Tab：回复邮件落款人

// 邮件风格控制（新增）
const emailTone = ref('casual') // 语气：formal(正式) / casual(随和) / lively(活泼)
const emailLength = ref('standard') // 长度：short(简短) / standard(标准) / detailed(详细)
const emailGreeting = ref('hi') // 称呼：dear(亲爱的) / hi(嗨) / hey(嘿)

// 风格选项定义
const toneOptions = [
  { value: 'formal', label: '正式', desc: '商务专业', icon: '👔' },
  { value: 'casual', label: '随和', desc: '自然友好', icon: '😊' },
  { value: 'lively', label: '活泼', desc: '轻松有趣', icon: '🎉' }
]

const lengthOptions = [
  { value: 'short', label: '简短', desc: '50字以内', icon: '📝' },
  { value: 'standard', label: '标准', desc: '100字左右', icon: '📄' },
  { value: 'detailed', label: '详细', desc: '200字以上', icon: '📚' }
]

const greetingOptions = [
  { value: 'dear', label: 'Dear', desc: '正式礼貌', icon: '💼' },
  { value: 'hi', label: 'Hi', desc: '友好自然', icon: '👋' },
  { value: 'hey', label: 'Hey', desc: '轻松亲近', icon: '✌️' }
]

// 导入邮件模板
import emailTemplates from '../../config/email-templates.json'

// 邮件撰写功能增强
const emailType = ref('first_confirm') // 邮件类型：first_confirm | modification | follow_up
const senderName = ref('Customer Support Team') // 落款人
const confirmationDeadline = ref('') // 确认截止时间
const selectedTemplate = ref(null) // 选中的场景模板

// 邮件类型选项
const emailTypeOptions = [
  { value: 'first_confirm', label: '首封确认', desc: '订单收到后的首次确认', icon: '📧' },
  { value: 'modification', label: '修改确认', desc: '客户要求修改后的确认', icon: '✏️' },
  { value: 'follow_up', label: '追评邮件', desc: '发货后的售后跟进', icon: '⭐' }
]

// 当前邮件类型的模板列表
const currentTemplates = computed(() => {
  return emailTemplates[emailType.value]?.templates || []
})

// 预设落款人选项
const senderOptions = [
  'Customer Support Team',
  'Pet Tag Studio',
  'Sarah',
  'Emily',
  'Custom...'
]

onMounted(async () => {
  await store.getPendingOrders()
  // 调试输出
  console.log('🔍 OrdersPending 页面数据:', {
    storeOrders: store.orders.length,
    allOrders: allOrders.value.length,
    filteredOrders: filteredOrders.value.length,
    firstOrder: store.orders[0]?.etsy_order_id || '无'
  })
  
  // 加载保存的邮件设置
  loadEmailSettings()

  // 将 confirmDesign 挂载到 window，供设计器 iframe 调用
  window.confirmDesign = confirmDesign

  // 监听设计器 iframe 发来的 confirmDesign 消息（备用通道）
  window.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'confirmDesign') {
      confirmDesign()
    }
  })
})

// 加载邮件设置
const loadEmailSettings = () => {
  try {
    const savedSettings = localStorage.getItem('emailSettings')
    if (savedSettings) {
      const settings = JSON.parse(savedSettings)
      emailTone.value = settings.tone || 'casual'
      emailLength.value = settings.length || 'standard'
      emailGreeting.value = settings.greeting || 'hi'
      senderName.value = settings.senderName || 'Customer Support Team'
      emailType.value = settings.emailType || 'first_confirm'
      console.log('✅ 已加载保存的邮件设置')
    }
  } catch (e) {
    console.warn('加载邮件设置失败:', e)
  }
}

// 保存邮件设置
const saveEmailSettings = () => {
  try {
    const settings = {
      tone: emailTone.value,
      length: emailLength.value,
      greeting: emailGreeting.value,
      senderName: senderName.value,
      emailType: emailType.value
    }
    localStorage.setItem('emailSettings', JSON.stringify(settings))
    settingsSaved.value = true
    setTimeout(() => { settingsSaved.value = false }, 2000)
    console.log('✅ 邮件设置已保存')
  } catch (e) {
    console.error('保存邮件设置失败:', e)
  }
}

// 监听 Tab 切换，自动选择第一个订单
watch(orderTab, (newTab) => {
  if (newTab === 'new' && filteredOrders.value.length > 0) {
    // 切换到新订单 Tab 时，自动选择第一个订单
    const firstNewOrder = filteredOrders.value[0]
    if (firstNewOrder) {
      selectOrder(firstNewOrder)
      console.log('📌 自动选择新订单:', firstNewOrder.etsy_order_id)
    }
  } else if (newTab === 'email' && filteredOrders.value.length > 0) {
    // 切换到邮件撰写 Tab 时，自动选择第一个有效果图但未发送邮件的订单
    const firstEmailOrder = filteredOrders.value[0]
    if (firstEmailOrder) {
      selectOrder(firstEmailOrder)
      console.log('📌 自动选择邮件撰写订单:', firstEmailOrder.etsy_order_id)
    }
    // 自动选择第一个模板（标准确认）
    if (currentTemplates.value.length > 0) {
      selectedTemplate.value = currentTemplates.value[0]
      console.log('📌 自动选择模板:', selectedTemplate.value.name)
    }
  } else if (newTab === 'pending' && filteredOrders.value.length > 0) {
    // 切换到待创建 Tab 时，自动选择第一个订单
    const firstPendingOrder = filteredOrders.value[0]
    if (firstPendingOrder) {
      selectOrder(firstPendingOrder)
      console.log('📌 自动选择待创建订单:', firstPendingOrder.etsy_order_id)
    }
  }
})

const allOrders = computed(() => {
  const filtered = store.orders.filter(o => ['new', 'pending'].includes(o.status))
  console.log('🔍 allOrders 计算:', store.orders.length, '->', filtered.length)
  return filtered
})

const filteredOrders = computed(() => {
  let orders = allOrders.value
  
  // 按运营筛选
  if (activeAccount.value !== 'all') {
    orders = orders.filter(o => o.operator === activeAccount.value || o.shops?.operator === activeAccount.value)
  }
  
  // 按状态标签筛选
  // 新订单：无效果图的 pending 订单
  // 邮件撰写：有效果图的 pending 订单（等待发送邮件）
  // 待创建：有效果图且已发送邮件的 pending 订单
  if (orderTab.value === 'new') {
    orders = orders.filter(o => o.status === 'pending' && !o.effect_image_url)
  } else if (orderTab.value === 'email') {
    orders = orders.filter(o => o.status === 'pending' && o.effect_image_url && !o.email_sent)
  } else if (orderTab.value === 'pending') {
    orders = orders.filter(o => o.status === 'pending' && o.effect_image_url && o.email_sent)
  }
  
  return orders
})

const allOrdersCount = computed(() => {
  let orders = allOrders.value
  if (activeAccount.value !== 'all') {
    orders = orders.filter(o => o.operator === activeAccount.value || o.shops?.operator === activeAccount.value)
  }
  return orders.length
})
const newOrdersCount = computed(() => {
  let orders = allOrders.value.filter(o => o.status === 'pending' && !o.effect_image_url)
  if (activeAccount.value !== 'all') {
    orders = orders.filter(o => o.operator === activeAccount.value || o.shops?.operator === activeAccount.value)
  }
  return orders.length
})
const emailOrdersCount = computed(() => {
  let orders = allOrders.value.filter(o => o.status === 'pending' && o.effect_image_url && !o.email_sent)
  console.log('📧 邮件撰写Tab筛选:', {
    总数: allOrders.value.length,
    满足条件: orders.length,
    详情: allOrders.value.map(o => ({
      id: o.etsy_order_id,
      status: o.status,
      has_effect: !!o.effect_image_url,
      email_sent: o.email_sent
    }))
  })
  if (activeAccount.value !== 'all') {
    orders = orders.filter(o => o.operator === activeAccount.value || o.shops?.operator === activeAccount.value)
  }
  return orders.length
})
const modifyCount = computed(() => {
  let orders = allOrders.value.filter(o => o.status === 'pending' && o.effect_image_url && o.email_sent && o.email_status === 'needs_change')
  if (activeAccount.value !== 'all') {
    orders = orders.filter(o => o.operator === activeAccount.value || o.shops?.operator === activeAccount.value)
  }
  return orders.length
})
const pendingCount = computed(() => {
  let orders = allOrders.value.filter(o => o.status === 'pending' && o.effect_image_url && o.email_sent)
  if (activeAccount.value !== 'all') {
    orders = orders.filter(o => o.operator === activeAccount.value || o.shops?.operator === activeAccount.value)
  }
  return orders.length
})

const selectOrder = async (order) => {
  console.log('👉 selectOrder:', {
    id: order.etsy_order_id,
    effect_image_url: order.effect_image_url || '无'
  })
  selectedOrder.value = order
  // 选择新订单时清空已确认的邮件内容
  confirmedEmailContent.value = ''
  pendingEmailContent.value = ''
  
  // 如果在待创建Tab，加载该订单的邮件内容
  if (orderTab.value === 'pending' && order.email_sent) {
    try {
      const emailLog = await store.getEmailLogByOrderId(order.id)
      if (emailLog && emailLog.content) {
        pendingEmailContent.value = emailLog.content
        console.log('✅ 已加载邮件内容')
      }
    } catch (e) {
      console.warn('加载邮件内容失败:', e)
    }
  }
  
  if (designerFrame.value && designerFrame.value.contentWindow) {
    // 从 sku_mapping 获取 shape 和 color
    const shapeMap = { '心形': 'heart', '圆形': 'circle', '骨头形': 'bone' }
    const colorMap = { '金色': 'Gold', '银色': 'Silver', '玫瑰金': 'RoseGold', '黑色': 'Black' }
    
    const shape = shapeMap[order.sku_mapping?.shape] || 'heart'
    const color = colorMap[order.sku_mapping?.color] || 'Silver'
    
    // 尺寸：映射为 L / S（供设计器保存SVG时画标注线）
    const rawSize = order.sku_mapping?.size || order.product_size || ''
    const sizeMap = { '大': 'L', 'L': 'L', 'Large': 'L', 'LARGE': 'L', '小': 'S', 'S': 'S', 'Small': 'S', 'SMALL': 'S' }
    const size = sizeMap[rawSize] || 'L'
    
    // 解析背面文字：如果包含空格，分离文字和电话
    let backText = order.back_text || ''
    let phone = ''
    if (backText.includes(' ')) {
      const parts = backText.split(' ')
      backText = parts[0]
      phone = parts.slice(1).join(' ')
    }
    
    designerFrame.value.contentWindow.postMessage({
      type: 'loadOrder',
      data: {
        frontText: order.front_text || '',
        backText: backText,
        phone: phone,
        shape: shape,
        color: color,
        font: order.font_code || 'F-04',
        size: size
      }
    }, '*')
    
    console.log('📤 发送订单数据到设计器:', {
      orderId: order.etsy_order_id,
      shape: shape,
      color: color,
      size: size,
      frontText: order.front_text,
      backText: backText,
      phone: phone
    })
  }
}

const onDesignerLoad = () => {
  if (selectedOrder.value && designerFrame.value) {
    selectOrder(selectedOrder.value)
  }
}

const saveEffectImage = () => {
  return new Promise((resolve, reject) => {
    if (!selectedOrder.value || !designerFrame.value) {
      reject(new Error('请先选择一条订单'))
      return
    }
    
    // 获取设计器生成的SVG数据
    const handleMessage = async (event) => {
      if (event.data && event.data.type === 'svgData') {
        window.removeEventListener('message', handleMessage)
        
        try {
          // 保存效果图，获取返回的URL
          const result = await store.saveEffectImage(selectedOrder.value.id, event.data.svgData)
          
          // 更新本地订单数据（使用返回的URL）
          selectedOrder.value.effect_image_url = result.url
          
          alert('✅ 效果图已保存')
          resolve()
        } catch (e) {
          alert('❌ 保存失败：' + e.message)
          reject(e)
        }
      }
    }
    window.addEventListener('message', handleMessage)
    designerFrame.value.contentWindow.postMessage({ type: 'getSVG' }, '*')
  })
}

const moveToPending = async (order) => {
  if (!confirm(`确认将新订单 ${order.etsy_order_id || order.id} 转为待确认？`)) return
  try {
    await store.updateOrderStatus(order.id, 'pending')
    alert('✅ 已转为待确认订单')
  } catch (e) {
    alert('❌ 操作失败：' + e.message)
  }
}

const confirmOrder = async (order) => {
  if (!confirm(`确认将订单 ${order.etsy_order_id || order.id} 改为生产中？`)) return
  try {
    await store.updateOrderStatus(order.id, 'producing')
    selectedOrder.value = null
    alert('✅ 订单已转入生产中！')
  } catch (e) {
    alert('❌ 操作失败：' + e.message)
  }
}

const rollbackToEdit = async (order) => {
  if (!confirm(`确认将订单 ${order.etsy_order_id || order.id} 回退到编辑状态？\n此操作会清空效果图数据，订单将回到"新订单"Tab。`)) return
  try {
    await store.clearEffectImage(order.id)
    selectedOrder.value = null
    alert('✅ 订单已回退到编辑状态！')
  } catch (e) {
    alert('❌ 操作失败：' + e.message)
  }
}

const confirmDesign = async () => {
  if (!selectedOrder.value) {
    alert('请先选择一条订单')
    return
  }
  
  const currentOrderId = selectedOrder.value.id
  console.log('📌 confirmDesign 开始, 订单ID:', currentOrderId)
  
  try {
    // 保存效果图（等待完成）
    await saveEffectImage()
    console.log('✅ 效果图保存完成')
    
    // 刷新订单列表，确保数据同步
    await store.getPendingOrders()
    console.log('✅ 订单列表已刷新, 总数:', store.orders.length)
    
    // 查找更新后的订单
    const savedOrder = store.orders.find(o => o.id === currentOrderId)
    console.log('🔍 查找订单:', savedOrder ? {
      id: savedOrder.id,
      status: savedOrder.status,
      effect_image_url: savedOrder.effect_image_url,  // 显示完整URL
      email_sent: savedOrder.email_sent
    } : '未找到')
    
    if (savedOrder) {
      // 先选中订单
      selectedOrder.value = savedOrder
    }
    
    // 跳转到邮件撰写Tab
    orderTab.value = 'email'
    
    alert('✅ 设计稿已确认，请编写邮件发送给客户确认')
  } catch (e) {
    console.error('❌ confirmDesign 失败:', e)
    alert('❌ 操作失败：' + e.message)
  }
}

const goToEmailTab = (order) => {
  selectOrder(order)
  orderTab.value = 'email'
}

const rollbackToEmail = async (order) => {
  if (!confirm(`确认将订单 ${order.etsy_order_id || order.id} 回退到邮件撰写状态？\n此操作会标记邮件为未发送，订单将回到"邮件撰写"Tab。`)) return
  try {
    await store.updateEmailSentStatus(order.id, false)
    selectedOrder.value = null
    alert('✅ 订单已回退到邮件撰写状态！')
  } catch (e) {
    alert('❌ 操作失败：' + e.message)
  }
}

const initials = computed(() => {
  const name = selectedOrder.value?.customer_name || 'M'
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
})

const generateEmail = () => {
  if (!selectedOrder.value) {
    alert('请先选择一条订单')
    return
  }
  if (!selectedTemplate.value) {
    alert('请先选择一个场景模板')
    return
  }
  
  const order = selectedOrder.value
  const firstName = order.customer_name?.split(' ')[0] || 'there'
  const orderId = order.etsy_order_id || order.id
  const effectImageUrl = order.effect_image_url || ''
  
  // 计算24小时截止时间
  const now = new Date()
  const deadline = new Date(now.getTime() + 24 * 60 * 60 * 1000)
  const deadlineStr = deadline.toLocaleString('en-US', { 
    month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit', timeZoneName: 'short' 
  })
  confirmationDeadline.value = deadlineStr
  
  // 获取模板内容
  const tone = emailTone.value
  const length = emailLength.value
  const templateContent = selectedTemplate.value.content[tone]?.[length]
  
  if (!templateContent) {
    alert('模板内容不存在，请检查模板配置')
    return
  }
  
  // 替换变量
  const replaceVars = (text) => {
    return text
      .replace(/\{firstName\}/g, firstName)
      .replace(/\{orderId\}/g, orderId)
      .replace(/\{effectImageUrl\}/g, effectImageUrl)
      .replace(/\{senderName\}/g, senderName.value)
      .replace(/\{confirmationDeadline\}/g, deadlineStr)
  }
  
  // 根据称呼类型调整开头
  const greetingMap = {
    dear: { en: `Dear ${firstName},`, zh: `${firstName}您好，` },
    hi: { en: `Hi ${firstName}!`, zh: `嗨 ${firstName}！` },
    hey: { en: `Hey ${firstName} 👋`, zh: `嘿 ${firstName}～` }
  }
  
  // 落款映射
  const signMap = {
    formal: { en: `Best regards,\n${senderName.value}`, zh: `此致\n${senderName.value}` },
    casual: { en: `Best,\n${senderName.value}`, zh: `祝好，\n${senderName.value}` },
    lively: { en: `Cheers! 🎉\n${senderName.value}`, zh: `加油！🎉\n${senderName.value}` }
  }
  
  const greeting = greetingMap[emailGreeting.value]
  const sign = signMap[tone]
  
  // 生成邮件内容
  emailContentEnglish.value = `${greeting.en}\n\n${replaceVars(templateContent.en)}\n\n${sign.en}`
  emailContentChinese.value = `${greeting.zh}\n\n${replaceVars(templateContent.zh)}\n\n${customerNote.value ? `\n备注：${customerNote.value}\n` : ''}${sign.zh}`
  emailContent.value = emailContentEnglish.value
}

const translateEmail = async () => {
  if (!emailContentChinese.value) {
    alert('请先生成中文邮件内容')
    return
  }
  
  isTranslating.value = true
  try {
    // 调用后端翻译API
    const response = await fetch('http://localhost:8000/api/translate/email', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        chinese_content: emailContentChinese.value
      })
    })
    
    const result = await response.json()
    
    if (result.success) {
      emailContentEnglish.value = result.data.english_content
      emailContent.value = result.data.english_content
      alert('✅ 翻译成功！英文内容已更新')
    } else {
      alert('❌ 翻译失败：' + result.message)
    }
  } catch (e) {
    alert('❌ 翻译失败：' + e.message)
  } finally {
    isTranslating.value = false
  }
}

const copyEmail = async () => {
  if (!emailContentChinese.value && !emailContentEnglish.value) {
    alert('请先点击「生成邮件」')
    return
  }
  try {
    const fullContent = `=== 中文版本 Chinese Version ===\n\n${emailContentChinese.value}\n\n=== English Version ===\n\n${emailContentEnglish.value}`
    await navigator.clipboard.writeText(fullContent)
    alert('✅ 中英文邮件内容已复制到剪贴板！')
  } catch (e) {
    alert('复制失败，请手动复制')
  }
}

const submitEmail = async () => {
  if (!emailContentChinese.value && !emailContentEnglish.value) {
    alert('请先点击「生成邮件」')
    return
  }
  if (!selectedOrder.value) {
    alert('请先选择订单')
    return
  }
  try {
    // 合并中英文内容
    const fullContent = `=== 中文版本 Chinese Version ===\n\n${emailContentChinese.value}\n\n=== English Version ===\n\n${emailContentEnglish.value}`
    
    // 邮件类型标签映射
    const emailTypeLabels = {
      'first_confirm': '首封确认邮件',
      'modification': '修改确认邮件',
      'follow_up': '追评邮件'
    }
    
    // 1. 保存邮件记录到 email_logs 表
    await store.saveEmailLog({
      order_id: selectedOrder.value.id,
      email_type: emailType.value,
      subject: `【${emailTypeLabels[emailType.value]}】Your Custom ${selectedOrder.value.sku_mapping?.product_name || 'Product'} - ${selectedOrder.value.etsy_order_id}`,
      content: fullContent,
      effect_image_url: selectedOrder.value.effect_image_url,
      sender_name: senderName.value,
      confirmation_deadline: emailType.value === 'first_confirm' ? confirmationDeadline.value : null
    })
    
    // 2. 更新订单状态为已发送邮件
    await store.updateEmailSentStatus(selectedOrder.value.id, true)
    
    // 3. 设置已确认的邮件内容（显示在右侧“确认邮件”栏）
    confirmedEmailContent.value = emailContentEnglish.value
    
    // 4. 清空邮件内容
    emailContentChinese.value = ''
    emailContentEnglish.value = ''
    emailContent.value = ''
    customerNote.value = ''
    
    // 5. 刷新订单列表
    await store.getPendingOrders()
    
    // 6. 跳转到待创建Tab，并选中当前订单
    orderTab.value = 'pending'
    const updatedOrder = store.orders.find(o => o.id === selectedOrder.value.id)
    if (updatedOrder) {
      selectedOrder.value = updatedOrder
    }
    // 7. 设置待创建Tab的邮件预览内容（流转时直接使用已保存的内容）
    pendingEmailContent.value = fullContent
    
    alert('✅ 邮件已保存，订单已流转到待创建状态！')
  } catch (e) {
    alert('❌ 邮件保存失败：' + e.message)
  }
}

// 提取邮件中的英文版本（去除中文版本和多余空行）
const getEnglishEmailContent = (content) => {
  if (!content) return ''
  
  // 提取英文版本：取 === English Version === 之后的内容
  const englishMarker = '=== English Version ==='
  const parts = content.split(englishMarker)
  const englishOnly = parts.length > 1 ? parts[1] : content
  
  // 去除多余的空行（保留最多两个连续换行）
  return englishOnly
    .replace(/\n{3,}/g, '\n\n')  // 将3个或更多换行符替换为2个
    .trim()
}

// 复制分享链接（效果图+邮件）
const copyShareLink = async () => {
  if (!selectedOrder.value) {
    alert('请先选择订单')
    return
  }
  try {
    // 生成分享链接（包含效果图和订单ID）
    const shareUrl = `${window.location.origin}/share/order/${selectedOrder.value.id}`
    await navigator.clipboard.writeText(shareUrl)
    alert('✅ 分享链接已复制！\n客服可通过此链接查看效果图和邮件内容')
  } catch (e) {
    alert('复制失败，请手动复制')
  }
}

// 复制邮件内容（用于客服粘贴到Etsy）
const copyEmailContent = async () => {
  if (!selectedOrder.value) {
    alert('请先选择订单')
    return
  }
  try {
    // 从etsy订单中获取已保存的邮件内容
    const emailLog = await store.getEmailLogByOrderId(selectedOrder.value.id)
    if (emailLog && emailLog.content) {
      await navigator.clipboard.writeText(emailLog.content)
      alert('✅ 邮件内容已复制！\n客服可粘贴到Etsy后台发送给客户')
    } else {
      alert('暂无邮件内容，请先生成邮件')
    }
  } catch (e) {
    alert('复制失败：' + e.message)
  }
}

// 确认发送给客户（订单进入生产流程）
const confirmSendToCustomer = async () => {
  if (!selectedOrder.value) {
    alert('请先选择订单')
    return
  }
  if (!confirm(`确认将订单 ${selectedOrder.value.etsy_order_id} 转入生产流程？\n\n请确保已通过Etsy将效果图和邮件发送给客户。`)) return
  
  try {
    // 更新订单状态为生产中
    await store.updateOrderStatus(selectedOrder.value.id, 'producing')
    selectedOrder.value = null
    alert('✅ 订单已转入生产中！')
  } catch (e) {
    alert('❌ 操作失败：' + e.message)
  }
}

// 前往物流下单页面
const goToShipping = () => {
  if (!selectedOrder.value) {
    alert('请先选择订单')
    return
  }
  // 带上订单ID跳转到物流下单页面
  router.push({
    path: '/admin/shipping',
    query: { orderId: selectedOrder.value.id }
  })
}

// 客户修改Tab：加载设计器
const loadDesignToModifyTab = () => {
  modifyDesignerUrl.value = '/designer-standalone.html'
  console.log('📌 客户修改Tab：开始加载设计器')
}

// 客户修改Tab：设计器加载完成
const onModifyDesignerLoad = () => {
  if (selectedOrder.value && modifyDesignerFrame.value) {
    // 从 sku_mapping 获取 shape 和 color
    const shapeMap = { '心形': 'heart', '圆形': 'circle', '骨头形': 'bone' }
    const colorMap = { '金色': 'Gold', '银色': 'Silver', '玫瑰金': 'RoseGold', '黑色': 'Black' }
    
    const shape = shapeMap[selectedOrder.value.sku_mapping?.shape] || 'heart'
    const color = colorMap[selectedOrder.value.sku_mapping?.color] || 'Silver'
    
    // 尺寸：映射为 L / S
    const rawSize = selectedOrder.value.sku_mapping?.size || selectedOrder.value.product_size || ''
    const sizeMap = { '大': 'L', 'L': 'L', 'Large': 'L', 'LARGE': 'L', '小': 'S', 'S': 'S', 'Small': 'S', 'SMALL': 'S' }
    const size = sizeMap[rawSize] || 'L'
    
    // 解析背面文字
    let backText = selectedOrder.value.back_text || ''
    let phone = ''
    if (backText.includes(' ')) {
      const parts = backText.split(' ')
      backText = parts[0]
      phone = parts.slice(1).join(' ')
    }
    
    modifyDesignerFrame.value.contentWindow.postMessage({
      type: 'loadOrder',
      data: {
        frontText: selectedOrder.value.front_text || '',
        backText: backText,
        phone: phone,
        shape: shape,
        color: color,
        font: selectedOrder.value.font_code || 'F-04',
        size: size
      }
    }, '*')
    
    console.log('📤 客户修改Tab：发送订单数据到设计器:', {
      orderId: selectedOrder.value.etsy_order_id,
      shape, color, size,
      frontText: selectedOrder.value.front_text,
      backText, phone
    })
  }
}

// 客户修改Tab：AI生成回复邮件（占位函数）
const generateReplyEmail = () => {
  if (!selectedOrder.value) {
    alert('请先选择订单')
    return
  }
  
  const customerName = selectedOrder.value.customer_name?.split(' ')[0] || 'there'
  const sender = replySenderName.value
  
  // 简单的模板回复（后期接入AI）
  const template = `Hi ${customerName}!

Thank you for your feedback. We have updated the design according to your requirements:

✅ Front text changed to: "${selectedOrder.value.front_text || 'Luna'}"
✅ Back phone number updated

Please check the new preview below and let us know if everything looks good!

Best regards,
${sender}`
  
  replyContent.value = template
  console.log('✨ AI生成回复邮件完成')
}
</script>
