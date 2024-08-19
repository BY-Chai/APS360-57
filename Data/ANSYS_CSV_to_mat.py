import os
import scipy
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

"""
An ANSYS output file is a flattened grid
x
x
x
x
y
y
y
y
z
z
z
z

nodenumber,    x-coordinate,    y-coordinate,    z-coordinate,  total-pressure,         density,      x-velocity,      y-velocity,      z-velocity,    x-coordinate,    y-coordinate

"""

# Constants to set up
DT = 0.1 # Timestep size


# Directory to folder
filepath = r".\APS360_Cyl2D_Lam_2"

is_firstfile = True
t_n = 0
t = []
for file in os.listdir(filepath):
    print("File processed:", file)
    ansys = pd.read_csv(filepath + '\\' + file, engine = 'c', sep=',')

    # Initialize geometry with first file
    if is_firstfile:
        # Points along axes
        x = np.array(ansys[r'    x-coordinate'])
        y = np.array(ansys[r'    y-coordinate'])

        Pos = np.stack([x, y], 1)

        P_lin = np.expand_dims(np.array(ansys[r'        pressure']),0)
        U_lin = np.array(ansys[r'      x-velocity'])
        V_lin = np.array(ansys[r'      y-velocity'])

        Vels = np.expand_dims(np.stack([U_lin, V_lin], 1), 0)

        is_firstfile = False
    else:
        U_lin = np.array(ansys[r'      x-velocity'])
        V_lin = np.array(ansys[r'      y-velocity'])
        P_lin = np.concatenate((P_lin, np.expand_dims(np.array(ansys[r'        pressure']), 0)), 0)
        Vels = np.concatenate((Vels, np.expand_dims(np.stack([U_lin, V_lin], 1), 0)), 0)

    # Accumulate the timesteps
    t_n += 1
    t.append(t_n*DT)

Vels = np.transpose(Vels, (1,2,0))
P_lin = np.transpose(P_lin)
t = np.transpose(np.array([t]))


print(Vels.shape)
print(P_lin.shape)
print(t.shape)

filename = f"{filepath[2:]}.mat"
scipy.io.savemat(filename, {'U_star': Vels, 'p_star': P_lin, 'X_star': Pos, 't': t})