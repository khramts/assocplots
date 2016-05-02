import matplotlib.pyplot as plt
import numpy as np
from scipy.stats.mstats import mquantiles
from scipy.stats import binom
from scipy.stats import norm
from scipy.stats import linregress
from scipy.stats import chi2

def get_lambda(p, definition = 'median'):
    '''
    Evaluates Lambda value
    :param p: distribution of p-values
    :param definition: definition of lambda
    :return:
    '''
    if definition == 'median':
        pm = np.median(p)
        Chi = chi2.ppf(1. - pm, 1)
        return Chi / chi2.ppf(0.5,1)
    else:
        raise Exception("Only 'median' definition of lambda is implemented at this moment.")

def qqplot(data, labels, n_quantiles=100, alpha=0.95, error_type='theoretical', distribution = 'binomial', log10conv=True, color=['k', 'r', 'b'], fill_dens=[0.1, 0.1, 0.1], type = 'uniform', title='title'):
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
    xmax = 0
    ymax = 0
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
            if np.sum(alpha) > 0:
                for i in range(0, len(q_pos)):
                    if distribution == 'binomial':
                        q_err[i, :] = binom.interval(alpha=alpha, n=len(data[j]), p=q_pos[i])
                    elif distribution == 'normal':
                        q_err[i, :] = norm.interval(alpha, len(data[j])*q_pos[i], np.sqrt(len(data[j])*q_pos[i]*(1.-q_pos[i])))
                        q_err[i, q_err[i, :] < 0] = 1e-12
                    else:
                        print('Distribution is not defined!')
                q_err /= 1.0*len(data[j])
                for i in range(0, 100):
                    q_err[i,:] += 1e-12
            # print(q_err[100:, :])
            slope, intercept, r_value, p_value, std_err = linregress(q_th, q_data)
            # print(labels[j], ' -- Slope: ', slope, " R-squared:", r_value**2)
            plt.plot(-np.log10(q_th[n_quantiles-1:]), -np.log10(q_data[n_quantiles-1:]), '-', color=color[j])
            plt.plot(-np.log10(q_th[:n_quantiles]), -np.log10(q_data[:n_quantiles]), '.', color=color[j], label=labels[j])
            xmax = np.max([xmax, - np.log10(q_th[1])])
            ymax = np.max([ymax, - np.log10(q_data[0])])
            # print(- np.log10(q_th[:]))
            if np.sum(alpha)>0:
                if error_type=='experimental':
                    plt.fill_between(-np.log10(q_th), -np.log10(q_data/q_th*q_err[:,0]), -np.log10(q_data/q_th*q_err[:,1]), color=color[j], alpha=fill_dens[j], label='%1.3f CI'%alpha)
        if np.sum(alpha)>0:
            if error_type=='theoretical':
                plt.fill_between(-np.log10(q_th), -np.log10(q_err[:,0]), -np.log10(q_err[:,1]), color=color[j], alpha=fill_dens[j], label='%1.3f CI'%alpha)
    plt.legend(loc=4)
    plt.xlabel('Theoretical -log10')
    plt.ylabel('Experimental -log10')
    plt.plot([0, 100], [0, 100],'--k')
    # print(xmax,ymax)
    plt.xlim([0, np.ceil(xmax)])
    plt.ylim([0, np.ceil(ymax*1.05)])
    plt.title(title)
    plt.tight_layout()
    # return q_data, q_th, q_err
