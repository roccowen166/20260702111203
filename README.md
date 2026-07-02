# 标准测试流程系统 (Standard Test Flow System)

基于 Vue3 + FastAPI + MySQL 的标准测试流程管理系统。

## 技术栈

### 前端
- Vue 3 + Vite + TypeScript
- Element Plus (UI 组件库)
- Tailwind CSS (原子化 CSS)
- Vue Router (路由)
- Pinia (状态管理)
- Axios (HTTP 请求)

### 后端
- Python FastAPI (异步 Web 框架)
- SQLAlchemy 2.0 (async ORM)
- aiomysql (MySQL 异步驱动)
- python-jose (JWT 认证)
- passlib[bcrypt] (密码加密)
- Pydantic v2 (数据校验)
- openpyxl (Excel 导出)
- Alembic (数据库迁移)

### 数据库
- MySQL 8.0

## 项目结构

```
20260702111203/
├── frontend/          # Vue3 前端项目
│   ├── src/
│   │   ├── api/       # API 请求封装
│   │   ├── assets/    # 静态资源
│   │   ├── components/# 公共组件
│   │   ├── layouts/   # 布局组件
│   │   ├── router/    # 路由配置
│   │   ├── stores/    # Pinia 状态管理
│   │   ├── views/     # 页面视图
│   │   ├── App.vue
│   │   └── main.ts
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── tailwind.config.js
│
├── backend/           # FastAPI 后端项目
│   ├── app/
│   │   ├── api/       # API 路由
│   │   ├── core/      # 核心配置(安全/数据库/依赖)
│   │   ├── models/    # SQLAlchemy 模型
│   │   ├── schemas/   # Pydantic 模型
│   │   ├── services/  # 业务逻辑
│   │   ├── utils/     # 工具函数
│   │   ├── uploads/   # 上传文件目录
│   │   └── main.py    # 应用入口
│   ├── alembic/       # 数据库迁移
│   ├── requirements.txt
│   └── .env.example
│
├── docker-compose.yml # Docker 一键部署 (MySQL + 后端 + 前端)
├── README.md
└── .gitignore
```

## 部署方式

### 方式一：Docker 一键部署（推荐）

> 前提：已安装 Docker 和 Docker Compose

```bash
# 在项目根目录执行，一键启动所有服务
docker-compose up -d --build
```

启动完成后：
- **前端**: http://localhost (端口 80)
- **后端 API 文档**: http://localhost:8000/docs
- **MySQL**: localhost:3306

**默认管理员账号**: `admin@test.com` / `123456`

常用命令：
```bash
docker-compose up -d --build      # 构建并后台启动
docker-compose logs -f backend    # 查看后端日志
docker-compose logs -f frontend   # 查看前端日志
docker-compose down               # 停止所有服务
docker-compose down -v            # 停止并删除数据卷（慎用，会清空数据）
```

### 方式二：本地开发模式

#### 1. 启动 MySQL 数据库

```bash
docker-compose up -d mysql
```

#### 2. 启动后端

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 3. 启动前端

```bash
cd frontend
npm install
npm run dev
```

#### 4. 访问系统

- 前端: http://localhost:5173
- 后端 API 文档: http://localhost:8000/docs

## 功能模块

1. **用户登录** - 邮箱+密码登录，JWT 认证，管理员/普通用户角色
2. **项目管理** - 项目列表选择，原理图/图片上传下载
3. **问题记录** - 历史问题汇总，新建/编辑问题记录
4. **测试用例** - 历史测试用例汇总，动态步骤新建
5. **报表导出** - 问题+用例 Excel 汇总导出
