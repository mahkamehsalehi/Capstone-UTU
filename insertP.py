# Insert value p at position j in array ps1

import numpy as np

def insert_p(ps1, j, p):
    # 1 <= j < len(ps1) 
    ps2 = np.insert(ps1, j+1, p, axis=0)
    # return new array with p inserted
    return ps2

