import matplotlib.pyplot as plt
import numpy as np
from scipy.stats.mstats import mquantiles
from scipy.stats import binom
from scipy.stats import linregress

def qqplot(data, labels, n_quantiles=100, alpha=0.95, error_type='theoretical', log10conv=True, color='k', type = 'uniform'):
    '''
    Function for plotting Quantile Quantile (QQ) plots with confidence interval (CI)
    :param data: NumPy 1D array with data
    :param labels:
    :param type: type of the plot
    :param n_quantiles: number of quntiles to plot
    :param alpha: confidence interval
    :param log10conv: conversion to -log10(p) for the figure
    :return: nothing
    '''
    if type == 'uniform':
        # we expect distribution from 0 to 1
        for j in range(len(data)):
            # define quantiles positions:
            q_pos = np.concatenate([np.arange(99.)/len(data[j]), np.logspace(-np.log10(len(data[j]))+2, 0, n_quantiles)])
            # define quantiles in data
            q_data = mquantiles(data[j], prob=q_pos, alphap=0, betap=1, limit=(0, 1)) # linear interpolation
            # define theoretical predictions
            q_th = q_pos.copy()
            # evaluate errors
            q_err = np.zeros([len(q_pos),2])
            if alpha>0:
                for i in range(0, n_quantiles):
                    q_err[i,:] = binom.interval(alpha=alpha, n=len(data[j]), p=q_pos[i])
                q_err /= 1.0*len(data[j])
                for i in range(0, 100):
                    q_err[i,:] += 1e-12
            slope, intercept, r_value, p_value, std_err = linregress(q_th, q_data)
            print(labels[j], ' -- Slope: ', slope, " R-squared:", r_value**2)
            plt.plot(-np.log10(q_th), -np.log10(q_data), '.', color=color[j], label=labels[j])
            if alpha>0:
                if error_type=='experimental':
                    plt.fill_between(-np.log10(q_th), -np.log10(q_data/q_th*q_err[:,0]), -np.log10(q_data/q_th*q_err[:,1]), color=color[j], alpha=0.1, label='%1.3f CI'%alpha)
        if alpha>0:
            if error_type=='theoretical':
                plt.fill_between(-np.log10(q_th), -np.log10(q_err[:,0]), -np.log10(q_err[:,1]), color='k', alpha=0.1, label='%1.3f CI'%alpha)
    plt.legend(loc=4)
    plt.xlabel('Theoretical -log10')
    plt.ylabel('Experimental -log10')
    plt.plot([0, 8], [0, 8],'--k')
    plt.xlim([0, 7])
    plt.ylim([0, 7])
    return q_data, q_th, q_err
