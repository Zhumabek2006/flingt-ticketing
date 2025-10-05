from pydantic import BaseModel
from .models import UserRole
from typing import Optional
from datetime import datetime, date, time

class UserCreate(BaseModel):
    email: str
    password: str
    role: str = "regular"  # Принимаем строку, конвертируем в enum в CRUD

class UserOut(BaseModel):
    id: int
    email: str
    role: UserRole
    is_active: bool
    created_at: datetime
    company_id: Optional[int] = None

class CompanyCreate(BaseModel):
    name: str

class CompanyOut(BaseModel):
    id: int
    name: str
    is_active: bool
    created_at: datetime

class ManagerCreate(BaseModel):
    company_name: str
    email: str
    password: str

class UserUpdate(BaseModel):
    is_active: bool

class FlightCreate(BaseModel):
    flight_number: str
    departure_city: str
    arrival_city: str
    departure_date: str  # Принимаем строку
    departure_time: str  # Принимаем строку
    arrival_date: str   # Принимаем строку
    arrival_time: str   # Принимаем строку
    total_seats: int
    price: float

class FlightOut(BaseModel):
    id: int
    flight_number: str
    departure_city: str
    arrival_city: str
    departure_date: date
    departure_time: time
    arrival_date: date
    arrival_time: time
    total_seats: int
    available_seats: int
    price: float
    is_active: bool
    created_at: datetime
    company_id: int

class FlightUpdate(BaseModel):
    is_active: bool

class CompanyStats(BaseModel):
    total_flights: int
    active_flights: int
    total_seats: int
    available_seats: int
    total_revenue: float