import math
import json
import numpy as np
import matplotlib.pyplot as plt

from utils import generate_jsonname_BH_exp, generate_plotname_BH_exp

def plot_BH_exp(results, ratio_s, mode_s, m_s, method_s, filename, 
                plotname, rownames, colnames, 
                patterns=None, colors=None, xticks=None, yticks=None):
    m = len(ratio_s)
    n = len(mode_s)
    _, axes = plt.subplots(m, n, figsize=(3*n+0.25, 3*m+0.25))
    for i, ratio in enumerate(ratio_s):
        for j, mode in enumerate(mode_s):
            for method in method_s:
                length = len(results[ratio][mode][method])
                features = dict()
                if patterns: features['linestyle']=patterns[method]
                if colors: features['color']=colors[method]
                axes[i][j].plot(results[ratio][mode][method], label=method, linewidth=3, **features)
                if xticks is not None:
                    if i != m-1: axes[i][j].set_xticks([])
                    else: axes[i][j].set_xticks(list(range(length)), xticks)
                if yticks is not None:
                    if j != 0: axes[i][j].set_yticks([])
                    else: axes[i][j].set_yticks(yticks)
    axes[0][0].legend()
    if plotname: plt.suptitle(plotname, fontweight='bold')
    if rownames:
        for ind, name in enumerate(rownames):
            axes[ind][0].set_ylabel(name)
    if colnames:
        for ind, name in enumerate(colnames):
            axes[-1][ind].set_xlabel(name)
    plt.tight_layout()
    plt.savefig(filename, bbox_inches='tight')

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
    print(' methods: ', methods)
    print(f' criterion: {criterion}')
    print(f' alpha: {alpha}')
    print('==============================================')
    colors = ['#1E3888', '#47A8BD', '#F5E663', '#FFAD69', '#A52422']
    for L in L_s:
        jsonname_means, jsonname_ses = generate_jsonname_BH_exp(L)
        plotname_means, plotname_ses = generate_plotname_BH_exp(L)
        with open('results/processed/'+jsonname_means, 'r') as file:
            means = json.load(file)
            plot_BH_exp(means, ratio_s, mode_s, m_s, methods, 'results/plots'+plotname_means,  
                        plotname ='Plot of Power as a function of number of hypotheses', 
                        rownames =['0% null', '25% null', '50% null', '75% null'],
                        colnames =['Config D', 'Config E', 'Config I'],
                        patterns = {'Bonferroni' : ':', 'Hochberg': '--', 'BH': '-'},
                        colors = {'Bonferroni' : '#A52422', 'Hochberg': '#F5E663', 'BH': '#47A8BD'},
                        xticks =[4, 8, 16, 32, 64], yticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0])
        with open('results/processed/'+jsonname_ses, 'r') as file:
            ses = json.load(file)
            plot_BH_exp(ses, ratio_s, mode_s, m_s, methods, 'results/plots'+plotname_ses, 
                        plotname='Plot of Power SE', rownames=None, colnames=None)
