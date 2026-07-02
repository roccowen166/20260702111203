"""初始化默认数据"""

import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal
from app.core.security import get_password_hash
from app.models.user import User

logger = logging.getLogger(__name__)


async def create_default_admin():
    """创建默认管理员账号（如不存在）"""
    async with AsyncSessionLocal() as db:  # type: AsyncSession
        # 检查是否已有用户
        result = await db.execute(select(User).limit(1))
        if result.scalar_one_or_none():
            return

        # 创建默认管理员
        admin = User(
            email="admin@test.com",
            hashed_password=get_password_hash("123456"),
            full_name="系统管理员",
            role="admin",
        )
        db.add(admin)
        await db.commit()
        logger.info("默认管理员已创建: admin@test.com / 123456")
