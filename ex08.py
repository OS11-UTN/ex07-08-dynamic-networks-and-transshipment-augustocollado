import numpy as np
from scipy.optimize import linprog
from basic_utils import nn2na
import math

# parameters

# NN order: Plants, Stocks, Sales

NN = np.array([
    [0, 0, 0, 0, 0, 0,  1, 0, 1, 0,     0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0,  0, 1, 0, 1,     0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0,  1, 0, 1, 0,     0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0,  0, 1, 0, 1,     0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0,  1, 0, 1, 0,     0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0,  0, 1, 0, 1,     0, 0, 0, 0, 0, 0],
    
    [0, 0, 0, 0, 0, 0,  0, 0, 0, 0,     1, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0,  0, 0, 0, 0,     0, 1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 0,  0, 0, 0, 0,     1, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0,  0, 0, 0, 0,     0, 1, 0, 1, 0, 1],

    [0, 0, 0, 0, 0, 0,  0, 0, 0, 0,     0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0,  0, 0, 0, 0,     0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0,  0, 0, 0, 0,     0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0,  0, 0, 0, 0,     0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0,  0, 0, 0, 0,     0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0,  0, 0, 0, 0,     0, 0, 0, 0, 0, 0],
])

# order of the arcs should be the same as nn2na returns
arcs = np.array([
    'P1A-St1A', 'P1A-St2A', 'P1B-St1B', 'P1B-St2B', 
    'P2A-St1A', 'P2A-St2A', 'P2B-St1B', 'P2B-St2B', 
    'P3A-St1A', 'P3A-St2A', 'P3B-St1B', 'P3B-St2B',
    'St1A-S1A', 'St1A-S2A', 'St1A-S3A', 'St1B-S1B', 'St1B-S2B', 'St1B-S3B',
    'St2A-S1A', 'St2A-S2A', 'St2A-S3A', 'St2B-S1B', 'St2B-S2B', 'St2B-S3B', 
] )
Cost = np.array([
    100, 100, 200, 200, 
    150, 150, 150, 150, 
    200, 200, 100, 100, 
    100, 150, 200, 100, 150, 200,
    200, 150, 100, 200, 150, 100
]) 

BPlants = [
    20, 30, 10, 40, 30, 10,
    0, 0, 0, 0, 
    0, 0, 0, 0, 0, 0
]

BSales = [
    20, 30, 10, 40, 30, 10,
    0, 0, 0, 0, 
    -30, -40, -10, -20, -20, -20
]

# solution

NA = nn2na(NN)

# Lower equal restrictions: Plants
Bleq = np.array(BPlants)
Aleq = NA.copy()
Aleq[6:] = 0

# Equal restrictions: Sale points
Aeq = NA.copy()
#Aeq[:NN.shape[0] - 6] = 0
Beq = np.array(BSales)

bounds = tuple( [ (0, math.inf) for i in range (0, Aeq.shape[1]) ] )

result = linprog(Cost, A_eq = Aeq, b_eq = Beq, bounds=bounds, method='simplex' )

indexes = np.where(np.array(result.x) > 0.9)

print('Min Cost: %s' % (result.fun))

for i in indexes:
    print('%s: %s' % (arcs[i], result.x[i]))


