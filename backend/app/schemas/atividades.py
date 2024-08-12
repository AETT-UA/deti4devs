from pydantic import BaseModel
from typing import Optional

class AtividadeBase(BaseModel):
    nome: str
    pontos: Optional[int] = 0

class AtividadeCreate(AtividadeBase):
    pass

class AtividadeUpdate(AtividadeBase):
    pass

class Atividade(AtividadeBase):
    id: int

    class Config:
        orm_mode = True
