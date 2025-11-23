import pytest
import random
import numpy as np
from methods import MultiTest
from src.utils import divide_0div0, compare_reject_result

# Import implemented functions

'''
Test functionality correctness for `methods.py` and `utils.py`
'''

class TestMethodologyFunctionCorrectness:
    '''
    Class of functions that test correctness of
    functions in `methods.py`
    '''
    def test_Bonferroni(self):
        ''' Test correctness of Bonferroni implementation '''
        p_values = np.array([0.1, 0.2, 0.001, 0.001, 0.3, 0.1, 0.5, 0.005, 0.01])
        n = len(p_values)
        for alpha in (0.05, 0.1, 0.2):
            expected_output = (p_values <= alpha/n).astype('int')
            assert (expected_output == MultiTest.BonferroniMethod(p_values, alpha, m=None)).all(), \
                   'Bonferroni method gives unexpected output'
            assert (expected_output == MultiTest.BonferroniMethod(p_values, alpha, m=n)).all(), \
                   'Bonferroni method gives unexpected output'

    def test_trivial(self):
        ''' Test MultiTest methods with trivial p values of 0. and 1. '''
        m_0 = 20
        m_1 = 20
        easy_p_values = np.array([0]*m_0+[1]*m_1, dtype='float') # Super convenient p values
        random.shuffle(easy_p_values)
        for method in [MultiTest.BonferroniMethod, MultiTest.BHMethod, MultiTest.HochbergMethod]:
            for alpha in [0.01, 0.05, 0.1, 0.2, 0.5, 0.9]:
                output = method(easy_p_values, alpha)
                assert (np.abs(output+easy_p_values-1.) < 1e-9).all(), \
                       f'Method {method.__name__} with alpha {alpha} gives unexpected results.'

    def test_sorted(self):
        ''' Test Multitest methods with sorted p values. '''
        m_0 = 20
        m_1 = 20
        sorted_p_values = np.array([0.001, 0.001, 0.002, 0.002, 0.01, 0.01, 0.05, 0.1, 0.2]) # Sorted p values
        for method in [MultiTest.BonferroniMethod, MultiTest.BHMethod, MultiTest.HochbergMethod]:
            for alpha in [0.01, 0.05, 0.1, 0.2, 0.5, 0.9]:
                output = method(sorted_p_values, alpha)
                output_sorted = np.sort(output)[::-1]
                assert (np.abs(output-output_sorted) < 1e-9).all(), \
                       f'Method {method.__name__} with alpha {alpha} gives unexpected result.'

class TestUtilFunctionCorrectness:
    '''
    Class of functions that test correctness of
    functions in `utils.py`
    '''
    def test_matching(self):
        '''
        Test function `testing_measure`
        that matches the ground truth and the rejection output
        of a testing method.
        '''
        ground_truth     = np.array([1, 1, 0, 0, 1, 0, 0, 1], dtype='int')
        rejection_result = np.array([1, 0, 1, 0, 0, 0, 1, 1], dtype='int')
        result = compare_reject_result(ground_truth, rejection_result, criteria=('power', 'type1', 'type2', 'fdr'))
        assert abs(result['power']-0.5) < 1e-9, f"Power should be 0.5, but got {result['power']}"
        assert abs(result['type1']-2) < 1e-9, f"Type1 should be 0.5, but got {result['type1']}"
        assert abs(result['type2']-2) < 1e-9, f"Type2 should be 0.5, but got {result['type2']}"
        assert abs(result['fdr']-0.5) < 1e-9, f"fdr should be 0.5, but got {result['fdr']}"

    def test_matching_2(self):
        '''
        Test function `testing_measure`
        that matches the ground truth and the rejection output
        of a testing method
        in the case of 2 dimensional rejection result
        '''
        ground_truth     = np.array( [1, 1, 0, 0, 1, 0, 0, 1], dtype='int')
        rejection_result = np.array([[1, 0, 1, 0, 0, 0, 1, 1],
                                     [1, 1, 0, 0, 0, 1, 1, 0],
                                     [0, 0, 1, 1, 0, 1, 1, 0],
                                     [1, 1, 0, 0, 1, 0, 0, 1]], dtype='int')
        result = compare_reject_result(ground_truth, rejection_result, criteria=('power', 'type1', 'type2', 'fdr'))
        expected_result = dict()
        expected_result['power'] = np.array([0.5, 0.5, 0., 1.])
        expected_result['type1'] = np.array([2, 2, 4, 0])
        expected_result['type2'] = np.array([2, 2, 4, 0])
        expected_result['fdr'] = np.array([0.5, 0.5, 1, 0])
        for criterion in ('power', 'type1', 'type2', 'fdr'):
            assert (abs(result[criterion]-expected_result[criterion]) < 1e-9).all(), \
                   f'{criterion} should be {expected_result[criterion]}, but got {result[criterion]}'

    def test_0div0(self):
        '''Tests the function `divide_0div0`'''
        numerator = np.array([1, 2, 3, 4, 0, 0, 0, 0], dtype='int')
        denominator = np.array([2, 4, 1, 2, 0, 0, 1, 2], dtype='int')
        expected_output_1 = np.array([0.5, 0.5, 3., 2., 1., 1., 0., 0.])
        expected_output_0 = np.array([0.5, 0.5, 3., 2., 0., 0., 0., 0.])
        output_1 = divide_0div0(numerator, denominator, alt_value=1.)
        output_0 = divide_0div0(numerator, denominator, alt_value=0.)
        assert (abs(output_1-expected_output_1) < 1e-9).all(), '0div0 function not consistent with alt. value 1.'
        assert (abs(output_0-expected_output_0) < 1e-9).all(), '0div0 function not consistent with alt. value 0.'
