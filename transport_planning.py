# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 23:29:56 2020

@author: sattwik
"""

'''
QUESTION:
    A security company was hired to transport larger amounts of cash. The cash is printed in
    central banks i = 1, . . . , n and shall be transported to commercial banks j = 1, . . . , m. Every
    central bank i can print up to bi units of cash. Every commercial bank requires at least dj
    units of cash.
    The security company can now transport from every central bank i to every commercial bank
    j at most T units of cash. While transporting, there is a risk of a robbery. In order to minimize
    the loss in such a case, the banks want to distribute their money to all the connections (i, j)
    such that the maximum amount of transported cash on such a connection is minimized.
    Model this problem as an integer program, and explain the meaning of your variables and
    constraints.

INSTANCE OF PROBLEM SOLVED HERE:
    Central banks CB1, CB2 have capacities 16 and 12 units of cash
    Commercial banks CMB1, CMB2, CMB3, CMB4 have demands 9, 5, 8 and 6 units of cash respectively
    We have to find the MINIMUM units of cash that need to flow throw each cap so that the capacities and demand are satisfied

IDEA OF THE SOLUTION:
    We define the upper limit for cash flow through each of the arc joining a central bank and a commercial bank as a variable
    We then minimize this upper bound so that each arc has the minimum flow satisfying the capacity and demand constraints 
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
    variable T is an integer which is the upper bound on the number of units of cash flowing from Central bank to commercial bank through any arc joing them
'''

T = model.addVar(lb = 0, vtype='i', obj =1, name="min_flow")


'''
VARIABLE 2:
    variable x[i][j] is the number of units of cash flowing from Central bank i to commercial bank j
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
CONSTRAINT 3: UPPER LIMIT ON CASH
    units of cash on each arc from CB to CMB <= T
'''

model.addConstrs(
    (x[(i,j)] <= T for i in cb for j in cmb), "lower_bound")

'''
INVOKING THE OPTIMIZER:
'''

model.optimize()

'''
PRINTING THE SOLUTION:
'''

if model.status == GRB.OPTIMAL:
    print("\nRESULT:\n")
    for i in cb:
        for j in cmb:
            print(f"{x[(i,j)].x} units of cash is transferred from Central Bank {i} to Commercial Bank {j}")
else:
    print("\n\nRESULT:\nNo solution could be obtained for given preferences")
