include .env

export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1
.DEFAULT_GOAL := build
SUBDIR = .

indocker = $(if $(IN_DOCKER), $(1), docker compose exec app sh -c '(cd $(SUBDIR) && $(1))')

## spin up the env
build: down
	docker compose build
	docker compose up -d
	$(MAKE) url

## stop container
down:
	docker compose down --remove-orphans

sh:
	docker compose exec app sh

sh-db:
	docker exec -it db psql --username postgres

migrations:
	$(call indocker, python manage.py wait_for_db && python manage.py makemigrations)


migrate:
	$(call indocker, python manage.py migrate)

test: flake
	$(call indocker, python manage.py test)

flake:
	$(call indocker, flake8)

flake-fix:
	$(call indocker, autopep8 --recursive --in-place app)

url:
	@ printf 'API: http://0.0.0.0:8000 \n'
	@ printf 'DB: $(DB_HOST) \n'
