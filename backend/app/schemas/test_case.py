"""测试用例 Pydantic 模型"""

from datetime import datetime
from pydantic import BaseModel, Field


class TestCaseStep(BaseModel):
    step_no: int = Field(..., ge=1)
    action: str = Field(..., min_length=1)
    expected_result: str = ""


class TestCaseBase(BaseModel):
    project_id: int
    title: str = Field(..., min_length=1, max_length=200)
    description: str = ""
    preconditions: str = ""
    steps: list[TestCaseStep] = []
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")
    status: str = Field(default="draft", pattern="^(draft|active|deprecated)$")


class TestCaseCreate(TestCaseBase):
    pass


class TestCaseUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = None
    preconditions: str | None = None
    steps: list[TestCaseStep] | None = None
    priority: str | None = Field(None, pattern="^(low|medium|high)$")
    status: str | None = Field(None, pattern="^(draft|active|deprecated)$")


class TestCaseOut(TestCaseBase):
    id: int
    created_by: int | None
    created_by_name: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PaginatedTestCases(BaseModel):
    items: list[TestCaseOut]
    total: int
    page: int
    page_size: int
