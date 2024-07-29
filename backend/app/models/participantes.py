from typing import Optional
from typing import List

from sqlalchemy import String, Integer, Boolean, Float, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base
from app.core.config import settings

from .users import Users
from .participacao import Participacao

class Participantes(Base):
    __tablename__ = "participantes"
    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, 
                ForeignKey(f"{settings.SCHEMA_NAME}.users.id"), 
                    nullable=False, 
                    index=True, 
                    ondelete="CASCADE")
    nmec: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    pontos: Mapped[int] = mapped_column(Float, nullable=False, default=0)
    
    user: Mapped[Users] = relationship("Users", back_populates="participantes")
    participacoes: Mapped[List["Participacao"]] = relationship("Participacao", back_populates="participante")
    
