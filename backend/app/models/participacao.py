from sqlalchemy import ForeignKey, Integer, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.config import settings
from app.db.base_class import Base

class Participacao(Base):
    __tablename__ = "participacao"
    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    participante_id: Mapped[int] = mapped_column(
        ForeignKey(f"{settings.SCHEMA_NAME}.participantes.id", ondelete="CASCADE"),
        nullable=False
    )
    atividade_id: Mapped[int] = mapped_column(
        ForeignKey(f"{settings.SCHEMA_NAME}.atividade.id", ondelete="CASCADE"),
        nullable=False
    )
    timestamp: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, nullable=False, server_default="CURRENT_TIMESTAMP")

    participante: Mapped["Participantes"] = relationship("Participantes", back_populates="participacoes")
    atividade: Mapped["Atividade"] = relationship("Atividade", back_populates="participacoes")