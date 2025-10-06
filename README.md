# Flight Ticketing Web Service

A web application for flight ticket booking with user authentication and role-based access control.

## Features
- User registration and authentication
- Role-based access (regular users, managers, admins)
- Flight search and booking interface
- Admin dashboard for system management
- Company dashboard for managers

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Modern web browser

### Quick Start (Windows)
1. **Install Dependencies**: The virtual environment is already set up with all required packages
2. **Run Backend**: Double-click `run_backend.bat` or run:
   ```bash
   uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```
3. **Run Frontend**: Double-click `run_frontend.bat` or open `frontend/index.html` in your browser

### Manual Setup
1. **Activate Virtual Environment**:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

2. **Install Dependencies** (if not already installed):
   ```bash
   pip install -r backend/requirements.txt
   ```

3. **Run Backend**:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

4. **Open Frontend**: Open `frontend/index.html` in your browser

## Usage

### Default Admin Account
- **Email**: `admin@gmail.com`
- **Password**: `admin123!`
- **Role**: Admin (full system access)

### User Registration
- Regular users can register through the signup page
- Only regular users can self-register
- Managers and admins must be created by existing admins

### Navigation
- **Home Page**: Browse flights and search
- **Login**: Access user dashboard, company dashboard, or admin dashboard based on role
- **Signup**: Register as a new regular user

## API Documentation
Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation.

## Project Structure
```
project/
├── backend/           # FastAPI backend
│   ├── main.py       # Main application
│   ├── models.py     # Database models
│   ├── schemas.py    # Pydantic schemas
│   ├── auth.py       # Authentication logic
│   ├── crud.py       # Database operations
│   └── routers/      # API routes
├── frontend/         # HTML frontend
│   ├── index.html    # Home page
│   ├── login.html    # Login page
│   ├── signup.html   # Registration page
│   └── *_dashboard.html # Role-specific dashboards
└── run_*.bat         # Windows batch files for easy startup
```

## Troubleshooting
- **Backend won't start**: Make sure port 8000 is not in use
- **CORS errors**: The backend is configured to allow requests from localhost and file:// protocols
- **Database issues**: The SQLite database will be created automatically on first run
 
 youtube: https://youtu.be/N5QJgSCeDzs