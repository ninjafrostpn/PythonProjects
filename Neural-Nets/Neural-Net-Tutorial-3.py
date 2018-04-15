# https://www.youtube.com/watch?v=Ilg3gGewQ5U
import numpy as np


def sigmoidsquish(x):
    return 1 / (1 + np.exp(-x))


def costfunction(predicted, actual, deriv=False):
    if deriv:
        return 2 * (predicted - actual)
    return np.sum((predicted - actual) ** 2)


inputdata = np.float32([[0, 0],
                        [0, 1],
                        [1, 0],
                        [1, 1]])
outputdata = np.float32([[1, 1],
                         [1, 0],
                         [0, 1],
                         [0, 0]])


class NeuralNet:
    def __init__(self, sizes):
        self.sizes = sizes
        self.synno = len(sizes) - 1
        self.synweights = []
        self.synbiases = []
        for i in range(self.synno):
            self.synweights.append(2 * np.random.random((sizes[i], sizes[i + 1])) - 1)
            self.synbiases.append(2 * np.random.random(sizes[i + 1]) - 1)
    
    def forwardpropagate(self, inputdata):
        layer = inputdata.copy()
        layers = [layer]
        for i in range(self.synno):
            layer = sigmoidsquish(layer.dot(self.synweights[i]) + self.synbiases[i])
            layers.append(layer)
        return layers
    
    def backpropagate(self, inputdata, outputdata):
        prediction = self.forwardpropagate(inputdata)
        print(inputdata, "->", prediction[-1])
        print("Should be:", outputdata)
        cost = costfunction(prediction[-1], outputdata)
        print("How bad? {:.2} bad.".format(cost))
        nudges = -costfunction(prediction[-1], outputdata, True)
        for i in range(-1, -(self.synno + 1), -1):
            # print("Nudges required:", nudges)
            self.synbiases[i] += nudges
            newnudges = np.dot(self.synweights[i], nudges)
            self.synweights[i] += np.array([prediction[i-1]]).T.dot(np.array([nudges]))
            nudges = newnudges
            

N = NeuralNet((2, 20, 2))
for k in range(100):
    for p in range(len(inputdata)):
        N.backpropagate(inputdata[p], outputdata[p])
