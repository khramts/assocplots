import matplotlib.pyplot as plt
import numpy as np

from assocplots.qqplot import *

# data = np.genfromtxt('C:\\Users\\Ekaterina\\Desktop\\file_transfer\\fem_assoc_dos_ocd_occc_eur_sr-qc.hg19.dosage.assoc.dosage.QCed')
# data = data[:,-1]
# data2 = np.genfromtxt('C:\\Users\\Ekaterina\\Desktop\\file_transfer\\mal_assoc_dos_ocd_occc_eur_sr-qc.hg19.dosage.assoc.dosage.QCed')
# data2 = data2[:,-1]


q_data, q_th, q_err = qqplot([data, data2], labels=['female', 'male'], error_type='experimental', n_quantiles=1000, alpha=0.95, color=['r', 'b'])


data_male = np.genfromtxt('sample_data\GIANT_Randall2013PlosGenet_stage1_publicrelease_HapMapCeuFreq_BMI_MEN_N.txt', dtype=None, names=True)
data_female = np.genfromtxt('sample_data\GIANT_Randall2013PlosGenet_stage1_publicrelease_HapMapCeuFreq_BMI_WOMEN_N.txt', dtype=None, names=True)


q_data, q_th, q_err = qqplot([data_female['P2gc'], data_male['P2gc']], labels=['female', 'male'], error_type='experimental', n_quantiles=1000, alpha=0.95, color=['r', 'b'])





data = mock_data_generation(1, 100000)

data[0]['chr']=1

manhattan(data[0]['pval'], data[0]['pos'], data[0]['chr'], 'abc',
          p2=None, pos2=None, chr2=None, label2=None,
          type='single',
          chrs_plot=None, chrs_names=None,
          cut=2,
          colors=['k', '0.5'],
          title='Title',
          xlabel='chromosome',
          ylabel='-log10(p-value)',
          top1=0,
          top2=0,
          lines=[10, 15],
          lines_colors=['g', 'r'],
          zoom=None)