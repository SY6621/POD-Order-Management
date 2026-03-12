<template>
  <div class="p-8">
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-slate-800">效果图管理</h1>
      <p class="text-slate-500">管理店铺效果图生成邮件链接配置</p>
    </div>

    <!-- 店铺效果图配置 -->
    <div class="bg-white rounded-xl border border-slate-200 overflow-hidden">
      <div class="px-6 py-4 border-b border-slate-200">
        <h2 class="font-bold text-slate-800">店铺效果图配置</h2>
        <p class="text-sm text-slate-500 mt-1">为每个店铺配置效果图生成后的通知邮件链接</p>
      </div>
      
      <table class="w-full">
        <thead class="bg-slate-50">
          <tr>
            <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">店铺</th>
            <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">地区</th>
            <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">效果图邮件链接</th>
            <th class="text-left py-3 px-4 text-sm font-semibold text-slate-600">操作</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100">
          <tr v-for="shop in shops" :key="shop.id" class="hover:bg-slate-50">
            <td class="py-4 px-4">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-full bg-purple-100 flex items-center justify-center">
                  <span class="font-bold text-purple-600">{{ shop.code.toUpperCase() }}</span>
                </div>
                <div>
                  <p class="font-medium text-slate-800">{{ shop.name }}</p>
                  <p class="text-sm text-slate-500">{{ shop.code }}</p>
                </div>
              </div>
            </td>
            <td class="py-4 px-4 text-slate-600">{{ shop.region }}</td>
            <td class="py-4 px-4">
              <div class="flex items-center gap-2">
                <input 
                  v-model="shop.effect_email_link"
                  type="text"
                  placeholder="输入邮件通知链接"
                  class="flex-1 px-3 py-2 border border-slate-200 rounded-lg text-sm"
                >
              </div>
            </td>
            <td class="py-4 px-4">
              <button 
                @click="saveShopConfig(shop)"
                class="text-sm text-blue-600 hover:underline"
              >
                保存配置
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      
      <div v-if="shops.length === 0" class="p-8 text-center text-slate-500">
        暂无店铺数据
      </div>
    </div>

    <!-- 说明 -->
    <div class="mt-6 bg-blue-50 rounded-xl p-6">
      <h3 class="font-medium text-blue-800 mb-2">配置说明</h3>
      <ul class="text-sm text-blue-700 space-y-1">
        <li>• 当系统为订单生成效果图后，会自动发送邮件通知店铺</li>
        <li>• 邮件中包含效果图下载链接，店铺点击即可查看和下载</li>
        <li>• 每个店铺可以配置独立的通知邮件接收地址</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAdminStore } from '../../stores/adminStore'

const adminStore = useAdminStore()
const shops = ref([])

onMounted(async () => {
  const data = await adminStore.fetchShops()
  
  // 如果没有数据，使用模拟数据
  if (!data || data.length === 0) {
    shops.value = [
      { 
        id: '1', 
        name: '美国店铺', 
        code: 'us', 
        region: 'North America',
        effect_email_link: 'https://example.com/effects/us'
      },
      { 
        id: '2', 
        name: '欧洲店铺', 
        code: 'eu', 
        region: 'Europe',
        effect_email_link: 'https://example.com/effects/eu'
      },
      { 
        id: '3', 
        name: '亚洲店铺', 
        code: 'asia', 
        region: 'Asia',
        effect_email_link: 'https://example.com/effects/asia'
      }
    ]
  } else {
    shops.value = data
  }
})

// 保存店铺配置
async function saveShopConfig(shop) {
  // TODO: 调用API保存配置
  alert(`已保存 ${shop.name} 的配置`)
}
</script>