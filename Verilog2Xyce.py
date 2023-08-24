import os


from . import Verilog2VerilogA

def Verilog2Xyce(
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

    Verilog2VerilogA.Verilog2VerilogA(inputVerilogFile, 
                     configFile, 
                     solnFile, 
                     remoteTestPath,    
                     libraryFile=libraryFile,
                     devFile=devFile, 
                     length_file=length_file,
                     timeFile=timeFile,
                     preRouteSim=preRouteSim, 
                     outputVerilogFile=outputVerilogFile,
                     parser="XYCE",
                     runScipt=runScipt)
    
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