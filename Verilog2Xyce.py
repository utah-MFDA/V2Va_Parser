
import os

from . import Verilog2VerilogA
from . import SpiceParser

import pandas as pd

"""

soln DF

inputNode, chemName, InConcentration #, outNode, outConcentration #possilbly not nesessary

device DF

input, device, arguments

time DF

sim_name, type, time, slice

"""

#Verilog2VerilogA

def Verilog2Xyce(
        inputVerilogFile, 
        configFile, # used for header and footer of spice file
        solnFile, 
        remoteTestPath,    
        libraryFile=None,
        devDF=None, 
        length_file=None,
        timeDF=None,
        probeList=None,
        preRouteSim=False, 
        outputVerilogFile=None, 
        runScipt=True):
    
    spiceOutputDir = os.path.dirname(os.path.relpath(inputVerilogFile)) + "/spiceFiles"
    
    
    #Verilog2VerilogA.Verilog2VerilogA(
    SpiceParser.Parse_Verilog(
                     inputVerilogFile, 
                     configFile, 
                     solnFile, 
                     remoteTestPath,    
                     libraryFile=libraryFile,
                     devDF=devDF, 
                     length_file=length_file,
                     timeDF=timeDF,
                     preRouteSim=preRouteSim, 
                     outputVerilogFile=outputVerilogFile,
                     probeList=probeList,
                     parser="XYCE",
                     runScipt=runScipt)
    
    #Verilog2VerilogA.convert_nodes_2_numbers_xyce(spiceOutputDir)
    SpiceParser.convert_nodes_2_numbers_xyce(spiceOutputDir)

    # remove .cir
    
    """
    for f in os.listdir(spiceOutputDir):
        if os.path.isfile(os.path.join(spiceOutputDir, f)) and f[-4:]==".cir":
            f = '/'.join([spiceOutputDir,f])
            os.remove(f)
    """
    for f in os.listdir(spiceOutputDir):
        if os.path.isfile(os.path.join(spiceOutputDir, f)) and f[-4:]==".cir":
            f = '/'.join([spiceOutputDir,f])
            os.rename(f, f+".str")

    # rename .cir.num
    
    for f in os.listdir(spiceOutputDir):
        if os.path.isfile(os.path.join(spiceOutputDir, f)) and f[-8:]==".cir.num":
            f = '/'.join([spiceOutputDir,f])
            os.rename(f, f[:-4])
            
def Verilog2Xyce_from_csv(
        inputVerilogFile, 
        configFile, 
        solnFile, 
        remoteTestPath,    
        libraryFile=None,
        devFile=None, 
        length_file=None,
        timeFile=None,
        preRouteSim=False, 
        outputVerilogFile=None, 
        runScipt=True):
    
    # create solution dateFrame
    solnDF = pd.read_csv(solnFile)
    
    # create device dataFrame
    devDF  = pd.read_csv(devFile)
    
    # create time dataFrame
    timeDF = pd.read_csv(timeFile)
    
    Verilog2Xyce(
        inputVerilogFile, 
        configFile, 
        solnDF, 
        remoteTestPath,    
        libraryFile,
        devDF, 
        length_file,
        timeDF,
        None,
        preRouteSim, 
        outputVerilogFile, 
        runScipt)
            
def Verilog2Xyce_from_config(
        inputVerilogFile, 
        configFile, 
        solnInputList,
        #simEvalList,
        remoteTestPath,    
        libraryFile=None,
        devList=None, 
        length_file=None,
        simTimesList=None,
        simProbeList=None,
        preRouteSim=False, 
        outputVerilogFile=None, 
        runScipt=True):

    # create soln DF
    solnCol = ['Inlet', 'Solution', 'InConcentration']
    solnDF  = pd.DataFrame(columns=solnCol)
    print('Chemical inputs')
    for soln in solnInputList:
        # [Inlet, Solution, InConcentration, Outlet, OutConcentration]
        chem = solnInputList[soln]
        chemArr = [[chem.getNode(), chem.getChem(), chem.getInValue()]]
        temp_chem = pd.DataFrame(chemArr, columns=solnCol)
        
        print(chemArr)
        
        solnDF = pd.concat([solnDF, temp_chem])

    # create dev DF
    devCol = ['Inlet', 'Device', 'DevVars'] 
    devDF  = pd.DataFrame(columns=devCol)
    print('Device inputs')
    for dev in devList:
        #[Input, Device, DevVar]
        d = devList[dev]
        devDF = pd.concat([devDF, 
            pd.DataFrame([[d.getNode(), d.getType(), ','.join(d.getArgs())]], columns=devCol)
            ])
    
    # create time DF
    timeCol = ['Name', 'Simulation Type', 'Duration', 'Time Slice'] 
    timeDF  = pd.DataFrame(columns=timeCol)
    print('simulation inputs')
    for ind, t in enumerate(simTimesList):
        # [Name, Simulation Type, Duration, TIme, Slice]
        print(simTimesList[t])
        timeDF = pd.concat([timeDF, 
            pd.DataFrame([['Sim_'+str(ind)] + simTimesList[t][0]], columns=timeCol)
            ])
        
    print(devDF)

    Verilog2Xyce(
        inputVerilogFile, 
        configFile, 
        solnDF, 
        remoteTestPath,    
        libraryFile,
        devDF, 
        length_file,
        timeDF,
        simProbeList,
        preRouteSim, 
        outputVerilogFile, 
        runScipt)

    
if __name__ == "__main__":

    inV         = './testFiles/xyce_test_1/smart_toilet.v'
    confFile    = "./VMF_xyce.mfsp"
    libraryFile = "./../component_library/StandardCellLibrary.csv"
    solnFile    = "./testFiles/xyce_test_1/smart_toilet_spec.csv"
    devFile     = "./testFiles/xyce_test_1/devices.csv"
    timeFile    = "./testFiles/xyce_test_1/simTime.csv"

    Verilog2Xyce(
        inputVerilogFile=inV, 
        configFile=confFile, 
        solnFile=solnFile, 
        remoteTestPath="",    
        libraryFile=libraryFile,
        devFile=devFile, 
        length_file=None,
        timeFile=timeFile,
        preRouteSim=False, 
        outputVerilogFile=None, 
        runScipt=True)
