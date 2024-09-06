from pydantic import BaseModel
from datetime import datetime

class InscricaoBase(BaseModel):
    participante_id: int
    evento_id: int
    timestamp: datetime

class InscricaoCreate(InscricaoBase):
    pass
class Inscricao(InscricaoBase):
    id: int

    class Config:
        from_attributes = True
    