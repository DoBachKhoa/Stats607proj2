import math
import numpy as np
import json
from utils import mean_and_se, generate_params_BH_exp, \
                  generate_filename_BH_exp, generate_jsonname_BH_exp
from tqdm import tqdm

if __name__ == '__main__':
    L_s = [5., 10.]
    m_s = [4, 8, 16, 32, 64]
    ratio_s = ['0.00', '0.25', '0.50', '0.75']
    num_rep = 2000
    mode_s = ['D', 'E', 'I']
    methods = ['Bonferroni', 'Hochberg', 'BH']
    criterion = 'power'
    alpha = 0.05
    print('=============== Begin raw output summary ===============')
    print(' L_s: ', L_s)
    print(' m_s: ', m_s)
    print(' ratio_s: ', ratio_s)
    print(' num_rep: ', num_rep)
    print(' methods: ', methods)
    print(f' criterion: {criterion}')
    print(f' alpha: {alpha}')
    print('=======================================================')
    for L in L_s:
        print(f' Processing for L = {L} ...')
        means = dict()
        ses = dict()
        generator = generate_params_BH_exp([L], m_s, ratio_s, mode_s, methods)
        for (_, m, r, mode, method) in tqdm(list(generator)):
            m_0 = int(np.rint(m*float(r)).astype('int'))
            filename = generate_filename_BH_exp(L, m_0, m, mode, num_rep, method, criterion)
            test_result = np.array(np.load('results/raw/'+filename, allow_pickle=True))
            mean, se = mean_and_se(test_result)
            means.setdefault(r, dict()).setdefault(mode, dict()).setdefault(method, []).append(mean)
            ses.setdefault(r, dict()).setdefault(mode, dict()).setdefault(method, []).append(se)
        jsonname_means, jsonname_ses = generate_jsonname_BH_exp(L)
        with open('results/processed/'+jsonname_means, 'w') as f_mean:
            json.dump(means, f_mean, indent=4)
        with open('results/processed/'+jsonname_ses, 'w') as f_se:
            json.dump(ses, f_se, indent=4)
