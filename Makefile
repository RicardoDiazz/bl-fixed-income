.PHONY: install format lint test download clean eda all

install:
	.\uv sync

format:
	.\uv run ruff format src/

lint:
	.\uv run ruff check src/

download:
	.\uv run python src/data/download.py

clean:
	.\uv run python src/data/clean.py

eda:
	.\uv run python src/visualization/eda.py

all: download clean eda