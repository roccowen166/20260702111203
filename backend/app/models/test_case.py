"""测试用例模型"""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import String, Text, DateTime, func, ForeignKey, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class TestCase(Base):
    """测试用例表"""

    __tablename__ = "test_cases"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True, comment="项目ID")
    title: Mapped[str] = mapped_column(String(200), nullable=False, comment="用例标题")
    description: Mapped[str] = mapped_column(Text, default="", comment="用例描述")
    preconditions: Mapped[str] = mapped_column(Text, default="", comment="前置条件")
    steps: Mapped[list] = mapped_column(JSON, default=list, comment="测试步骤JSON")
    priority: Mapped[str] = mapped_column(String(20), default="medium", comment="优先级: low/medium/high")
    status: Mapped[str] = mapped_column(String(20), default="draft", comment="状态: draft/active/deprecated")
    created_by: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True, comment="创建人ID")
    created_by_name: Mapped[str] = mapped_column(String(100), default="", comment="创建人姓名")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间"
    )

    # 关联关系
    project = relationship("Project", back_populates="test_cases")
