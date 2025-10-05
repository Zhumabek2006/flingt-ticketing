from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from backend.database import engine, Base
from backend.routers import auth as auth_router, admin as admin_router, companies
from backend.routers import public as public_router, tickets as tickets_router
from backend import models, schemas, crud, auth
import logging

app = FastAPI()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Middleware для логирования ошибок валидации
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error on {request.url}: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем все источники для разработки
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.crud import get_user_by_email
from backend.schemas import UserCreate
from backend.auth import get_password_hash
from sqlalchemy import text

db = SessionLocal()
# Лёгкая миграция для добавления колонок first_name/last_name в SQLite, если их нет
try:
    db.execute(text("ALTER TABLE users ADD COLUMN first_name VARCHAR"))
except Exception:
    pass
try:
    db.execute(text("ALTER TABLE users ADD COLUMN last_name VARCHAR"))
except Exception:
    pass
db.commit()
admin = get_user_by_email(db, "admin@gmail.com")
if not admin:
    admin_create = UserCreate(email="admin@gmail.com", password="admin123!", role="admin")
    crud.create_user(db, admin_create)
db.close()

app.include_router(auth_router.router)
app.include_router(admin_router.router)
app.include_router(companies.router)
app.include_router(public_router.router)
app.include_router(tickets_router.router)

@app.get("/users/me", response_model=schemas.UserOut)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user