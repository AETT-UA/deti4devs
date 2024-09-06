from pydantic import BaseModel
from typing import Optional
from .atividades import AtividadeBase


class EventoBase(AtividadeBase):
    tipo:str
    empresa_id:int
    lotacao_max:int
class EventoUpdate(EventoBase):
    pass
class EventoCreate(EventoBase):
    pass
class Evento(EventoBase):
    lotacao:int
    id:int
    class Config:
        from_attributes = True