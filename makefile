test:
	pytype cosmic/ tests/ && \
	pytest -s . --cov cosmic --cov-report term-missing

format:
	isort -rc . && \
	black -l 79 .
