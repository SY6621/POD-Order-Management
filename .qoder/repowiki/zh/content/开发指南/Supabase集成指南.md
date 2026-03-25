# Supabase集成指南

<cite>
**本文档引用的文件**
- [backend/src/utils/logger.py](file://backend/src/utils/logger.py)
- [frontend/src/utils/supabase.js](file://frontend/src/utils/supabase.js)
- [backend/src/config/settings.py](file://backend/src/config/settings.py)
- [backend/.env](file://backend/.env)
- [frontend/.env](file://frontend/.env)
- [backend/scripts/check_supabase_resources.py](file://backend/scripts/check_supabase_resources.py)
- [backend/scripts/test_supabase_connection.py](file://backend/scripts/test_supabase_connection.py)
- [backend/scripts/upload_assets_to_supabase.py](file://backend/scripts/upload_assets_to_supabase.py)
- [backend/scripts/verify_storage.py](file://backend/scripts/verify_storage.py)
- [backend/src/services/database_service.py](file://backend/src/services/database_service.py)
- [backend/pyproject.toml](file://backend/pyproject.toml)
- [frontend/package.json](file://frontend/package.json)
- [backend/scripts/keep_supabase_alive.py](file://backend/scripts/keep_supabase_alive.py)
- [backend/scripts/list_storage_files.py](file://backend/scripts/list_storage_files.py)
- [backend/scripts/init_multitenant.py](file://backend/scripts/init_multitenant.py)
- [backend/scripts/create_tables_sql.md](file://backend/scripts/create_tables_sql.md)
- [backend/scripts/init_subaccount.sql](file://backend/scripts/init_subaccount.sql)
- [backend/scripts/init_multitenant.sql](file://backend/scripts/init_multitenant.sql)
- [frontend/src/stores/shopStore.js](file://frontend/src/stores/shopStore.js)
- [frontend/src/stores/adminStore.js](file://frontend/src/stores/adminStore.js)
- [frontend/src/views/StorePortal/StoreLogin.vue](file://frontend/src/views/StorePortal/StoreLogin.vue)
- [frontend/src/views/StorePortal/StoreOrders.vue](file://frontend/src/views/StorePortal/StoreOrders.vue)
- [frontend/src/views/Admin/AdminUsers.vue](file://frontend/src/views/Admin/AdminUsers.vue)
- [frontend/src/views/Admin/AdminShops.vue](file://frontend/src/views/Admin/AdminShops.vue)
- [frontend/src/views/Admin/AdminDashboard.vue](file://frontend/src/views/Admin/AdminDashboard.vue)
- [frontend/src/stores/orderStore.js](file://frontend/src/stores/orderStore.js)
- [frontend/public/designer-standalone.html](file://frontend/public/designer-standalone.html)
- [backend/src/models/order.py](file://backend/src/models/order.py)
- [backend/scripts/check_storage.py](file://backend/scripts/check_storage.py)
- [backend/scripts/add_operator_email.sql](file://backend/scripts/add_operator_email.sql)
- [docs/frontend-backend-api.md](file://docs/frontend-backend-api.md)
</cite>

## 更新摘要
**变更内容**
- 新增多租户架构章节，包含多店铺数据隔离和权限控制
- 增强权限管理和用户管理功能，支持主账号-子账号体系
- 更新数据库架构图，反映新的表结构和关系
- 新增子账号权限管理功能说明
- 更新前端多租户界面实现
- **新增** 订单存储功能重大改进：SVG格式图像处理、向量路径嵌入、错误处理增强
- **新增** 效果图存储架构：SVG向量图形与JPG位图双轨存储
- **新增** 设计器向量化功能：自动将文字转为SVG路径
- **新增** 生产文档表：支持PDF生成的完整文档链路

## 目录
1. [简介](#简介)
2. [项目结构概览](#项目结构概览)
3. [核心组件分析](#核心组件分析)
4. [多租户架构设计](#多租户架构设计)
5. [权限管理体系](#权限管理体系)
6. [订单存储架构](#订单存储架构)
7. [向量化图像处理](#向量化图像处理)
8. [错误处理增强](#错误处理增强)
9. [架构概览](#架构概览)
10. [详细组件分析](#详细组件分析)
11. [依赖关系分析](#依赖关系分析)
12. [性能考虑](#性能考虑)
13. [故障排除指南](#故障排除指南)
14. [结论](#结论)

## 简介

Supabase集成指南旨在为ETSY订单自动化系统提供完整的Supabase数据库和存储服务集成方案。该系统通过Supabase实现了订单数据管理、资源存储、以及前后端数据同步功能。

**更新** 系统现已引入多租户架构，支持多个商店的独立数据隔离和权限控制，增强了权限管理和用户管理功能。同时，订单存储功能得到重大改进，实现了SVG格式图像处理、向量路径嵌入和增强的错误处理机制。

Supabase是一个开源的Firebase替代方案，提供了PostgreSQL数据库、认证、存储等功能。在本项目中，Supabase被用来：

- 存储订单数据和业务逻辑
- 提供实时数据同步
- 管理静态资源文件
- 支持多租户和权限控制
- 实现主账号-子账号权限体系
- **新增** 支持向量化图像存储和处理

## 项目结构概览

项目采用前后端分离架构，Supabase作为后端数据层的核心组件：

```mermaid
graph TB
subgraph "前端应用"
FE[Vue.js前端应用]
FE_API[API接口调用]
FE_STORE[Pinia状态管理]
DESIGNER[独立设计器]
end
subgraph "后端服务"
BE[Python后端服务]
DB[Supabase数据库]
STORAGE[Supabase存储]
end
subgraph "多租户架构"
SHOPS[shops表 - 店铺信息]
USERS[users表 - 用户权限]
PERMISSIONS[user_shop_permissions表 - 权限关联]
ORDERS[orders表 - 订单数据]
PRODUCTION_DOCS[production_documents表 - 生产文档]
end
subgraph "存储架构"
EFFECT_IMAGES[effect-images存储桶 - SVG向量图]
TEMPLATES[templates存储桶 - 模板文件]
PHOTOS[photos存储桶 - 实拍图]
FONTS[fonts存储桶 - 字体文件]
end
subgraph "外部服务"
ETSY[ETSY平台]
EMAIL[邮件服务]
end
FE --> FE_API
FE_API --> BE
FE_STORE --> FE_API
DESIGNER --> FE_API
BE --> DB
DB --> SHOPS
DB --> USERS
DB --> PERMISSIONS
DB --> ORDERS
DB --> PRODUCTION_DOCS
BE --> STORAGE
STORAGE --> EFFECT_IMAGES
STORAGE --> TEMPLATES
STORAGE --> PHOTOS
STORAGE --> FONTS
ETSY --> BE
EMAIL --> BE
```

**图表来源**
- [frontend/src/stores/shopStore.js:1-190](file://frontend/src/stores/shopStore.js#L1-L190)
- [frontend/src/stores/adminStore.js:1-321](file://frontend/src/stores/adminStore.js#L1-L321)
- [backend/src/services/database_service.py:1-112](file://backend/src/services/database_service.py#L1-L112)
- [frontend/src/stores/orderStore.js:496-609](file://frontend/src/stores/orderStore.js#L496-L609)

**章节来源**
- [backend/src/config/settings.py:1-61](file://backend/src/config/settings.py#L1-L61)
- [backend/.env:1-8](file://backend/.env#L1-L8)
- [frontend/.env:1-4](file://frontend/.env#L1-L4)

## 核心组件分析

### 配置管理系统

配置管理模块负责统一管理Supabase连接参数和环境变量：

```mermaid
classDiagram
class Settings {
+str IMAP_SERVER
+int IMAP_PORT
+str EMAIL_ADDRESS
+str EMAIL_PASSWORD
+str SUPABASE_URL
+str SUPABASE_KEY
+str LOG_LEVEL
+Path ASSETS_DIR
+Path TEMPLATES_DIR
+Path FONTS_DIR
+Path OUTPUT_DIR
+validate() bool
+validate_supabase() bool
+ensure_output_dir() Path
}
class DatabaseService {
-Client _client
-DatabaseService _instance
+__new__() DatabaseService
+__init__() void
+insert(table, data) Dict
+select(table, filters, limit) List
+update(table, filters, data) Dict
+upload_file(bucket, file_path, dest_name) str
}
Settings --> DatabaseService : "提供配置"
```

**图表来源**
- [backend/src/config/settings.py:12-61](file://backend/src/config/settings.py#L12-L61)
- [backend/src/services/database_service.py:10-112](file://backend/src/services/database_service.py#L10-L112)

### 前端Supabase客户端

前端通过专门的客户端模块管理Supabase连接：

```mermaid
sequenceDiagram
participant App as 应用程序
participant Config as 环境配置
participant Client as Supabase客户端
participant API as Supabase API
App->>Config : 读取VITE_SUPABASE_URL
App->>Config : 读取VITE_SUPABASE_KEY
Config-->>App : 返回配置参数
App->>Client : createClient(URL, KEY)
Client->>API : 初始化连接
API-->>Client : 连接成功
Client-->>App : 导出客户端实例
```

**图表来源**
- [frontend/src/utils/supabase.js:1-18](file://frontend/src/utils/supabase.js#L1-L18)

**章节来源**
- [backend/src/config/settings.py:18-19](file://backend/src/config/settings.py#L18-L19)
- [frontend/src/utils/supabase.js:4-13](file://frontend/src/utils/supabase.js#L4-L13)

## 多租户架构设计

### 数据库架构

系统采用多租户架构，通过独立的表结构实现数据隔离：

```mermaid
erDiagram
SHOPS {
UUID id PK
VARCHAR name
VARCHAR code UK
VARCHAR region
VARCHAR password_hash
VARCHAR api_key
VARCHAR status
TIMESTAMP created_at
TIMESTAMP updated_at
}
USERS {
UUID id PK
VARCHAR username UK
VARCHAR password_hash
VARCHAR role
UUID shop_id FK
VARCHAR email
VARCHAR status
TIMESTAMP last_login_at
TIMESTAMP created_at
TIMESTAMP updated_at
}
USER_SHOP_PERMISSIONS {
UUID id PK
UUID user_id FK
UUID shop_id FK
UUID granted_by FK
TIMESTAMP granted_at
JSONB permissions
}
ORDERS {
UUID id PK
UUID shop_id FK
VARCHAR shop_order_id
VARCHAR etsy_order_id
VARCHAR status
JSONB order_data
TIMESTAMP created_at
TIMESTAMP updated_at
}
SHOP_ACCESS_LOGS {
UUID id PK
UUID shop_id FK
VARCHAR action
INET ip_address
TEXT user_agent
TIMESTAMP created_at
}
SHOPS ||--o{ ORDERS : contains
SHOPS ||--o{ USER_SHOP_PERMISSIONS : grants
USERS ||--o{ USER_SHOP_PERMISSIONS : has
USERS ||--o{ SHOP_ACCESS_LOGS : generates
```

**图表来源**
- [backend/scripts/create_tables_sql.md:1-114](file://backend/scripts/create_tables_sql.md#L1-L114)
- [backend/scripts/init_subaccount.sql:28-38](file://backend/scripts/init_subaccount.sql#L28-L38)

### 多租户数据隔离

多租户架构通过以下机制实现数据隔离：

1. **店铺维度隔离**: 所有数据都与特定店铺关联
2. **权限控制**: 通过用户角色和权限表控制访问范围
3. **订单关联**: 订单数据通过shop_id字段与店铺绑定
4. **访问日志**: 记录每个店铺的操作历史

**章节来源**
- [backend/scripts/create_tables_sql.md:1-114](file://backend/scripts/create_tables_sql.md#L1-L114)
- [backend/scripts/init_multitenant.py:29-102](file://backend/scripts/init_multitenant.py#L29-L102)

## 权限管理体系

### 角色定义

系统支持以下角色类型：

| 角色 | 描述 | 权限范围 |
|------|------|----------|
| admin | 系统管理员 | 全部店铺，全部功能 |
| store_operator | 店铺运营人员 | 自身店铺，订单管理 |
| factory | 工厂操作员 | 工厂相关功能 |
| main | 主账号 | 管理子账号，分配权限 |
| sub | 子账号 | 分配的店铺权限 |

### 权限控制机制

```mermaid
flowchart TD
Start([用户登录]) --> CheckRole{"检查用户角色"}
CheckRole --> Admin["admin - 系统管理员"]
CheckRole --> StoreOperator["store_operator - 店铺运营"]
CheckRole --> Factory["factory - 工厂操作员"]
CheckRole --> Main["main - 主账号"]
CheckRole --> Sub["sub - 子账号"]
Admin --> FullAccess["完全访问权限"]
StoreOperator --> ShopAccess["仅自身店铺访问"]
Factory --> FactoryAccess["工厂功能访问"]
Main --> ManageSub["管理子账号权限"]
Sub --> AssignedAccess["根据权限分配访问"]
ShopAccess --> FilterOrders["按shop_id过滤订单"]
AssignedAccess --> CheckPermission["检查user_shop_permissions"]
FilterOrders --> AccessGranted["访问权限授予"]
CheckPermission --> AccessGranted
```

**图表来源**
- [backend/scripts/init_subaccount.sql:20-21](file://backend/scripts/init_subaccount.sql#L20-L21)

### 子账号权限管理

系统支持主账号-子账号的层级权限体系：

1. **主账号**: 拥有最高权限，可以管理子账号
2. **子账号**: 通过主账号授权，获得特定店铺的访问权限
3. **权限继承**: 子账号继承主账号的部分管理能力
4. **权限审计**: 记录所有权限变更和操作日志

**章节来源**
- [backend/scripts/init_subaccount.sql:1-90](file://backend/scripts/init_subaccount.sql#L1-L90)
- [frontend/src/views/Admin/AdminUsers.vue:146-359](file://frontend/src/views/Admin/AdminUsers.vue#L146-L359)

## 订单存储架构

### 存储桶设计

系统采用多存储桶架构，针对不同类型的资源进行专业化管理：

```mermaid
graph TB
subgraph "存储桶架构"
EFFECT_IMAGES[effect-images<br/>SVG向量图存储]
TEMPLATES[templates<br/>SVG模板文件]
PHOTOS[photos<br/>产品实拍图]
FONTS[fonts<br/>字体文件]
ASSETS[assets<br/>通用资源]
end
subgraph "存储策略"
VECTOR[向量化存储<br/>SVG格式，无损缩放]
RASTER[位图存储<br/>JPG/PNG格式]
FONT[字体存储<br/>TTF/OTF格式]
end
EFFECT_IMAGES --> VECTOR
TEMPLATES --> VECTOR
PHOTOS --> RASTER
FONTS --> FONT
ASSETS --> VECTOR
ASSETS --> RASTER
```

**图表来源**
- [backend/scripts/upload_assets_to_supabase.py:47-55](file://backend/scripts/upload_assets_to_supabase.py#L47-L55)

### 效果图存储流程

系统实现了双轨存储架构，支持SVG向量图和JPG位图两种格式：

```mermaid
sequenceDiagram
participant Designer as 设计器
participant OrderStore as 订单存储
participant Storage as Supabase Storage
participant OrdersTable as Orders表
participant ProdDocsTable as Production Documents表
Designer->>OrderStore : 保存SVG效果图
OrderStore->>Storage : 上传SVG文件
Storage-->>OrderStore : 返回文件URL
OrderStore->>OrdersTable : 更新effect_image_url
OrdersTable-->>OrderStore : 订单记录更新
OrderStore->>ProdDocsTable : 同步保存effect_svg_url
ProdDocsTable-->>OrderStore : 生产文档更新
OrderStore-->>Designer : 返回存储结果
```

**图表来源**
- [frontend/src/stores/orderStore.js:496-609](file://frontend/src/stores/orderStore.js#L496-L609)

**章节来源**
- [frontend/src/stores/orderStore.js:496-609](file://frontend/src/stores/orderStore.js#L496-L609)
- [backend/src/models/order.py:147-171](file://backend/src/models/order.py#L147-L171)

## 向量化图像处理

### SVG向量化功能

系统集成了先进的向量化图像处理功能，能够将位图图像转换为SVG矢量格式：

```mermaid
flowchart TD
Start([图像输入]) --> Preprocess["预处理<br/>二值化处理"]
Preprocess --> TraceOutline["轮廓追踪<br/>Marching Squares算法"]
TraceOutline --> SimplifyPath["路径简化<br/>Douglas-Peucker算法"]
SimplifyPath --> GenerateSVG["生成SVG路径<br/>M/L/Z命令"]
GenerateSVG --> OptimizeSVG["SVG优化<br/>路径合并"]
OptimizeSVG --> VectorizeText["文本向量化<br/>字体转路径"]
VectorizeText --> FinalSVG["最终SVG输出"]
FinalSVG --> UploadStorage["上传到Storage"]
```

**图表来源**
- [frontend/public/designer-standalone.html:1011-1153](file://frontend/public/designer-standalone.html#L1011-L1153)

### 向量化算法实现

系统实现了完整的向量化处理管道：

1. **二值化处理**: 将彩色图像转换为黑白二值图像
2. **轮廓追踪**: 使用简化版Marching Squares算法追踪边缘
3. **路径简化**: 应用Douglas-Peucker算法减少路径点数
4. **SVG生成**: 将路径点转换为SVG path命令
5. **文本向量化**: 将字体转换为可编辑的SVG路径

**章节来源**
- [frontend/public/designer-standalone.html:1011-1153](file://frontend/public/designer-standalone.html#L1011-L1153)

## 错误处理增强

### 异常处理架构

系统实现了多层次的错误处理机制，确保数据一致性和用户体验：

```mermaid
flowchart TD
Error([错误发生]) --> TryBlock["Try块<br/>主要操作"]
TryBlock --> Success{"操作成功?"}
Success --> |是| SuccessHandler["成功处理<br/>更新本地状态"]
Success --> |否| ErrorHandler["错误处理<br/>捕获异常"]
ErrorHandler --> LogError["记录错误日志<br/>console.error"]
LogError --> UserMessage["用户提示<br/>error.value"]
UserMessage --> Cleanup["清理操作<br/>loading=false"]
Cleanup --> ReThrow["重新抛出<br/>throw err"]
SuccessHandler --> Cleanup
ReThrow --> End([结束])
```

**图表来源**
- [frontend/src/stores/orderStore.js:502-609](file://frontend/src/stores/orderStore.js#L502-L609)

### 错误处理策略

系统采用了以下错误处理策略：

1. **渐进式错误处理**: 对于可选操作（如生产文档更新）使用try-catch包装
2. **用户友好提示**: 通过error.value向用户显示错误信息
3. **日志记录**: 使用console.error记录详细的错误信息
4. **状态清理**: 在finally块中确保loading状态正确清理
5. **部分成功处理**: 即使部分操作失败，也尽量保证数据一致性

**章节来源**
- [frontend/src/stores/orderStore.js:502-609](file://frontend/src/stores/orderStore.js#L502-L609)

## 架构概览

系统采用分层架构设计，Supabase作为数据基础设施层：

```mermaid
graph TB
subgraph "表现层"
UI[用户界面]
API[REST API]
STORE[Pinia状态管理]
DESIGNER[独立设计器]
end
subgraph "业务逻辑层"
OrderService[订单服务]
EmailService[邮件服务]
PDFService[PDF服务]
ShopService[店铺服务]
UserService[用户服务]
EffectImageService[效果图像服务]
DesignService[设计服务]
end
subgraph "数据访问层"
DBService[数据库服务]
StorageService[存储服务]
AuthManager[认证管理器]
PermissionManager[权限管理器]
EffectImageManager[效果图像管理器]
DesignDataManager[设计数据管理器]
end
subgraph "多租户管理层"
TenantManager[多租户管理器]
PermissionManager
end
subgraph "Supabase基础设施"
PostgreSQL[PostgreSQL数据库]
Storage[对象存储]
Auth[认证服务]
Realtime[实时订阅]
end
UI --> API
API --> STORE
STORE --> OrderService
OrderService --> DBService
EmailService --> DBService
PDFService --> StorageService
ShopService --> PermissionManager
UserService --> AuthManager
EffectImageService --> EffectImageManager
DesignService --> DesignDataManager
DBService --> PostgreSQL
StorageService --> Storage
DBService --> Auth
DBService --> Realtime
PermissionManager --> TenantManager
TenantManager --> PostgreSQL
EffectImageManager --> Storage
DesignDataManager --> Storage
```

**图表来源**
- [backend/src/services/database_service.py:1-112](file://backend/src/services/database_service.py#L1-L112)
- [frontend/src/stores/shopStore.js:1-190](file://frontend/src/stores/shopStore.js#L1-L190)
- [frontend/src/stores/adminStore.js:1-321](file://frontend/src/stores/adminStore.js#L1-L321)

## 详细组件分析

### 数据库服务组件

数据库服务组件提供了统一的Supabase访问接口：

#### 核心功能

1. **连接管理**: 单例模式确保只有一个数据库连接实例
2. **CRUD操作**: 提供标准的数据增删改查方法
3. **文件上传**: 集成Supabase Storage进行文件管理
4. **订单管理**: 特化的订单数据操作方法
5. **多租户支持**: 自动处理店铺数据隔离

#### 数据库操作流程

```mermaid
flowchart TD
Start([开始操作]) --> CheckConfig["检查Supabase配置"]
CheckConfig --> ConfigValid{"配置有效?"}
ConfigValid --> |否| ThrowError["抛出配置错误"]
ConfigValid --> |是| CreateClient["创建数据库客户端"]
CreateClient --> Operation{"选择操作类型"}
Operation --> Insert["插入数据"]
Operation --> Select["查询数据"]
Operation --> Update["更新数据"]
Insert --> InsertExec["执行插入操作"]
Select --> SelectExec["执行查询操作"]
Update --> UpdateExec["执行更新操作"]
InsertExec --> InsertSuccess{"操作成功?"}
SelectExec --> SelectSuccess{"查询成功?"}
UpdateExec --> UpdateSuccess{"更新成功?"}
InsertSuccess --> |是| ReturnData["返回数据"]
InsertSuccess --> |否| HandleError["处理错误"]
SelectSuccess --> |是| ReturnList["返回列表"]
SelectSuccess --> |否| HandleError
UpdateSuccess --> |是| ReturnUpdated["返回更新结果"]
UpdateSuccess --> |否| HandleError
HandleError --> End([结束])
ReturnData --> End
ReturnList --> End
ReturnUpdated --> End
ThrowError --> End
```

**图表来源**
- [backend/src/services/database_service.py:27-62](file://backend/src/services/database_service.py#L27-L62)

**章节来源**
- [backend/src/services/database_service.py:1-112](file://backend/src/services/database_service.py#L1-L112)

### 资源上传组件

资源上传组件负责将本地资源文件上传到Supabase Storage：

#### 上传流程

```mermaid
sequenceDiagram
participant Script as 上传脚本
participant FS as 本地文件系统
participant Storage as Supabase Storage
participant DB as 数据库
Script->>FS : 遍历资源目录
FS-->>Script : 返回文件列表
Script->>Storage : 创建Bucket(如不存在)
Storage-->>Script : Bucket状态
loop 遍历每个文件
Script->>FS : 读取文件内容
FS-->>Script : 文件字节流
Script->>Storage : 上传文件
Storage-->>Script : 上传结果
Script->>DB : 更新文件元数据
DB-->>Script : 更新完成
end
Script-->>Script : 生成访问URL
```

**图表来源**
- [backend/scripts/upload_assets_to_supabase.py:39-66](file://backend/scripts/upload_assets_to_supabase.py#L39-L66)

#### 支持的资源类型

| 资源类型 | 目录结构 | 文件扩展名 | MIME类型 |
|---------|----------|------------|----------|
| 模板文件 | templates/ | .svg | image/svg+xml |
| 实拍图片 | photos/ | .jpg, .jpeg, .png | image/jpeg, image/png |
| 字体文件 | fonts/ | .ttf, .otf | font/ttf, font/otf |
| PDF文件 | output/ | .pdf | application/pdf |

**章节来源**
- [backend/scripts/upload_assets_to_supabase.py:46-55](file://backend/scripts/upload_assets_to_supabase.py#L46-L55)

### 连接测试组件

连接测试组件用于验证Supabase连接的可用性：

#### 测试流程

```mermaid
flowchart TD
TestStart([开始连接测试]) --> LoadEnv["加载环境变量"]
LoadEnv --> CheckEnv{"检查配置完整?"}
CheckEnv --> |否| EnvError["输出配置错误"]
CheckEnv --> |是| CreateClient["创建Supabase客户端"]
CreateClient --> TestConnection["测试数据库连接"]
TestConnection --> ConnectionOK{"连接成功?"}
ConnectionOK --> |否| ConnError["连接失败"]
ConnectionOK --> |是| TestQuery["执行查询测试"]
TestQuery --> QueryOK{"查询成功?"}
QueryOK --> |否| QueryError["查询失败"]
QueryOK --> |是| TestComplete["测试完成"]
EnvError --> TestEnd([结束])
ConnError --> TestEnd
QueryError --> TestEnd
TestComplete --> TestEnd
```

**图表来源**
- [backend/scripts/test_supabase_connection.py:19-64](file://backend/scripts/test_supabase_connection.py#L19-L64)

**章节来源**
- [backend/scripts/test_supabase_connection.py:1-67](file://backend/scripts/test_supabase_connection.py#L1-L67)

### 资源检查组件

资源检查组件用于验证Supabase中的数据完整性：

#### 检查流程

```mermaid
flowchart TD
CheckStart([开始资源检查]) --> ListTables["列出数据库表"]
ListTables --> CheckTemplates["检查templates表"]
CheckTemplates --> CheckPhotos["检查product_photos表"]
CheckPhotos --> CheckSKU["检查sku_mapping表"]
CheckSKU --> CheckFonts["检查fonts表"]
CheckFonts --> ListBuckets["列出Storage buckets"]
ListBuckets --> CheckBucketStatus["检查bucket状态"]
CheckBucketStatus --> GenerateReport["生成检查报告"]
GenerateReport --> CheckEnd([检查完成])
```

**图表来源**
- [backend/scripts/check_supabase_resources.py:14-58](file://backend/scripts/check_supabase_resources.py#L14-L58)

**章节来源**
- [backend/scripts/check_supabase_resources.py:1-62](file://backend/scripts/check_supabase_resources.py#L1-L62)

### 多租户初始化组件

多租户初始化组件负责设置数据库结构和默认数据：

#### 初始化流程

```mermaid
sequenceDiagram
participant InitScript as 初始化脚本
participant DB as Supabase数据库
participant ShopsTable as shops表
participant UsersTable as users表
participant OrdersTable as orders表
InitScript->>DB : 检查表结构
DB-->>InitScript : 返回表状态
alt shops表不存在
InitScript->>DB : 创建shops表
DB-->>InitScript : 表创建成功
else users表不存在
InitScript->>DB : 创建users表
DB-->>InitScript : 表创建成功
else orders表不存在
InitScript->>DB : 扩展orders表
DB-->>InitScript : 列添加成功
end
InitScript->>DB : 插入默认店铺数据
DB-->>InitScript : 数据插入成功
InitScript-->>InitScript : 初始化完成
```

**图表来源**
- [backend/scripts/init_multitenant.py:15-112](file://backend/scripts/init_multitenant.py#L15-L112)

**章节来源**
- [backend/scripts/init_multitenant.py:1-112](file://backend/scripts/init_multitenant.py#L1-L112)

### 效果图像存储组件

**新增** 效果图像存储组件负责管理SVG向量图像的完整生命周期：

#### 存储流程

```mermaid
sequenceDiagram
participant OrderStore as 订单存储
participant Storage as Supabase Storage
participant OrdersTable as Orders表
participant ProdDocsTable as Production Documents表
OrderStore->>OrderStore : 创建SVG Blob
OrderStore->>Storage : 上传SVG文件
Storage-->>OrderStore : 返回文件URL
OrderStore->>OrdersTable : 更新effect_image_url
OrdersTable-->>OrderStore : 订单记录更新
OrderStore->>ProdDocsTable : 同步保存effect_svg_url
ProdDocsTable-->>OrderStore : 生产文档更新
OrderStore-->>OrderStore : 更新本地缓存
OrderStore-->>Client : 返回存储结果
```

**图表来源**
- [frontend/src/stores/orderStore.js:496-609](file://frontend/src/stores/orderStore.js#L496-L609)

**章节来源**
- [frontend/src/stores/orderStore.js:496-609](file://frontend/src/stores/orderStore.js#L496-L609)

## 依赖关系分析

### 后端依赖

后端项目使用Poetry管理依赖，Supabase相关依赖如下：

```mermaid
graph TB
subgraph "后端依赖树"
Poetry[Poetry项目]
subgraph "核心依赖"
Supabase[supabase ^2.27.2]
Requests[requests ^2.31.0]
FastAPI[fastapi ^0.128.2]
SQLAlchemy[sqlalchemy ^2.0.0]
end
subgraph "开发依赖"
PyTest[pytest ^8.0.0]
Black[black ^24.1.1]
Pylint[pylint ^3.0.3]
end
end
Poetry --> Supabase
Poetry --> Requests
Poetry --> FastAPI
Poetry --> SQLAlchemy
Poetry --> PyTest
Poetry --> Black
Poetry --> Pylint
```

**图表来源**
- [backend/pyproject.toml:32-35](file://backend/pyproject.toml#L32-L35)

### 前端依赖

前端项目使用npm管理依赖，Supabase相关依赖：

```mermaid
graph TB
subgraph "前端依赖树"
NPM[npm项目]
subgraph "核心依赖"
SupabaseJS[@supabase/supabase-js ^2.93.3]
Vue[vue ^3.5.24]
ElementPlus[element-plus ^2.13.2]
Pinia[Pinia ^2.3.0]
end
subgraph "开发依赖"
Vite[vite ^7.2.4]
TailwindCSS[tailwindcss ^4.2.1]
end
end
NPM --> SupabaseJS
NPM --> Vue
NPM --> ElementPlus
NPM --> Pinia
NPM --> Vite
NPM --> TailwindCSS
```

**图表来源**
- [frontend/package.json:13-20](file://frontend/package.json#L13-L20)

**章节来源**
- [backend/pyproject.toml:1-69](file://backend/pyproject.toml#L1-L69)
- [frontend/package.json:1-31](file://frontend/package.json#L1-L31)

## 性能考虑

### 连接优化

1. **连接池管理**: 使用单例模式避免重复创建数据库连接
2. **超时设置**: 合理设置数据库操作超时时间
3. **批量操作**: 对于大量数据操作使用批量处理

### 存储优化

1. **文件压缩**: 上传前对图片进行适当压缩
2. **缓存策略**: 利用CDN缓存静态资源
3. **分块上传**: 对于大文件使用分块上传机制
4. **向量化优势**: SVG格式无损缩放，减少存储空间
5. **双轨存储**: 向量图用于高精度显示，位图用于兼容性

### 查询优化

1. **索引设计**: 为常用查询字段建立索引
2. **分页查询**: 对大数据集使用分页机制
3. **条件过滤**: 使用WHERE条件减少数据传输
4. **多租户查询**: 通过shop_id字段实现高效过滤
5. **存储桶优化**: 针对不同存储桶类型优化查询

### 多租户性能优化

1. **权限缓存**: 缓存用户权限信息减少数据库查询
2. **数据分区**: 按店铺ID分区存储订单数据
3. **并发控制**: 实现租户间的并发访问控制
4. **监控指标**: 监控各店铺的资源使用情况

### 向量化性能优化

1. **路径简化**: 使用Douglas-Peucker算法减少SVG路径点数
2. **内存管理**: 优化图像处理过程中的内存使用
3. **异步处理**: 将耗时的向量化操作异步化
4. **缓存机制**: 缓存常用的向量化结果

## 故障排除指南

### 常见问题及解决方案

#### 连接问题

| 问题症状 | 可能原因 | 解决方案 |
|---------|----------|----------|
| 连接超时 | 网络不稳定 | 检查网络连接，增加重试机制 |
| 认证失败 | 密钥错误 | 验证SUPABASE_URL和SUPABASE_KEY配置 |
| 数据库不可用 | 服务暂停 | 运行保活脚本或检查服务状态 |

#### 多租户问题

| 问题症状 | 可能原因 | 解决方案 |
|---------|----------|----------|
| 数据隔离失效 | shop_id字段缺失 | 检查orders表结构，添加shop_id列 |
| 权限错误 | 用户权限配置错误 | 验证user_shop_permissions表数据 |
| 店铺访问失败 | 店铺状态异常 | 检查shops表status字段 |
| 子账号权限不生效 | 权限缓存问题 | 清除权限缓存，重新登录 |

#### 存储问题

| 问题症状 | 可能原因 | 解决方案 |
|---------|----------|----------|
| 上传失败 | 权限不足 | 检查bucket权限设置 |
| 文件丢失 | 存储空间不足 | 清理不需要的文件 |
| 访问被拒绝 | CORS配置 | 配置正确的CORS规则 |
| SVG文件损坏 | 向量化失败 | 检查图像质量和向量化参数 |

#### 数据完整性问题

```mermaid
flowchart TD
Problem([发现问题]) --> IdentifyType{"识别问题类型"}
IdentifyType --> ConnectionIssue["连接问题"]
IdentifyType --> MultiTenantIssue["多租户问题"]
IdentifyType --> StorageIssue["存储问题"]
IdentifyType --> DataIssue["数据问题"]
ConnectionIssue --> CheckEnv["检查环境配置"]
CheckEnv --> TestConn["运行连接测试"]
TestConn --> FixConfig["修复配置问题"]
MultiTenantIssue --> CheckStructure["检查数据库结构"]
CheckStructure --> VerifyPermissions["验证权限配置"]
VerifyPermissions --> FixPermissions["修复权限问题"]
StorageIssue --> VerifyBucket["验证bucket状态"]
VerifyBucket --> CheckPermission["检查权限设置"]
CheckPermission --> FixPermission["修复权限问题"]
DataIssue --> ValidateSchema["验证数据结构"]
ValidateSchema --> CheckConstraints["检查约束条件"]
CheckConstraints --> FixData["修复数据问题"]
FixConfig --> Monitor["监控系统状态"]
FixPermissions --> Monitor
FixPermission --> Monitor
FixData --> Monitor
Monitor --> Resolution([问题解决])
```

**图表来源**
- [backend/scripts/test_supabase_connection.py:29-31](file://backend/scripts/test_supabase_connection.py#L29-L31)
- [backend/scripts/verify_storage.py:14-35](file://backend/scripts/verify_storage.py#L14-L35)

#### 向量化问题

| 问题症状 | 可能原因 | 解决方案 |
|---------|----------|----------|
| SVG生成失败 | 图像质量差 | 提供高质量的输入图像 |
| 路径过于复杂 | 文字过多 | 简化设计内容 |
| 向量化速度慢 | 图像过大 | 优化图像尺寸 |
| 字体渲染异常 | 字体文件缺失 | 确保字体文件完整上传 |

**章节来源**
- [backend/scripts/keep_supabase_alive.py:18-48](file://backend/scripts/keep_supabase_alive.py#L18-L48)
- [backend/scripts/list_storage_files.py:14-52](file://backend/scripts/list_storage_files.py#L14-L52)

### 调试工具

系统提供了多种调试工具来帮助诊断问题：

1. **连接测试**: 验证Supabase连接的可用性
2. **资源检查**: 检查数据库表和存储桶的状态
3. **文件验证**: 验证存储中的文件完整性
4. **保活脚本**: 确保数据库服务保持活跃状态
5. **多租户检查**: 验证数据库结构和权限配置
6. **存储检查**: 验证Storage桶的配置和访问权限

**章节来源**
- [backend/scripts/check_supabase_resources.py:14-58](file://backend/scripts/check_supabase_resources.py#L14-L58)
- [backend/scripts/verify_storage.py:14-56](file://backend/scripts/verify_storage.py#L14-L56)

## 结论

Supabase集成为ETSY订单自动化系统提供了强大的数据基础设施。通过引入多租户架构，系统现在能够支持多个商店的独立数据隔离和权限控制，增强了系统的可扩展性和安全性。

**更新** 系统的订单存储功能得到了重大改进，实现了SVG格式图像处理、向量路径嵌入和增强的错误处理机制。这些改进不仅提升了用户体验，还为后续的PDF生成和生产文档管理奠定了坚实基础。

### 关键优势

1. **可靠性**: 使用单例模式和连接池管理确保连接稳定性
2. **可扩展性**: 支持水平扩展和分布式部署
3. **安全性**: 内置认证和授权机制，实现严格的多租户隔离
4. **易用性**: 提供直观的API和丰富的工具链
5. **灵活性**: 支持主账号-子账号的灵活权限管理
6. **向量化优势**: SVG格式提供无损缩放和高精度显示
7. **错误处理**: 多层次的异常处理确保系统稳定性

### 多租户架构优势

1. **数据隔离**: 每个店铺的数据完全独立，互不影响
2. **权限控制**: 精细的权限粒度，支持复杂的权限组合
3. **审计跟踪**: 完整的操作日志，便于合规审计
4. **性能优化**: 针对多租户场景的查询优化
5. **扩展性**: 支持动态添加新店铺和用户

### 订单存储架构优势

1. **向量化存储**: SVG格式提供无损缩放和高精度显示
2. **双轨存储**: 同时支持向量图和位图，满足不同需求
3. **智能同步**: 自动同步到生产文档表，支持PDF生成
4. **错误容错**: 多层次错误处理确保数据一致性
5. **性能优化**: 路径简化和内存管理提升处理效率

### 最佳实践建议

1. **配置管理**: 使用环境变量管理敏感信息
2. **错误处理**: 实现完善的异常处理和日志记录
3. **性能监控**: 建立性能指标监控体系
4. **备份策略**: 制定定期备份和恢复计划
5. **权限管理**: 定期审查和更新用户权限
6. **安全审计**: 建立完善的安全审计机制
7. **向量化优化**: 定期优化向量化算法和参数
8. **存储管理**: 建立存储桶的生命周期管理策略

通过遵循这些指导原则，可以确保Supabase集成在生产环境中稳定可靠地运行，为多租户订单自动化系统提供坚实的技术基础。新增的向量化图像处理功能和增强的错误处理机制将进一步提升系统的专业性和用户体验。