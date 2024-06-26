import numpy as np

from getBoundingBox import get_bounding_box 
from getCrossing0 import getCrossing0
from bbOverlap import bb_overlap

def getCrossing(ps1, ps2, p0):
    """
    Finds the intersection point(s) of two curves (ps1 and ps2) closest to p0.
    There can be two crossings since ps1 and ps2 are generalized curves (GCs).
    Returns an empty list or the closest valid intersection point(s).
    """

    # Initialize variables
    p = []
    counter = 0
    n1, n2 = len(ps1), len(ps2)

    # Brute force search through segments of both curves.
    for i1 in range(n1 - 1):
        segm1 = ps1[i1:i1 + 2]
        for j1 in range(n2 - 1):
            segm2 = ps2[j1:j1 + 2]

            if bb_overlap(get_bounding_box(segm1), get_bounding_box(segm2)):
                pFound = getCrossing0(segm1, segm2)
                if len(pFound) != 0: # is not None:
                    p.append(pFound)
                    counter += 1

    # Find the closest intersection point to p0
    if counter >= 1:
        distances = np.linalg.norm(np.array(p) - np.array(p0), axis=1)
        closest_index = np.argmin(distances)
        return p[closest_index]

    return []