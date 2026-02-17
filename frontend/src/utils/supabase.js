import { createClient } from '@supabase/supabase-js'

// 从环境变量获取 Supabase 配置
const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL
const SUPABASE_KEY = import.meta.env.VITE_SUPABASE_KEY

// 检查配置是否存在
if (!SUPABASE_URL || !SUPABASE_KEY) {
  console.error('⚠️ Supabase 配置缺失，请检查 .env 文件')
}

// 创建 Supabase 客户端实例
const supabase = createClient(SUPABASE_URL, SUPABASE_KEY)

console.log('✅ Supabase 客户端初始化成功')

export default supabase
