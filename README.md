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

## Key API Overview
- **Auth model:** Token auth; include `Authorization: Token <token>` on protected endpoints.
- Swagger UI at `/api/docs/`, OpenAPI schema at `/api/schema/`.
- **Health:**
   - `GET /api/health-check/` (public).
- **Users:**
  - `POST /api/user/create/` (register),
  - `POST /api/user/token/` (login),
- **Recipes:**
   - `GET/POST /api/recipe/recipes/` (supports `tags` and `ingredients` filters),
   - `POST /api/recipe/recipes/{id}/upload-image/` (upload images).
- **Tags:**
   - `GET/POST /api/recipe/tags/`,
- **Ingredients:**
   - `GET/POST /api/recipe/ingredients/`

## Deployment (AWS)
Terraform-based IaC that provisions the EC2 host and boots the stack automatically, see `terraform/README.md`.

## Troubleshooting
- If the API container exits immediately, confirm Postgres credentials in `.env`.
- Use `docker compose logs app` (or `db`) to inspect startup issues.
- Ensure database migrations have run (`make migrate`) after modifying models.
