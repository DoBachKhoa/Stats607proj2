import json
import time
import argparse
import numpy as np
from src.run_experiment import main_experiment
from matplotlib import pyplot as plt

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', '-s', help='Experiment randomization seed (default: 17)', 
                        action='store', default=17)
    parser.add_argument('--alpha', '-a', help='P value threshold (default: 0.05)', action='store',
                         default=0.05)
    parser.add_argument('--outdir', '-o', help='Output directory in `results/` (default: plots)', 
                        action='store', default='plots')
    parser.add_argument('--num_reps', '-n',
                        help='Experiment sample sizes, comma-separated (default: [200, 630, 2000])', 
                        action='append', type=lambda s: [int(x) for x in s.split(',')])
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

if __name__ == '__main__':

    # Parsing input arguments
    args = parse_arguments()
    with open(args.infile, 'r') as file:
        params = json.load(file)
    params['seed'] = args.seed
    params['num_rep'] = args.num_reps
    params['criterion'] = args.criterion
    params['alpha'] = args.alpha
    params['outdir'] = args.outdir
    params['vectorize'] = not args.unvectorized
    params['n_jobs'] = args.n_jobs
    params['prob_alt_hypo'] = args.probabilistic

    # Parsing size
    if args.num_reps is None: num_reps = [200, 630, 2000]
    else: num_reps = [x for group in args.num_reps for x in group]

    # Run experiment
    times = []
    for num_rep in num_reps:
        print(f'Running with sample size {num_rep} ... ')
        params['num_rep'] = num_rep
        times.append(main_experiment(params=params, printing=False))
    plt.plot(num_reps, times)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Sample size (log scale)')
    plt.ylabel('Runtime (log scale)')
    plt.title('Runtime as a function of sample size', fontweight='bold')
    plt.savefig(f'results/{args.outdir}/complexity_plot.png', bbox_inches='tight')
    plt.close()
