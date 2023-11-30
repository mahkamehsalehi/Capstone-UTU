import numpy as np

def getCrossing0(segm1, segm2):
    """
    Returns the intersection point of two line segments, segm1 and segm2.
    Returns an empty list if the intersection is outside the segments or at infinity.
    """

    eps = 1.0e-4
    a1, n1 = segm1[0], segm1[1] - segm1[0]
    a2, n2 = segm2[0], segm2[1] - segm2[0]

    N = np.column_stack((n1, -n2))
    if abs(np.linalg.det(N)) > eps:
        u1u2 = np.linalg.solve(N, a2 - a1)
        if 0.0 <= min(u1u2) and max(u1u2) <= 1.0:
            return a1 + u1u2[0] * n1
        else:
            return []
    else:
        return []

