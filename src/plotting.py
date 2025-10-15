import math
import numpy as np
import matplotlib.pyplot as plt

from utils import generate_jsonname_BH_exp

if __name__ == '__main__':
    L_s = [5.0, 10.0]
    m_s = [4, 8, 16, 32, 64]
    ratio_s = ['0.00', '0.25', '0.50', '0.75']
    mode_s = ['D', 'E', 'I']
    methods = ['Bonferroni', 'Hochberg', 'BH']
    criterion = 'power'
    alpha = 0.05
    print('=============== Begin plotting ===============')
    print(' L_s: ', L_s)
    print(' m_s: ', m_s)
    print(' ratio_s: ', ratio_s)
    print(' num_rep: ', num_rep)
    print(' methods: ', methods)
    print(f' criterion: {criterion}')
    print(f' alpha: {alpha}')
    print('==============================================')
