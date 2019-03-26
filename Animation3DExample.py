# From https://stackoverflow.com/questions/5179589/continuous-3d-plotting-i-e-figure-update-using-python-matplotlib
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib


class plot3dClass(object):
    def __init__(self, systemSideLength, lowerCutoffLength):
        self.systemSideLength = systemSideLength
        self.lowerCutoffLength = lowerCutoffLength
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')

        rng = np.arange(0, self.systemSideLength, self.lowerCutoffLength)
        self.X, self.Y = np.meshgrid(rng, rng)

        heightR = np.zeros(self.X.shape)
        self.surf = self.ax.scatter(self.X, self.Y, heightR, c="#ff00ff")

    def drawNow(self, heightR):
        self.surf.remove()
        self.surf = self.ax.scatter(self.X, self.Y, heightR, c="#ff00ff")
        plt.draw()
        self.fig.canvas.flush_events()


matplotlib.interactive(True)

p = plot3dClass(5, 1)
while True:
    p.drawNow(np.random.random(p.X.shape))
