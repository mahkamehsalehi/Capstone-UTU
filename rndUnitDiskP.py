import numpy as np

def rnd_unit_disk_p():
    # rndUnitDiskP returns a uniformly random point on a unit disk
    r = np.sqrt(np.random.rand())
    theta = 2 * np.pi * np.random.rand()
    p = r * np.array([np.cos(theta), np.sin(theta)])
    return p