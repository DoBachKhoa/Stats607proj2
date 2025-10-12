import math
import numpy as np

def testing_result(true_result, test_result, criteria=('power')):
    output = dict()
    m = len(true_result)
    m_0 = m - np.sum(true_result)
    R = np.sum(test_result)
    S = np.sum(test_result & true_result)
    T = m - m_0 - S
    U = m - R - T
    V = R - S
    if 'power' in criteria: output['power'] = S/R
    if 'type1' in criteria: output['type1'] = V
    if 'type2' in criteria: output['type2'] = T
    if 'fdr' in criteria: output['fdr'] = V/R
    if 'm_0' in criteria: output[]'m_0'] = m_0
    if 'm' in criteria: output['m'] = m
    return output

def _distribute_mean_E(m_1, L):
    '''
    Distributes alternative hypotheses mean for BH paper's experiment
    under configuration E (Equal)
    '''
    d, r = divmod(m_1, 4)
    output = [[L/4, d], [L/2, d], [3*L/4, d], [L, d]]
    for i in range(r): output[i][1] += 1

def _distribute_mean_I(m_1, L, mode):
    '''
    Distributes alternative hypotheses mean for BH paper's experiment
    under configuration I (linear Increasing)
    '''
    d, r = divmod(m_1, 10)
    output = [[L/4, d], [L/2, 2*d], [3*L/4, 3*d], [L, 4*d]]
    if r > 0: output[3][1] += 1
    if r > 1: output[2][1] += 1
    if r > 2: output[1][1] += 1
    if r > 3: output[0][1] += 1
    if r > 4: output[3][1] += 1
    if r > 5: output[2][1] += 1
    if r > 6: output[1][1] += 1
    if r > 7: output[3][1] += 1
    if r > 8: output[2][1] += 1
    return output

def _distribute_mean_D(m_1, L, mode):
    '''
    Distributes alternative hypotheses mean for BH paper's experiment
    under configuration D (linear Decreasing)
    '''
    d, r = divmod(m_1, 10)
    output = [[L/4, 4*d], [L/2, 3**d], [3*L/4, 2*d], [L, d]]
    if r > 0: output[0][1] += 1
    if r > 1: output[1][1] += 1
    if r > 2: output[2][1] += 1
    if r > 3: output[3][1] += 1
    if r > 4: output[0][1] += 1
    if r > 5: output[1][1] += 1
    if r > 6: output[2][1] += 1
    if r > 7: output[0][1] += 1
    if r > 8: output[1][1] += 1
    return output

def distributte_mean_BH_exp(m_1, L, mode):
    '''
    Distributes alternative hypotheses mean for BH paper's experiment
    '''
    configs = ('E': _distribute_mean_E, 'I': _distribute_mean_I, 'D': _distribute_mean_D)
    temp = configs[mode](m_1, L)
    output = []
    for val, num in temp:
        for _ in range(num):
            output.append(val)
    return output
