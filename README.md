# Recipe App API

Containerised Django REST API for managing personal recipes, ingredients, and tags. The service exposes authenticated CRUD endpoints, auto-generated API docs, and production-ready Docker orchestration.

# Code Structure

High-level layout of the Django API project and supporting infrastructure.

```
.
├── app/
│   ├── app/            # Django project settings, URLs, WSGI config
│   ├── core/           # Shared models, permissions, management commands, tests
│   ├── recipe/         # Recipe domain: serializers, viewsets, routing, tests
│   └── user/           # Authentication endpoints, serializers, tests
├── Dockerfile          # Base image for the API service
├── docker-compose.yml  # Dev compose stack (API + Postgres)
├── docker-compose-deploy.yml  # Production-style stack with Nginx proxy
├── proxy/              # Nginx configuration templates for deployment
├── scripts/            # Helper shell scripts executed in containers
├── Makefile            # Convenience commands for containerized workflows
├── requirements*.txt   # Python dependencies for dev and prod
└── README.md           # Project usage, development, and deployment notes
```

The Django entrypoint is `app/manage.py`. Environment variables are loaded from `.env` for local use and from your host environment in deployed environments.

## Features
- Token-based authentication with user registration and profile management endpoints
- Recipe CRUD with nested tag and ingredient management plus image uploads
- Filtering helpers for tags, ingredients, and assigned-only lists
- Health check endpoint for uptime monitoring and readiness probes
- Auto-generated OpenAPI schema and Swagger UI via `drf-spectacular`
- Docker Compose workflows for local development and production-style deployment

## Tech Stack
- Python 3 / Django 3.2 with Django REST Framework and PostgreSQL
- `drf-spectacular` for schema + Swagger UI, `django-cors-headers` for CORS support
- Docker + docker-compose for dev and deployment; Nginx proxy for production image
- Makefile helpers to wrap common containerised commands

## Local Development
1. Install Docker and Docker Compose plus `make` (available by default on macOS/Linux).
2. Configure environment variables. An example `.env` is included in the repo—update the values or create your own with:
   ```bash
   cat <<'ENV' > .env
   DJANGO_SECRET_KEY=changeme
   DEBUG=1
   DB_HOST=db
   DB_NAME=devdb
   DB_USER=devuser
   DB_PASS=devpass
   ENV
   ```
3. Spin up the dev stack (builds images, runs migrations, starts containers):
   ```bash
   make build
   ```
4. Other helpful Make targets:
   - `make down` – stop containers and remove orphans
   - `make sh` – open a shell inside the app container
   - `make sh-db` – open a psql shell in the Postgres container
   - `make migrate` – apply migrations
   - `make migrations` – generate new migrations
   - `make url` – print service URLs


## API Docs & URLs
- API root: `http://localhost:8000/api/`
- Swagger UI: `http://localhost:8000/api/docs/`
- OpenAPI schema: `http://localhost:8000/api/schema/`
- Health check: `http://localhost:8000/api/health-check/`

## Tests
- Run unit tests: `make test`
- Lint with Flake8: `make flake`
- Auto-format with autopep8: `make flake-fix`

## API Overview
All recipe endpoints require token authentication unless read-only. Typical flow:
1. Create user: `POST /api/user/create/`
2. Obtain token: `POST /api/user/token/`
3. Authenticate requests with header `Authorization: Token <token>`

Key endpoint groups:
- `/api/recipe/recipes/` – list, create, update, delete recipes; supports `tags` and `ingredients` query parameters for filtering; upload images via `POST /{id}/upload-image/`
- `/api/recipe/tags/` – manage tags; optional `assigned_only=1` filter
- `/api/recipe/ingredients/` – manage ingredients with the same filters as tags

Swagger UI documents payloads, query parameters, and response schemas in detail.

## Deployment (EC2)
1. Provision an EC2 instance with Docker and Docker Compose installed; open ports 80/443 as needed.
2. Clone the repository (or pull your own fork) onto the instance: `git clone <repo> && cd recipe-app-api`.
3. Create a production `.env` with secure values (e.g., `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `DB_*`, and `DEBUG=0`).
4. Build and start the production stack with Nginx:
   ```bash
   docker compose -f docker-compose-deploy.yml build
   docker compose -f docker-compose-deploy.yml up -d
   ```
5. Run database migrations inside the app container:
   ```bash
   docker compose -f docker-compose-deploy.yml exec app python manage.py migrate
   ```
6. Verify health: `curl http://<server-ip>/api/health-check/`. Configure DNS/TLS for your domain as desired.

## Troubleshooting
- If the API container exits immediately, confirm Postgres credentials in `.env`.
- Use `docker compose logs app` (or `db`) to inspect startup issues.
- Ensure database migrations have run (`make migrate`) after modifying models.
