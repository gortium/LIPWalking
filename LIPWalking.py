import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
import copy
import TrajectorySolver as ts
import scipy.optimize as opt

# Transpose matrix lib ???
T = np.zeros((4, 4))

# Foot position


oldLeftFootPose = np.zeros((4, 4))
oldLeftFootPose[0, 3] = -10  # x = -10
oldLeftFootPose[1, 3] = -10  # y = -10

actualLeftFootPose = copy.deepcopy(oldLeftFootPose)

nextLeftFootPose = copy.deepcopy(oldLeftFootPose)
nextLeftFootPose[0, 3] += 40  # x += 20

oldRightFootPose = np.zeros((4, 4))
oldRightFootPose[0, 3] = 10  # x = 10
oldRightFootPose[1, 3] = 10  # y = 10

actualRightFootPose = copy.deepcopy(oldRightFootPose)

nextRightFootPose = copy.deepcopy(oldRightFootPose)
nextRightFootPose[0, 3] += 40  # x += 20

#def generateNextFootPos():

# CoM trajectory
tf1 = tf2 = 1
posS = 0
posV = 8
posF = 0
velS = 1
velF = 1
sol3v = opt.fsolve(ts.trajPoly3Via, (1, 1, 1, 1, 1, 1, 1, 1), (tf1, tf2, posS, posV, posF, velS, velF))
posTrajPoly3v1 = np.poly1d(sol3v[:4])
posTrajPoly3v2 = np.poly1d(sol3v[4:8])

# IK for supporting leg

# Stepping foot trajectory

# IK for Stepping foot

# Draw graph
def draw():

    # Create a figure and a 3D Axes
    fig = plt.figure()
    ax = Axes3D(fig)

    # Setting the axes properties
    ax.set_xlim3d([0.0, 1.0])
    ax.set_xlabel('X')

    ax.set_ylim3d([0.0, 1.0])
    ax.set_ylabel('Y')

    ax.set_zlim3d([0.0, 1.0])
    ax.set_zlabel('Z')

    ax.set_title('3D Test')

    orgX = np.array([oldRightFootPose[0,3],nextRightFootPose[0,3],
                   oldLeftFootPose[0, 3],nextLeftFootPose[0,3]])

    orgY = np.array([oldRightFootPose[1,3],nextRightFootPose[1,3],
                   oldLeftFootPose[1,3],nextLeftFootPose[1,3]])

    traj1X = np.arange(0, tf1, 0.001)
    traj1y = posTrajPoly3v1(traj1X)

    def init():
        #ax.scatter(orgX, orgY, marker='o', s=20, c="goldenrod", alpha=0.6)
        ax.plot(traj1X, traj1y, 10, marker='x', s=20, c="red", alpha=0.6)
        return fig,

    def animate(i):
        ax.view_init(elev=20., azim=i)
        return fig,

    # Animate
    anim = animation.FuncAnimation(fig, update_traj, 25, fargs=(data, lines),
                                   interval=50, blit=False)

    fig.show()

draw()
