from requests import Session
from app.api import deps
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app import crud
from app.dtos import participantes_dto

router = APIRouter()

@router.get("/", response_model=List[participantes_dto.ParticipantesDTO])
def read_participantes(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    participantes = crud.participantes.get_multi(db, skip=skip, limit=limit)
    return participantes