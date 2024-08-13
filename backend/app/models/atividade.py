from typing import List

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dependencies.database import Base

class Atividade(Base):
    __tablename__ = "atividade"
    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    pontos: Mapped[int] = mapped_column(Integer, default=0)
    #empresa_id: Mapped[int] = mapped_column(
    #    ForeignKey(f"empresas.id", ondelete="CASCADE"),
    #    nullable=False
    #)

    #empresa: Mapped["Empresas"] = relationship("Empresas", back_populates="atividades")
    eventos: Mapped[List["Eventos"]] = relationship("Eventos", back_populates="atividade")
    desafios: Mapped[List["Desafios"]] = relationship("Desafios", back_populates="atividade")
    participacoes: Mapped[List["Participacao"]] = relationship("Participacao", back_populates="atividade")