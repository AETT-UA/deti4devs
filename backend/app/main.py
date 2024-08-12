from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.dependencies.database import Base, engine
from app.routes import auth
from app import models

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(auth.router)

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)