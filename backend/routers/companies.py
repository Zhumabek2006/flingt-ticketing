from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend import crud, schemas, auth, models

router = APIRouter(prefix="/company", tags=["company"])

@router.get("/flights")
def get_company_flights(db: Session = Depends(get_db), current_user = Depends(auth.get_current_user)):
    if current_user.role != models.UserRole.manager:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if not current_user.company_id:
        raise HTTPException(status_code=400, detail="User is not associated with any company")
    return crud.get_company_flights(db, current_user.company_id)

@router.post("/flights")
def create_flight(flight: schemas.FlightCreate, db: Session = Depends(get_db), current_user = Depends(auth.get_current_user)):
    print(f"Получены данные рейса: {flight}")
    if current_user.role != models.UserRole.manager:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if not current_user.company_id:
        raise HTTPException(status_code=400, detail="User is not associated with any company")
    return crud.create_flight(db, flight, current_user.company_id)

@router.put("/flights/{flight_id}/status")
def update_flight_status(flight_id: int, flight_update: schemas.FlightUpdate, db: Session = Depends(get_db), current_user = Depends(auth.get_current_user)):
    if current_user.role != models.UserRole.manager:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if not current_user.company_id:
        raise HTTPException(status_code=400, detail="User is not associated with any company")
    return crud.update_flight_status(db, flight_id, current_user.company_id, flight_update.is_active)

@router.get("/stats")
def get_company_stats(db: Session = Depends(get_db), current_user = Depends(auth.get_current_user)):
    if current_user.role != models.UserRole.manager:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if not current_user.company_id:
        raise HTTPException(status_code=400, detail="User is not associated with any company")
    return crud.get_company_stats(db, current_user.company_id)

@router.delete("/flights/{flight_id}")
def delete_flight(flight_id: int, db: Session = Depends(get_db), current_user = Depends(auth.get_current_user)):
    if current_user.role != models.UserRole.manager:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if not current_user.company_id:
        raise HTTPException(status_code=400, detail="User is not associated with any company")
    result = crud.delete_flight(db, flight_id, current_user.company_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Flight not found")
    if result is False:
        raise HTTPException(status_code=400, detail="Cannot delete flight with existing tickets")
    return {"status": "ok"}

@router.get("/flights/{flight_id}/passengers")
def flight_passengers(flight_id: int, db: Session = Depends(get_db), current_user = Depends(auth.get_current_user)):
    if current_user.role != models.UserRole.manager:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if not current_user.company_id:
        raise HTTPException(status_code=400, detail="User is not associated with any company")
    result = crud.get_flight_passengers(db, flight_id, current_user.company_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Flight not found")
    return result
