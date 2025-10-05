from sqlalchemy import Column, Integer, String, Enum, Boolean, DateTime, ForeignKey, Float, Date, Time
from sqlalchemy.orm import relationship
from .database import Base
import enum
from datetime import datetime

class UserRole(enum.Enum):
    regular = "regular"
    manager = "manager"
    admin = "admin"

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Связь с менеджерами
    managers = relationship("User", back_populates="company")
    # Связь с рейсами
    flights = relationship("Flight", back_populates="company")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRole))
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Связь с компанией
    company = relationship("Company", back_populates="managers")

class Flight(Base):
    __tablename__ = "flights"
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    flight_number = Column(String, nullable=False)
    departure_city = Column(String, nullable=False)
    arrival_city = Column(String, nullable=False)
    departure_date = Column(Date, nullable=False)
    departure_time = Column(Time, nullable=False)
    arrival_date = Column(Date, nullable=False)
    arrival_time = Column(Time, nullable=False)
    total_seats = Column(Integer, nullable=False)
    available_seats = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Связь с компанией
    company = relationship("Company", back_populates="flights")