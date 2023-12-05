from getCSCpointsAndCSCerror import get_CSC_error

def fun_adapter(x, ps):
    # fun_adapter helps to use fminsearch()
    # e = fun_adapter(x, ps)
    # Uses get_csc_error!!
    a_pixel = x[:2]  # Extract the first two elements of x as a_pixel
    h = 0.0  # Initialize h with a constant value (commented out: x[2])

    # Call another function to compute the error and common length
    e, _ = get_CSC_error(a_pixel, h, ps)

    return e