.PHONY: install format lint test download clean eda equilibrium all

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

equilibrium:
	.\uv run python src/models/equilibrium.py

all: download clean eda equilibrium