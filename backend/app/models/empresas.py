from typing import List

from sqlalchemy import String, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dependencies.database import Base

class Empresas(Base):
    __tablename__ = "empresas"
    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey(f"users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )
    sponsor_type: Mapped[str] = mapped_column(String(50), nullable=True)
    spotlight_time: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, nullable=True)

    user: Mapped["Users"] = relationship("Users", back_populates="empresas")
    atividades: Mapped[List["Atividade"]] = relationship("Atividade", back_populates="empresa")
    eventos: Mapped[List["Eventos"]] = relationship("Eventos", back_populates="empresa")
    desafios: Mapped[List["Desafios"]] = relationship("Desafios", back_populates="empresa")