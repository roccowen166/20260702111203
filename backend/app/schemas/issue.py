"""问题记录 Pydantic 模型"""

from datetime import datetime
from pydantic import BaseModel, Field


class IssueBase(BaseModel):
    project_id: int
    title: str = Field(..., min_length=1, max_length=200)
    description: str = ""
    severity: str = Field(default="medium", pattern="^(low|medium|high|critical)$")
    status: str = Field(default="open", pattern="^(open|in_progress|resolved|closed)$")
    reporter: str = ""
    assignee: str = ""


class IssueCreate(IssueBase):
    pass


class IssueUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = None
    severity: str | None = Field(None, pattern="^(low|medium|high|critical)$")
    status: str | None = Field(None, pattern="^(open|in_progress|resolved|closed)$")
    reporter: str | None = None
    assignee: str | None = None


class IssueOut(IssueBase):
    id: int
    created_by: int | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PaginatedIssues(BaseModel):
    items: list[IssueOut]
    total: int
    page: int
    page_size: int
