
#import PySpice as sp

from hspiceParser import import_export
import numpy as np
import pandas as pd

TRdata = []
TR_c   = []

outputC = " v_outc"

for i in range(1,4):
    inputFileBase = "./smart_toilet_soln"+str(i)+"/smart_toilet_soln" + str(i) + "_o.tr0"
    csvFile= "./smart_toilet_soln"+str(i)+"/smart_toilet_soln" + str(i) + "_o_tr0.csv"

    import_export(inputFileBase, "csv")

    df = pd.read_csv(csvFile, delimiter = ",")

    TRdata.append(df)

    print(df.columns)

    TR_c.append(df.loc[:0, outputC])

    
pass
