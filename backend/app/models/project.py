"""项目模型"""

from datetime import datetime

from sqlalchemy import String, Text, DateTime, func, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Project(Base):
    """项目表"""

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, comment="项目名称")
    description: Mapped[str] = mapped_column(Text, default="", comment="项目描述")
    status: Mapped[str] = mapped_column(String(20), default="active", comment="状态: active/archived/draft")
    created_by: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True, comment="创建人ID")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间"
    )

    # 关联关系
    files = relationship("ProjectFile", back_populates="project", cascade="all, delete-orphan")
    issues = relationship("Issue", back_populates="project", cascade="all, delete-orphan")
    test_cases = relationship("TestCase", back_populates="project", cascade="all, delete-orphan")


class ProjectFile(Base):
    """项目文件表（原理图、图片等）"""

    __tablename__ = "project_files"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, comment="项目ID")
    filename: Mapped[str] = mapped_column(String(255), nullable=False, comment="文件名")
    file_type: Mapped[str] = mapped_column(String(50), default="", comment="文件类型")
    file_url: Mapped[str] = mapped_column(String(500), nullable=False, comment="文件访问URL")
    file_path: Mapped[str] = mapped_column(String(500), nullable=False, comment="文件存储路径")
    file_size: Mapped[int] = mapped_column(Integer, default=0, comment="文件大小(字节)")
    uploaded_by: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True, comment="上传人ID")
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), comment="上传时间")

    # 关联关系
    project = relationship("Project", back_populates="files")
