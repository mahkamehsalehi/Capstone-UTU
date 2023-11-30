def getNewOris(pss):
    """
    Extracts 'ori' values from a list of objects 'pss'.
    Returns two lists: all 'ori' values and unique 'ori' values.
    """

    # Extract 'ori' values from each object in the list.
    allOris = [obj.ori for obj in pss]

    # Find unique 'ori' values.
    uniqueOris = list(set(allOris))

    return allOris, uniqueOris
