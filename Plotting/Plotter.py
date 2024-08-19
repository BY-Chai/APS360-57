from matplotlib import pyplot as plt
import matplotlib.animation as animation
import scipy
import numpy as np

#WIP
def plot_csv_series(path, title): # UNUSABLE
    pass
    plt.title("Losses")
    plt.plot(range(0,len(losses)), losses)
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend(loc='best')
    plt.show()

def crop_geometry(data, data_coords, x_bounds: tuple, y_bounds: tuple):
    # Crop y-axis
    y_mask = np.where((data_coords[:,1] <= min(y_bounds)) | (data_coords[:,1] >= max(y_bounds)))
    data = np.delete(data, y_mask[0], axis=0)
    data_coords = np.delete(data_coords, y_mask[0], axis=0)

    # Crop x-axis
    x_mask = np.where((data_coords[:,0] <= min(x_bounds)) | (data_coords[:,0] >= max(x_bounds)))
    data = np.delete(data, x_mask[0], axis=0)
    data_coords = np.delete(data_coords, x_mask[0], axis=0)
    return data, data_coords


def plot_contour(data, geometry, timestep, ax=None): # UNUSABLE
    if ax is None:
        fig, ax = plt.subplots()
    contour = ax.tricontourf(geometry[:,0], geometry[:,1], data[:,0,timestep], cmap='jet')
    ax.set_xlabel(r'$x$')
    ax.set_ylabel(r'$y$')
    ax.title.set_text(r'$p(x,\; y, \; t)$')
    ax.set_aspect('equal')
    if ax is None:
        plt.colorbar(contour, ax=ax)
        plt.show()
    return contour


def plot_scatter(data, geometry, timestep, ax=None):
    if ax is None:
        fig, ax = plt.subplots()
    scatter = ax.scatter(x=geometry[:,0], y=geometry[:,1], c=data[...,timestep], cmap='jet')
    ax.set_xlabel(r'$x$')
    ax.set_ylabel(r'$y$')
    ax.title.set_text(r'$p(x,\; y, \; t)$')
    ax.set_aspect('equal')
    plt.colorbar(scatter, ax=ax)
    if ax is None:
        plt.show()
    return scatter

def animator(data, geometry, start_time, gif_path=None):
    data = data[..., start_time:]
    fig, ax = plt.subplots()

    scatter = plot_scatter(data, geometry, 0, ax)
    
    def init_animate():
        return scatter,

    def animate(i):
        scatter.set_array(data[...,i])
        ax.title.set_text(fr'V(x, y, t = {start_time+i})')
        return scatter,

    ani = animation.FuncAnimation(fig, animate, init_func=init_animate, frames=data.shape[-1], interval=1000, blit=True)
    if gif_path:
        writer = animation.PillowWriter(fps=15,metadata=dict(artist='Me'),bitrate=1000)
        ani.save(gif_path, writer=writer)
    plt.show()
    return ani


##### Define custom error functions
def error_abs(data1, data2):
    return data1 - data2



##### To be configured
# Files
pred1 = scipy.io.loadmat('./Results/run_skip_cylinder_wake (0-140).mat')
pred2 = scipy.io.loadmat('./Results/run_skip_cylinder_wake (140-200).mat')
truth = scipy.io.loadmat('./Data/Cleaned_APS360_0012_dt0001_2.mat')

#NACApred = scipy.io.loadmat('./Results/run_Cleaned_APS360_0012_dt0001_2.mat')


U_star = np.array(pred1['U_star'])
X_star = np.array(pred1['X_star'])
P_star = np.array(pred1['p_star'])

U_star2 = np.array(pred2['U_star'])
P_star2 = np.array(pred2['p_star'])


U_star = np.concatenate((U_star, U_star2), axis=2)
P_star = np.concatenate((P_star, P_star2), axis=1)

U_truth = np.array(truth['U_star'])
X_truth = np.array(truth['X_star'])
P_truth = np.array(truth['p_star'])


#U_err = U_star - U_truth
#P_err = P_star - P_truth

#animator(U_err[:,0,:], X_star, 0, './Figures/cylskip_Uerr (0-200).gif')
animator(U_truth[:,1,:], X_truth, 0, './Figures/APS360_0012_dt0001_2_V.gif')
#animator(P_err, X_star, 0, './Figures/cylskip_Perr (0-200).gif')