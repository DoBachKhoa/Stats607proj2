import math
import numpy as np

def divide_0div0(numerator, denominator, alt_value=0):
    '''
    Performs element-wise division where 0/0 is treated as alt_value.
    '''
    result = np.zeros_like(numerator, dtype=float)
    non_zero_denominator_mask = (denominator != 0)
    result[non_zero_denominator_mask] = numerator[non_zero_denominator_mask] / denominator[non_zero_denominator_mask]
    zero_divide_zero_mask = (numerator == 0) & (denominator == 0)
    result[zero_divide_zero_mask] = alt_value
    return result

def testing_measure(true_result, test_result, criteria=('power')):
    '''
    Matches the ground truth which is a 1d array of 1's and 0's
    indicating not null and null hypotheses
    with rows of test result
    each row is 1 for rejection and 0 for not rejecting
    supported criteria are: 'power', 'type1', 'type2', 'fdr', 'm', 'm_0'
    'm' for the number of ground truth hypotheses
    'm_0' for the number of groud truth null hypotheses
    true_result is 1d, test_result could be 1d or 2d; the row length must be the same
    '''
    output = dict()
    m = true_result.shape[0]
    m_0 = m - np.sum(true_result, axis=-1)
    R = np.sum(test_result, axis=-1)
    S = np.sum(test_result & true_result, axis=-1)
    T = m - m_0 - S
    U = m - R - T
    V = R - S
    if 'power' in criteria:
        assert m_0 < m, 'No non-null hypothesis, cannot calculate power'
        output['power'] = S / (m-m_0)
    if 'type1' in criteria: output['type1'] = V
    if 'type2' in criteria: output['type2'] = T
    if 'fdr' in criteria: output['fdr'] = divide_0div0(V, R, 0)
    if 'm_0' in criteria: output['m_0'] = m_0
    if 'm' in criteria: output['m'] = m
    return output

def _distribute_mean_E(m_1, L):
    '''
    Distributes alternative hypotheses mean for BH paper's experiment
    under configuration E (Equal)
    '''
    d, r = divmod(m_1, 4)
    output = [[L/4, d], [L/2, d], [3*L/4, d], [L, d]]
    for i in range(r): output[-i-1][1] += 1
    return output

def _distribute_mean_I(m_1, L):
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

def _distribute_mean_D(m_1, L):
    '''
    Distributes alternative hypotheses mean for BH paper's experiment
    under configuration D (linear Decreasing)
    '''
    d, r = divmod(m_1, 10)
    output = [[L/4, 4*d], [L/2, 3*d], [3*L/4, 2*d], [L, d]]
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

def mean_and_se(nums):
    '''
    Return the mean and empirical se of number in nums
    '''
    assert len(nums.shape) == 1, 'Input has dimension not equal 1'
    l = len(nums)
    mean = nums.sum()/l
    std = np.sqrt(np.sum((nums-mean)*(nums-mean))/(l-1))
    se = std/np.sqrt(l)
    return mean, se

def distribute_means_BH_exp(m_1, L, mode):
    '''
    Distributes alternative hypotheses mean for BH paper's experiment
    '''
    configs = {'E': _distribute_mean_E, 'I': _distribute_mean_I, 'D': _distribute_mean_D}
    temp = configs[mode](m_1, L)
    # print(m_1, L, mode, temp)
    output = []
    for val, num in temp:
        for _ in range(num):
            output.append(val)
    return output

def generate_filename_BH_exp(L, m_0, m, mode, num_rep, method, criterion):
    L = np.round(float(L), 1)
    return f'exp_output_L{L}_mo{m_0}_m{m}_mode{mode}_nrep{num_rep}_method{method}_criterion{criterion}.npy'

def generate_jsonname_BH_exp(L):
    return f'exp_proceeded_output_means_L{L}.json', f'exp_proceeded_output_ses_L{L}.json'

def generate_plotname_BH_exp(L):
    return f'exp_plot_means_L{L}.png', f'exp_plot_ses_L{L}.png'

def generate_params_BH_exp(L_s, m_s, ratio_s, mode_s, method_s):
    for L in L_s:
        for r in ratio_s:
            for mode in mode_s:
                for method in method_s:
                    for m in m_s: # Intentionally put m last to help parsing
                        yield (L, m, r, mode, method)
