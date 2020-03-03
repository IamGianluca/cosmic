test:
	pytype cosmic/ tests/ && \
	pytest -s .

format:
	black -l 79 .
