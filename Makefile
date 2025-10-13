.PHONY: all test clean

# Abbreviations
PY := python3
PIP := python3 -m pip 
VENV_DIR := .venv
VENV_PYT := $(VENV_DIR)/bin/$(PY)
VENV_PIP := $(VENV_DIR)/bin/$(PIP)

# Default target first
all : test figures

# Virtual environment
venv : requirements.txt # check requirement changes
	$(PY) -m venv $(VENV_DIR)
	$(VENV_PIP) install -r requirements.txt

# Run tests
test : venv

# Run simulation
simulate : venv

# Run analyze
analyze : venv simulate

# Run plotting figures
figures : venv analyze

# Clean ups
clean : 
	rm -rf $(VENV_DIR)
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete



