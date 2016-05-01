import numpy as np

import numpy as np
import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.pyplot as plt

def manhattan(p1, pos1, chr1, label1,
               p2=None, pos2=None, chr2=None, label2=None,
               type='single',
               chrs_plot=None, chrs_names=None,
               cut = 2,
               colors = ['k', '0.5'],
               title='Title',
               xlabel='chromosome',
               ylabel='-log10(p-value)',
               top1 = 0,
               top2 = 0,
               lines = [10, 15],
               lines_colors = ['g', 'r'],
               zoom = None):
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
    :param type: Can be 'single', 'double' or 'inverted'
    :param chrs_plot: list of chromosomes that should be plotted. If empty [] all chromosomes will be plotted
    :param cut: lower cut (default 2)
    :param colors: sequence of colors (default: black/gray)
    :param title: defines the title of the plot
    :param xlabel: defines the xlabel of the plot
    :param ylabel: defines the ylabel of the plot
    :param top: Defines the upper limit of the plot. If 0, it is detected automatically.
    :param lines: Horizontal lines to plot.
    :param lines_colors: Colors for the horizontal lines.
    :param zoom: [chromosome, position, range] Zooms into a region.
    :return:
    '''

    # Setting things up
    shift=np.array([0.0])
    plt.clf()

    # If chrs_plot is empty, we need to generate a list of chromosomes
    if chrs_plot is None:
        chrs_list = np.unique(chr1)
        chrs_list.sort()
    else:
        chrs_list = chrs_plot


    # If chrs_names is empty, we need to generate a list of names for chromosomes
    if chrs_names is None:
        chrs_names = [str(chrs_list[i])  for i in range(len(chrs_list))]

    plot_positions = False
    if len(chrs_list) == 1:
        plot_positions = True


    for ii, i in enumerate(chrs_list):
        if type != 'single':
            ax1 = plt.subplot(2,1,1)
        else:
            plt.subplot(1,1,1)
        print(i)
        filt = chr1==i
        x = shift[-1]+pos1[filt]
        y = -np.log10(p1[filt])
        plt.plot(x[y>cut], y[y>cut], '.', color=colors[ii % len(colors)])
        shift_f = np.max(x)

        if zoom is not None:
            if zoom[0] == i:
                zoom_shift = zoom[1] + shift[-1]

        if type != 'single':
            plt.subplot(2,1,2)#, sharex=ax1)
            filt = chr2==i
            x = shift[-1]+pos2[filt]
            y = -np.log10(p2[filt])
            plt.plot(x[y>cut], y[y>cut], '.', color=colors[ii % len(colors)])
            shift_m = np.max(x)
        else:
            shift_m = 0

        shift = np.append(shift, np.max([shift_f, shift_m]))

        if type != 'single':
            plt.subplot(2,1,1)
        else:
            plt.subplot(1,1,1)
        plt.plot([shift[-1], shift[-1]], [0, 1000], '-k', lw=0.5, color='lightgray')
        plt.xlim([0, shift[-1]])

        if type != 'single':
            plt.subplot(2,1,2)
            plt.plot([shift[-1], shift[-1]], [0, 1000], '-k', lw=0.5, color='lightgray')
            plt.xlim([0, shift[-1]])
        # print(shift)

    # Defining top boundary of a plot
    if top1 == 0:
        if type != 'single':
            top1 = np.ceil(np.max([np.max(-np.log10(p1)), np.max(-np.log10(p2))]))
        else:
            top1 = np.ceil(np.max(-np.log10(p1)))

    if top2 == 0:
        if type != 'single':
            top2 = top1

    # Setting up the position of labels:
    shift_label = shift[-1]
    shift = (shift[1:]+shift[:-1])/2.
    labels = chrs_names

    # Plotting horizontal lines
    for i, y in enumerate(lines):
        if type != 'single':
            plt.subplot(2,1,1)
            plt.plot([0, shift_label], [y, y], color = lines_colors[i])
            plt.subplot(2,1,2)
            plt.plot([0, shift_label], [y, y], color = lines_colors[i])
        else:
            plt.subplot(1,1,1)
            plt.plot([0, shift_label], [y, y], color = lines_colors[i])

    if type != 'single':
        plt.subplot(2,1,1)
        if not plot_positions:
            plt.xticks(shift, labels)
        plt.ylim([cut+0.05, top1])
    else:
        plt.subplot(1,1,1)
        plt.ylim([cut, top1])
    plt.title(title)
    if type != 'single':
        plt.setp(plt.gca().get_xticklabels(), visible=False)
        if not plot_positions:
            plt.xticks(shift)
    else:
        if not plot_positions:
            plt.xticks(shift, labels)

    plt.text(shift_label*0.95,top1*0.95,label1,#bbox=dict(boxstyle="round", fc="1.0"),
            verticalalignment='top', horizontalalignment='right')

    if type != 'single':
        plt.subplot(2,1,2)
        plt.ylim([cut, top2])
        if type == 'inverted':
            plt.gca().invert_yaxis()
        if not plot_positions:
            plt.xticks(shift, labels)
        if type == 'inverted':
            plt.text(shift_label*0.95,top2*0.95,label2,#bbox=dict(boxstyle="round", fc="1.0"),
                verticalalignment='bottom', horizontalalignment='right')
        else:
            plt.text(shift_label*0.95,top2*0.95,label2,#bbox=dict(boxstyle="round", fc="1.0"),
                verticalalignment='top', horizontalalignment='right')
        plt.ylabel(ylabel)
        plt.gca().yaxis.set_label_coords(-0.065,1.)
        plt.xlabel(xlabel)
        # plt.tight_layout(hspace=0.001)
        plt.subplots_adjust(hspace=0.00)
    else:
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)

    if zoom is not None:
        if type != 'single':
            plt.subplot(2,1,1)
            plt.xlim([zoom_shift-zoom[2], zoom_shift+zoom[2]])
            plt.subplot(2,1,2)
            plt.xlim([zoom_shift-zoom[2], zoom_shift+zoom[2]])
        else:
            plt.subplot(1,1,1)
            plt.xlim([zoom_shift-zoom[2], zoom_shift+zoom[2]])

    return 0

# def manhattan1(p1, pos1, chr1, label1, info1=[], info1_bins=[], info_colors=[], cut = 2, colors = ['k', '0.5'], title='Title', top = 0):
#     '''
#     Static Manhattan plot
#     :param p1: p-values for the top panel
#     :param pos1: positions
#     :param chr1: chromosomes numbers
#     :param label1: label
#     :param cut: lower cut (default 2)
#     :param colors: sequence of colors (default: black/gray)
#     :return:
#     '''
#     import matplotlib as mpl
#     mpl.rcParams['axes.color_cycle'] = ['k', '0.5']
#     shift=np.array([0.0])
#     plt.clf()
#     for i in range(1,23):
#         print(i)
#         filt = (chr1==i)
#         x = shift[-1]+pos1[filt]
#         y = -np.log10(p1[filt])
#         # print(filt.sum(), x[:5])
#         if len(info1) == 0:
#             plt.plot(x[y>cut], y[y>cut], '.')
#         else:
#             for k in range(len(info1_bins)-1):
#                 filt2 = (info1[filt] > info1_bins[k]) & (info1[filt] <= info1_bins[k+1])
#                 # print(filt.sum())
#                 plt.plot(x[filt2 & (y > cut)], y[filt2 & (y > cut)], '.', alpha=0.7, color=info_colors[k])
#         shift_f = np.max(x)
#         shift = np.append(shift, shift_f)
#         plt.plot([shift[-1], shift[-1]], [0, 10], '-k', lw=0.5, color='lightgray')
#         plt.xlim([0, shift[-1]])
#     if top == 0:
#         top = np.ceil(np.max([np.max(-np.log10(p1)), np.max(-np.log10(p2))]))
#     shift = (shift[1:]+shift[:-1])/2.
#     plt.ylim([cut, top])
#     plt.title(title)
#     # plt.setp(plt.gca().get_xticklabels(), visible=False)
#     plt.xticks(shift)
#     # plt.text(shift[12],8,label1,bbox=dict(boxstyle="round", fc="1.0"))
#     labels = np.arange(1,23).astype(str)
#     labels[-2] = ''
#     labels[-4] = ''
#     labels[-6] = ''
#     labels[-8] = ''
#     labels[-10] = ''
#     plt.xticks(shift, labels)
#     plt.ylabel('-log10(p-value)')
#     plt.xlabel('chromosome')
#     # plt.tight_layout(hspace=0.001)
#     # plt.subplots_adjust(hspace=0.001)


def reduce_data(data, top_snps=1000):
    '''
    Function reduces data for interactive plot
    :param data: list of datasets
    :param top_snps: number of snps to include
    :return: combined table
    '''
