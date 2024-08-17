from typing import Optional
from typing import List

from sqlalchemy import String, Integer, Boolean, Float, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dependencies.database import Base

class Staff(Base):
    __tablename__ = "staff"
    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey(f"users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )
    
    user: Mapped["Users"] = relationship("Users", back_populates="staff")