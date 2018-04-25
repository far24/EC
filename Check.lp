\ENCODING=ISO-8859-1
\Problem name: 

Minimize
 obj: - 300 y_owner_A_depot_1_ES#0 - 200 y_owner_A_depot_2_NS#1
      - 100 y_owner_B_depot_3_ES#2 + 300 y_owner_A_depot_1_EF#3
      + 200 y_owner_A_depot_2_NF#4 + 100 y_owner_B_depot_3_EF#5
      + 10 x_carr_0_IMP_0_depot_('A',_1)#6 + 20 x_carr_0_IMP_0_depot_('A',_2)#7
      + 30 x_carr_0_IMP_0_depot_('B',_3)#8 + 10 x_carr_1_IMP_0_depot_('A',_1)#9
      + 20 x_carr_1_IMP_0_depot_('A',_2)#10
      + 30 x_carr_1_IMP_0_depot_('B',_3)#11
Subject To
 _ES#0: y_owner_A_depot_1_ES#0  = 1
 _ES#1: y_owner_B_depot_3_ES#2  = 1
 _ES#2: y_owner_A_depot_1_EF#3  = 1
 _ES#3: y_owner_B_depot_3_EF#5  = 1
 NS#4:  - y_owner_A_depot_2_NS#1 + y_owner_A_depot_2_NF#4 >= 0
Bounds
 0 <= y_owner_A_depot_1_ES#0 <= 1
 0 <= y_owner_A_depot_2_NS#1 <= 1
 0 <= y_owner_B_depot_3_ES#2 <= 1
 0 <= y_owner_A_depot_1_EF#3 <= 1
 0 <= y_owner_A_depot_2_NF#4 <= 1
 0 <= y_owner_B_depot_3_EF#5 <= 1
      x_carr_0_IMP_0_depot_('A',_1)#6 >= 0
      x_carr_0_IMP_0_depot_('A',_2)#7 >= 0
      x_carr_0_IMP_0_depot_('B',_3)#8 >= 0
      x_carr_1_IMP_0_depot_('A',_1)#9 >= 0
      x_carr_1_IMP_0_depot_('A',_2)#10 >= 0
      x_carr_1_IMP_0_depot_('B',_3)#11 >= 0
Binaries
 y_owner_A_depot_1_ES#0  y_owner_A_depot_2_NS#1  y_owner_B_depot_3_ES#2 
 y_owner_A_depot_1_EF#3  y_owner_A_depot_2_NF#4  y_owner_B_depot_3_EF#5 
Generals
 x_carr_0_IMP_0_depot_('A',_1)#6  x_carr_0_IMP_0_depot_('A',_2)#7 
 x_carr_0_IMP_0_depot_('B',_3)#8  x_carr_1_IMP_0_depot_('A',_1)#9 
 x_carr_1_IMP_0_depot_('A',_2)#10  x_carr_1_IMP_0_depot_('B',_3)#11 
End
