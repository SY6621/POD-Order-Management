# ETSY订单自动化系统

## 📖 项目简介

ETSY订单自动化处理系统，实现以下核心功能：
- 📧 自动读取Etsy订单邮件
- 📋 智能解析订单数据
- 🖼️ 自动生成效果图
- 🏷️ 生成物流标签

---

## 🚀 快速开始

### 1. 环境要求

- **Python**: 3.10+
- **Poetry**: 1.7+ （Python包管理工具）
- **操作系统**: Windows 10/11

### 2. 安装Poetry

如果尚未安装Poetry，请执行以下命令：

**方式一：使用官方安装脚本（推荐）**
```powershell
# PowerShell执行
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

**方式二：使用pip安装**
```powershell
pip install poetry
```

**验证安装**
```powershell
poetry --version
```

> 📌 Poetry官方文档：https://python-poetry.org/docs/#installation

### 3. 安装项目依赖

```powershell
# 进入后端目录
cd D:\ETSY_Order_Automation\backend

# 安装依赖（Poetry会自动创建虚拟环境）
poetry install
```

### 4. 激活虚拟环境

```powershell
# 方式一：激活虚拟环境Shell
poetry shell

# 方式二：在虚拟环境中执行命令（无需激活）
poetry run python your_script.py
```

### 5. 配置环境变量

在 `backend/` 目录下创建 `.env` 文件：

```ini
# 邮箱配置
IMAP_SERVER=imap.gmail.com
IMAP_PORT=993
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

# 数据库配置
DATABASE_URL=sqlite:///./data/orders.db

# 日志级别
LOG_LEVEL=INFO
```

---

## 📁 项目结构

```
ETSY_Order_Automation/
├── backend/              # Python后端
│   ├── src/              # 源代码
│   │   ├── config/       # 配置模块
│   │   ├── models/       # 数据模型
│   │   ├── services/     # 业务服务
│   │   └── utils/        # 工具函数
│   ├── tests/            # 测试文件
│   └── pyproject.toml    # Poetry配置
├── frontend/             # Vue3前端（预留）
├── .qoder/rules/         # Qoder开发规范
├── docs/                 # 项目文档
├── logs/                 # 日志文件
└── data/                 # 数据存储
```

---

## 🛠️ 常用命令

```powershell
# 安装依赖
poetry install

# 添加新依赖
poetry add package_name

# 添加开发依赖
poetry add --group dev package_name

# 运行测试
poetry run pytest

# 代码格式化
poetry run black src/

# 代码检查
poetry run pylint src/

# 查看虚拟环境路径
poetry env info --path
```

---

## 📜 Git版本号规范

### 版本号格式

```
POD V{主版本}.{次版本}_{日期}
```

### 规则说明

| 组件 | 含义 | 示例 |
|------|------|------|
| **POD** | 项目代码（Product Order Delivery - 产品订单交付系统） | POD |
| **V{主版本}** | 重大功能迭代（如V1、V2） | V1 |
| **.{次版本}** | 功能更新/优化（递增01、02、03...） | .03 |
| **_{日期}** | 提交日期（YYYYMMDD） | _20260313 |

### 版本历史

| 版本号 | 日期 | 说明 |
|--------|------|------|
| `POD V1.02_20260313` | 2026-03-13 | 物流下单功能完善 |
| `POD V1.03_20260313` | 2026-03-13 | 待创建Tab页面UI优化 |
| `POD V1.04_20260326` | 2026-03-26 | SVG设计器尺寸标注与PDF效果图完整集成 - 设计器添加尺寸标注线、PDF支持正反双面渲染、修复SKU/邮编字段兼容 |

### 提交示例

```bash
git commit -m "POD V1.03_20260313: 待创建Tab页面UI优化 - 订单列表与详情高度一致、字体放大"
```

---

## ✅ 回归测试

- 端到端回归测试用例：`docs/回归测试_订单端到端流程.md`

---

## 📋 开发规范

详见 `.qoder/rules/code-standard.md`

- 代码风格：PEP8
- 注释风格：Google Style
- 命名规范：snake_case

---

## 📞 联系方式

如有问题，请提交Issue或联系开发者。

---

## 📜 许可证

MIT License
