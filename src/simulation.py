import math
import numpy as np
from scipy.stats import norm
from methods import NormalMeanHypotheses, MultiTest
from utils import testing_result, distribute_means_BH_exp, generate_filename
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
    p_values = generator.generate_p_values(norm.cdf, size=num_rep)

    # Run hypothesis test
    control_method = dict_methods[method]
    decision = control_method(p_values, alpha)
    ground_truth = np.array([0]*m_0+[1]*(m-m_0))
    # print(ground_truth, ground_truth.shape, decision.shape, L, m_0, m, mode, ' AAA')
    result = testing_result(ground_truth, decision)
    
    # Save in csv
    if saving:
        filename = generate_filename(L, m_0, m, mode, num_rep, method, criterion)
        np.save('results/raw/'+filename, result)
    return result

if __name__ == '__main__':
    L_s = [5., 10.]
    m_s = [4, 8, 16, 32, 64]
    ratio_s = [0., 0.25, 0.5, 0.75]
    num_rep = 2000
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
    def generate_params():
        for L in L_s:
            for m in m_s:
                for r in ratio_s:
                    for mode in ['I', 'D', 'E']:
                        for method in methods:
                            yield (L, m, r, mode, method)
    for (L, m, r, mode, method) in tqdm(list(generate_params())):
        m_0 = int(np.rint(m*r).astype('int'))
        simulate_BH_exp(L, m_0, m, mode, num_rep, method, criterion, alpha=alpha, saving=True)
