from sqlalchemy import String, Integer, Column, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dependencies.database import Base

class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    auth_token: Mapped[str] = mapped_column(String(255), nullable=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)


    participantes: Mapped["Participantes"] = relationship("Participantes", back_populates="user")
    staff: Mapped["Staff"] = relationship("Staff", back_populates="user")
    empresas: Mapped["Empresas"] = relationship("Empresas", back_populates="user")

