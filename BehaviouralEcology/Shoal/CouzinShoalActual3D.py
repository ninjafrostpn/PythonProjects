# Based on Couzin et al. (2002), but as a 2D simulation
from mpl_toolkits import mplot3d
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

boxedin = True
showfish = True
matplotlib.interactive(True)

# Interface initialisation
w = np.float32([200, 200, 200])
if showfish:
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    if boxedin:
        ax.set_xlim(0, w[0])
        ax.set_ylim(w[1], 0)
        ax.set_zlim(0, w[2])
    ax.invert_zaxis()
else:
    fig = plt.figure()
    ax1 = fig.add_subplot(2, 1, 1)
    ax2 = fig.add_subplot(2, 1, 2, sharex=ax1)
    plt.draw()

# Set simulation parameters
N = 100       # Number of fish
s = 10         # Speed of fish (px per time unit)
T = 0.1       # Timestep (time units per cycle)
alpha = 270   # Visual range of fish (degrees, centred on front of fish)
theta = 40    # Turning speed of fish (degrees per time unit)
sigma = 0.05  # Error
r_r = 2       # Outer radius of Zone of Repulsion
r_o_d = 4    # Width of Zone of Orientation
r_a_d = 28    # Width of Zone of Attraction

# The position vectors, c, and unit direction vectors, v, of the fish
c = np.random.random_sample((N, 3)) * w
while True:
    mask_c_bad = np.linalg.norm(c - w/2, axis=1) > r_a_d
    if np.any(mask_c_bad):
        c[mask_c_bad] = np.random.random_sample((np.sum(mask_c_bad), 3)) * w
    else:
        break
v = np.float32([np.sin([ang + np.pi/2, ang, ang - np.pi/2]) for ang in (np.random.random_sample(N) * (np.pi * 2))])
v = (v.T / np.linalg.norm(v, axis=1)).T  # Normalisation. There's a lot of this in this program.

# A pair of arrays, covering every possible non-self interaction combination
# - pairs[0] are used as the fish doing the detecting, generally called fish i
# - pairs[1] are used as the fish being detected, generally called fish j
pairs = np.nonzero(np.tri(N, dtype="bool") ^ ~np.tri(N, k=-1, dtype="bool"))

if showfish:
    # Select random colours
    colours = np.random.random_sample((N, 3))
    # Cater for weird render order of arrow parts
    colours = np.append(colours, [colours[int(i/2)] for i in range(N * 2)], axis=0)


T_total = 0
recording = False
r_o_d_records = []
p_group_records = []
m_group_records = []
print("Start Simulation")
print("Stabilisation start for", r_o_d)
while True:
    # The vector pointing from each fish i to each fish j
    r_ij = c[pairs[1]] - c[pairs[0]]         # Full vector
    r_ij_abs = np.linalg.norm(r_ij, axis=1)  # Distance
    r_ij_norm = (r_ij.T / r_ij_abs).T        # Normalised vector

    # The angle between the direction of travel for fish i and the line of sight from i to j
    ang_vis = np.arctan2(np.linalg.norm(np.cross(r_ij_norm, v[pairs[0]]).reshape(r_ij.shape[0], -1), axis=1),
                         np.einsum('ij, ij->i', r_ij_norm, v[pairs[0]]))
    # Mask (for the pair arrays) that singles out the pairings where fish i can see fish j
    # (einsum here takes the dot product of each pair of corresponding vectors very quickly)
    mask_visible = alpha / 2 > np.abs(ang_vis * (180 / np.pi))

    # Mask (for the pair arrays) that singles out the pairings where fish j is in fish i's zone of repulsion
    mask_zor = mask_visible & (r_ij_abs < r_r)

    # Generating the mask (for the pair arrays) that singles out fish i which have either:
    # - a tank wall in their repulsion zone (this is not in the model as per the paper)
    # - any fish in their repulsion zone
    mask_mode_r = np.zeros(r_ij_abs.shape, dtype="bool")
    if boxedin:
        # Masks (for the list of all fish i) that single out:
        mask_toplft = np.any(c < r_r, axis=1)      # those close to the top or left walls
        mask_btmrgt = np.any(c > w - r_r, axis=1)  # those close to the bottom or right walls
        # Fills in mask_mode_r with all the fish satisfying any of these conditions
        for i in set(pairs[0][mask_zor]):
            mask_mode_r |= (pairs[0] == i) | mask_toplft[pairs[0]] | mask_btmrgt[pairs[0]]
    else:
        for i in set(pairs[0][mask_zor]):
            mask_mode_r |= (pairs[0] == i)
    # Masks (for the pair arrays) that single out pairings where fish j is in fish i's
    mask_zoo = mask_visible & ~mask_mode_r & (r_ij_abs < r_r + r_o_d)                      # Zone of Orientation
    mask_zoa = mask_visible & ~mask_mode_r & ~mask_zoo & (r_ij_abs < r_r + r_o_d + r_a_d)  # Zone of Attraction

    # Generating the unit direction vectors representing the direction fish i would like to go
    d_i = np.zeros((N, 3))
    # Generating unit direction vectors for repulsion
    d_r = np.zeros((N, 3))
    d_r[pairs[0][mask_zor]] -= r_ij_norm[mask_zor]
    if boxedin:
        # (These must be redone separately to mask_topleft etc else the fish move on a certain diagonal away from walls)
        d_r[c < r_r] += 1
        d_r[c > w - r_r] -= 1
    d_r[pairs[0][mask_zor]] = (d_r[pairs[0][mask_zor]].T / np.linalg.norm(d_r[pairs[0][mask_zor]], axis=1)).T
    d_i += d_r
    # Generating unit direction vectors for orientation
    d_o = np.zeros((N, 3))
    d_o[pairs[0][mask_zoo]] += v[pairs[1][mask_zoo]]
    d_o[pairs[0][mask_zoo]] = (d_o[pairs[0][mask_zoo]].T / np.linalg.norm(d_o[pairs[0][mask_zoo]], axis=1)).T
    d_i += d_o
    # Generating unit direction vectors for orientation
    d_a = np.zeros((N, 3))
    d_a[pairs[0][mask_zoa]] += r_ij_norm[mask_zoa]
    d_a[pairs[0][mask_zoa]] = (d_a[pairs[0][mask_zoa]].T / np.linalg.norm(d_a[pairs[0][mask_zoa]], axis=1)).T
    d_i += d_a
    # Mask (for the list of all fish i) that singles out all the fish i with zero vectors as their intended direction
    mask_zeroes = np.all(d_i == 0, axis=1)
    # Setting zero vectors to be the same direction the fish is currently going
    d_i[mask_zeroes] = v[mask_zeroes]
    # Ensure normalisation of all of the intended direction vectors
    # (Takes care of fish i with fish in both their Zones of Orientation and Attraction)
    d_i = (d_i.T / np.linalg.norm(d_i, axis=1)).T

    # Introduce random variation, supposed to be a gaussian wrapped around a sphere, centred on d_i
    rand_turn1 = np.random.random_sample(N) * np.pi * 2  # Direction around the axis
    rand_turn2 = np.random.vonmises(0, sigma, N)         # Angle away from the axis, wrapped normal
    # Generate two vectors orthogonal to d_i and each other
    u1 = np.float32([d_i[:, 1], -d_i[:, 0], np.zeros(d_i.shape[0])]).T
    mask_fail = np.all(u1 == 0, axis=1)
    u1[mask_fail] = np.float32([d_i[mask_fail][:, 2], np.zeros(np.sum(mask_fail)), -d_i[mask_fail][:, 0]]).T
    u2 = np.cross(d_i, u1)
    # Generate random vector orthogonal to d_i
    d_perp = ((np.cos(rand_turn1) * u1.T) + (np.sin(rand_turn1) * u2.T)).T
    d_i_new = ((np.cos(rand_turn2 * (np.pi / 180)) * d_i.T) + (np.sin(rand_turn2 * (np.pi / 180)) * d_perp.T)).T
    d_i = (d_i_new.T / np.linalg.norm(d_i_new, axis=1)).T

    # The angle between each fish i's current and intended directions
    ang_turn = np.arctan2(np.linalg.norm(np.cross(v, d_i), axis=1), np.einsum('ij, ij->i', v, d_i))
    # Mask (for the list of all fish i) that singles out fish i who can cover their intended turn in one timestep
    mask_close = np.abs(ang_turn * (180/np.pi)) < theta * T
    # Turns said fish (but doesn't bother with fish who aren't turning at all)
    v[mask_close & ~mask_zeroes] = d_i[mask_close & ~mask_zeroes]
    # Current and new cardinal direction angle for fish i which can't cover their intended turn in one timestep
    d_perp = np.cross((np.cross(v[~mask_close & ~mask_zeroes],
                                d_i[~mask_close & ~mask_zeroes])),
                      v[~mask_close & ~mask_zeroes])
    mask_antiparallel = np.all(d_perp == 0, axis=1)
    if np.any(mask_antiparallel):
        u1 = np.float32([v[~mask_close & ~mask_zeroes][mask_antiparallel][:, 1],
                         -v[~mask_close & ~mask_zeroes][mask_antiparallel][:, 0],
                         np.zeros(np.sum(mask_antiparallel))]).T
        mask_fail = np.all(u1 == 0, axis=1)
        u1[mask_fail] = np.float32([v[~mask_close & ~mask_zeroes][mask_antiparallel][mask_fail][:, 2],
                                    np.zeros(np.sum(mask_fail)),
                                    -v[~mask_close & ~mask_zeroes][mask_antiparallel][mask_fail][:, 0]]).T
        u2 = np.cross(v[~mask_close & ~mask_zeroes][mask_antiparallel], u1)
        ang_rand = np.pi * 2 * np.random.random_sample(np.sum(mask_antiparallel))
        d_perp[mask_antiparallel] = ((np.cos(ang_rand) * u1.T) + (np.sin(ang_rand) * u2.T)).T
    d_perp = (d_perp.T / np.linalg.norm(d_perp, axis=1)).T
    v_new = (np.cos(theta * T * (np.pi / 180)) * v[~mask_close & ~mask_zeroes]) + \
            (np.sin(theta * T * (np.pi / 180)) * d_perp)
    # Turns these fish
    v[~mask_close & ~mask_zeroes] = v_new

    c += v * s * T  # Movement of all fish i in the direction of v at speed s over one timestep, T
    if boxedin:
        c = np.minimum(np.maximum(c, 0), w)  # But stop them at the screen edge

    T_total += T

    # Obtain shoal metrics
    c_group = np.average(c, axis=0)
    d_group = np.average(v, axis=0)
    p_group = np.linalg.norm(np.sum(v, axis=0)) / N
    r_ic = c - c_group
    m_group = np.linalg.norm(np.sum(np.cross(v, r_ic), axis=0)) / N

    # Drawing things
    if showfish:
        if not boxedin:
            r_max = np.max(np.abs(r_ic))
            top = c_group + r_max
            btm = c_group - r_max
            ax.set_xlim(btm[0], top[0])
            ax.set_ylim(top[1], btm[1])
            ax.set_zlim(btm[2], top[2])
        drawnarrows = ax.quiver(*c.T,
                                *v.T,
                                color=colours,
                                pivot="tip", length=min(w)/10, arrow_length_ratio=0.5)
        plt.draw()
        fig.canvas.flush_events()
        drawnarrows.remove()
    else:
        if T_total > 500:
            recording = not recording
            if recording:
                print("Recording start for", r_o_d)
                p_group_total = p_group
                m_group_total = m_group
            else:
                print("Recording stop for", r_o_d)
                print(r_o_d, p_group_total / T_total, m_group_total / T_total)
                r_o_d_records.append(r_o_d)
                p_group_records.append(p_group_total / T_total)
                m_group_records.append(m_group_total / T_total)
                scat1 = ax1.scatter(r_o_d_records, p_group_records)
                scat2 = ax2.scatter(r_o_d_records, m_group_records)
                plt.draw()
                fig.canvas.flush_events()
                scat1.remove()
                scat2.remove()
                r_o_d += 0.1
                r_o_d %= 5
                # Reset
                c = np.random.random_sample((N, 3)) * w
                while True:
                    mask_c_bad = np.linalg.norm(c - w / 2, axis=1) > r_a_d
                    print(sum(mask_c_bad))
                    if np.any(mask_c_bad):
                        c[mask_c_bad] = np.random.random_sample((np.sum(mask_c_bad), 3)) * w
                    else:
                        break
                v = np.float32([np.sin([ang + np.pi / 2, ang, ang - np.pi / 2]) for ang in
                                (np.random.random_sample(N) * (np.pi * 2))])
                v = (v.T / np.linalg.norm(v, axis=1)).T
                print("Stabilisation start for", r_o_d)
            T_total %= 500
        elif recording:
            p_group_total += p_group
            m_group_total += m_group
