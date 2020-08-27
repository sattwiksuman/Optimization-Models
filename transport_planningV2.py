# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 10:38:48 2020

@author: sattwik
"""

'''
QUESTION:
    A security company was hired to transport larger amounts of cash. The cash is printed in
    central banks i = 1, . . . , n and shall be transported to commercial banks j = 1, . . . , m. Every
    central bank i can print up to bi units of cash. Every commercial bank requires at least dj
    units of cash.
    The security company can wants to minimize the number of used connections (i, j)

INSTANCE OF PROBLEM SOLVED HERE:
    Central banks CB1, CB2 have capacities 16 and 12 units of cash
    Commercial banks CMB1, CMB2, CMB3, CMB4 have demands 9, 5, 8 and 6 units of cash respectively
    We have to find the MINIMUM no. of arcs joing Central banks and Commercial Banks such that
    the capacities and demand requirements are satisfied.

IDEA OF THE SOLUTION:
    Along with the (integer) variable that stored the amount of flow through each arc we also have
    another (binary) variable that tells whether the arc is used or not. 
    We then minimize the sum of this binary variable. 
'''

'''
DEFINITION OF THE PROBLEM BY DEFINING ALL THE DATA:
'''

#importing Gurobipy and defining the model:

from gurobipy import *
model = Model("Banks")

#Defining the banks:

cb, cb_cap = gurobipy.multidict({'cb1':16, 'cb2':12})    #Central Banks and their capacities are defined in this dictionary

cmb, cmb_cap = gurobipy.multidict({'cmb1':9, 'cmb2':5, 'cmb3':8, 'cmb4':6})     #Commercial Banks and their demands are defined in this dictionary

'''
VARIABLE 1:
    variable y(i,j) is an binary variable which tells whether the arc from Central bank i to commercial bank j is used or not
'''

y = model.addVars(cb, cmb, obj=1, lb=0, ub=1, vtype='i', name="active")

'''
VARIABLE 2:
    variable x(i,j) is the number of units of cash flowing from Central bank i to commercial bank j
'''

x = model.addVars(cb, cmb, lb = 0, obj=0, vtype='i', name="cash_flow")

'''
CONSTRAINT 1: CENTAL BANK CAPACITY
    sum of units of cash on all arcs starting from CBi <= capacity of CBi
'''

model.addConstrs(
    (x.sum(i, '*') <= cb_cap[i] for i in cb), "cb_cap")

'''
CONSTRAINT 2: COMMERCIAL BANK CAPACITY
    sum of units of cash on all arcs reaching CMBi >= demand of CMBi
'''

model.addConstrs(
    (x.sum('*', j) >= cmb_cap[j] for j in cmb), "cmb_cap")

'''
CONSTRAINT 3: ACTIVITY CONSTRAINT
    if arc from CBi to CMBj is active only then x(i,j) is counted  
'''
M=max(cb_cap[i] for i in cb)    #M can be any sufficiently large number. In this case it has been chosen as the max capacity of central banks

model.addConstrs(
    (x[(i,j)] <= y[(i,j)]*M for i in cb for j in cmb), "activity_constraint")

'''
INVOKING THE OPTIMIZER:
'''

model.optimize()

'''
PRINTING THE SOLUTION:
'''
counter = 0
if model.status == GRB.OPTIMAL:
    print("\nRESULT:\n")
    for i in cb:
        for j in cmb:
            if y[(i,j)].x==1:
                print(f"{x[(i,j)].x} units of cash is transferred from {i} to {j}")
                counter=counter+1
            else: print(f"Arc joining {i} and {j} is inactive")
    print(f"\nNumber of arcs used = {counter}")
else:
    print("\n\nRESULT:\nNo solution could be obtained for given preferences")

