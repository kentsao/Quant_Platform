from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.database import get_db
from backend.models import schemas, user_model
from backend.models.strategy_model import Strategy as DBStrategy  # Alias for clarity
from backend.services import strategy_service
from backend.dependencies import get_current_user  # We'll define this later

router = APIRouter(prefix="/strategies", tags=["Strategies"])

@router.post("/", response_model=schemas.Strategy, status_code=201)
async def create_strategy(strategy: schemas.StrategyCreate, db: Session = Depends(get_db), current_user: user_model.User = Depends(get_current_user)):
    return strategy_service.create_strategy(db=db, strategy=strategy, provider_id=current_user.id)

@router.get("/{strategy_id}", response_model=schemas.Strategy)
async def read_strategy(strategy_id: int, db: Session = Depends(get_db), current_user: user_model.User = Depends(get_current_user)):
    db_strategy = strategy_service.get_strategy(db, strategy_id=strategy_id)
    if db_strategy is None:
        raise HTTPException(status_code=404, detail="Strategy not found")
    if db_strategy.provider_id != current_user.id and db_strategy.sharing_status == "private":
        raise HTTPException(status_code=403, detail="Not authorized to view this strategy")
    return db_strategy

@router.put("/{strategy_id}", response_model=schemas.Strategy)
async def update_strategy(strategy_id: int, strategy: schemas.StrategyCreate, db: Session = Depends(get_db), current_user: user_model.User = Depends(get_current_user)):
    db_strategy = strategy_service.get_strategy(db, strategy_id=strategy_id)
    if db_strategy is None:
        raise HTTPException(status_code=404, detail="Strategy not found")
    if db_strategy.provider_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this strategy")
    return strategy_service.update_strategy(db=db, strategy_id=strategy_id, strategy=strategy)

@router.delete("/{strategy_id}", status_code=204)
async def delete_strategy(strategy_id: int, db: Session = Depends(get_db), current_user: user_model.User = Depends(get_current_user)):
    db_strategy = strategy_service.get_strategy(db, strategy_id=strategy_id)
    if db_strategy is None:
        raise HTTPException(status_code=404, detail="Strategy not found")
    if db_strategy.provider_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this strategy")
    strategy_service.delete_strategy(db=db, strategy_id=strategy_id)
    return {"detail": "Strategy deleted successfully"}