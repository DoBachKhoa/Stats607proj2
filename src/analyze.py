import os
import math
import json
import numpy as np
from tqdm import tqdm
from src.utils import mean_and_se, generate_params_BH_exp, \
                      generate_filename_BH_exp, generate_jsonname_BH_exp
from src.constants import RAW_OUTPUT_DIR, PROCESSED_OUTPUT_DIR

if __name__ == '__main__':
    os.makedirs(PROCESSED_OUTPUT_DIR, exist_ok=True)
    with open('params.json', 'r') as file:
        params = json.load(file)
    print('=============== Begin raw output summary ===============')
    print(' L_s: ', params['L_s'])
    print(' m_s: ', params['m_s'])
    print(' ratio_s: ', params['ratio_s'])
    print(' num_rep: ', params['num_rep'])
    print(' methods: ', params['methods'])
    print(f" criterion: {params['criterion']}")
    print(f" alpha: {params['alpha']}")
    print('=======================================================')
    for L in params['L_s']:
        print(f' Processing for L = {L} ...')
        means = dict()
        ses = dict()
        generator = generate_params_BH_exp([L], params['m_s'], params['ratio_s'], params['mode_s'], params['methods'])
        for (_, m, r, mode, method) in tqdm(list(generator)):
            m_0 = int(np.rint(m*float(r)).astype('int'))
            filename = generate_filename_BH_exp(L, m_0, m, mode, params['num_rep'], method, params['criterion'])
            test_result = np.array(np.load(RAW_OUTPUT_DIR+filename, allow_pickle=True))
            mean, se = mean_and_se(test_result)
            means.setdefault(r, dict()).setdefault(mode, dict()).setdefault(method, []).append(mean)
            ses.setdefault(r, dict()).setdefault(mode, dict()).setdefault(method, []).append(se)
        jsonname_means, jsonname_ses = generate_jsonname_BH_exp(L)
        with open(PROCESSED_OUTPUT_DIR+jsonname_means, 'w') as f_mean:
            json.dump(means, f_mean, indent=4)
        with open(PROCESSED_OUTPUT_DIR+jsonname_ses, 'w') as f_se:
            json.dump(ses, f_se, indent=4)
