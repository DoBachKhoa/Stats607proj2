import sys
import json
import time
import numpy as np
from src.simulation import main_simulation
from src.analyze import main_analyze
from src.plotting import main_plotting

if __name__ == '__main__':

    # Pharsing parameters
    params_file = 'params.json'
    if len(sys.argv) > 1: params_file = str(sys.argv[1])
    with open(params_file, 'r') as file:
        params = json.load(file)

    # Running 3 steps of the experiment
    main_simulation(params=params)
    main_analyze(params=params)
    main_plotting(params=params)
