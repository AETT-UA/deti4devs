from pydantic import BaseModel, root_validator  # Import root_validator
from typing import Optional
from .atividades import AtividadeBase
from .users import UserCreate, User
from datetime import datetime

class EmpresaBase(AtividadeBase):
    sponsor_type: str
    spotlight_time: Optional[datetime]

class EmpresaCreate(EmpresaBase):
    user: Optional[UserCreate] = None
    user_id: Optional[int] = None

    @root_validator(pre=True)
    def check_user(cls, values):
        user = values.get("user")
        user_id = values.get("user_id")
        if user is not None and user_id is not None:
            raise ValueError("user and user_id are mutually exclusive")
        if user is None and user_id is None:
            raise ValueError("user or user_id is required")
        return values

class EmpresaUpdate(EmpresaBase):
    user_id: Optional[int]

class Empresa(EmpresaBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
