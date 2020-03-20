build:
	docker-compose build

up:
	docker-compose up -d app

logs:
	docker-compose logs app | tail -100

down:
	docker-compose down

logs:
	docker-compose logs app | tail -100

all:	down build up test

test:
	mypy  cosmic/ tests/ --ignore-missing-imports && \
	pytest -s . --tb=short --cov cosmic --cov-report term-missing

unittest:
	mypy  cosmic/ tests/ --ignore-missing-imports && \
	pytest -s ./tests/unit ./tests/integration --cov cosmic --cov-report term-missing

format:
	isort -rc . && \
	black -l 79 .
