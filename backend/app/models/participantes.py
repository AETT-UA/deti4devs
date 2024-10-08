from typing import Optional
from typing import List

from sqlalchemy import String, Integer, Boolean, Float, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dependencies.database import Base

class Participantes(Base):
    __tablename__ = "participantes"
    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column( 
                ForeignKey(f"users.id", ondelete="CASCADE"),
                    nullable=False, 
                    index=True, 
                    )
    nmec: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    pontos: Mapped[int] = mapped_column(Float, nullable=False, default=0)
    
    user: Mapped["Users"] = relationship("Users", back_populates="participantes")
    participacoes: Mapped[List["Participacao"]] = relationship("Participacao", back_populates="participantes")
    
