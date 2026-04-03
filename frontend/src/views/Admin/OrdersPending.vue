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
      <div class="w-[65%] space-y-3 min-w-0">
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
            <button class="px-3 py-1 rounded-full" :class="orderTab === 'new' ? 'bg-amber-50 text-amber-600 font-medium' : 'text-slate-500'" @click="orderTab = 'new'">待处理 {{ newCount }}</button>
            <button class="px-3 py-1 rounded-full" :class="orderTab === 'waiting' ? 'bg-purple-50 text-purple-600 font-medium' : 'text-slate-500'" @click="orderTab = 'waiting'">待回复 {{ waitingCount }}</button>
            <button class="px-3 py-1 rounded-full" :class="orderTab === 'pending' ? 'bg-orange-50 text-orange-600 font-medium' : 'text-slate-500'" @click="orderTab = 'pending'">待创建 {{ pendingCreateCount }}</button>
            <button class="px-3 py-1 rounded-full" :class="orderTab === 'all' ? 'bg-blue-50 text-blue-600 font-medium' : 'text-slate-500'" @click="orderTab = 'all'">全部 {{ allCount }}</button>
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
                  <th class="px-3 whitespace-nowrap font-medium min-w-[180px]">操作</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                <tr v-for="order in filteredOrders" :key="order.id" @click="selectOrder(order)" 
                    :class="['hover:bg-slate-50 transition-colors h-[40px] cursor-pointer', selectedOrder?.id === order.id ? 'bg-blue-50' : '']">
                  <td class="px-3 whitespace-nowrap font-mono text-slate-600 text-[11px]">{{ order.shops?.name || order.shops?.code || order.shop_code || '-' }}</td>
                  <td class="px-3 whitespace-nowrap font-medium text-slate-700">{{ order.etsy_order_id || order.id }}</td>
                  <td class="px-3 whitespace-nowrap text-slate-600">{{ order.customer_name }}</td>
                  <td class="px-3 whitespace-nowrap text-slate-600">{{ order.shipping_country || order.country || '-' }}</td>
                  <td class="px-3 whitespace-nowrap font-mono text-slate-500 text-[11px]">{{ order.sku_mapping?.sku_code || order.sku_id || '-' }}</td>
                  <td class="px-3 whitespace-nowrap text-slate-600">{{ order.quantity }}</td>
                  <td class="px-3 whitespace-nowrap">
                    <span v-if="order.status === '新订单'" class="bg-amber-100 text-amber-600 px-2 py-0.5 rounded text-[10px] font-bold">待处理</span>
                    <span v-else-if="order.status === '客户修改'" class="bg-orange-100 text-orange-700 px-2 py-0.5 rounded text-[10px] font-bold">客户修改</span>
                    <span v-else-if="order.status === '待回复'" class="bg-blue-100 text-blue-700 px-2 py-0.5 rounded text-[10px] font-bold">待回复</span>
                    <span v-else-if="order.status === '待创建'" class="bg-green-100 text-green-700 px-2 py-0.5 rounded text-[10px] font-bold">待创建</span>
                    <span v-else class="bg-slate-100 text-slate-600 px-2 py-0.5 rounded text-[10px] font-bold">{{ order.status }}</span>
                  </td>
                  <td class="px-3 whitespace-nowrap">
                    <el-tag v-if="order.effect_image_url" type="success" size="small" class="text-[10px]">已生成</el-tag>
                    <el-tag v-else type="info" size="small" class="text-[10px]">未生成</el-tag>
                  </td>
                  <td class="px-3 whitespace-nowrap">
                    <div class="flex items-center gap-1">
                      <!-- 待处理状态：生成效果图 -->
                      <template v-if="order.status === '新订单' || order.status === '客户修改'">
                        <el-button size="small" type="primary" link @click.stop="selectOrder(order); orderTab = 'new'">生成效果图</el-button>
                        <el-button size="small" type="default" link @click.stop="selectOrder(order)">详情</el-button>
                      </template>
                      <!-- 待回复状态：重发邮件 + 客户已确认 + 回退 -->
                      <template v-else-if="order.status === '待回复'">
                        <el-button size="small" type="primary" link @click.stop="selectOrder(order)">重发邮件</el-button>
                        <el-button size="small" type="success" link @click.stop="confirmByCustomer(order)">客户已确认</el-button>
                        <el-button size="small" type="warning" link @click.stop="revertToPending(order)">回退</el-button>
                      </template>
                      <!-- 待创建状态：创建物流单 + 退回待处理 -->
                      <template v-else-if="order.status === '待创建'">
                        <el-button size="small" type="success" link @click.stop="goToShipping(order)">创建物流单</el-button>
                        <el-button size="small" type="warning" link @click.stop="revertToEffectSent(order)">回退</el-button>
                      </template>
                      <!-- 其他状态 -->
                      <template v-else>
                        <el-button size="small" type="default" link @click.stop="selectOrder(order)">详情</el-button>
                      </template>
                    </div>
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
            <div class="text-xs text-slate-500" v-if="selectedOrder">
              订单 <span class="font-bold text-slate-700">{{ selectedOrder.etsy_order_id || selectedOrder.id }}</span>
              <span v-if="selectedOrder.customer_name" class="text-slate-400"> - {{ selectedOrder.customer_name }}</span>
            </div>
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
                  <img v-if="selectedOrder?.effect_image_url" :src="selectedOrder.effect_image_url" class="max-w-[300px] max-h-[300px] object-contain" alt="效果图" @error="$event.target.src=''" />
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
                    <button v-for="name in senderOptions" :key="name"
                      :class="['px-2 py-0.5 rounded text-xs border transition-all',
                        senderName === name ? 'bg-blue-50 border-blue-200 text-blue-600' : 'bg-white border-slate-200 text-slate-500 hover:border-slate-300']"
                      @click="senderName = name">
                      {{ name }}
                    </button>
                  </div>
                  <input v-if="!senderOptions.includes(senderName)"
                    v-model="senderName" 
                    type="text" 
                    class="flex-1 min-w-[80px] bg-slate-50 border border-slate-200 rounded px-2 py-0.5 text-xs text-slate-600 focus:outline-none focus:ring-1 focus:ring-blue-500/20 focus:border-blue-500"
                    placeholder="自定义..." />
                </div>
              </div>
            </div>

            <!-- 操作按钮 -->
            <div class="flex gap-2">
              <button @click="generateEmail" :disabled="isGeneratingEmail" class="flex-1 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white py-2 rounded-lg font-medium text-sm flex items-center justify-center gap-1 shadow-sm transition-all">
                <svg v-if="!isGeneratingEmail" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/></svg>
                <svg v-else class="animate-spin w-4 h-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                {{ isGeneratingEmail ? '生成中...' : '✨ 生成邮件' }}
              </button>
              <button @click="copyEmail" class="bg-white border border-slate-200 hover:bg-slate-50 text-slate-600 px-4 py-2 rounded-lg font-medium text-sm flex items-center justify-center gap-1 transition-all">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="2"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>
                复制
              </button>
              <button @click="clearEmailContent" class="bg-white border border-slate-200 hover:bg-slate-50 text-slate-600 px-4 py-2 rounded-lg font-medium text-sm flex items-center justify-center gap-1 transition-all">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="2"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/></svg>
                清除
              </button>
              <button @click="submitEmail" :disabled="isSendingEmail" class="flex-1 bg-green-600 hover:bg-green-700 disabled:bg-green-400 text-white py-2 rounded-lg font-medium text-sm flex items-center justify-center gap-1 shadow-sm transition-all">
                <svg v-if="!isSendingEmail" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2"><path d="M20 6 9 17l-5-5"/></svg>
                <svg v-else class="animate-spin w-4 h-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                {{ isSendingEmail ? '发送中...' : '确认并发送' }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧：订单详情 + 发送面板（所有Tab右侧宽度一致） -->
      <div class="w-[35%] shrink-0 space-y-3 min-w-[280px]">
        <!-- 订单详情 -->
        <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
          <div class="px-3 py-2 border-b border-slate-100 bg-slate-50">
            <h3 class="font-bold text-slate-800 text-sm">订单详情</h3>
          </div>
          <div v-if="selectedOrder" class="p-2">
            <!-- 图片左 + 信息右 横排布局 -->
            <div class="flex gap-3">
              <!-- 左：实拍图 -->
              <div class="w-28 h-28 shrink-0 bg-slate-100 rounded-lg overflow-hidden">
                <img v-if="selectedOrder.product_image" :src="selectedOrder.product_image" class="w-full h-full object-contain"/>
                <div v-else class="w-full h-full flex items-center justify-center text-slate-400 text-xs">暂无图片</div>
              </div>
              <!-- 右：订单信息 两列 -->
              <div class="flex-1 min-w-0">
                <div class="grid grid-cols-2 gap-x-2 gap-y-0.5">
                  <div><span class="text-[11px] text-slate-400">订单ID:</span> <span class="text-xs text-red-500 font-medium">{{ selectedOrder.etsy_order_id }}</span></div>
                  <div><span class="text-[11px] text-slate-400">尺寸:</span> <span class="text-xs text-slate-700">{{ selectedOrder.sku_mapping?.size || '30mm' }}</span></div>
                  <div><span class="text-[11px] text-slate-400">客户:</span> <span class="text-xs text-slate-700">{{ selectedOrder.customer_name }}</span></div>
                  <div><span class="text-[11px] text-slate-400">正面:</span> <span class="text-xs text-slate-800 font-bold">{{ selectedOrder.front_text || '-' }}</span></div>
                  <div><span class="text-[11px] text-slate-400">国家:</span> <span class="text-xs text-slate-700">{{ selectedOrder.shipping_country || selectedOrder.country || '-' }}</span></div>
                  <div><span class="text-[11px] text-slate-400">字体:</span> <span class="text-xs text-slate-800 font-bold">{{ selectedOrder.font_code || 'F-04' }}</span></div>
                  <div><span class="text-[11px] text-slate-400">形状:</span> <span class="text-xs text-slate-700">{{ selectedOrder.sku_mapping?.shape || '圆形' }}</span></div>
                  <div><span class="text-[11px] text-slate-400">背面:</span> <span class="text-xs text-slate-800 font-bold">{{ selectedOrder.back_text || '-' }}</span></div>
                  <div><span class="text-[11px] text-slate-400">颜色:</span> <span class="text-xs text-slate-700">{{ selectedOrder.sku_mapping?.color || '古铜金' }}</span></div>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="p-3 text-center text-sm text-slate-400">请在左侧选择订单</div>
        </div>

        <!-- 红框4：首封邮件区域 -->
        <div v-if="orderTab === 'new' && selectedOrder" class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
          <!-- 头部 -->
          <div class="px-3 py-2 border-b border-slate-100 flex items-center justify-between">
            <h3 class="text-sm font-semibold text-slate-700 flex items-center gap-1">
              <span>📧</span> 首封邮件
            </h3>
          </div>

          <div class="p-3 space-y-3">
            <!-- 模板 + 落款 选择行 -->
            <div class="flex items-center gap-3 text-xs">
              <div class="flex items-center gap-1">
                <span class="text-slate-500">模板:</span>
                <select v-model="templateSelectValue" class="border border-slate-200 rounded px-2 py-1 text-xs bg-white">
                  <option v-for="tpl in firstEmailTemplateOptions" :key="tpl.key" :value="tpl.key">{{ tpl.name }}</option>
                  <option value="__custom__">自定义...</option>
                </select>
                <input v-if="templateSelectValue === '__custom__'" v-model="customTemplateName" type="text" class="border border-slate-200 rounded px-2 py-1 text-xs bg-white w-20" placeholder="模板名" />
              </div>
              <div class="flex items-center gap-1">
                <span class="text-slate-500">落款:</span>
                <select v-model="senderSelectValue" class="border border-slate-200 rounded px-2 py-1 text-xs bg-white">
                  <option value="Sophia">Sophia</option>
                  <option value="Customer Support Team">Customer Support Team</option>
                  <option value="Pet Tag Studio">Pet Tag Studio</option>
                  <option value="__custom__">自定义...</option>
                </select>
                <input v-if="senderSelectValue === '__custom__'" v-model="customSenderName" @input="firstEmailSender = customSenderName" type="text" class="border border-slate-200 rounded px-2 py-1 text-xs bg-white w-24" placeholder="输入落款名" />
              </div>
            </div>

            <!-- 邮件预览框 -->
            <div class="bg-slate-50 border border-slate-200 rounded-lg p-3 text-xs text-slate-700 leading-relaxed max-h-[300px] overflow-y-auto whitespace-pre-wrap">
              {{ firstEmailPreview }}
            </div>

            <!-- 编辑模板折叠区 -->
            <div class="border-t border-slate-100 mt-2 pt-2">
              <button @click="showTemplateEditor = !showTemplateEditor" class="flex items-center gap-1 text-xs text-slate-500 hover:text-slate-700">
                <span>✏️ 编辑模板</span>
                <span class="text-[10px]">{{ showTemplateEditor ? '▲' : '▼' }}</span>
              </button>
              <div v-if="showTemplateEditor" class="mt-2 space-y-2">
                <textarea v-model="templateEditContent" rows="14" class="w-full text-xs border border-slate-200 rounded-lg p-2 resize-y focus:outline-none focus:ring-1 focus:ring-blue-300" placeholder="编辑模板内容..."></textarea>
                <button @click="saveTemplate" class="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-medium">
                  💾 保存模板
                </button>
              </div>
            </div>

            <!-- 操作按钮 -->
            <div class="flex gap-2">
              <button @click="copyFirstEmail" class="flex-1 flex items-center justify-center gap-1 px-3 py-1.5 border border-slate-300 text-slate-600 rounded-lg hover:bg-slate-50 text-xs">
                📋 复制
              </button>
              <!-- 两步确认：确认效果图按钮 -->
              <button 
                v-if="!isEffectConfirmed"
                @click="confirmEffect"
                class="flex-1 flex items-center justify-center gap-1 px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-medium">
                ✓ 确认效果图
              </button>
              <button 
                v-else
                disabled
                class="flex-1 flex items-center justify-center gap-1 px-3 py-1.5 bg-gray-200 text-gray-500 cursor-not-allowed rounded-lg text-xs font-medium">
                ✅ 效果图已确认
              </button>
              <!-- 确认并发送按钮 -->
              <button 
                @click="sendFirstEmail"
                :disabled="!canSendFirstEmail || isSendingFirstEmail"
                :class="canSendFirstEmail && !isSendingFirstEmail
                  ? 'bg-green-600 hover:bg-green-700 text-white' 
                  : 'bg-gray-300 text-gray-500 cursor-not-allowed'"
                class="flex-1 flex items-center justify-center gap-1 px-3 py-1.5 rounded-lg text-xs font-medium">
                <span v-if="isSendingFirstEmail">发送中...</span>
                <span v-else>📤 传送效果图/邮件</span>
              </button>
            </div>
          </div>
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
                {{ modifyLastEmail || '暂无邮件记录' }}
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
                <span class="text-[10px] text-green-500">ServiceLink</span>
              </div>
              <div class="bg-slate-50 border border-slate-200 rounded p-2 min-h-[60px] text-slate-700 whitespace-pre-wrap">
                {{ modifyCustomerRequest || '暂无客户修改要求记录' }}
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
                  <span>📜</span> 历史记录 ({{ modifyOrderLogs.length }})
                </span>
                <svg :class="['w-3 h-3 transition-transform', showHistory ? 'rotate-180' : '']" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m6 9 6 6 6-6"/></svg>
              </button>
              <div v-if="showHistory" class="px-2 pb-2 max-h-32 overflow-y-auto text-[10px] text-slate-600 space-y-1">
                <div v-for="log in modifyOrderLogs" :key="log.id" class="py-0.5 border-b border-slate-100 last:border-0">
                  <span class="text-slate-400">{{ formatLogTime(log.sent_at) }}</span> · 
                  <span class="text-slate-700">{{ log.email_type === 'first_confirm' ? '首封确认' : log.email_type === 'modification' ? '修改确认' : '追评邮件' }}</span>
                </div>
                <div v-if="modifyOrderLogs.length === 0" class="text-slate-400 text-center py-1">暂无历史记录</div>
              </div>
            </div>

            <!-- 操作按钮 -->
            <div class="flex gap-2 pt-2">
              <button @click="saveModifyDraft" class="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg font-medium text-[11px] shadow-sm transition-colors">保存草稿</button>
              <button @click="markModifyHandled" class="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white py-2 rounded-lg font-medium text-[11px] shadow-sm transition-colors">标记已处理</button>
            </div>
          </div>
        </div>

          <!-- Tab2: 待回复 - 邮件状态与操作面板 -->
          <div v-if="orderTab === 'waiting' && selectedOrder" class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
            <div class="px-3 py-2 border-b border-slate-100 bg-slate-50">
              <h3 class="font-bold text-slate-800 text-sm">📧 已发送邮件</h3>
            </div>
            <div class="p-3 space-y-3">
              <!-- 邮件状态信息 -->
              <div class="space-y-1 text-xs">
                <div class="flex items-center justify-between">
                  <span class="text-slate-500">发送时间:</span>
                  <span class="text-slate-700">{{ formatDate(selectedOrder.email_sent_at || selectedOrder.updated_at) }}</span>
                </div>
                <div class="flex items-center justify-between">
                  <span class="text-slate-500">等待天数:</span>
                  <span :class="daysSince(selectedOrder.email_sent_at || selectedOrder.updated_at) > 3 ? 'text-red-600 font-bold' : 'text-slate-700'">
                    {{ daysSince(selectedOrder.email_sent_at || selectedOrder.updated_at) }} 天
                    <span v-if="daysSince(selectedOrder.email_sent_at || selectedOrder.updated_at) > 3" class="text-[10px] ml-1">⚠️ 超时</span>
                  </span>
                </div>
              </div>

              <!-- 操作按钮 -->
              <div class="flex gap-2 pt-2 border-t border-slate-100">
                <button @click="markCustomerConfirmed" class="flex-1 bg-green-600 hover:bg-green-700 text-white py-2 rounded-lg text-xs font-medium flex items-center justify-center gap-1 transition-all">
                  ✅ 客户已确认
                </button>
                <button @click="markCustomerModify" class="flex-1 bg-orange-500 hover:bg-orange-600 text-white py-2 rounded-lg text-xs font-medium flex items-center justify-center gap-1 transition-all">
                  ✏️ 客户要修改
                </button>
              </div>
              <button @click="resendEmail" :disabled="isResendingEmail" class="w-full bg-purple-600 hover:bg-purple-700 disabled:bg-purple-400 text-white py-2 rounded-lg text-xs font-medium flex items-center justify-center gap-1 transition-all">
                <span v-if="isResendingEmail">发送中...</span>
                <span v-else>📧 重发邮件</span>
              </button>
            </div>
          </div>

          <!-- Tab3: 待创建 - 操作面板 -->
          <div v-if="orderTab === 'pending' && selectedOrder" class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
            <div class="px-3 py-2 border-b border-slate-100 bg-slate-50">
              <h3 class="font-bold text-slate-800 text-sm">📦 准备下单</h3>
            </div>
            <div class="p-3 space-y-3">
              <p class="text-xs text-slate-500">客户已确认效果图，现在可以创建物流单。</p>
              
              <!-- 操作按钮 -->
              <div class="flex gap-2">
                <button @click="goToShipping" class="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2.5 rounded-lg text-xs font-medium flex items-center justify-center gap-1 transition-all">
                  📦 创建物流单
                </button>
                <button @click="returnToPendingFromTab3" class="flex-1 border border-slate-300 text-slate-600 rounded-lg hover:bg-slate-50 py-2.5 text-xs font-medium flex items-center justify-center gap-1 transition-all">
                  ↩️ 退回待处理
                </button>
              </div>
            </div>
          </div>

          <!-- Tab4: 全部 - 根据订单状态动态显示操作面板 -->
          <div v-if="orderTab === 'all' && selectedOrder" class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
            <div class="px-3 py-2 border-b border-slate-100 bg-slate-50">
              <h3 class="font-bold text-slate-800 text-sm">⚡ 快捷操作</h3>
            </div>
            <div class="p-3 space-y-3">
              <!-- 待处理/客户修改：显示去生成效果图 -->
              <template v-if="selectedOrder.status === '新订单' || selectedOrder.status === '客户修改'">
                <p class="text-xs text-slate-500">
                  <span v-if="selectedOrder.status === '客户修改'">客户要求修改，请重新生成效果图。</span>
                  <span v-else>此订单需要生成效果图并发送首封确认邮件。</span>
                </p>
                <div class="flex gap-2">
                  <button @click="orderTab = 'new'; selectOrder(selectedOrder)" class="flex-1 bg-amber-600 hover:bg-amber-700 text-white py-2 rounded-lg text-xs font-medium transition-all">
                    🎨 去生成效果图
                  </button>
                </div>
              </template>

              <!-- 待回复：显示客户已确认/客户要修改 -->
              <template v-else-if="selectedOrder.status === '待回复'">
                <div class="space-y-1 text-xs mb-2">
                  <div class="flex items-center justify-between">
                    <span class="text-slate-500">等待天数:</span>
                    <span :class="daysSince(selectedOrder.email_sent_at || selectedOrder.updated_at) > 3 ? 'text-red-600 font-bold' : 'text-slate-700'">
                      {{ daysSince(selectedOrder.email_sent_at || selectedOrder.updated_at) }} 天
                    </span>
                  </div>
                </div>
                <div class="flex gap-2">
                  <button @click="markCustomerConfirmed" class="flex-1 bg-green-600 hover:bg-green-700 text-white py-2 rounded-lg text-xs font-medium transition-all">
                    ✅ 客户已确认
                  </button>
                  <button @click="markCustomerModify" class="flex-1 bg-orange-500 hover:bg-orange-600 text-white py-2 rounded-lg text-xs font-medium transition-all">
                    ✏️ 客户要修改
                  </button>
                </div>
                <button @click="resendEmail" :disabled="isResendingEmail" class="w-full bg-purple-600 hover:bg-purple-700 disabled:bg-purple-400 text-white py-2 rounded-lg text-xs transition-all">
                  {{ isResendingEmail ? '发送中...' : '📧 重发邮件' }}
                </button>
              </template>

              <!-- 待创建：显示创建物流单/退回待处理 -->
              <template v-else-if="selectedOrder.status === '待创建'">
                <p class="text-xs text-slate-500">客户已确认，可以创建物流单。</p>
                <div class="flex gap-2">
                  <button @click="goToShipping" class="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg text-xs font-medium transition-all">
                    📦 创建物流单
                  </button>
                  <button @click="returnToPendingFromTab3" class="flex-1 border border-slate-300 text-slate-600 rounded-lg hover:bg-slate-50 py-2 text-xs font-medium transition-all">
                    ↩️ 退回待处理
                  </button>
                </div>
              </template>

              <!-- 其他状态 -->
              <template v-else>
                <p class="text-xs text-slate-400">当前状态暂无可用操作</p>
              </template>
            </div>
          </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useOrderStore } from '../../stores/orderStore'
import { sendConfirmationEmail } from '../../utils/api.js'
import { ElMessage, ElMessageBox } from 'element-plus'
import supabase from '../../utils/supabase'

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
const isGeneratingEmail = ref(false) // AI邮件生成loading状态
const showCustomerNote = ref(true) // 客户需求折叠状态
const settingsSaved = ref(false) // 设置保存状态
const showHistory = ref(false) // 客户修改Tab：历史记录折叠状态
const replyContent = ref('') // 客户修改Tab：邮件/信息回复内容
const replySenderName = ref('Customer Support Team') // 客户修改Tab：回复邮件落款人
const modifyOrderLogs = ref([]) // 客户修改Tab：订单的邮件历史记录
const modifyCustomerRequest = ref('') // 客户修改Tab：客户的修改要求
const modifyLastEmail = ref('') // 客户修改Tab：上次发送的邮件内容

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

// 邮件模板数据（从API加载）
const emailTemplatesData = ref({})
const isTemplatesLoading = ref(false)

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

// 当前邮件类型的模板列表（从API加载的数据）
const currentTemplates = computed(() => {
  return emailTemplatesData.value[emailType.value] || []
})

// 加载邮件模板（从后端API）
const loadEmailTemplates = async () => {
  isTemplatesLoading.value = true
  try {
    const apiBase = import.meta.env.VITE_API_BASE || 'http://localhost:8000'
    const response = await fetch(`${apiBase}/api/email-templates`)
    const result = await response.json()
    
    if (result.success && result.data) {
      emailTemplatesData.value = result.data
      console.log('✅ 邮件模板加载成功:', Object.keys(result.data).map(k => `${k}(${result.data[k].length}个)`).join(', '))
    } else {
      console.error('❌ 邮件模板加载失败:', result.message)
      emailTemplatesData.value = {}
    }
  } catch (e) {
    console.error('❌ 邮件模板加载异常:', e.message)
    emailTemplatesData.value = {}
  } finally {
    isTemplatesLoading.value = false
  }
}

// 预设落款人选项
const senderOptions = [
  'Customer Support Team',
  'Pet Tag Studio',
  'Sophia'
]

// ===== 首封邮件区域 =====
const firstEmailTemplate = ref('standard')
const firstEmailSender = ref('Sophia')
const senderSelectValue = ref('Sophia')
const customSenderName = ref('')
const templateSelectValue = ref('standard')
const customTemplateName = ref('')
const isSendingFirstEmail = ref(false)

// 落款下拉联动
watch(senderSelectValue, (val) => {
  if (val !== '__custom__') {
    firstEmailSender.value = val
  } else {
    firstEmailSender.value = customSenderName.value || 'Sophia'
  }
})

// 模板下拉联动
watch(templateSelectValue, (val) => {
  if (val !== '__custom__') {
    firstEmailTemplate.value = val
  }
  // 自定义时保持当前模板内容，用户可在编辑区修改
})

// 硬编码默认模板（如果API读不到就用这些）- 使用reactive使其响应式
const defaultFirstEmailTemplates = reactive({
  standard: {
    name: '标准确认',
    key: 'standard',
    content: `Hi {firstName},\n\nThank you so much for your order!\nI've finished your design proof for the custom heart pet ID tag.\nPlease kindly check and confirm the details within 24 hours if you need any changes.\nIf I don't hear from you within 24 hours, I will proceed with production as requested to avoid delay.\nThank you for your support!\n\nBest regards,\n{senderName}`
  },
  urgent: {
    name: '加急确认',
    key: 'urgent',
    content: `Hi {firstName},\n\nThank you for your order!\nYour design proof is ready. Since this is a rush order, please review and confirm within 12 hours so we can start production right away.\nIf I don't hear back within 12 hours, I'll proceed as requested.\nThank you!\n\nBest regards,\n{senderName}`
  },
  custom: {
    name: '定制需求确认',
    key: 'custom',
    content: `Hi {firstName},\n\nThank you so much for your order!\nI've carefully prepared your custom design based on your special requirements. Please take a moment to review everything, especially the personalization details.\nPlease confirm within 24 hours if everything looks good, or let me know if you'd like any changes.\nLooking forward to hearing from you!\n\nBest regards,\n{senderName}`
  }
})

// 模板编辑相关
const showTemplateEditor = ref(false)
const templateEditContent = ref('')

// 从localStorage加载自定义模板
const loadCustomTemplates = () => {
  try {
    const saved = localStorage.getItem('firstEmailCustomTemplates')
    if (saved) {
      const parsed = JSON.parse(saved)
      // 合并到 defaultFirstEmailTemplates 中
      Object.keys(parsed).forEach(key => {
        if (defaultFirstEmailTemplates[key]) {
          defaultFirstEmailTemplates[key].content = parsed[key]
        }
      })
    }
  } catch (e) {
    console.warn('加载自定义模板失败:', e)
  }
}

// 保存模板到localStorage
const saveTemplate = () => {
  const key = firstEmailTemplate.value
  if (!key) return
  
  // 更新运行时数据
  if (defaultFirstEmailTemplates[key]) {
    defaultFirstEmailTemplates[key].content = templateEditContent.value
  }
  
  // 持久化到localStorage
  try {
    const saved = JSON.parse(localStorage.getItem('firstEmailCustomTemplates') || '{}')
    saved[key] = templateEditContent.value
    localStorage.setItem('firstEmailCustomTemplates', JSON.stringify(saved))
    ElMessage.success('模板已保存')
  } catch (e) {
    ElMessage.error('保存失败')
  }
}

// 切换模板时，同步编辑区内容
watch(firstEmailTemplate, (newVal) => {
  const tpl = defaultFirstEmailTemplates[newVal]
  templateEditContent.value = tpl ? tpl.content : ''
})

// 展开编辑器时，同步当前模板内容
watch(showTemplateEditor, (isOpen) => {
  if (isOpen) {
    const tpl = defaultFirstEmailTemplates[firstEmailTemplate.value]
    templateEditContent.value = tpl ? tpl.content : ''
  }
})

// 模板选项列表
const firstEmailTemplateOptions = computed(() => {
  // 先尝试从已加载的emailTemplatesData中读取first_confirm类型
  const apiTemplates = emailTemplatesData.value?.first_confirm
  if (apiTemplates && apiTemplates.length > 0) {
    return apiTemplates.map(t => ({ key: t.template_key, name: t.name }))
  }
  // fallback到硬编码
  return Object.values(defaultFirstEmailTemplates)
})

// 邮件预览（计算属性）— 直接使用本地硬编码模板，不走API
const firstEmailPreview = computed(() => {
  const order = selectedOrder.value
  const firstName = order ? (order.customer_name || '').split(' ')[0] || 'Customer' : 'Customer'
  const sender = firstEmailSender.value

  // 直接从硬编码模板读取（API旧数据不可靠）
  const defaultTpl = defaultFirstEmailTemplates[firstEmailTemplate.value]
  const templateText = defaultTpl ? defaultTpl.content : ''

  // 替换变量
  return templateText
    .replace(/\{firstName\}/g, firstName)
    .replace(/\{senderName\}/g, sender)
})

// 复制邮件内容
const copyFirstEmail = async () => {
  if (!firstEmailPreview.value) return
  try {
    await navigator.clipboard.writeText(firstEmailPreview.value)
    ElMessage.success('邮件内容已复制到剪贴板')
  } catch (err) {
    // fallback
    const textarea = document.createElement('textarea')
    textarea.value = firstEmailPreview.value
    document.body.appendChild(textarea)
    textarea.select()
    document.execCommand('copy')
    document.body.removeChild(textarea)
    ElMessage.success('邮件内容已复制到剪贴板')
  }
}

// 确认并发送
const sendFirstEmail = async () => {
  if (!canSendFirstEmail.value || !selectedOrder.value) {
    if (!selectedOrder.value) {
      ElMessage.warning('请先选择一条订单')
    } else if (!isEffectConfirmed.value) {
      ElMessage.warning('请先确认效果图')
    }
    return
  }

  isSendingFirstEmail.value = true
  try {
    // 1. 保存邮件记录到 email_logs 表
    await store.saveEmailLog({
      order_id: selectedOrder.value.id,
      email_type: 'first_confirm',
      subject: `Your Custom Pet Tag Design Preview - Order #${selectedOrder.value.etsy_order_id || selectedOrder.value.id}`,
      content: firstEmailPreview.value,
      effect_image_url: selectedOrder.value.effect_image_url || '',
      sender_name: firstEmailSender.value
    })

    // 2. 更新订单状态为"待回复"
    const { error } = await supabase
      .from('orders')
      .update({ 
        status: '待回复',
        email_sent: true,
        email_sent_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      })
      .eq('id', selectedOrder.value.id)
    
    if (error) throw error

    // 3. 刷新订单列表
    await store.getPendingOrders()

    // 4. 清空选中 + 重置确认状态
    selectedOrder.value = null
    isEffectConfirmed.value = false

    ElMessage.success('已发送，订单已移至"待回复"')
  } catch (err) {
    console.error('发送失败:', err)
    ElMessage.error('发送失败：' + (err.message || '未知错误'))
  } finally {
    isSendingFirstEmail.value = false
  }
}

onMounted(async () => {
  await store.getPendingOrders()
  // 加载邮件模板
  await loadEmailTemplates()
  // 调试输出
  console.log('🔍 OrdersPending 页面数据:', {
    storeOrders: store.orders.length,
    allOrders: allOrders.value.length,
    filteredOrders: filteredOrders.value.length,
    firstOrder: store.orders[0]?.etsy_order_id || '无'
  })
  
  // 加载保存的邮件设置
  loadEmailSettings()
  
  // 加载自定义邮件模板
  loadCustomTemplates()
  // 初始化编辑区内容
  templateEditContent.value = defaultFirstEmailTemplates[firstEmailTemplate.value]?.content || ''

  // 将 confirmDesign 挂载到 window，供设计器 iframe 调用
  window.confirmDesign = confirmDesign

  // 监听设计器 iframe 发来的 confirmDesign 消息（备用通道）
  window.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'confirmDesign') {
      confirmDesign()
    }
    // 监听设计器参数变化消息，自动撤销效果图确认
    if (event.data && event.data.type === 'paramChanged') {
      if (isEffectConfirmed.value) {
        isEffectConfirmed.value = false
        // 通知 iframe 恢复按钮状态
        const iframe = document.querySelector('iframe')
        if (iframe && iframe.contentWindow) {
          iframe.contentWindow.postMessage({ type: 'resetEffectConfirm' }, '*')
        }
        console.log('⚠️ 设计器参数已变化，效果图确认已自动撤销')
      }
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

// 格式化日志时间
const formatLogTime = (timestamp) => {
  if (!timestamp) return '-'
  const date = new Date(timestamp)
  return date.toLocaleString('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 格式化日期
const formatDate = (timestamp) => {
  if (!timestamp) return '-'
  const date = new Date(timestamp)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 等待天数计算
const waitingDays = computed(() => {
  if (!selectedOrder.value?.updated_at) return 0
  const diff = Date.now() - new Date(selectedOrder.value.updated_at).getTime()
  return Math.floor(diff / (1000 * 60 * 60 * 24))
})

// ===== 两步确认逻辑 =====
const isEffectConfirmed = ref(false) // 效果图确认状态

// 效果图确认方法
const confirmEffect = () => {
  if (!selectedOrder.value) return
  if (!selectedOrder.value.effect_image_url) {
    ElMessage.warning('请先生成效果图')
    return
  }
  isEffectConfirmed.value = true
  ElMessage.success('效果图已确认')
}

// 计算是否可以发送首封邮件
const canSendFirstEmail = computed(() => {
  return isEffectConfirmed.value && firstEmailPreview.value && firstEmailPreview.value.trim() !== ''
})

// 选中订单切换时重置确认状态
watch(selectedOrder, () => {
  isEffectConfirmed.value = false
})

// 重发邮件loading状态
const isResendingEmail = ref(false)

// Tab2 "待回复"：客户已确认 → 移到待创建
const markCustomerConfirmed = async () => {
  if (!selectedOrder.value) return
  try {
    const { error } = await supabase
      .from('orders').update({ status: '待创建' }).eq('id', selectedOrder.value.id)
    if (error) throw error
    await store.getPendingOrders()
    selectedOrder.value = null
    ElMessage.success('订单已移至"待创建"')
  } catch (e) { ElMessage.error('操作失败：' + e.message) }
}

// Tab2 "待回复"：客户要修改 → 退回待处理（客户修改状态）
const markCustomerModify = async () => {
  if (!selectedOrder.value) return
  try {
    const { error } = await supabase
      .from('orders').update({ status: '客户修改' }).eq('id', selectedOrder.value.id)
    if (error) throw error
    await store.getPendingOrders()
    selectedOrder.value = null
    ElMessage.success('订单已退回"待处理"（客户修改）')
  } catch (e) { ElMessage.error('操作失败：' + e.message) }
}

// Tab3 "待创建"：退回待处理
const returnToPendingFromTab3 = async () => {
  if (!selectedOrder.value) return
  try {
    const { error } = await supabase
      .from('orders').update({ status: '新订单' }).eq('id', selectedOrder.value.id)
    if (error) throw error
    await store.getPendingOrders()
    selectedOrder.value = null
    ElMessage.success('订单已退回"待处理"')
  } catch (e) { ElMessage.error('操作失败：' + e.message) }
}

// 等待天数（基于 email_sent_at 字段）
const daysSince = (dateStr) => {
  if (!dateStr) return 0
  const diff = Date.now() - new Date(dateStr).getTime()
  return Math.floor(diff / (1000 * 60 * 60 * 24))
}

// 客户已确认 - 表格行操作
const confirmByCustomer = async (order) => {
  if (!order) return
  try {
    await store.updateOrderStatus(order.id, '待创建')
    ElMessage.success('订单已移至待创建')
    await store.getPendingOrders()
    selectedOrder.value = null
  } catch (e) {
    ElMessage.error('操作失败: ' + e.message)
  }
}

// 客户已确认 - 右侧面板操作
const confirmByCustomerFromPanel = async () => {
  if (!selectedOrder.value) return
  await confirmByCustomer(selectedOrder.value)
}

// 退回待处理 - 表格行操作
const revertToPending = async (order) => {
  if (!order) return
  try {
    const { error } = await supabase.from('orders').update({ status: '新订单' }).eq('id', order.id)
    if (error) throw error
    ElMessage.success('订单已退回待处理')
    await store.getPendingOrders()
    selectedOrder.value = null
  } catch (e) {
    ElMessage.error('操作失败: ' + e.message)
  }
}

// 退回到待回复 - 表格行操作（从待创建状态回退）
const revertToEffectSent = async (order) => {
  if (!order) return
  try {
    const { error } = await supabase.from('orders').update({ status: '待回复' }).eq('id', order.id)
    if (error) throw error
    ElMessage.success('订单已退回待回复')
    await store.getPendingOrders()
    selectedOrder.value = null
  } catch (e) {
    ElMessage.error('操作失败: ' + e.message)
  }
}

// 退回待处理 - 右侧面板操作
const revertToPendingFromPanel = async () => {
  if (!selectedOrder.value) return
  await revertToPending(selectedOrder.value)
}

// 退回到待回复 - 右侧面板操作
const revertToEffectSentFromPanel = async () => {
  if (!selectedOrder.value) return
  await revertToEffectSent(selectedOrder.value)
}

// 重发邮件
const resendEmail = async () => {
  if (!selectedOrder.value) return
  isResendingEmail.value = true
  try {
    // 1. 获取最近一次邮件记录内容
    const { data: lastEmail } = await supabase
      .from('email_logs')
      .select('*')
      .eq('order_id', selectedOrder.value.id)
      .order('created_at', { ascending: false })
      .limit(1)
      .maybeSingle()
    
    if (!lastEmail) {
      ElMessage.warning('未找到历史邮件记录，请返回Tab1重新发送')
      return
    }

    // 2. 保存新的邮件日志（标记为重发）
    await supabase
      .from('email_logs')
      .insert({
        order_id: selectedOrder.value.id,
        email_type: 'resend_confirm',
        subject: lastEmail.subject,
        content: lastEmail.content,
        effect_image_url: lastEmail.effect_image_url || selectedOrder.value.effect_image_url || '',
        sender_name: lastEmail.sender_name || 'Sophia',
        status: 'sent'
      })

    // 3. 更新订单的 email_sent_at 为最新时间
    await supabase
      .from('orders')
      .update({
        email_sent_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      })
      .eq('id', selectedOrder.value.id)

    // 4. 刷新订单数据
    await store.getPendingOrders()
    const refreshed = store.orders.find(o => o.id === selectedOrder.value.id)
    if (refreshed) selectedOrder.value = refreshed

    ElMessage.success('✅ 邮件已重发')
  } catch (err) {
    console.error('重发邮件失败:', err)
    ElMessage.error('重发失败：' + (err.message || '未知错误'))
  } finally {
    isResendingEmail.value = false
  }
}

// 前往物流下单页面（带订单参数）
const goToShippingWithOrder = (order) => {
  if (!order) {
    ElMessage.warning('请先选择订单')
    return
  }
  selectOrder(order)
  router.push({
    path: '/admin/orders/shipping',
    query: { orderId: order.id }
  })
}

// 监听 Tab 切换，自动选择第一个订单
watch(orderTab, (newTab) => {
  if (newTab === 'new' && filteredOrders.value.length > 0) {
    // 切换到待处理 Tab 时，自动选择第一个订单
    const firstNewOrder = filteredOrders.value[0]
    if (firstNewOrder) {
      selectOrder(firstNewOrder)
      console.log('📌 自动选择待处理订单:', firstNewOrder.etsy_order_id)
    }
  } else if (newTab === 'waiting' && filteredOrders.value.length > 0) {
    // 切换到待回复 Tab 时，自动选择第一个订单
    const firstWaitingOrder = filteredOrders.value[0]
    if (firstWaitingOrder) {
      selectOrder(firstWaitingOrder)
      console.log('📌 自动选择待回复订单:', firstWaitingOrder.etsy_order_id)
    }
  } else if (newTab === 'pending' && filteredOrders.value.length > 0) {
    // 切换到待创建 Tab 时，自动选择第一个订单
    const firstPendingOrder = filteredOrders.value[0]
    if (firstPendingOrder) {
      selectOrder(firstPendingOrder)
      console.log('📌 自动选择待创建订单:', firstPendingOrder.etsy_order_id)
    }
  } else if (newTab === 'all' && filteredOrders.value.length > 0) {
    // 切换到全部 Tab 时，自动选择第一个订单
    const firstAllOrder = filteredOrders.value[0]
    if (firstAllOrder) {
      selectOrder(firstAllOrder)
      console.log('📌 自动选择订单:', firstAllOrder.etsy_order_id)
    }
  }
})

const allOrders = computed(() => {
  // 返回所有待确认模块相关状态的订单（新订单, 客户修改, 待回复, 待创建）
  // 具体Tab筛选由 filteredOrders 负责
  console.log('🔍 allOrders 计算:', store.orders.length, '条订单', {
    订单状态分布: store.orders.reduce((acc, o) => {
      acc[o.status] = (acc[o.status] || 0) + 1
      return acc
    }, {})
  })
  return store.orders
})

const filteredOrders = computed(() => {
  let orders = allOrders.value
  
  // 按运营筛选
  if (activeAccount.value !== 'all') {
    orders = orders.filter(o => o.operator === activeAccount.value || o.shops?.operator === activeAccount.value)
  }
  
  // 按Tab状态筛选（新4Tab结构）
  // 待处理：status = '新订单' 或 '客户修改'
  // 待回复：status = '待回复'（已发效果图等客户确认）
  // 待创建：status = '待创建'（客户已确认，等待创建物流单）
  // 全部：显示所有待确认订单（新订单, 客户修改, 待回复, 待创建）
  if (orderTab.value === 'new') {
    orders = orders.filter(o => o.status === '新订单' || o.status === '客户修改')
  } else if (orderTab.value === 'waiting') {
    orders = orders.filter(o => o.status === '待回复')
  } else if (orderTab.value === 'pending') {
    orders = orders.filter(o => o.status === '待创建')
  } else if (orderTab.value === 'all') {
    orders = orders.filter(o => ['新订单', '客户修改', '待回复', '待创建'].includes(o.status))
  }
  
  return orders
})

// Tab计数计算属性（新4Tab结构）
const newCount = computed(() => {
  // 待处理：status = '新订单' 或 '客户修改'
  let orders = allOrders.value.filter(o => o.status === '新订单' || o.status === '客户修改')
  if (activeAccount.value !== 'all') {
    orders = orders.filter(o => o.operator === activeAccount.value || o.shops?.operator === activeAccount.value)
  }
  return orders.length
})
const waitingCount = computed(() => {
  // 待回复：status = '待回复'
  let orders = allOrders.value.filter(o => o.status === '待回复')
  if (activeAccount.value !== 'all') {
    orders = orders.filter(o => o.operator === activeAccount.value || o.shops?.operator === activeAccount.value)
  }
  return orders.length
})
const pendingCreateCount = computed(() => {
  // 待创建：status = '待创建'
  let orders = allOrders.value.filter(o => o.status === '待创建')
  if (activeAccount.value !== 'all') {
    orders = orders.filter(o => o.operator === activeAccount.value || o.shops?.operator === activeAccount.value)
  }
  return orders.length
})
const allCount = computed(() => {
  // 全部：显示所有待确认订单（新订单, 客户修改, 待回复, 待创建）
  let orders = allOrders.value.filter(o => ['新订单', '客户修改', '待回复', '待创建'].includes(o.status))
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
  
  // 如果在客户修改Tab，加载邮件记录和客户修改要求
  if (orderTab.value === 'modify') {
    await loadModifyOrderData(order)
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
          
          console.log('✅ 效果图已保存:', result.url)
          resolve(result)
        } catch (e) {
          ElMessage.error('❌ 保存失败：' + e.message)
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
    await store.updateOrderStatus(order.id, '新订单')
    alert('✅ 已转为待确认订单')
  } catch (e) {
    alert('❌ 操作失败：' + e.message)
  }
}

const confirmOrder = async (order) => {
  if (!confirm(`确认将订单 ${order.etsy_order_id || order.id} 进入物流下单？`)) return
  try {
    await store.updateOrderStatus(order.id, '待创建')
    selectedOrder.value = null
    ElMessage.success('订单已确认，即将进入物流下单页面')
    setTimeout(() => {
      router.push({
        path: '/admin/orders/shipping',
        query: { orderId: order.id }
      })
    }, 500)
  } catch (e) {
    ElMessage.error('操作失败：' + e.message)
  }
}

const rollbackToEdit = async (order) => {
  if (!confirm(`确认将订单 ${order.etsy_order_id || order.id} 回退到新订单状态？\n此操作会清空效果图数据，订单将回到"新订单"Tab。`)) return
  try {
    await store.clearEffectImage(order.id)
    selectedOrder.value = null
    await store.getPendingOrders()
    ElMessage.success('✅ 订单已回退到新订单状态！')
  } catch (e) {
    ElMessage.error('❌ 操作失败：' + e.message)
  }
}

const confirmDesign = async () => {
  if (!selectedOrder.value) {
    ElMessage.warning('请先选择一条订单')
    return
  }

  try {
    // 1. 保存效果图到服务器
    await saveEffectImage()
    console.log('✅ 效果图保存完成')

    // 2. 刷新订单列表确保数据同步
    await store.getPendingOrders()
    const savedOrder = store.orders.find(o => o.id === selectedOrder.value.id)
    if (savedOrder) selectedOrder.value = savedOrder

    // 3. 标记效果图已确认
    isEffectConfirmed.value = true

    ElMessage.success('✅ 效果图已确认')
  } catch (e) {
    console.error('❌ confirmDesign 失败:', e)
    ElMessage.error('❌ 操作失败：' + e.message)
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
    // 同时清空 email_status
    await supabase.from('orders').update({ 
      email_status: null,
      updated_at: new Date().toISOString()
    }).eq('id', order.id)
    selectedOrder.value = null
    await store.getPendingOrders()
    ElMessage.success('✅ 订单已回退到邮件撰写状态！')
  } catch (e) {
    ElMessage.error('❌ 操作失败：' + e.message)
  }
}

// 回退到待创建状态（从客户修改回退）
const rollbackToPending = async (order) => {
  if (!confirm(`确认将订单 ${order.etsy_order_id || order.id} 回退到待创建状态？\n此操作会清空客户修改状态，订单将回到"待创建"Tab。`)) return
  try {
    await supabase.from('orders').update({ 
      email_status: null,
      updated_at: new Date().toISOString()
    }).eq('id', order.id)
    selectedOrder.value = null
    await store.getPendingOrders()
    ElMessage.success('✅ 订单已回退到待创建状态！')
  } catch (e) {
    ElMessage.error('❌ 操作失败：' + e.message)
  }
}

// 重置订单为新订单（清空所有状态，用于测试）
const resetOrderToNew = async (order) => {
  if (!confirm(`确认将订单 ${order.etsy_order_id || order.id} 重置为新订单？\n此操作会清空效果图和邮件状态，订单将回到"新订单"Tab。`)) return
  try {
    await store.clearEffectImage(order.id)
    selectedOrder.value = null
    await store.getPendingOrders()
    ElMessage.success('✅ 订单已重置为新订单状态！')
  } catch (e) {
    ElMessage.error('❌ 操作失败：' + e.message)
  }
}

// 全局重置：将生产中/已确认订单回退到pending新订单状态（测试用）
const resetToPending = async (order) => {
  if (!confirm(`⚠️ 测试功能：确认将订单 ${order.etsy_order_id || order.id} 重置为新订单？\n\n此操作会将订单状态重置为pending，并清空：\n- 效果图\n- 邮件发送状态\n- 邮件状态标记\n\n订单将回到"新订单"Tab。`)) return
  try {
    const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
    const supabaseKey = import.meta.env.VITE_SUPABASE_ANON_KEY
    
    const response = await fetch(
      `${supabaseUrl}/rest/v1/orders?id=eq.${order.id}`,
      {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'apikey': supabaseKey,
          'Authorization': `Bearer ${supabaseKey}`,
          'Prefer': 'return=representation'
        },
        body: JSON.stringify({
          status: '新订单',
          effect_image_url: null,
          email_sent: false,
          email_status: null,
          updated_at: new Date().toISOString()
        })
      }
    )
    
    if (!response.ok) {
      throw new Error('重置订单状态失败')
    }
    
    selectedOrder.value = null
    await store.getPendingOrders()
    ElMessage.success('✅ 订单已重置为新订单状态！')
  } catch (e) {
    ElMessage.error('❌ 操作失败：' + e.message)
  }
}

const initials = computed(() => {
  const name = selectedOrder.value?.customer_name || 'M'
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
})

const generateEmail = async () => {
  if (!selectedOrder.value) {
    ElMessage.warning('请先选择一条订单')
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
  
  // 修改确认类型：调用AI API生成
  if (emailType.value === 'modification') {
    isGeneratingEmail.value = true
    try {
      const apiBase = import.meta.env.VITE_API_BASE || 'http://localhost:8000'
      const response = await fetch(`${apiBase}/api/ai/generate-email`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          scene: 'modify_confirm',
          customer_name: firstName,
          product_name: order.sku_mapping?.product_name || 'Custom Pet Tag',
          front_text: order.front_text || '',
          back_text: order.back_text || '',
          shape: order.sku_mapping?.shape || '',
          color: order.sku_mapping?.color || '',
          size: order.sku_mapping?.size || '',
          tone: emailTone.value,
          length: emailLength.value,
          sender_name: senderName.value,
          customer_request: customerNote.value,
          operator_note: '',
          effect_image_url: effectImageUrl,
          confirmation_deadline: deadlineStr,
          order_id: orderId
        })
      })
      
      const result = await response.json()
      
      if (result.success) {
        // 处理换行符：字面\n转为真实换行
        const processNewlines = (text) => text.replace(/\\n/g, '\n')
        emailContentChinese.value = processNewlines(result.data.chinese_content || '')
        emailContentEnglish.value = processNewlines(result.data.english_content || '')
        emailContent.value = emailContentEnglish.value
        ElMessage.success('AI邮件生成成功！')
      } else {
        ElMessage.error('AI生成失败：' + (result.message || '未知错误'))
      }
    } catch (e) {
      ElMessage.error('AI生成异常：' + e.message)
    } finally {
      isGeneratingEmail.value = false
    }
    return
  }
  
  // 首封确认 / 追评邮件：用模板填充
  if (!selectedTemplate.value) {
    ElMessage.warning('请先选择一个场景模板')
    return
  }
  
  // 获取模板内容
  const tone = emailTone.value
  const length = emailLength.value
  const templateContent = selectedTemplate.value.content[tone]?.[length]
  
  if (!templateContent) {
    ElMessage.warning('模板内容不存在，请检查模板配置')
    return
  }
  
  // 替换变量 - URL掩码处理
  const replaceVars = (text) => {
    // 将supabase存储URL替换为友好文本
    const maskedUrl = effectImageUrl && effectImageUrl.includes('supabase.co') 
      ? '[View Design Preview]' 
      : effectImageUrl
    
    return text
      .replace(/\{firstName\}/g, firstName)
      .replace(/\{orderId\}/g, orderId)
      .replace(/\{effectImageUrl\}/g, maskedUrl)
      .replace(/\{senderName\}/g, senderName.value)
      .replace(/\{confirmationDeadline\}/g, deadlineStr)
      .replace(/\\n/g, '\n') // 换行符处理：字面\n转为真实换行
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
  
  // 生成邮件内容（模板已包含完整的问候、正文和落款，直接替换变量即可）
  // 模板content字段中已经包含落款如 "Best,\n{senderName}" 或 "祝好，\n{senderName}"
  emailContentEnglish.value = replaceVars(templateContent.en)
  emailContentChinese.value = replaceVars(templateContent.zh)
  // 如果有客户备注，追加到中文邮件末尾
  if (customerNote.value) {
    emailContentChinese.value += `\n\n备注：${customerNote.value}`
  }
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
    const apiBase = import.meta.env.VITE_API_BASE || 'http://localhost:8000'
    const response = await fetch(`${apiBase}/api/translate/email`, {
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

// 清除邮件内容
const clearEmailContent = () => {
  emailContentChinese.value = ''
  emailContentEnglish.value = ''
  emailContent.value = ''
  customerNote.value = ''
  ElMessage.success('邮件内容已清除')
}

// 邮件发送loading状态
const isSendingEmail = ref(false)

const submitEmail = async () => {
  if (!emailContentChinese.value && !emailContentEnglish.value) {
    ElMessage.warning('请先点击「生成邮件」')
    return
  }
  if (!selectedOrder.value) {
    ElMessage.warning('请先选择订单')
    return
  }
  
  isSendingEmail.value = true
  
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
    
    // 2. 尝试发送邮件（有客户邮箱时才发送，发送失败不阻断主流程）
    let emailSendSuccess = false
    if (selectedOrder.value.customer_email) {
      try {
        // 从效果图URL中提取文件名作为effect_image_path
        const effectImageUrl = selectedOrder.value.effect_image_url || ''
        const effectImagePath = effectImageUrl.split('/').pop() || ''
        
        // 构建产品信息
        const productInfo = `${selectedOrder.value.sku_mapping?.product_name || 'Custom Product'} (${selectedOrder.value.sku_mapping?.sku_code || selectedOrder.value.sku_id || 'N/A'})`
        
        await sendConfirmationEmail({
          order_id: selectedOrder.value.id,
          to_email: selectedOrder.value.customer_email || '',
          customer_name: selectedOrder.value.customer_name || '',
          product_info: productInfo,
          effect_image_path: effectImagePath
        })
        
        emailSendSuccess = true
        console.log('✅ 邮件已自动发送至客户邮箱')
      } catch (sendError) {
        console.log('⚠️ 自动发送邮件跳过:', sendError.message)
      }
    } else {
      console.log('⚠️ 订单无客户邮箱，跳过自动发送')
    }
    
    // 3. 更新订单状态为已发送邮件
    await store.updateEmailSentStatus(selectedOrder.value.id, true)
    
    // 4. 设置已确认的邮件内容（显示在右侧"确认邮件"栏）
    confirmedEmailContent.value = emailContentEnglish.value
    
    // 5. 清空邮件内容
    emailContentChinese.value = ''
    emailContentEnglish.value = ''
    emailContent.value = ''
    customerNote.value = ''
    
    // 6. 刷新订单列表
    await store.getPendingOrders()
    
    // 7. 跳转到待创建Tab，并选中当前订单
    orderTab.value = 'pending'
    const updatedOrder = store.orders.find(o => o.id === selectedOrder.value.id)
    if (updatedOrder) {
      selectedOrder.value = updatedOrder
    }
    // 8. 设置待创建Tab的邮件预览内容（流转时直接使用已保存的内容）
    pendingEmailContent.value = fullContent
    
    // 9. 显示成功提示
    if (emailSendSuccess) {
      ElMessage.success('✅ 邮件已保存并发送，订单已流转到待创建状态！')
    } else {
      ElMessage.success('✅ 邮件已保存，订单已流转到待创建状态！')
    }
  } catch (e) {
    ElMessage.error('❌ 邮件保存失败：' + e.message)
  } finally {
    isSendingEmail.value = false
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
    ElMessage.warning('请先选择订单')
    return
  }
  try {
    // 从etsy订单中获取已保存的邮件内容
    const emailLog = await store.getEmailLogByOrderId(selectedOrder.value.id)
    if (emailLog && emailLog.content) {
      await navigator.clipboard.writeText(emailLog.content)
      ElMessage.success('✅ 邮件内容已复制！客服可粘贴到Etsy后台发送给客户')
    } else {
      ElMessage.warning('暂无邮件内容，请先生成邮件')
    }
  } catch (e) {
    ElMessage.error('复制失败：' + e.message)
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
    await store.updateOrderStatus(selectedOrder.value.id, '生产中')
    selectedOrder.value = null
    alert('✅ 订单已转入生产中！')
  } catch (e) {
    alert('❌ 操作失败：' + e.message)
  }
}

// 前往物流下单页面
const goToShipping = () => {
  if (!selectedOrder.value) {
    ElMessage.warning('请先选择订单')
    return
  }
  // 带上订单ID跳转到物流下单页面
  router.push({
    path: '/admin/orders/shipping',
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

// 客户修改Tab：加载订单相关数据（邮件记录 + 客户修改要求）
const loadModifyOrderData = async (order) => {
  if (!order) return
  
  try {
    // 1. 加载邮件历史记录
    const emailLogs = await store.getOrderEmailLogs(order.id)
    modifyOrderLogs.value = emailLogs || []
    
    // 2. 获取最新邮件内容
    if (emailLogs && emailLogs.length > 0) {
      modifyLastEmail.value = emailLogs[0].content || ''
    }
    
    // 3. 从 Supabase 加载 service_link_logs 获取客户修改要求
    const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
    const supabaseKey = import.meta.env.VITE_SUPABASE_ANON_KEY
    
    const response = await fetch(
      `${supabaseUrl}/rest/v1/service_link_logs?order_id=eq.${order.id}&action=eq.request_modify&select=*&order=created_at.desc`,
      {
        headers: {
          'apikey': supabaseKey,
          'Authorization': `Bearer ${supabaseKey}`
        }
      }
    )
    
    if (response.ok) {
      const logs = await response.json()
      if (logs && logs.length > 0) {
        // 从 action_details JSONB 字段提取修改原因
        const latestLog = logs[0]
        modifyCustomerRequest.value = latestLog.action_details?.reason 
          || latestLog.action_details?.feedback 
          || '客户请求修改，但未填写具体原因'
      } else {
        modifyCustomerRequest.value = '暂无客户修改要求记录'
      }
    }
    
    console.log('📋 客户修改Tab数据加载完成:', {
      emailLogs: emailLogs?.length || 0,
      lastEmail: modifyLastEmail.value ? '已加载' : '无',
      customerRequest: modifyCustomerRequest.value
    })
  } catch (e) {
    console.error('❌ 加载客户修改Tab数据失败:', e)
  }
}

// 客户修改Tab：保存草稿
const saveModifyDraft = async () => {
  if (!selectedOrder.value) {
    alert('请先选择订单')
    return
  }
  
  try {
    // 保存回复邮件作为新的邮件记录
    if (replyContent.value.trim()) {
      await store.saveEmailLog({
        order_id: selectedOrder.value.id,
        email_type: 'modification',
        subject: `【修改确认】Your Custom ${selectedOrder.value.sku_mapping?.product_name || 'Product'} - ${selectedOrder.value.etsy_order_id}`,
        content: replyContent.value,
        effect_image_url: selectedOrder.value.effect_image_url,
        sender_name: replySenderName.value
      })
      console.log('✅ 草稿已保存')
      alert('✅ 草稿已保存')
    } else {
      alert('请先填写回复内容')
    }
  } catch (e) {
    console.error('❌ 保存草稿失败:', e)
    alert('❌ 保存失败：' + e.message)
  }
}

// 客户修改Tab：标记已处理（将订单流转回待创建Tab）
const markModifyHandled = async () => {
  if (!selectedOrder.value) {
    alert('请先选择订单')
    return
  }
  
  if (!confirm(`确认将订单 ${selectedOrder.value.etsy_order_id} 标记为已处理？\n\n订单将流转到「待创建」Tab，等待发送给客户确认。`)) return
  
  try {
    const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
    const supabaseKey = import.meta.env.VITE_SUPABASE_ANON_KEY
    
    // 更新订单的 email_status 为空（恢复到待创建状态）
    const response = await fetch(
      `${supabaseUrl}/rest/v1/orders?id=eq.${selectedOrder.value.id}`,
      {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'apikey': supabaseKey,
          'Authorization': `Bearer ${supabaseKey}`,
          'Prefer': 'return=representation'
        },
        body: JSON.stringify({
          email_status: null,
          updated_at: new Date().toISOString()
        })
      }
    )
    
    if (!response.ok) {
      throw new Error('更新订单状态失败')
    }
    
    // 刷新订单列表
    await store.getPendingOrders()
    
    // 清空选中状态
    selectedOrder.value = null
    modifyOrderLogs.value = []
    modifyCustomerRequest.value = ''
    modifyLastEmail.value = ''
    replyContent.value = ''
    
    alert('✅ 订单已标记为已处理，已流转到「待创建」Tab！')
    console.log('✅ 订单修改已处理完成')
  } catch (e) {
    console.error('❌ 标记处理失败:', e)
    alert('❌ 操作失败：' + e.message)
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
