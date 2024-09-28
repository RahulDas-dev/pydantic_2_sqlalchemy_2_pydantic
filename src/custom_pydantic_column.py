from typing import Optional

from pydantic import BaseModel, TypeAdapter  # pydantic version > 2.0.0
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.engine import Dialect
from sqlalchemy.types import JSON, TypeDecorator


class PydanticColumn(TypeDecorator):
    """PydanticColumn type.
    * for custom column type implementation check
    https://docs.sqlalchemy.org/en/20/core/custom_types.html
    * Uses sqlalchemy.dialects.postgresql.JSONB if dialects == postgresql
    else generic sqlalchemy.types.JSON
    * Saving:
        - Acceps the pydantic model and converts it to a dict on save.
        - SQLAlchemy engine JSON-encodes the dict to a string.
    * Loading:
        - Pulls the string from the database.
        - SQLAlchemy engine JSON-decodes the string to a dict.
        - Uses the dict to create a pydantic model.
    """

    impl = JSON
    cache_ok = True

    def __init__(self, pydantic_type: type[BaseModel]):
        super().__init__()
        if not issubclass(pydantic_type, BaseModel):
            raise ValueError("Column Type Should be Pydantic Class")
        self.pydantic_type = pydantic_type

    def load_dialect_impl(self, dialect: Dialect) -> TypeDecorator:
        # Use JSONB for PostgreSQL and JSON for other databases.
        return (
            dialect.type_descriptor(JSONB())
            if dialect.name == "postgresql"
            else dialect.type_descriptor(JSON())
        )

    def process_bind_param(
        self,
        value: Optional[BaseModel],
        dialect: Dialect,  # noqa: ARG002
    ) -> Optional[str]:
        # return value.dict() if value else None   # pydantic <2.0.0
        return value.model_dump() if value else None

    def process_result_value(
        self,
        value: Optional[dict],
        dialect: Dialect,  # noqa: ARG002
    ) -> Optional[BaseModel]:
        # return parse_obj_as(self.pydantic_type, value) if value else None # pydantic < 2.0.0
        return TypeAdapter(self.pydantic_type).validate_python(value)
