from getBoundingBox import get_bounding_box 
from getCrossing0 import getCrossing0
from bbOverlap import bb_overlap


def get_crossing(ps1, ps2):
    """
    Finds a single intersection point of two curves represented by ps1 and ps2.
    Returns an empty list or a valid intersection point.
    """

    # Initialize p as an empty list for default return value.
    p = []
    n1, n2 = len(ps1), len(ps2)

    # Brute force search through segments of both curves.
    for i1 in range(n1 - 1):
        segm1 = ps1[i1:i1 + 2]
        for j1 in range(n2 - 1):
            segm2 = ps2[j1:j1 + 2]
            if bb_overlap(get_bounding_box(segm1), get_bounding_box(segm2)):
                print("found bbOverlap")
                p = getCrossing0(segm1, segm2)
                if p:
                    return p  # Return the intersection point if found.

    return p  # Return an empty list if no intersection is found.