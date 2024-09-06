from sqlalchemy import ForeignKey, Integer, TIMESTAMP, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy.sql

from app.dependencies.database import Base

class Inscricoes(Base):
    __tablename__ = "inscricoes_eventos"
    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    participante_id: Mapped[int] = mapped_column(
        ForeignKey(f"participantes.id", ondelete="CASCADE"),
        nullable=False
    )
    evento_id: Mapped[int] = mapped_column(
        ForeignKey(f"eventos.id", ondelete="CASCADE"),
        nullable=False
    )
    timestamp: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, nullable=False, server_default=sqlalchemy.sql.func.current_timestamp())

    participantes: Mapped["Participantes"] = relationship("Participantes", back_populates="inscricoes")
    eventos: Mapped["Eventos"] = relationship("Eventos", back_populates="inscricoes")

    # Unique constraint to prevent duplicate registrations
    __table_args__ = (
        UniqueConstraint('participante_id', 'evento_id', name='unique_participante_evento'),
    )