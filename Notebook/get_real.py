import numpy as np

def get_real(path):
    # Read data from file
    with open(path, 'r') as f:
        lines = f.readlines()

    # Extract ratio and angle from file
    ratio = float(lines[0].split('=')[1])
    angle = float(lines[1].split('=')[1])

    # Extract time and position data from file
    data = np.loadtxt(lines[3:], delimiter=',')
    t = (data[:,0] - data[0,0])/ratio
    x = data[:,1] - data[0,1]
    y = data[:,2] - data[0,2]

    z = np.sqrt(x**2 + y**2)

    return t,z, ratio, angle

