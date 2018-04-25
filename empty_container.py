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
supply_imp, supply_port = read_dat_file("./supply.dat")
num_imp = len(supply_imp)
num_port = len(supply_port)
print("Supply from", num_imp, "importer are:",supply_imp)
print("Supply from", num_port,"port are :",supply_port)

# Demand file
demand_exp, demand_port = read_dat_file("./demand.dat")
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

for i in range(len(owner_depot)):
    print(owner_depot[i])


# declaring cplex model
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
print("Fixed cost are:", fc * -1 )
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
print(num_N)


# Constraints: New facilities should remain open at the finish if opened at start
for i in range(len(num_N) / 2):
    y_N_start= y[num_N[i]]
    y_N_finish = y[num_N[i]+len(y_F)]
    rh = 0
    print(y_N_finish, y_N_start)
    model.linear_constraints.add(
        lin_expr=[cplex.SparsePair([y_N_finish , y_N_start], [1, -1])],
        senses=["G"], rhs=[rh], names=['NS']
    )



dist_exp_depot = read_dat_file("./OD_j_i.dat")
print(dist_exp_depot)
for j in range(0,2):
    for i in range(len(owner_depot)):
        print(j,i)
        print(dist_exp_depot[j][i])




x_imp_depot = []
x_imp_depot_all = []
cost_imp_depot = []
cost_imp_depot_all = []
# variable add 1: container vol from IMPORT to DEPOT\
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

for i in range(len(x_imp_depot_all)):
    print(x_imp_depot_all[i], cost_imp_depot_all[i])

model.variables.add(names=x_imp_depot_all,
                   obj=cost_imp_depot_all,
                   lb =[0] * len(x_imp_depot_all),
                   types = 'I' *  len(x_imp_depot_all)
                   )
# model.write("Check.lp")
#
# import webbrowser
# webbrowser.open("check.lp")