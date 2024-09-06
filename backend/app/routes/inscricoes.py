from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.auth import get_current_active_user
from app.dependencies.database import get_db
from ..models.users import Users
from ..models.inscricoes_eventos import Inscricoes
from ..schemas.inscricoes import Inscricao,InscricaoCreate
from sqlalchemy.orm import Session
import sqlalchemy

router = APIRouter(
    prefix="/incricoes",
    tags=["incrições"],
    responses={404: {"description": "Not found"}}
)

"""
This is the file where you should implement some CRUD
operations (update not included) to manage the 'incricoes' table.
It should be only accessible to privileged users (staff).
Subscriptions are the way to link users to events.
To do so, you should use these endpoints:
- POST /eventos/{evento_id}/subscription
- DELETE /eventos/{evento_id}/subscription
"""

@router.post("/", response_model=Inscricao)
def create_inscricao(inscricao: InscricaoCreate, current_user: Annotated[Users, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    # TODO: Validate if the user is a staff member
    db_inscricao = Inscricoes(
        participante_id=inscricao.participante_id,
        evento_id=inscricao.evento_id
    )
    db.add(db_inscricao)
    try:
        db.commit()
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=400, detail="Inscrição already exists")
    db.refresh(db_inscricao)
    return Inscricao.model_validate(db_inscricao)

@router.get("/", response_model=List[Inscricao])
def read_inscricoes(current_user: Annotated[Users, Depends(get_current_active_user)], event_id: int = None, participant_id: int = None, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    # TODO: Validate if the user is a staff member
    db_inscricoes = db.query(Inscricoes)
    if event_id:
        db_inscricoes = db_inscricoes.filter(Inscricoes.evento_id == event_id)
    if participant_id:
        db_inscricoes = db_inscricoes.filter(Inscricoes.participante_id == participant_id)
    db_inscricoes.offset(skip).limit(limit).all()
    return db_inscricoes

@router.get("/{inscricao_id}", response_model=Inscricao)
def read_inscricao(inscricao_id: int, current_user: Annotated[Users, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    # TODO: Validate if the user is a staff member
    db_inscricao = db.query(Inscricoes).filter(Inscricoes.id == inscricao_id).first()
    if db_inscricao is None:
        raise HTTPException(status_code=404, detail="Inscricao not found")
    return Inscricao.model_validate(db_inscricao)

@router.delete("/{inscricao_id}")
def delete_inscricao(inscricao_id: int, current_user: Annotated[Users, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    # TODO: Validate if the user is a staff member
    db_inscricao = db.query(Inscricoes).filter(Inscricoes.id == inscricao_id).first()
    if db_inscricao is None:
        raise HTTPException(status_code=404, detail="Inscricao not found")
    db.delete(db_inscricao)    
    return {"message": "Inscricao deleted successfully"}




