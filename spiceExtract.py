
#import PySpice as sp

from hspiceParser import import_export

inputFile = "./smart_toilet_soln1/smart_toilet_soln1_o.tr0"
outputFile= "./smart_toilet_soln1/smart_toilet_soln1_o"

import_export(inputFile, outputFile)