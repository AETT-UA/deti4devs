from loguru import logger
from itertools import starmap
from typing import (
    Any,
    Dict,
    Generic,
    Iterable,
    Optional,
    Sequence,
    Type,
    TypeVar,
    Union,
    Tuple,
)

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import select, delete, update
from fastapi.encoders import jsonable_encoder
from sqlalchemy.sql import ColumnCollection, ColumnElement
from psycopg2.errors import ForeignKeyViolation, UniqueViolation

from app.db.base_class import Base

_PrimaryKeyType = Union[Any, Tuple[Any, ...]]

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BadSelectorKey(Exception):
    pass


def _primary_key(
    model_name: str, id: _PrimaryKeyType, columns: ColumnCollection
) -> Sequence[ColumnElement]:
    cols_values = columns.values()
    if isinstance(id, Iterable):
        id_iter = iter(id)
        col_iter = iter(cols_values)

        selector = list(
            starmap(lambda col, id_sel: col == id_sel, zip(col_iter, id_iter))
        )

        if next(col_iter, None) is not None or next(id_iter, None) is not None:
            raise BadSelectorKey(
                "Mismatch in the length of the selector"
                " "
                f'and the primary key columns for "{model_name}"'
            )

        return selector
    else:
        if len(columns) != 1:
            raise BadSelectorKey(
                f'Selector only has one column but "{model_name}"'
                " "
                f"has {len(columns)} primary key columns",
            )

        return [cols_values[0] == id]


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    _foreign_key_checks = {}
    _unique_violation_msg = "Already exists"

    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model
        self.primary_key = self.model.__table__.primary_key.columns

    def _integrity_error_handler(self, e: IntegrityError):
        if isinstance(e.orig, ForeignKeyViolation):
            msg = self._foreign_key_checks.get(e.orig.diag.constraint_name, None)
            if msg is not None:
                raise HTTPException(status_code=400, detail=msg)
            else:
                logger.error("Unhandled foreign key violation")
        elif isinstance(e.orig, UniqueViolation):
            raise HTTPException(status_code=409, detail=self._unique_violation_msg)

    def get(
        self, db: Session, id: _PrimaryKeyType, for_update: bool = False
    ) -> Optional[ModelType]:
        return db.get(self.model, id, with_for_update=for_update)

    def get_multi(
        self,
        db: Session,
        *,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
        for_update: bool = False,
    ) -> Sequence[ModelType]:
        stmt = select(self.model).limit(limit).offset(skip)
        if for_update:
            stmt = stmt.with_for_update()

        return db.execute(stmt).scalars(stmt).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        try:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except IntegrityError as e:
            self._integrity_error_handler(e)
            raise e

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        try:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except IntegrityError as e:
            self._integrity_error_handler(e)
            raise e

    def update_locked(
        self,
        db: Session,
        *,
        id: _PrimaryKeyType,
        obj_in: UpdateSchemaType,
    ) -> Optional[ModelType]:
        update_data = obj_in.model_dump(exclude_unset=True)
        if len(update_data) != 0:
            stmt = update(self.model).values(update_data).returning(self.model)
        else:
            stmt = select(self.model)

        stmt = stmt.where(*_primary_key(self.model.__name__, id, self.primary_key))

        try:
            return db.execute(stmt).scalar_one_or_none()
        except IntegrityError as e:
            self._integrity_error_handler(e)
            raise e

    def delete(self, db: Session, *, id: _PrimaryKeyType) -> Optional[ModelType]:
        stmt = (
            delete(self.model)
            .where(*_primary_key(self.model.__name__, id, self.primary_key))
            .returning(self.model)
        )
        res = db.execute(stmt).one_or_none()
        if res is None:
            return None
        return res[0]