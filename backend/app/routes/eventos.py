from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.auth import get_current_active_user
from app.dependencies.database import get_db
from ..models.users import Users
from ..models.atividade import Atividade
from ..models.eventos import Eventos
from ..schemas.eventos import Evento,EventoCreate,EventoUpdate

from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/eventos",
    tags=["eventos"],
    responses={404: {"description": "Not found"}}
)


# Event CRUD

@router.post("/",response_model=Evento)
def create_post(evento: EventoCreate,current_user: Annotated[Users, Depends(get_current_active_user)],db: Session = Depends(get_db)):
    db_atividade= Atividade(nome=evento.tipo, pontos=evento.pontos)
    db.add(db_atividade)
    db.flush()
    db_evento = Eventos(
        tipo=evento.tipo,
        empresa_id=evento.empresa_id,
        atividade_id=db_atividade.id
    )
    db.add(db_evento)
    db.commit()
    db.refresh(db_atividade)
    db.refresh(db_evento)

    return Evento(
        id=db_evento.id,
        nome=db_atividade.nome,
        pontos=db_atividade.pontos,
        tipo=db_evento.tipo,
        empresa_id=db_evento.empresa_id
    )
@router.get("/",response_model=List[Evento])
def read_eventos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_eventos = (
        db.query(
            Eventos.id,
            Atividade.nome,
            Atividade.pontos,
            Eventos.tipo,
            Eventos.empresa_id
            )
        .join(Atividade, Eventos.atividade_id == Atividade.id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return db_eventos
@router.get("/{evento_id}",response_model=Evento)
def read_eventos(evento_id:int, db: Session = Depends(get_db)):
    db_eventos = (
        db.query(
            Eventos.id,
            Atividade.nome,
            Atividade.pontos,
            Eventos.tipo,
            Eventos.empresa_id
            )
        .join(Atividade, Eventos.atividade_id == Atividade.id)
        .filter(Eventos.id==evento_id)
        .first()
    )

    return db_eventos

@router.put("/{evento_id}",response_model=Evento)
def update_eventos(evento_id:int,evento:EventoUpdate,current_user: Annotated[Users, Depends(get_current_active_user)],db: Session = Depends(get_db)):

    db_evento = (
        db.query(
            Eventos.id,
            Atividade.nome,
            Atividade.pontos,
            Eventos.tipo,
            Eventos.empresa_id,
            Atividade.id.label("atividade_id")
        )
        .join(Atividade, Eventos.atividade_id == Atividade.id)
        .filter(Eventos.id == evento_id)
        .first()
    )

    if db_evento is None:
        raise HTTPException(status_code=404,detail="Evento not Found.")

    db.query(Atividade).filter(Atividade.id == db_evento.atividade_id).update({
        "nome": evento.nome,
        "pontos": evento.pontos
    })
    # update 'Eventos' object
    db.query(Eventos).filter(Eventos.id == evento_id).update({
        "tipo": evento.tipo,
        "empresa_id": evento.empresa_id
    })

    db.commit()


    return Evento(
        id=evento_id,
        **vars(evento)
    )

@router.delete("/{evento_id}",response_model=Evento)
def delete_eventos(evento_id:int,current_user: Annotated[Users, Depends(get_current_active_user)],db: Session = Depends(get_db)):
    db_evento = (
        db.query(
            Eventos.id,
            Atividade.nome,
            Atividade.pontos,
            Eventos.tipo,
            Eventos.empresa_id,
            Atividade.id.label("atividade_id")
        )
        .join(Atividade, Eventos.atividade_id == Atividade.id)
        .filter(Eventos.id == evento_id)
        .first()
    )

    if db_evento is None:
        raise HTTPException(status_code=404,detail="Evento not Found.")
    db.query(Atividade).filter(Atividade.id == db_evento.atividade_id).delete()
    db.commit()
    return db_evento


# Event registration

from ..models.inscricoes_eventos import Inscricoes
from ..models.participantes import Participantes
from ..schemas.inscricoes import InscricaoResponse

@router.post("/{evento_id}/inscricao")
def inscricao_evento(evento_id:int,current_user: Annotated[Users, Depends(get_current_active_user)],db: Session = Depends(get_db)):
    # check if user is a participant
    db_participante = db.query(Participantes).filter(Participantes.user_id == current_user.id).first()
    if db_participante is None:
        raise HTTPException(status_code=404,detail="Participant not Found.")
    
    # check if event exists
    db_evento = db.query(Eventos).filter(Eventos.id == evento_id).first()
    if db_evento is None:
        raise HTTPException(status_code=404,detail="Event not Found.")
    
    # duplicated user registered is prevented by the unique constraint in the database
    db_inscricao = Inscricoes(participante_id=db_participante.id, evento_id=evento_id)
    db.add(db_inscricao)
    db.commit()
    db.refresh(db_inscricao)

    return db_inscricao
