from typing import Optional, List

from pydantic import BaseModel

from app.core.config import settings

class ParticipantesDTO(BaseModel):
    ...
    
class ParticipantesCreateDTO(BaseModel):
    ...
    
class ParticipantesUpdateDTO(BaseModel):
    ...
    