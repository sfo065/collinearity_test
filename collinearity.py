import pandas as pd
import numpy as np

header = ['ID', 'x', 'y', 'z', 'height2', 'rx', 'ry', 'rz',
          'pos1', 'pos2', 'pos3', 'att1', 'att2', 'att3', 'week', 'ToW', 'n_sat',
          'PDOP', 'lat', 'long', 'height']
nx, ny = 17004, 26460
metadata = pd.read_table(r'../Code/testing/ims/flyfoto/GNSSINS/EO_V355_TT-14525V_20210727_1.txt', comment='#', delim_whitespace=True, names=header)
focal_length = int(100.5*1e-3/4e-6) # image coordinates
ppa = np.array((nx/2 - int(0.08*1e-3/4e-6), ny/2)) # image coordinates
cx, cy, cz, rx, ry, rz =  [metadata.loc[5][i] for i in ['x', 'y', 'z', 'rx', 'ry', 'rz']]
rx, ry, rz = np.deg2rad(np.array((rx, ry, rz)))

def RotationMatrix(rx, ry, rz):
    R1 = np.array([[1, 0, 0],
                   [0, np.cos(rx), -np.sin(rx)],
                   [0, np.sin(rx),np.cos(rx)]])
    
    R2 = np.array([[np.cos(ry), 0, np.sin(ry)],
                   [0, 1, 0],
                   [-np.sin(ry), 0, np.cos(ry)]])
    
    R3 = np.array([[np.cos(rz), -np.sin(rz), 0],
                   [np.sin(rz), np.cos(rz), 0],
                   [0, 0, 1]])
    
    return (R1@R2@R3).T 

def UTM_to_image(X, C, x0, R, f):
    '''
    Calculates image coordinates using collinearity equations.

    X: Object position in external coordinates coordinates
    C: Camera position in external coordinates
    x0: Focal point in image coordinates
    R: Perspective projection matrix from RotationMatrix()
    f: Focal length in image coordinates
    '''
    d = X-C
    denom = (R[0, 2]*d[0] + R[1, 2]*d[1] + R[2, 2]*d[2])
    x = x0[0] - f*(R[0, 0]*d[0] + R[1, 0]*d[1] + R[2, 0]*d[2])/denom
    y = x0[1] - f*(R[0, 1]*d[0] + R[1, 1]*d[1] + R[2, 1]*d[2])/denom
    return int(x), int(y)

# test_point is some point in UTM-coords to be transformed to image coords.  
 
R = RotationMatrix(rx, ry, rz)
C = np.array((cx, cy, cz))
pt_im = UTM_to_image(test_point, C, ppa, R, focal_length)