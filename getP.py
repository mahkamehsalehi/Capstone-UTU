import numpy as np
from scipy.spatial import KDTree

def get_p(pss, p, d_max):
    i = 0
    j = 0
    d = np.inf

    for i0, ps in enumerate(pss):
        n = len(ps)
        if n > 0:
            tree = KDTree(ps)
            ji, di = tree.query([p], k=1)

            if di < d:
                d = di[0]
                i = i0
                j = ji[0]

    flag = (d < d_max)
    return flag, i, j
