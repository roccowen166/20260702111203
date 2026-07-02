"""测试用例 API 路由"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.test_case import TestCase
from app.schemas.test_case import TestCaseCreate, TestCaseUpdate, TestCaseOut, PaginatedTestCases

router = APIRouter(prefix="/test-cases", tags=["测试用例"])


@router.get("", response_model=PaginatedTestCases, summary="获取测试用例列表")
async def list_test_cases(
    page: int = 1,
    page_size: int = 20,
    project_id: int | None = None,
    status: str | None = None,
    priority: str | None = None,
    keyword: str = "",
    db: AsyncSession = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    query = select(TestCase)
    count_query = select(func.count(TestCase.id))

    if project_id:
        query = query.where(TestCase.project_id == project_id)
        count_query = count_query.where(TestCase.project_id == project_id)

    if status:
        query = query.where(TestCase.status == status)
        count_query = count_query.where(TestCase.status == status)

    if priority:
        query = query.where(TestCase.priority == priority)
        count_query = count_query.where(TestCase.priority == priority)

    if keyword:
        query = query.where(TestCase.title.contains(keyword))
        count_query = count_query.where(TestCase.title.contains(keyword))

    total = (await db.execute(count_query)).scalar()
    result = await db.execute(
        query.offset((page - 1) * page_size).limit(page_size).order_by(TestCase.id.desc())
    )
    items = result.scalars().all()

    return PaginatedTestCases(
        items=[TestCaseOut.model_validate(t) for t in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{case_id}", response_model=TestCaseOut, summary="获取测试用例详情")
async def get_test_case(
    case_id: int,
    db: AsyncSession = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    result = await db.execute(select(TestCase).where(TestCase.id == case_id))
    case = result.scalar_one_or_none()
    if not case:
        raise HTTPException(status_code=404, detail="测试用例不存在")
    return TestCaseOut.model_validate(case)


@router.post("", response_model=TestCaseOut, summary="创建测试用例")
async def create_test_case(
    data: TestCaseCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    # 序列化步骤数据
    steps_data = [s.model_dump() if hasattr(s, "model_dump") else s for s in data.steps]

    case = TestCase(
        **{k: v for k, v in data.model_dump().items() if k != "steps"},
        steps=steps_data,
        created_by=user.id,
        created_by_name=user.full_name,
    )
    db.add(case)
    await db.flush()
    await db.refresh(case)
    return TestCaseOut.model_validate(case)


@router.put("/{case_id}", response_model=TestCaseOut, summary="更新测试用例")
async def update_test_case(
    case_id: int,
    data: TestCaseUpdate,
    db: AsyncSession = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    result = await db.execute(select(TestCase).where(TestCase.id == case_id))
    case = result.scalar_one_or_none()
    if not case:
        raise HTTPException(status_code=404, detail="测试用例不存在")

    update_data = data.model_dump(exclude_unset=True)
    if "steps" in update_data and update_data["steps"] is not None:
        update_data["steps"] = [
            s.model_dump() if hasattr(s, "model_dump") else s
            for s in update_data["steps"]
        ]

    for key, value in update_data.items():
        setattr(case, key, value)

    await db.flush()
    await db.refresh(case)
    return TestCaseOut.model_validate(case)


@router.delete("/{case_id}", summary="删除测试用例")
async def delete_test_case(
    case_id: int,
    db: AsyncSession = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    result = await db.execute(select(TestCase).where(TestCase.id == case_id))
    case = result.scalar_one_or_none()
    if not case:
        raise HTTPException(status_code=404, detail="测试用例不存在")
    await db.delete(case)
    return {"detail": "删除成功"}
