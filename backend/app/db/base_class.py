import re

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr
from app.core.config import settings

convention = {
    "ix": "ix_%(column_0N_label)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_N_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=convention)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Generate table name automatically from class name.

        e.g.: `TestingTable` converts to `testing_table`.
        """
        names = re.findall(r"[A-Z][a-z]+|[A-Z]+(?![a-z])", cls.__name__)
        return "_".join(names).lower()

    @declared_attr.directive
    def __table_args__(cls):
        return {"schema": settings.SCHEMA_NAME}

    def dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}