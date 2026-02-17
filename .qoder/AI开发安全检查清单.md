# AI开发安全检查清单

## 每次修改代码前必须确认

### ✅ 修改前检查
- [ ] AI已读取完整文件内容（read_file）
- [ ] AI明确说明修改的目的和位置
- [ ] 我已理解修改的影响范围
- [ ] 如果是核心文件（pdf_service.py, orderStore.js, Dashboard.vue, Orders.vue），我已明确授权

### ✅ 修改后检查
- [ ] 使用`git diff`查看实际改动
- [ ] 确认改动符合预期
- [ ] 没有意外删除或新增代码
- [ ] 运行测试脚本验证功能正常

### ✅ 提交前检查
- [ ] 所有改动都经过验证
- [ ] commit信息清晰描述本次改动
- [ ] 已创建备份分支（如果是重大改动）

## 对话管理策略

### 何时重启对话
- 完成一个大功能模块
- 对话轮次超过50轮
- AI回答开始出现偏差
- 感觉上下文丢失

### 重启对话前必做
1. `git commit -m "阶段性提交：<功能描述>"`
2. 记录当前进度和待办事项
3. 准备好新对话需要的上下文文件

## 紧急恢复流程

### 发现误改后立即执行
```powershell
# 1. 停止所有操作
# 2. 查看改动
git diff

# 3. 恢复文件
git checkout -- <误改的文件>

# 4. 或者整体回退
git reset --hard HEAD
```

## 核心文件清单

以下文件修改前必须额外谨慎：

### 后端核心
- `backend/src/services/pdf_service.py`
- `backend/src/services/effect_image_service.py`
- `backend/src/services/email_service.py`
- `backend/src/models/order.py`

### 前端核心
- `frontend/src/stores/orderStore.js`
- `frontend/src/views/Dashboard/Dashboard.vue`
- `frontend/src/views/Orders/Orders.vue`
- `frontend/src/utils/supabase.js`

### 配置文件
- `backend/.env`
- `frontend/.env`
- `backend/pyproject.toml`
- `frontend/package.json`

## 最佳实践

1. **小步提交**：每完成一个小功能就commit
2. **描述性commit**：`git commit -m "修复：PDF中文字体显示问题"`
3. **定期备份**：每天结束创建完整备份
4. **验证后提交**：先测试，再commit
5. **保持警惕**：AI建议修改核心文件时，先review再执行
