# -*- coding: utf-8 -*-
"""
Created on Wed Jan  1 20:39:21 2020

@author: sattwik
"""

'''

QUESTION:    
    We consider the problem of assigning students to courses with limited capacity. We are given
    n students, and each student i ∈ {1, . . . , n} wants to attend ai courses. Moreover, for each
    course j ∈ {1, . . . , m} we know the maximum number of students bj that may attend it.
    Finally, every student i also gave a preference ci,j for each course j, where smaller ci,j -values
    mean higher preferences. We now want to minimize the sum of all preferences (of studentcourse assignments), satisfying the constraints that every student is assigned to their requested
    number of courses and that the maximum course capacity is not exceeded.
    
    (a) Model this problem as an integer program, and briefly explain the meaning of your variables
        and constraints.
    (b) Since there might not exist a feasible assignment, the model shall now be modified to
        guarantee the existence of solution. To achieve this, not all students have to be assigned
        their requested number of courses. Instead, for each student a penalty cost of M shall be
        added to the objective for each course fewer than the requested number of courses.
        Extend your model from part (a) accordingly. You do not have to restate the model, but
        specify the required modifications instead. Explain all changes you make to your model.
    (c) Additionally, overbooking of courses shall be possible. For every course j we know a
        number dj ∈ Z+ of additional slots as well as penalty costs fj ∈ R+. The penalty costs fj
        have to be paid once as soon as at least one of the additional slots of course j is occupied.
        Extend your model from part (a) accordingly. You do not have to restate the model, but
        specify the required modifications instead. Explain all changes you make to your model.


INSTANCE OF PROBLEM USED FOR THE CODE:
    6 students and 3 courses.
    each student has to take 2 courses and the class size for each course is 4
    each students give a preference of 2 courses
    our program allocates courses to students satisfying student preference and batch sizes  
'''

import gurobipy as gp
from gurobipy import *

model = Model("student_to_courses")

students, stud_cap = gp.multidict({'stud1':2, 'stud2':2, 'stud3':2, 'stud4':2, 'stud5':2, 'stud6':2})

courses, course_cap = gp.multidict({'crs1':4, 'crs2':4, 'crs3':4})

courses, add_course_cap = gp.multidict({'crs1':2, 'crs2':2, 'crs3':2})  #for part 'c'

courses, add_course_cost = gp.multidict({'crs1':10, 'crs2':10, 'crs3':10})  #for part 'c'


#the dictionary with keys "arcs" and value "preference" defined below is of the form -> student, courses : preferences 

#This definition of arcs is for part 'a' of the Solution
#This definition can also be used for part 'c' in case we don't want to include the case of additing penalty costs to unpreferred courses.

'''
arcs, pref = gp.multidict({
        ('stud1', 'crs1'): 1,
        ('stud1', 'crs2'): 2,
        ('stud2', 'crs1'): 1,
        ('stud2', 'crs2'): 2,
        ('stud3', 'crs2'): 1,
        ('stud3', 'crs3'): 2,
        ('stud4', 'crs2'): 1,
        ('stud4', 'crs3'): 2,
        ('stud5', 'crs3'): 1,
        ('stud5', 'crs1'): 2,
        ('stud6', 'crs3'): 1,
        ('stud6', 'crs1'): 2,})
'''

#Below definition of arcs is for part 'b' of the solution 
#This arc definition can also be used for part 'c'

'''
This is implemented by adding a preference = a very large value 
for all subjects that the student has not preferred
M is assigned a large value (100 in this case)
'''

M=100
 
arcs, pref = gp.multidict({
        ('stud1', 'crs1'): 1,
        ('stud1', 'crs2'): 2,
        ('stud1', 'crs3'): M,
        ('stud2', 'crs1'): 1,
        ('stud2', 'crs2'): 2,
        ('stud2', 'crs3'): M,
        ('stud3', 'crs2'): 1,
        ('stud3', 'crs1'): 2,
        ('stud3', 'crs3'): M,
        ('stud4', 'crs3'): 1,
        ('stud4', 'crs1'): 2,
        ('stud4', 'crs2'): M,
        ('stud5', 'crs3'): 1,
        ('stud5', 'crs1'): 2,
        ('stud5', 'crs2'): M,
        ('stud6', 'crs2'): 1,
        ('stud6', 'crs3'): 2,
        ('stud6', 'crs1'): M,})



#the above tuples dictionary is of the form -> student, courses : preferences    

'''
VARIABLE 1:
    variable x[i] tells whether arc[i] is assigned or not 
'''
    
x = model.addVars(arcs, obj=pref, vtype='b', name="assign")

'''
VARIABLE 2:
    variable y[i] counts the number of additonal slots of course[i] that have been used
'''

y = model.addVars(courses, lb = 0, ub= add_course_cap, obj=add_course_cost, vtype='i', name="add_counter")



'''
CONSTRAINT 1: STUDENT_CAP
    number of arc containing stud1 <=stud_cap('stud1')
'''

model.addConstrs(
    (x.sum(i, '*') == stud_cap[i] for i in students), "student_cap")


'''
CONSTRAINT 2: COURSE_CAP (THIS WAS USED FOR PART A AND B)
    number of arc containing crs1 <=course_cap('crs1')
'''

'''
model.addConstrs(
    (x.sum('*', i) <= course_cap[i] for i in courses), "course_cap")
'''



#FOR PART C FOLLOWING COURSE CAPACITY CONSTRAINT HAS TO BE USED (THIS CAN BE USED EVEN WHEN ARCS ARE DEFINED USING M PENALTY COSTS)
'''
CONSTRAINT 3: ADD_COURSE_CAPACITY
    number of arcs containing 'crs1'<=course_cap('crs1') + y['crs1]
'''

model.addConstrs(
    (x.sum('*', i) <= (course_cap[i] + y[i]) for i in courses), "add_course_cap")


#Run the optimization

model.optimize()


#Print the Solution:

if model.status == GRB.OPTIMAL:
    print("\nRESULT:")
    for j in courses:
        print(f"\nCourse {j} has following students:")
        for i in students:
            if (i,j) in arcs:
                if x[i,j].x==1:
                    print(f"    {i}")
else:
    print("\n\nRESULT:\nNo solution could be obtained for given preferences")
