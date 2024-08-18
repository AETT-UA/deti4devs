from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.auth import get_current_active_user
from app.dependencies.database import get_db
from ..models.users import Users
from ..models.empresas import Empresas
from ..models.atividade import Atividade
from ..schemas.users import User, UserCreate
from ..schemas.empresas import *
from sqlalchemy.orm import Session
from datetime import datetime

from app.routes.auth import register_user, get_password_hash

router = APIRouter(
    prefix="/empresas",
    tags=["empresas"],
    responses={404: {"description": "Not found"}}
)

@router.post("/", response_model=Empresa)
def create_empresa(
    empresa: EmpresaCreate,
    db: Session = Depends(get_db)
):
    # TODO: check if user is allowed to create empresa (staff)
    if empresa.user_id is None:
        # create 'Users' object
        db_user = db.query(Users).filter(Users.username == empresa.user.username).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        hashed_password = get_password_hash(empresa.user.password)
        db_user = Users(username=empresa.user.username, email=empresa.user.email, full_name=empresa.user.full_name, hashed_password=hashed_password)
        db.add(db_user)
    else:
        # retrieve 'Users' object
        db_user = db.query(Users).filter(Users.id == empresa.user_id).first()
        if db_user is None:
            raise HTTPException(status_code=400, detail="User not found")

    # create 'Atividade' object
    db_atividade = Atividade(
        nome=empresa.nome,
        pontos=empresa.pontos
    )
    db.add(db_atividade)

    db.flush()

    # create 'Empresas' object
    db_empresa = Empresas(
        sponsor_type=empresa.sponsor_type,
        spotlight_time=empresa.spotlight_time,
        atividade_id=db_atividade.id,
        user_id=db_user.id
    )
    db.add(db_empresa)

    db.commit()

    db.refresh(db_atividade)
    db.refresh(db_empresa)

    # return joined object
    return Empresa(
            id=db_empresa.id,
            nome=db_atividade.nome,
            pontos=db_atividade.pontos,
            sponsor_type=db_empresa.sponsor_type,
            spotlight_time=db_empresa.spotlight_time,
            user_id=db_user.id
        )

@router.get("/", response_model=List[Empresa])
def read_empresas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    # Join 'Atividade' and 'Desafios' tables
    db_empresas = (
        db.query(
            Empresas.id,
            Atividade.nome,
            Atividade.pontos,
            Empresas.sponsor_type,
            Empresas.spotlight_time,
            Empresas.user_id
            )
        .join(Atividade, Empresas.atividade_id == Atividade.id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    if len(db_empresas) == 0:
        return list()

    return db_empresas

@router.get("/{empresa_id}", response_model=Empresa)
def read_empresa(empresa_id: int, db: Session = Depends(get_db)):
    # Join 'Atividade' and 'Desafios' tables
    db_empresas = (
        db.query(
            Empresas.id,
            Atividade.nome,
            Atividade.pontos,
            Empresas.sponsor_type,
            Empresas.spotlight_time,
            Empresas.user_id
            )
        .join(Atividade, Empresas.atividade_id == Atividade.id)
        .filter(Empresas.id == empresa_id)
        .first()
    )
    if db_empresas is None:
        raise HTTPException(status_code=404, detail="Desafio not found")
    return db_empresas

@router.put("/{empresa_id}", response_model=Empresa)
def update_empresa(
    empresa_id: int,
    empresa: EmpresaUpdate,
    db: Session = Depends(get_db)
):
    # TODO: check if user is allowed to update empresa (staff)
    # Join 'Atividade' and 'Empresas' tables
    db_empresas = (
        db.query(Empresas)
        .filter(Empresas.id == empresa_id)
        .first()
    )
    if db_empresas is None:
        raise HTTPException(status_code=404, detail="Empresa not found")
    
    try:
        # update 'Atividade' object
        db.query(Atividade).filter(Atividade.id == db_empresas.atividade_id).update({
            "nome": empresa.nome,
            "pontos": empresa.pontos
        })

        # update 'Empresas' object
        db.query(Empresas).filter(Empresas.id == empresa_id).update({
            "sponsor_type": empresa.sponsor_type,
            "spotlight_time": empresa.spotlight_time
        })

        db.commit()

        db.refresh(db_empresas)

        # Recarregar a instância da atividade para refletir as mudanças
        db_atividade = db.query(Atividade).filter(Atividade.id == db_empresas.atividade_id).first()

        # return joined object
        return Empresa(
            id=db_empresas.id,
            nome=db_atividade.nome,
            pontos=db_atividade.pontos,
            sponsor_type=db_empresas.sponsor_type,
            spotlight_time=db_empresas.spotlight_time,
            user_id=db_empresas.user_id
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/{empresa_id}", response_model=Empresa)
def delete_empresa(empresa_id: int, db: Session = Depends(get_db)):
    # TODO: check if user is allowed to delete empresa (staff)
    # Join 'Atividade' and 'Empresas' tables
    db_empresas = (
        db.query(Empresas)
        .filter(Empresas.id == empresa_id)
        .first()
    )
    if db_empresas is None:
        raise HTTPException(status_code=404, detail="Empresa not found")
    
    db_atividades = (
        db.query(Atividade)
        .filter(Atividade.id == db_empresas.atividade_id)
        .first()
    )

    response = Empresa(
        id=db_empresas.id,
        nome=db_atividades.nome,
        pontos=db_atividades.pontos,
        sponsor_type=db_empresas.sponsor_type,
        spotlight_time=db_empresas.spotlight_time,
        user_id=db_empresas.user_id
    )

    # disable user
    db.query(Users).filter(Users.id == db_empresas.user_id).update(
        {"disabled": True}
    )
    
    # delete atividade (this will delete empresa too)
    db.query(Atividade).filter(Atividade.id == db_atividades.id).delete()
    db.commit()
    return response
