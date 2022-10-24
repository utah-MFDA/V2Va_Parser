import subprocess
import Verilog2VerilogA

if __name__ == "__main__":
    
    # construct file path
    filePath = "./testFiles/smart_toilet_test2".replace("./", "./V2Va_Parser/")
    fileName = "smart_toilet2.v"

    fullFilePath = filePath + "/" + fileName
    fullFilePath = fullFilePath#.replace("./", "./V2Va_Parser/")

    configFile = "./V2Va_Parser/VMF_template.json"

    solnFile   = "./V2Va_Parser/testFiles/smart_toilet_test2/solutionFile.csv"

    # build sp file

    print("\n\nstart builing sp file\n")

    Verilog2VerilogA.Verilog2VerilogA(fullFilePath, configFile, solnFile)

    print("\nend building sp file\n\n")

    pass

    # execute shell script
    remoteShellScript = "./src/sendFileHSpice.bash"

    # read list file
    spiceFilePath = filePath + '/spiceFiles/spiceList'
    spiceListFile = open(spiceFilePath)

    # Construct command path
    sendFileCommand = remoteShellScript + " " + fileName + " " + filePath
    sendFileCommand = sendFileCommand.replace("./", "./V2Va_Parser/")

    print("start send file\n")
    for line in spiceListFile:     
        subprocess.call(sendFileCommand, shell=True)
    
    print("\nend send file\n\n")

