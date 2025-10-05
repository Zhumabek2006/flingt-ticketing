from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend import auth, crud, schemas

router = APIRouter(prefix="/tickets", tags=["tickets"])

@router.post("", response_model=schemas.TicketOut)
def buy_ticket(payload: schemas.TicketCreate, db: Session = Depends(get_db), current_user = Depends(auth.get_current_user)):
    ticket = crud.create_ticket(db, user_id=current_user.id, flight_id=payload.flight_id)
    if ticket is None:
        raise HTTPException(status_code=400, detail="Flight is unavailable")
    return ticket

@router.get("/my")
def my_tickets(db: Session = Depends(get_db), current_user = Depends(auth.get_current_user)):
    tickets = crud.get_user_tickets(db, current_user.id)
    # Формируем удобный вывод с данными рейса
    result = []
    for t in tickets:
        f = t.flight
        result.append({
            "id": t.id,
            "flight_id": f.id,
            "flight_number": f.flight_number,
            "route": f"{f.departure_city} → {f.arrival_city}",
            "date": str(f.departure_date),
            "time": str(f.departure_time),
            "price": t.price,
            "status": t.status.value,
            "created_at": t.created_at.isoformat(),
        })
    return result

@router.put("/{ticket_id}/cancel")
def cancel(ticket_id: int, db: Session = Depends(get_db), current_user = Depends(auth.get_current_user)):
    result = crud.cancel_ticket(db, current_user.id, ticket_id)
    if result is None:
        raise HTTPException(status_code=400, detail="Cannot cancel this ticket")
    if result is False:
        raise HTTPException(status_code=400, detail="Refund window closed (less than 24h before departure)")
    return {"status": "ok"}


