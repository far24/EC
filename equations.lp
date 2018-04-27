\ENCODING=ISO-8859-1
\Problem name: 

Minimize
 obj: 200 y_DEP_101,2_NF#4 + 10 x_OC_0_IMP_0_DEP_(101,_1)#6
      + 15 x_OC_0_IMP_0_DEP_(101,_2)#7 + 20 x_OC_0_IMP_0_DEP_(202,_3)#8
      + 20 x_OC_0_PORT_0_DEP_(101,_1)#9 + 25 x_OC_0_PORT_0_DEP_(101,_2)#10
      + 30 x_OC_0_PORT_0_DEP_(202,_3)#11 + 20 x_OC_0_DEP_(101,_1)_EXP_0#12
      + 25 x_OC_0_DEP_(101,_2)_EXP_0#13 + 30 x_OC_0_DEP_(202,_3)_EXP_0#14
      + 20 x_OC_0_DEP_(101,_1)_PORT_0#15 + 25 x_OC_0_DEP_(101,_2)_PORT_0#16
      + 30 x_OC_0_DEP_(202,_3)_PORT_0#17
Subject To
 _ES#0:                  y_DEP_101,1_ES#0  = 1
 _ES#1:                  y_DEP_202,3_ES#2  = 1
 FS#2:                   y_DEP_101,1_EF#3  = 1
 FS#3:                   y_DEP_202,3_EF#5  = 1
 NS#4:                   - y_DEP_101,2_NS#1 + y_DEP_101,2_NF#4  = 0
 supply_IMP_0_OC_0#5:    x_OC_0_IMP_0_DEP_(101,_1)#6
                         + x_OC_0_IMP_0_DEP_(101,_2)#7
                         + x_OC_0_IMP_0_DEP_(202,_3)#8  = 40
 supply_PORT_0_OC_0#6:   x_OC_0_PORT_0_DEP_(101,_1)#9
                         + x_OC_0_PORT_0_DEP_(101,_2)#10
                         + x_OC_0_PORT_0_DEP_(202,_3)#11  = 60
 Demand_EXP_0_OC_0#7:    x_OC_0_DEP_(101,_1)_EXP_0#12
                         + x_OC_0_DEP_(101,_2)_EXP_0#13
                         + x_OC_0_DEP_(202,_3)_EXP_0#14  = 30
 Demand_PORT_0_OC_0#8:   x_OC_0_DEP_(101,_1)_PORT_0#15
                         + x_OC_0_DEP_(101,_2)_PORT_0#16
                         + x_OC_0_DEP_(202,_3)_PORT_0#17  = 75
 F_Invent_DEP_0_OC_0#9:  - x_OC_0_IMP_0_DEP_(101,_1)#6
                         - x_OC_0_PORT_0_DEP_(101,_1)#9
                         + x_OC_0_DEP_(101,_1)_EXP_0#12
                         + x_OC_0_DEP_(101,_1)_PORT_0#15
                         + F_Invent_OC_0_DEP_(101,_1)#18  = 10
 F_Invent_DEP_1_OC_0#10: - x_OC_0_IMP_0_DEP_(101,_2)#7
                         - x_OC_0_PORT_0_DEP_(101,_2)#10
                         + x_OC_0_DEP_(101,_2)_EXP_0#13
                         + x_OC_0_DEP_(101,_2)_PORT_0#16
                         + F_Invent_OC_0_DEP_(101,_2)#19  = 0
 F_Invent_DEP_2_OC_0#11: - x_OC_0_IMP_0_DEP_(202,_3)#8
                         - x_OC_0_PORT_0_DEP_(202,_3)#11
                         + x_OC_0_DEP_(202,_3)_EXP_0#14
                         + x_OC_0_DEP_(202,_3)_PORT_0#17
                         + F_Invent_OC_0_DEP_(202,_3)#20  = 0
 Cap_D(101,_1)#12:       - 80 y_DEP_101,1_EF#3 + x_OC_0_IMP_0_DEP_(101,_1)#6
                         + x_OC_0_PORT_0_DEP_(101,_1)#9 <= -10
 Cap_D(101,_2)#13:       - 70 y_DEP_101,2_NF#4 + x_OC_0_IMP_0_DEP_(101,_2)#7
                         + x_OC_0_PORT_0_DEP_(101,_2)#10 <= 0
 Cap_D(202,_3)#14:       - 50 y_DEP_202,3_EF#5 + x_OC_0_IMP_0_DEP_(202,_3)#8
                         + x_OC_0_PORT_0_DEP_(202,_3)#11 <= 0
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
      x_OC_0_PORT_0_DEP_(101,_1)#9 >= 0
      x_OC_0_PORT_0_DEP_(101,_2)#10 >= 0
      x_OC_0_PORT_0_DEP_(202,_3)#11 >= 0
      x_OC_0_DEP_(101,_1)_EXP_0#12 >= 0
      x_OC_0_DEP_(101,_2)_EXP_0#13 >= 0
      x_OC_0_DEP_(202,_3)_EXP_0#14 >= 0
      x_OC_0_DEP_(101,_1)_PORT_0#15 >= 0
      x_OC_0_DEP_(101,_2)_PORT_0#16 >= 0
      x_OC_0_DEP_(202,_3)_PORT_0#17 >= 0
      F_Invent_OC_0_DEP_(101,_1)#18 >= 0
      F_Invent_OC_0_DEP_(101,_2)#19 >= 0
      F_Invent_OC_0_DEP_(202,_3)#20 >= 0
Binaries
 y_DEP_101,1_ES#0  y_DEP_101,2_NS#1  y_DEP_202,3_ES#2  y_DEP_101,1_EF#3 
 y_DEP_101,2_NF#4  y_DEP_202,3_EF#5 
Generals
 x_OC_0_IMP_0_DEP_(101,_1)#6  x_OC_0_IMP_0_DEP_(101,_2)#7 
 x_OC_0_IMP_0_DEP_(202,_3)#8  x_OC_0_PORT_0_DEP_(101,_1)#9 
 x_OC_0_PORT_0_DEP_(101,_2)#10  x_OC_0_PORT_0_DEP_(202,_3)#11 
 x_OC_0_DEP_(101,_1)_EXP_0#12  x_OC_0_DEP_(101,_2)_EXP_0#13 
 x_OC_0_DEP_(202,_3)_EXP_0#14  x_OC_0_DEP_(101,_1)_PORT_0#15 
 x_OC_0_DEP_(101,_2)_PORT_0#16  x_OC_0_DEP_(202,_3)_PORT_0#17 
 F_Invent_OC_0_DEP_(101,_1)#18  F_Invent_OC_0_DEP_(101,_2)#19 
 F_Invent_OC_0_DEP_(202,_3)#20 
End
