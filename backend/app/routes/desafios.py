from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.database import get_db
from ..models.desafios import Desafios
from ..schemas.desafios import DesafioCreate, DesafioUpdate, Desafio
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/desafios",
    tags=["desafios"],
    responses={404: {"description": "Not found"}}
)

@router.post("/", response_model=Desafio)
def create_desafio(desafio: DesafioCreate, db: Session = Depends(get_db)):
    db_desafio = Desafios(**desafio.dict())
    db.add(db_desafio)
    db.commit()
    db.refresh(db_desafio)
    return db_desafio

@router.get("/", response_model=List[Desafio])
def read_desafios(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Desafios).offset(skip).limit(limit).all()

@router.get("/{desafio_id}", response_model=Desafio)
def read_desafio(desafio_id: int, db: Session = Depends(get_db)):
    db_desafio = db.query(Desafios).filter(Desafios.id == desafio_id).first()
    if db_desafio is None:
        raise HTTPException(status_code=404, detail="Desafio not found")
    return db_desafio

@router.put("/{desafio_id}", response_model=Desafio)
def update_desafio(desafio_id: int, desafio: DesafioUpdate, db: Session = Depends(get_db)):
    db_desafio = db.query(Desafios).filter(Desafios.id == desafio_id).first()
    if db_desafio is None:
        raise HTTPException(status_code=404, detail="Desafio not found")
    for key, value in desafio.dict().items():
        setattr(db_desafio, key, value)
    db.commit()
    db.refresh(db_desafio)
    return db_desafio

@router.delete("/{desafio_id}", response_model=Desafio)
def delete_desafio(desafio_id: int, db: Session = Depends(get_db)):
    db_desafio = db.query(Desafios).filter(Desafios.id == desafio_id).first()
    if db_desafio is None:
        raise HTTPException(status_code=404, detail="Desafio not found")
    db.delete(db_desafio)
    db.commit()
    return db_desafio