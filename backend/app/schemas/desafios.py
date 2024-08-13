from pydantic import BaseModel
from typing import Optional
from .atividades import AtividadeBase

class DesafioBase(AtividadeBase):
    descricao: str
    #empresa_id: int

class DesafioCreate(DesafioBase):
    pass

class DesafioUpdate(DesafioBase):
    pass

class Desafio(DesafioBase):
    id: int

    class Config:
        from_attributes = True
