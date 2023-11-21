
#import numpy as np
import sys
import pandas as pd
import re
import json
import os

"""
input arguments

input file, or -i; input file can be v or vmf
output file, or -o; the output file is .va if no argument is given
length file, or -l; assumed name with .xlsx or csv
library file, or -lib; this can be written into the vmf file
template file, or -mfsp; this adds additional start and ending file information
"""

def Verilog2VerilogA(inputVerilogFile, 
                     configFile, 
                     solnDF, 
                     remoteTestPath,    
                     libraryFile=None,
                     devDF=None, 
                     length_file=None,
                     timeDF=None,
                     preRouteSim=False, 
                     outputVerilogFile=None,
                     parser="XYCE", 
                     runScipt=True):

    inputVerilogFile = inputVerilogFile.replace('\\', '/')
    # input file declaration
    #inFile_Verilog = "smart_toilet.v"
    inFile_Verilog = inputVerilogFile
    #inFile_lengths = "smart_toilet_lengths.xlsx"
    print('\n\n----------------------------------------------------------')
    print("PreRoute:" + str(preRouteSim) + "")
    print('----------------------------------------------------------\n\n')

    if not preRouteSim:
        if length_file == None:
            inFile_lengths = inputVerilogFile[:-2] + "_lengths.xlsx"
        else:
            inFile_lengths = length_file
 
    # import library file
    if libraryFile==None:
        library_csv =    "StandardCellLibrary.csv"
    else:
        library_csv = libraryFile

    # output file declaration
    if outputVerilogFile == None:
        outFile_sp     = inFile_Verilog[:-2] + '.sp'

    # files for start and ending expressions
    #configFile     = "VMF_template.mfsp"
    initExpress    = "initExpression_V2VA"
    endExpress     = "endExpression_V2VA"

    outfile_VA = inFile_Verilog[:-1] + 'va'

    # local library location for testing

    libraryPath = "~/Github/component_library/VerilogA/Elibrary/standardCells/"
    #libraryPath2= "~/Github/component_library/VerilogA/Elibrary/"

    # --------------------------------------------------------------
    # open files
    # --------------------------------------------------------------

    # Verilog file
    Vfile = open(inFile_Verilog)
    #SPfile= open(outFile_sp, '+w')
    with open(configFile, 'r') as f:
        configFile = json.load(f)

    #print(configFile["START"])

    iExp  = configFile["START"]
    eExp  = configFile["END"]


    # Load standard cell library
    library = pd.read_csv(library_csv)
    wireLenDF = None
    if not preRouteSim:
        wireLenDF = pd.read_excel(inFile_lengths)
        # Catches unnamed wire length column
        if wireLenDF.columns.tolist()[0] == 'Unnamed: 0':
            wireLenDF=wireLenDF.rename(columns={'Unnamed: 0':'wire'})


    # load solution concentrations
    #solnDF = pd.read_csv(solnFile)
    # used to keep track of appending to run sim file
    numSoln = 0

    # load device file ------------------------------------
    #devDF = pd.read_csv(devFile)

    # load time file
    #timeDF = pd.read_csv(timeFile)

    #SP_file_list = 
    # write to spice files
    # path/newfile/file.v
    #SP_outputFile_name = inFile_Verilog[:-2] + '_' + soln[1].loc['inlet'] + '.sp'
    SP_outputFile_pathA= inFile_Verilog.split('/')[:-1]
    SP_outputFile_path = ""

    for s in SP_outputFile_pathA: SP_outputFile_path += s + "/"

    

    if preRouteSim:
        SP_outputFile_path = SP_outputFile_path + "spiceFiles/preRoute/" 
        SP_outputFile_name = SP_outputFile_path + 'preR_' + inFile_Verilog.split('/')[-1]
    else:
        SP_outputFile_path = SP_outputFile_path + "spiceFiles/" 
        SP_outputFile_name = SP_outputFile_path + inFile_Verilog.split('/')[-1]

    if not os.path.exists(SP_outputFile_path):
        os.mkdir(SP_outputFile_path)

    SP_outputFile_list = SP_outputFile_path + "spiceList"
    SP_list = open(SP_outputFile_list, 'w')
    SP_list.write('OutputFile,Chemical,Outlets\n')

    # Create soln files
    createChemSubArrays(solnDF)

    #for soln in solnDF.iterrows():
    for soln in solnDF.groupby(['Solution']):
        Vfile = open(inFile_Verilog)
        #iExp  = open(initExpress)
        #eExp  = open(endExpress)

        chem = str(soln[0][0])
        chemDF = soln[1]

        # write to spice files
        # path/newfile/file.v
        if(parser=="HSPICE"):
            #SP_outputFile_name_new = SP_outputFile_name[:-2] + '_' + soln[1].loc['inlet'] + '.sp'
            SP_outputFile_name_new = SP_outputFile_name[:-2] + '_' + chem + '.sp'
        if(parser=="XYCE"):
            #SP_outputFile_name_new = SP_outputFile_name[:-2] + '_' + soln[1].loc['inlet'] + '.cir'
            SP_outputFile_name_new = SP_outputFile_name[:-2] + '_' + chem + '.cir'

        SPfile = open(SP_outputFile_name_new, '+w')
        if parser == "HSPICE":
            SP_list.write(SP_outputFile_name_new)
        elif parser == "XYCE":
            SP_list.write(os.path.basename(SP_outputFile_name_new))
        SP_list.write(','+chem+',')
        
        #SPfile.write(''.join(iExp.readlines()))
        SPfile.write(iExp)

        if(runScipt):
            createSpiceRunScript(SP_outputFile_name_new[:-3], numSoln, remoteTestPath)
            numSoln += 1

        # import library files in sp scripts
        if(parser=="HSPICE"):
            hspice_lib_import(SPfile, library, libraryPath)
            
        numberOfComponents = 0
        currentLine = ''
        # wire list used to keep track of number of connections
        wireList    = {}
        inputList   = []
        outputWords = []
        outNum      = 0
        probeList   = {}



        # get line
        for line_num, line in enumerate(Vfile):

            # combines lines until end char
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
            # split different variables for line
            vars = line.split(' ')[0]
        
            VA_line_str = ''


            if vars == 'input':

                VA_line_str, numberOfComponents, inputList = parseInput(
                    vars, 
                    line, 
                    numberOfComponents, 
                    soln, 
                    inputList, 
                    wireLenDF,
                    chemDF,
                    devDF,
                    preRouteSim=preRouteSim, 
                    parser=parser)
                
                VA_line_str += '\n'

            elif vars == 'output':
                VA_line_str, numberOfComponents, outNum = praseOutput(
                    vars, 
                    line, 
                    numberOfComponents, 
                    soln, 
                    outputWords, 
                    wireLenDF, 
                    SP_list,
                    outNum,
                    preRouteSim=preRouteSim,
                    parser=parser)


            elif vars == 'module':
                pass
            
            elif vars == 'wire':

                VA_line_str, numberOfComponents = parseWire(
                    vars, 
                    line, 
                    line_num, 
                    wireList, 
                    wireLenDF, 
                    numberOfComponents,
                    preRouteSim=preRouteSim,
                    parser=parser)
                
            elif vars == 'endmodule':
                pass


            # variable is a standard cell
            else:
                #line_var = line.lstrip().split(' ')[0]
                VA_line_str, numberOfComponents = parseSTDCell(
                    vars, 
                    line, 
                    line_num, 
                    library, 
                    wireList, 
                    inputList, 
                    outputWords, 
                    numberOfComponents, 
                    parser=parser) 
                
            # Write line to file
            SPfile.write(VA_line_str)
            # refresh line every pass
            currentLine = ''

        SPfile.write(simulationTime(timeDF, outputWords))

        #SPfile.write(''.join(eExp.readlines()))
        SPfile.write(eExp)

## -------------------------------------------------------------------------------------
#   Smaller methods
## -------------------------------------------------------------------------------------

"""

"""

def parseInput(vars, 
               line, 
               numberOfComponents, 
               soln, 
               inputList, 
               wireLenDF,
               chemDF,
               devDF,
               preRouteSim=False, 
               parser="XYCE"):
    
    params = line.replace('input ', '').replace(' ', '').split(',')

    VA_line_str = ''
    
    if(parser=="HSPICE"):
        for p in params:
            df = chemDF.loc[chemDF['Inlet'] == p]
            dev = devDF.loc[devDF['Inlet'] == p]['Device'].values[0]
            devVars = devDF.loc[devDF['Inlet'] == p]['DevVars'].values[0] 
            VA_line_str += 'X' + str(numberOfComponents) + ' ' +\
                str(p) + '_0 ' + str(p) + '_0c ' +\
                str(dev)  + ' ' + str(devVars) + ' '
            if not df.empty:
                VA_line_str += 'chemConcentration=' + str(df['InConcentration'].values[0]) + ' '
            
            #if str(p) == soln[1].loc['inlet']:
            #   VA_line_str += 'chemConcentration=' + str(soln[1].loc['solutionC']) + ' '
            VA_line_str += '\n'
            numberOfComponents += 1

        # build init lines for inputs
        for p in params:
            VA_line_str += 'X' + str(numberOfComponents) +\
                ' ' + str(p) + '_0 ' + str(p) + '_1  ' +\
                str(p) + '_0c ' + str(p) + '_1c Channel length='
            
            VA_line_str += getWireLength(wireLenDF, p, preRouteSim)

            inputList.append(p)

            numberOfComponents += 1
        
        VA_line_str += '\n'

    elif(parser=="XYCE"):
        for p in params:
            inputList.append(p)

            df = chemDF.loc[chemDF['Inlet'] == p]
            dev = devDF.loc[devDF['Inlet'] == p]['Device'].values[0]
            devVars = devDF.loc[devDF['Inlet'] == p]['DevVars'].values[0] 
            
            VA_line_str += 'YPressurePump ' + str(p) + ' ' +\
                str(p) + '_0 ' + str(p) + '_0c '+\
                ' ' + str(devVars) + ' '
            
            if not df.empty:
                VA_line_str += 'chemConcentration=' + str(df['InConcentration'].values[0]) + ' '
            VA_line_str += '\n'
            numberOfComponents += 1

            VA_line_str += 'Ychannel ' + str(p) + '_channel ' +\
                str(p) + '_0 ' + str(p) + '_1 ' + \
                str(p) + '_0c ' + str(p) + '_1c length='
            row = wireLenDF.loc[wireLenDF['wire'] == p]
            try:
                wireLength = row.iloc[0,1]
            except IndexError:
                raise IndexError("Unable to parse wires: is "+p+" in list?")

            VA_line_str += str(wireLength) + 'm\n\n'


    return VA_line_str, numberOfComponents, inputList

"""

"""

def praseOutput(vars, 
                line, 
                numberOfComponents, 
                soln, 
                outputWords, 
                wireLenDF, 
                SP_list,
                outNum,
                preRouteSim=False,
                parser="XYCE"):
    outputLine = line.replace('output ', '')
    VA_line_str = ''

    if(parser=="HSPICE"):
        for out in outputLine.replace(' ', '').split(','):
            outputWords.append(out)

            pressureOut = '0'
            pressureIn  = str(out) + '_ch'

            chemIn  = str(out) + '_chC'
            chemOut = 'outc' + str(outNum)

            VA_line_str += 'X' + str(numberOfComponents) + ' ' + pressureIn + ' ' + pressureOut + ' ' + chemIn + ' ' + chemOut + ' Channel length='
            outNum += 1

            # track output 
            SP_list.write(chemOut + ';')

            # add output wire
            # row = wireLenDF.loc[wireLenDF['wire'] == out]
            #row = wireLenDF.loc[wireLenDF.iloc[:,0] == out]
            #wireLength = row.iloc[0,1]
            #VA_line_str += str(wireLength) + 'm\n\n'

            VA_line_str += getWireLength(wireLenDF, out, preRouteSim)

            numberOfComponents += 1
    
    if(parser=="XYCE"):
        for out in outputLine.replace(' ', '').split(','):
            outputWords.append(out)

            outName = "output"+str(outNum)

            pressureOut = '0'   
            pressureIn  = str(out) + '_ch'

            chemIn  = str(out) + '_chC'
            chemOut = 'outc' + str(outNum)

            VA_line_str += 'Ychannel '+ outName + ' ' + pressureIn + ' ' + pressureOut + ' ' + chemIn + ' ' + chemOut +  ' length='
            outNum += 1

            # track output 
            SP_list.write(chemOut + '\n')
            
            # add output wire
            VA_line_str += getWireLength(wireLenDF, out, preRouteSim)

            numberOfComponents += 1

    return VA_line_str, numberOfComponents, outNum
"""

"""

def parseWire(vars, 
              line, 
              line_num, 
              wireList, 
              wireLenDF, 
              numberOfComponents, 
              preRouteSim=False,
              parser="XYCE"):
    # create channel modules
    wires = line.replace('wire ', '').replace(' ', '').split(',')

    VA_line_str = ''

    if(parser=="HSPICE"):
        init_wire_string = '*Declared wires'

        for w in wires:
            # get length of connection

            # string
            VA_line_str += 'X' + str(numberOfComponents) + ' ' + str(w) + '_0 ' + str(w) + '_1 ' + ' ' + str(w) + '_0c ' + str(w) + '_1c  ' + 'Channel length='

            VA_line_str += getWireLength(wireLenDF, w, preRouteSim)

            #outFile_sp

            wireList[w] = 0
            numberOfComponents += 1

    if(parser=="XYCE"):
        init_wire_string = '*Declared wires'

        for w in wires:
            # get length of connection

            wire_conn1 = str(w) + '_0'
            wire_conn2 = str(w) + '_1'
            wire_conn_chem_1 = str(w) + '_0c'
            wire_conn_chem_2 = str(w) + '_1c'

            # string
            VA_line_str += 'Ychannel ' + str(w) + ' ' +\
                wire_conn1 + ' ' + wire_conn2 + ' ' +\
                wire_conn_chem_1 + ' ' + wire_conn_chem_2 + ' length='

            VA_line_str += getWireLength(wireLenDF, w, preRouteSim)

            wireList[w] = 0

            numberOfComponents += 1

    return VA_line_str, numberOfComponents
    #pass


"""
inputs :
vars - input variables 
line - line string
library - library database (pandas)
"""
def parseSTDCell(vars, line, line_num, library, wireList, inputList, outputWords, numberOfComponents, parser="XYCE"):
    if (library['Standard_Cell'].eq(vars)).any():
        
        # var 0 should be module name
        standardCell = vars
        
        line = ' '.join(line.split())
    
        ioPara = ''.join(line.replace('  ', ' ').split(' ')[2:])

        # initialize variables
        io_expression = False
        connectionWord= False
        portPhrase = ''
        ports      = []
        VA_line_str = ''

        # get named ios
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

        # Generate sting for var

        if(parser=="HSPICE"):
            VA_line_str += 'X' + str(numberOfComponents) + ' '
            VA_line_str_chem = ''

            for p in ports:
                if p in wireList.keys():
                    VA_line_str += str(p) + '_' + str(wireList[p]) + ' '
                    VA_line_str_chem += str(p) + '_' + str(wireList[p]) + 'c '
                    wireList[p] += 1
                else:
                    if p in inputList:
                        VA_line_str += str(p) + '_1 '
                        VA_line_str_chem += str(p) + '_1c '
                    elif p in outputWords:
                        VA_line_str += str(p) + '_ch '
                        VA_line_str_chem += str(p) + '_chC '
                    else:
                        VA_line_str += str(p) + ' '
                        VA_line_str_chem += str(p) + 'c '
            
            VA_line_str += VA_line_str_chem + vars + '\n'

        elif(parser=="XYCE"):
            cellName  = line.split(' ')[1]

            VA_line_str += 'Y' + standardCell + ' ' + cellName + ' '
            # + str(numberOfComponents) + ' '
            VA_line_str_chem = ''

            for p in ports:
                if p in wireList.keys():
                    VA_line_str += str(p) + '_' + str(wireList[p]) + ' '
                    VA_line_str_chem += str(p) + '_' + str(wireList[p]) + 'c '
                    wireList[p] += 1
                else:
                    if p in inputList:
                        VA_line_str += str(p) + '_1 '
                        VA_line_str_chem += str(p) + '_1c '
                    elif p in outputWords:
                        VA_line_str += str(p) + '_ch '
                        VA_line_str_chem += str(p) + '_chC '
                    else:
                        VA_line_str += str(p) + ' '
                        VA_line_str_chem += str(p) + 'c '

            VA_line_str += VA_line_str_chem + '\n'

        # probes for mixer
        #if vars == 'diffmix_25px_0':
            
        #    probeList['X'+str(numberOfComponents)]

        numberOfComponents += 1

        return VA_line_str, numberOfComponents

    else:
        print("String: " + vars + " line number: " + str(line_num) + " not in library.")

        return '', numberOfComponents

def getWireLength(wireLenDF, df_index, preRouteSim):
    if not preRouteSim:
        row = wireLenDF.loc[wireLenDF.iloc[:,0] == df_index]
        wireLength = row.iloc[0,1]
        #return str(wireLength) + 'm\n'
        #VA_line_str += str(wireLength) + 'm\n'
    else:
        wireLength = 0.00001
        #VA_line_str += str(wireLength) + 'm\n'

    return str(wireLength) + 'm\n'

def createChemSubArrays(solnDF):

    #g = solnDF.groupby(['Solution'], group_keys=True).apply(lambda x:x)

    #print(g)
    pass
    for g in solnDF.groupby(['Solution']):
        pass
        print(g)
        g = g

def simulationTime(timeDF, outputWords):

    VA_line_str = '\n\n'

    for sim in timeDF.iterrows():

        #print(str(sim[1]["Simulation Type"]) )

        if sim[1]["Simulation Type"] == "transient" or \
            sim[1]["Simulation Type"] == "tran":

            VA_line_str +=  ".tran " + str(sim[1]["Time Slice"]) + ' ' + str(sim[1]["Duration"]) + '\n'

    for out in outputWords:

        VA_line_str += ".print tran V(" + str(out) + "_chC)\n"

    VA_line_str += ".end\n\n"

    return VA_line_str

    


class simple_netlist:
    def __init__(self):
        self.inputList = []
        self.outputList = []
        self.wireList = []

    def loadStdCellLibrary(lib_file):
        pass

    def isInput(in_str):
        pass

    def isOutput(out_str):
        pass

    def isWire(wire_str):
        pass

    def getWireLength(wire_str):
        pass


def createSpiceRunScript(outputFileName, numSoln, remoteTestPath):
    
    # make run spice file

    outputFileName = outputFileName.replace('\\', '/')
    outputPath = ''

    if len(outputFileName.split('/')) > 1:
        fileCharLen = len(outputFileName.split('/')[-1])
        outputPath = outputFileName[:-fileCharLen]
        outputFileName = outputFileName[-fileCharLen:]

    if numSoln == 0:
        simScript = open(outputPath + '/' + "runSims.csh", '+w')
        simScript.write('#/bin/tcsh\n\n')
        simScript.write('cd ' + outputPath.replace('./', remoteTestPath) + "\n\n")
    else:
        simScript = open(outputPath + '/' + "runSims.csh", 'a')
    
    if outputFileName[:1] == './': 
        rm_start = 2
    else:
        rm_start = 0

    # TODO put replace earlier
    o_soln_name = outputFileName
    #mkDirPhrase = "mkdir " + outputPath + o_soln_name + "\n"
    #spiceScriptPhrase = "hspice " + outputPath + o_soln_name + ".sp -o "  + outputPath  + o_soln_name + "/" + o_soln_name[rm_start:] + "_o\n\n"
    mkDirPhrase = "mkdir ./" + o_soln_name + "\n"
    spiceScriptPhrase = "hspice -i ./"  + o_soln_name + ".sp -o ./"  + o_soln_name + "/" + o_soln_name[rm_start:] + "_o\n\n"
    simScript.write(mkDirPhrase + spiceScriptPhrase)

def hspice_lib_import(SPfile, library, libraryPath):
    for rowN, row in enumerate(library.iterrows()):
        #if rowN == 0:
        #    continue
        rStr = row[1]['Standard_Cell']
        libStr = '.hdl ' + libraryPath + 'E' + rStr + '.va\n'
        SPfile.write(libStr)

    SPfile.write('\n')

    SPfile.write('*hard coded EChannel, used for wires\n' + '.hdl ' + libraryPath + "EChannel.va\n")
    SPfile.write('*hard coded Pressure Pump, used for wires\n' + '.hdl ' + libraryPath + "EPrPump.va\n\n\n")

def convert_nodes_2_numbers_xyce(SPfile):
    if os.path.isfile(SPfile) and SPfile[-4:]==".cir":
        SPfile = [SPfile]
    else:
        # if directory is given
        SPfile = ['/'.join([SPfile, f]) 
                       for f in os.listdir(SPfile) 
                       if os.path.isfile(os.path.join(SPfile, f)) and f[-4:]==".cir"]

    for f in SPfile:
        SPfile_o = open(f, 'r')

        new_file = f+'.num'
        SPfile_n = open(new_file, 'w')

        nodeList = {}

        for line in SPfile_o:
            # remove leading WS
            line = line.rstrip()

            # remove comments
            line = line.split('*')[0]
            line_comment = ''.join(line.split('*')[1:])

            


            if line == "" or line == "\n":
                SPfile_n.write(line + line_comment+'\n')
            else:
                line_vars = line.replace('  ', ' ').split(' ')
                if len(line_vars) > 1:
                    arg1 = line_vars[0]
                    end_line_str = []
                    line_nodes = []
                    # xyce command start with .
                    if arg1[0] == ".":
                        for ind, param in enumerate(line_vars[1:]):
                            for n in nodeList.keys():
                                if n in param:
                                    n_num = str(nodeList[n])
                                    rplace_str = '('+n+')'
                                    newParam = param.replace('('+n+')', '('+n_num+')')
                                    line_vars[ind+1] = newParam
                        new_sp_line = ' '.join(line_vars)+'\n'
                    else:
                        # replaces params for numbers
                        # <device> <name>
                        device = [arg1, line_vars[1]]
                        for param in line_vars[2:]:
                            # exception for parameters which will explicitly use =
                            if "=" in param:
                                end_line_str += [param]
                            elif param == '0':
                                line_nodes.append(0)
                            else:
                                if param not in nodeList.keys():
                                    # we do not want 0
                                    nodeList[param] = len(nodeList)+1
                                line_node = nodeList[param]
                                line_nodes.append(line_node)
                    # append all
                        new_sp_line = ' '.join(
                            device+
                            [str(x) for x in line_nodes]+
                            end_line_str
                            )+'\n'
                    
                    SPfile_n.write(new_sp_line+line_comment)
                else:
                    SPfile_n.write(line + line_comment+'\n')

        node_file = f+'.nodes'
        with open(node_file, 'w') as node_f:
            json.dump(nodeList, node_f)

        SPfile_o.close()
        SPfile_n.close()

        







if __name__ == "__main__":
    #inV = sys.argv[1]
    #inV      = '.\\testFiles\\smart_toilet_test2\\smart_toilet2.v'
    #confFile = "./VMF_template.mfsp"
    #solnFile = "solutionFile.csv"
    
    # Xyce test 1
    inV         = './testFiles/xyce_test_1/smart_toilet.v'
    confFile    = "./VMF_xyce.mfsp"
    libraryFile = "./../component_library/StandardCellLibrary.csv"
    solnFile    = "./testFiles/xyce_test_1/smart_toilet_spec.csv"
    devFile     = "./testFiles/xyce_test_1/devices.csv"
    timeFile    = "./testFiles/xyce_test_1/simTime.csv"
    
    parser   = "XYCE"

    Verilog2VerilogA(inputVerilogFile=inV, 
                     configFile=confFile, 
                     solnFile=solnFile, 
                     remoteTestPath="",    
                     libraryFile=libraryFile,
                     devFile=devFile, 
                     length_file=None,
                     timeFile=timeFile,
                     preRouteSim=False, 
                     outputVerilogFile=None,
                     parser="XYCE", 
                     runScipt=False)
    
    convert_test_file = "./testFiles/xyce_test_1/"

    convert_nodes_2_numbers_xyce(convert_test_file)

    #Verilog2VerilogA(inV, confFile, solnFile, remoteTestPath="", libraryFile=libraryFile, parser=parser, runScipt=False)
