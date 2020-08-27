# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 10:30:26 2019

@author: sattwik
"""

from gurobipy import *

model = Model("Matching Student of a Municipalty to appropriate Schools")

'''
QUESTION:
    We consider a county with a set I of municipalities, a set J of schools and a set K of class
    levels. Every school j ∈ J has a capacity of Cj,k pupils in the class level k ∈ K. For every
    municipality i ∈ I the number of pupils of class level k ∈ K are given as Si,k. Finally, the
    distance of municipality i ∈ I to school j ∈ J is di,j .
    We now want to decide how many pupils of which municipality and which class level should
    go to which school in order to minimize the total travel distance of all pupils.
    Model this problem as an integer program and explain the meaning of your variables and
    constraints.

INSTANCE OF PROBLEM USED FOR THE CODE:
    There are three municipalties: I=[I1, I2, I3]
    There are two Schools J=[J1, J2]
    There are three grades K=[K1, K2, K3]
    For School J1 and J2, all class capacities are Cjk = 30
    For each municipalty I, number of students per class Sik= 25
    Distance from Schools to Municipalty: 
              I1   I2   I3
          J1  15   10   12 
          J2  16   12   16
    We need to decide how many people from which municipalty go to which school such that distance covered in total is minimized
'''

#For the above question lets first define the arrays and constants that will define the problem for us

#Array of Municipalties:
I=['I1', 'I2', 'I3']

#Array of Schools:
J=['J1', 'J2']

#Array of classes:
K=['K1', 'K2', 'K3']

#Array of Class sizes per School: C[i][j] is the size for School (i+1) and Class (j+1):
C=[[38,38,38],[38,38,38]]

#Array that stores the students per class in each municipalty: rows are municipalty and columns are class:
S=[[25,25,25],[25,25,25],[25,25,25]]

#Array of Distances from Municipalty to Schools: Rows are schools and columns are municipalties
d=[[15,10,12], [16,12,16]]

#total number of students:
N=0
for s in range(len(S)):
    for t in range(len(S[s])):
        N=N+S[s][t]


#Defining the variable for Integer Linear Program:

'''
VARIABLE:
we define a variable for each student that decides whether 
student n belonging to municipalty i studying in class k
goes to school j or not
'''

x = {}
for n in range(N):
    x[n] = {}
    for i in range(len(I)):
        x[n][i]={}
        for k in range(len(K)):
            x[n][i][k] = {}
            for j in range(len(J)):
                x[n][i][k][j] = model.addVar(lb=0, ub=1, vtype='i', obj=d[j][i], name="Student"+str(n+1)+"_municipaltyI"+str(i+1)+"_classK"+str(k+1)+"_schoolJ"+str(j+1))
              

'''
CONSTRAINT 1:
    Every class Kk in School Jj has a capacity of Cjk = C[j][k]
'''

for j in range(len(J)):
    for k in range(len(K)):
        model.addConstr(quicksum(x[n][i][k][j] for i in range(len(I)) for n in range(N)) <=C[j][k], "ClassSize")
    
'''
CONSTRAINT 2:
    In every municipalty I[i] there are Sik = S[i][k] number of students in class K[k]
'''          

for i in range(len(I)):
    for k in range(len(K)):
        model.addConstr(quicksum(x[n][i][k][j] for j in range(len(J)) for n in range(N)) <=S[i][k], "MunicipalSize")
    
'''
CONSTRAINT 3:
    One student can only go to a particular class in a particular school  
'''

for n in range(N):
    model.addConstr(quicksum(x[n][i][k][j] for i in range(len(I)) for k in range(len(K)) for j in range(len(J))) ==1, "UniqueStudent")
    
model.optimize()

'''
for n in range(N):
     for i in range(len(I)):
        for k in range(len(K)):
            for j in range(len(J)):
                if x[n][i][k][j].x == 1:
                    print(f"student {n+1} belonging to Municipalty I{i+1} studying in class K{k+1} goes to school J{j+1}")
'''                

for i in range(len(I)):
    
    for k in range(len(K)):
        for j in range(len(J)):
            count=0
            for n in range(N):
                if x[n][i][k][j].x == 1:
                    count = count + 1
            if count>=1:
                print(f"{count} number of students from Municipalty I{i+1} studying in class K{k+1} go to school J{j+1}")
            