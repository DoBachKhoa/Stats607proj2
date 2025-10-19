import math
import numpy as np

class MultipleHypotheses:
    '''
    Base multiple hypothesis class
    '''
    def __init__(self, num_hypo=1, num_null=1, rng=None):
        assert num_hypo >= num_null, \
            "Number of null hypotheses cannot surpass number of hypotheses"
        self.num_hypo = num_hypo
        self.num_null = num_null
        self.num_alt  = num_hypo - num_null
        if rng is not None: self.rng = rng
        else: self.rng = np.random.default_rng()

    def generate_data(self, size=None):
        raise NotImplementedError

    def generate_p_values(self, test, size=None):
        return test(self.generate_data(size=size))

class StandardNullHypotheses(MultipleHypotheses):
    '''
    Simple uniform hypothesis family
    Generated data can also be thought of as p values under the null
    '''
    def __init__(self, num_hypo=1, rng=None):
        super().__init__(self, num_hypo=num_hypo, num_null=0, rng=rng)
        
    def generate_data(self, size=None):
        if size == None: return self.rng.uniform(0, 1, self.num_hypo)
        else: return self.rng.uniform(0, 1, size = (size, self.num_hypo))

class NormalMeanHypotheses(MultipleHypotheses):
    '''
    Similar-variance 1D Normal distribution hypotheses
    The null indicates that the mean is 0
    '''
    def __init__(self, num_null, alt_means, sigma=1., rng=None):
        num_hypo = num_null + len(alt_means)
        super().__init__(num_hypo, num_null, rng = rng)
        self.means = np.array([0.]*num_null+list(alt_means))
        self.sigma = sigma

    def generate_data(self, size=None):
        if size == None: return self.rng.normal(self.means, self.sigma, size=self.num_hypo)
        else: return self.rng.normal(self.means, self.sigma, size=(size, self.num_hypo))


class MultiTest():
    '''
    Class of multiple testing rejection methods for FWER and FDR control
    '''
    @staticmethod
    def BonferroniMethod(p_values, alpha, m=None):
        if m == None: m = p_values.shape[-1]
        return (p_values <= (alpha/m)).astype('int')

    @staticmethod
    def _HochbergSimple(p_values, alpha):
        m = len(p_values)
        ordered_p_values = list(enumerate(list(p_values)))
        ordered_p_values.sort(key = lambda x: x[1])
        output = np.repeat(0, m).astype('int')
        for i in range(m-1, -1, -1):
            if ordered_p_values[i][1] <= alpha/(m-i):
                for j in range(i+1): output[ordered_p_values[j][0]] = 1
                return output
        return output

    @staticmethod
    def _BHSimple(p_values, alpha):
        m = len(p_values)
        ordered_p_values = list(enumerate(list(p_values)))
        ordered_p_values.sort(key = lambda x: x[1])
        output = np.repeat(0, m).astype('int')
        for i in range(m, 0, -1):
            if ordered_p_values[i-1][1] <= alpha*i/m:
                for j in range(i): output[ordered_p_values[j][0]] = 1
                return output
        return output

    @staticmethod
    def _applyMultipleTimes(p_values, alpha, method):
        if len(p_values.shape) == 1: return method(p_values, alpha)
        else: return np.array([method(case, alpha) for case in p_values])

    @staticmethod
    def HochbergMethod(p_values, alpha):
        return MultiTest._applyMultipleTimes(p_values, alpha, MultiTest._HochbergSimple)

    @staticmethod
    def BHMethod(p_values, alpha):
        return MultiTest._applyMultipleTimes(p_values, alpha, MultiTest._BHSimple)