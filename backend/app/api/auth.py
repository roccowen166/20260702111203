"""认证 API 路由"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.user import LoginRequest, Token, UserCreate, UserOut

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/login", response_model=Token, summary="邮箱密码登录")
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    """用户邮箱密码登录，返回 JWT Token"""
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码错误",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户已被禁用",
        )

    access_token = create_access_token(data={"sub": user.email})
    return Token(
        access_token=access_token,
        user=UserOut.model_validate(user),
    )


@router.post("/register", response_model=UserOut, summary="注册用户")
async def register(
    data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    """注册新用户（首个用户自动成为管理员）"""
    # 检查邮箱是否已存在
    result = await db.execute(select(User).where(User.email == data.email))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该邮箱已被注册",
        )

    # 检查是否是首个用户（自动设为管理员）
    count_result = await db.execute(select(User))
    is_first_user = count_result.scalars().first() is None

    user = User(
        email=data.email,
        hashed_password=get_password_hash(data.password),
        full_name=data.full_name,
        role="admin" if is_first_user else data.role,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return UserOut.model_validate(user)


@router.get("/me", response_model=UserOut, summary="获取当前用户信息")
async def me(current_user: User = Depends(get_current_user)):
    """获取当前登录用户信息"""
    return UserOut.model_validate(current_user)
