# Event Management API

Django REST API for managing events and handling user registrations.

## Features

- **User Authentication:** Registration and JWT authentication (`djangorestframework-simplejwt`).
- **Event Management:** Full CRUD operations with custom permissions (only organizers can edit/delete their events).
- **Event Registration:** User registration for upcoming events with validation preventing double registration or past-event registration.
- **Search & Filtering:** Event search by title/description and filtering by date/location (`django-filter`).
- **Background Notifications:** Asynchronous email confirmation upon event registration using Celery & Redis.
- **API Documentation:** OpenAPI 3 schema and interactive Swagger UI via `drf-spectacular`.
- **CI/CD:** Automated code linting/formatting with Ruff, test suite with `pytest`, and GitHub Actions workflow.

## Tech Stack

- **Language & Framework:** Python 3.12, Django 6, Django REST Framework
- **Database & Queue:** PostgreSQL 15, Redis 7, Celery
- **Tooling:** Poetry, Ruff, pre-commit, pytest, Docker, Docker Compose

---

## Getting Started

### Prerequisites

- Docker and Docker Compose installed
- Git

### Running via Docker Compose

1. **Clone the repository:**
```bash
   git clone <repository-url>
   cd test-task-event-management
```

2. **Configure Environment Variables:** Create a `.env` file from the template:
```bash
   cp .env.example .env
```
   Ensure `POSTGRES_HOST=db` and `REDIS_URL=redis://redis:6379/0` inside `.env` for Docker containers.

3. **Build and start services:**
```bash
   docker-compose up --build -d
```

4. **Run Migrations:**
```bash
   docker-compose exec web python manage.py migrate
```

5. **Access Application:**
   - Swagger UI: http://127.0.0.1:8000/api/docs/
   - Admin Panel: http://127.0.0.1:8000/admin/

### Local Development Setup

1. **Install Dependencies:**
```bash
   poetry install
```

2. **Start Infrastructure Services** (PostgreSQL & Redis):
```bash
   docker-compose up -d db redis
```

3. **Configure Local `.env`:**
```ini
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5433
   REDIS_URL=redis://localhost:6379/0
```

4. **Apply Migrations:**
```bash
   poetry run python manage.py migrate
```

5. **Run Development Server:**
```bash
   poetry run python manage.py runserver
```

6. **Run Celery Worker** (in a separate terminal):
```bash
   poetry run celery -A core worker -l INFO --pool=solo
```

### Testing & Quality Control

- **Run Pytest:**
```bash
  poetry run pytest
```

- **Run Ruff Linter & Formatter:**
```bash
  poetry run ruff check .
  poetry run ruff format .
```