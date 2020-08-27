# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 15:32:31 2019

@author: sattwik
"""

from gurobipy import *
model = Model("knapsack")

items=[4,17,10,9,6,7,8]
profits=[10,14,3,16,7,3,6]




b=27


x={}

for i in range(len(items)):
    x[i]=model.addVar(vtype='b', obj=profits[i])     #objective function; obj=coeff of the variable

model.ModelSense= -1 #maximise objective function


model.addConstr(quicksum(items[i]*x[i] for i in range(len(items)))<=b)

model.optimize()


profit=0

for i in range(len(items)):
    if x[i].x>0:
        print(f"item {i} moves into knapsack")
        profit = profit + profits[i]
 
print(profit)