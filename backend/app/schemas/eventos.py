from pydantic import BaseModel
from typing import Optional
from .atividades import AtividadeBase


class EventoBase(AtividadeBase):
    tipo:str
    empresa_id:int
class EventoUpdate(EventoBase):
    pass
class EventoCreate(EventoBase):
    pass
class Evento(EventoBase):
    id:int
    class Config:
        pass