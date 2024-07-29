# Criei isto como exemplo para mostrar como ficaria a implementação de um CRUD

from app.crud.base import CRUDBase
from app.models.participantes import Participantes
from app.dtos.participantes_dto import ParticipantesDTO, ParticipantesCreateDTO, ParticipantesUpdateDTO

class CRUDStaff(CRUDBase[Participantes, 
                         ParticipantesDTO, 
                         ParticipantesCreateDTO, 
                         ParticipantesUpdateDTO]):
    pass
