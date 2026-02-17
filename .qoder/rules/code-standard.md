# ETSY订单自动化系统 - 代码规范

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
- 示例：`MAX_RETRY_COUNT`, `DEFAULT_TIMEOUT`, `API_BASE_URL`

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
