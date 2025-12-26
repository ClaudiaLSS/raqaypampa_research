#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 11:22:23 2024

@author: claudia
"""

import pulp
import math

# DATA
P = 7 # number of consumption points
Coord = [[74,34,0],[244,200,55],[195,428,85],[354,342,88],[392,356,94],[431,334,94],[495,272,95]] # point coordinates
L = [[0.0 for p in range(P)] for d in range(P)] # distance between points
for p in range(P):
  for d in range(P):
    L[p][d] = math.sqrt((Coord[p][0]-Coord[d][0])**2+(Coord[p][1]-Coord[d][1])**2+(Coord[p][2]-Coord[d][2])**2)
ED = [300,1000,300,300,1000,300,200] # energy demand
PD = [200,500,200,200,500,200,150] # power demand
AD = 3 # required autonomy
S = 3 # types of panels
ES = [217,326,434] # energy of panels
PS = [50,75,100] # power of panels
CS = [451,636,821] # cost of panels
Z = 3 # types of panel controllers
PZ = [50,75,100] # power of panel controllers
CZ = [67,81,95] # cost of panel controllers
A = 2 #
EA = [[95,445],[357,1460],[581,2135],[498,1889],[504,1913],[488,1856],[512,1926]]# energy of turbines
PA = [300,1200] # power of turbines
CA = [974,2737] # cost of turbines
R = 2 # types of turbine controllers
PR = [420,1440] # power of turbine controllers
CR = [165,285] # cost of turbine controllers
B = 2 # types of batteries
EB = [1500,3000] # capacity of batteries
CB = [225,325] # cost of batteries
I = 2 # types of inverters
PI = [300,1000] # power of inverters
CI = [377,1000] # cost of inverters
CC = 3 # cost of wires
CM = 50 # cost of meters
M = 10000000 # very high value

# VARIABLES
xs = pulp.LpVariable.dicts("Panels",(range(P),range(S)),0,None,pulp.LpInteger)
xz = pulp.LpVariable.dicts("Panel controllers",(range(P),range(Z)),0,None,pulp.LpInteger)
xa = pulp.LpVariable.dicts("Turbines",(range(P),range(A)),0,None,pulp.LpInteger)
xr = pulp.LpVariable.dicts("Turbine controllers",(range(P),range(R)),0,None,pulp.LpInteger)
xb = pulp.LpVariable.dicts("Batteries",(range(P),range(B)),0,None,pulp.LpInteger)
xi = pulp.LpVariable.dicts("Inverters",(range(P),range(I)),0,None,pulp.LpInteger)
fe = pulp.LpVariable.dicts("Eflow",(range(P),range(P)),0,None,pulp.LpContinuous)
fp = pulp.LpVariable.dicts("Pflow",(range(P),range(P)),0,None,pulp.LpContinuous)
xg = pulp.LpVariable.dicts("Generators",range(P),0,1,pulp.LpInteger)
xc = pulp.LpVariable.dicts("Lines",(range(P),range(P)),0,1,pulp.LpInteger)
xm = pulp.LpVariable.dicts("Meters",range(P),0,1,pulp.LpInteger)

# OBJECTIVE FUNCTION
model = pulp.LpProblem("System",pulp.LpMinimize)
model += pulp.lpSum(CA[a]*xa[p][a] for p in range(P) for a in range(A)) + pulp.lpSum(CR[r]*xr[p][r] for p in range(P) for r in range(R)) + pulp.lpSum(CS[s]*xs[p][s] for p in range(P) for s in range(S)) + pulp.lpSum(CZ[z]*xz[p][z] for p in range(P) for z in range(Z)) + pulp.lpSum(CB[b]*xb[p][b] for p in range(P) for b in range(B)) + pulp.lpSum(CI[i]*xi[p][i] for p in range(P) for i in range(I)) + pulp.lpSum(CM*xm[p] for p in range(P)) + pulp.lpSum(L[p][d]*CC*xc[p][d] for p in range(P) for d in range(P) if p!=d)

# CONSTRAINTS
for p in range(P):
  model += pulp.lpSum(xs[p][s] for s in range(S)) <= M*xg[p]
for p in range(P):
  model += pulp.lpSum(xa[p][a] for a in range(A)) + pulp.lpSum(xs[p][s] for s in range(S)) >= xg[p]
for p in range(P):
  model += pulp.lpSum(fe[q][p] for q in range(P) if q!=p) + pulp.lpSum(ES[s]*xs[p][s] for s in range(S)) + pulp.lpSum(EA[p][a]*xa[p][a] for a in range(A)) >= ED[p] + pulp.lpSum(fe[p][d] for d in range(P) if d!=p)
for p in range(P):
  model += pulp.lpSum(fp[q][p] for q in range(P) if q!=p) + pulp.lpSum(PI[i]*xi[p][i] for i in range(I)) >= PD[p] + pulp.lpSum(fp[p][d] for d in range(P) if d!=p)
for p in range(P):
  model += pulp.lpSum(EB[b]*xb[p][b] for b in range(B)) + M*(1-xg[p]) >= AD*(ED[p] + pulp.lpSum(fe[p][d] for d in range(P) if d!=p))
for p in range(P):
  for i in range(I):
    xi[p][i] <= M*xg[p]
for p in range(P):
  for d in range(P):
    if p!=d:
      model += fe[p][d] <= M*xc[p][d]
for p in range(P):
  for d in range(P):
    if p!=d:
      model += fp[p][d] <= M*xc[p][d]
for p in range(P):
  model += pulp.lpSum(xc[q][p] for q in range(P) if q!=p) + xg[p] <= 1
for p in range(P):
  model += pulp.lpSum(xa[p][a] for a in range(A)) <= M*xg[p]
for p in range(P):
  model += pulp.lpSum(PR[r]*xr[p][r] for r in range(R)) >= pulp.lpSum(PA[a]*xa[p][a] for a in range(A))
for p in range(P):
  model += pulp.lpSum(PZ[z]*xz[p][z] for z in range(Z)) >= pulp.lpSum(PS[s]*xs[p][s] for s in range(S))
for p in range(P):
  model += pulp.lpSum(xc[p][d] for d in range(P) if d!=p) <= M*xm[p]
for p in range(P):
  model += pulp.lpSum(xc[q][p] for q in range(P) if q!=p) <= xm[p]

solver = pulp.PULP_CBC_CMD(msg=True, warmStart=True)
model.solve(solver)

# PRINT RESULTS
print(model.objective.value())