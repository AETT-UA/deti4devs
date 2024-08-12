from sqlalchemy import ForeignKey, Integer, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy.sql

from app.dependencies.database import Base

class Participacao(Base):
    __tablename__ = "participacao"
    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    participante_id: Mapped[int] = mapped_column(
        ForeignKey(f"participantes.id", ondelete="CASCADE"),
        nullable=False
    )
    atividade_id: Mapped[int] = mapped_column(
        ForeignKey(f"atividade.id", ondelete="CASCADE"),
        nullable=False
    )
    timestamp: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, nullable=False, server_default=sqlalchemy.sql.func.current_timestamp())

    participantes: Mapped["Participantes"] = relationship("Participantes", back_populates="participacoes")
    atividade: Mapped["Atividade"] = relationship("Atividade", back_populates="participacoes")