import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.interactive(True)


# Actor\Other  Cooperate Defect
#              _________ ______
#             |         |      |
# Cooperate   |    R    |  S   |
#             |---------|------|
# Defect      |    T    |  P   |
#             |_________|______|

# Values designate benefits to the actor
R = 3  # If both cooperate
S = 0  # If the actor cooperates and its partner defects
T = 5  # If the actor defects and its partner cooperates
P = 1  # If both defect


def normalise(vec):
    d = np.linalg.norm(vec, axis=-1)
    retvec = np.zeros(vec.shape)
    mask = (d != 0)
    retvec[mask] = (vec[mask].T / d[mask]).T
    return retvec


fig, ax = plt.subplots()

lft, top, rgt, btm = 0, 100, 100, 0
w, h = rgt - lft, top - btm
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

# The sampled x and y coordinates
samplex = np.linspace(lft, rgt, 25, dtype="float32")
sampley = np.linspace(top, btm, 25, dtype="float32")
# Arrays of corresponding x and y coordinates populating a full grid
samplexx, sampleyy = np.meshgrid(samplex, sampley)

N = 100
tracerpos = (np.random.random_sample([N, 2]) * (w, h)) + (lft, btm)


# x for defectors, y for cooperators
def field(xxin, yyin):
    population = xxin + yyin
    dfctprop = xxin / population
    coopprop = yyin / population
    return np.float32([xxin * ((dfctprop * P) + (coopprop * T)),
                       yyin * ((dfctprop * S) + (coopprop * R))])


tstep = 0.0001
while True:
    points = ax.scatter(*(tracerpos.T / np.sum(tracerpos, axis=-1)), color="R", s=30, marker="*")
    samplepop = samplexx + sampleyy
    arrows = ax.quiver(samplexx / samplepop, sampleyy / samplepop,
                       *(field(samplexx, sampleyy) / samplepop))  # The inputs X, Y, U, V appear to be flattened
    plt.draw()
    fig.canvas.flush_events()
    points.remove()
    arrows.remove()
    for i in range(100):
        tracerpos += field(*tracerpos.T).T * tstep
