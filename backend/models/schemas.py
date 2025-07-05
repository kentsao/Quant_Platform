from pydantic import BaseModel, constr, EmailStr, validator
from datetime import datetime
from typing import Optional, List, Dict
from enum import Enum

class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr
    password: constr(min_length=8)

    class Config:
        orm_mode = True

class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    cash: float
    created_at: datetime  # Changed 'registration_date' to 'created_at'

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username_or_email: str
    password: constr(min_length=8)

class SharingStatus(str, Enum):
    PRIVATE = "private"
    PUBLIC = "public"
    RENTABLE = "rentable"

class StrategyCreate(BaseModel):
    name: constr(min_length=3, max_length=100)
    description: Optional[str] = None
    parameters: Optional[Dict] = {}
    sharing_status: SharingStatus = SharingStatus.PRIVATE
    rental_fee: Optional[float] = 0.0
    profit_sharing_percentage: Optional[float] = 0.0
    category: Optional[str] = None
    asset_types: Optional[List[str]] = []

    class Config:
        orm_mode = True

class Strategy(BaseModel):
    id: int
    provider_id: int
    name: str
    description: Optional[str] = None
    creation_date: datetime
    parameters: Optional[Dict] = {}
    sharing_status: SharingStatus

    rental_fee: float
    profit_sharing_percentage: float
    last_backtest_date: Optional[datetime] = None
    total_return: Optional[float] = None
    annualized_return: Optional[float] = None
    volatility: Optional[float] = None
    sharpe_ratio: Optional[float] = None
    max_drawdown: Optional[float] = None
    category: Optional[str] = None
    asset_types: Optional[List[str]] = []

    class Config:
        orm_mode = True
        use_enum_values = True 