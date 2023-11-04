from typing import Optional

from sqlalchemy import Enum, MetaData, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.custom_pydantic_column import PydanticColumn
from src.pydantic_model import DatasetDescriptor, ProjecStatus, ProjecType

meta = MetaData()


class Base(DeclarativeBase):
    metadata = meta


class Projects(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    descriptions: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True, default=None
    )
    ptype: Mapped[ProjecType] = mapped_column(Enum(ProjecType), nullable=False)
    status: Mapped[ProjecStatus] = mapped_column(Enum(ProjecStatus), nullable=False)
    dataset_info: Mapped[Optional[DatasetDescriptor]] = mapped_column(
        PydanticColumn(DatasetDescriptor), nullable=True
    )
