\ENCODING=ISO-8859-1
\Problem name: 

Minimize
 obj: 100 time_1_carr_0_owner_0_DEPOT_N_0 - 100 time_0_carr_0_owner_0_DEPOT_N_0
      + 20 vol_time_0_carr_0_IMP_0_own_0_DEPOT_0
      + 10 vol_time_0_carr_0_IMP_0_own_0_DEPOT_1
      + 20 vol_time_1_carr_0_IMP_0_own_0_DEPOT_0
      + 10 vol_time_1_carr_0_IMP_0_own_0_DEPOT_1
      + 20 vol_time_0_carr_0_DEPOT_0_own_0_EXPORT_0
      + 16 vol_time_0_carr_0_DEPOT_1_own_0_EXPORT_0
      + 20 vol_time_1_carr_0_DEPOT_0_own_0_EXPORT_0
      + 16 vol_time_1_carr_0_DEPOT_1_own_0_EXPORT_0
      + 20 vol_time_0_carr_0_DEPOT_0_own_0_PORT_0
      + 30 vol_time_0_carr_0_DEPOT_1_own_0_PORT_0
      + 20 vol_time_1_carr_0_DEPOT_0_own_0_PORT_0
      + 30 vol_time_1_carr_0_DEPOT_1_own_0_PORT_0
      + 20 vol_time_0_carr_0_PORT_0_own_0_DEPOT_0
      + 14 vol_time_0_carr_0_PORT_0_own_0_DEPOT_1
      + 20 vol_time_1_carr_0_PORT_0_own_0_DEPOT_0
      + 14 vol_time_1_carr_0_PORT_0_own_0_DEPOT_1
Subject To
 Depot_Open_0:             time_1_carr_0_owner_0_DEPOT_E_0
                           - time_0_carr_0_owner_0_DEPOT_E_0 >= 0
 Depot_Open_1:             time_1_carr_0_owner_0_DEPOT_N_0
                           - time_0_carr_0_owner_0_DEPOT_N_0 >= 0
 Depot_E_0:                time_0_carr_0_owner_0_DEPOT_E_0  = 1
 Depot_E_0:                time_1_carr_0_owner_0_DEPOT_E_0  = 1
 supply_IM_0_t_0:          vol_time_0_carr_0_IMP_0_own_0_DEPOT_0
                           + vol_time_0_carr_0_IMP_0_own_0_DEPOT_1  = 50
 supply_IM_0_t_1:          vol_time_1_carr_0_IMP_0_own_0_DEPOT_0
                           + vol_time_1_carr_0_IMP_0_own_0_DEPOT_1  = 55
 supply_P_0_t_0:           vol_time_0_carr_0_PORT_0_own_0_DEPOT_0
                           + vol_time_0_carr_0_PORT_0_own_0_DEPOT_1  = 80
 supply_P_0_t_1:           vol_time_1_carr_0_PORT_0_own_0_DEPOT_0
                           + vol_time_1_carr_0_PORT_0_own_0_DEPOT_1  = 75
 demand_EX_0_t_0:          vol_time_0_carr_0_DEPOT_0_own_0_EXPORT_0
                           + vol_time_0_carr_0_DEPOT_1_own_0_EXPORT_0  = 70
 demand_EX_0_t_1:          vol_time_1_carr_0_DEPOT_0_own_0_EXPORT_0
                           + vol_time_1_carr_0_DEPOT_1_own_0_EXPORT_0  = 65
 demand_P_0_t_0:           vol_time_0_carr_0_DEPOT_0_own_0_PORT_0
                           + vol_time_0_carr_0_DEPOT_1_own_0_PORT_0  = 60
 demand_P_0_t_1:           vol_time_1_carr_0_DEPOT_0_own_0_PORT_0
                           + vol_time_1_carr_0_DEPOT_1_own_0_PORT_0  = 65
 Inventory_D_0_t_0:        Inventory_time_0_carr_0_own_0_DEPOT_0  = 20
 Inventory_D_1_t_0:        Inventory_time_0_carr_0_own_0_DEPOT_1  = 0
 Inventory_update_D_0_t_0: - vol_time_0_carr_0_IMP_0_own_0_DEPOT_0
                           + vol_time_0_carr_0_DEPOT_0_own_0_EXPORT_0
                           + vol_time_0_carr_0_DEPOT_0_own_0_PORT_0
                           - vol_time_0_carr_0_PORT_0_own_0_DEPOT_0
                           - Inventory_time_0_carr_0_own_0_DEPOT_0
                           + Inventory_time_1_carr_0_own_0_DEPOT_0  = 0
 Inventory_update_D_1_t_0: - vol_time_0_carr_0_IMP_0_own_0_DEPOT_1
                           + vol_time_0_carr_0_DEPOT_1_own_0_EXPORT_0
                           + vol_time_0_carr_0_DEPOT_1_own_0_PORT_0
                           - vol_time_0_carr_0_PORT_0_own_0_DEPOT_1
                           - Inventory_time_0_carr_0_own_0_DEPOT_1
                           + Inventory_time_1_carr_0_own_0_DEPOT_1  = 0
 Cap_D_0_Own_0_t_0:        - 80 time_0_carr_0_owner_0_DEPOT_E_0
                           + vol_time_0_carr_0_IMP_0_own_0_DEPOT_0
                           + vol_time_0_carr_0_PORT_0_own_0_DEPOT_0
                           + Inventory_time_0_carr_0_own_0_DEPOT_0 <= 0
 Cap_D_1_Own_0_t_0:        - 70 time_0_carr_0_owner_0_DEPOT_N_0
                           + vol_time_0_carr_0_IMP_0_own_0_DEPOT_1
                           + vol_time_0_carr_0_PORT_0_own_0_DEPOT_1
                           + Inventory_time_0_carr_0_own_0_DEPOT_1 <= 0
 Cap_D_0_Own_0_t_1:        - 80 time_1_carr_0_owner_0_DEPOT_E_0
                           + vol_time_1_carr_0_IMP_0_own_0_DEPOT_0
                           + vol_time_1_carr_0_PORT_0_own_0_DEPOT_0
                           + Inventory_time_1_carr_0_own_0_DEPOT_0 <= 0
 Cap_D_1_Own_0_t_1:        - 70 time_1_carr_0_owner_0_DEPOT_N_0
                           + vol_time_1_carr_0_IMP_0_own_0_DEPOT_1
                           + vol_time_1_carr_0_PORT_0_own_0_DEPOT_1
                           + Inventory_time_1_carr_0_own_0_DEPOT_1 <= 0
 Budget_D_1_Owner_0:       100 time_0_carr_0_owner_0_DEPOT_N_0 <= 100
 Budget_D_1_Owner_0:       100 time_1_carr_0_owner_0_DEPOT_N_0 <= 110
Bounds
 0 <= time_1_carr_0_owner_0_DEPOT_E_0 <= 1
 0 <= time_1_carr_0_owner_0_DEPOT_N_0 <= 1
 0 <= time_0_carr_0_owner_0_DEPOT_E_0 <= 1
 0 <= time_0_carr_0_owner_0_DEPOT_N_0 <= 1
      vol_time_0_carr_0_IMP_0_own_0_DEPOT_0 >= 0
      vol_time_0_carr_0_IMP_0_own_0_DEPOT_1 >= 0
      vol_time_1_carr_0_IMP_0_own_0_DEPOT_0 >= 0
      vol_time_1_carr_0_IMP_0_own_0_DEPOT_1 >= 0
      vol_time_0_carr_0_DEPOT_0_own_0_EXPORT_0 >= 0
      vol_time_0_carr_0_DEPOT_1_own_0_EXPORT_0 >= 0
      vol_time_1_carr_0_DEPOT_0_own_0_EXPORT_0 >= 0
      vol_time_1_carr_0_DEPOT_1_own_0_EXPORT_0 >= 0
      vol_time_0_carr_0_DEPOT_0_own_0_PORT_0 >= 0
      vol_time_0_carr_0_DEPOT_1_own_0_PORT_0 >= 0
      vol_time_1_carr_0_DEPOT_0_own_0_PORT_0 >= 0
      vol_time_1_carr_0_DEPOT_1_own_0_PORT_0 >= 0
      vol_time_0_carr_0_PORT_0_own_0_DEPOT_0 >= 0
      vol_time_0_carr_0_PORT_0_own_0_DEPOT_1 >= 0
      vol_time_1_carr_0_PORT_0_own_0_DEPOT_0 >= 0
      vol_time_1_carr_0_PORT_0_own_0_DEPOT_1 >= 0
      Inventory_time_0_carr_0_own_0_DEPOT_0 >= 0
      Inventory_time_0_carr_0_own_0_DEPOT_1 >= 0
      Inventory_time_1_carr_0_own_0_DEPOT_0 >= 0
      Inventory_time_1_carr_0_own_0_DEPOT_1 >= 0
Binaries
 time_1_carr_0_owner_0_DEPOT_E_0  time_1_carr_0_owner_0_DEPOT_N_0 
 time_0_carr_0_owner_0_DEPOT_E_0  time_0_carr_0_owner_0_DEPOT_N_0 
Generals
 vol_time_0_carr_0_IMP_0_own_0_DEPOT_0  vol_time_0_carr_0_IMP_0_own_0_DEPOT_1 
 vol_time_1_carr_0_IMP_0_own_0_DEPOT_0  vol_time_1_carr_0_IMP_0_own_0_DEPOT_1 
 vol_time_0_carr_0_DEPOT_0_own_0_EXPORT_0 
 vol_time_0_carr_0_DEPOT_1_own_0_EXPORT_0 
 vol_time_1_carr_0_DEPOT_0_own_0_EXPORT_0 
 vol_time_1_carr_0_DEPOT_1_own_0_EXPORT_0 
 vol_time_0_carr_0_DEPOT_0_own_0_PORT_0 
 vol_time_0_carr_0_DEPOT_1_own_0_PORT_0 
 vol_time_1_carr_0_DEPOT_0_own_0_PORT_0 
 vol_time_1_carr_0_DEPOT_1_own_0_PORT_0 
 vol_time_0_carr_0_PORT_0_own_0_DEPOT_0 
 vol_time_0_carr_0_PORT_0_own_0_DEPOT_1 
 vol_time_1_carr_0_PORT_0_own_0_DEPOT_0 
 vol_time_1_carr_0_PORT_0_own_0_DEPOT_1  Inventory_time_0_carr_0_own_0_DEPOT_0 
 Inventory_time_0_carr_0_own_0_DEPOT_1  Inventory_time_1_carr_0_own_0_DEPOT_0 
 Inventory_time_1_carr_0_own_0_DEPOT_1 
End
