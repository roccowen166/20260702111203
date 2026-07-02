"""问题记录 API 路由"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.issue import Issue
from app.schemas.issue import IssueCreate, IssueUpdate, IssueOut, PaginatedIssues

router = APIRouter(prefix="/issues", tags=["问题记录"])


@router.get("", response_model=PaginatedIssues, summary="获取问题列表")
async def list_issues(
    page: int = 1,
    page_size: int = 20,
    project_id: int | None = None,
    status: str | None = None,
    severity: str | None = None,
    keyword: str = "",
    db: AsyncSession = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    query = select(Issue)
    count_query = select(func.count(Issue.id))

    if project_id:
        query = query.where(Issue.project_id == project_id)
        count_query = count_query.where(Issue.project_id == project_id)

    if status:
        query = query.where(Issue.status == status)
        count_query = count_query.where(Issue.status == status)

    if severity:
        query = query.where(Issue.severity == severity)
        count_query = count_query.where(Issue.severity == severity)

    if keyword:
        query = query.where(Issue.title.contains(keyword))
        count_query = count_query.where(Issue.title.contains(keyword))

    total = (await db.execute(count_query)).scalar()
    result = await db.execute(
        query.offset((page - 1) * page_size).limit(page_size).order_by(Issue.id.desc())
    )
    items = result.scalars().all()

    return PaginatedIssues(
        items=[IssueOut.model_validate(i) for i in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{issue_id}", response_model=IssueOut, summary="获取问题详情")
async def get_issue(
    issue_id: int,
    db: AsyncSession = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    result = await db.execute(select(Issue).where(Issue.id == issue_id))
    issue = result.scalar_one_or_none()
    if not issue:
        raise HTTPException(status_code=404, detail="问题不存在")
    return IssueOut.model_validate(issue)


@router.post("", response_model=IssueOut, summary="创建问题记录")
async def create_issue(
    data: IssueCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    issue = Issue(**data.model_dump(), created_by=user.id)
    if not issue.reporter:
        issue.reporter = user.full_name
    db.add(issue)
    await db.flush()
    await db.refresh(issue)
    return IssueOut.model_validate(issue)


@router.put("/{issue_id}", response_model=IssueOut, summary="更新问题记录")
async def update_issue(
    issue_id: int,
    data: IssueUpdate,
    db: AsyncSession = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    result = await db.execute(select(Issue).where(Issue.id == issue_id))
    issue = result.scalar_one_or_none()
    if not issue:
        raise HTTPException(status_code=404, detail="问题不存在")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(issue, key, value)

    await db.flush()
    await db.refresh(issue)
    return IssueOut.model_validate(issue)


@router.delete("/{issue_id}", summary="删除问题记录")
async def delete_issue(
    issue_id: int,
    db: AsyncSession = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    result = await db.execute(select(Issue).where(Issue.id == issue_id))
    issue = result.scalar_one_or_none()
    if not issue:
        raise HTTPException(status_code=404, detail="问题不存在")
    await db.delete(issue)
    return {"detail": "删除成功"}
