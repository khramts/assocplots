import numpy as np
from pandas import DataFrame
from bokeh.plotting import figure, output_notebook, show, gridplot
from bokeh.models import ColumnDataSource, widgets, CustomJS
from bokeh.models.glyphs import Circle, Square
from bokeh.models import HoverTool

from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.io import output_file, show, vform, vplot, hplot

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
        data['pval1'][j] = data1['pval'][i]
        data['pval2'][j] = data2['pval'][np.where(data2['snp'] == data1['snp'][i])]
        j += 1

    for i in ind2:
        if np.sum(data2['snp'][i] == data['snp'])==0:
            data['snp'][j] = data2['snp'][i]
            data['pos'][j] = data2['pos'][i]
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
        if err_mode == 'simple':
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

    return cut1, cut2, data


def mann_only_interactive(data, cut1, cut2):
    '''
    Generate interactive dots.
    :param data:
    :param cut1:
    :param cut2:
    :return:
    '''
    ts = DataFrame({'snp': data['snp'],
                    'pos': data['pos'],
                    'pval1': -np.log10(data['pval1']),
                    'pval1_q': -np.log10(data['pval1_q']),
                    'pval2': -np.log10(data['pval2']),
                    'pval2_q': -np.log10(data['pval2_q'])})
    hover1 = HoverTool(
        tooltips=[
            ("snp", "@snp"),
            ("pos", "@pos"),
            ("-log10(pval1,pval2)", "(@pval1, @pval2)"),
        ]
    )
    hover2 = HoverTool(
        tooltips=[
            ("snp", "@snp"),
            ("pos", "@pos"),
            ("-log10(pval1,pval2)", "(@pval1, @pval2)"),
        ]
    )
    hoverq = HoverTool(
        tooltips=[
            ("snp", "@snp"),
            ("pos", "@pos"),
            ("-log10(pval1,pval2)", "(@pval1, @pval2)"),
        ]
    )
    tools1 = ['reset', 'wheel_zoom','box_select', hover1]
    tools2 = ['reset', 'wheel_zoom','box_select', hover2]
    toolsq = ['reset', 'wheel_zoom','box_select', hoverq]

    source = ColumnDataSource(data=ts)
#     original_source = ColumnDataSource(data=ts)

    source_filt = ColumnDataSource(data=dict(snp=[], pos=[], pval1=[], pval2=[]))

    source.callback = CustomJS(args=dict(source_filt=source_filt), code="""
        var inds = cb_obj.get('selected')['1d'].indices;
        var d1 = cb_obj.get('data');
        var d2 = source_filt.get('data');
        d2['snp'] = []
        d2['pos'] = []
        d2['pval1'] = []
        d2['pval2'] = []
        for (i = 0; i < inds.length; i++) {
            d2['snp'].push(d1['snp'][inds[i]])
            d2['pos'].push(d1['pos'][inds[i]])
            d2['pval1'].push(d1['pval1'][inds[i]])
            d2['pval2'].push(d1['pval2'][inds[i]])
        }
        source_filt.trigger('change');
       // data_table_filt.trigger('change');
        """)

    selection_glyph = Circle(fill_color='firebrick', line_color=None)
    nonselection_glyph = Circle(fill_color='blue', fill_alpha=0.1, line_color=None)
    selection_glyph_2 = Square(fill_color='firebrick', line_color=None)
    nonselection_glyph_2 = Square(fill_color='olive', fill_alpha=0.1, line_color=None)

    p1 = figure(plot_width=900, plot_height=300, tools=tools1, x_range=[0, 100000], webgl=True)
    r1 = p1.circle('pos', 'pval1', source=source, line_color=None, size=10)
    r1.selection_glyph = selection_glyph
    r1.nonselection_glyph = nonselection_glyph
    p1.patch([0, np.max(data['pos']), np.max(data['pos']), 0], [0, 0, -np.log10(cut1), -np.log10(cut1)], alpha=0.2, line_color=None, fill_color='blue', line_width=2)

    p2 = figure(plot_width=900, plot_height=300, tools=tools2, x_range=p1.x_range, y_range=p1.y_range, webgl=True)
    r2 = p2.square('pos', 'pval2', source=source, line_color=None, size=10, color="olive")
    r2.selection_glyph = selection_glyph_2
    r2.nonselection_glyph = nonselection_glyph_2
    p2.patch([0, np.max(data['pos']), np.max(data['pos']), 0], [0, 0, -np.log10(cut1), -np.log10(cut1)], alpha=0.2, line_color=None, fill_color='olive', line_width=2)

    pq1 = figure(plot_width=400, plot_height=400, tools=toolsq, webgl=True)
    pq1.line([0, 5], [0, 5], line_width=3, color="black", alpha=0.5, line_dash=[4, 4])
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

    columns = [
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