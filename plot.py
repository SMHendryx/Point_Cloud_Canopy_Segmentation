import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_3d(x, y, z, color, title):
    """Plot a set of 3D points.

    x: numpy array, (N)
    y: numpy array, (N)
    z: numpy array, (N)
    color: numpy array, (N)
    title: string
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    indices = np.argsort(z)
    x = x[indices]
    y = y[indices]
    z = z[indices]
    color = color[indices]

    ax.scatter(x, y, z, c=color, alpha=1)

    min_x, max_x = x.min(), x.max()
    min_y, max_y = y.min(), y.max()
    min_z, max_z = z.min(), z.max()
    max_range = np.max([max_x - min_x, max_y - min_y, max_z - min_z])

    mid_x = (min_x + max_x) / 2.0
    mid_y = (min_y + max_y) / 2.0
    mid_z = (min_z + max_z) / 2.0

    ax.set_xlim(mid_x - max_range / 2.0, mid_x + max_range / 2.0)
    ax.set_ylim(mid_y - max_range / 2.0, mid_y + max_range / 2.0)
    ax.set_zlim(mid_z - max_range / 2.0, mid_z + max_range / 2.0)

    plt.title(title)
    plt.show()


def plot_height(pts, title):
    """Plot a set of 3D points color coded by height.

    pts: numpy array, (N x 3)
    title: string
    """
    plot_3d(pts[:, 0], pts[:, 1], pts[:, 2], pts[:, 2], title)

def plot_color(pts, color, title):
    """Plot a set of 3D points color coded by an array of values.
    Color values will be automatically scaled to fit.

    pts: numpy array, (N x 3)
    color: numpy array, (N)
    title: string
    """
    plot_3d(pts[:, 0], pts[:, 1], pts[:, 2], color, title)
