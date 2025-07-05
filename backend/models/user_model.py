from sqlalchemy import Boolean, Column, Integer, String, DateTime, Float  # Import Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from datetime import datetime

from backend.database.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    cash = Column(Float, default=0.0)  # Add the cash column

    strategies = relationship("Strategy", back_populates="provider")

    def __repr__(self):
        return f"<User id={self.id}, username='{self.username}', email='{self.email}'>"