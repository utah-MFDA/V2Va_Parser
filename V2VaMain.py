import subprocess
import Verilog2VerilogA
import spiceExtract

def buildSPfile(fullFilePath, configFile, solnFile, remoteTestPath):
    print("\n\nstart builing sp file\n")

    Verilog2VerilogA.Verilog2VerilogA(fullFilePath, configFile, solnFile, remoteTestPath)

    print("\nend building sp file\n\n")

def sendFiles(filePath, fullPath, localPathRoute):
    # execute shell script
    remoteShellScript = "./src/sendFileHSpice.bash".replace("./", localPathRoute)

    # read list file
    # the spiceFiles is created by the V2Va parser
    spiceFilePath = fullPath + '/spiceFiles/spiceList'
    spiceListFile = open(spiceFilePath)

    # Construct command path
    #sendFileCommand = remoteShellScript + " " + fileName + " " + filePath
    #sendFileCommand = sendFileCommand.replace("./", localPathRoute)

    print("start send file\n")
    for line in spiceListFile:
        # Construct command path
        line = line.replace('\n', '')
        sendFileCommand = remoteShellScript + " " + line.split('/')[-1] + " " + fullPath + "/spiceFiles "# + filePath.replace('./', '')
        #sendFileCommand = sendFileCommand     
        subprocess.call(sendFileCommand, shell=True)
    
    sendFileCommand = remoteShellScript + " runSims.csh " + fullPath + "/spiceFiles " + filePath.replace('./', '')
    #sendFileCommand = sendFileCommand     
    subprocess.call(sendFileCommand, shell=True)

    print("\nend send files\n\n")

def runSimFiles(filePath, localPathRoute):
    print("\nrun simulations\n")

    runSimCommand = "./src/runSimsRemote.bash".replace("./", localPathRoute) + " " + filePath.replace('./', '') + "/spiceFiles"

    subprocess.call(runSimCommand, shell=True)

    print("\nend run simulations\n\n")

def downloadFiles(filePath, fullPath, localPathRoute):
    
    # the spiceFiles is created by the V2Va parser
    spiceFilePath = fullPath + '/spiceFiles/spiceList'
    spiceListFile = open(spiceFilePath)

    getFileScript = "./src/getFileHSpice.bash ".replace("./", localPathRoute)
    
    print("\nDownloading file\n")
    
    for line in spiceListFile:
        # Construct command path
        line = line.replace('\n', '')
        remotePath = fullPath.replace('./', '') + "/spiceFiles/" + line.split('/')[-1].replace(".sp", "") + ""
        getFileCommand = getFileScript + line.split('/')[-1].replace(".sp", "_o") + " " + remotePath + " " + fullPath + "/spiceFiles " + fullPath + "/spiceFiles "# + filePath.replace('./', '')
        #sendFileCommand = sendFileCommand     
        subprocess.call(getFileCommand, shell=True)

    print("Done getting files")

def extractChemData(fullPath):

    print("\nExtracting data\n\n")

    spiceExtract.parseSpiceOut(fullPath + '/spiceFiles/', "spiceList")

    print("\nDone extracting data\n\n")

# main -------------------------------------------

if __name__ == "__main__":
    
    localPathRoute = "./V2Va_Parser/"

    # construct file path
    filePath = "./testFiles/smart_toilet_test2"#.replace("./", "./V2Va_Parser/")
    fileName = "smart_toilet2.v"

    fullPath     = filePath.replace("./", localPathRoute)
    fullFilePath = fullPath + "/" + fileName
    #fullFilePath = fullFilePath#.replace("./", "./V2Va_Parser/")

    configFile = "./V2Va_Parser/VMF_template.json"

    solnFile   = "./V2Va_Parser/testFiles/smart_toilet_test2/solutionFile.csv"

    remoteTestPath = "~/Verilog_Tests/"

    # build sp file
    #buildSPfile(fullFilePath, configFile, solnFile, remoteTestPath)

    # send files to remote server
    #sendFiles(filePath, fullPath, localPathRoute)
    
    # run simulation files
    #runSimFiles(fullPath, localPathRoute)

    # get files from remote server
    #downloadFiles(filePath, fullPath, localPathRoute)

    # run file extraction
    extractChemData(fullPath)
    
