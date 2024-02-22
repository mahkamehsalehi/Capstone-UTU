def bb_overlap(bb1, bb2):
    # bb_overlap checks if two BBs overlap
    # is_overlapping = bb_overlap(bb1, bb2)
    no_contact = (
        bb2[2] < bb1[0] or
        bb2[3] < bb1[1] or
        bb1[2] < bb2[0] or
        bb1[3] < bb2[1]
    )

    is_overlapping = not no_contact

    return is_overlapping