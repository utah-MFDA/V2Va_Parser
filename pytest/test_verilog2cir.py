

def test_convert_2_cir():
    from Verilog2VerilogA import Verilog2VerilogA 
    
    inV         = './testFiles/xyce_test_1/smart_toilet.v'
    confFile    = "./VMF_xyce.mfsp"
    libraryFile = "./testFiles//StandardCellLibrary.csv"
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
    

def test_convert_nodes_2_numbers():
    from Verilog2VerilogA import Verilog2VerilogA, convert_nodes_2_numbers_xyce
    
    inV         = './testFiles/xyce_test_1/smart_toilet.v'
    confFile    = "./VMF_xyce.mfsp"
    libraryFile = "./testFiles/StandardCellLibrary.csv"
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
    
    convert_test_file = "./testFiles/xyce_test_1/spiceFiles/smart_toilet_H2O.cir"

    convert_nodes_2_numbers_xyce(convert_test_file)