---
name: standard-test-flow-system
overview: 构建一个基于 Vue.js + Node.js + MySQL 的标准测试流程系统，包含人员登录、项目管理与资料下载、问题记录管理、测试用例管理、以及 Excel 报表导出功能，支持管理员和普通用户两种角色。
design:
  architecture:
    framework: vue
  styleKeywords:
    - Enterprise Dashboard
    - Clean Professional
    - Card-based Layout
    - Data-driven Interface
  fontSystem:
    fontFamily: PingFang SC
    heading:
      size: 20px
      weight: 600
    subheading:
      size: 16px
      weight: 500
    body:
      size: 14px
      weight: 400
  colorSystem:
    primary:
      - "#409EFF"
      - "#337ecc"
    background:
      - "#F5F7FA"
      - "#FFFFFF"
    text:
      - "#303133"
      - "#606266"
      - "#909399"
    functional:
      - "#67C23A"
      - "#E6A23C"
      - "#F56C6C"
todos:
  - id: init-project
    content: 初始化Vue3+Vite前端项目和Node.js+Express后端项目结构
    status: pending
  - id: setup-database
    content: 设计并创建MySQL数据库表结构和SequORM模型定义
    status: pending
    dependencies:
      - init-project
  - id: auth-module
    content: 实现JWT登录认证系统和角色权限中间件
    status: pending
    dependencies:
      - setup-database
  - id: project-module
    content: 开发项目管理和资料上传下载功能（API+前端页面）
    status: pending
    dependencies:
      - auth-module
  - id: issue-module
    content: 开发问题记录管理模块（历史列表+新建编辑+状态流转）
    status: pending
    dependencies:
      - project-module
  - id: testcase-module
    content: 开发测试用例管理模块（历史汇总+动态步骤表单）
    status: pending
    dependencies:
      - project-module
  - id: report-export
    content: 使用xlsx skill开发Excel报表汇总导出功能
    status: pending
    dependencies:
      - issue-module
      - testcase-module
  - id: integration-test
    content: 全流程集成测试和UI细节优化
    status: pending
    dependencies:
      - report-export
---

## 产品概述

一个标准测试流程管理系统，用于测试团队进行项目测试工作的全流程管理，包括项目资料下载、问题记录管理、测试用例管理以及报表汇总导出功能。

## 核心功能

- **用户登录与权限管理**：支持管理员和普通用户两种角色登录，不同角色拥有不同的操作权限
- **项目管理**：登录后选择对应项目，查看并下载该项目的原理图和相关图片资料
- **问题记录管理**：展示历史问题记录汇总列表，支持新建、编辑、删除问题记录
- **测试用例管理**：展示历史测试用例和测试问题记录汇总，支持创建新的测试用例
- **报表导出**：将问题记录和测试用例记录汇总后导出为Excel表格文件

## 用户角色权限

- **管理员**：用户管理、项目管理、所有数据的增删改查、报表导出
- **普通用户**：查看分配的项目、下载项目资料、创建/编辑自己的问题记录和测试用例、导出报表

## 技术栈选型

| 层级 | 技术选型 | 说明 |
| --- | --- | --- |
| 前端框架 | Vue 3 + TypeScript | 现代化响应式框架，组合式API |
| UI组件库 | Element Plus | 企业级Vue3组件库，表格/表单丰富 |
| 构建工具 | Vite | 快速构建和热更新 |
| 状态管理 | Pinia | Vue3官方推荐状态管理 |
| 后端框架 | Node.js + Express | 轻量级RESTful API服务 |
| 数据库 | MySQL 8.0 | 关系型数据库，稳定可靠 |
| ORM | Sequelize | Node.js成熟ORM框架 |
| 文件存储 | 本地文件系统 / Multer | 项目资料的上传和下载 |
| Excel导出 | exceljs | 服务端生成Excel文件 |
| 认证 | JWT (jsonwebtoken) | 无状态身份验证 |


## 实现方案

采用前后端分离架构，前端Vue3单页应用通过RESTful API与Node.js后端通信。系统按模块划分为认证模块、项目模块、问题记录模块、测试用例模块和报表模块。

### 核心技术决策

1. **Sequelize ORM**：相比原生SQL，提供模型定义、迁移、关联查询能力，便于维护
2. **JWT Token认证**：无状态设计，适合前后端分离架构，Token存储在localStorage
3. **Multer中间件**：处理项目资料（原理图/图片）的上传存储
4. **exceljs库**：支持样式设置、合并单元格等高级Excel功能，满足报表需求
5. **Element Plus**：提供完整的Table、Form、Dialog、Upload等企业级组件

### 数据库核心表设计

- users: 用户表(id, username, password, role, created_at)
- projects: 项目表(id, name, description, created_by, created_at)
- project_files: 项目资料表(id, project_id, file_name, file_path, file_type, created_at)
- issues: 问题记录表(id, project_id, user_id, title, description, status, priority, created_at)
- test_cases: 测试用例表(id, project_id, user_id, title, steps, expected_result, actual_result, status, created_at)

## 目录结构

```
c:/Users/Admin/CodeBuddy/20260702111203/
├── client/                          # 前端Vue3项目
│   ├── src/
│   │   ├── api/                     # API请求封装
│   │   │   ├── request.ts           # Axios实例和拦截器
│   │   │   ├── auth.ts              # 认证相关API
│   │   │   ├── project.ts           # 项目相关API
│   │   │   ├── issue.ts             # 问题记录API
│   │   │   ├── testCase.ts          # 测试用例API
│   │   │   └── report.ts            # 报表导出API
│   │   ├── views/                   # 页面视图
│   │   │   ├── Login.vue            # 登录页面
│   │   │   ├── Dashboard.vue        # 首页仪表盘
│   │   │   ├── ProjectSelect.vue    # 项目选择页
│   │   │   ├── ProjectDetail.vue    # 项目详情+资料下载
│   │   │   ├── IssueList.vue        # 问题记录列表
│   │   │   ├── IssueForm.vue        # 新建/编辑问题记录
│   │   │   ├── TestCaseList.vue     # 测试用例列表
│   │   │   ├── TestCaseForm.vue     # 新建/测试用例
│   │   │   └── ReportExport.vue     # 报表汇总导出
│   │   ├── components/              # 公共组件
│   │   │   ├── AppHeader.vue       # 顶部导航栏
│   │   │   ├── AppSidebar.vue      # 侧边菜单栏
│   │   │   ├── FileDownload.vue    # 文件下载组件
│   │   │   └── DataTable.vue       # 通用数据表格
│   │   ├── stores/                  # Pinia状态管理
│   │   │   ├── user.ts             # 用户状态
│   │   │   ├── project.ts          # 项目状态
│   │   │   └── app.ts              # 应用全局状态
│   │   ├── router/                 # Vue Router路由
│   │   │   └── index.ts
│   │   ├── types/                  # TypeScript类型定义
│   │   │   ├── user.d.ts
│   │   │   ├── project.d.ts
│   │   │   ├── issue.d.ts
│   │   │   └── testCase.d.ts
│   │   ├── utils/                  # 工具函数
│   │   │   └── index.ts
│   │   ├── App.vue
│   │   └── main.ts
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
├── server/                          # 后端Node.js项目
│   ├── src/
│   │   ├── config/                 # 配置文件
│   │   │   ├── database.ts         # 数据库配置
│   │   │   └── config.ts           # 应用配置
│   │   ├── controllers/            # 控制器层
│   │   │   ├── auth.controller.ts  # 认证控制器
│   │   │   ├── project.controller.ts
│   │   │   ├── issue.controller.ts
│   │   │   ├── testCase.controller.ts
│   │   │   └── report.controller.ts
│   │   ├── models/                 # Sequelize数据模型
│   │   │   ├── User.model.ts
│   │   │   ├── Project.model.ts
│   │   │   ├── ProjectFile.model.ts
│   │   │   ├── Issue.model.ts
│   │   │   └── TestCase.model.ts
│   │   ├── routes/                 # 路由定义
│   │   │   ├── index.ts
│   │   │   ├── auth.routes.ts
│   │   │   ├── project.routes.ts
│   │   │   ├── issue.routes.ts
│   │   │   ├── testCase.routes.ts
│   │   │   └── report.routes.ts
│   │   ├── middleware/             # 中间件
│   │   │   ├── auth.middleware.ts  # JWT认证中间件
│   │   │   ├── role.middleware.ts  # 角色权限中间件
│   │   │   └── upload.middleware.ts# 文件上传中间件
│   │   ├── services/               # 业务逻辑层
│   │   │   ├── auth.service.ts
│   │   │   ├── project.service.ts
│   │   │   ├── issue.service.ts
│   │   │   ├── testCase.service.ts
│   │   │   └── report.service.ts
│   │   ├── utils/                  # 工具函数
│   │   │   └── excelGenerator.ts   # Excel生成工具
│   │   └── app.ts                  # Express应用入口
│   ├── uploads/                    # 上传文件存储目录
│   ├── package.json
│   └── tsconfig.json
├── database/                        # 数据库初始化
│   └── init.sql                    # 初始化SQL脚本
└── README.md                        # 项目说明文档
```

## 关键实现说明

1. **性能优化**：列表接口分页查询，避免全量数据加载；前端使用虚拟滚动处理大数据量表格
2. **安全性**：密码bcrypt加密存储；JWT Token过期机制；API输入参数校验；文件上传类型和大小限制
3. **文件下载**：项目资料通过流式传输下载，支持批量打包下载
4. **Excel导出**：服务端使用exceljs生成格式化的Excel，包含表头样式、条件格式、自动列宽

## 设计风格

采用现代企业级管理后台设计风格，以清晰的功能导向为核心，配合专业的视觉呈现。整体界面布局为经典的后台管理模式：左侧固定导航菜单 + 右侧内容区域，顶部包含面包屑导航和用户信息栏。界面注重信息层次分明，操作流程清晰直观，配色专业稳重，适合测试管理场景的日常使用。

## 页面规划（5个核心页面）

### 页面1：登录页面

- 全屏居中卡片式登录框
- 包含Logo区域、账号密码输入框、登录按钮
- 支持记住登录状态选项
- 底部显示系统名称和版本信息

### 页面2：项目工作台（首页）

- 顶部统计卡片行：显示当前项目数、待处理问题数、测试用例完成率
- 我的项目列表区：以卡片网格形式展示已参与项目
- 最近动态时间线：最近的问题记录和测试用例更新
- 快捷操作入口：快速进入问题记录或测试用例页面

### 页面3：项目详情与资料中心

- 项目基本信息展示区（名称、描述、负责人、创建时间）
- 资料文件列表区：以表格形式列出原理图和图片资料，含预览缩略图
- 批量下载按钮：支持勾选多个文件一键打包下载
- 单个文件下载：每行带独立下载按钮

### 页面4：问题记录管理中心

- 左侧筛选面板：按状态（新建/处理中/已解决/已关闭）、优先级、日期范围筛选
- 主区域数据表格：展示问题ID、标题、项目、负责人、状态、优先级、创建时间
- 顶部操作栏：新建按钮 + 批量操作 + 搜索框
- 新建/编辑弹窗：表单含标题、描述(富文本)、优先级选择、附件上传、状态流转

### 页面5：测试用例管理中心

- 布局同问题记录页，保持一致的操作体验
- 表格额外展示：执行步骤数、预期结果、实际结果、通过/失败状态标识
- 测试用例弹窗：步骤可动态增删的表单，每步含操作描述和预期结果
- 页面6：报表汇总导出
- 导出配置面板：选择项目范围、时间范围、数据类型（问题/用例/全部）
- 预览区域：实时预览将要导出的数据概览
- 导出按钮触发Excel文件下载
- 历史导出记录列表

## Agent Extensions

### Skill

- **xlsx**
- Purpose: 用于系统第4步的Excel报表导出功能开发和测试验证
- Expected outcome: 实现问题记录和测试用例记录的Excel格式化导出，支持自定义样式、多工作表、数据筛选等功能