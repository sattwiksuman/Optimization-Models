# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 14:47:44 2019

@author: sattwik
"""

from gurobipy import *
model = Model("a vortex colouring problem")

#set of vertices:
v=[1,2,3,4,5]
#set of edges:
e=[[1,2],[1,3],[2,3],[2,4],[3,4],[4,5]]

C=["orange", "blue", "black", "yellow" ]

#for every vortex in an edge we need different colours: one binary variable x for each vortex colour pair
x={}
for i in v:
    x[i]={}
    for c in C:
        x[i][c]=model.addVar(vtype=GRB.BINARY)


for i in v:
    model.addConstr(quicksum(x[i][c] for c in C)==1)
    
        

for c in C:
    for edge in e:
        i=edge[0]
        j=edge[1]
        model.addConstr(x[i][c]+x[j][c] <= 1)
        
model.optimize()

for i in v:
    for c in C:
        if x[i][c].x>0:
            print("vertex"+str(i)+"_colour="+str(c))