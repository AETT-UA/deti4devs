from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.sql import func

from app.dependencies.auth import get_current_active_user
from app.dependencies.database import get_db
from ..models.users import Users
from ..models.atividade import Atividade
from ..models.eventos import Eventos
from ..schemas.eventos import Evento,EventoCreate,EventoUpdate
from ..models.inscricoes_eventos import Inscricoes
from ..models.participantes import Participantes
from ..schemas.inscricoes import Inscricao


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
        lotacao_max=evento.lotacao_max,
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
        lotacao_max=db_evento.lotacao_max,
        lotacao=0,
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
            Eventos.lotacao_max,
            Eventos.empresa_id,
            func.count(Inscricoes.id).label('lotacao')
            )
        .join(Atividade, Eventos.atividade_id == Atividade.id)
        .outerjoin(Inscricoes, Inscricoes.evento_id == Eventos.id)
        .group_by(Eventos.id, Atividade.nome, Atividade.pontos, Eventos.tipo, Eventos.lotacao_max, Eventos.empresa_id)
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
            Eventos.lotacao_max,
            Eventos.empresa_id,
            func.count(Inscricoes.id).label('lotacao')
            )
        .join(Atividade, Eventos.atividade_id == Atividade.id)
        .outerjoin(Inscricoes, Inscricoes.evento_id == Eventos.id)
        .group_by(Eventos.id, Atividade.nome, Atividade.pontos, Eventos.tipo, Eventos.lotacao_max, Eventos.empresa_id)
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
            Eventos.lotacao_max,
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
        "lotacao_max": evento.lotacao_max,
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
            Eventos.lotacao_max,
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

@router.post("/{evento_id}/subscription", response_model=Inscricao)
def subscribe_evento(evento_id:int,current_user: Annotated[Users, Depends(get_current_active_user)],db: Session = Depends(get_db)):
    # verify if lotacao is not exceeded
    db_evento = db.query(Eventos).filter(Eventos.id == evento_id).first()
    if db_evento is None:
        raise HTTPException(status_code=404,detail="Event not Found.")
    if db_evento.lotacao_max is not None:
        db_inscricoes = db.query(Inscricoes).filter(Inscricoes.evento_id == evento_id).count()
        if db_inscricoes >= db_evento.lotacao_max:
            raise HTTPException(status_code=400,detail="Event is full.")
    else:
        raise HTTPException(status_code=500,detail="Unexpected behavior, please contact the administrator.")
    
    # check if user is a participant
    db_participante = db.query(Participantes).filter(Participantes.user_id == current_user.id).first()
    if db_participante is None:
        raise HTTPException(status_code=404,detail="Should be a participant to subscribe to an event.")
        
    # duplicated user registered is prevented by the unique constraint in the database
    db_inscricao = Inscricoes(participante_id=db_participante.id, evento_id=evento_id)
    db.add(db_inscricao)
    db.commit()
    db.refresh(db_inscricao)

    return db_inscricao

@router.delete("/{evento_id}/subscription", response_model=Inscricao)
def unsubscribe_evento(evento_id:int,current_user: Annotated[Users, Depends(get_current_active_user)],db: Session = Depends(get_db)):
    db_participante = db.query(Participantes).filter(Participantes.user_id == current_user.id).first()
    if db_participante is None:
        raise HTTPException(status_code=404,detail="Participant not Found.")
    
    db_inscricao = db.query(Inscricoes).filter(Inscricoes.participante_id == db_participante.id, Inscricoes.evento_id == evento_id).first()
    if db_inscricao is None:
        raise HTTPException(status_code=404,detail="Registration not Found.")
    
    db.delete(db_inscricao)
    db.commit()
    return db_inscricao