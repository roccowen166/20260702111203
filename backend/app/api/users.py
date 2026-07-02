"""用户管理 API 路由"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_admin
from app.models.user import User
from app.schemas.user import UserOut, UserUpdate

router = APIRouter(prefix="/users", tags=["用户管理"])


@router.get("", summary="获取用户列表")
async def list_users(
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    result = await db.execute(select(User).order_by(User.id))
    users = result.scalars().all()
    return {"items": [UserOut.model_validate(u) for u in users]}


@router.put("/{user_id}", response_model=UserOut, summary="更新用户")
async def update_user(
    user_id: int,
    data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(user, key, value)

    await db.flush()
    await db.refresh(user)
    return UserOut.model_validate(user)
