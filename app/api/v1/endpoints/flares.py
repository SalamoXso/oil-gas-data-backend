from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.flare import Flare
from app.utils.database import get_db

router = APIRouter()

@router.get("/flares/")
def get_flares(db: Session = Depends(get_db)):
    return db.query(Flare).all()

@router.post("/flares/")
def create_flare(flare_data: dict, db: Session = Depends(get_db)):
    flare = Flare(**flare_data)
    db.add(flare)
    db.commit()
    db.refresh(flare)
    return flare