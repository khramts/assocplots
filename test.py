import matplotlib.pyplot as plt
import numpy as np

from assocplots.qqplot import *

data = np.genfromtxt('C:\\Users\\Ekaterina\\Desktop\\file_transfer\\fem_assoc_dos_ocd_occc_eur_sr-qc.hg19.dosage.assoc.dosage.QCed')
data = data[:,-1]
data2 = np.genfromtxt('C:\\Users\\Ekaterina\\Desktop\\file_transfer\\mal_assoc_dos_ocd_occc_eur_sr-qc.hg19.dosage.assoc.dosage.QCed')
data2 = data2[:,-1]


q_data, q_th, q_err = qqplot([data, data2], labels=['female', 'male'], error_type='experimental', n_quantiles=1000, alpha=0.95, color=['r', 'b'])
