.PHONY: all venv test simulate analyze figures clean

# Abbreviations
PY := python3
PIP := python3 -m pip 
VENV_DIR := .venv
VENV_PY := $(VENV_DIR)/bin/$(PY)
VENV_PIP := $(VENV_DIR)/bin/$(PIP)
RESULT_DIR := results
RAW_RESULT_DIR := $(RESULT_DIR)/raw # Raw generated data
PROC_RESULT_DIR := $(RESULT_DIR)/processed # Processed data/summaries
PLOT_RESULT_DIR := $(RESULT_DIR)/plots # Plots

# Default target first
all : test simulate analyze figures

# Virtual environment
$(VENV_DIR) : requirements.txt # check requirement changes
	$(PY) -m venv $(VENV_DIR)
	$(VENV_PIP) install -r requirements.txt
	touch $(VENV_DIR)

venv : $(VENV_DIR)

# Run tests
test : $(VENV_DIR)
	$(VENV_PY) -m pytest src/testcorrectness.py

# Simulate 
$(RAW_RESULT_DIR) : $(VENV_DIR) src/analyze.py
	mkdir -p $(RESULT_DIR)
	mkdir -p $(RAW_RESULT_DIR)
	$(VENV_PY) src/simulation.py
	touch $(RAW_RESULT_DIR)
simulate : $(RAW_RESULT_DIR) 

# Run analyze
$(PROC_RESULT_DIR): $(RAW_RESULT_DIR) src/analyze.py
	mkdir -p $(PROC_RESULT_DIR)
	$(VENV_PY) src/analyze.py
	touch $(PROC_RESULT_DIR)
analyze : $(PROC_RESULT_DIR) 

# Run plotting figures
$(PLOT_RESULT_DIR): $(PROC_RESULT_DIR) src/plotting.py
	mkdir -p $(PLOT_RESULT_DIR)
	$(VENV_PY) src/plotting.py
	touch $(PLOT_RESULT_DIR)
figures : $(PLOT_RESULT_DIR)

# Clean ups
clean : 
	rm -rf $(VENV_DIR)
	rm -rf $(RESULT_DIR)
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
