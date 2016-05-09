import numpy as np
from pandas import DataFrame
from bokeh.plotting import figure, output_notebook, show, gridplot
from bokeh.models import ColumnDataSource, widgets, CustomJS
from bokeh.models.glyphs import Circle, Square
from bokeh.models import HoverTool

from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.models import FixedTicker

from bokeh.io import output_file, show, vform, vplot, hplot
import re

def sorted_nicely( l ):
    """ Sort the given iterable in the way that humans expect."""
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(l, key = alphanum_key)


def data_reduce(data1, data2, N=1000, err_mode='poisson'):
    '''
    Reducing number of points in order to speed-up rendering. Only top N points in each data set will be displayed.
    :param data1: First data set
    :param data2: Second data set
    :param N: Number of points to display. Total number of points will be <=2N
    :param err_mode:
    :return:
    '''
    ind1 = data1['pval'].argsort()[:N]
    cut1 = data1['pval'][data1['pval'].argsort()[N]]
    ind2 = data2['pval'].argsort()[:N]
    cut2 = data2['pval'][data2['pval'].argsort()[N]]
    ind = np.array(list(set(np.concatenate([ind1,ind2]))))
    print(len(ind))
    data = np.ones(2*N, dtype=[('snp', np.dtype('U25')),
                               ('pos', np.int),
                               ('chr', np.dtype('U5')),
                               ('pval1', float),
                               ('pval2', float),
                               ('pval1_q', float),
                               ('pval2_q', float),
                               ('pval1_q_top', float),
                               ('pval2_q_top', float),
                               ('pval1_q_bot', float),
                               ('pval2_q_bot', float)])
    j=0
    for i in ind1:
        data['snp'][j] = data1['snp'][i]
        data['pos'][j] = data1['pos'][i]
        data['chr'][j] = data1['chr'][i]
        data['pval1'][j] = data1['pval'][i]
        data['pval2'][j] = data2['pval'][np.where(data2['snp'] == data1['snp'][i])]
        j += 1

    for i in ind2:
        if np.sum(data2['snp'][i] == data['snp'])==0:
            data['snp'][j] = data2['snp'][i]
            data['pos'][j] = data2['pos'][i]
            data['chr'][j] = data2['chr'][i]
            data['pval2'][j] = data2['pval'][i]
            data['pval1'][j] = data1['pval'][np.where(data1['snp'] == data2['snp'][i])[0]]
            j += 1

    for i in range(len(data)):
        data['pval1_q'][i] = 1.0*np.sum(data['pval1'][i]>=data1['pval']) / len(data1)
        data['pval2_q'][i] = 1.0*np.sum(data['pval2'][i]>=data2['pval']) / len(data2)
        if err_mode == 'poisson':
            temp_err_1 = np.sqrt(np.sum(data['pval1'][i]>=data1['pval'])) / len(data1)
            data['pval1_q_top'][i] = data['pval1'][i] + temp_err_1
            data['pval1_q_bot'][i] = data['pval1'][i] - temp_err_1
            if data['pval1_q_bot'][i] < 0:
                data['pval1_q_bot'][i] = 1e-12
            temp_err_2 = np.sqrt(np.sum(data['pval2'][i]>=data2['pval'])) / len(data2)
            data['pval2_q_top'][i] = data['pval2'][i] + temp_err_2
            data['pval2_q_bot'][i] = data['pval2'][i] - temp_err_2
            if data['pval2_q_bot'][i] < 0:
                data['pval2_q_bot'][i] = 1e-12
        elif err_mode == 'simple':
            temp_err_1 = np.sqrt(np.sum(data['pval1_q'][i]>=data1['pval'])) / len(data1)
            data['pval1_q_top'][i] = data['pval1'][i] + temp_err_1
            data['pval1_q_bot'][i] = data['pval1'][i] - temp_err_1
            if data['pval1_q_bot'][i] < 0:
                data['pval1_q_bot'][i] = 1e-12
            temp_err_2 = np.sqrt(np.sum(data['pval2'][i]>=data2['pval'])) / len(data2)
            data['pval2_q_top'][i] = data['pval2'][i] + temp_err_2
            data['pval2_q_bot'][i] = data['pval2'][i] - temp_err_2
            if data['pval2_q_bot'][i] < 0:
                data['pval2_q_bot'][i] = 1e-12
        # else:

    return cut1, cut2, data



def data_reduce_fast(data1, data2, N=1000, err_mode='poisson'):
    '''
    Reducing number of points in order to speed-up rendering. Only top N points in each data set will be displayed.
    :param data1: First data set
    :param data2: Second data set
    :param N: Number of points to display. Total number of points will be <=2N
    :param err_mode:
    :return:
    '''
    ind1 = data1['pval'].argsort()[:N]
    cut1 = data1['pval'][data1['pval'].argsort()[N]]
    ind2 = data2['pval'].argsort()[:N]
    cut2 = data2['pval'][data2['pval'].argsort()[N]]

    ind = np.array(list(set(np.concatenate([ind1,ind2]))))
    print(len(ind))

    data1.sort(order='snp')
    data2.sort(order='snp')

    indx = np.searchsorted(data2['snp'], data1['snp'])
    indx[indx>=len(data2['snp'])] = len(data2['snp'])-1
    m1 = data2['snp'][indx] == data1['snp']
    data1m = data1[m1]
    indx = np.searchsorted(data1m['snp'], data2['snp'])
    indx[indx >= len(data1m['snp'])] = len(data1m['snp']) - 1
    m1 = data1m['snp'][indx] == data2['snp']
    data2m = data2[m1]

    data = np.ones(len(data1m), dtype=[('snp', np.dtype('U25')),
                               ('pos', np.int),
                               ('chr', np.dtype('U5')),
                               ('pval1', float),
                               ('pval2', float),
                               ('pval1_q', float),
                               ('pval2_q', float),
                               ('pval1_q_top', float),
                               ('pval2_q_top', float),
                               ('pval1_q_bot', float),
                               ('pval2_q_bot', float)])

    data['snp'] = data1m['snp']
    data['pos'] = data1m['pos']
    data['chr'] = data1m['chr']
    data['pval1'] = data1m['pval']
    data['pval2'] = data2m['pval']

    data = data[(data['pval1']<cut1) | (data['pval2']<cut2)]


    for i in range(len(data)):
        data['pval1_q'][i] = 1.0*np.sum(data['pval1'][i]>=data1['pval']) / len(data1)
        data['pval2_q'][i] = 1.0*np.sum(data['pval2'][i]>=data2['pval']) / len(data2)
        # if err_mode == 'poisson':
        #     temp_err_1 = np.sqrt(np.sum(data['pval1'][i]>=data1['pval'])) / len(data1)
        #     data['pval1_q_top'][i] = data['pval1'][i] + temp_err_1
        #     data['pval1_q_bot'][i] = data['pval1'][i] - temp_err_1
        #     if data['pval1_q_bot'][i] < 0:
        #         data['pval1_q_bot'][i] = 1e-12
        #     temp_err_2 = np.sqrt(np.sum(data['pval2'][i]>=data2['pval'])) / len(data2)
        #     data['pval2_q_top'][i] = data['pval2'][i] + temp_err_2
        #     data['pval2_q_bot'][i] = data['pval2'][i] - temp_err_2
        #     if data['pval2_q_bot'][i] < 0:
        #         data['pval2_q_bot'][i] = 1e-12
        # elif err_mode == 'simple':
        #     temp_err_1 = np.sqrt(np.sum(data['pval1_q'][i]>=data1['pval'])) / len(data1)
        #     data['pval1_q_top'][i] = data['pval1'][i] + temp_err_1
        #     data['pval1_q_bot'][i] = data['pval1'][i] - temp_err_1
        #     if data['pval1_q_bot'][i] < 0:
        #         data['pval1_q_bot'][i] = 1e-12
        #     temp_err_2 = np.sqrt(np.sum(data['pval2'][i]>=data2['pval'])) / len(data2)
        #     data['pval2_q_top'][i] = data['pval2'][i] + temp_err_2
        #     data['pval2_q_bot'][i] = data['pval2'][i] - temp_err_2
        #     if data['pval2_q_bot'][i] < 0:
        #         data['pval2_q_bot'][i] = 1e-12
        # else:

    return cut1, cut2, data


def mann_only_interactive(data, cut1, cut2, chrs_plot=None):
    '''
    Generate interactive dots.
    :param data:
    :param cut1:
    :param cut2:
    :return:
    '''

    # Defining DataFrame for bokeh
    ts = DataFrame({'snp': data['snp'],
                    'pos': data['pos'],
                    'chr': data['chr'],
                    'color': np.zeros(len(data), dtype='S20'),
                    'abspos': data['pos'],
                    'pval1': -np.log10(data['pval1']),
                    'pval1_q': -np.log10(data['pval1_q']),
                    'pval2': -np.log10(data['pval2']),
                    'pval2_q': -np.log10(data['pval2_q'])})

    # Calculating proper positions

    if chrs_plot is None:
        chrs = np.unique(ts['chr'])
        if type(chrs[0]) == str:
            chrs = sorted_nicely(chrs)
        else:
            chrs.sort()
    else:
        chrs = chrs_plot

    print(chrs)

    temp_pos = 0
    xtixks_pos = np.zeros(len(chrs)+1)
    print(chrs)
    for i in range(len(chrs)):
        # Can be optimized here
        temp = ts['abspos'][ts['chr'] == chrs[i]]
        if len(temp) > 0:
            temp = np.max(temp)
        else:
            temp = 1000
        print(temp)
        xtixks_pos[i+1] = temp
        # temp_pos += temp
        # xtixks_pos[i+1] = temp_pos
        # ts['abspos'][ts['chr'] == chrs[i+1]] += temp_pos

    print(xtixks_pos)
    xtixks_pos = np.cumsum(xtixks_pos)
    print(xtixks_pos)

    for i in range(len(chrs)):
        ts['abspos'][ts['chr'] == chrs[i]] += xtixks_pos[i]

    print(xtixks_pos)
    xtixks_pos = (xtixks_pos[1:] + xtixks_pos[:-1])/2.0
    print(xtixks_pos)
    print(chrs)

    for i in range(len(chrs)):
        if i % 2 == 0:
            ts['color'][ts['chr'] == chrs[i]] = '#FA8072'
        else:
            ts['color'][ts['chr'] == chrs[i]] = '#00BFFF'

    # Defining hover tools
    hover1 = HoverTool(
        tooltips=[
            ("chr", "@chr"),
            ("snp", "@snp"),
            ("pos", "@pos"),
            ("-log10(pval1,pval2)", "(@pval1, @pval2)"),
        ]
    )
    hover2 = HoverTool(
        tooltips=[
            ("chr", "@chr"),
            ("snp", "@snp"),
            ("pos", "@pos"),
            ("-log10(pval1,pval2)", "(@pval1, @pval2)"),
        ]
    )
    hoverq = HoverTool(
        tooltips=[
            ("chr", "@chr"),
            ("snp", "@snp"),
            ("pos", "@pos"),
            ("-log10(pval1,pval2)", "(@pval1, @pval2)"),
        ]
    )
    tools1 = ['reset', 'xwheel_zoom', 'xpan', 'box_select', hover1]
    tools2 = ['reset', 'xwheel_zoom', 'xpan', 'box_select', hover2]
    toolsq = ['reset', 'wheel_zoom', 'pan', 'box_select', hoverq]

    source = ColumnDataSource(data=ts)
#     original_source = ColumnDataSource(data=ts)

    source_filt = ColumnDataSource(data=dict(snp=[], pos=[], pval1=[], pval2=[]))

    source.callback = CustomJS(args=dict(source_filt=source_filt), code="""
        var inds = cb_obj.get('selected')['1d'].indices;
        var d1 = cb_obj.get('data');
        var d2 = source_filt.get('data');
        d2['snp'] = []
        d2['pos'] = []
        d2['chr'] = []
        d2['pval1'] = []
        d2['pval2'] = []
        for (i = 0; i < inds.length; i++) {
            d2['snp'].push(d1['snp'][inds[i]])
            d2['pos'].push(d1['pos'][inds[i]])
            d2['chr'].push(d1['chr'][inds[i]])
            d2['pval1'].push(d1['pval1'][inds[i]])
            d2['pval2'].push(d1['pval2'][inds[i]])
        }
        source_filt.trigger('change');
       // data_table_filt.trigger('change');
        """)

    selection_glyph = Circle(fill_color='firebrick', line_color=None, size=6)
    nonselection_glyph = Circle(fill_color='gray', fill_alpha=0.1, line_color=None, size=6)
    selection_glyph_2 = Square(fill_color='firebrick', line_color=None, size=6)
    nonselection_glyph_2 = Square(fill_color='gray', fill_alpha=0.1, line_color=None, size=6)

    upper_bound = np.ceil(np.max([np.max(ts['pval1']), np.max(ts['pval2'])]) + .51)

    p1 = figure(responsive=True,
                plot_width=900,
                plot_height=300,
                tools=tools1,
                x_range=[0, np.max(ts['abspos'])],
                y_range=[-0.12*upper_bound, upper_bound],
                webgl=True)
    r1 = p1.circle('abspos', 'pval1', source=source, line_color=None, color='color', size=6)
    r1.selection_glyph = selection_glyph
    r1.nonselection_glyph = nonselection_glyph
    p1.patch([0, np.max(ts['abspos']), np.max(ts['abspos']), 0], [0, 0, -np.log10(cut1), -np.log10(cut1)], alpha=0.5, line_color=None, fill_color='gray', line_width=2)

    p2 = figure(responsive=True,
                plot_width=900,
                plot_height=300,
                tools=tools2,
                x_range=p1.x_range,
                y_range=p1.y_range,
                webgl=True)
    r2 = p2.square('abspos', 'pval2', source=source, line_color=None, color='color', size=6)
    r2.selection_glyph = selection_glyph_2
    r2.nonselection_glyph = nonselection_glyph_2
    p2.patch([0, np.max(ts['abspos']), np.max(ts['abspos']), 0], [0, 0, -np.log10(cut1), -np.log10(cut1)], alpha=0.5, line_color=None, fill_color='gray', line_width=2)

    pq1 = figure(responsive=True, plot_width=400, plot_height=400, tools=toolsq, webgl=True)
    pq1.line([0, 7], [0, 7], line_width=3, color="black", alpha=0.5, line_dash=[4, 4])
    rq1 = pq1.circle('pval1_q', 'pval1', source=source, line_color=None, size=10)
#     err_x = -np.log10(np.concatenate([data['pval1_q'][:100], data['pval1_q'][100::-1]]))
#     err_y = -np.log10(np.concatenate([data['pval1_q_top'][:100], data['pval1_q_bot'][100::-1]]))
#     er1 = pq1.patch(err_x, err_y, alpha=0.2, color='blue')
    rq2 = pq1.square('pval2_q', 'pval2', source=source, line_color=None, size=10, color="olive")
#     err_x = -np.log10(np.concatenate([data['pval2_q'][:100], data['pval2_q'][100::-1]]))
#     err_y = -np.log10(np.concatenate([data['pval2_q_top'][:100], data['pval2_q_bot'][100::-1]]))
#     er2 = pq1.patch(err_x, err_y, alpha=0.2, color='olive')
    rq1.selection_glyph = selection_glyph
    rq1.nonselection_glyph = nonselection_glyph
    rq2.selection_glyph = selection_glyph_2
    rq2.nonselection_glyph = nonselection_glyph_2

    # Labels for axes
    pq1.yaxis.axis_label = "Experimental quantiles, -log10(p)"
    pq1.xaxis.axis_label = "Theoretical quantiles, -log10(p)"
    p1.yaxis.axis_label = "-log10(p)"
    p1.xaxis.axis_label = "Chromosomes"
    p2.yaxis.axis_label = "-log10(p)"
    p2.xaxis.axis_label = "Chromosomes"
    p1.xgrid.grid_line_color = None
    p2.xgrid.grid_line_color = None

    # print(xtixks_pos)
    p1.xaxis[0].ticker = FixedTicker(ticks=[])
    p2.xaxis[0].ticker = FixedTicker(ticks=[])
    p1.text(xtixks_pos,xtixks_pos*0-0.12*upper_bound, [str(chrs[i]) for i in range(len(chrs))], text_align='center')
    p2.text(xtixks_pos,xtixks_pos*0-0.12*upper_bound, [str(chrs[i]) for i in range(len(chrs))], text_align='center')
    # p1.xaxis[0].ti

    columns = [
        TableColumn(field="chr", title="chr"),
        TableColumn(field="snp", title="snp"),
        TableColumn(field="pos", title="pos"),
        TableColumn(field="pval1", title="pval1"),
        TableColumn(field="pval2", title="pval2"),
    ]
    data_table = DataTable(source=source, columns=columns, width=300, height=280)
    p3 = vform(data_table)

    data_table_filt = DataTable(source=source_filt, columns=columns, width=500, height=500)
    p4 = vform(data_table_filt)

    return p1,p2,p3,p4,pq1