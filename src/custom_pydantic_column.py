from pydantic import BaseModel, TypeAdapter  # pydantic version > 2.0.0
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import JSON, TypeDecorator

# from pydantic import parse_obj_as               # pydantic version <2.0.0


class PydanticColumn(TypeDecorator):
    """
    PydanticColumn type.
    * for custom column type implementation check https://docs.sqlalchemy.org/en/20/core/custom_types.html
    * Uses sqlalchemy.dialects.postgresql.JSONB if dialects == postgresql else generic sqlalchemy.types.JSON
    SAVING:
        - Uses SQLAlchemy JSON type under the hood.
        - Acceps the pydantic model and converts it to a dict on save.
        - SQLAlchemy engine JSON-encodes the dict to a string.
    RETRIEVING:
        - Pulls the string from the database.
        - SQLAlchemy engine JSON-decodes the string to a dict.
        - Uses the dict to create a pydantic model.
    """

    impl = JSON
    cache_ok = True

    def __init__(self, pydantic_type):
        super().__init__()
        if not issubclass(pydantic_type, BaseModel):
            raise ValueError("Column Type Should be Pydantic Class")
        self.pydantic_type = pydantic_type

    def load_dialect_impl(self, dialect):
        # Use JSONB for PostgreSQL and JSON for other databases.
        if dialect.name == "postgresql":
            return dialect.type_descriptor(JSONB())
        else:
            return dialect.type_descriptor(JSON())

    def process_bind_param(self, value, dialect):
        # return value.dict() if value else None
        return value.model_dump() if value else None

    def process_result_value(self, value, dialect):
        # return parse_obj_as(self.pydantic_type, value) if value else None
        return TypeAdapter(self.pydantic_type).validate_python(value)
