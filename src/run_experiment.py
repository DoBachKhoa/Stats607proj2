import sys
import json
import time
import argparse
import numpy as np
from src.simulation import main_simulation
from src.analyze import main_analyze
from src.plotting import main_plotting

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', '-s', help='Experiment randomization seed (default: 17)', 
                        action='store', default=17)
    parser.add_argument('--alpha', '-a', help='P value threshold (default: 0.05)', action='store',
                         default=0.05)
    parser.add_argument('--outdir', '-o', help='Output directory in `results/` (default: plots)', 
                        action='store', default='plots')
    parser.add_argument('--num_rep', '-n', help='Experiment sample size (default: 20000)', 
                        action='store', default=20000)
    parser.add_argument('--n_jobs', '-j', help='Number of thres to use (default: 1 - unparallel)', 
                        action='store', default=1)
    parser.add_argument('--unvectorized', '-u', help='Option to run unvectorized baseline', 
                        action='store_true')
    parser.add_argument('--probabilistic', '-p', help='Run probabilistic alt. hypo. generation \
                        instead of deterministic one', action='store_true')
    parser.add_argument('--criterion', '-c', help='Performance criterion (default: power)',
                        action='store', default='power')
    parser.add_argument('--infile', '-i', help='Input json file for experiment parameters \
                        that will be plotted: L_s, m_s, ratio_s, mode_s, and methods \
                        (default: params.json)', action='store', default='params.json')
    return parser.parse_args()

def main_experiment(params, printing=True):
    '''
    Main function to run the experiment.
    Will be run by the `if __name__ == '__main__'` of this script.
    Takes in a dictionary of keyword-parameter pairs.
    Returns the total runtime.
    '''
    # Running 3 steps of the experiment
    timestart = time.perf_counter()
    times = []
    times.append(['Simulation', main_simulation(params=params, print_params=printing)])
    times.append(['Process data', main_analyze(params=params, print_params=printing)])
    times.append(['Plotting', main_plotting(params=params, print_params=printing)])

    # Print out the time records
    if printing:
        print('Runtime decomposition:')
        for step, step_times in times:
            print(f'   Step [{step}]:')
            for sub_step, step_time in step_times:
                print(f'      [{sub_step}]: {np.round(step_time, 3)}s')

    # Returns runtime
    return time.perf_counter()-timestart

if __name__ == '__main__':

    # Parsing input arguments
    args = parse_arguments()
    with open(args.infile, 'r') as file:
        params = json.load(file)
    params['seed'] = args.seed
    params['num_rep'] = args.num_rep
    params['criterion'] = args.criterion
    params['alpha'] = args.alpha
    params['outdir'] = args.outdir
    params['vectorize'] = not args.unvectorized
    params['n_jobs'] = args.n_jobs
    params['prob_alt_hypo'] = args.probabilistic

    # Run experiment
    main_experiment(params=params)
