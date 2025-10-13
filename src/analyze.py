import math
import numpy as np
from utils import mean_and_se, generate_filename_BH_exp, generate_filename_BH_exp
from tqdm import tqdm

if __name__ == '__main__':
    L_s = [5., 10.]
    m_s = [4, 8, 16, 32, 64]
    ratio_s = [0., 0.25, 0.5, 0.75]
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
    generator = generate_params_BH_exp(L_s, m_s, rato_s, mode_s, methods)
    for (L, m, r, mode, method) in tqdm(list(generator)):
        m_0 = int(np.rint(m*r).astype('int'))
        filename = generate_filename_BH_exp(L, m_0, m, mode, num_rep, method, criterion)
        test_result = np.load('results/raw/'+filename)
        mean, se = mean_and_se(test_result)