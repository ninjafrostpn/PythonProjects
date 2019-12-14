# Basic idea:
# Character moving around
# Display follows, pointing in a direction from a point near them
# Can draw out the environment sitting in the direction of the arrow toward the point
# Environment made up of pixel values representing the density of the material found there
# Lowest density is 1, 0 indicates absence of material
# (possibly negative numbers for places the environment is drawn to; might help calculation)
# Higher-density pixels can be drawn out into several lower ones
