from __future__ import print_function
import cplex

prob = cplex.Cplex()

# i: depot
# j: importer
# k: exporter
# h: port
# l: ocean carrier
# d: depot owner
# t: time period

# Time period
T = [0,1]
# Number of ocean carrier
L = [0]
# number of importers
IMP = [0]
# number of exporter
EXP = [0]
# Number of owners of the facilities
D = [0,1]
# number of ports
H = [0]
# total number of depots/facilities (F) consists of
# number of existing depots/facilities (EF) and
# number of potential/new depots/facilities (NF)
EF =[['Own_0_Depot_E0'],['Own_1_Depot_E0']]
NF = [['Own_0_Depot_N0'],[]]
F = []
for d in range(len(D)):
    F.append([])  # Owner 1, owner 2, ...
    for e in range(len(EF[d])):
        F[d].append(EF[d][e]) # add existing facilities for each owner
    for n in range(len(NF[d])):
        F[d].append(NF[d][n]) # add new facilities for each owner
# print(F)

# fixed Cost of depot of owner in the respective time period
fixed_cost = [
    [[[0,100],[0]], [[0,100],[0]]],
    [[[0,100],[0]], [[0, 100],[0]]]
              ]


# Cost of trucking in each time period
cost_trucking = [2, 2, 3]


# distance from origin to destination in each time period

dist_imp_depot = [
                [[10,5,10] , [10,10,10]], #[time period][importer][depot]
                [[10,5,10] , [10,10,10]]
                  ]
dist_depot_exp = [
                [[10,10,10] , [8,10,10]], # [time period][depot][exporter]
                [[10,10,10] , [8,10,10]]
                  ]
dist_port_depot = [
                [[10,7,10] , [10,10,10]], # [time period][port][depot]
                [[10,7,10] , [10,10,10]]
                  ]
dist_depot_port = [
                [[10,10,10] , [15,10,10]], # [time period][depot][port]
                [[10,10,10] , [15,10,10]]
                  ]
#############################################################################################
# Supply of EC from Importers and ports for each time period
supply_imp = [[85, 50, 35], # Time Period 1
              [85, 80, 90]  # Time Period 2
              ]
supply_port = [[80, 80, 65], [100, 100, 120]]

# Demand of EC of Exporters and ports for each time period
demand_exp = [[70, 50, 85], # Time Period 1
              [90, 80, 10]  # Time Period 2
              ]
demand_port = [[80, 55, 65], [110, 75, 95]]

# Capacity of the depot in the planning horizon
# capacity_depot = [[100,250,250], #Planning horizon 1
#                   [250,250,250]  #Planning horizon 2
#                   ]

# Budget for each depot owner for new establishment and expansion for each time period
#budget = []

# invertory of ocean carrier l container at depot i owned by d
#V = []
#############################################################################################
# decision variables
# Binary variable: '1' if depot i owner d serves ocean carrier l is OPEN;
# '0' otherwise
depot_time = []

# Number of container of ocean carrier l
# shipped form origin (imp, depot, port) to destination (depot, exporter, port)
x_imp_depot = []
x_depot_exp = []
x_port_depot = []
x_depot_port = []

# Exapansion Decision variable for depot owner d
# for the planning horizon
expansion_depot = []

############################################################################################################
# set the sense of the problem
prob.objective.set_sense(prob.objective.sense.minimize)

# variable add 0:
for t in range(len(T)): #time period
    depot_time.append([])
    for l in range(len(L)):
        depot_time[t].append([])
        for d in range(len(D)):
            depot_time[t][l].append([]) #depot owner
            for i in range(len(EF[d])):
                depot_time[t][l][d].append("time_"+str(t)+ "_carr_" +str(l)+"_owner_"+str(d)+"_DEPOT_E_"+str(i))

for t in range(len(T)):
    for l in range(len(L)):
        for d in range(len(D)):
            for i in range(len(NF[d])):
                depot_time[t][l][d].append("time_"+str(t)+"_carr_" + str(l) + "_owner_"+str(d)+"_DEPOT_N_"+str(i))


bin_after_depot_time=[]
bin_after_fixed_cost = []
for t in range(len(T)-1):
    for l in range(len(L)):
        for d in range(len(D)):
            for i in range(len(F[d])):
                bin_after_depot_time.append(depot_time[t+1][l][d][i])
                bin_after_fixed_cost.append(fixed_cost[t+1][l][d][i])

# print(bin_after_depot_time)
# print(bin_after_fixed_cost)

prob.variables.add(names= bin_after_depot_time,
                   obj= bin_after_fixed_cost,
                   lb= [0] * len(bin_after_depot_time),
                   ub= [1] * len(bin_after_depot_time),
                   types= ['B'] * len(bin_after_depot_time)
                   )

bin_prev_depot_time = []
bin_prev_fixed_cost = []
for t in range(len(T)-1):
    for l in range(len(L)):
        for d in range(len(D)):
            for i in range(len(F[d])):
                bin_prev_depot_time.append(depot_time[t][l][d][i])
                bin_prev_fixed_cost.append(-1 * fixed_cost[t][l][d][i])


# print(bin_prev_depot_time)
# print(bin_prev_fixed_cost)

prob.variables.add(names= bin_prev_depot_time,
                   obj= bin_prev_fixed_cost,
                   lb= [0] * len(bin_prev_depot_time),
                   ub= [1] * len(bin_prev_depot_time),
                   types= ['B'] * len(bin_prev_depot_time)
                   )

# Constraints add
# Once a depot is opened in one time, it remains open in other time
for d in range(len(D)):
    for i in range(len(F[d])):
        for l in range(len(L)):
            binary_constraint = []
            for t in range(len(T)):
                binary_constraint.append(depot_time[t][l][d][i])
                rh = 0
            # print(binary_constraint , rh)
            prob.linear_constraints.add(
                lin_expr= [cplex.SparsePair(binary_constraint, [-1,1])],
                senses= ["G"], rhs= [rh]
            )

# The existing depot remains open(=1) all the time
for t in range(len(T)):
    for l in range(len(L)):
        for d in range(len(D)):
            for i in range(len(EF[d])): # Existing depot
                rh = 1
                # print(depot_time[t][l][d][i], rh)
                prob.linear_constraints.add(
                    lin_expr = [cplex.SparsePair([depot_time[t][l][d][i]], [1])],
                    senses=["E"], rhs=[rh]
                )


x_imp_depot_all = []
cost_imp_depot = []
cost_imp_depot_all = []
# variable add 1: container vol from IMPORT to DEPOT
for t in range(len(T)):
    x_imp_depot.append([])
    cost_imp_depot.append([])
    for l in range(len(L)):
        x_imp_depot[t].append([])
        cost_imp_depot[t].append([])
        for j in range(len(IMP)):
            x_imp_depot[t][l].append([])
            cost_imp_depot[t][l].append([])
            for d in range(len(F)):
                x_imp_depot[t][l][j].append([])
                cost_imp_depot[t][l][j].append([])
                for i in range(len(F[d])):
                    x_imp_depot_all.append("vol_time_" + str(t) + "_carr_" + str(l) + "_IMP_" + str(j) + '_own_' + str(d) + '_DEPOT_'+ str(i))
                    x_imp_depot[t][l][j][d].append("vol_time_" + str(t) + "_carr_" + str(l) + "_IMP_" + str(j) + '_own_' + str(d) + '_DEPOT_'+ str(i))
                    cost_imp_depot_all.append(cost_trucking[t] * dist_imp_depot[t][j][i])
                    cost_imp_depot[t][l][j][d].append(cost_trucking[t] * dist_imp_depot[t][j][i])
                    # print("Distance from Imp to Depot: ", cost_trucking[t], dist_imp_depot[t][j][i])

# print(x_imp_depot)
# for i in range(len(x_imp_depot_all)):
#     print(x_imp_depot_all[i], cost_imp_depot_all[i])

prob.variables.add(names=x_imp_depot_all,
                   obj=cost_imp_depot_all,
                   lb =[0] * len(x_imp_depot_all),
                   types = 'I' *  len(x_imp_depot_all)
                   )

# variable add 2: container vol from DEPORT to EXPORT
x_depot_exp_all = []
cost_depot_exp = []
cost_depot_exp_all = []
for t in range(len(T)):
    x_depot_exp.append([])
    cost_depot_exp.append([])
    for l in range(len(L)):
        x_depot_exp[t].append([])
        cost_depot_exp[t].append([])
        for d in range(len(F)):
            x_depot_exp[t][l].append([])
            cost_depot_exp[t][l].append([])
            for i in range(len(F[d])):
                x_depot_exp[t][l][d].append([])
                cost_depot_exp[t][l][d].append([])
                for k in range(len(EXP)):
                    # print("depot:", i, " Exporter: ", k )
                    x_depot_exp_all.append("vol_time_" + str(t) + "_carr_" + str(l) + "_DEPOT_" + str(i) + '_own_' + str(d) + '_EXPORT_'+ str(k))
                    x_depot_exp[t][l][d][i].append("vol_time_" + str(t) + "_carr_" + str(l) + "_DEPOT_" + str(i) + '_own_' + str(d) + '_EXPORT_'+ str(k))
                    cost_depot_exp_all.append(cost_trucking[t] * dist_depot_exp[t][i][k])
                    cost_depot_exp[t][l][d][i].append(cost_trucking[t] * dist_depot_exp[t][i][k])
                    # print("Distance from Depot to Exporter: ", cost_trucking[t], dist_depot_exp[t][i][k])

# for i in range(len(x_depot_exp_all)):
#     print(x_depot_exp_all[i], cost_depot_exp_all[i])

prob.variables.add(names=x_depot_exp_all,
                   obj=cost_depot_exp_all,
                   lb = [0] * len(x_depot_exp_all),
                   types='I' * len(x_depot_exp_all)
                   )


# variable add 3: container vol from DEPOT to PORT
cost_depot_port_all = []
cost_depot_port = []
x_depot_port_all = []
for t in range(len(T)):
    x_depot_port.append([])
    cost_depot_port.append([])
    for l in range(len(L)):
        x_depot_port[t].append([])
        cost_depot_port[t].append([])
        for d in range(len(F)):
            x_depot_port[t][l].append([])
            cost_depot_port[t][l].append([])
            for i in range(len(F[d])):
                x_depot_port[t][l][d].append([])
                cost_depot_port[t][l][d].append([])
                for h in range(len(H)):
                    # print('time: {}; depot: {}, exporter: {}'.format(t,i,k))
                    x_depot_port_all.append("vol_time_" + str(t) + "_carr_" + str(l) + "_DEPOT_" + str(i) + '_own_' + str(d) + '_PORT_'+ str(h))
                    x_depot_port[t][l][d][i].append("vol_time_" + str(t) + "_carr_" + str(l) + "_DEPOT_" + str(i) + '_own_' + str(d) + '_PORT_'+ str(h))
                    cost_depot_port_all.append(cost_trucking[t] * dist_depot_port[t][i][h])
                    cost_depot_port[t][l][d][i].append(cost_trucking[t] * dist_depot_exp[t][i][h])
                    # print("Distance from Depot to Port: ", cost_trucking[t], dist_depot_port[t][i][h])

# for i in range(len(x_depot_port_all)):
#     print(x_depot_port_all[i], cost_depot_port_all[i])

prob.variables.add(names=x_depot_port_all,
                   obj=cost_depot_port_all,
                   lb = [0] * len(x_depot_port_all),
                   types='I' * len(x_depot_port_all)
                   )


# variable add 4: container vol from PORT to DEPOT
x_port_depot_all = []
cost_port_depot_all = []
cost_port_depot = []
for t in range(len(T)):
    x_port_depot.append([])
    cost_port_depot.append([])
    for l in range(len(L)):
        x_port_depot[t].append([])
        cost_port_depot[t].append([])
        for h in range(len(H)):
            x_port_depot[t][l].append([])
            cost_port_depot[t][l].append([])
            for d in range(len(F)):
                x_port_depot[t][l][h].append([])
                cost_port_depot[t][l][h].append([])
                for i in range(len(F[d])):
                    x_port_depot_all.append("vol_time_" + str(t) + "_carr_" + str(l) + "_PORT_" + str(h) + '_own_' + str(d) + '_DEPOT_'+ str(i))
                    x_port_depot[t][l][h][d].append("vol_time_" + str(t) + "_carr_" + str(l) + "_PORT_" + str(h) + '_own_' + str(d) + '_DEPOT_'+ str(i))
                    cost_port_depot_all.append(cost_trucking[t] * dist_port_depot[t][h][i])
                    cost_port_depot[t][l][h][d].append(cost_trucking[t] * dist_port_depot[t][h][i])
#                     print("Distance from Depot to Port: ", cost_trucking[t], dist_port_depot[t][h][i])
#
# for i in range(len(x_port_depot_all)):
#     print(x_port_depot_all[i], cost_port_depot_all[i])


prob.variables.add(names=x_port_depot_all,
                   obj=cost_port_depot_all,
                   lb = [0] * len(x_depot_port_all),
                   types='I' * len(x_port_depot_all)
                   )



# Constraints add
# constraints add 1: Supply from IMPORT to DEPOT
supply_imp = [
    [[[50],[60]],[[50],[60]]], #[time_period][ocean carrier][importer]
    [[[70],[60]],[[50],[60]]]
              ]
for t in range(len(T)):
    for l in range(len(L)):
        for j in range(len(IMP)):
            supply_constraint_1 = []
            for d in range(len(F)):
                for i in range(len(F[d])):
                    supply_constraint_1.append(x_imp_depot[t][l][j][d][i])
            rh = supply_imp[t][l][j]
            # print(supply_constraint_1, rh)
            prob.linear_constraints.add(
                lin_expr = [cplex.SparsePair(supply_constraint_1, [1] * len(supply_constraint_1))],
                senses=["E"], rhs=rh)


# constraints add 2: Supply from PORT to DEPOT

supply_port = [
    [[[80],[85]],[[80],[85]]], #[time_period][ocean carrier][port]
    [[[90],[85]],[[80],[85]]]
              ]

for t in range(len(T)):
    for l in range(len(L)):
        for h in range(len(H)):
            supply_constraint_2 = []
            for d in range(len(F)):
                for i in range(len(F[d])):
                    supply_constraint_2.append(x_port_depot[t][l][h][d][i])
            rh = supply_port[t][l][h]
            # print(supply_constraint_2, rh)
            prob.linear_constraints.add(
                lin_expr=[cplex.SparsePair(supply_constraint_2, [1] * len(supply_constraint_2))],
                senses=["E"], rhs=rh)


demand_exp = [
    [[[70],[50]],[[85],[90]]], #[time_period][ocean carrier][exporter]
    [[[80],[100]],[[80],[85]]]
              ]

# # constraints add 3: Demand of EXPORT from DEPOT
for t in range(len(T)):
    for l in range(len(L)):
        for k in range(len(EXP)):
            demand_constraint_1 = []
            for d in range(len(F)):
                for i in range(len(F[d])):
                    demand_constraint_1.append(x_depot_exp[t][l][d][i][k])
            rh = demand_exp[t][l][k]
            # print(demand_constraint_1, rh)
            prob.linear_constraints.add(
                lin_expr=[cplex.SparsePair(demand_constraint_1, [1] * len(demand_constraint_1))],
                senses=["E"], rhs=rh)

demand_port = [
    [[[55],[65]],[[110],[90]]], #[time_period][ocean carrier][port]
    [[[65],[55]],[[100],[111]]]
              ]

# constraints add 4: Demand of PORT from DEPOT
for t in range(len(T)):
    for l in range(len(L)):
        for h in range(len(H)):
            demand_constraint_2 = []
            for d in range(len(F)):
                for i in range(len(F[d])):
                    demand_constraint_2.append(x_depot_port[t][l][d][i][h])
            rh = demand_port[t][l][h]
            # print(demand_constraint_2, rh)
            prob.linear_constraints.add(
                lin_expr=[cplex.SparsePair(demand_constraint_2, [1] * len(demand_constraint_2))],
                senses=["E"], rhs= rh)


# Constraints add 5: Capacity of the depot, not finished need to add the binary variable

#Capacity of the depot in different time horizon
capacity_depot = [
    [[[80, 75], [70,65]],[[45,0]]],  #[time_period][depot_owner][depot][carrier]
    [[[500, 250], [500, 250]],[[45,0]]]
                ]


# for i in range(0, len(x_imp_depot_all)):
#     print(x_imp_depot_all[i])

# print(depot_time)



for t in range(len(T)):
    for d in range(len(F)):
        capacity_constraint_1 = []
        capacity_coeff =[]
        for i in range(len(F[d])):
            for j in range(len(IMP)):
                for l in range(len(L)):
                    capacity_constraint_1.append(x_imp_depot[t][l][j][d][i])
                    capacity_coeff.append(1)
                    # print("I --> D: ", x_imp_depot[t][l][j][d][i])

            for h in range(len(H)):
                for l in range(len(L)):
                    capacity_constraint_1.append(x_port_depot[t][l][h][d][i])
                    capacity_coeff.append(1)
                    # print("P --> D: ", x_port_depot[t][l][h][d][i])
            for l in range(len(L)):
                capacity_constraint_1.append(depot_time[t][l][d][i])
                # print("Depot existence: ", depot_time[t][l][d][i])
                capacity_coeff.append(-1 * capacity_depot[t][d][i][l])

    rh = 0
    prob.linear_constraints.add(
        lin_expr=[cplex.SparsePair(capacity_constraint_1, capacity_coeff)],
        senses=["L"], rhs=[rh]
    )
    # print("Time period: ", t, "\nCapacity constraint check: \n", len(capacity_constraint_1), capacity_constraint_1)
    # print("RHS:", capacity_coeff)

# initial inventory (t = 0)

# # inventory update
# for t in range(len(T)-1):
#     for l in range(len(L)):
#         for d in range(len(F)):
#             for i in range(len(F[d])):
#                 for k in range(len(EXP)):
#                     print(x_depot_exp[t][l][d][i][k])
#                 for h in range(len(H)):
#                     print(x_depot_port[t][l][d][i][h])
#                 for j in range(len(IMP)):
#                     print(x_imp_depot[t][l][j][d][i])
#                 for h in range(len(H)):
#                     print(x_imp_depot[t][l][h][d][i])


budget = [
    [[[0, 100],[0]],[[0,100],[0]]], #[time_period][carrier][depot_owner][depot]
    [[[0, 110], [0]], [[0, 110], [0]]]
]


for t in range(len(T)):
    # print("-------new time period----")
    for d in range(len(F)):
        total_budget = 0
        budget_constraint = []
        budget_coeff = []
        for i in range(len(F[d])):
            for l in range(len(L)):
                total_budget = - total_budget - budget[t][l][d][i]
                budget_constraint.append(depot_time[t][l][d][i])
                budget_coeff.append(fixed_cost[t][l][d][i])
                # print("Depot status: ",depot_time[t][l][d][i])
                # print("Budget depot owner:", budget[t][l][d][i])
                # print("Total budget", rh)
                # print("Fixed costs:",fixed_cost[t][l][d][i], "\n")
                # print("costraint eqn: \n", budget_constraint , budget_coeff, rh)
    prob.linear_constraints.add(
        lin_expr=[cplex.SparsePair(budget_constraint, budget_coeff)],
        senses=["L"], rhs=[0]
    )

# budget constraint




######################################################################################################################
prob.solve()

sol = prob.solution
# solution.get_status() returns an integer code
print("Solution status = ", sol.get_status())
if sol.is_primal_feasible():
    print("Solution value  = ", sol.get_objective_value())
else:
    print("No solution available.")

print("Binary variable: ")
# print(depot_time)
for t in range(len(T)):
    # print(depot_time[t])
    for l in range(len(L)):
        for d in range(len(D)):
            # print(depot_time[t][d])
            for i in range(len(F[d])):
                print(depot_time[t][l][d][i], sol.get_values(depot_time[t][l][d][i]))


print("\nDepot --> Export:")
for i in range(len(x_depot_exp_all)):
    print((x_depot_exp_all[i], sol.get_values(x_depot_exp_all[i])))

print("\nDepot --> Port:")
for i in range(len(x_depot_port_all)):
    print((x_depot_port_all[i], sol.get_values(x_depot_port_all[i])))

print("\nImporter --> Depot:")
for i in range(len(x_imp_depot_all)):
    print((x_imp_depot_all[i], sol.get_values(x_imp_depot_all[i])))



print("\nPort --> Depot:")
for i in range(len(x_port_depot_all)):
    print((x_port_depot_all[i], sol.get_values(x_port_depot_all[i])))
