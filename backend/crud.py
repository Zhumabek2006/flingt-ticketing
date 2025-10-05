from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .models import User, Company, Flight, UserRole, Ticket, TicketStatus
from .auth import get_password_hash
from . import schemas
from sqlalchemy import func

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def check_user_active(db: Session, user_id: int):
    """
    Проверяет статус пользователя.
    Если пользователь заблокирован (is_active=False), выбрасывает исключение.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Пользователь заблокирован"
        )
    return user

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    
    # Конвертируем строку в enum
    if user.role == "admin":
        role = UserRole.admin
    elif user.role == "manager":
        role = UserRole.manager
    else:
        role = UserRole.regular
    
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        role=role,
        first_name=user.first_name,
        last_name=user.last_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def get_all_companies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Company).offset(skip).limit(limit).all()

def create_company(db: Session, company: schemas.CompanyCreate):
    db_company = Company(name=company.name)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

def get_company_by_name(db: Session, name: str):
    return db.query(Company).filter(Company.name == name).first()

def create_manager(db: Session, manager: schemas.ManagerCreate):
    # Найти или создать компанию
    company = get_company_by_name(db, manager.company_name)
    if not company:
        company = create_company(db, schemas.CompanyCreate(name=manager.company_name))
    
    # Создать менеджера
    hashed_password = get_password_hash(manager.password)
    from .models import UserRole
    db_manager = User(
        email=manager.email, 
        hashed_password=hashed_password, 
        role=UserRole.manager,
        company_id=company.id
    )
    db.add(db_manager)
    db.commit()
    db.refresh(db_manager)
    return db_manager

def update_user_status(db: Session, user_id: int, is_active: bool):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.is_active = is_active
        db.commit()
        db.refresh(user)
    return user

def get_users_count(db: Session):
    return db.query(User).count()

def get_companies_count(db: Session):
    return db.query(Company).count()

def get_active_users_count(db: Session):
    return db.query(User).filter(User.is_active == True).count()

# Flight CRUD operations
def create_flight(db: Session, flight: schemas.FlightCreate, company_id: int):
    from datetime import datetime
    
    # Конвертируем строки в даты и время
    departure_date = datetime.strptime(flight.departure_date, '%Y-%m-%d').date()
    departure_time = datetime.strptime(flight.departure_time, '%H:%M').time()
    arrival_date = datetime.strptime(flight.arrival_date, '%Y-%m-%d').date()
    arrival_time = datetime.strptime(flight.arrival_time, '%H:%M').time()
    
    db_flight = Flight(
        company_id=company_id,
        flight_number=flight.flight_number,
        departure_city=flight.departure_city,
        arrival_city=flight.arrival_city,
        departure_date=departure_date,
        departure_time=departure_time,
        arrival_date=arrival_date,
        arrival_time=arrival_time,
        total_seats=flight.total_seats,
        available_seats=flight.total_seats,  # Initially all seats are available
        price=flight.price
    )
    db.add(db_flight)
    db.commit()
    db.refresh(db_flight)
    return db_flight

def get_company_flights(db: Session, company_id: int, skip: int = 0, limit: int = 100):
    return db.query(Flight).filter(Flight.company_id == company_id).offset(skip).limit(limit).all()

def get_flight_by_id(db: Session, flight_id: int, company_id: int):
    return db.query(Flight).filter(Flight.id == flight_id, Flight.company_id == company_id).first()

def update_flight_status(db: Session, flight_id: int, company_id: int, is_active: bool):
    flight = db.query(Flight).filter(Flight.id == flight_id, Flight.company_id == company_id).first()
    if flight:
        flight.is_active = is_active
        db.commit()
        db.refresh(flight)
    return flight

def delete_flight(db: Session, flight_id: int, company_id: int):
    # Нельзя удалить рейс, если по нему уже есть билеты
    flight = db.query(Flight).filter(Flight.id == flight_id, Flight.company_id == company_id).first()
    if not flight:
        return None
    has_tickets = db.query(Ticket).filter(Ticket.flight_id == flight_id).count() > 0
    if has_tickets:
        return False
    db.delete(flight)
    db.commit()
    return True

def get_flight_passengers(db: Session, flight_id: int, company_id: int):
    # Проверяем принадлежность рейса компании
    flight = db.query(Flight).filter(Flight.id == flight_id, Flight.company_id == company_id).first()
    if not flight:
        return None
    # Выгружаем билеты с пользователями
    from sqlalchemy.orm import joinedload
    tickets = (
        db.query(Ticket)
        .options(joinedload(Ticket.user))
        .filter(Ticket.flight_id == flight_id)
        .order_by(Ticket.created_at.desc())
        .all()
    )
    result = []
    for t in tickets:
        result.append({
            "ticket_id": t.id,
            "status": t.status.value,
            "price": t.price,
            "created_at": t.created_at.isoformat(),
            "user": {
                "id": t.user.id,
                "email": t.user.email,
                "first_name": getattr(t.user, "first_name", None),
                "last_name": getattr(t.user, "last_name", None),
                "is_active": t.user.is_active,
            }
        })
    return result

def get_company_flights_count(db: Session, company_id: int):
    return db.query(Flight).filter(Flight.company_id == company_id).count()

def get_active_company_flights_count(db: Session, company_id: int):
    return db.query(Flight).filter(Flight.company_id == company_id, Flight.is_active == True).count()

def get_company_stats(db: Session, company_id: int):
    flights = db.query(Flight).filter(Flight.company_id == company_id).all()
    
    total_flights = len(flights)
    active_flights = len([f for f in flights if f.is_active])
    total_seats = sum(f.total_seats for f in flights)
    available_seats = sum(f.available_seats for f in flights)
    total_revenue = sum((f.total_seats - f.available_seats) * f.price for f in flights)
    
    return {
        "total_flights": total_flights,
        "active_flights": active_flights,
        "total_seats": total_seats,
        "available_seats": available_seats,
        "total_revenue": total_revenue
    }

# Tickets
def create_ticket(db: Session, user_id: int, flight_id: int):
    flight = db.query(Flight).filter(Flight.id == flight_id, Flight.is_active == True).first()
    if not flight or flight.available_seats <= 0:
        return None
    flight.available_seats -= 1
    ticket = Ticket(user_id=user_id, flight_id=flight_id, price=flight.price, status=TicketStatus.active)
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket

def get_user_tickets(db: Session, user_id: int):
    # Возвращаем билеты вместе с данными рейса
    from sqlalchemy.orm import joinedload
    return (
        db.query(Ticket)
        .options(joinedload(Ticket.flight))
        .filter(Ticket.user_id == user_id)
        .order_by(Ticket.created_at.desc())
        .all()
    )

def cancel_ticket(db: Session, user_id: int, ticket_id: int):
    from datetime import datetime, timedelta
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id, Ticket.user_id == user_id).first()
    if not ticket or ticket.status != TicketStatus.active:
        return None
    flight = db.query(Flight).filter(Flight.id == ticket.flight_id).first()
    # Проверка окна возврата 24ч
    flight_dt = datetime.combine(flight.departure_date, flight.departure_time)
    if flight_dt - datetime.utcnow() < timedelta(hours=24):
        return False
    ticket.status = TicketStatus.refunded
    ticket.canceled_at = datetime.utcnow()
    flight.available_seats += 1
    db.commit()
    db.refresh(ticket)
    return ticket
