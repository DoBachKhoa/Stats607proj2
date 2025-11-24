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
    times = []
    times.append(['Simulation', main_simulation(params=params)])
    times.append(['Process data', main_analyze(params=params)])
    times.append(['Plotting', main_plotting(params=params)])

    # Print out the time records
    print('Runtime decomposition:')
    for step, step_times in times:
        print(f'   Step [{step}]:')
        for sub_step, step_time in step_times:
            print(f'      [{sub_step}]: {np.round(step_time, 3)}s')
