# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 15:13:55 2019

@author: sattwik
"""

from gurobipy import *


model = Model("MIN_BINS")

items=[4,17,10,9,6,7,8] #We have 7 items with capacity as stored in the array
bins=[25,20,30,27,15]   #We have say total of 5 bins in the warehouse each with capacity 25units

#We need to compute minimum number of bins required to store all the bins and which items are stored together

#formulating variables

y={}
x={}

for j in range(len(bins)):
        y[j]=model.addVar(vtype='b', obj=1.0)   #whether bin j is used or not

for i in range(len(items)):
    x[i]={}
    for j in range(len(bins)):
        x[i][j]=model.addVar(vtype='b', obj=0.0)  #whether item i is in bin j
   
'''
for j in range(len(bins)):
    model.addConstr(quicksum(items[i]*x[i][j] for i in range(len(items))) <= bins[j])  #capacity of bin constraint
'''
    
for i in range(len(items)):
    model.addConstr(quicksum(x[i][j] for j in range(len(bins)))==1) #items are not repeated
   
for j in range(len(bins)):
    model.addConstr(quicksum(items[i]*x[i][j] for i in range(len(items))) <= bins[j]*y[j])  #capacity of bins if bins are open
    
    
model.optimize()

no_bins=0

for j in range(len(bins)):
    counter=0
    for i in range(len(items)):
        if x[i][j].x==1:
            print(f"item {i+1} is in bin {j+1}")
            counter+=1
    if counter>=1:
        no_bins+=1

print(f"Minimum number of bins used = {no_bins}")

