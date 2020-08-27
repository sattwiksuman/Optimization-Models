# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 22:32:21 2020

@author: sattwik
"""

'''
QUESTION:
    We are given n data points j = 1, 2, . . . , n, data point j having coordinates (aj , bj ) in the
    plane. Moreover, we consider m possible centers i = 1, . . . , m, center i having coordinates
    (ci, di). The data shall be be grouped in up to k groups. To this end, we want to select up
    to k centers that represent the groups. Every data point shall be assigned to exactly one
    center, such that the maximum Euclidean distance between data points and assigned centers
    is minimized.
    Model this problem as a mixed-integer program (MIP), and explain the meaning of your
    variables and constraints.

INSTANCE OF THE PROBLEM:
    We are given 10 data points, dp->{P1, P2,...P10} and their coordinates dp_x, dp_y
    We are given 4 centres, cent->{C1, C2, C3, C4} and their coordinates cent_x, cent_y
    we have to select k=3 centres that group the ten points in such a way that
    the maximum distance between data points and the assigned centres is minimized.
    
IDEA OF SOLUTION:
    Define a continuous variable 'm' that sets an upperlimit on the arc distances.
    By minizing 'm' we can minimise the maximum distance between a datapoint and its associated centre
'''

'''
DEFINITION OF THE PROBLEM BY DEFINING ALL THE DATA:
'''

#importing Gurobipy and defining the model:

import math
from gurobipy import *
model = Model("K_centres")

#Defining the points and the centres along with their coordinates and the euclidian distances between each pair :

cent, cent_x, cent_y = gurobipy.multidict({'C1':[1.5, 2], 'C2':[2.5, 2], 'C3':[3.5, 2], 'C4':[3, 2.8]})    #Centres

dp, dp_x, dp_y= gurobipy.multidict({'P1':[1,1], 'P2':[1,2], 'P3':[1,3], 'P4':[2,1], 'P5': [2,2], 'P6':[2,3], 'P7':[3,1], 'P8':[3,2], 'P9':[3,3], 'P10':[2.5, 3.5]})    #Data Points

#Calculating the distances for each of the arcs:

dist_calc = {}

for i in cent:
    for j in dp:
        dist_calc[i, j] = math.sqrt((cent_x[i]-dp_x[j])**2+(cent_y[i]-dp_y[j])**2)
        
arc, d = gurobipy.multidict(dist_calc) #arc stores all the possible arcs between centres and data points; and d stores the corresponding distances

k=3     #3 out of the 4 possible centres need to be selected

'''
VARIABLES:
    1. x(i,j) is a binary variable which tells whether arc (i,j) joining centre i to data point j is selected
    2. y(i) is a binary variable which tells whether centre i is selected or not
    3. m is a continuous variable that sets a upper limit on the arc distances
'''

x = model.addVars(arc, obj=0, vtype='b', name="arc_select")

y = model.addVars(cent, obj=0, vtype='b', name="center_select")

m = model.addVar(lb=0, obj=1, vtype=GRB.CONTINUOUS, name="center_select")

'''
CONSTRAINT 1:
    k number of points among all the possible centre points are selected
    => sum of y(i) is k
'''

model.addConstr(
    (y.sum('*') == k), "k_centres")

'''
CONSTRAINT 2:
    For each data point only one associated centre has to be selected
    => sum of x(i,j) over i for each j =1
'''

model.addConstrs(
    (x.sum('*', j) == 1 for j in dp), "one_associated_centre")

'''
CONSTRAINT 3:
    If a centre i and an arc (i,j) are containing the center are selected, then the distance of the arc should be upper bounded by 'm'
    If x(i,j)==1, then , x(i,j)*d(i,j)<=m*y(i)
'''

model.addConstrs(
    (x[(i, j)]*d[i,j]<= m*y[i] for i in cent for j in dp), "distance")

'''
INVOKING THE OPTIMIZER:
'''

model.optimize()

'''
PRINTING THE SOLUTION:
'''
import matplotlib.pyplot as plt

if model.status == GRB.OPTIMAL:
    print("\nRESULT:\n")
    for i in cent:
        if y[i].x==1:
            plt.scatter(cent_x[i], cent_y[i], color='r', label='Centres')
            plt.annotate(i,(cent_x[i], cent_y[i]))
            for j in dp: 
                if x[(i,j)].x==1:
                    plt.scatter(dp_x[j], dp_y[j], color='g', label='Data Points')
                    plt.annotate(j,(dp_x[j], dp_y[j]))
                    plt.plot([cent_x[i], dp_x[j]],[cent_y[i], dp_y[j]])
                    print(f"{i} is joined to {j}")           
else:
    print("\n\nRESULT:\nNo solution could be obtained for given preferences")

#plt.legend()
plt.show()