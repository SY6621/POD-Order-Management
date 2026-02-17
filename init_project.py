#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ETSY订单自动化系统 - Windows项目初始化脚本
功能：自动创建项目目录结构、配置文件和开发规范文档
作者：Qoder
日期：2026-01-28
"""

import os
import sys
import ctypes
from pathlib import Path


def check_admin_privileges():
    """
    检测当前脚本是否以管理员权限运行
    返回值：True表示有管理员权限，False表示无权限
    """
    try:
        # Windows系统检测管理员权限的方式
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except AttributeError:
        # 非Windows系统返回True（跳过检测）
        return True


def print_banner():
    """打印欢迎横幅"""
    banner = """
╔══════════════════════════════════════════════════════════════════╗
║         ETSY订单自动化系统 - 项目初始化工具 v1.0                  ║
║                   Windows专用版本                                 ║
╚══════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def create_directory_structure(base_path: Path):
    """
    创建项目目录结构
    参数 base_path: 项目根目录路径（Path对象）
    """
    # 定义所有需要创建的目录
    directories = [
        base_path / "backend",                    # Python后端代码目录
        base_path / "backend" / "src",            # 后端源代码
        base_path / "backend" / "src" / "config", # 配置模块
        base_path / "backend" / "src" / "models", # 数据模型
        base_path / "backend" / "src" / "services", # 业务服务
        base_path / "backend" / "src" / "utils",  # 工具函数
        base_path / "backend" / "tests",          # 测试目录
        base_path / "frontend",                   # Vue3前端（预留）
        base_path / ".qoder" / "rules",           # Qoder规则库
        base_path / "docs",                       # 项目文档
        base_path / "logs",                       # 日志目录
        base_path / "data",                       # 数据存储目录
    ]
    
    print("\n📁 正在创建目录结构...")
    for directory in directories:
        try:
            # exist_ok=True 防止目录已存在时报错
            os.makedirs(directory, exist_ok=True)
            print(f"   ✅ {directory}")
        except PermissionError:
            print(f"   ❌ 无权限创建: {directory}")
            print("   💡 请以管理员身份运行此脚本")
            sys.exit(1)
        except Exception as e:
            print(f"   ❌ 创建失败: {directory} - {e}")
            sys.exit(1)
    
    print("✅ 目录结构创建完成！")


def create_pyproject_toml(backend_path: Path):
    """
    生成Poetry项目配置文件 pyproject.toml
    参数 backend_path: backend目录路径
    """
    # pyproject.toml内容 - Poetry项目配置（使用双引号三引号避免嵌套冲突）
    pyproject_content = """[tool.poetry]
name = "etsy-order-automation"
version = "0.1.0"
description = "ETSY订单自动化处理系统 - 自动读取邮件、解析订单、生成效果图和物流标签"
authors = ["Your Name <your.email@example.com>"]
readme = "README.md"
packages = [{include = "src"}]

[tool.poetry.dependencies]
# Python版本要求
python = "^3.10"

# ===== 核心依赖 =====
# HTTP请求库，用于API调用
requests = "^2.31.0"
# IMAP邮件客户端，用于读取Etsy订单邮件
imapclient = "^3.0.0"
# 图像处理库，用于效果图生成
pillow = "^10.2.0"
# PDF生成库，用于物流标签生成
reportlab = "^4.0.8"
# SVG生成库，用于矢量图形处理
svgwrite = "^1.4.3"
# 数据库ORM，用于订单数据存储
sqlalchemy = "^2.0.25"
# 环境变量管理
python-dotenv = "^1.0.0"
# 模板引擎，用于生成邮件/报告
jinja2 = "^3.1.3"
# 日期时间处理
python-dateutil = "^2.8.2"

[tool.poetry.group.dev.dependencies]
# ===== 开发依赖 =====
# 代码格式化工具
black = "^24.1.1"
# 单元测试框架
pytest = "^8.0.0"
# 代码静态检查
pylint = "^3.0.3"
# 类型检查
mypy = "^1.8.0"
# 测试覆盖率
pytest-cov = "^4.1.0"

[tool.black]
# Black代码格式化配置
line-length = 88
target-version = ['py310']
include = '\\.pyi?$'

[tool.pylint.messages_control]
# Pylint配置
disable = "C0114,C0115,C0116"

[tool.pytest.ini_options]
# Pytest配置
testpaths = ["tests"]
python_files = "test_*.py"
python_functions = "test_*"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
"""
    
    pyproject_path = backend_path / "pyproject.toml"
    print("\n📄 正在生成 pyproject.toml...")
    
    try:
        with open(pyproject_path, "w", encoding="utf-8") as f:
            f.write(pyproject_content)
        print(f"   ✅ {pyproject_path}")
    except Exception as e:
        print(f"   ❌ 生成失败: {e}")
        sys.exit(1)


def create_code_standard(qoder_rules_path: Path):
    """
    生成Qoder代码规范文档
    参数 qoder_rules_path: .qoder/rules目录路径
    """
    # 代码规范内容
    code_standard_content = '''# ETSY订单管理系统 - 代码规范

## 1. 代码风格规范（PEP8）

### 1.1 缩进与空格
- 使用 **4个空格** 进行缩进，禁止使用Tab
- 运算符两侧各保留一个空格：`x = 1 + 2`
- 逗号后面加空格：`func(a, b, c)`
- 冒号后面加空格（字典除外）：`if condition: pass`

### 1.2 行长度限制
- 每行代码最多 **88个字符**（Black默认）
- 长表达式使用括号换行，不使用反斜杠

### 1.3 空行规范
- 顶级函数和类定义之间：**2个空行**
- 类内方法之间：**1个空行**
- 函数内逻辑段落之间：**1个空行**

### 1.4 导入规范
```python
# 标准库
import os
import sys
from pathlib import Path

# 第三方库
import requests
from sqlalchemy import create_engine

# 本地模块
from src.models import Order
from src.utils import logger
```

---

## 2. 命名规范（snake_case）

### 2.1 变量和函数
- 使用 **snake_case**（小写下划线分隔）
- 示例：`order_id`, `parse_email_content()`, `get_order_list()`

### 2.2 类名
- 使用 **PascalCase**（大驼峰）
- 示例：`OrderParser`, `EmailService`, `EffectImageGenerator`

### 2.3 常量
- 使用 **UPPER_SNAKE_CASE**（大写下划线分隔）
[tool.poetry]
name = "etsy-order-automation"
version = "0.1.0"
description = "ETSY订单自动化处理系统 - 自动读取邮件、解析订单、生成效果图和物流标签"
authors = ["Your Name <your.email@example.com>"]
package-mode = false

[tool.poetry.dependencies]
# ... existing code ...
### 2.4 私有成员
- 单下划线前缀表示内部使用：`_internal_method()`
- 双下划线前缀表示名称修饰：`__private_attr`

### 2.5 命名示例
```python
# 正确 ✅
user_name = "张三"
order_count = 10
def calculate_total_price():
    pass

# 错误 ❌
userName = "张三"      # 驼峰命名
OrderCount = 10        # 首字母大写
def CalculatePrice():  # 驼峰函数名
    pass
```

---

## 3. 注释规范（Google风格）

### 3.1 模块注释
```python
"""
模块名称：订单解析器
功能描述：解析Etsy订单邮件，提取订单信息
作者：Your Name
创建日期：2026-01-28
"""
```

### 3.2 函数/方法注释
```python
def parse_order_email(email_content: str, order_type: str = "standard") -> dict:
    """解析订单邮件内容，提取订单详情。

    从邮件原始内容中提取订单号、客户信息、商品列表等关键数据，
    并返回结构化的订单字典。

    Args:
        email_content: 邮件原始文本内容
        order_type: 订单类型，可选值为 "standard" 或 "express"
            默认为 "standard"

    Returns:
        包含订单信息的字典，结构如下：
        {
            "order_id": str,      # 订单号
            "customer": dict,     # 客户信息
            "items": list,        # 商品列表
            "total_price": float  # 订单总价
        }

    Raises:
        ValueError: 当邮件内容格式无法识别时抛出
        ParseError: 当订单数据提取失败时抛出

    Example:
        >>> email = "Order #12345..."
        >>> result = parse_order_email(email)
        >>> print(result["order_id"])
        "12345"
    """
    pass
```

### 3.3 类注释
```python
class OrderService:
    """订单管理服务类。

    提供订单的增删改查、状态管理、批量处理等功能。
    支持与数据库交互，实现订单数据的持久化存储。

    Attributes:
        db_session: 数据库会话对象
        logger: 日志记录器实例
        cache: 订单缓存字典

    Example:
        >>> service = OrderService(db_session)
        >>> order = service.get_order_by_id("12345")
        >>> service.update_order_status(order, "shipped")
    """
    
    def __init__(self, db_session):
        """初始化订单服务。

        Args:
            db_session: SQLAlchemy数据库会话对象
        """
        self.db_session = db_session
```

### 3.4 行内注释
```python
# 计算订单总价（含税）
total_price = subtotal * (1 + tax_rate)

x = x + 1  # 增加计数器（注释与代码间隔2个空格）
```

---

## 4. 类型注解规范

### 4.1 基本类型注解
```python
from typing import List, Dict, Optional, Union, Tuple

def process_order(
    order_id: str,
    items: List[dict],
    discount: Optional[float] = None
) -> Dict[str, Union[str, float]]:
    """处理订单"""
    pass
```

### 4.2 复杂类型
```python
from typing import TypedDict, Literal

class OrderDict(TypedDict):
    """订单字典类型定义"""
    order_id: str
    status: Literal["pending", "processing", "shipped", "delivered"]
    items: List[Dict[str, Union[str, int, float]]]
```

---

## 5. 错误处理规范

### 5.1 异常捕获
```python
try:
    result = parse_email(content)
except ValueError as e:
    logger.error(f"邮件格式错误: {e}")
    raise
except Exception as e:
    logger.exception(f"未知错误: {e}")
    raise RuntimeError("邮件解析失败") from e
```

### 5.2 自定义异常
```python
class OrderParseError(Exception):
    """订单解析异常"""
    
    def __init__(self, order_id: str, message: str):
        self.order_id = order_id
        super().__init__(f"订单 {order_id} 解析失败: {message}")
```

---

## 6. 日志规范

```python
import logging

# 配置日志格式
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# 使用示例
logger.debug("调试信息：变量值为 %s", value)
logger.info("订单 %s 处理完成", order_id)
logger.warning("重试次数已达 %d 次", retry_count)
logger.error("订单处理失败: %s", error_message)
logger.exception("发生异常")  # 自动记录堆栈信息
```

---

## 7. 文件组织规范

```
backend/
├── src/
│   ├── __init__.py
│   ├── config/           # 配置模块
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── models/           # 数据模型
│   │   ├── __init__.py
│   │   └── order.py
│   ├── services/         # 业务逻辑
│   │   ├── __init__.py
│   │   ├── email_service.py
│   │   └── order_service.py
│   └── utils/            # 工具函数
│       ├── __init__.py
│       └── logger.py
└── tests/                # 测试文件
    ├── __init__.py
    └── test_order_service.py
```

---

## 8. Git提交规范

### 提交信息格式
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type类型
- `feat`: 新功能
- `fix`: 修复Bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建/工具相关

### 示例
```
feat(order): 添加订单批量导出功能

- 支持CSV和Excel格式导出
- 添加日期范围筛选
- 优化大数据量导出性能

Closes #123
```
'''
    
    code_standard_path = qoder_rules_path / "code-standard.md"
    print("\n📋 正在生成代码规范文档...")
    
    try:
        with open(code_standard_path, "w", encoding="utf-8") as f:
            f.write(code_standard_content)
        print(f"   ✅ {code_standard_path}")
    except Exception as e:
        print(f"   ❌ 生成失败: {e}")
        sys.exit(1)


def create_readme(base_path: Path):
    """
    生成项目README文档
    参数 base_path: 项目根目录路径
    """
    readme_content = '''# ETSY订单自动化系统

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
cd D:\\ETSY_Order_Automation\\backend

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
'''
    
    readme_path = base_path / "README.md"
    print("\n📖 正在生成 README.md...")
    
    try:
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(readme_content)
        print(f"   ✅ {readme_path}")
    except Exception as e:
        print(f"   ❌ 生成失败: {e}")
        sys.exit(1)


def create_env_example(backend_path: Path):
    """
    生成环境变量示例文件
    参数 backend_path: backend目录路径
    """
    env_content = '''# ========================================
# ETSY订单自动化系统 - 环境变量配置
# 复制此文件为 .env 并填入实际值
# ========================================

# ----- 邮箱配置 -----
IMAP_SERVER=imap.gmail.com
IMAP_PORT=993
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

# ----- 数据库配置 -----
DATABASE_URL=sqlite:///./data/orders.db

# ----- 日志配置 -----
LOG_LEVEL=INFO
LOG_FILE=../logs/app.log

# ----- API配置（如需要） -----
# ETSY_API_KEY=your_api_key
# ETSY_API_SECRET=your_api_secret
'''
    
    env_example_path = backend_path / ".env.example"
    print("\n🔐 正在生成 .env.example...")
    
    try:
        with open(env_example_path, "w", encoding="utf-8") as f:
            f.write(env_content)
        print(f"   ✅ {env_example_path}")
    except Exception as e:
        print(f"   ❌ 生成失败: {e}")
        sys.exit(1)


def create_gitignore(base_path: Path):
    """
    生成.gitignore文件
    参数 base_path: 项目根目录路径
    """
    gitignore_content = '''# ========================================
# Python
# ========================================
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# ========================================
# 虚拟环境
# ========================================
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/
.poetry/

# ========================================
# IDE
# ========================================
.idea/
.vscode/
*.swp
*.swo
*~

# ========================================
# 测试
# ========================================
.tox/
.coverage
.coverage.*
htmlcov/
.pytest_cache/
.mypy_cache/

# ========================================
# 日志和数据
# ========================================
logs/
*.log
data/*.db
data/*.sqlite

# ========================================
# 系统文件
# ========================================
.DS_Store
Thumbs.db
desktop.ini

# ========================================
# 项目特定
# ========================================
*.pdf
*.tmp
output/
'''
    
    gitignore_path = base_path / ".gitignore"
    print("\n🚫 正在生成 .gitignore...")
    
    try:
        with open(gitignore_path, "w", encoding="utf-8") as f:
            f.write(gitignore_content)
        print(f"   ✅ {gitignore_path}")
    except Exception as e:
        print(f"   ❌ 生成失败: {e}")
        sys.exit(1)


def create_init_files(base_path: Path):
    """
    创建Python包的__init__.py文件
    参数 base_path: 项目根目录路径
    """
    init_locations = [
        base_path / "backend" / "src" / "__init__.py",
        base_path / "backend" / "src" / "config" / "__init__.py",
        base_path / "backend" / "src" / "models" / "__init__.py",
        base_path / "backend" / "src" / "services" / "__init__.py",
        base_path / "backend" / "src" / "utils" / "__init__.py",
        base_path / "backend" / "tests" / "__init__.py",
    ]
    
    print("\n🐍 正在创建 __init__.py 文件...")
    
    for init_path in init_locations:
        try:
            with open(init_path, "w", encoding="utf-8") as f:
                f.write('"""Package initialization."""\n')
            print(f"   ✅ {init_path}")
        except Exception as e:
            print(f"   ❌ 创建失败: {init_path} - {e}")


def print_next_steps():
    """打印下一步操作指引"""
    next_steps = """
╔══════════════════════════════════════════════════════════════════╗
║                    🎉 项目初始化完成！                            ║
╚══════════════════════════════════════════════════════════════════╝

📌 下一步操作指引：

┌─────────────────────────────────────────────────────────────────┐
│ 1️⃣  安装Poetry（如果尚未安装）                                   │
│                                                                 │
│    PowerShell执行：                                              │
│    (Invoke-WebRequest -Uri https://install.python-poetry.org   │
│     -UseBasicParsing).Content | python -                        │
│                                                                 │
│    📎 官方安装文档：                                              │
│    https://python-poetry.org/docs/#installation                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 2️⃣  安装项目依赖                                                 │
│                                                                 │
│    cd D:\\ETSY_Order_Automation\\backend                          │
│    poetry install                                               │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 3️⃣  激活虚拟环境                                                 │
│                                                                 │
│    poetry shell                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 4️⃣  配置环境变量                                                 │
│                                                                 │
│    复制 backend\\.env.example 为 backend\\.env                     │
│    填入邮箱、数据库等实际配置                                       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 5️⃣  验证安装                                                     │
│                                                                 │
│    poetry run python -c "import requests; print('✅ 安装成功')"   │
└─────────────────────────────────────────────────────────────────┘

💡 提示：
   • 代码规范请参考 .qoder/rules/code-standard.md
   • 项目说明请参考 README.md
   • 遇到问题请检查Python版本是否为3.10+

🔗 有用的链接：
   • Poetry文档：https://python-poetry.org/docs/
   • Python PEP8：https://peps.python.org/pep-0008/
   • Google Python风格指南：https://google.github.io/styleguide/pyguide.html
"""
    print(next_steps)


def main():
    """主函数 - 执行项目初始化"""
    # 打印欢迎横幅
    print_banner()
    
    # Step 1: 检测管理员权限
    print("🔍 正在检测运行权限...")
    if not check_admin_privileges():
        print("\n❌ 错误：权限不足！")
        print("💡 请右键点击脚本，选择「以管理员身份运行」")
        print("   或在管理员PowerShell中执行：python init_project.py")
        sys.exit(1)
    print("   ✅ 管理员权限验证通过")
    
    # Step 2: 设置项目根目录路径（使用pathlib避免反斜杠转义问题）
    base_path = Path("D:/ETSY_Order_Automation")
    backend_path = base_path / "backend"
    qoder_rules_path = base_path / ".qoder" / "rules"
    
    print(f"\n📍 项目根目录: {base_path}")
    
    # Step 3: 创建目录结构
    create_directory_structure(base_path)
    
    # Step 4: 生成配置文件
    create_pyproject_toml(backend_path)
    
    # Step 5: 生成代码规范文档
    create_code_standard(qoder_rules_path)
    
    # Step 6: 生成README
    create_readme(base_path)
    
    # Step 7: 生成环境变量示例
    create_env_example(backend_path)
    
    # Step 8: 生成.gitignore
    create_gitignore(base_path)
    
    # Step 9: 创建__init__.py文件
    create_init_files(base_path)
    
    # Step 10: 打印下一步操作指引
    print_next_steps()


if __name__ == "__main__":
    main()
