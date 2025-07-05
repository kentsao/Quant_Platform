from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import JSON  # For storing parameters as JSON
from sqlalchemy.types import Enum as SqlEnum  # Use this explicitly
from backend.database.database import Base
import enum

# Define the Python Enum for sharing status
class SharingStatus(str, enum.Enum):
    PRIVATE = "private"
    PUBLIC = "public"
    RENTABLE = "rentable"

# Define the SQLAlchemy model
class Strategy(Base):
    __tablename__ = "strategies"

    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, nullable=False)
    description = Column(Text)
    creation_date = Column(DateTime, default=func.now())
    parameters = Column(JSON)  # Store strategy logic as JSON
    sharing_status = Column(SqlEnum(SharingStatus, native_enum=False), default=SharingStatus.PRIVATE)
    rental_fee = Column(Float, default=0.0)
    profit_sharing_percentage = Column(Float, default=0.0)
    last_backtest_date = Column(DateTime)
    total_return = Column(Float)
    annualized_return = Column(Float)
    volatility = Column(Float)
    sharpe_ratio = Column(Float)
    max_drawdown = Column(Float)
    category = Column(String)
    asset_types = Column(JSON)  # E.g., ["stocks", "bonds"]

    provider = relationship("User", back_populates="strategies")

    def __repr__(self):
        return f"<Strategy id={self.id}, name='{self.name}', provider_id={self.provider_id}>"
