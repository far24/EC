\ENCODING=ISO-8859-1
\Problem name: 

Minimize
 obj: - 100 owner_0_depot_1_NS - 100 owner_0_depot_1_NF
Subject To
 _ES#0: owner_0_depot_0_ES  = 1
 _ES#1: owner_1_depot_0_ES  = 1
 _ES#2: owner_0_depot_0_EF  = 1
 _ES#3: owner_1_depot_0_EF  = 1
 NS#4:  - owner_0_depot_1_NS + owner_0_depot_1_NF >= 0
Bounds
 0 <= owner_0_depot_0_ES <= 1
 0 <= owner_0_depot_1_NS <= 1
 0 <= owner_1_depot_0_ES <= 1
 0 <= owner_0_depot_0_EF <= 1
 0 <= owner_0_depot_1_NF <= 1
 0 <= owner_1_depot_0_EF <= 1
Binaries
 owner_0_depot_0_ES  owner_0_depot_1_NS  owner_1_depot_0_ES 
 owner_0_depot_0_EF  owner_0_depot_1_NF  owner_1_depot_0_EF 
End
