from pydantic import BaseModel
from typing import Optional

class AtividadeBase(BaseModel):
    nome: str
    pontos: Optional[int] = 0
