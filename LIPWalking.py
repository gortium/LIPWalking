import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
import copy
import TrajectorySolver as ts
import scipy.optimize as opt
import ForwardKinematic as fk
import InverseKinematic as ik

class LIPWalking:

    def __init__(self):
        # PARARMS
        self.phaseTime = 2
        self.phase = "right"  # "right" for right foot supporting
        self.animStep = 0.1
        self.realTimeLimit = 20
        self.time = np.arange(0, self.realTimeLimit, self.animStep)
        self.walkHeight = 10
        self.lastPhaseShift = 0
        self.walkStep = 20

        # Initial foot position
        self.oldLeftFootPose = np.zeros((4, 4))
        self.oldLeftFootPose[0, 3] = -self.walkStep/2  # x = -10
        self.oldLeftFootPose[1, 3] = -10  # y = -10

        self.actualSteppingFootPose = copy.deepcopy(self.oldLeftFootPose)

        self.newLeftFootPose = copy.deepcopy(self.oldLeftFootPose)
        self.newLeftFootPose[0, 3] += self.walkStep  # x += 20

        self.oldRightFootPose = np.zeros((4, 4))
        self.oldRightFootPose[0, 3] = 0  # x = 0
        self.oldRightFootPose[1, 3] = 10  # y = 10

        self.newRightFootPose = copy.deepcopy(self.oldRightFootPose)

        self.footPoses = [self.oldLeftFootPose, self.oldRightFootPose, self.newLeftFootPose]

        # init CoM poses
        self.comPose = self.oldRightFootPose - self.oldLeftFootPose
        self.comPose[3, 3] = self.walkHeight

        self.generateNextPhase()


# Stepping foot trajectory

# IK for Stepping foot


# Draw graph
    def draw(self):

        # Create a figure and a 3D Axes
        fig = plt.figure()
        ax = Axes3D(fig)

        # Setting the axes properties
        ax.view_init(20, 220)

        #ax.set_xlim3d([-20.0, 20.0])
        ax.set_xlabel('X')

        ax.set_ylim3d([-20.0, 20.0])
        ax.set_ylabel('Y')

        ax.set_zlim3d([0.0, 20.0])
        ax.set_zlabel('Z')

        ax.set_title('LIP WALKING')

        #traj1X = np.arange(0, phaseTime, 0.001)
        #traj1y = posTrajPoly3v1(traj1X)

        self.footScats = [ax.scatter(pose[0, 3], pose[1, 3], 0, s=50, c="g") for pose in self.footPoses]
        self.comScats = [ax.scatter(self.comPose[0, 3], self.comPose[1, 3], self.walkHeight, s=100, c="r")]
        self.pendulumLine = ax.plot([self.oldRightFootPose[0, 3], self.comPose[0, 3]],
                                    [self.oldRightFootPose[1, 3], self.comPose[1, 3]],
                                    zs=[self.oldRightFootPose[3, 3], self.comPose[3, 3]], linewidth=4, linestyle="--", c="#FFFFFF")

        supFootX, supFootY = np.meshgrid([self.oldRightFootPose[0, 3] - 5.0,
                                    self.oldRightFootPose[0, 3] + 5.0],
                                   [self.oldRightFootPose[1, 3] - 2.5,
                                    self.oldRightFootPose[1, 3] + 2.5])
        self.supportingFootPlane = [ax.plot_surface(supFootX, supFootY, 0, color="g", alpha=0.5)]

        stepFootX, stepFootY = np.meshgrid([self.actualSteppingFootPose[0, 3] - 5.0,
                                    self.actualSteppingFootPose[0, 3] + 5.0],
                                   [self.actualSteppingFootPose[1, 3] - 2.5,
                                    self.actualSteppingFootPose[1, 3] + 2.5])
        self.steppingFootPlane = [ax.plot_surface(stepFootX, stepFootY, 0, color="g", alpha=0.3)]

        def animate(time):
            # EVERY PHASE SHIFT
            if self.updatePhase(time):
                self.footScats[0].remove()
                self.footScats.pop(0)
                self.footScats.append(ax.scatter(self.footPoses[-1][0, 3], self.footPoses[-1][1, 3], 0, s=50, c="g"))
                self.supportingFootPlane[0].remove()
                self.supportingFootPlane.pop(0)
                footX, footY = np.meshgrid([self.footPoses[-2][0, 3] - 5.0,
                                            self.footPoses[-2][0, 3] + 5.0],
                                           [self.footPoses[-2][1, 3] - 2.5,
                                            self.footPoses[-2][1, 3] + 2.5])
                self.supportingFootPlane.append(ax.plot_surface(footX, footY, 0, color="g", alpha=0.5))
                for scat in self.comScats:
                    scat.remove()
                self.comScats = []

            # EVERY ANIM FRAME
            self.steppingFootPlane[0].remove()
            self.steppingFootPlane.pop()
            stepFootX, stepFootY = np.meshgrid([self.actualSteppingFootPose[0, 3] - 5.0,
                                                self.actualSteppingFootPose[0, 3] + 5.0],
                                               [self.actualSteppingFootPose[1, 3] - 2.5,
                                                self.actualSteppingFootPose[1, 3] + 2.5])
            self.steppingFootPlane.append(ax.plot_surface(stepFootX, stepFootY, self.actualSteppingFootPose[3, 3], color="g", alpha=0.3))
            self.pendulumLine[0].remove()
            self.pendulumLine.pop(0)
            self.pendulumLine.extend(ax.plot([self.footPoses[-2][0, 3], self.comPose[0, 3]],
                                             [self.footPoses[-2][1, 3], self.comPose[1, 3]],
                                             zs=[self.footPoses[-2][3, 3], self.comPose[3, 3]],
                                             linewidth=4, linestyle="--",
                                             c="#000000"))

            self.comScats.append(ax.scatter(self.comPose[0, 3], self.comPose[1, 3], self.walkHeight, s=100, c="r"))
            ax.set_xlim3d([self.comPose[0, 3]-20, self.comPose[0, 3]+20])

            print(time)

        # Animate
        anim = animation.FuncAnimation(fig, animate, init_func=self.__init__, frames=self.time, interval=50, blit=False, repeat=True)

        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)

        anim.save('com.mp4', writer=writer)
        
        plt.show()


    def updatePhase(self, time):
        self.updateComPos(time)
        self.updateFootPos(time)
        if time - self.lastPhaseShift >= self.phaseTime:
            self.lastPhaseShift = time
            self.generateNextPhase()
            return True
        else:
            return False

    def updateFootPos(self, time):
        if self.phase == "right":
            self.actualSteppingFootPose[0, 3] = self.oldLeftFootPose[0, 3] + (time - self.lastPhaseShift) * (self.walkStep / 2) - (self.walkStep)
            self.actualSteppingFootPose[1, 3] = self.oldLeftFootPose[1, 3]
            if self.actualSteppingFootPose[0, 3] < self.oldRightFootPose[0, 3]:
                self.actualSteppingFootPose[3, 3] = self.firstfootTraj(time - self.lastPhaseShift)
            if self.actualSteppingFootPose[0, 3] > self.oldRightFootPose[0, 3]:
                self.actualSteppingFootPose[3, 3] = self.secfootTraj(time - self.lastPhaseShift - self.phaseTime/2)

        if self.phase == "left":
            self.actualSteppingFootPose[0, 3] = self.oldRightFootPose[0, 3] + (time - self.lastPhaseShift) * (self.walkStep / 2) - (self.walkStep)
            self.actualSteppingFootPose[1, 3] = self.oldRightFootPose[1, 3]
            if self.actualSteppingFootPose[0, 3] < self.oldLeftFootPose[0, 3]:
                self.actualSteppingFootPose[3, 3] = self.firstfootTraj(time - self.lastPhaseShift)
            if self.actualSteppingFootPose[0, 3] > self.oldLeftFootPose[0, 3]:
                self.actualSteppingFootPose[3, 3] = self.secfootTraj(time - self.lastPhaseShift - self.phaseTime/2)

    def updateComPos(self, time):
        self.comPose[0, 3] = time * (self.walkStep/4) + (self.walkStep/4)
        if self.phase == "right":
            if self.comPose[0, 3] < self.oldRightFootPose[0, 3]:
                self.comPose[1, 3] = self.firstComTraj(time - self.lastPhaseShift)
            if self.comPose[0, 3] > self.oldRightFootPose[0, 3]:
                self.comPose[1, 3] = self.secComTraj(time - self.lastPhaseShift - self.phaseTime/2)

        if self.phase == "left":
            if self.comPose[0, 3] < self.oldLeftFootPose[0, 3]:
                self.comPose[1, 3] = self.firstComTraj(time - self.lastPhaseShift)
            if self.comPose[0, 3] > self.oldLeftFootPose[0, 3]:
                self.comPose[1, 3] = self.secComTraj(time - self.lastPhaseShift - self.phaseTime/2)

    def generateNextPhase(self):

        self.computeNewFootPos()

        if self.phase == "left":
            self.firstComTraj, self.secComTraj = self.computeViaTraj(self.phaseTime / 2, self.phaseTime / 2,
                                                                   abs(self.oldLeftFootPose[1, 3]) - abs(self.oldRightFootPose[1, 3]),
                                                                        self.oldRightFootPose[1, 3],
                                                                   abs(self.newLeftFootPose[1, 3]) - abs(self.oldRightFootPose[1, 3]),
                                                                   20, -20)

            self.firstfootTraj, self.secfootTraj = self.computeViaTraj(self.phaseTime / 2, self.phaseTime / 2,
                                                                       self.oldRightFootPose[3, 3],
                                                                       self.walkHeight/4,
                                                                       self.newRightFootPose[3, 3],
                                                                       0, 0)
            self.phase = "right"

        elif self.phase == "right":
            self.firstComTraj, self.secComTraj = self.computeViaTraj(self.phaseTime / 2, self.phaseTime / 2,
                                                                   abs(self.oldLeftFootPose[1, 3]) - abs(self.oldRightFootPose[1, 3]),
                                                                        self.oldLeftFootPose[1, 3],
                                                                   abs(self.newLeftFootPose[1, 3]) - abs(self.oldRightFootPose[1, 3]),
                                                                   -20, 20)

            self.firstfootTraj, self.secfootTraj = self.computeViaTraj(self.phaseTime / 2, self.phaseTime / 2,
                                                                       self.oldLeftFootPose[3, 3],
                                                                       self.walkHeight/4,
                                                                       self.newLeftFootPose[3, 3],
                                                                       0, 0)

            self.phase = "left"


    def computeNewFootPos(self):
        if self.phase == "right":
            self.oldRightFootPose = self.newRightFootPose
            self.newRightFootPose[0, 3] += self.walkStep  # x += 20
            self.footPoses.append(self.newRightFootPose)
            self.footPoses.pop(0)

        elif self.phase == "left":
            self.oldLeftFootPose = self.newLeftFootPose
            self.newLeftFootPose[0, 3] += self.walkStep  # x += 20
            self.footPoses.append(self.newLeftFootPose)
            self.footPoses.pop(0)

    # CoM trajectory
    def computeViaTraj(self, tf1, tf2, posS, posV, posF, velS, velF):
        sol3v = opt.fsolve(ts.trajPoly3Via, np.array([1, 1, 1, 1, 1, 1, 1, 1]),
                           (tf1, tf2, posS, posV, posF, velS, velF))

        return np.poly1d(sol3v[:4]), np.poly1d(sol3v[4:8])


def main():
    lipwalker = LIPWalking()
    lipwalker.draw()

if __name__ == "__main__":
    main()
