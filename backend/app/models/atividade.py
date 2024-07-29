from typing import Optional
from typing import List

from sqlalchemy import String, Integer, Boolean, Float, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base
from app.core.config import settings

from .empresas import Empresas
from .eventos import Eventos
from .desafios import Desafios
from .participacao import Participacao

class Atividade(Base):
    __tablename__ = "atividade"
    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    pontos: Mapped[int] = mapped_column(Integer, default=0)
    empresa_id: Mapped[int] = mapped_column(
        ForeignKey(f"{settings.SCHEMA_NAME}.empresas.id", ondelete="CASCADE"),
        nullable=False
    )

    empresa: Mapped["Empresas"] = relationship("Empresas", back_populates="atividades")
    eventos: Mapped[List["Eventos"]] = relationship("Eventos", back_populates="atividade")
    desafios: Mapped[List["Desafios"]] = relationship("Desafios", back_populates="atividade")
    participacoes: Mapped[List["Participacao"]] = relationship("Participacao", back_populates="atividade")