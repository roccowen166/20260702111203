"""FastAPI 应用入口"""

import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.database import init_db
from app.api import auth, projects, issues, test_cases, reports, users

logger = logging.getLogger("app.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期：启动时初始化数据库（连接失败不阻塞启动）"""
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    try:
        await init_db()
        from app.services.init_data import create_default_admin
        await create_default_admin()
        logger.info("数据库初始化成功")
    except Exception as e:
        logger.warning("数据库连接失败，服务以降级模式启动: %s", e)
    yield


app = FastAPI(
    title="标准测试流程系统 API",
    description="Standard Test Flow System - 基于 Vue3 + FastAPI + MySQL",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件服务（上传的文件）
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# 注册路由
api_prefix = "/api"
app.include_router(auth.router, prefix=api_prefix)
app.include_router(projects.router, prefix=api_prefix)
app.include_router(issues.router, prefix=api_prefix)
app.include_router(test_cases.router, prefix=api_prefix)
app.include_router(reports.router, prefix=api_prefix)
app.include_router(users.router, prefix=api_prefix)


@app.get("/", tags=["健康检查"])
async def root():
    return {"message": "标准测试流程系统 API", "docs": "/docs"}


@app.get("/health", tags=["健康检查"])
async def health():
    return {"status": "ok"}
