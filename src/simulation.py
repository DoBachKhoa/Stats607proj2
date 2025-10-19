import math
import numpy as np
from scipy.stats import norm
from methods import NormalMeanHypotheses, MultiTest
from utils import compare_reject_result, distribute_means_BH_exp, \
                  generate_filename_BH_exp, generate_params_BH_exp
from tqdm import tqdm

dict_methods = {
    'Bonferroni': MultiTest.BonferroniMethod,
    'Hochberg': MultiTest.HochbergMethod,
    'BH':MultiTest.BHMethod
}

def simulate_BH_exp(L, m_0, m, mode, num_rep, method, criterion, alpha=0.05, saving=True):
    
    # Generate data
    alt_means = distribute_means_BH_exp(m-m_0, L, mode)
    generator = NormalMeanHypotheses(m_0, alt_means, sigma=1.)
    test = lambda data: 1-2*np.abs(norm.cdf(data)-0.5)
    p_values = generator.generate_p_values(test, size=num_rep)

    # Run hypothesis test
    control_method = dict_methods[method]
    decision = control_method(p_values, alpha)
    ground_truth = np.array([0]*m_0+[1]*(m-m_0))
    # print(ground_truth, ground_truth.shape, decision.shape, L, m_0, m, mode, ' AAA')
    result = compare_reject_result(ground_truth, decision)
    
    # Save in csv
    if saving:
        filename = generate_filename_BH_exp(L, m_0, m, mode, num_rep, method, criterion)
        np.save('results/raw/'+filename, result[criterion])
    return result

if __name__ == '__main__':
    L_s = [5., 10.]
    m_s = [4, 8, 16, 32, 64]
    ratio_s = ['0.00', '0.25', '0.50', '0.75']
    num_rep = 2000
    mode_s = ['D', 'E', 'I']
    methods = ['Bonferroni', 'Hochberg', 'BH']
    criterion = 'power'
    alpha = 0.05
    print('=============== Begin simulation ===============')
    print(' L_s: ', L_s)
    print(' m_s: ', m_s)
    print(' ratio_s: ', ratio_s)
    print(' num_rep: ', num_rep)
    print(' methods: ', methods)
    print(f' criterion: {criterion}')
    print(f' alpha: {alpha}')
    print('================================================')
    generator = generate_params_BH_exp(L_s, m_s, ratio_s, mode_s, methods)
    for (L, m, r, mode, method) in tqdm(list(generator)):
        m_0 = int(np.rint(m*float(r)).astype('int'))
        simulate_BH_exp(L, m_0, m, mode, num_rep, method, criterion, alpha=alpha, saving=True)
