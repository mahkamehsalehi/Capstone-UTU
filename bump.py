import numpy as np

def bump(r):
    # bump is the bump function (scaled to [0,1]), loved by all of us!
    # note: vectorized computation
    # out = bump(r)

    out = np.multiply(r <= 1.0, np.exp(np.divide(-1, (1 - np.power(r,2)))))

    return out