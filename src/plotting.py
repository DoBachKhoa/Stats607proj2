import math
import json
import numpy as np
import matplotlib.pyplot as plt
from utils import generate_jsonname_BH_exp, generate_plotname_BH_exp

def plot_BH_exp(results, ratio_s, mode_s, m_s, method_s, 
                filename, plotname, rownames, colnames, 
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
    plt.close()

def plot_BH_exp_ses_hist(results, ratio_s, mode_s, m_s, method_s,
                         filename='histogram.png', plotname=None, colors=None, transparency=0.5, bins=20):
    # Load data from dictionary `results`
    m = len(ratio_s)
    n = len(mode_s)
    output = dict()
    for ratio in ratio_s:
        for mode in mode_s:
            for method in method_s:
                for num in results[ratio][mode][method]:
                    output.setdefault(method, []).append(num)
                
    # Handling bin positionings
    left_limit = np.min([np.min(l) for l in output.values()])-1e-6
    right_limit = np.max([np.max(l) for l in output.values()])+1e-6
    offset = (right_limit-left_limit)/bins/2./len(method_s)

    # Plotting
    for i, method in enumerate(method_s):
        bin_positions = np.linspace(left_limit-i*offset, right_limit+(len(method_s)-1-i)*offset, bins+1)
        # print(bin_positions, offset)
        if colors: plt.hist(output[method], label=method, alpha=transparency, color=colors[method], bins=bin_positions)
        else: plt.hist(output[method], label=method, alpha=transparency)
    if plotname: plt.title(plotname)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(filename)
    plt.close()

if __name__ == '__main__':
    with open('params.json', 'r') as file:
        params = json.load(file)
    print('=============== Begin plotting ===============')
    print(' L_s: ', params['L_s'])
    print(' m_s: ', params['m_s'])
    print(' ratio_s: ', params['ratio_s'])
    print(' methods: ', params['methods'])
    print(' configs: ', params['mode_s'])
    print(f" criterion: {params['criterion']}")
    print(f" alpha: {params['alpha']}")
    print('==============================================')
    colors = ['#1E3888', '#47A8BD', '#F5E663', '#FFAD69', '#A52422']
    for L in params['L_s']:
        jsonname_means, jsonname_ses = generate_jsonname_BH_exp(L)
        plotname_means, plotname_ses = generate_plotname_BH_exp(L, pdf=True)
        with open('results/processed/'+jsonname_means, 'r') as file:
            means = json.load(file)
            plot_BH_exp(means, params['ratio_s'], params['mode_s'], params['m_s'], params['methods'], 
                        filename = 'results/plots'+plotname_means,  
                        plotname = 'Plot of Power as a function of number of hypotheses', 
                        rownames = [str(np.round(float(ratio)*100, 1))+'% null' for ratio in params['ratio_s']],
                        colnames = ['Config '+config for config in params['mode_s']],
                        patterns = {'Bonferroni' : ':', 'Hochberg': '--', 'BH': '-'},
                        colors = {'Bonferroni' : '#A52422', 'Hochberg': '#F5E663', 'BH': '#47A8BD'},
                        xticks = params['m_s'], yticks = [0, 0.2, 0.4, 0.6, 0.8, 1.0])
        with open('results/processed/'+jsonname_ses, 'r') as file:
            ses = json.load(file)
            plot_BH_exp_ses_hist(ses, params['ratio_s'], params['mode_s'], params['m_s'], params['methods'],
                                 filename='results/plots'+plotname_ses, plotname='Histogram of se',
                                 colors = {'Bonferroni' : '#A52422', 'Hochberg': '#F5E663', 'BH': '#47A8BD'},
                                 transparency=0.5, bins=20)
            # plot_BH_exp(ses, params['ratio_s'], params['mode_s'], params['m_s'], params['methods'],
            #             'results/plots'+plotname_ses, plotname='Plot of Power SE', rownames=None, colnames=None)
