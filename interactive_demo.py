# Load standard libraries
import numpy as np
from pandas import DataFrame
from bokeh.plotting import figure, output_notebook, show, gridplot
from bokeh.models import ColumnDataSource, widgets, CustomJS
from bokeh.models.glyphs import Circle, Square
from bokeh.models import HoverTool

from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.io import output_file, show, vform, vplot, hplot


from assocplots.misc import mock_data_generation


data_m = np.genfromtxt('HIP_MEN_chr_pos_rs_pval.txt', dtype=None, names=['chr', 'pos', 'snp', 'pval'])
data_w = np.genfromtxt('HIP_WOMEN_chr_pos_rs_pval.txt', dtype=None, names=['chr', 'pos', 'snp', 'pval'])


# data = mock_data_generation(M=100000)
#
# data1=data[0]
# data1['pval'] /= 500000.*np.exp(-(data1['pos']-0.5*len(data1))**2/5.0)+1.
# data2=data[1]

# from assocplots.interactive import *

cut1, cut2, data = data_reduce(data_m, data_w, N=5000)

p1,p2,p3,p4,pq1 = mann_only_interactive(data, cut1, cut2)
show(vplot(p1,p2))
show(hplot(pq1,p4))
show(p4)
from assocplots.htmloutput import *
write_to_html([p1,p2,pq1,p4], filename='output.hmtl', title='Title')
