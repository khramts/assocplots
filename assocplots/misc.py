import numpy as np

def mock_data_generation(N=2,
                         M=10000,
                         seed=42,
                         chrs=[str(i) for i in range(1,23)] + ['X'],
                         lens=[248.450001, 243.025291, 197.754109, 190.840667, 180.652798, 170.713592, 159.073247, \
                              146.116596, 140.970765, 135.308233, 134.702538, 133.540295, 95.786711, 86.871164, \
                              82.237259, 90.043659, 80.988066, 77.875413, 58.818272, 62.849219, 33.414816,\
                              34.165155, 152.148603]):
    '''
    Generation of mock catalogues
    :param N: number of catalogs
    :param M: number of snps per catalog
    :return: list of catalogs
    '''
    res = []
    np.random.seed(seed)
    for k in range(N):
        snp = np.array([], dtype=np.dtype('U25'))
        chr = np.array([], dtype='|S2')
        pos = np.array([], dtype=np.int)
        pval = np.array([], dtype=np.float)
        pos_max = 0
        for i in range(len(chrs)):
            Mx = np.int(M*lens[i]/np.sum(lens))
            # posx = np.random.randint(1, np.int(lens[i] * 1e6), Mx)
            posx = np.arange(1, Mx+1)*100
            pvalx = np.random.rand(Mx)
            chrx = np.array([chrs[i]] * Mx)
            snpx = np.array(['rs_'+chrx[j]+'_'+str(posx[j]) for j in range(len(posx))])
            # pos_max += posx.max()
            snp = np.concatenate([snp, snpx])
            chr = np.concatenate([chr, chrx])
            pos = np.concatenate([pos, posx])
            pval = np.concatenate([pval, pvalx])
        x = np.zeros(len(pos), dtype=[('snp', np.dtype('U25')), ('chr', np.dtype('U2')), ('pos', np.int), ('pval', np.float)])
        x['snp'] = snp
        x['chr'] = chr
        x['pos'] = pos
        x['pval'] = pval
        res.append(x)
    return res

def data_reduce_2(data1,data2,N=100):
    '''
    Reduces data for interactive plot
    :param data: list of catalogs
    :return: table
    '''
    ind1 = data1['pval'].argsort()[N:][::-1]
    ind2 = data2['pval'].argsort()[N:][::-1]
    ind = np.array(list(set([ind1,ind2])))