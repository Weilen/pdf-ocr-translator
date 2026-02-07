.PHONY: lint test format

lint:
	ruff check .

test:
	pytest

format:
	ruff format .
