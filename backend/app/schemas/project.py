"""项目相关 Pydantic 模型"""

from datetime import datetime
from pydantic import BaseModel, Field


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str = ""
    status: str = "active"


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = None
    status: str | None = None


class ProjectOut(ProjectBase):
    id: int
    created_by: int | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ProjectFileOut(BaseModel):
    id: int
    project_id: int
    filename: str
    file_type: str
    file_url: str
    file_size: int
    uploaded_at: datetime

    model_config = {"from_attributes": True}


class PaginatedProjects(BaseModel):
    items: list[ProjectOut]
    total: int
    page: int
    page_size: int
