.PHONY: install lint test eda

install:
	.\uv sync

lint:
	.\uv run ruff check src
	.\uv run ruff format src --check

test:
	$env:PYTHONPATH = "src"; .\uv run pytest

eda:
	$env:PYTHONPATH = "src"; .\uv run streamlit run dashboard/app.py