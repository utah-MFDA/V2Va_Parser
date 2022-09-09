
#import PySpice as sp

from hspiceParser import import_export

inputFile = "./smart_toilet/smart_toilet_o.tr0"
outputFile= "./smart_toilet/smart_toilet_o"

import_export(inputFile, outputFile)