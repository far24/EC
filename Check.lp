\ENCODING=ISO-8859-1
\Problem name: 

Minimize
 obj: - 300 y_owner_A_depot_1_ES#0 - 200 y_owner_A_depot_2_NS#1
      - 100 y_owner_B_depot_3_ES#2 + 300 y_owner_A_depot_1_EF#3
      + 200 y_owner_A_depot_2_NF#4 + 100 y_owner_B_depot_3_EF#5
      + 10 x_carr_0_IMP_0_depot_('A',_1)#6 + 15 x_carr_0_IMP_0_depot_('A',_2)#7
      + 20 x_carr_0_IMP_0_depot_('B',_3)#8 + 10 x_carr_1_IMP_0_depot_('A',_1)#9
      + 15 x_carr_1_IMP_0_depot_('A',_2)#10
      + 20 x_carr_1_IMP_0_depot_('B',_3)#11
      + 20 x_carr_0_PORT_0_depot_('A',_1)#12
      + 25 x_carr_0_PORT_0_depot_('A',_2)#13
      + 30 x_carr_0_PORT_0_depot_('B',_3)#14
      + 20 x_carr_1_PORT_0_depot_('A',_1)#15
      + 25 x_carr_1_PORT_0_depot_('A',_2)#16
      + 30 x_carr_1_PORT_0_depot_('B',_3)#17
      + 10 x_carr_0_DEPOT_('A',_1)_EXP_0#18
      + 15 x_carr_0_DEPOT_('A',_2)_EXP_0#19
      + 20 x_carr_0_DEPOT_('B',_3)_EXP_0#20
      + 10 x_carr_1_DEPOT_('A',_1)_EXP_0#21
      + 15 x_carr_1_DEPOT_('A',_2)_EXP_0#22
      + 20 x_carr_1_DEPOT_('B',_3)_EXP_0#23
Subject To
 _ES#0:                  y_owner_A_depot_1_ES#0  = 1
 _ES#1:                  y_owner_B_depot_3_ES#2  = 1
 _ES#2:                  y_owner_A_depot_1_EF#3  = 1
 _ES#3:                  y_owner_B_depot_3_EF#5  = 1
 NS#4:                   - y_owner_A_depot_2_NS#1 + y_owner_A_depot_2_NF#4 >= 0
 supply_IMP_0_carr_0#5:  x_carr_0_IMP_0_depot_('A',_1)#6
                         + x_carr_0_IMP_0_depot_('A',_2)#7
                         + x_carr_0_IMP_0_depot_('B',_3)#8  = 65
 supply_IMP_0_carr_1#6:  x_carr_1_IMP_0_depot_('A',_1)#9
                         + x_carr_1_IMP_0_depot_('A',_2)#10
                         + x_carr_1_IMP_0_depot_('B',_3)#11  = 85
 supply_PORT_0_carr_0#7: x_carr_0_PORT_0_depot_('A',_1)#12
                         + x_carr_0_PORT_0_depot_('A',_2)#13
                         + x_carr_0_PORT_0_depot_('B',_3)#14  = 65
 supply_PORT_0_carr_1#8: x_carr_1_PORT_0_depot_('A',_1)#15
                         + x_carr_1_PORT_0_depot_('A',_2)#16
                         + x_carr_1_PORT_0_depot_('B',_3)#17  = 85
 Demand_EXP_0_carr_0#9:  x_carr_0_DEPOT_('A',_1)_EXP_0#18
                         + x_carr_0_DEPOT_('A',_2)_EXP_0#19
                         + x_carr_0_DEPOT_('B',_3)_EXP_0#20  = 60
 Demand_EXP_0_carr_1#10: x_carr_1_DEPOT_('A',_1)_EXP_0#21
                         + x_carr_1_DEPOT_('A',_2)_EXP_0#22
                         + x_carr_1_DEPOT_('B',_3)_EXP_0#23  = 90
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
      x_carr_0_PORT_0_depot_('A',_1)#12 >= 0
      x_carr_0_PORT_0_depot_('A',_2)#13 >= 0
      x_carr_0_PORT_0_depot_('B',_3)#14 >= 0
      x_carr_1_PORT_0_depot_('A',_1)#15 >= 0
      x_carr_1_PORT_0_depot_('A',_2)#16 >= 0
      x_carr_1_PORT_0_depot_('B',_3)#17 >= 0
      x_carr_0_DEPOT_('A',_1)_EXP_0#18 >= 0
      x_carr_0_DEPOT_('A',_2)_EXP_0#19 >= 0
      x_carr_0_DEPOT_('B',_3)_EXP_0#20 >= 0
      x_carr_1_DEPOT_('A',_1)_EXP_0#21 >= 0
      x_carr_1_DEPOT_('A',_2)_EXP_0#22 >= 0
      x_carr_1_DEPOT_('B',_3)_EXP_0#23 >= 0
Binaries
 y_owner_A_depot_1_ES#0  y_owner_A_depot_2_NS#1  y_owner_B_depot_3_ES#2 
 y_owner_A_depot_1_EF#3  y_owner_A_depot_2_NF#4  y_owner_B_depot_3_EF#5 
Generals
 x_carr_0_IMP_0_depot_('A',_1)#6  x_carr_0_IMP_0_depot_('A',_2)#7 
 x_carr_0_IMP_0_depot_('B',_3)#8  x_carr_1_IMP_0_depot_('A',_1)#9 
 x_carr_1_IMP_0_depot_('A',_2)#10  x_carr_1_IMP_0_depot_('B',_3)#11 
 x_carr_0_PORT_0_depot_('A',_1)#12  x_carr_0_PORT_0_depot_('A',_2)#13 
 x_carr_0_PORT_0_depot_('B',_3)#14  x_carr_1_PORT_0_depot_('A',_1)#15 
 x_carr_1_PORT_0_depot_('A',_2)#16  x_carr_1_PORT_0_depot_('B',_3)#17 
 x_carr_0_DEPOT_('A',_1)_EXP_0#18  x_carr_0_DEPOT_('A',_2)_EXP_0#19 
 x_carr_0_DEPOT_('B',_3)_EXP_0#20  x_carr_1_DEPOT_('A',_1)_EXP_0#21 
 x_carr_1_DEPOT_('A',_2)_EXP_0#22  x_carr_1_DEPOT_('B',_3)_EXP_0#23 
End
