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

# Assume, number of liner shipping company is 2
L = [0]
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
                y_S.append('y_DEP_'  + str(owner[rec]) +"," + str(depot[rec])+ '_ES')
            else:
                y_S.append('y_DEP_'  + str(owner[rec]) +"," + str(depot[rec]) + '_NS')
        if loop == 1:
            if status[rec] == 1:
                y_F.append('y_DEP_'  + str(owner[rec]) +"," + str(depot[rec])+ '_EF')
            else:
                y_F.append('y_DEP_'  + str(owner[rec]) +"," + str(depot[rec])+ '_NF')

# status of all the facility in the time period, y
y = y_S + y_F
# print(y_S)
# print(y_F)
# fixed cost for the depots are the coefficients for depot status
fc_owner, fc_depot, fc = read_dat_file("./owner_depot_FC_t1.dat")
# print("Fixed cost are:", fc * -1 )
# adding binary variable to the objective function with fixed cost as coefficient
model.variables.add(names= y_S,
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
    if re.search('ES', i_status):
        print(i_status)
        rh = 1
        model.linear_constraints.add(
            lin_expr=[cplex.SparsePair([i_status], [1])],
            senses=["E"], rhs=[rh], names=['ES']
        )
for y_index in range(len(y)):
    i_status = y[y_index]
    if re.search('EF', i_status):
        print(i_status)
        rh = 1
        model.linear_constraints.add(
            lin_expr=[cplex.SparsePair([i_status], [1])],
            senses=["E"], rhs=[rh], names=['FS']
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
        senses=["E"], rhs=[rh], names=['NS']
    )
#_______________________________________________________________________________________
# Adding variable to objective function and constrains
#_______________________________________________________________________________________
# variable 1 add: container vol from IMPORT to DEPOT (x_imp_depot)
#---------------------------------------------------------------------------------------
# Create variable x_imp_depot ; type 'list
x_imp_depot = []
x_imp_depot_all = []

# Coefficient of the variables are the cost = cost of trucking * distance between O-D
dist_exp_depot = read_dat_file("./OD_j_i.dat")
# print(dist_exp_depot)
cost_imp_depot = []
cost_imp_depot_all = []



for l in range(len(L)):
    x_imp_depot.append([])
    cost_imp_depot.append([])
    for j in range(num_imp):
        x_imp_depot[l].append([])
        cost_imp_depot[l].append([])
        for i in range(len(owner_depot)):
            x_imp_depot[l][j].append("x_OC_" + str(l) + "_IMP_" + str(j) + "_DEP_" + str(owner_depot[i]))
            x_imp_depot_all.append("x_OC_" + str(l) + "_IMP_" + str(j) + "_DEP_" + str(owner_depot[i]))
            cost_imp_depot[l][j].append(dist_exp_depot[j][i])
            cost_imp_depot_all.append(dist_exp_depot[j][i])

# for i in range(len(x_imp_depot_all)):
#     print("Flow from IMP to DEPOT:", x_imp_depot_all[i], "\tCost from IMP to DEPOT:", cost_imp_depot_all[i])

# Adding variable [cost_imp_depot][x_imp_depot] to the model
model.variables.add(names=x_imp_depot_all,
                   obj=cost_imp_depot_all,
                   lb =[0] * len(x_imp_depot_all),
                   types = 'I' *  len(x_imp_depot_all)
                   )

#_______________________________________________________________________________________
# Constraints Supply 1: total (sum of) number of EC container from importer to
# depot for each liner shipping company (x_carr_l_IMP_j_depot_(d, i))
# equals to the total supply from importer (S_j)
# (d,i)Sum(x_carr_l_PORT_j_depot_(d, i)) = S_j ; for (l:{L}, j : {J})
#---------------------------------------------------------------------------------------
# Supply file: Supply of ocean carrier 'l's EC from importer j (S_j_l)
# Supply file : Each line(array) is importer;
#               Each element in line(array) is # of container of liner shipper
# Loading Supply file :
S_j =  read_dat_file("./supply_imp.dat")
# print(S_j)

for l in range(len(L)):
    supply_constraint_1 = []
    for j in range(num_imp):
        for i in range(len(owner_depot)):
            # print("l = ",l,"j = ",j,"i = ",i)
            supply_constraint_1.append(x_imp_depot[l][j][i])
        rh = S_j[j][l]
        # print(supply_constraint_1, rh)
        model.linear_constraints.add(
            lin_expr = [cplex.SparsePair(supply_constraint_1, [1] * len(supply_constraint_1))],
            senses=["E"],
            rhs= [rh],
            names= ['supply_IMP_' + str(j)+'_OC_' + str(l)]
        )

#_______________________________________________________________________________________
# variable 2 add: container vol from port to DEPOT (x_port_depot)
#---------------------------------------------------------------------------------------
# Create variable x_port_depot ; type 'list
x_port_depot = []
x_port_depot_all = []

# Coefficient of the variables are the cost = cost of trucking * distance between O-D
dist_port_depot = read_dat_file("./OD_h_i.dat")
# print(dist_port_depot[0])
cost_port_depot = []
cost_port_depot_all = []


for l in range(len(L)):
    x_port_depot.append([])
    cost_port_depot.append([])
    for h in range(num_port):
        x_port_depot[l].append([])
        cost_port_depot[l].append([])
        for i in range(len(owner_depot)):
            x_port_depot[l][h].append("x_OC_" + str(l) + "_PORT_" + str(h) + "_DEP_" + str(owner_depot[i]))
            x_port_depot_all.append("x_OC_" + str(l) + "_PORT_" + str(h) + "_DEP_" + str(owner_depot[i]))
            cost_port_depot[l][h].append(dist_port_depot[h][i])
            cost_port_depot_all.append(dist_port_depot[h][i])

# for i in range(len(x_imp_depot_all)):
#     print(x_port_depot_all[i], cost_port_depot_all[i])

# Adding variable [cost_port_depot][x_port_depot] to the model
model.variables.add(names=x_port_depot_all,
                   obj=cost_port_depot_all,
                   lb =[0] * len(x_port_depot_all),
                   types = 'I' *  len(x_port_depot_all)
                   )

#_______________________________________________________________________________________
# Constraints Supply 2: total (sum of) number of EC container from PORT to DEPOT for
# each liner shipping company (x_carr_l_PORT_j_depot_(d, i))
# equals to the total supply from port (S_h)
# (d,i)Sum(x_carr_l_PORT_j_depot_(d, i)) = S_h ; for (l:{L}, h : {H})
#---------------------------------------------------------------------------------------
# Supply file: Supply of ocean carrier 'l's EC from PORT h (S_h_l)
# Supply file : Each line(array) is PORT;
#               Each element in line(array) is # of container of liner shipper
# Loading Supply file
S_h =  read_dat_file("./supply_port.dat")
# print(S_h)

for l in range(len(L)):
    supply_constraint_2 = []
    for h in range(num_port):
        for i in range(len(owner_depot)):
            # print("l = ",l,"j = ",j,"i = ",i)
            supply_constraint_2.append(x_port_depot[l][h][i])
        rh = S_h[h][l]
        # print(supply_constraint_2, rh)
        model.linear_constraints.add(
            lin_expr = [cplex.SparsePair(supply_constraint_2, [1] * len(supply_constraint_2))],
            senses=["E"],
            rhs= [rh],
            names= ['supply_PORT_' + str(j)+'_OC_' + str(l)]
        )
#_______________________________________________________________________________________
# variable 3 add: container vol from DEPOT to EXPORTER (x_depot_exp)
#---------------------------------------------------------------------------------------
# Create variable x_depot_exp ; type 'list
x_depot_exp = []
x_depot_exp_all = []

# Coefficient of the variables are the cost = cost of trucking * distance between O-D
dist_depot_exp = read_dat_file("./OD_i_k.dat")
# print(dist_depot_exp)

cost_depot_exp = []
cost_depot_exp_all = []


for l in range(len(L)):
    x_depot_exp.append([])
    cost_depot_exp.append([])
    for i in range(len(owner_depot)):
        x_depot_exp[l].append([])
        cost_depot_exp[l].append([])
        for k in range(num_exp):
            x_depot_exp[l][i].append("x_OC_" + str(l) + "_DEP_" + str(owner_depot[i]) + "_EXP_" + str(k))
            x_depot_exp_all.append("x_OC_" + str(l) + "_DEP_" + str(owner_depot[i]) + "_EXP_" + str(k))
            cost_depot_exp[l][i].append(dist_depot_exp[k][i])
            cost_depot_exp_all.append(dist_depot_exp[k][i])

# for i in range(len(x_depot_exp_all)):
#     print(x_depot_exp_all[i], cost_depot_exp_all[i])

# Adding variable [cost_depot_exp][x_depot_exp] to the model
model.variables.add(names = x_depot_exp_all,
                   obj=cost_depot_exp_all,
                   lb =[0] * len(x_depot_exp_all),
                   types = 'I' *  len(x_depot_exp_all)
                   )

#_______________________________________________________________________________________
# Constraints Demand 1: total (sum of) number of EC container from DEPOT to EXPORTER for
# each liner shipping company (x_carr_l_depot_(d, i)_PORT_j)
# equals to the total Demand in EXPORTER (D_k)
# (d,i)Sum(x_carr_l_PORT_j_depot_(d, i)) = S_h ; for (l:{L}, k : {K})
#---------------------------------------------------------------------------------------
# Demand file: Demand of ocean carrier 'l's EC in EXPORTER (D_k)
# Demand file : Each line(array) is EXPORTER;
#               Each element in line(array) is # of container of liner shipper
# Loading Supply file
D_k =  read_dat_file("./demand_exp.dat")
# print(D_k)
# print(x_depot_exp)


for l in range(len(L)):
    demand_constraint_1 = []
    for k in range(num_exp):
        for i in range(len(owner_depot)):
            # print("l = ",l,"j = ",j,"i = ",i)
            demand_constraint_1.append(x_depot_exp[l][i][k])
        rh = D_k[k][l]
        # print(demand_constraint_1, rh)
        model.linear_constraints.add(
            lin_expr = [cplex.SparsePair(demand_constraint_1, [1] * len(demand_constraint_1))],
            senses=["E"],
            rhs= [rh],
            names= ['Demand_EXP_' + str(k)+'_OC_' + str(l)]
        )

#_______________________________________________________________________________________
# variable 4 add: container vol from DEPOT to PORT (x_depot_port)
#---------------------------------------------------------------------------------------
# Create variable x_depot_port ; type 'list
x_depot_port = []
x_depot_port_all = []

# Coefficient of the variables are the cost = cost of trucking * distance between O-D
dist_depot_port = read_dat_file("./OD_i_h.dat")
# print(dist_depot_exp)
cost_depot_port = []
cost_depot_port_all = []



for l in range(len(L)):
    x_depot_port.append([])
    cost_depot_port.append([])
    for i in range(len(owner_depot)):
        x_depot_port[l].append([])
        cost_depot_port[l].append([])
        for h in range(num_port):
            x_depot_port[l][i].append("x_OC_" + str(l) + "_DEP_" + str(owner_depot[i]) + "_PORT_" + str(h))
            x_depot_port_all.append("x_OC_" + str(l) + "_DEP_" + str(owner_depot[i]) + "_PORT_" + str(h))
            cost_depot_port[l][i].append(dist_depot_port[h][i])
            cost_depot_port_all.append(dist_depot_port[h][i])

# for i in range(len(x_depot_port_all)):
#     print(x_depot_port_all[i], cost_depot_port_all[i])

# Adding variable [cost_depot_port][x_depot_port] to the obj function of the model
model.variables.add(names = x_depot_port_all,
                   obj = cost_depot_port_all,
                   lb =[0] * len(x_depot_port_all),
                   types = 'I' *  len(x_depot_port_all)
                   )

#_______________________________________________________________________________________
# Constraints Demand 2: total (sum of) number of EC container from Depot to port
# for each liner shipping company (x_carr_l_DEPOT_(d, i)_PORT_h)
# equals to the total demand of Port (D_h)
# (d,i)Sum(x_carr_l_PORT_j_depot_(d, i)) = S_h ; for (l:{L}, h : {H})
#---------------------------------------------------------------------------------------
# Demand file: Demand of ocean carrier 'l's EC in PORT (D_h)
# Demand file : Each line(array) is EXPORTER;
#               Each element in line(array) is # of container of liner shipper
# Loading Demand file
D_h =  read_dat_file("./demand_port.dat")
# print("Demand of port:", D_h)

for l in range(len(L)):
    demand_constraint_2 = []
    for h in range(num_port):
        for i in range(len(owner_depot)):
            # print("l = ",l,"j = ",j,"i = ",i)
            demand_constraint_2.append(x_depot_port[l][i][h])
        rh = D_h[h][l]
        # print(demand_constraint_2, rh)
        model.linear_constraints.add(
            lin_expr = [cplex.SparsePair(demand_constraint_2, [1] * len(demand_constraint_2))],
            senses=["E"],
            rhs= [rh],
            names= ['Demand_PORT_' + str(h)+'_OC_' + str(l)]
        )

# _______________________________________________________________________________________
# variable 5 add: inventory of depot for each liner shipper 'l' at the end of the time period
# ---------------------------------------------------------------------------------------
# Create variable v_depot_carr_F ; type 'list
v_depot_carr_F = []
v_depot_carr_F_all = []

# co-efficent of inventory of depot is 'zero'
# because these variables are not included in the objective function

for l in range(len(L)):
    v_depot_carr_F.append([])
    for i in range(len(owner_depot)):
        v_depot_carr_F[l].append("F_Invent_OC_" + str(l) + '_DEP_'+ str(owner_depot[i]))
        v_depot_carr_F_all.append("F_Invent_OC_" + str(l) + '_DEP_'+ str(owner_depot[i]))
#
# for i in range(len(v_depot_carr_F_all)):
#     print(v_depot_carr_F_all[i])

# Adding variable [0]*[x_depot_port] to the obj function of the model
model.variables.add(names = v_depot_carr_F_all,
                   lb = [0] * len(v_depot_carr_F_all),
                   types= 'I' * len(v_depot_carr_F_all)
                   )
#_______________________________________________________________________________________
# Constraints inventory : Number of EC container in DEPOT
# for each liner shipping company at the Finish of the time period is (x_carr_l_DEPOT_(d, i)_PORT_h)
# equals to the Number of EC container in DEPOT for each liner shipping company at the Start (v_depot_carr_S)
# + sum of(total) EC from IMPORTER to DEPOT for each shipping liner (x_imp_depot)
# + sum of(total) EC from PORT to DEPOT for each shipping liner (x_port_depot)
# - sum of(total) EC from DEPOT to EXPORTER for each shipping liner (x_depot_exp)
# - sum of(total) EC from DEPOT to PORT for each shipping liner (x_depot_port)
#---------------------------------------------------------------------------------------
# Inventory file: Inventory of ocean carrier 'l's EC in DEPOT (V_i)
# Demand file : Each line(array) is DEPOT;
#               Each element in line(array) is # of container of liner shipper
# Loading Demand file
inventory_depot_S = read_dat_file("./inventory_depot_S.dat")
# print(inventory_depot_S)


for i in range(len(owner_depot)):
    for l in range(len(L)):
        inventory_costraint = []
        inventory_coeff = []
        # print("F_Inventory of Depot: ", i, owner_depot[i], "for carrier : ", l, "is:", v_depot_carr_F[l][i])
        inventory_costraint.append(v_depot_carr_F[l][i])
        inventory_coeff.append(1)
        # print("S_Inventory of Depot: ", i, owner_depot[i], "for carrier : ", l, "is:", inventory_depot_S[i][l])
        rh = inventory_depot_S[i][l]
        for k in range(num_exp):
            # print("l", l, "i", i, "k", k, "\nI --> D", x_depot_exp[l][i][k])
            inventory_costraint.append(x_depot_exp[l][i][k])
            inventory_coeff.append(1)
        for h in range(num_port):
            # print("l", l, "i", i, "h", h, "\nD --> P", x_depot_port[l][i][h])
            inventory_costraint.append(x_depot_port[l][i][h])
            inventory_coeff.append(1)
        for h in range(num_port):
            # print("l", l, "h", h, "i", i, "\nP --> D", x_port_depot[l][h][i])
            inventory_costraint.append(x_port_depot[l][h][i])
            inventory_coeff.append(-1)
        for j in range(num_imp):
            # print("l",l,"j",j,"i",i,"\nI --> D",x_imp_depot[l][j][i])
            inventory_costraint.append(x_imp_depot[l][j][i])
            inventory_coeff.append(-1)

        # print(inventory_costraint)
        # print(inventory_coeff)
        model.linear_constraints.add(
            lin_expr=[cplex.SparsePair(inventory_costraint, inventory_coeff)],
            senses=["E"],
            rhs =[rh],
            names = ['F_Invent_DEP_' + str(i) + '_OC_' + str(l)]
        )

#_______________________________________________________________________________________
# Constraints Capacity: Total Number (sum of) of EC container of ocean carrier ('l') in DEPOT
# inventory at the start of the time period
# + sum of(total) EC from IMPORTER to DEPOT for each shipping liner (x_imp_depot)
# + sum of(total) EC from PORT to DEPOT for each shipping liner (x_port_depot)
# LESS THAN EQUAL capapcity of the depot , if the depot is open
#---------------------------------------------------------------------------------------
# Inventory file: Inventory of ocean carrier 'l's EC in DEPOT (V_i)
# Demand file : Each line(array) is DEPOT;
#               Each element in line(array) is # of container of liner shipper
# Loading Demand file

capacity_depot = read_dat_file("./owner_depot_CAP.dat")
# print(capacity_depot)

for i in range(len(owner_depot)):
    capacity_constraint = []
    capacity_coeff = []
    for j in range(num_imp):
        for l in range(len(L)):
            capacity_constraint.append(x_imp_depot[l][j][i])
            capacity_coeff.append(1)
            # print("I --> D: ", x_imp_depot[l][j][i])

    for h in range(num_port):
        for l in range(len(L)):
            capacity_constraint.append(x_port_depot[l][h][i])
            capacity_coeff.append(1)
            # print("P --> D: ", x_port_depot[l][h][i])
    invent_l = 0
    for l in range(len(L)):
        invent_l = invent_l + inventory_depot_S[i][l]
        # print(invent_l)
    rh = -1 * invent_l

    capacity_constraint.append(y_F[i])
    capacity_coeff.append(-1 * capacity_depot[0][i])

    print(capacity_constraint)
    print(capacity_coeff)
    print(i)
    model.linear_constraints.add(
        lin_expr = [cplex.SparsePair(capacity_constraint, capacity_coeff)],
        senses=["L"],
        rhs= [rh],
        names = ["Cap_D" + str(owner_depot[i])]
    )

model.write("equations.lp")

######################################################################################################################
model.solve()

sol = model.solution

if sol.is_primal_feasible():
    print("Solution value  = ", sol.get_objective_value())
else:
    print("No solution available.")

# solution.get_status() returns an integer code
status = model.solution.get_status()
print("Solution Status = ", status , ":", model.solution.status[status])
# Solution type
print("Solution type: ", model.solution.get_solution_type())

print("\nBinary variable: ")
# print(depot_time)
for loop in range(0,2):
    if loop == 0:
        for i in range(len(owner_depot)):
            print(y[i], sol.get_values(y[i]))
    if loop == 1:
        for i in range(len(owner_depot)):
            print(y[i + (len(y)/2)], sol.get_values(y[i+ (len(y)/2)]))

print("\nSupply of EC:")

print("Importer --> Depot:")
for i in range(len(x_imp_depot_all)):
    print((x_imp_depot_all[i], sol.get_values(x_imp_depot_all[i])))

print("Port --> Depot:")
for i in range(len(x_port_depot_all)):
    print((x_port_depot_all[i], sol.get_values(x_port_depot_all[i])))


print("\nMeeting Demand of EC:\n")


print("Depot --> Export:")
for i in range(len(x_depot_exp_all)):
    print((x_depot_exp_all[i], sol.get_values(x_depot_exp_all[i])))

print("Depot --> Port:")
for i in range(len(x_depot_port_all)):
    print((x_depot_port_all[i], sol.get_values(x_depot_port_all[i])))

print("\nInventory at Depot:")
for i in range(len(v_depot_carr_F_all)):
    print((v_depot_carr_F_all[i], sol.get_values(v_depot_carr_F_all[i])))

