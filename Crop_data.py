from Plotter import crop_geometry
import scipy
import numpy as np

inp = scipy.io.loadmat('APS360_Cyl2D_Lam_2.mat')

Ux_star_inp = np.array(inp['U_star'])[:,0,:]
Uy_star_inp = np.array(inp['U_star'])[:,1,:]
P_star_inp = np.array(inp['p_star'])
X_star_inp = np.array(inp['X_star'])
t = np.array(inp['t'])

# Bounds x, y of sampling region, in m (order of axis tuples matters, order of bounds in each axis doesn't matter)
bounds = ((8, 1),(2,-2))
timestart = 0
timestop = 201

Ux_star_crop, X_star_crop = crop_geometry(Ux_star_inp[...,timestart:timestop], X_star_inp, bounds[0], bounds[1])
Uy_star_crop, X_star_crop = crop_geometry(Uy_star_inp[...,timestart:timestop], X_star_inp, bounds[0], bounds[1])
P_star_crop, X_star_crop = crop_geometry(P_star_inp[...,timestart:timestop], X_star_inp, bounds[0], bounds[1])
t = np.expand_dims(np.arange(0, timestop-timestart), 1)
Vels = np.stack([Ux_star_crop, Uy_star_crop], 1)

scipy.io.savemat('Test_APS360_Cyl2D_Lam_2.mat', {'U_star': Vels, 'p_star': P_star_crop, 'X_star': X_star_crop, 't': t})