def bb_overlap(bb1, bb2):
    # bb_overlap checks if two BBs overlap
    # is_overlapping = bb_overlap(bb1, bb2)

    no_contact = (
        bb1[1, 0] < bb2[0, 0] or
        bb2[1, 0] < bb1[0, 0] or
        bb1[1, 1] < bb2[0, 1] or
        bb2[1, 1] < bb1[0, 1]
    )

    is_overlapping = not no_contact

    return is_overlapping