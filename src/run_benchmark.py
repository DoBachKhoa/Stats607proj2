import json
import time
import argparse
import numpy as np
from src.run_experiment import main_experiment

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', '-s', help='Experiment randomization seed (default: 17)', 
                        action='store', default=17)
    parser.add_argument('--alpha', '-a', help='P value threshold (default: 0.05)', action='store',
                         default=0.05)
    parser.add_argument('--num_rep', '-n', help='Experiment sample size (default: 20000)', 
                        action='store', default=20000)
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
    params['num_rep'] = args.num_rep
    params['criterion'] = args.criterion
    params['alpha'] = args.alpha

    # Run the cases
    times = dict()
    for vec in [False, True]:
        for n_jobs in [1, 2]:
            for prob in [True, False]:
                name = f"{'vec'  if vec else 'unvec'}_"+\
                       f"{'par'  if n_jobs>1 else 'unpar'}_"+\
                       f"{'prob' if prob else 'des'}"
                params['outdir'] = f'benchmark_plots/{name}'
                params['vectorize'] = vec
                params['n_jobs'] = n_jobs
                params['prob_alt_hypo'] = prob
                print(f'Running experiment {name} ... ')
                times.setdefault(vec, dict())\
                     .setdefault(n_jobs, dict())[prob] = \
                     np.round(main_experiment(params=params, printing=False), 3)
                
    # Print output
    time_vec_par = f'{times[True][2][False]}/{times[True][2][True]}'
    time_vec_unpar = f'{times[True][1][False]}/{times[True][1][True]}'
    time_unvec_par = f'{times[False][2][False]}/{times[False][2][True]}'
    time_unvec_unpar = f'{times[False][1][False]}/{times[False][1][True]}'
    time_vec_par = time_vec_par + ' '*(14-len(time_vec_par))
    time_vec_unpar = time_vec_unpar + ' '*(14-len(time_vec_unpar))
    time_unvec_par = time_unvec_par + ' '*(14-len(time_unvec_par))
    time_unvec_unpar = time_unvec_unpar + ' '*(14-len(time_unvec_unpar))
    print()
    print()
    print('Timing of the runs (deterministic/probabilistic alt. hypo. p value generation):')
    print()
    print(f'                     Unvectorized           Vectorized')
    print(f'               +----------------------+----------------------+')
    print(f'               |                      |                      |')
    print(f'Unparallelized |    {time_unvec_unpar}    |    {time_vec_unpar}    |')
    print(f'               |                      |                      |')
    print(f'               +----------------------+----------------------+')
    print(f'               |                      |                      |')
    print(f'Parallelized   |    {time_unvec_par}    |    {time_vec_par}    |')
    print(f'               |                      |                      |')
    print(f'               +----------------------+----------------------+')
