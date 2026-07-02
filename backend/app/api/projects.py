"""项目管理 API 路由"""

import os
import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.responses import FileResponse
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.config import settings
from app.core.deps import get_current_user
from app.models.user import User
from app.models.project import Project, ProjectFile
from app.schemas.project import (
    ProjectCreate, ProjectUpdate, ProjectOut, ProjectFileOut, PaginatedProjects,
)

router = APIRouter(prefix="/projects", tags=["项目管理"])


@router.get("", response_model=PaginatedProjects, summary="获取项目列表")
async def list_projects(
    page: int = 1,
    page_size: int = 20,
    keyword: str = "",
    db: AsyncSession = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    """获取项目列表（分页）"""
    query = select(Project)
    count_query = select(func.count(Project.id))

    if keyword:
        query = query.where(Project.name.contains(keyword))
        count_query = count_query.where(Project.name.contains(keyword))

    total_result = await db.execute(count_query)
    total = total_result.scalar()

    query = query.offset((page - 1) * page_size).limit(page_size).order_by(Project.id.desc())
    result = await db.execute(query)
    items = result.scalars().all()

    return PaginatedProjects(
        items=[ProjectOut.model_validate(p) for p in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{project_id}", response_model=ProjectOut, summary="获取项目详情")
async def get_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    return ProjectOut.model_validate(project)


@router.post("", response_model=ProjectOut, summary="创建项目")
async def create_project(
    data: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    project = Project(**data.model_dump(), created_by=user.id)
    db.add(project)
    await db.flush()
    await db.refresh(project)
    return ProjectOut.model_validate(project)


@router.put("/{project_id}", response_model=ProjectOut, summary="更新项目")
async def update_project(
    project_id: int,
    data: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(project, key, value)

    await db.flush()
    await db.refresh(project)
    return ProjectOut.model_validate(project)


@router.delete("/{project_id}", summary="删除项目")
async def delete_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")

    await db.delete(project)
    return {"detail": "删除成功"}


# === 项目文件管理 ===

@router.get("/{project_id}/files", summary="获取项目文件列表")
async def list_project_files(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(ProjectFile).where(ProjectFile.project_id == project_id).order_by(ProjectFile.uploaded_at.desc())
    )
    files = result.scalars().all()
    return {"items": [ProjectFileOut.model_validate(f) for f in files]}


@router.post("/{project_id}/files", response_model=ProjectFileOut, summary="上传项目文件")
async def upload_project_file(
    project_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    # 检查项目是否存在
    proj_result = await db.execute(select(Project).where(Project.id == project_id))
    if not proj_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="项目不存在")

    # 读取文件内容
    content = await file.read()
    if len(content) > settings.MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail=f"文件大小超过限制({settings.MAX_FILE_SIZE // 1024 // 1024}MB)")

    # 保存文件
    ext = os.path.splitext(file.filename or "")[1]
    saved_filename = f"{uuid.uuid4().hex}{ext}"
    upload_dir = os.path.join(settings.UPLOAD_DIR, str(project_id))
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, saved_filename)

    with open(file_path, "wb") as f:
        f.write(content)

    # 创建记录
    file_record = ProjectFile(
        project_id=project_id,
        filename=file.filename,
        file_type=ext.lstrip(".").lower(),
        file_url=f"/uploads/{project_id}/{saved_filename}",
        file_path=file_path,
        file_size=len(content),
        uploaded_by=user.id,
    )
    db.add(file_record)
    await db.flush()
    await db.refresh(file_record)
    return ProjectFileOut.model_validate(file_record)


@router.get("/{project_id}/files/{file_id}/download", summary="下载项目文件")
async def download_project_file(
    project_id: int,
    file_id: int,
    db: AsyncSession = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(ProjectFile).where(ProjectFile.id == file_id, ProjectFile.project_id == project_id)
    )
    file_record = result.scalar_one_or_none()
    if not file_record:
        raise HTTPException(status_code=404, detail="文件不存在")

    if not os.path.exists(file_record.file_path):
        raise HTTPException(status_code=404, detail="文件已丢失")

    return FileResponse(
        path=file_record.file_path,
        filename=file_record.filename,
        media_type="application/octet-stream",
    )


@router.delete("/{project_id}/files/{file_id}", summary="删除项目文件")
async def delete_project_file(
    project_id: int,
    file_id: int,
    db: AsyncSession = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(ProjectFile).where(ProjectFile.id == file_id, ProjectFile.project_id == project_id)
    )
    file_record = result.scalar_one_or_none()
    if not file_record:
        raise HTTPException(status_code=404, detail="文件不存在")

    # 删除物理文件
    if os.path.exists(file_record.file_path):
        os.remove(file_record.file_path)

    await db.delete(file_record)
    return {"detail": "删除成功"}
