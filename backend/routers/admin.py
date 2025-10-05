from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend import crud, schemas, auth, models

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users")
def get_all_users(db: Session = Depends(get_db), current_user = Depends(auth.get_current_user)):
    if current_user.role != models.UserRole.admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return crud.get_all_users(db)

@router.get("/companies")
def get_all_companies(db: Session = Depends(get_db), current_user = Depends(auth.get_current_user)):
    if current_user.role != models.UserRole.admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return crud.get_all_companies(db)

@router.post("/managers")
def create_manager(manager: schemas.ManagerCreate, db: Session = Depends(get_db), current_user = Depends(auth.get_current_user)):
    if current_user.role != models.UserRole.admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return crud.create_manager(db, manager)

@router.put("/users/{user_id}/status")
def update_user_status(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db), current_user = Depends(auth.get_current_user)):
    if current_user.role != models.UserRole.admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return crud.update_user_status(db, user_id, user_update.is_active)

@router.get("/stats")
def get_admin_stats(db: Session = Depends(get_db), current_user = Depends(auth.get_current_user)):
    if current_user.role != models.UserRole.admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return {
        "total_users": crud.get_users_count(db),
        "active_users": crud.get_active_users_count(db),
        "total_companies": crud.get_companies_count(db)
    }
