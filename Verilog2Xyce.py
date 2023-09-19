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
    
    spiceOutputDir = os.path.dirname(os.path.relpath(inputVerilogFile)) + "/spiceFiles"

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
    
    Verilog2VerilogA.convert_nodes_2_numbers_xyce(spiceOutputDir)

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