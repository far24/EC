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
D = [0]
# number of ports
H = [0]

# Existing depots
EF =[['Own_0_Depot_E0'],    # owner i = 0
     ['Own_1_Depot_E0']     # owner i = 1
     ]
# Potential depots
NF = [['Own_0_Depot_N0'],
      []
      ]

# total number of depots/facilities (F) consists of
# number of existing depots/facilities (EF) and
# number of potential/new depots/facilities (NF)
F = []
for d in range(len(D)):
    F.append([])
    for e in range(len(EF[d])):
        F[d].append(EF[d][e])
    for n in range(len(NF[d])):
        F[d].append(NF[d][n])
#print ("Total Facilty (EF+NF) in the region \n", F)

# fixed Cost of depot of owner in the respective time period
fixed_cost = [
    [[0,100],[0]],  # [time period 1]; [owner_1, [depot_1, depot_2,...]]
    [[0,100],[0]]   # [time period 2] ;
    ]


# Cost of trucking in each time period
cost_trucking = [2, 2, 3]   # [time period 1, time period 2,...]


# distance from origin to destination in each time period

dist_imp_depot = [[[100,50,10] , [10,10,10]], # [time period_1] [imp_1] [depot_1, depot_2, ...]
                  [[100,50,10] , [10,10,10]]
                  ]
dist_depot_exp = [[[100,50,10] , [10,10,10]],
                  [[100,50,10] , [10,10,10]]
                  ]
dist_port_depot = [[[50,100,10] , [10,10,10]],
                  [[50,100,10] , [10,10,10]]
                  ]
dist_depot_port = [[[50,100,10] , [10,10,10]],
                  [[50,100,10] , [10,10,10]]
                  ]

# Inventory of ocean carrier l container at depot i owned by d
V = []


#############################################################################################
# decision variables
# Binary variable: '1' if depot i owner d serves ocean carrier l is OPEN;
# '0' otherwise
depot_time = []

# Number of containers (Volume) of ocean carrier l
# shipped form origin (imp, depot, port) to destination (depot, exporter, port)
# for each time period
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
    for d in range(len(D)): #depot owner
        depot_time[t].append([])
        for i in range(len(EF[d])): # Existing depot
            depot_time[t][d].append("time_"+str(t)+"_owner_"+str(d)+"_DEPOT_E_"+str(i))


for t in range(len(T)):
    for d in range(len(D)):
        for i in range(len(NF[d])): # potential depot
            depot_time[t][d].append("time_"+str(t)+"_owner_"+str(d)+"_DEPOT_N_"+str(i))



bin_after_depot_time=[]
bin_after_fixed_cost = []
for t in range(len(T)-1):
    for d in range(len(D)):
        for i in range(len(F[d])):
            bin_after_depot_time.append(depot_time[t+1][d][i])
            bin_after_fixed_cost.append(fixed_cost[t+1][d][i])
            # print(depot_time[t+1][d][i])
            # print(fixed_cost[t+1][d][i])

print(bin_after_depot_time)
print(bin_after_fixed_cost)

prob.variables.add(names= bin_after_depot_time,
                   obj= bin_after_fixed_cost,
                   lb= [0] * len(bin_after_depot_time),
                   ub= [1] * len(bin_after_depot_time),
                   types= ['B'] * len(bin_after_depot_time)
                   )

bin_prev_depot_time = []
bin_prev_fixed_cost = []
for t in range(len(T)-1):
    for d in range(len(D)):
        for i in range(len(F[d])):
            bin_prev_depot_time.append(depot_time[t][d][i])
            bin_prev_fixed_cost.append(-1 * fixed_cost[t][d][i])
        # print(depot_time[t][d][i])
        # print(-1 * fixed_cost[t][d][i])

print(bin_prev_depot_time)
print(bin_prev_fixed_cost)

prob.variables.add(names= bin_prev_depot_time,
                   obj= bin_prev_fixed_cost,
                   lb= [0] * len(bin_prev_depot_time),
                   ub= [1] * len(bin_prev_depot_time),
                   types= ['B'] * len(bin_prev_depot_time)
                   )

#############################################################################################
# Constraints add
# Once a depot is opened in one time, it remains open in other time
for d in range(len(D)):
    for i in range(len(F[d])):
        binary_constraint = []
        for t in range(len(T)):
            binary_constraint.append(depot_time[t][d][i])
            rh = 0
        print(binary_constraint , rh)
        prob.linear_constraints.add(
            lin_expr= [cplex.SparsePair(binary_constraint, [-1,1])],
            senses= ["G"], rhs= [rh]
        )

# The existing depot remains open(=1) all the time
for t in range(len(T)):
    for d in range(len(D)):
        for i in range(len(EF[d])):
            print(depot_time[t][d][i])
            rh = 1
            prob.linear_constraints.add(
                lin_expr = [cplex.SparsePair([depot_time[t][d][i]], [1])],
                senses=["E"], rhs=[rh]
            )
'''
#############################################################################################
x_imp_depot_all = []
cost_imp_depot = []
cost_imp_depot_all = []
# variable add 1(SUPPLY): Volumes of containers (volume) from IMPORTER to DEPOT
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
                    cost_imp_depot_all.append(cost_trucking[t] * dist_depot_port[t][j][i])
                    cost_imp_depot[t][l][j][d].append(cost_trucking[t] * dist_imp_depot[t][j][i])

# print(x_imp_depot)
# for i in range(len(x_imp_depot_all)):
#     print(x_imp_depot_all[i], cost_imp_depot_all[i])
#
# for i in range(len(cost_imp_depot_all)):
#     print(cost_imp_depot_all[i])

prob.variables.add(names=x_imp_depot_all,
                   obj=cost_imp_depot_all,
                   lb =[0] * len(x_imp_depot_all),
                   types = 'I' *  len(x_imp_depot_all)
                   )

# variable add 2 (DEMAND): Volumes of containers from DEPOT to EXPORT
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
                    x_depot_exp_all.append("vol_time_" + str(t) + "_carr_" + str(l) +'_own_' + str(d)+ "_DEPOT_" + str(i) + '_EXPORT_'+ str(k))
                    x_depot_exp[t][l][d][i].append("vol_time_" + str(t) + "_carr_" + str(l)  + '_own_' + str(d) +  "_DEPOT_" + str(i)+'_EXPORT_'+ str(k))
                    cost_depot_exp_all.append(cost_trucking[t] * dist_depot_port[t][i][k])
                    cost_depot_exp[t][l][d][i].append(cost_trucking[t] * dist_depot_exp[t][i][k])

# for i in range(len(x_depot_exp_all)):
#     print(x_depot_exp_all[i],cost_depot_exp_all[i])

prob.variables.add(names=x_depot_exp_all,
                   obj=cost_depot_exp_all,
                   lb = [0] * len(x_depot_exp_all),
                   types='I' * len(x_depot_exp_all)
                   )

# variable add 3 (DEMAND): Volumes of containers from DEPOT to PORT
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
                    x_depot_port_all.append("vol_time_" + str(t) + "_carr_" + str(l) + '_own_' + str(d) + "_DEPOT_" + str(i) + '_PORT_'+ str(h))
                    x_depot_port[t][l][d][i].append("vol_time_" + str(t) + "_carr_" + str(l) + '_own_' + str(d) + "_DEPOT_" + str(i) + '_PORT_'+ str(h))
                    cost_depot_port_all.append(cost_trucking[t] * dist_depot_port[t][i][h])
                    cost_depot_port[t][l][d][i].append(cost_trucking[t] * dist_depot_exp[t][i][h])

# for i in range(len(x_depot_port_all)):
#     print(x_depot_port_all[i],cost_depot_port_all[i])

prob.variables.add(names=x_depot_port_all,
                   obj=cost_depot_port_all,
                   lb = [0] * len(x_depot_port_all),
                   types='I' * len(x_depot_port_all)
                   )

# variable add 4(SUPPLY): container vol from PORT to DEPOT
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

for i in range(len(x_port_depot_all)):
    print(x_port_depot_all[i],cost_port_depot_all[i])

prob.variables.add(names=x_port_depot_all,
                   obj=cost_port_depot_all,
                   lb = [0] * len(x_depot_port_all),
                   types='I' * len(x_port_depot_all)
                   )

#############################################################################################
# Constraints add
# constraints add 1: Supply from IMPORT to DEPOT
supply_imp = [[[[50],[60]],
               [[50],[60]]
               ],
              [[[50],[60]],
               [[50],[60]]
               ]
              ]
for t in range(len(T)):
    for l in range(len(L)):
        for j in range(len(IMP)):
            supply_constraint_1 = []
            for d in range(len(F)):
                for i in range(len(F[d])):
                    supply_constraint_1.append(x_imp_depot[t][l][j][d][i])
            rh = supply_imp[t][l][j]
            print(supply_constraint_1, rh)
            prob.linear_constraints.add(
                lin_expr = [cplex.SparsePair(supply_constraint_1, [1] * len(supply_constraint_1))],
                senses=["E"], rhs=rh)

# constraints add 2: Supply from PORT to DEPOT

supply_port = [[[[80],[85]],
               [[80],[85]]
               ],
              [[[80],[85]],
               [[80],[85]]
               ]
              ]

for t in range(len(T)):
    for l in range(len(L)):
        for h in range(len(H)):
            supply_constraint_2 = []
            for d in range(len(F)):
                for i in range(len(F[d])):
                    supply_constraint_2.append(x_port_depot[t][l][h][d][i])
            rh = supply_port[t][l][h]
            print(supply_constraint_2, rh)
            prob.linear_constraints.add(
                lin_expr=[cplex.SparsePair(supply_constraint_2, [1] * len(supply_constraint_2))],
                senses=["E"], rhs=rh)

demand_exp = [[[[70],[50]],
               [[85],[90]]
               ],
              [[[80],[100]],
               [[80],[85]]
               ]
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
            print(demand_constraint_1, rh)
            prob.linear_constraints.add(
                lin_expr=[cplex.SparsePair(demand_constraint_1, [1] * len(demand_constraint_1))],
                senses=["E"], rhs=rh)


demand_port = [[[[55],[65]],
               [[110],[90]]
               ],
              [[[65],[55]],
               [[100],[111]]
               ]
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
            print(demand_constraint_2, rh)
            prob.linear_constraints.add(
                lin_expr=[cplex.SparsePair(demand_constraint_2, [1] * len(demand_constraint_2))],
                senses=["E"], rhs= rh)


# Constraints add 5: Capacity of the depot, not finished need to add the binary variable

#Capacity of the depot in different time horizon
capacity_depot = [[[80, 75],[250]],
                  [[500, 250 ],[250]]]

for t in range(len(T)):
    for d in range(len(F)):
        for i in range(len(F[d])):
            capacity_constraint_1 = []
            for j in range(len(IMP)):
                for l in range(len(L)):
                    capacity_constraint_1.append(x_imp_depot[t][l][j][d][i])
            for h in range(len(H)):
                for l in range(len(L)):
                    capacity_constraint_1.append(x_port_depot[t][l][h][d][i])
            # print(capacity_depot[t][d][i],depot_time[t][d][i])
            capacity_constraint_coeff = [1] * len(capacity_constraint_1)
            capacity_constraint_1.append(depot_time[t][d][i])
            capacity_constraint_coeff.append(-1 *capacity_depot[t][d][i])
            print(capacity_constraint_1, capacity_constraint_coeff)
            prob.linear_constraints.add(
                        lin_expr=[cplex.SparsePair(capacity_constraint_1,capacity_constraint_coeff)],
                        senses=["L"], rhs=[0])

# Constrainst add: Invertory of the depot
V_all = []
for t in range(len(T)):
    V.append([])
    for d in range(len(D)):
        V[t].append([])
        for i in range(len(F[d])):
            V[t][d].append([])
            for l in range(len(L)):
                V[t][d][i].append("time_" + str(t)+ "_carr_" + str(l) +"_V_depot_"+ str(i) + "_owner_" + str(d))
                V_all.append("time_" + str(t)+ "_carr_" + str(l) +"_V_depot_"+ str(i) + "_owner_" + str(d))

# for i in range(len(V_all)):
#     print(V_all[i])

for t in range(len(T)):
    for d in range(len(D)):
        inventory_constraint = []
        for i in range(len(F[d])):

            for l in range(len(L)):
                for k in range(len(EXP)):
                    inventory_constraint.append(x_depot_exp[t][l][d][i][k])

# for i in range(len(inventory_constraint)):
#     print(inventory_constraint[i])






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
    for d in range(len(D)):
        # print(depot_time[t][d])
        for i in range(len(F[d])):
            print(depot_time[t][d][i], sol.get_values(depot_time[t][d][i]))


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
'''