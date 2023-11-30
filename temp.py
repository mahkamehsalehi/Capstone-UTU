 #finding the projection of a point p onto a line segment defined by two points ps(i,:) and ps(i+1,:)
 
 def get_proj_on_segment(p, p1, p2):
    # Find the projection of point p onto the line segment defined by p1 and p2

    # Vector representing the line segment
    v = p2 - p1

    # Vector from p1 to p
    w = p - p1

    # Compute the projection parameter
    t = np.dot(w, v) / np.dot(v, v)

    # Clamp t to the interval [0, 1]
    t = np.clip(t, 0, 1)

    # Compute the projected point q
    q = p1 + t * v

    # Compute the distance between p and q
    d = np.linalg.norm(p - q)

    return q, d

# Example usage within the loop
for i in range(i1, i2):
    qi, di = get_proj_on_segment(p, ps[i, :], ps[i + 1, :])

    if di <= d:
        q = qi
        d = di
# Rest of the code...
