from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies.core import ACCESS_TOKEN_EXPIRE_MINUTES
from app.dependencies.database import get_db
from ..models.users import UserDB
from ..schemas.users import UserCreate, User, Token
from sqlalchemy.orm import Session

from ..dependencies.auth import authenticate_user, create_access_token,get_current_active_user, get_password_hash

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}}
)

@router.post("/register", response_model=User)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    db_user = UserDB(username=user.username, email=user.email, full_name=user.full_name, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return User.model_validate(db_user)

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@router.get("/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[UserDB, Depends(get_current_active_user)],
):
    return User.model_validate(current_user)

@router.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[UserDB, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]