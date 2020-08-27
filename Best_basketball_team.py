# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 09:57:48 2020

@author: sattwik
"""

'''
QUESTION:
    Given a table of 7 Players with attributes such as: Position and Rating in terms of Execution, Throwing, Jumping and Defence
    
    Furthermore, the given contraints are:
    • At least 2 players must be able to play Guard, at least 2 must be able to play Forward
    and at least one must be suitable for Center.
    • For every skill execution, throwing and jumping the chosen players must have an average
    score of at least 2.
    • Connor and Francis don’t like each other and hence must not be selected simultaneously.
    • Ethan only plays well if he can play together with his buddys Andy and Donald. Thus,
    if he is selected, the others must be selected, too.
    • Brayden and Connor are key players. Hence, at least one of them must be part of the
    team.
 OBJECTIVE: To select a team with 5 players that has maximum defensive rating
'''

from gurobipy import *

model = Model("Basketball_team")

players_data = {'Player':['Andy', 'Brayden', 'Connor', 'Donald', 'Ethan', 'Francis', 'Greg'],
        'Position':[['G'], ['C'], ['F', 'G'], ['C', 'F'], ['F', 'G'], ['C', 'F'], ['F', 'G']],
        'Execution':[1, 2, 2, 3, 3, 3, 3 ],
        'Throwing':[3, 1, 3, 3, 3, 1, 2 ],
        'Jumping':[3, 3, 2, 3, 1, 2, 2],
        'Defence':[1, 2, 2, 3, 3, 3, 2]}

index={}
n=0
for i in players_data['Player']:
    index[i]=n
    n=n+1

'''
VARIABLE 1:
    variable x[i] tells whether player[i] is selected or not 
'''
    
x={}
#x = model.addVars(players_data['Player'], obj=players_data['Defence'], vtype='b', name="assign")
for i in range(len(players_data['Player'])):
    x[i]=model.addVar(vtype='b', obj=players_data['Defence'][i])

'''
CONSTRAINT 1: TEAM_CAP
    number of players selected ==5
'''

model.addConstr(quicksum(x[i] for i in range(len(players_data['Player'])))==5)

'''
CONSTRAINT 2:
    At least 2 players must be able to play Guard, at least 2 must be able to play Forward
    and at least one must be suitable for Center.
'''

model.addConstr(quicksum(x[i] for i in range(len(players_data['Player'])) if 'G' in players_data['Position'][i] )>=2)

'''
CONSTRAINT 3:
    For every skill execution, throwing and jumping the chosen players must have an average
    score of at least 2.
'''

model.addConstr(quicksum(players_data['Throwing'][i]*x[i] for i in range(len(players_data['Player'])))>=10)

model.addConstr(quicksum(players_data['Jumping'][i]*x[i] for i in range(len(players_data['Player'])))>=10)

'''
CONSTRAINT 4:
    Connor and Francis don’t like each other and hence must not be selected simultaneously.
'''

model.addConstr(quicksum(x[i] for i in range(len(players_data['Player'])) if players_data['Player']=='Connor' or players_data['Player']=='Francis') <=1)

'''
CONSTRAINT 5:
    Ethan only plays well if he can play together with his buddys Andy and Donald. Thus,
    if he is selected, the others must be selected, too.
'''
#e=index['Ethan']
#a=index['Andy']
#d=index['Donald']

model.addConstr(x[index['Andy']]+x[index['Donald']]>= 1+ x[index['Ethan']])

'''
CONSTRAINT 6:
    Brayden and Connor are key players. Hence, at least one of them must be part of the
    team.
'''

model.addConstr(x[index['Brayden']]+x[index['Connor']]>= 1)

#INVOKING THE SOLVER TO CARRY OUT THE OPTIMIZATION:

model.ModelSense = -1 #for maximizing
model.optimize()


#PRINTING THE RESULTS:

total_throw=0
total_jump=0
total_def=0
if model.status == GRB.OPTIMAL:
    print("\nRESULT:\nPlayers selected in the team are:")
    for i in range(len(players_data['Player'])):
        if x[i].x==1:
            print(f"{players_data['Player'][i]}")
            total_throw = total_throw + players_data['Throwing'][i]
            total_jump = total_jump + players_data['Jumping'][i]
            total_def = total_def + players_data['Defence'][i]
    print(f"\nAverage Throwing points for the selected team = {total_throw/5}")
    print(f"\nAverage Jumping points for the selected team = {total_jump/5}")
    print(f"\nTotal Defence points for the selected team = {total_def}")
else:
    print("\n\nRESULT:\nNo solution could be obtained for given preferences")