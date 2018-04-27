\ENCODING=ISO-8859-1
\Problem name: 

Minimize
 obj: - 300 y_DEP_101,1_ES#0 - 200 y_DEP_101,2_NS#1 - 100 y_DEP_202,3_ES#2
      + 300 y_DEP_101,1_EF#3 + 200 y_DEP_101,2_NF#4 + 100 y_DEP_202,3_EF#5
      + 10 x_OC_0_IMP_0_DEP_(101,_1)#6 + 15 x_OC_0_IMP_0_DEP_(101,_2)#7
      + 20 x_OC_0_IMP_0_DEP_(202,_3)#8 + 10 x_OC_1_IMP_0_DEP_(101,_1)#9
      + 15 x_OC_1_IMP_0_DEP_(101,_2)#10 + 20 x_OC_1_IMP_0_DEP_(202,_3)#11
      + 20 x_OC_0_PORT_0_DEP_(101,_1)#12 + 25 x_OC_0_PORT_0_DEP_(101,_2)#13
      + 30 x_OC_0_PORT_0_DEP_(202,_3)#14 + 20 x_OC_1_PORT_0_DEP_(101,_1)#15
      + 25 x_OC_1_PORT_0_DEP_(101,_2)#16 + 30 x_OC_1_PORT_0_DEP_(202,_3)#17
      + 20 x_OC_0_DEP_(101,_1)_EXP_0#18 + 25 x_OC_0_DEP_(101,_2)_EXP_0#19
      + 30 x_OC_0_DEP_(202,_3)_EXP_0#20 + 20 x_OC_1_DEP_(101,_1)_EXP_0#21
      + 25 x_OC_1_DEP_(101,_2)_EXP_0#22 + 30 x_OC_1_DEP_(202,_3)_EXP_0#23
      + 20 x_OC_0_DEP_(101,_1)_PORT_0#24 + 25 x_OC_0_DEP_(101,_2)_PORT_0#25
      + 30 x_OC_0_DEP_(202,_3)_PORT_0#26 + 20 x_OC_1_DEP_(101,_1)_PORT_0#27
      + 25 x_OC_1_DEP_(101,_2)_PORT_0#28 + 30 x_OC_1_DEP_(202,_3)_PORT_0#29
Subject To
 _ES#0:                  y_DEP_101,1_ES#0  = 1
 _ES#1:                  y_DEP_101,2_NS#1  = 1
 _ES#2:                  y_DEP_202,3_ES#2  = 1
 _ES#3:                  y_DEP_101,1_EF#3  = 1
 _ES#4:                  y_DEP_101,2_NF#4  = 1
 _ES#5:                  y_DEP_202,3_EF#5  = 1
 NS#6:                   - y_DEP_101,2_NS#1 + y_DEP_101,2_NF#4 >= 0
 supply_IMP_0_OC_0#7:    x_OC_0_IMP_0_DEP_(101,_1)#6
                         + x_OC_0_IMP_0_DEP_(101,_2)#7
                         + x_OC_0_IMP_0_DEP_(202,_3)#8  = 65
 supply_IMP_0_OC_1#8:    x_OC_1_IMP_0_DEP_(101,_1)#9
                         + x_OC_1_IMP_0_DEP_(101,_2)#10
                         + x_OC_1_IMP_0_DEP_(202,_3)#11  = 85
 supply_PORT_0_OC_0#9:   x_OC_0_PORT_0_DEP_(101,_1)#12
                         + x_OC_0_PORT_0_DEP_(101,_2)#13
                         + x_OC_0_PORT_0_DEP_(202,_3)#14  = 65
 supply_PORT_0_OC_1#10:  x_OC_1_PORT_0_DEP_(101,_1)#15
                         + x_OC_1_PORT_0_DEP_(101,_2)#16
                         + x_OC_1_PORT_0_DEP_(202,_3)#17  = 85
 Demand_EXP_0_OC_0#11:   x_OC_0_DEP_(101,_1)_EXP_0#18
                         + x_OC_0_DEP_(101,_2)_EXP_0#19
                         + x_OC_0_DEP_(202,_3)_EXP_0#20  = 60
 Demand_EXP_0_OC_1#12:   x_OC_1_DEP_(101,_1)_EXP_0#21
                         + x_OC_1_DEP_(101,_2)_EXP_0#22
                         + x_OC_1_DEP_(202,_3)_EXP_0#23  = 90
 Demand_PORT_0_OC_0#13:  x_OC_0_DEP_(101,_1)_PORT_0#24
                         + x_OC_0_DEP_(101,_2)_PORT_0#25
                         + x_OC_0_DEP_(202,_3)_PORT_0#26  = 80
 Demand_PORT_0_OC_1#14:  x_OC_1_DEP_(101,_1)_PORT_0#27
                         + x_OC_1_DEP_(101,_2)_PORT_0#28
                         + x_OC_1_DEP_(202,_3)_PORT_0#29  = 70
 F_Invent_DEP_0_OC_0#15: - x_OC_0_IMP_0_DEP_(101,_1)#6
                         - x_OC_0_PORT_0_DEP_(101,_1)#12
                         + x_OC_0_DEP_(101,_1)_EXP_0#18
                         + x_OC_0_DEP_(101,_1)_PORT_0#24
                         + F_Invent_OC_0_DEP_(101,_1)#30  = 10
 F_Invent_DEP_0_OC_1#16: - x_OC_1_IMP_0_DEP_(101,_1)#9
                         - x_OC_1_PORT_0_DEP_(101,_1)#15
                         + x_OC_1_DEP_(101,_1)_EXP_0#21
                         + x_OC_1_DEP_(101,_1)_PORT_0#27
                         + F_Invent_OC_1_DEP_(101,_1)#33  = 20
 F_Invent_DEP_1_OC_0#17: - x_OC_0_IMP_0_DEP_(101,_2)#7
                         - x_OC_0_PORT_0_DEP_(101,_2)#13
                         + x_OC_0_DEP_(101,_2)_EXP_0#19
                         + x_OC_0_DEP_(101,_2)_PORT_0#25
                         + F_Invent_OC_0_DEP_(101,_2)#31  = 20
 F_Invent_DEP_1_OC_1#18: - x_OC_1_IMP_0_DEP_(101,_2)#10
                         - x_OC_1_PORT_0_DEP_(101,_2)#16
                         + x_OC_1_DEP_(101,_2)_EXP_0#22
                         + x_OC_1_DEP_(101,_2)_PORT_0#28
                         + F_Invent_OC_1_DEP_(101,_2)#34  = 25
 F_Invent_DEP_2_OC_0#19: - x_OC_0_IMP_0_DEP_(202,_3)#8
                         - x_OC_0_PORT_0_DEP_(202,_3)#14
                         + x_OC_0_DEP_(202,_3)_EXP_0#20
                         + x_OC_0_DEP_(202,_3)_PORT_0#26
                         + F_Invent_OC_0_DEP_(202,_3)#32  = 5
 F_Invent_DEP_2_OC_1#20: - x_OC_1_IMP_0_DEP_(202,_3)#11
                         - x_OC_1_PORT_0_DEP_(202,_3)#17
                         + x_OC_1_DEP_(202,_3)_EXP_0#23
                         + x_OC_1_DEP_(202,_3)_PORT_0#29
                         + F_Invent_OC_1_DEP_(202,_3)#35  = 15
 Cap_D(101,_1)#21:       - 150 y_DEP_101,1_EF#3 + x_OC_0_IMP_0_DEP_(101,_1)#6
                         + x_OC_1_IMP_0_DEP_(101,_1)#9
                         + x_OC_0_PORT_0_DEP_(101,_1)#12
                         + x_OC_1_PORT_0_DEP_(101,_1)#15 <= -30
 Cap_D(101,_2)#22:       - 150 y_DEP_101,2_NF#4 + x_OC_0_IMP_0_DEP_(101,_2)#7
                         + x_OC_1_IMP_0_DEP_(101,_2)#10
                         + x_OC_0_PORT_0_DEP_(101,_2)#13
                         + x_OC_1_PORT_0_DEP_(101,_2)#16 <= -45
 Cap_D(202,_3)#23:       - 200 y_DEP_202,3_EF#5 + x_OC_0_IMP_0_DEP_(202,_3)#8
                         + x_OC_1_IMP_0_DEP_(202,_3)#11
                         + x_OC_0_PORT_0_DEP_(202,_3)#14
                         + x_OC_1_PORT_0_DEP_(202,_3)#17 <= -20
Bounds
 0 <= y_DEP_101,1_ES#0 <= 1
 0 <= y_DEP_101,2_NS#1 <= 1
 0 <= y_DEP_202,3_ES#2 <= 1
 0 <= y_DEP_101,1_EF#3 <= 1
 0 <= y_DEP_101,2_NF#4 <= 1
 0 <= y_DEP_202,3_EF#5 <= 1
      x_OC_0_IMP_0_DEP_(101,_1)#6 >= 0
      x_OC_0_IMP_0_DEP_(101,_2)#7 >= 0
      x_OC_0_IMP_0_DEP_(202,_3)#8 >= 0
      x_OC_1_IMP_0_DEP_(101,_1)#9 >= 0
      x_OC_1_IMP_0_DEP_(101,_2)#10 >= 0
      x_OC_1_IMP_0_DEP_(202,_3)#11 >= 0
      x_OC_0_PORT_0_DEP_(101,_1)#12 >= 0
      x_OC_0_PORT_0_DEP_(101,_2)#13 >= 0
      x_OC_0_PORT_0_DEP_(202,_3)#14 >= 0
      x_OC_1_PORT_0_DEP_(101,_1)#15 >= 0
      x_OC_1_PORT_0_DEP_(101,_2)#16 >= 0
      x_OC_1_PORT_0_DEP_(202,_3)#17 >= 0
      x_OC_0_DEP_(101,_1)_EXP_0#18 >= 0
      x_OC_0_DEP_(101,_2)_EXP_0#19 >= 0
      x_OC_0_DEP_(202,_3)_EXP_0#20 >= 0
      x_OC_1_DEP_(101,_1)_EXP_0#21 >= 0
      x_OC_1_DEP_(101,_2)_EXP_0#22 >= 0
      x_OC_1_DEP_(202,_3)_EXP_0#23 >= 0
      x_OC_0_DEP_(101,_1)_PORT_0#24 >= 0
      x_OC_0_DEP_(101,_2)_PORT_0#25 >= 0
      x_OC_0_DEP_(202,_3)_PORT_0#26 >= 0
      x_OC_1_DEP_(101,_1)_PORT_0#27 >= 0
      x_OC_1_DEP_(101,_2)_PORT_0#28 >= 0
      x_OC_1_DEP_(202,_3)_PORT_0#29 >= 0
      F_Invent_OC_0_DEP_(101,_1)#30 >= 0
      F_Invent_OC_0_DEP_(101,_2)#31 >= 0
      F_Invent_OC_0_DEP_(202,_3)#32 >= 0
      F_Invent_OC_1_DEP_(101,_1)#33 >= 0
      F_Invent_OC_1_DEP_(101,_2)#34 >= 0
      F_Invent_OC_1_DEP_(202,_3)#35 >= 0
Binaries
 y_DEP_101,1_ES#0  y_DEP_101,2_NS#1  y_DEP_202,3_ES#2  y_DEP_101,1_EF#3 
 y_DEP_101,2_NF#4  y_DEP_202,3_EF#5 
Generals
 x_OC_0_IMP_0_DEP_(101,_1)#6  x_OC_0_IMP_0_DEP_(101,_2)#7 
 x_OC_0_IMP_0_DEP_(202,_3)#8  x_OC_1_IMP_0_DEP_(101,_1)#9 
 x_OC_1_IMP_0_DEP_(101,_2)#10  x_OC_1_IMP_0_DEP_(202,_3)#11 
 x_OC_0_PORT_0_DEP_(101,_1)#12  x_OC_0_PORT_0_DEP_(101,_2)#13 
 x_OC_0_PORT_0_DEP_(202,_3)#14  x_OC_1_PORT_0_DEP_(101,_1)#15 
 x_OC_1_PORT_0_DEP_(101,_2)#16  x_OC_1_PORT_0_DEP_(202,_3)#17 
 x_OC_0_DEP_(101,_1)_EXP_0#18  x_OC_0_DEP_(101,_2)_EXP_0#19 
 x_OC_0_DEP_(202,_3)_EXP_0#20  x_OC_1_DEP_(101,_1)_EXP_0#21 
 x_OC_1_DEP_(101,_2)_EXP_0#22  x_OC_1_DEP_(202,_3)_EXP_0#23 
 x_OC_0_DEP_(101,_1)_PORT_0#24  x_OC_0_DEP_(101,_2)_PORT_0#25 
 x_OC_0_DEP_(202,_3)_PORT_0#26  x_OC_1_DEP_(101,_1)_PORT_0#27 
 x_OC_1_DEP_(101,_2)_PORT_0#28  x_OC_1_DEP_(202,_3)_PORT_0#29 
 F_Invent_OC_0_DEP_(101,_1)#30  F_Invent_OC_0_DEP_(101,_2)#31 
 F_Invent_OC_0_DEP_(202,_3)#32  F_Invent_OC_1_DEP_(101,_1)#33 
 F_Invent_OC_1_DEP_(101,_2)#34  F_Invent_OC_1_DEP_(202,_3)#35 
End
