
import numpy as np  # Importing Numpy for numerical operations
from scipy.spatial import cKDTree  # Importing SciPy's KDTree for nearest neighbour search

def get_CSC_points(aPixel, h):
    """
    Function to generate the Cone Spherical Coordinates (CSC) points in a 3D unit sphere.

    Args:
        aPixel (numpy array): Pixel coordinates in image space
        h (float): Height of the cone at its base

    Returns:
        ps (numpy array): Corresponding pixel coordinates on 3D unit sphere CSC
    """

    global rMax, thetaMax, c  # Global variables

    aPixel = aPixel - c  # Subtract mean pixel location from input pixel location
    r = np.linalg.norm(aPixel)  # Compute Euclidean distance (r) of pixel from origin
    theta = thetaMax * r / rMax  # Theta is proportional to radius normalized by maximum possible radius
    phi = np.arctan2(aPixel[1], aPixel[0])  # Phi is angle in x-y plane

    na = [np.sin(theta) * np.cos(phi), np.sin(theta) * np.sin(phi), np.cos(theta)]  # Normal vector at base of cone
    na0 = [np.cos(phi), np.sin(phi), 0.0]  # Unit vector in x-y plane
    nb = np.cross(na0, na) / np.linalg.norm(np.cross(na0, na))  # Normal vector at first vertex of cone
    nc = np.cross(na, nb) / np.linalg.norm(np.cross(na, nb))  # Normal vector at second vertex of cone

    rho = np.sqrt(1.0 - h**2)  # Radius of CSC in 3D

    deltaPixel = 8.0  # Approximate distance between points on CSC
    dPsi = deltaPixel / (rho * rMax)  # Angular increment along axis of symmetry
    psis = np.arange(0, 2*np.pi, dPsi)  # Array of angular positions along axis of symmetry

    n = len(psis)  # Number of points on CSC

    cps = np.zeros((n,3))  # Initialize array for storing coordinates of points on CSC
    for i in range(n):
        psi = psis[i]  # Angular position along axis of symmetry
        cps[i,:] = h * na + rho * (nb * np.cos(psi) + nc * np.sin(psi))  # Compute coordinates of point on CSC

    ps = np.zeros((n,2))  # Initialize array for storing pixel coordinates on CSC
    counter = 0
    for i in range(n):
        p3d = cps[i,:]  # Coordinates of point on CSC
        phi = np.arctan2(p3d[1], p3d[0])  # Angle in x-y plane
        theta = np.arccos(p3d[2])  # Angular distance from origin
        if theta <= thetaMax:
            r = theta / thetaMax * rMax  # Compute radius of point on CSC
            p = c + r * [np.cos(phi), np.sin(phi)]  # Convert polar coordinates to Cartesian and add mean pixel location
            counter += 1
            ps[counter,:] = p  # Store pixel coordinate in array
    ps = ps[:counter,:]  # Trim array to number of points on CSC

    dps = np.diff(ps)  # Compute differences between consecutive pixels
    ls = np.linalg.norm(dps, axis=1)  # Compute Euclidean distances along each dimension
    l0 = np.mean(ls)   # Approximate average distance between points on CSC
    lMax = np.max(ls)  # Maximum distance between consecutive pixels

    if lMax >3 * l0:  # If maximum distance exceeds three times the average, trim array to remove extraneous points
        inds = np.concatenate((np.arange(i+1, n), np.arange(n)), axis=0)
        ps = ps[inds,:]

    return ps  # Return pixel coordinates on CSC

def get_CSC_error(aPixel, h, ps):
    """
    Function to compute the error in converting a given set of pixels from image space to Cone Spherical Coordinates (CSC).

    Args:
        aPixel (numpy array): Pixel coordinates in image space
        h (float): Height of the cone at its base
        ps (numpy array): Corresponding pixel coordinates on 3D unit sphere CSC

    Returns:
        e (float): Mean distance between each pixel and its nearest neighbour on CSC
        l (int): Number of pixels in original image space
    """

    cps = get_CSC_points(aPixel, h)  # Generate CSC points for given input pixel coordinates

    tree = cKDTree(cps)  # Construct KDTree from CSC points
    ds, _ = tree.query(ps, k=1)  # Compute distances of original pixels to nearest neighbour in CSC

    e = np.mean(ds)  # Mean distance between each pixel and its nearest neighbour on CSC
    l = len(ds)  # Number of pixels in original image space

    return e, l  # Return mean error and number of pixels in original image space

