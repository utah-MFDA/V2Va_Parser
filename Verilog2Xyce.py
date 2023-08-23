
import Verilog2VerilogA

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

    Verilog2VerilogA(inputVerilogFile, 
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
    