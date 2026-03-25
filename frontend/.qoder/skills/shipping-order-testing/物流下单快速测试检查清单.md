# 物流下单快速测试检查清单

## 🔧 环境检查（5分钟）

```powershell
# 1. 检查前端服务
cd D:\ETSY_Order_Automation\frontend
npm run dev
# 访问 http://localhost:5173

# 2. 检查后端服务
cd D:\ETSY_Order_Automation\backend
poetry run uvicorn src.api.main:app --reload --port 8000
# 访问 http://localhost:8000/health

# 3. 检查4PX配置
cd D:\ETSY_Order_Automation\backend
type .env | findstr "FOURPX"
```

## 📦 测试数据准备

```powershell
# 检查订单状态
cd D:\ETSY_Order_Automation\backend
poetry run python scripts/check_order_status.py

# 如果没有"confirmed"状态订单，手动设置
# 方式1: 使用重置脚本
poetry run python scripts/reset_orders_for_test.py

# 方式2: SQL更新
# UPDATE orders SET status = 'confirmed' WHERE id = 'xxx';
```

## ✅ 功能测试清单

### 阶段一：页面加载（1分钟）
- [ ] 访问 http://localhost:5173/admin/orders/shipping
- [ ] 页面标题显示"物流下单"
- [ ] 顶部统计显示正确
- [ ] 物流公司Tab显示正常
- [ ] 左侧订单列表加载

### 阶段二：选择订单（1分钟）
- [ ] 点击某个订单的"选择"按钮
- [ ] 选中行背景变蓝
- [ ] 右侧表单自动填充
- [ ] 收件人信息正确显示

### 阶段三：创建物流订单（2分钟）
- [ ] 点击"创建物流订单"按钮
- [ ] 按钮显示loading状态
- [ ] 等待3-10秒返回结果
- [ ] 显示绿色成功提示
- [ ] 显示运单号
- [ ] 订单从列表移除

### 阶段四：面单操作（1分钟）
- [ ] 点击"下载面单PDF"
- [ ] 新标签页打开PDF
- [ ] PDF显示正确信息
- [ ] 点击"打印面单"
- [ ] 打印预览窗口打开

### 阶段五：数据验证（2分钟）
```powershell
# 检查物流表更新
cd D:\ETSY_Order_Automation\backend
poetry run python -c "
from supabase import create_client
import os
env = {}
with open('.env') as f:
    for line in f:
        if '=' in line and not line.startswith('#'):
            k, v = line.strip().split('=', 1)
            env[k] = v.strip('\"').strip(\"'\")
sb = create_client(env['SUPABASE_URL'], env['SUPABASE_KEY'])
logs = sb.table('logistics').select('*').order('id', desc=True).limit(1).execute()
print('最新物流记录:', logs.data[0] if logs.data else '无')
"
```

- [ ] `tracking_number` 有值
- [ ] `label_url` 有值
- [ ] `shipping_status` = 'shipped'
- [ ] `orders.status` = 'producing'

## ❌ 异常场景测试

- [ ] 清空必填字段，点击下单 → 显示错误提示
- [ ] 使用错误API密钥 → 显示签名错误
- [ ] 网络断开 → 显示网络错误

## 📊 测试结果报告

```
测试日期：__________
测试人员：__________
测试环境：□ 开发  □ 测试  □ 生产

测试结果：
□ 全部通过
□ 部分失败（见下方记录）
□ 严重阻塞

失败项记录：
1. ________________________
2. ________________________
3. ________________________

建议：
________________________
```

## 🚀 快速验证命令

```powershell
# 一键检查所有服务状态
cd D:\ETSY_Order_Automation\backend
echo "=== 检查后端 ===" ; curl http://localhost:8000/health
echo "`n=== 检查前端 ===" ; curl http://localhost:5173
echo "`n=== 检查数据库订单 ===" ; poetry run python scripts/check_order_status.py
echo "`n=== 检查4PX配置 ===" ; type .env | findstr "FOURPX"
```
