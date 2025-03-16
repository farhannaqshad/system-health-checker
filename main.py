# from distutils.command.config import config
# from operator import getitem
import Configuration.ConfigurationParser as configuration
import Controller.SSHController as sshController
import time
import Controller.sftpController as sftpController
import sys

# commandOutput = ""
def writeDatatoFile(filename, data):
    try:
        print("writing data to file:: ", filename)
        with open(filename, "w", encoding="utf-8") as external_file:
            # add_text = "This text will be added to the file"
            print(data, file=external_file)
            external_file.close()
    except Exception as e:
        print("exception:: ", e)


def filterOutputOfCommand(commandOuput, filename):
    if commandOuput != "":
        writeDatatoFile(filename=filename, data=commandOuput)


def executeApplicationStatusCommands(configurationParser, sshClient, obj):
# check application status
    if configurationParser.executeApplicationCommands == True:
        for val in configurationParser.applicationStatusCommands:
            commandOutput = sshClient.executeCommand(str(val))
            filename = 'Reports/' + obj.get('hostname') +"_applicationStatusCommands" + "_" + configurationParser.get_key(val, configurationParser.applicationCommandDict)+"_"+ str(time.time()) + ".txt"                        
            filterOutputOfCommand(commandOuput=commandOutput, filename=filename)

def executeLogRelatedCommandsOneByOne(configurationParser, sshClient, obj, pathToFile, fileToSearch, useWildCardSign):
    if configurationParser.executeLogsExtractionCommands == True:
        for val in configurationParser.stringsToSearch:
            stringCommandToExecute = configurationParser.formatGrepCommand(val, pathToFile, fileToSearch, useWildCardSign)
            print(stringCommandToExecute)
            commandOutput = sshClient.executeCommand(stringCommandToExecute)
            filename = 'Reports/' + obj.get('hostname') +"_LogToSearchCommands" + "_" + pathToFile.replace("/","-") + "_" + fileToSearch + "_" + configurationParser.get_key(val, configurationParser.stringsToSearchDict)+"_"+ str(time.time()) + ".txt"
            filterOutputOfCommand(commandOuput=commandOutput, filename=filename)

def extractLogFilesAndExecuteCommands(configurationParser, sshClient, obj):
    logFileList = obj.get("logFiles")
    for logFileDict in logFileList:
        pathToFile = logFileDict.get("pathToFile")
        fileToSearch = logFileDict.get("fileToSearch")
        useWildCardSign = logFileDict.get("useWildCardSign")
        print("Path: {0}, fileName: {1}, useWildCardSign: {2}".format(pathToFile, fileToSearch, useWildCardSign))
        executeLogRelatedCommandsOneByOne(configurationParser, sshClient, obj, pathToFile, fileToSearch, useWildCardSign)

def executeLogRelatedCommands(configurationParser, sshClient, obj):
    if len(obj.get("logFiles")) > 0:
        extractLogFilesAndExecuteCommands(configurationParser, sshClient, obj)
    else:
        if configurationParser.executeLogsExtractionCommands == True:
            for val in configurationParser.stringsToSearch:
                stringCommandToExecute = configurationParser.formatGrepCommand(val)
                commandOutput = sshClient.executeCommand(stringCommandToExecute)
                filename = 'Reports/' + obj.get('hostname') +"_LogToSearchCommands" + "_" + configurationParser.get_key(val, configurationParser.stringsToSearchDict)+"_"+ str(time.time()) + ".txt"
                filterOutputOfCommand(commandOuput=commandOutput, filename=filename)

def downloadSAfiles(configurationParser, sftpClient, obj):
    if configurationParser.downloadAndAnalyzeSARFile == True:
        sftpClient.downloadFile(obj.get('hostname'), obj.get('username'), obj.get('password'), obj.get('sarFilePath'), obj.get('servername'), "SA")
    else:
        print('Sar file download option is off')

def downloadGCfiles(configurationParser, sftpClient, obj):
    if configurationParser.downloadAndAnalyzeGCFile == True:
        if len(obj.get("gcLogFiles")) > 0:
            i = 0
            for gcFilePath in obj.get("gcLogFiles"):
                sftpClient.downloadFile(obj.get('hostname'), obj.get('username'), obj.get('password'), gcFilePath, obj.get('servername')+"_"+str(i), "GC")
                i+=1
        else:
            print("No gc location found in config")    
    else:
        print("GC file download option is off")

if __name__ == "__main__":
    # Ensure one argument is passed
    if len(sys.argv) != 2:
        print("Error: Missing required argument.")
        print("Usage: python main.py <software_family_code>")
        print("Refer to 'main-conf.cfg' for valid software family codes.")
        sys.exit(1)
    try: 
        configurationParser = configuration.returnConfigParserObject()
        configurationParser.readConfigurationFile(sys.argv[1])
    except Exception as e:
        print("Unable to read configuration file")
        exit

    if configurationParser.isConfigReadSuccess:
        # create instance of SSH client Controller
        try: 
            sshClient = sshController.returnSSHControllerObj()
        except Exception as e:
            print("Unable to create ssh client")
            exit

        try: 
            sftpClient = sftpController.returnSftpControllerObj()
        except Exception as e:
            print("Unable to create sftp client")
            exit
 
        # connect SSH connection
        try:
        
            for obj in configurationParser.listServerDetails:
                # print(obj.get('hostname'))
                password = input(f"{obj.get('hostname')}@{obj.get('username')}'s password:")
                isConnected = sshClient.createConnection(obj.get('hostname'), obj.get('username'), obj.get('password'))
                print(f"able to connect to {obj.get('hostname')}@{obj.get('username')}'s")
                if isConnected:
                    try:
                        executeApplicationStatusCommands(configurationParser=configurationParser, sshClient=sshClient, obj=obj)                        
                        executeLogRelatedCommands(configurationParser=configurationParser, sshClient=sshClient, obj=obj)
                        downloadSAfiles(configurationParser, sftpClient, obj)
                        downloadGCfiles(configurationParser, sftpClient, obj)
                    except Exception as e:
                        sshClient.closeConnection()
                        print("unable to store output:: ", e)
                else:
                    print("Unable to connect ssh client")
        except Exception as e:
            print("Unable to connect ssh client")
            # exit

        sshClient.closeConnection()
    else:
        print('Unable to read configuration for further processing')
