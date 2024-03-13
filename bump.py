import numpy as np

def bump(r):
    # bump is the bump function (scaled to [0,1]), loved by all of us!
    # note: vectorized computation
    # out = bump(r)

    eps = 1.0e-5
    zoneTest = (r <= 1.0)
    not_zoneTest = (r > 1.0)
    #not_zoneTest[not_zoneTest <= 1.0] = 0
    #not_zoneTest[not_zoneTest != 0] = 1 

    r = np.multiply(zoneTest, r) + np.multiply(not_zoneTest, (1.0 - eps))
    out = np.exp(np.divide(-1, (1 - np.power(r,2))))

    return out