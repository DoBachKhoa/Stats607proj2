import os
import time
import math
import json
import numpy as np
from tqdm import tqdm
from src.utils import mean_and_se, generate_params_BH_exp, \
                      generate_filename_BH_exp, generate_jsonname_BH_exp
from src.constants import RAW_OUTPUT_DIR, PROCESSED_OUTPUT_DIR

def main_analyze(filename='params.json', params=None, print_params=True):
    '''
    Main function to analyze the raw output and use that to generate processed ones.
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
    os.makedirs(PROCESSED_OUTPUT_DIR, exist_ok=True)
    if params is None:
        with open(filename, 'r') as file:
            params = json.load(file)
    if print_params:
        print('=============== Begin raw output summary ===============')
        print(' L_s: ', params['L_s'])
        print(' m_s: ', params['m_s'])
        print(' ratio_s: ', params['ratio_s'])
        print(' num_rep: ', params['num_rep'])
        print(' methods: ', params['methods'])
        print(f" criterion: {params['criterion']}")
        print(f" alpha: {params['alpha']}")
        print('=======================================================')
    time_setup = time.perf_counter()-time1
    time_process = 0
    time_save = 0
    for L in params['L_s']:
        time1 = time.perf_counter()
        print(f' Processing for L = {L} ...')
        means = dict()
        ses = dict()
        generator = generate_params_BH_exp([L], params['m_s'], params['ratio_s'], params['mode_s'], params['methods'])
        time2 = time.perf_counter()
        for (_, m, r, mode, method) in tqdm(list(generator)):
            m_0 = int(np.rint(m*float(r)).astype('int'))
            filename = generate_filename_BH_exp(L, m_0, m, mode, params['num_rep'], method, params['criterion'])
            test_result = np.array(np.load(f'{RAW_OUTPUT_DIR}/{filename}', allow_pickle=True))
            mean, se = mean_and_se(test_result)
            means.setdefault(r, dict()).setdefault(mode, dict()).setdefault(method, []).append(mean)
            ses.setdefault(r, dict()).setdefault(mode, dict()).setdefault(method, []).append(se)
        time3 = time.perf_counter()
        jsonname_means, jsonname_ses = generate_jsonname_BH_exp(L)
        with open(f'{PROCESSED_OUTPUT_DIR}/{jsonname_means}', 'w') as f_mean:
            json.dump(means, f_mean, indent=4)
        with open(f'{PROCESSED_OUTPUT_DIR}/{jsonname_ses}', 'w') as f_se:
            json.dump(ses, f_se, indent=4)
        time4 = time.perf_counter()
        time_setup += time2-time1
        time_process += time3-time2
        time_save += time4-time3
    return [['Set ups', time_setup], ['Process data', time_process], ['Save data', time_save]]

if __name__ == '__main__':
    main_analyze()
