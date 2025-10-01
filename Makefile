.PHONY: fmt lint test

fmt:
	python -m pip install -q ruff black
	ruff check --fix . || true
	black .

lint:
	python -m pip install -q ruff
	ruff check .

test:
	python -m pip install -q -r requirements.txt
	python -m pip install -q pytest
	pytest -q

