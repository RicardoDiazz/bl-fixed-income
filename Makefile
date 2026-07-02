.PHONY: install format lint test download clean features eda all

install:
	.\uv sync

format:
	.\uv run ruff format src/

lint:
	.\uv run ruff check src/

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

all: install download clean features test