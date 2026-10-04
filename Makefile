.PHONY: install format lint test download clean features eda report deploy all

install:
	.\uv sync

format:
	.\uv run ruff format src/ dashboard/ tests/

lint:
	.\uv run ruff check src/ dashboard/ tests/

test:
	.\uv run pytest

download:
	.\uv run python src/data/download.py

clean:
	.\uv run python src/data/clean.py

features:
	.\uv run python src/features/returns.py
	.\uv run python src/features/targets.py
	.\uv run python src/features/build_features.py

eda:
	.\uv run python -m streamlit run dashboard/app.py

report:
	.\uv run python dashboard/report/generate_reports.py

deploy:
	.\uv run python -m streamlit run dashboard/presentation.py

all: install download clean features test report
