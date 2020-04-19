import numpy as np

def nn2na(NN):

    indexes = np.argwhere(NN)

    NA = np.zeros([NN.shape[0], indexes.shape[0]]).astype(int)

    for i, arc in enumerate(indexes):
        NA[arc[0], i] = 1
        NA[arc[1], i] = -1

    return NA

