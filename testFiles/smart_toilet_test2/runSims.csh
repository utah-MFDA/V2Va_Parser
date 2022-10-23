#/bin/tcsh

mkdir ./V2Va_Parser/testFiles/smart_toilet_test2/smart_toilet2_soln1
hspice ./V2Va_Parser/testFiles/smart_toilet_test2/smart_toilet2_soln1.sp -o ./V2Va_Parser/testFiles/smart_toilet_test2/smart_toilet2_soln1/smart_toilet2_soln1_o

mkdir ./V2Va_Parser/testFiles/smart_toilet_test2/smart_toilet2_soln2
hspice ./V2Va_Parser/testFiles/smart_toilet_test2/smart_toilet2_soln2.sp -o ./V2Va_Parser/testFiles/smart_toilet_test2/smart_toilet2_soln2/smart_toilet2_soln2_o

mkdir ./V2Va_Parser/testFiles/smart_toilet_test2/smart_toilet2_soln3
hspice ./V2Va_Parser/testFiles/smart_toilet_test2/smart_toilet2_soln3.sp -o ./V2Va_Parser/testFiles/smart_toilet_test2/smart_toilet2_soln3/smart_toilet2_soln3_o

