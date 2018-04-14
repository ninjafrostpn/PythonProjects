# Based on https://iamtrask.github.io/2015/07/12/basic-python-network/

import numpy as np


# sigmoid function
def sigmoid(x, deriv=False):
    if deriv:
        # The derivative of the sigmoid function, for calculating direction/intensity of errors
        # Here, x is the output of the sigmoid function of the original x
        return x * (1 - x)
    # The sigmoid function returns higher values as closer to 1, lower as closer to 0
    # 1/(1+e^(-x))
    return 1 / (1 + np.exp(-x))


# input dataset. Each row is a training example giving values for each of the 3 inputs
inputdata = np.array([[0, 0, 1],
                      [0, 1, 1],
                      [1, 0, 1],
                      [1, 1, 1]])

# output dataset. Each row is a training example giving a value for each of the 1 (...) outputs
outputdata = np.array([[0],
                       [0],
                       [1],
                       [1]])

# seed random numbers to make calculation
# deterministic (just a good practice)
np.random.seed(1)

# initialize weights randomly with mean 0
syn0 = 2 * np.random.random((3, 1)) - 1

for iter in range(10000):
    # forward propagation
    layer0 = inputdata
    layer1 = sigmoid(np.dot(layer0, syn0))
    print(layer1)
    
    # how much did we miss?
    layer1_error = outputdata - layer1
    
    # multiply how much we missed by the
    # slope of the sigmoid at the values in l1
    layer1_delta = layer1_error * sigmoid(layer1, True)
    
    # update weights
    syn0 += np.dot(layer0.T, layer1_delta)

print("Output After Training:")
print(layer1)
