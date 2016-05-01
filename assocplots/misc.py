import numpy as np

def mock_data_generation(N=2, M=10000):
    '''
    Generation of mock catalogues
    :param N: number of catalogs
    :param M: number of snps per catalog
    :return: list of catalogs
    '''
    res = []
    for k in range(N):
        pos = np.arange(M)
        pval = np.random.rand(M) / (np.random.rand(M)<0.999)
        chr = np.random.randint(1, 23, M)
        x = [((u"rs%04d"%i), chr[i], pos[i], pval[i]) for i in pos[np.random.permutation(M)]]
        x = np.array(x, dtype=[('snp', np.dtype('U25')), ('chr', np.int), ('pos', np.int), ('pval', np.float)])
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