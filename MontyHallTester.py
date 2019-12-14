import numpy as np

# First choice has:
# - a 2/3 chance of being a goat, 0
# - a 1/3 chance of being a car, 1
# One goat revealed and effectively removed after choice made, now:
# - if it is a goat, 0, then:
#   - a stay, 0, will result in a goat
#   - a swap, 1, will result in a car
# - if it is a car,  1, then:
#   - a stay, 0, will result in a car
#   - a swap, 1, will result in a goat
# Every assortment tested, separated by swap vs stay
first = np.tile(np.repeat([0, 1], [2, 1]), 2)
swap = np.repeat([0, 1], 3)
result = (first + swap) % 2
print("Stay Victory: {}% chance\nSwap Victory: {}% chance".format(100 * sum(result[:3])/3, 100 * sum(result[3:])/3))
