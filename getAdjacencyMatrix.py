import numpy as np
from scipy.sparse import csr_matrix

# getAdjacencyMatrix returns the graph Laplacian L,
    # a weighted adjacency matrix A1 of a triangularization tris
    # and the edge distance matrix G
    # [L, Ll, Al, G] = getAdjacencyMatrix(tris, ps, delta)
    # L, Ll: normal and inverse distance-weighted Laplacian
    # Al: inverse distance weighted adjacency matrix
    # delta: mean edge length of tris
def get_adjacency_matrix(tris, ps, delta):

    # 0) initialization
    n = np.max(tris) + 1 # Python gives index out of bounds without +1
    A0 = csr_matrix((n, n))
    A = csr_matrix((n, n))
    G = csr_matrix((n, n))
    m = tris.shape[0]
    tris = np.column_stack([tris[:, 0], tris[:, 1], tris[:, 2], tris[:, 0]])

    # 1) assemble the matrices
    # 1.1) A: mean of v(p)= mean_{q\in N(p)} N(q)
    # 1.2) Al: v(p)= (sum_{q\in N(p)} N(q)/||p-q|| )/( sum_{q\in N(p)} 1/||p-q||
    # v'= A[v], v'= Al[v]
    for i in range(m):
        t = tris[i, :]
        for j in range(3):
            k1 = t[j]
            k2 = t[j + 1]
            p = ps[k1, :]
            q = ps[k2, :]
            temp = np.linalg.norm(p - q)
            G[k1, k2] = temp
            G[k2, k1] = temp
            temp = delta / temp
            A[k1, k2] = temp
            A[k2, k1] = temp
            A0[k1, k2] = 1
            A0[k2, k1] = 1

    # 2) unit property attained for A1
    # for i in range(n): A1[:, i] = A[:, i] / np.sum(A[:, i])
    Al = A / (np.ones((n, 1)) * np.sum(A, axis=0))

    # 3) weighted normalized Laplacian
    D0 = np.zeros(n)
    D = np.zeros(n)
    for i in range(n):
        D[i] = np.sum(A[i, :])
        D0[i] = np.sum(A0[i, :])

    # 1.3) the Laplacian
    sqrtD0 = np.diag(np.sqrt(1. / D0))
    L0 = np.eye(n) - sqrtD0 @ A0 @ sqrtD0
    sqrtD = np.diag(np.sqrt(1. / D))
    Ll = np.eye(n) - sqrtD @ A @ sqrtD

    return L0, Ll, Al, G