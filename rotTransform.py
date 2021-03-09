def rotTransform(x, y, theta):
    import numpy as np
    import math
    # Create an array of x and y
    xy = np.array([[x],[y]])
    # Creating a transformation matrix (rows = [ , , ], col = [],[],[])
    matrix= np.array([[math.cos(theta),math.sin(theta)],
                     [-math.sin(theta),math.cos(theta)]])
    # Transform the coord. to x' and y'
    transformed = np.dot(matrix,xy)
    # Return the new coordinates
    return transformed

