from sqlalchemy import inspect
from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.auth import get_current_active_user
from app.dependencies.database import get_db
from ..models.users import Users
from ..models.desafios import Desafios
from ..models.atividade import Atividade
from ..schemas.desafios import DesafioCreate, DesafioUpdate, Desafio
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/desafios", tags=["desafios"], responses={404: {"description": "Not found"}}
)


@router.post("/", response_model=Desafio)
def create_desafio(
    desafio: DesafioCreate,
    current_user: Annotated[Users, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    # TODO: check if user is allowed to create desafio (staff)
    try:
        with db.begin():
            # create 'Atividade' object
            db_atividade = Atividade(nome=desafio.nome, pontos=desafio.pontos)
            db.add(db_atividade)
            db.flush()  # flush to get the id

            # create 'Desafios' object
            db_desafio = Desafios(
                descricao=desafio.descricao,
                # empresa_id=desafio.empresa_id,
                atividade_id=db_atividade.id,
            )
            db.add(db_desafio)

        db.refresh(db_atividade)
        db.refresh(db_desafio)

        # return joined object
        return Desafio(
                id=db_desafio.id,
                nome=db_atividade.nome,
                pontos=db_atividade.pontos,
                descricao=db_desafio.descricao,
            )
    except Exception as e:
        db.rollback()
        return HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[Desafio])
def read_desafios(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    # Join 'Atividade' and 'Desafios' tables
    db_desafios = (
        db.query(
            Desafios.id,
            Atividade.nome,
            Atividade.pontos,
            Desafios.descricao,
            )
        .join(Atividade, Desafios.atividade_id == Atividade.id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return db_desafios


@router.get("/{desafio_id}", response_model=Desafio)
def read_desafio(desafio_id: int, db: Session = Depends(get_db)):
    # Join 'Atividade' and 'Desafios' tables
    db_desafio = (
        db.query(
            Desafios.id,
            Atividade.nome,
            Atividade.pontos,
            Desafios.descricao,
            )
        .join(Atividade, Desafios.atividade_id == Atividade.id)
        .filter(Desafios.id == desafio_id)
        .first()
    )
    if db_desafio is None:
        raise HTTPException(status_code=404, detail="Desafio not found")
    return db_desafio


@router.put("/{desafio_id}", response_model=Desafio)
def update_desafio(
    desafio_id: int,
    desafio: DesafioUpdate,
    current_user: Annotated[Users, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    # TODO: check if user is allowed to update desafio (staff)

    # Join 'Atividade' and 'Desafios' tables
    db_desafio = (
        db.query(
            Desafios.id,
            Atividade.nome,
            Atividade.pontos,
            Desafios.descricao,
            )
        .join(Atividade, Desafios.atividade_id == Atividade.id)
        .filter(Desafios.id == desafio_id)
        .first()
    )
    if db_desafio is None:
        raise HTTPException(status_code=404, detail="Desafio not found")

    # update 'Atividade' object
    db.query(Atividade).filter(Atividade.id == db_desafio.id).update(
        {"nome": desafio.nome, "pontos": desafio.pontos}
    )
    # update 'Desafios' object
    db.query(Desafios).filter(Desafios.id == db_desafio.id).update({
        "descricao": desafio.descricao,
    })
    db.commit()

    # return updated object
    return Desafio(
        id=db_desafio.id,
        nome=desafio.nome,
        pontos=desafio.pontos,
        descricao=desafio.descricao,
    )


@router.delete("/{desafio_id}", response_model=Desafio)
def delete_desafio(
    desafio_id: int,
    current_user: Annotated[Users, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    # TODO: check if user is allowed to delete desafio (staff)

    # Join 'Atividade' and 'Desafios' tables
    db_desafio = (
        db.query(
            Desafios.id,
            Atividade.nome,
            Atividade.pontos,
            Desafios.descricao,
            )
        .join(Atividade, Desafios.atividade_id == Atividade.id)
        .filter(Desafios.id == desafio_id)
        .first()
    )
    if db_desafio is None:
        raise HTTPException(status_code=404, detail="Desafio not found")

    # delete atividade (this will delete desafio too)
    db.query(Atividade).filter(Atividade.id == db_desafio.id).delete()
    db.commit()
    return db_desafio
