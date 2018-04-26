from __future__ import print_function
import sys
import cplex
from cplex.exceptions import CplexError
from inputdata import read_dat_file
import numpy as np
import re

#_______________________________________________________________________________________
# Notations
#--------------------
# i: depot
# j: importer
# k: exporter
# h: port
# l: ocean carrier
# d: depot owner
# t: time period

#_______________________________________________________________________________________
# Inputs
#--------------------
# depot_status: [d][i][status]; if the status == 1, the depot is existing for that time period
#               this file needs updating
# owner_depot_FC_: [d][i][Fixed Cost]; fixed cost for opening new depot; All existing depot FC is
#                   set to zero ('0')
# owner_depot_CAP_: [d][i][Capacity]; Capacity of the existing and new depot
# OD_from_to : distances from and to locations
# demand : [h][k]; demand of EC of port and exporter
# supply: [h][j]; supply of EC from port and importer

#_______________________________________________________________________________________
# Read the data files
#--------------------

# Supply file
supply_imp = read_dat_file("./supply_imp.dat")
supply_port = read_dat_file("./supply_port.dat")
num_imp = len(supply_imp)
num_port = len(supply_port)
print("Supply from", num_imp, "importer are:",supply_imp)
print("Supply from", num_port,"port are :",supply_port)

# Demand file
demand_exp = read_dat_file("./demand_exp.dat")
demand_port = read_dat_file("./demand_port.dat")
num_exp = len(demand_exp)
num_port = len(supply_port)
print("Demand of", num_exp, "exporter are:",demand_exp)
print("Demand of", num_port,"port are :",demand_port)

# depot file
depot, owner, status, cap = read_dat_file("./depot_status_start.dat")
num_depot = len(depot)
num_owner = len(set(owner))
print("Number of Depot: ", num_depot, "Names are: ", depot)
print("Number of owner: ", num_owner, "Names are: ", set(owner))
# make owner and depot pairs
owner_depot = zip(owner, depot)
print(owner_depot)

# for i in range(len(owner_depot)):
#     print(owner_depot[i])

#_______________________________________________________________________________________
# declaring cplex model
#--------------------

model = cplex.Cplex()

# create lists of binary variables for depot status at the start (y_S) and
# at the finish (y_F) of the time period

# status of facility at the start of the time period y_S
# status of facility at the finish of the time perido, y_F
y_S= []
y_F= []
for loop in range(0,2):
    for rec in range(len(status)):
        # print(depot[rec])
        # print(owner[rec])
        # print(status[rec])
        if loop == 0:
            if status[rec] == 1:
                y_S.append('y_owner_' + str(owner[rec]) + '_depot_' + str(depot[rec])+ '_ES')
            else:
                y_S.append('y_owner_' + str(owner[rec]) + '_depot_' + str(depot[rec])+ '_NS')
        if loop == 1:
            if status[rec] == 1:
                y_F.append('y_owner_' + str(owner[rec]) + '_depot_' + str(depot[rec])+ '_EF')
            else:
                y_F.append('y_owner_' + str(owner[rec]) + '_depot_' + str(depot[rec])+ '_NF')

# status of all the facility in the time period, y
y = y_S + y_F
# print(y_S)
# print(y_F)
# fixed cost for the depots are the coefficients for depot status
fc_owner, fc_depot, fc = read_dat_file("./owner_depot_FC_t1.dat")
# print("Fixed cost are:", fc * -1 )
# adding binary variable to the objective function with fixed cost as coefficient
model.variables.add(names= y_S,
                   obj= [-1*x for x in fc],
                   lb= [0] * len(y_S),
                   ub= [1] * len(y_S),
                   types= ['B'] * len(y_S)
                   )
model.variables.add(names= y_F,
                   obj=  fc,
                   lb= [0] * len(y_F),
                   ub= [1] * len(y_F),
                   types= ['B'] * len(y_F)
                   )

# Constraints: All existing facilities are open in the time period
for y_index in range(len(y)):
    i_status = y[y_index]
    if re.search('[E]', i_status):
        rh = 1
        model.linear_constraints.add(
            lin_expr=[cplex.SparsePair([i_status], [1])],
            senses=["E"], rhs=[rh], names=['ES']
        )


# Get the index of new/potential depot in the all facility list "y"
num_N = []
for i in range(len(y)):
    i_status = y[i]
    if re.search('[N]', i_status):
        num_N.append(i)
# print(num_N)


# Constraints: New facilities should remain open at the finish if opened at start
for i in range(len(num_N) / 2):
    y_N_start= y[num_N[i]]
    y_N_finish = y[num_N[i]+len(y_F)]
    rh = 0
    # print(y_N_finish, y_N_start)
    model.linear_constraints.add(
        lin_expr=[cplex.SparsePair([y_N_finish , y_N_start], [1, -1])],
        senses=["G"], rhs=[rh], names=['NS']
    )


#_______________________________________________________________________________________
# Adding variable to objective function and constrains
#--------------------
# Adding variable to objective function
# variable 1 add: container vol from IMPORT to DEPOT (x_imp_depot)
x_imp_depot = []
x_imp_depot_all = []
# Coefficient of the variables are the cost = cost of trucking * distance between O-D
dist_exp_depot = read_dat_file("./OD_j_i.dat")
# print(dist_exp_depot)
cost_imp_depot = []
cost_imp_depot_all = []
# Assume, number of liner shipping company is 2
L = [0,1]
for l in range(len(L)):
    x_imp_depot.append([])
    cost_imp_depot.append([])
    for j in range(num_imp):
        x_imp_depot[l].append([])
        cost_imp_depot[l].append([])
        for i in range(len(owner_depot)):
            x_imp_depot[l][j].append("x_carr_" + str(l) + "_IMP_" + str(j) + "_depot_" + str(owner_depot[i]))
            x_imp_depot_all.append("x_carr_" + str(l) + "_IMP_" + str(j) + "_depot_" + str(owner_depot[i]))
            cost_imp_depot[l][j].append(dist_exp_depot[j][i])
            cost_imp_depot_all.append(dist_exp_depot[j][i])

# for i in range(len(x_imp_depot_all)):
#     print(x_imp_depot_all[i], cost_imp_depot_all[i])

model.variables.add(names=x_imp_depot_all,
                   obj=cost_imp_depot_all,
                   lb =[0] * len(x_imp_depot_all),
                   types = 'I' *  len(x_imp_depot_all)
                   )

# Adding contraints to the model
# Contraints Supply 1: total (sum of) number of EC container from importer to depot for each liner shipping company (x_carr_l_IMP_j_depot_(d, i))
# equals to the total supply from importer (S_j)
# Supply file: Supply of ocean carrier 'l's EC from importer j (S_j_l)
# Loading Supply file
S_j =  read_dat_file("./supply_imp.dat")
# print(S_j)

for l in range(len(L)):
    for j in range(num_imp):
        supply_constraint_1 = []
        for i in range(len(owner_depot)):
            # print("l = ",l,"j = ",j,"i = ",i)
            supply_constraint_1.append(x_imp_depot[l][j][i])
        rh = S_j[j][l]
    # print(supply_constraint_1, rh)
    model.linear_constraints.add(
        lin_expr = [cplex.SparsePair(supply_constraint_1, [1] * len(supply_constraint_1))],
        senses=["E"],
        rhs= [rh],
        names= ['supply_IMP_' + str(j)+'_carr_' + str(l)]
    )


#_______________________________________________________________________________________
# Adding variable to objective function and constrains
#--------------------
# variable 2 add: container vol from port to DEPOT (x_port_depot)
x_port_depot = []
x_port_depot_all = []
# Coefficient of the variables are the cost = cost of trucking * distance between O-D
dist_port_depot = read_dat_file("./OD_h_i.dat")
# print(dist_port_depot[0])
cost_port_depot = []
cost_port_depot_all = []
# Assume, number of liner shipping company is 2
L = [0,1]
for l in range(len(L)):
    x_port_depot.append([])
    cost_port_depot.append([])
    for h in range(num_port):
        x_port_depot[l].append([])
        cost_port_depot[l].append([])
        for i in range(len(owner_depot)):
            x_port_depot[l][h].append("x_carr_" + str(l) + "_PORT_" + str(h) + "_depot_" + str(owner_depot[i]))
            x_port_depot_all.append("x_carr_" + str(l) + "_PORT_" + str(h) + "_depot_" + str(owner_depot[i]))
            cost_port_depot[l][h].append(dist_port_depot[h][i])
            cost_port_depot_all.append(dist_port_depot[h][i])

# for i in range(len(x_imp_depot_all)):
#     print(x_port_depot_all[i], cost_port_depot_all[i])
model.variables.add(names=x_port_depot_all,
                   obj=cost_port_depot_all,
                   lb =[0] * len(x_port_depot_all),
                   types = 'I' *  len(x_port_depot_all)
                   )

# Adding contraints to the model
# Contraints Supply 2: total (sum of) number of EC container from PORT to depot for each liner shipping company (x_carr_l_PORT_j_depot_(d, i))
# equals to the total supply from port (S_h)
# Supply file: Supply of ocean carrier 'l's EC from port h (S_h_l)
# Loading Supply file
S_h =  read_dat_file("./supply_port.dat")
# print(S_h)

for l in range(len(L)):
    for h in range(num_port):
        supply_constraint_2 = []
        for i in range(len(owner_depot)):
            # print("l = ",l,"j = ",j,"i = ",i)
            supply_constraint_2.append(x_port_depot[l][h][i])
        rh = S_h[h][l]
    # print(supply_constraint_2, rh)
    model.linear_constraints.add(
        lin_expr = [cplex.SparsePair(supply_constraint_2, [1] * len(supply_constraint_2))],
        senses=["E"],
        rhs= [rh],
        names= ['supply_PORT_' + str(j)+'_carr_' + str(l)]
    )
#_______________________________________________________________________________________
# Adding variable to objective function and constrains
#--------------------
# variable 3 add: container vol from DEPOT to EXPORTER (x_depot_exp)
x_depot_exp = []
x_depot_exp_all = []
# Coefficient of the variables are the cost = cost of trucking * distance between O-D
dist_depot_exp = read_dat_file("./OD_i_k.dat")
# print(dist_depot_exp)
cost_depot_exp = []
cost_depot_exp_all = []
# Assume, number of liner shipping company is 2
L = [0,1]
for l in range(len(L)):
    x_depot_exp.append([])
    cost_depot_exp.append([])
    for i in range(len(owner_depot)):
        x_depot_exp[l].append([])
        cost_depot_exp[l].append([])
        for k in range(num_exp):
            x_depot_exp[l][i].append("x_carr_" + str(l) + "_DEPOT_" + str(owner_depot[i]) + "_EXP_" + str(k))
            x_depot_exp_all.append("x_carr_" + str(l) + "_DEPOT_" + str(owner_depot[i]) + "_EXP_" + str(k))
            cost_depot_exp[l][i].append(dist_exp_depot[k][i])
            cost_depot_exp_all.append(dist_exp_depot[k][i])

# for i in range(len(x_depot_exp_all)):
#     print(x_depot_exp_all[i], cost_depot_exp_all[i])

model.variables.add(names = x_depot_exp_all,
                   obj=cost_depot_exp_all,
                   lb =[0] * len(x_depot_exp_all),
                   types = 'I' *  len(x_depot_exp_all)
                   )

# Adding contraints to the model
# Contraints Supply 1: total (sum of) number of EC container from importer to depot for each liner shipping company (x_carr_l_IMP_j_depot_(d, i))
# equals to the total supply from importer (S_j)
# Supply file: Supply of ocean carrier 'l's EC from importer j (S_j_l)
# Loading Supply file
D_k =  read_dat_file("./demand_exp.dat")
# print(D_k)
# print(x_depot_exp)


for l in range(len(L)):
    for k in range(num_exp):
        demand_constraint_1 = []
        for i in range(len(owner_depot)):
            # print("l = ",l,"j = ",j,"i = ",i)
            demand_constraint_1.append(x_depot_exp[l][i][k])
        rh = D_k[k][l]
        print(demand_constraint_1, rh)
        model.linear_constraints.add(
            lin_expr = [cplex.SparsePair(demand_constraint_1, [1] * len(demand_constraint_1))],
            senses=["E"],
            rhs= [rh],
            names= ['Demand_EXP_' + str(k)+'_carr_' + str(l)]
        )


model.write("Check.lp")

import webbrowser
webbrowser.open("check.lp")
