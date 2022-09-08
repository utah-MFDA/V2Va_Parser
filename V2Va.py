
import numpy as np
import pandas as pd
import re

inFile_Verilog = "smart_toilet.v"
inFile_lengths = "smart_toilet_lengths.xlsx"
library_csv =    "StandardCellLibrary.csv"
outFile_sp     = inFile_Verilog[:-2] + '.sp'

initExpress    = "initExpression_V2VA"
endExpress     = "endExpression_V2VA"

outfile_VA = inFile_Verilog[:-1] + 'va'

Vfile = open(inFile_Verilog)
SPfile= open(outFile_sp, '+w')
iExp  = open(initExpress)
eExp  = open(endExpress)

libraryPath = "./../component_library/VerilogA/Elibrary/standardCells/"

# Load standard cell library

library = pd.read_csv(library_csv)
wireLenDF = pd.read_excel(inFile_lengths)

SPfile.write(''.join(iExp.readlines()))

# import library files
for rowN, row in enumerate(library.iterrows()):
    #if rowN == 0:
    #    continue
    rStr = row[1]['Standard_Cell']
    libStr = '.hdl ' + libraryPath + rStr + '\n'
    SPfile.write(libStr)

SPfile.write('\n\n')

numberOfComponents = 0
currentLine = ''
wireList    = {}
outputWords = []


# get line
for line_num, line in enumerate(Vfile):

    if len(line) > 0 and not(line == '\n'):
        if not line.rstrip()[-1] == ';':
            # append to current line
            # remove comments
            if '//' in line:
                line = line.split('//')[0]
            currentLine += line
            continue
        else:
            # pass to parser
            currentLine += line
            line = currentLine
    else:
        continue

    # remove inital whitespace
    line = line.lstrip(' ').replace(';', '').replace('\n', '')
    vars = line.split(' ')[0]
 
    VA_line_str = ''


    if vars == 'input':

        # create pump devices
        # we will assume pressure pumping devices
        params = line.replace('input ', '').replace(' ', '').split(',')
        for p in params:
            VA_line_str += 'X' + str(numberOfComponents) + ' ' + str(p) + ' ' + str(p) + 'c PressurePump pressure=100k \n'
            numberOfComponents += 1
        
        VA_line_str += '\n'

    elif vars == 'output':
        outputLine = line.replace('output ', '')
        for out in line.replace(' ', '').split(','):
            outputWords.append(out)

    elif vars == 'module':
        pass
    
    elif vars == 'wire':
        # create channel modules
        wires = line.replace('wire ', '').replace(' ', '').split(',')
        
        #
        init_wire_string = '*Declared wires'
        
        for w in wires:
            # get length of connection

            # string
            VA_line_str += 'X' + str(numberOfComponents) + ' ' + str(w) + '_0 ' + str(w) + '_1 ' + 'EChannel length='

            row = wireLenDF.loc[wireLenDF['wire'] == w]

            wireLength = row.iloc[0,1]

            VA_line_str += str(wireLength) + '\n'

            outFile_sp

            wireList[w] = 0

            numberOfComponents += 1
        #pass
    elif vars == 'endmodule':
        pass


    # variable is a standard cell
    else:
        #line_var = line.lstrip().split(' ')[0]

        # check if in library
        if (library['Standard_Cell'].eq(vars)).any():
            standardCell = vars[0]
        
            ioPara = ''.join(line.replace('  ', ' ').split(' ')[2:])

            io_expression = False
            connectionWord= False
            portPhrase = ''
            ports      = []

            for char in ioPara:
                if not io_expression and not connectionWord and char == '.':
                    io_expression = True
                elif io_expression and not connectionWord and char == '(':
                    #Start connection word
                    io_expression = False
                    connectionWord = True
                elif not io_expression and connectionWord and char == ')':
                    #end of port word
                    io_expression = False
                    connectionWord= False
                    ports.append(portPhrase)
                    portPhrase = ''
                elif not io_expression and connectionWord:
                    portPhrase += char

            VA_line_str += 'X' + str(numberOfComponents) + ' '
            VA_line_str_chem = ''

            for p in ports:
                if p in wireList.keys():
                    VA_line_str += str(p) + '_' + str(wireList[p]) + ' '
                    VA_line_str_chem += str(p) + '_' + str(wireList[p]) + 'c '
                    wireList[p] += 1
                else:
                    VA_line_str += str(p) + ' '
                    VA_line_str_chem += str(p) + 'c '

                
            VA_line_str += VA_line_str_chem + vars + '\n'

            numberOfComponents += 1

        else:
            print("String: " + vars + " line number: " + str(line_num) + " not in library.")

    # Write line to file
    SPfile.write(VA_line_str)
    # refresh line every pass
    currentLine = ''

SPfile.write(''.join(eExp.readlines()))