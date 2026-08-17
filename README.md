# Event Management API

Django REST API for managing events and user registrations.

## Features

- **User Authentication:** Registration and JWT-based auth via `djangorestframework-simplejwt`.
- **Event Management:** Full CRUD with permissions — only the organizer can edit or delete their own events.
- **Event Registration:** Users can register for events; double registration and past-event registration are blocked.
- **Search & Filtering:** Events can be searched by title/description and filtered by date or location (`django-filter`).
- **Email Notifications:** Registration confirmation emails are sent asynchronously via Celery & Redis.
- **API Docs:** OpenAPI 3 schema + Swagger UI powered by `drf-spectacular`.
- **Linting, Tests & CI:** Ruff for code style, `pytest` for tests, GitHub Actions for automation.

## Tech Stack

- **Language & Framework:** Python 3.12, Django 6, Django REST Framework
- **Database & Queue:** PostgreSQL 15, Redis 7, Celery
- **Tooling:** Poetry, Ruff, pre-commit, pytest, Docker & Docker Compose

---

## Getting Started

### Prerequisites

- Docker and Docker Compose installed
- Git

### Running via Docker Compose

1. **Clone the repository:**
```bash
   git clone https://github.com/vlchshn/test-task-event-management.git
   cd test-task-event-management
```

2. **Configure Environment Variables:** Create a `.env` file from the template:
```bash
   cp .env.example .env
```
   Make sure `POSTGRES_HOST=db` and `REDIS_URL=redis://redis:6379/0` are set inside `.env` for Docker.

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

### Testing

- **Run Pytest:**
```bash
  poetry run pytest
```

- **Run Ruff Linter & Formatter:**
```bash
  poetry run ruff check .
  poetry run ruff format .
```
