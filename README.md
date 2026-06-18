# Employee Management System API

A REST API for managing employees and attendance, built with Django and Django REST Framework. The project follows a strict N-Tier Architecture and is fully containerized with Docker.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Running with Docker](#running-with-docker)
- [Running Tests](#running-tests)
- [API Endpoints](#api-endpoints)
- [API Documentation](#api-documentation)
- [Running Celery](#running-celery)
- [Git Workflow](#git-workflow)

---

## Overview

The Employee Management System API provides endpoints to:

- Manage employees (create, update, soft delete, search, filter)
- Record and track attendance (check-in, check-out, status)
- Generate attendance reports per employee or per department

All endpoints are protected with JWT authentication. The system automatically switches between SQLite (development) and PostgreSQL (production) based on environment variables.

---

## Architecture

The project follows a strict **N-Tier Architecture**. Each layer has one responsibility and communicates only with the layer directly below it:

```
Request
   ↓
View Layer       → Handles HTTP requests and responses
   ↓
Service Layer    → Contains all business logic
   ↓
Repository Layer → Handles all database queries
   ↓
Database Layer   → SQLite (dev) or PostgreSQL (prod)
```

### Rules
- Views never access models directly
- Views only call services
- Services only call repositories
- Repositories are the only ones that touch the database
- Business logic lives exclusively in services

---

## Project Structure

```
emp_mgmt_system/
│
├── apps/
│   ├── employees/           # Employee management
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── repositories.py
│   │   ├── services.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── tasks.py
│   │   └── tests/
│   │       ├── factories.py
│   │       ├── test_models.py
│   │       ├── test_repositories.py
│   │       ├── test_services.py
│   │       └── test_views.py
│   │
│   ├── attendance/          # Attendance tracking
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── repositories.py
│   │   ├── services.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── tests/
│   │
│   └── reports/             # Attendance reporting
│       ├── services.py
│       ├── views.py
│       └── urls.py
│
├── config/                  # Django project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── celery.py
│   └── wsgi.py
│
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── requirements.txt
├── pytest.ini
└── README.md
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.12 | Programming language |
| Django 6.0 | Web framework |
| Django REST Framework | API development |
| PostgreSQL 15 | Production database |
| SQLite | Development database |
| Redis 7 | Message broker for Celery |
| Celery 5 | Async task processing |
| Docker + Docker Compose | Containerization |
| JWT (SimpleJWT) | Authentication |
| drf-spectacular | API documentation |
| pytest + Factory Boy | Testing |
| uv | Package management |

---

## Getting Started

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager
- Docker Desktop (for Docker setup)

### Local Development

**1. Clone the repository:**
```bash
git clone https://github.com/DiamantONDO/employee_management_system.git
cd employee_management_system
```

**2. Install dependencies:**
```bash
uv sync
```

**3. Create your environment file:**
```bash
copy .env.example .env
```

**4. Run migrations:**
```bash
uv run python manage.py migrate
```

**5. Create a superuser:**
```bash
uv run python manage.py createsuperuser
```

**6. Start the development server:**
```bash
uv run python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000`.

---

## Environment Variables

Create a `.env` file at the root of the project. Use `.env.example` as a reference.

| Variable | Description | Example |
|---|---|---|
| `SECRET_KEY` | Django secret key | `django-super-secret-key-...` |
| `DEBUG` | Enable debug mode | `True` |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `localhost,127.0.0.1` |
| `PRODUCTION` | Switch to PostgreSQL | `False` |
| `DB_NAME` | PostgreSQL database name | `emp_mgmt_db` |
| `DB_USER` | PostgreSQL user | `postgres` |
| `DB_PASSWORD` | PostgreSQL password | `yourpassword` |
| `DB_HOST` | PostgreSQL host | `db` |
| `DB_PORT` | PostgreSQL port | `5432` |
| `REDIS_URL` | Redis connection URL | `redis://redis:6379/0` |

> **Note:** Never commit your `.env` file to Git. It is listed in `.gitignore`.

---

## Running with Docker

Docker runs the complete stack with one command — no manual setup needed.

**Start all services:**
```bash
docker compose up --build
```

This starts 5 services:

| Service | Description | Port |
|---|---|---|
| `web` | Django API server | 8001 |
| `db` | PostgreSQL database | 5432 |
| `redis` | Redis message broker | 6379 |
| `celery_worker` | Processes async tasks | — |
| `celery_beat` | Schedules periodic tasks | — |

**Stop all services:**
```bash
docker compose down
```

**View logs for a specific service:**
```bash
docker compose logs celery_worker
docker compose logs web
```

---

## Running Tests

The project uses `pytest` and `factory-boy` for testing.

**Run all tests:**
```bash
uv run pytest -v
```

**Run tests for a specific layer:**
```bash
# Model tests
uv run pytest apps/employees/tests/test_models.py -v

# Repository tests
uv run pytest apps/employees/tests/test_repositories.py -v

# Service tests
uv run pytest apps/employees/tests/test_services.py -v

# API tests
uv run pytest apps/employees/tests/test_views.py -v
```

**Run with coverage:**
```bash
uv run pytest --cov=apps -v
```

The project maintains **57 tests** across all layers — models, repositories, services and views.

---

## API Endpoints

All endpoints require a JWT Bearer token in the Authorization header:
```
Authorization: Bearer <access_token>
```

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/auth/login/` | Login and get JWT token |
| POST | `/api/v1/auth/refresh/` | Refresh an expired token |

**Login example:**
```json
POST /api/v1/auth/login/
{
  "username": "admin",
  "password": "yourpassword"
}
```

**Response:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### Employees

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/employees/` | List all employees |
| POST | `/api/v1/employees/` | Create a new employee |
| GET | `/api/v1/employees/{id}/` | Retrieve an employee |
| PUT | `/api/v1/employees/{id}/` | Update an employee |
| PATCH | `/api/v1/employees/{id}/` | Partially update an employee |
| DELETE | `/api/v1/employees/{id}/` | Soft delete an employee |

**Query parameters for listing:**

| Parameter | Type | Description |
|---|---|---|
| `search` | string | Search by first or last name |
| `department` | string | Filter by department (e.g. `IT`, `HR`) |
| `is_active` | boolean | Filter by active status |

**Create employee example:**
```json
POST /api/v1/employees/
{
  "employee_code": "EMP001",
  "first_name": "Diamant",
  "last_name": "Anthony",
  "email": "diamant@company.com",
  "department": "IT",
  "position": "Software Engineer",
  "date_joined": "2026-01-01"
}
```

> **Note:** Deletion is a soft delete — the employee is marked as `is_active: false` and remains in the database.

---

### Attendance

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/attendances/` | List all attendance records |
| POST | `/api/v1/attendances/` | Create an attendance record |
| GET | `/api/v1/attendances/{id}/` | Retrieve a record |
| PUT | `/api/v1/attendances/{id}/` | Update a record |
| PATCH | `/api/v1/attendances/{id}/` | Partially update a record |
| DELETE | `/api/v1/attendances/{id}/` | Delete a record |

**Query parameters for listing:**

| Parameter | Type | Description |
|---|---|---|
| `employee_id` | UUID | Filter by employee |
| `status` | string | Filter by status (`PRESENT`, `ABSENT`) |
| `date` | date | Filter by specific date |
| `start_date` | date | Filter from this date |
| `end_date` | date | Filter to this date |

**Create attendance example:**
```json
POST /api/v1/attendances/
{
  "employee": "uuid-of-employee",
  "attendance_date": "2026-06-18",
  "check_in_time": "09:00:00",
  "check_out_time": "17:00:00",
  "status": "PRESENT"
}
```

---

### Reports

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/reports/employee-summary/` | Attendance summary for one employee |
| GET | `/api/v1/reports/department-summary/` | Attendance summary for a department |

**Employee summary example:**
```
GET /api/v1/reports/employee-summary/?employee_id=uuid&start_date=2026-01-01&end_date=2026-06-18
```

**Response:**
```json
{
  "employee_id": "uuid",
  "employee_name": "Diamant Anthony",
  "total_days": 30,
  "present_days": 25,
  "absent_days": 5,
  "attendance_percentage": 83.33
}
```

---

## API Documentation

Interactive API documentation is available when the server is running:

| Tool | URL |
|---|---|
| Swagger UI | `http://127.0.0.1:8001/docs/` |
| ReDoc | `http://127.0.0.1:8001/redoc/` |

Both show all endpoints with request/response examples and allow you to test the API directly from the browser.

---

## Running Celery

Celery handles async and scheduled tasks (e.g. daily reports, cleanup jobs).

**Start the worker manually (outside Docker):**
```bash
celery -A config worker --loglevel=info
```

**Start the beat scheduler:**
```bash
celery -A config beat --loglevel=info
```

When using Docker, both are started automatically as separate services.

---

## Git Workflow

Each feature is developed in its own branch and merged to `main` via a Pull Request. Tests must pass before merging.

**Branch naming:**
```
feature/employee-model
feature/attendance-model
feature/employee-repository
feature/attendance-repository
feature/service-layer
feature/api-layer
feature/docker
feature/celery
feature/documentation
```

**Commit message format (Conventional Commits):**

| Prefix | When to use |
|---|---|
| `feat:` | New feature |
| `fix:` | Bug fix |
| `test:` | Adding or updating tests |
| `docs:` | Documentation |
| `refactor:` | Code improvement, no new feature |
| `chore:` | Config, dependencies, tooling |

**Example:**
```bash
git checkout -b feature/employee-model
# make changes
git add .
git commit -m "feat: add employee model with UUID and soft delete"
git push origin feature/employee-model
# open Pull Request on GitHub → merge → done
```

---

## Author

**Diamant Anthony**
Software Engineer Intern — Comprehensive Staffing Resources Ltd