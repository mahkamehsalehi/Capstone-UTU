import numpy as np

def get_proj_on_segment(p1, p2, p):
    # getProjOnSegment returns the nearest point on the 2D segment and the projection distance
    # pt, t, d = get_proj_on_segment(p1, p2, p)

    v1 = p - p1
    v2 = p2 - p1
    t = np.dot(v1, v2) / np.dot(v2, v2)

    t = np.minimum(np.maximum(0.0, t), 1.0)
    pt = p1 * (1 - t) + p2 * t
    d = np.linalg.norm(pt - p)

    return pt, t, d