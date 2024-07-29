from typing import Optional
from typing import List

from sqlalchemy import String, Integer, Boolean, Float, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base
from app.core.config import settings

class Users(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    auth_token: Mapped[str] = mapped_column(String(255), nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)


    participantes: Mapped["Participantes"] = relationship("Participantes", back_populates="user")
    staff: Mapped["Staff"] = relationship("Staff", back_populates="user")
    empresas: Mapped["Empresas"] = relationship("Empresas", back_populates="user")
