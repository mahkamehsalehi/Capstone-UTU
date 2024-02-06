import numpy as np
from sklearn.neighbors import NearestNeighbors

def get_p(pss, p, d_max):
    i = 0
    j = 0
    d = np.inf
    for i0, ps in enumerate(pss):
        n = len(ps['ps'])
        print('i0: ',i0)
        print('N: ',n)
        if n > 0 and p.size>0:
            print('ps: ',ps['ps'])
            neigh = NearestNeighbors(n_neighbors = 1, metric='euclidean')
            neigh.fit(ps['ps'])
            di, ji = neigh.kneighbors(p)
            print(di, ji)
            if di < d:
                d = di[0]
                i = i0
                j = ji[0]

    flag = (d < d_max)
    return flag, i, j
