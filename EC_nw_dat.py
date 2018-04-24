from __future__ import print_function
import numpy as np
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
y_exist = []
y_new = []
depot_status = np.loadtxt("./depot_status_start.dat")
for rec in depot_status:
    d = int(rec[0])
    i = int(rec[1])
    status = int(rec[2])
    if status == 1:
        y_exist.append('owner_' + str(d) + '_depot_' + str(i)+ '_E')
    else:
        y_new.append('owner_' + str(d) + '_depot_' + str(i)+ '_N')


# Adding variable 'existing depot' to the problem
# fixed cost 