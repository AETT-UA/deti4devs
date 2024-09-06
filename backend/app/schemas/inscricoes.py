from pydantic import BaseModel
from datetime import datetime

class InscricaoResponse(BaseModel):
    id: int
    participante_id: int
    evento_id: int
    timestamp: datetime

    class Config:
        from_attributes = True
    