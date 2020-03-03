test:
	pytype cosmic/ tests/ && \
	pytest -s .

format:
	isort -rc . && \
	black -l 79 .
