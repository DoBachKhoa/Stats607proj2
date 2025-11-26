import os
import time
import json
import numpy as np
from scipy.stats import norm
from joblib import Parallel, delayed
from src.methods import NormalMeanHypotheses, NormalMeanHypothesesProbabilistic, MultiTest
from src.utils import compare_reject_result, distribute_means_BH_exp, \
                      generate_filename_BH_exp, generate_params_BH_exp
from src.constants import RAW_OUTPUT_DIR
from tqdm import tqdm

dict_methods = {
    'Bonferroni': MultiTest.BonferroniMethod,
    'Hochberg': MultiTest.HochbergMethod,
    'BH':MultiTest.BHMethod
}

dict_methods_fast = {
    'Bonferroni': MultiTest.BonferroniMethod,
    'Hochberg': MultiTest.HochbergMethodFast,
    'BH':MultiTest.BHMethodFast
}

def probabilistic_alt_distribution(L, mode):
    a = np.array([L/4., L/2., 3*L/4., L])
    if   mode == 'D': p = np.array([.4, .3, .2, .1])
    elif mode == 'E': p = np.array([.25, .25, .25, .25])
    elif mode == 'I': p = np.array([.1, .2, .3, .4])
    else: raise ValueError(f"Invalid mode in put: {mode}")
    return a, p

def simulate_BH_exp(L, m_0, m, mode, num_rep, method, criterion, alpha=0.05, saving=True, \
                    vectorize=False, prob_alt_hypo=True, seed=17):
    
    # Generate data
    rng = np.random.default_rng(seed=seed)
    if not prob_alt_hypo:
        alt_means = distribute_means_BH_exp(m-m_0, L, mode)
        generator = NormalMeanHypotheses(m_0, alt_means, sigma=1., rng=rng)
    else:
        a, p = probabilistic_alt_distribution(L, mode)
        generator = NormalMeanHypothesesProbabilistic(m_0, num_alt=m-m_0, alt_means=a, alt_probs=p, rng=rng)
    test = lambda data: 1-2*np.abs(norm.cdf(data)-0.5)
    p_values = generator.generate_p_values(test, size=num_rep)

    # Run hypothesis test
    control_method = dict_methods_fast[method] if vectorize else dict_methods[method]
    decision = control_method(p_values, alpha)
    ground_truth = np.array([0]*m_0+[1]*(m-m_0))
    result = compare_reject_result(ground_truth, decision)
    
    # Save in csv
    if saving:
        filename = generate_filename_BH_exp(L, m_0, m, mode, num_rep, method, criterion)
        np.save(f'{RAW_OUTPUT_DIR}/{filename}', result[criterion])
    return result

def _main_simulation_L(params, L=None):
    '''
    Inner function to be called by the main function `main_simulation`.
    Generates all parameterset from `params` dictionary and runs all of them.

    PARAMETERS
    ----------
    params : dict
        input parameter arguments
    L : Optional (list or float)
        Input parameter L.
        If not None, use this argument instead of `params['L']`
    '''
    # Handling input parameter L
    if L is None: Ls = params['L_s']
    elif not isinstance(L, list): Ls = [L]
    else: Ls = L

    # Main loop
    generator = generate_params_BH_exp(Ls, params['m_s'], params['ratio_s'], 
                                       params['mode_s'], params['methods'])
    for (l, m, r, mode, method) in tqdm(list(generator)):
        m_0 = int(np.rint(m*float(r)).astype('int'))
        simulate_BH_exp(l, m_0, m, mode, params['num_rep'], method, params['criterion'], 
                        alpha=params['alpha'], saving=True, seed=params['seed'],
                        vectorize=params['vectorize'], prob_alt_hypo=params['prob_alt_hypo'])


def main_simulation(filename='params.json', params=None, print_params=True):
    '''
    Main function to simulate and generate raw output.
    Will be run by the `if __name__ == '__main__'` of this script.

    PARAMETERS
    ----------
    filename : str (default : 'params.json')
        if params is None: load json file from filename as params.
    params : Optional (dict) (default : None)
        input parameter for the simulation.
        if None: load json file from filename as params.
    print_params : Optional (bool)
        prints parameters

    RETURNS
    -------
    Runtime record of the script
    '''
    time1 = time.perf_counter()
    os.makedirs(RAW_OUTPUT_DIR, exist_ok=True)
    if params is None:
        with open(filename, 'r') as file:
            params = json.load(file)
    if print_params:
        print('=============== Begin simulation ===============')
        print(' L_s: ', params['L_s'])
        print(' m_s: ', params['m_s'])
        print(' ratio_s: ', params['ratio_s'])
        print(' num_rep: ', params['num_rep'])
        print(' methods: ', params['methods'])
        print(f" criterion: {params['criterion']}")
        print(f" alpha: {params['alpha']}")
        print('================================================')
    time2 = time.perf_counter()
    if params['n_jobs'] not in [0, 1]:
        parallel_function = lambda L: _main_simulation_L(params=params, L=L)
        Parallel(n_jobs=params['n_jobs'])(delayed(parallel_function)(L) for L in params['L_s'])
    else: _main_simulation_L(params=params)
    time3 = time.perf_counter()
    return [['Set ups', time2-time1], ['Main loop', time3-time2]]
        
if __name__ == '__main__':
    main_simulation()