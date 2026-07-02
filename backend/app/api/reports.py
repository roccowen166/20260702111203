"""报表导出 API 路由"""

import io
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.issue import Issue
from app.models.test_case import TestCase
from app.services.excel_service import ExcelService

router = APIRouter(prefix="/reports", tags=["报表导出"])


@router.get("/export-issues", summary="导出问题记录Excel")
async def export_issues(
    project_id: int | None = None,
    db: AsyncSession = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    query = select(Issue)
    if project_id:
        query = query.where(Issue.project_id == project_id)
    result = await db.execute(query.order_by(Issue.id.desc()))
    issues = result.scalars().all()

    wb = ExcelService.generate_issues_report(issues)
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)

    return StreamingResponse(
        buf,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=issues_report.xlsx"},
    )


@router.get("/export-test-cases", summary="导出测试用例Excel")
async def export_test_cases(
    project_id: int | None = None,
    status: str | None = None,
    db: AsyncSession = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    query = select(TestCase)
    if project_id:
        query = query.where(TestCase.project_id == project_id)
    if status:
        query = query.where(TestCase.status == status)
    result = await db.execute(query.order_by(TestCase.id.desc()))
    cases = result.scalars().all()

    wb = ExcelService.generate_test_cases_report(cases)
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)

    return StreamingResponse(
        buf,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=test_cases_report.xlsx"},
    )


@router.get("/export-all", summary="导出汇总报表Excel")
async def export_all(
    project_id: int | None = None,
    db: AsyncSession = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    issues_query = select(Issue)
    cases_query = select(TestCase)
    if project_id:
        issues_query = issues_query.where(Issue.project_id == project_id)
        cases_query = cases_query.where(TestCase.project_id == project_id)

    issues = (await db.execute(issues_query.order_by(Issue.id.desc()))).scalars().all()
    cases = (await db.execute(cases_query.order_by(TestCase.id.desc()))).scalars().all()

    wb = ExcelService.generate_summary_report(issues, cases)
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)

    return StreamingResponse(
        buf,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=summary_report.xlsx"},
    )
