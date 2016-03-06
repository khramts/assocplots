import numpy as np

import numpy as np
import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.pyplot as plt

def manhattan(p1, pos1, chr1, label1, p2, pos2, chr2, label2, cut = 2, colors = ['k', '0.5']):
    '''
    Static Manhattan plot
    :param p1: p-values for the top panel
    :param pos1: positions
    :param chr1: chromosomes numbers
    :param label1: label
    :param p2: p-values for the bottom panel
    :param pos2: positions
    :param chr2: chromosomes numbers
    :param label2: label
    :param cut: lower cut (default 2)
    :param colors: sequence of colors (default: black/gray)
    :return:
    '''
    import matplotlib as mpl
    mpl.rcParams['axes.color_cycle'] = ['k', '0.5']
    shift=np.array([0.0])
    plt.clf()
    for i in range(1,23):
        plt.subplot(2,1,1)
        print(i)
        filt = chr1==i
        x = shift[-1]+pos1[filt]
        y = -np.log10(p1[filt])
        plt.plot(x[y>cut], y[y>cut], '.')
        plt.ylim([cut, 9])
        shift_f = np.max(x)

        plt.subplot(2,1,2)
        filt = chr2==i
        x = shift[-1]+pos2[filt]
        y = -np.log10(p2[filt])
        plt.plot(x[y>cut], y[y>cut], '.')
        plt.ylim([cut, 9])
        shift_m = np.max(x)
        shift = np.append(shift, np.max([shift_f, shift_m]))

        plt.subplot(2,1,1)
        plt.plot([shift[-1], shift[-1]], [0, 10], '-k', lw=0.5, color='lightgray')
        plt.xlim([0, shift[-1]])
        plt.subplot(2,1,2)
        plt.plot([shift[-1], shift[-1]], [0, 10], '-k', lw=0.5, color='lightgray')
        plt.xlim([0, shift[-1]])
        print(shift)


    shift = (shift[1:]+shift[:-1])/2.
    plt.subplot(2,1,1)
    plt.setp(plt.gca().get_xticklabels(), visible=False)
    plt.xticks(shift)
    plt.text(shift[12],8,label1,bbox=dict(boxstyle="round", fc="1.0"))

    plt.subplot(2,1,2)
    plt.gca().invert_yaxis()
    labels = np.arange(1,23).astype(str)
    labels[-2] = ''
    labels[-4] = ''
    labels[-6] = ''
    labels[-8] = ''
    labels[-10] = ''
    plt.xticks(shift, labels)
    plt.text(shift[12],8,label2,bbox=dict(boxstyle="round", fc="1.0"))
    plt.ylabel('                                                  -log10(p-value)')
    plt.xlabel('chromosome')
    # plt.tight_layout(hspace=0.001)
    plt.subplots_adjust(hspace=0.001)


def reduce_data(data, top_snps=1000):
    '''
    Function reduces data for interactive plot
    :param data: list of datasets
    :param top_snps: number of snps to include
    :return: combined table
    '''
