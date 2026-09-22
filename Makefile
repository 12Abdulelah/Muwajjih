PYTHON ?= python
IMAGE ?= muwajjih:dev

.PHONY: install train test test-fast test-slow lint typecheck run image smoke up

install:
	$(PYTHON) -m pip install -e ".[dev,train]"

train:
	PYTHONPATH=src $(PYTHON) -m muwajjih.adapters.model.train

test:
	PYTHONPATH=src $(PYTHON) -m pytest

test-fast:
	PYTHONPATH=src $(PYTHON) -m pytest -m "not slow"

test-slow:
	PYTHONPATH=src $(PYTHON) -m pytest -m slow

lint:
	PYTHONPATH=src $(PYTHON) -m ruff check src tests scripts
	PYTHONPATH=src lint-imports
	$(MAKE) typecheck

typecheck:
	PYTHONPATH=src $(PYTHON) -m mypy src/muwajjih/domain src/muwajjih/service src/muwajjih/api

run:
	PYTHONPATH=src $(PYTHON) -m uvicorn muwajjih.api.app:app --host 0.0.0.0 --port 8000

image:
	docker build -t $(IMAGE) .

smoke:
	IMAGE=$(IMAGE) bash ./scripts/smoke.sh

up:
	docker compose up --build
