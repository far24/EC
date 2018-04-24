from __future__ import print_function
import numpy as np
import re
import cplex



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


prob = cplex.Cplex()

# Creating variable for existing depot
# reading the initial status of the depot at the begining of the time period
depot_status = np.loadtxt("./depot_status_start.dat")

# create lists of binary variables for depot status at the start (y_S) and
# at the finish (y_F) of the time period

# status of facility at the start of the time period y_S
# status of facility at the finish of the time perido, y_F
y_S= []
y_F= []
for loop in range(0,2):
    for rec in depot_status:
        d = int(rec[0])
        i = int(rec[1])
        status = int(rec[2])
        if loop == 0:
            if status == 1:
                y_S.append('owner_' + str(d) + '_depot_' + str(i)+ '_ES')
            else:
                y_S.append('owner_' + str(d) + '_depot_' + str(i)+ '_NS')
        if loop == 1:
            if status == 1:
                y_F.append('owner_' + str(d) + '_depot_' + str(i)+ '_EF')
            else:
                y_F.append('owner_' + str(d) + '_depot_' + str(i)+ '_NF')

# status of all the facility in the time period, y
y = y_S + y_F
# print(y_S)
# print(y_F)

# fixed cost for the depots are the coefficients for depot status
fc_owner, fc_depot, fc = np.loadtxt("./owner_depot_FC_t1.dat", unpack=True)
# print(-1*fc)
# adding binary variable to the objective function with fixed cost as coefficient
prob.variables.add(names= y_S,
                   obj= -1 * fc,
                   lb= [0] * len(y_S),
                   ub= [1] * len(y_S),
                   types= ['B'] * len(y_S)
                   )
prob.variables.add(names= y_F,
                   obj= -1 * fc,
                   lb= [0] * len(y_F),
                   ub= [1] * len(y_F),
                   types= ['B'] * len(y_F)
                   )

# Constraints: All existing facilities are open in the time period
for y_index in range(len(y)):
    i_status = y[y_index]
    if re.search('[E]', i_status):
        rh = 1
        prob.linear_constraints.add(
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
    prob.linear_constraints.add(
        lin_expr=[cplex.SparsePair([y_N_finish , y_N_start], [1, -1])],
        senses=["G"], rhs=[rh], names=['NS']
    )

prob.write("Check.lp")