from sqlalchemy.orm import Session
from backend.models import schemas
from backend.models.strategy_model import Strategy, SharingStatus

def create_strategy(db: Session, strategy: schemas.StrategyCreate, provider_id: int):
    sharing_status_enum = SharingStatus[strategy.sharing_status.name.upper()] # Convert to uppercase enum member
    db_strategy = Strategy(provider_id=provider_id, name=strategy.name,
                           description=strategy.description, parameters=strategy.parameters,
                           sharing_status=sharing_status_enum, rental_fee=strategy.rental_fee,
                           profit_sharing_percentage=strategy.profit_sharing_percentage,
                           category=strategy.category, asset_types=strategy.asset_types)
    db.add(db_strategy)
    db.commit()
    db.refresh(db_strategy)
    return db_strategy