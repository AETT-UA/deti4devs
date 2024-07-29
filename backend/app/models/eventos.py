from typing import Optional
from typing import List

from sqlalchemy import String, Integer, Boolean, Float, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base
from app.core.config import settings

from .atividade import Atividade
from .empresas import Empresas

class Eventos(Base):
    __tablename__ = "eventos"
    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    atividade_id: Mapped[int] = mapped_column(
        ForeignKey(f"{settings.SCHEMA_NAME}.atividade.id", ondelete="CASCADE"),
        nullable=False
    )
    empresa_id: Mapped[int] = mapped_column(
        ForeignKey(f"{settings.SCHEMA_NAME}.empresas.id", ondelete="CASCADE"),
        nullable=False
    )
    tipo: Mapped[str] = mapped_column(String(50), nullable=True)

    atividade: Mapped["Atividade"] = relationship("Atividade", back_populates="eventos")
    empresa: Mapped["Empresas"] = relationship("Empresas", back_populates="eventos")