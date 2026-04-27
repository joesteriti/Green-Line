.PHONY: all venv install setup notebook run check lint format format-check test clean help

# Configuration 
PYTHON      := python3
PIP         := $(PYTHON) -m pip
VENV        := .venv
NOTEBOOKS   := fare_evasion.ipynb performance_model/performance_model.ipynb

all: setup check

venv:
	$(PYTHON) -m venv $(VENV)
	@echo "Activate with: source $(VENV)/bin/activate"

install:
	$(PIP) install -r requirements.txt

setup: venv
	@echo "Then run: source $(VENV)/bin/activate && make install"

# --- Run ---
notebook:
	$(PYTHON) -m jupyter notebook

run: notebook

# Testing 
check:
	@for f in $(NOTEBOOKS); do \
		test -f $$f || (echo "Missing notebook: $$f" && exit 1); \
	done
	@test -f data/green_line_headways.csv || (echo "Missing data/green_line_headways.csv" && exit 1)
	@test -f .env || (echo "Missing .env (copy from .env.example and add MBTA_API_KEY)" && exit 1)
	@echo "Basic project checks passed."

test: check
	@echo "Notebook-level tests are in the bottom cells of performance_model/performance_model.ipynb."

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf dist/ build/ .coverage htmlcov/ .ipynb_checkpoints

help:
	@echo ""
	@echo "Usage: make <target>"
	@echo ""
	@echo "  all           Setup + basic reproducibility checks"
	@echo "  venv          Create local virtual environment"
	@echo "  install       Install dependencies from requirements.txt"
	@echo "  setup         Create .venv and print activation hint"
	@echo "  notebook      Launch Jupyter Notebook"
	@echo "  run           Alias for notebook"
	@echo "  check         Validate required files (.env/data/notebooks)"
	@echo "  lint          Run flake8 on Python source file(s)"
	@echo "  format        Format Python source file(s)"
	@echo "  format-check  Check formatting without modifying"
	@echo "  test          Reminder target for notebook test cells"
	@echo "  clean         Remove common cache/build artifacts"
	@echo ""