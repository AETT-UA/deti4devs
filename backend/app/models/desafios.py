from sqlalchemy import Integer, Boolean, Float, ForeignKey, Date, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dependencies.database import Base

class Desafios(Base):
    __tablename__ = "desafios"
    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    atividade_id: Mapped[int] = mapped_column(
        ForeignKey(f"atividade.id", ondelete="CASCADE"),
        nullable=False
    )
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    #empresa_id: Mapped[int] = mapped_column(
    #    ForeignKey(f"empresas.id", ondelete="CASCADE"),
    #    nullable=False
    #)

    atividade: Mapped["Atividade"] = relationship("Atividade", back_populates="desafios")
    #empresa: Mapped["Empresas"] = relationship("Empresas", back_populates="desafios")