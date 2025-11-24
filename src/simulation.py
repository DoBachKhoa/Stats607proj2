import os
import time
import math
import json
import numpy as np
from scipy.stats import norm
from src.methods import NormalMeanHypotheses, MultiTest
from src.utils import compare_reject_result, distribute_means_BH_exp, \
                      generate_filename_BH_exp, generate_params_BH_exp
from src.constants import RAW_OUTPUT_DIR
from tqdm import tqdm

dict_methods = {
    'Bonferroni': MultiTest.BonferroniMethod,
    'Hochberg': MultiTest.HochbergMethod,
    'BH':MultiTest.BHMethod
}

def simulate_BH_exp(L, m_0, m, mode, num_rep, method, criterion, alpha=0.05, saving=True):
    
    # Generate data
    seed = 17
    rng = np.random.default_rng(seed=seed)
    alt_means = distribute_means_BH_exp(m-m_0, L, mode)
    generator = NormalMeanHypotheses(m_0, alt_means, sigma=1., rng=rng)
    test = lambda data: 1-2*np.abs(norm.cdf(data)-0.5)
    p_values = generator.generate_p_values(test, size=num_rep)

    # Run hypothesis test
    control_method = dict_methods[method]
    decision = control_method(p_values, alpha)
    ground_truth = np.array([0]*m_0+[1]*(m-m_0))
    result = compare_reject_result(ground_truth, decision)
    
    # Save in csv
    if saving:
        filename = generate_filename_BH_exp(L, m_0, m, mode, num_rep, method, criterion)
        np.save(RAW_OUTPUT_DIR+filename, result[criterion])
    return result

def main_simulation(filename='params.json', params=None):
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

    RETURNS
    -------
    Runtime record of the script
    '''
    time1 = time.perf_counter()
    os.makedirs(RAW_OUTPUT_DIR, exist_ok=True)
    if params is None:
        with open(filename, 'r') as file:
            params = json.load(file)
    print('=============== Begin simulation ===============')
    print(' L_s: ', params['L_s'])
    print(' m_s: ', params['m_s'])
    print(' ratio_s: ', params['ratio_s'])
    print(' num_rep: ', params['num_rep'])
    print(' methods: ', params['methods'])
    print(f" criterion: {params['criterion']}")
    print(f" alpha: {params['alpha']}")
    print('================================================')
    generator = generate_params_BH_exp(params['L_s'], params['m_s'], params['ratio_s'], 
                                       params['mode_s'], params['methods'])
    time2 = time.perf_counter()
    for (L, m, r, mode, method) in tqdm(list(generator)):
        m_0 = int(np.rint(m*float(r)).astype('int'))
        simulate_BH_exp(L, m_0, m, mode, params['num_rep'], method, params['criterion'], 
                        alpha=params['alpha'], saving=True)
    time3 = time.perf_counter()
    return [['Set ups', time2-time1], ['Main loop', time3-time2]]
        
if __name__ == '__main__':
    main_simulation()