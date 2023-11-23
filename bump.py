import numpy as np

def bump(r):
    # bump is the bump function (scaled to [0,1]), loved by all of us!
    # note: vectorized computation
    # out = bump(r)

    out = np.multiply(r <= 1.0, np.exp(-1 / (1 - r**2)))

    return out