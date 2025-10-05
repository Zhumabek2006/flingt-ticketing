from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Flight

router = APIRouter(prefix="", tags=["public"])

@router.get("/flights")
def list_flights(
    db: Session = Depends(get_db),
    departure_city: str | None = Query(default=None),
    arrival_city: str | None = Query(default=None),
    date: str | None = Query(default=None)
):
    query = db.query(Flight).filter(Flight.is_active == True)
    if departure_city:
        query = query.filter(Flight.departure_city.ilike(f"%{departure_city}%"))
    if arrival_city:
        query = query.filter(Flight.arrival_city.ilike(f"%{arrival_city}%"))
    if date:
        query = query.filter(Flight.departure_date == date)
    return query.order_by(Flight.departure_date, Flight.departure_time).all()


