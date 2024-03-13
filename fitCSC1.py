import numpy as np
from scipy.optimize import fmin
from densifyCurve import densify_curve
from funAdapter import fun_adapter
from getCSCpointsAndCSCerror import get_CSC_error
from rndUnitDiskP import rnd_unit_disk_p

#!!!Requires densify_curve, rnd_unit_disk_p, get_csc_error and fun_adapter functions!!!

def fit_csc1(ps,rMax, c):


    # 0) densify close to the pixel size
    ps = densify_curve(ps, 2.0)
    n2 = ps.shape[0]

    # 1) random search
    # 1.1) aPixel must be within the (c, radius) disk
    n_tries = 20
    e_min = float('inf')
    a_pixel_min = []
    h_min = np.nan

    for _ in range(n_tries):
        a_pixel = c + rnd_unit_disk_p() * rMax
        h = 0.0
        e, l = get_CSC_error(a_pixel, h, ps)

        if e < e_min:
            e_min = e
            l_min = l
            a_pixel_min = a_pixel
            h_min = h

    a_pixel = a_pixel_min
    h = h_min
    e = e_min
    l = l_min

    # Visualization (optional, commented out with "if 0")
    # cps = get_csc_points(a_pixel, h)
    # plt.figure(3)
    # plt.plot(ps[:, 0], ps[:, 1], 'k.', cps[:, 0], cps[:, 1], 'b.')
    # plt.axis('equal')

    # 2) minimization of e
    x0 = np.concatenate([a_pixel, [h]])
    x = fmin(fun_adapter, x0, args=(ps,), disp=True, maxiter=300, ftol=1.0)
    a_pixel = x[:2]
    h = x[2]

    # Visualization (optional, commented out with "if 1")
    # cps = get_csc_points(a_pixel, h)
    # plt.figure(3)
    # plt.plot(cps[:, 0], cps[:, 1], 'bo', ps[:, 0], ps[:, 1], 'ko', markersize=2)
    # plt.axis('equal')

    # Set a flag indicating successful fit
    flag = 1

    return a_pixel, h, e, l, flag

# The rest of the functions (densify_curve, rnd_unit_disk_p, get_csc_error, get_csc_points, fun_adapter) would need to be implemented or imported.
