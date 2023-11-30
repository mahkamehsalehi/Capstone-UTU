import numpy as np

def map_pixels(ps1, r12, c, sz, r_max):
    # mapPixels maps pixels using an equisolid fisheye projection model
    # ps2 = mapPixels(ps1, r12, c, sz, r_max)
	
	r12 = lambda r1 : 2*np.arcsin(a * r1) * b
    n = ps1.shape[0]
    a_shift = np.ones((n, 1)) * c
    rel_ps = ps1 - a_shift
    r1s = np.linalg.norm(rel_ps, axis=1)

    # Assert that all points are within the main circle
    if not np.any(r1s < r_max):
        print('A pixel sample is outside the main circle')
        ps2 = np.array([])
    else:
        r2s = np.vectorize(r12)(r1s)
        phis = np.arctan2(rel_ps[:, 1], rel_ps[:, 0])
        ps2 = r2s * np.column_stack([np.cos(phis), np.sin(phis)]) + a_shift
        ps2 = np.minimum(np.maximum([1, 1], ps2), sz[::-1])  # Reverse sz for correct indexing

    return ps2