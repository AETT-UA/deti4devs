from typing import Optional
from typing import List

from sqlalchemy import String, Integer, Boolean, Float, ForeignKey, Date, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base
from app.core.config import settings

from .users import Users
from .atividade import Atividade
from .eventos import Eventos
from .desafios import Desafios

class Empresas(Base):
    __tablename__ = "empresas"
    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey(f"{settings.SCHEMA_NAME}.users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )
    sponsor_type: Mapped[str] = mapped_column(String(50), nullable=True)
    spotlight_time: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, nullable=True)

    user: Mapped["Users"] = relationship("Users", back_populates="empresas")
    atividades: Mapped[List["Atividade"]] = relationship("Atividade", back_populates="empresa")
    eventos: Mapped[List["Eventos"]] = relationship("Eventos", back_populates="empresa")
    desafios: Mapped[List["Desafios"]] = relationship("Desafios", back_populates="empresa")