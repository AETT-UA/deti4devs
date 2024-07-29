from typing import Optional
from typing import List

from sqlalchemy import String, Integer, Boolean, Float, ForeignKey, Date, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base
from app.core.config import settings

from .atividade import Atividade
from .empresas import Empresas

class Desafios(Base):
    __tablename__ = "desafios"
    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    atividade_id: Mapped[int] = mapped_column(
        ForeignKey(f"{settings.SCHEMA_NAME}.atividade.id", ondelete="CASCADE"),
        nullable=False
    )
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    empresa_id: Mapped[int] = mapped_column(
        ForeignKey(f"{settings.SCHEMA_NAME}.empresas.id", ondelete="CASCADE"),
        nullable=False
    )

    atividade: Mapped["Atividade"] = relationship("Atividade", back_populates="desafios")
    empresa: Mapped["Empresas"] = relationship("Empresas", back_populates="desafios")