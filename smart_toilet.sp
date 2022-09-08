* Converted from verilog for microfluidic simulation

.option post=1

.hdl ./../component_library/VerilogA/Elibrary/standardCells/Evalve_20px_1.va
.hdl ./../component_library/VerilogA/Elibrary/standardCells/Eserpentine_25px_0.va
.hdl ./../component_library/VerilogA/Elibrary/standardCells/Eserpentine_50px_0.va
.hdl ./../component_library/VerilogA/Elibrary/standardCells/Eserpentine_75px_0.va
.hdl ./../component_library/VerilogA/Elibrary/standardCells/Eserpentine_100px_0.va
.hdl ./../component_library/VerilogA/Elibrary/standardCells/Eserpentine_150px_0.va
.hdl ./../component_library/VerilogA/Elibrary/standardCells/Eserpentine_200px_0.va
.hdl ./../component_library/VerilogA/Elibrary/standardCells/Eserpentine_300px_0.va
.hdl ./../component_library/VerilogA/Elibrary/standardCells/Ediffmix_25px_0.va


X0 soln1 soln1c PressurePump pressure=100k 
X1 soln2 soln2c PressurePump pressure=100k 
X2 soln3 soln3c PressurePump pressure=100k 

X3 connect1_0 connect1_1 EChannel length=1.18
X4 connect2_0 connect2_1 EChannel length=1.18
X5 connect3_0 connect3_1 EChannel length=2.15
X6 connect4_0 connect4_1 EChannel length=3.27
X7 connect5_0 connect5_1 EChannel length=15.05
X8 connect6_0 connect6_1 EChannel length=4.41
X9 connect7_0 connect7_1 EChannel length=2.68
X10 soln2 connect1_0 soln2c connect1_0c serpentine_50px_0
X11 connect1_1 connect2_0 connect1_1c connect2_0c serpentine_150px_0
X12 soln1 connect2_1 connect3_0 soln1c connect2_1c connect3_0c diffmix_25px_0
X13 soln3 connect4_0 soln3c connect4_0c serpentine_300px_0
X14 connect4_1 connect5_0 connect4_1c connect5_0c serpentine_300px_0
X15 connect5_1 connect6_0 connect5_1c connect6_0c serpentine_300px_0
X16 connect3_1 connect6_1 connect7_0 connect3_1c connect6_1c connect7_0c diffmix_25px_0
X17 connect7_1 out connect7_1c outc serpentine_300px_0

.tran 0.01ms 1ms