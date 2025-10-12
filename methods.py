import math
import numpy as np

class MultipleHypotheses:
    '''
    Base multiple hypothesis class
    '''
    def __init__(self, num_hypo=1, num_nul=1):
        assert num_hypo >= num_null, \
            "Number of null hypotheses cannot surpass number of hypotheses"
        self.num_hypo = num_hypo
        self.num_null = num_null
        self.num_alt  = num_hypo - num_null

    def generate_data(self, size=None):
        raise NotImplementedError

    def generate_p_values(sefl, test):
        return test(self.generate_data())

class StandardNullHypotheses(MultipleHypotheses):
    '''
    Simple uniform hypothesis family
    Generated data can also be thought of as p values under the null
    '''
    def __init__(self, num_hypo=1):
        super().__init__(self, num_hypo=num_hypo, num_null=0)
        
    def generate_data(self, size=None)
        if shape == None: return np.random.uniform(self.num_hypo)
        else: return np.random.uniform(size = (size, self.num_hypo))

class NormalMeanHypotheses(MultipleHypotheses):
    '''
    Similar-variance 1D Normal distribution hypotheses
    The null indicates that the mean is 0
    '''
    def __init__(self, num_null, alt_means, sigma=1.):
        num_hypo = num_null + len(alt_means)
        super().__init__(num_hypo, num_null)
        self.means = np.array([0.]*num_null+list(alt_means))
        self.sigma = sigma

    def generate_data(self, size=None):
        if shape == None: return np.random.normal(self.means, self.sigma)
        else: return np.random.normal(self.means, shape=(size, self.num_hypo))


class MutiTest():
    '''
    Class of multiple testing rejection methods for FWER and FDR control
    '''
    @staticmethod
    def BonferroniMethod(p_values, alpha, m=None):
        if m == None: m = p_values.shape(-1)
        rejection = (p_values > (alpha/m)).astype('int')

    @staticmethod
    def HochbergMethod(p_values, alpha):
        m = p_values.shape(-1)
        pass

    @staticmethod
    def BHMethod(p_values, alpha):
        pass

    @staticmethod
    def _HochbergSimple(p_values, alpha):
        pass

    @staticmethod
    def _BHSimple(p_values, alpha):
        m = p_values.shape(-1)
        pass