from sqlalchemy import Column, Integer, String, DateTime, Float, func, Boolean
from sqlalchemy.ext.declarative import declarative_base
from backend.database.database import Base  # Import Base from our database setup

# Base = declarative_base() # No need to define it here again

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    cash = Column(Float, default=0.0)
    registration_date = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<User id={self.id}, username='{self.username}', email='{self.email}'>"