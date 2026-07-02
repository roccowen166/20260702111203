"""问题记录模型"""

from datetime import datetime

from sqlalchemy import String, Text, DateTime, func, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Issue(Base):
    """问题记录表"""

    __tablename__ = "issues"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True, comment="项目ID")
    title: Mapped[str] = mapped_column(String(200), nullable=False, comment="问题标题")
    description: Mapped[str] = mapped_column(Text, default="", comment="问题描述")
    severity: Mapped[str] = mapped_column(String(20), default="medium", comment="严重程度: low/medium/high/critical")
    status: Mapped[str] = mapped_column(String(20), default="open", comment="状态: open/in_progress/resolved/closed")
    reporter: Mapped[str] = mapped_column(String(100), default="", comment="报告人")
    assignee: Mapped[str] = mapped_column(String(100), default="", comment="负责人")
    created_by: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True, comment="创建人ID")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间"
    )

    # 关联关系
    project = relationship("Project", back_populates="issues")
