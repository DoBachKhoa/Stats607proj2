.PHONY: all venv test simulate analyze figures profile\
		help baseline complexity benchmark parallel\
		clean clean-env clean-generated

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
all : $(VENV_DIR) src/simulation.py src/methods.py src/analyze.py src/run_experiment.py clean-generated
	$(VENV_PY) -m src.run_experiment -u

help : $(VENV_DIR) src/simulation.py src/methods.py src/analyze.py src/run_experiment.py clean-generated
	$(VENV_PY) -m src.run_experiment -h

baseline :

complexity :

benchmark :

parallel :

# Profiler
profile : $(VENV_DIR) src/simulation.py src/methods.py src/analyze.py src/run_experiment.py clean-generated
	$(VENV_PY) -m cProfile -o prof.pstats -m src.run_experiment
	$(VENV_PY) -m snakeviz prof.pstats

# Virtual environment
$(VENV_DIR) : requirements.txt # check requirement changes
	$(PY) -m venv $(VENV_DIR)
	$(VENV_PIP) install -r requirements.txt
	touch $(VENV_DIR)

venv : $(VENV_DIR)

# Run tests
test : $(VENV_DIR) src/methods.py src/analyze.py
	$(VENV_PY) -m pytest src/testcorrectness.py

# Simulate 
$(RAW_RESULT_DIR) : $(VENV_DIR) src/simulation.py src/methods.py src/analyze.py params.json
	$(VENV_PY) -m src.simulation
	touch $(RAW_RESULT_DIR)
simulate : $(RAW_RESULT_DIR) 

# Run analyze
$(PROC_RESULT_DIR): $(RAW_RESULT_DIR) src/analyze.py
	$(VENV_PY) -m src.analyze
	touch $(PROC_RESULT_DIR)
analyze : $(PROC_RESULT_DIR) 

# Run plotting figures
$(PLOT_RESULT_DIR): $(PROC_RESULT_DIR) src/plotting.py
	$(VENV_PY) -m src.plotting
	touch $(PLOT_RESULT_DIR)
figures : $(PLOT_RESULT_DIR)

# Clean ups
clean : clean-env clean-generated

clean-venv : 
	rm -rf $(VENV_DIR)

clean-generated : 
	rm -rf $(RESULT_DIR)
	find . -type f -name "prof.pstats" -delete
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache"  -exec rm -rf {} +
