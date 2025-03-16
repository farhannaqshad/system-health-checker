import configparser
# from distutils.command.config import config
import os

class ConfigurationParser:

    def __init__( self ):
        self.listServerDetails = []
        self.listEnvDetails = []
        self.listHostNames = []
        self.listUsername = []
        self.listPassword = []
        self.applicationStatusCommands = []
        self.applicationErrorLogsCommand = None
        self.stringsToSearch = []
        self.stringToSearch = None
        self.pathToSearch = None
        self.fileToSearch = None
        self.healthCheckGroup = None
        self.useEnv = None
        self.useWildCard = False
        self.config = {}
        self.mainConfig = {}
        self.applicationCommandDict = {}
        self.stringsToSearchDict = {}
        self.executeApplicationCommands = False
        self.executeLogsExtractionCommands = False
        self.isConfigReadSuccess = True
        self.downloadAndAnalyzeSARFile = False
        self.downloadAndAnalyzeGCFile = False
        # Define the main configuration file path
        self.mainConfigPath = os.path.join(os.path.dirname(__file__), "main-conf.cfg")

    def readConfigurationFile(self, healthCheckGroup):
        """
        Reads the main configuration file (main-conf.cdf) to determine the correct config.cfg file path.
        Then reads the retrieved config.cfg.
        """
        try:
            self.healthCheckGroup = healthCheckGroup
            # Step 1: Retrieve the correct config.cfg file path
            config_file_path = self._getConfigFilePath()

            if not config_file_path:
                print(f"ERROR: No configuration file found for healthCheckGroup: {healthCheckGroup}")
                self.isConfigReadSuccess = False
                return
            print(config_file_path)

            # Step 2: Read the retrieved config.cfg file
            if os.path.exists(config_file_path):
                print(f"Loading configuration from: {config_file_path}")
                self.config = configparser.RawConfigParser();
                self.config.read(config_file_path)
                self._retrieveHostDetails()
                self._retrieveCommandsToExecute()
                self._retrieveLogFileDetails()
                self._retrieveApplicationStatusCommands()
                self._retrieveStringToSearchCommands()
            else:
                print(f"ERROR: The retrieved config file does not exist: {config_file_path}")
                self.isConfigReadSuccess = False

        except Exception as e:
            self.isConfigReadSuccess = False
            print(f"Failed to initialize the config parser instance. Error: {e}")

    def _getConfigFilePath(self):
        """
        Reads main-conf.cdf to determine which configuration file to load.
        """
        try:
            if not os.path.exists(self.mainConfigPath):
                print(f"ERROR: Main configuration file not found at: {self.mainConfigPath}")
                return None

            # Read the main configuration file
            main_config = configparser.ConfigParser()
            main_config.read(self.mainConfigPath)

            if "SoftwareMapping" not in main_config:
                print(f"ERROR: 'SoftwareMapping' section not found in {self.mainConfigPath}")
                return None

            if self.healthCheckGroup in main_config["SoftwareMapping"]:
                config_path = main_config["SoftwareMapping"][self.healthCheckGroup]

                # Normalize the path (handle relative paths)
                config_path = os.path.join(os.path.dirname(__file__), config_path)

                return config_path
            else:
                print(f"ERROR: Software family '{self.healthCheckGroup}' not found in main configuration.")
                return None

        except Exception as e:
            print(f"ERROR: Failed to read main configuration file. Exception: {e}")
            return None
    
    def _retrieveHostDetails(self):
        envs = self.config["envs"]

        for option in envs:
            self.listEnvDetails.append(envs.get(option=option))
        
        # self.useEnv = useEnv["use_env"]
        # print(self.useEnv)
        # if self.useEnv == 'dev':
        #     self.retrieveDevEnvDetails()
        # else:
        #     self.retrieveProdEnvDetails()
        self._retrieveEnvDetails()
    
    def _retrieveEnvDetails(self):
        for option in self.listEnvDetails:
            serverDetails = self.config[option]
            serverDict = {}
            # self.hostname = serverDetails["host"]
            serverDict['hostname'] = serverDetails["host"]
            serverDict['username'] = serverDetails["username"]
            serverDict['password'] = serverDetails["password"]
            serverDict['servername'] = serverDetails["hostName"]
            serverDict['sarFilePath'] = serverDetails["sarFilePath"]
            
            if serverDetails["logFileConfig"] != None:
                logFileConfig = serverDetails["logFileConfig"]
                logFileLocations = self.config[logFileConfig]
                print(logFileLocations)
                logFileList = self._addLogFileLocationsToServerDict(logFileLocations)
                serverDict['logFiles'] = logFileList
            
            if serverDetails["gcFileConfig"] != None:
                gcFileConfig = serverDetails["gcFileConfig"]
                gcFileLocations = self.config[gcFileConfig]
                gcLogFileList = self._addGCLogFileLocationsToServerDict(gcFileLocations)
                serverDict['gcLogFiles'] = gcLogFileList

            self.listServerDetails.append(serverDict)
        
        print(self.listServerDetails)

        # self.listUsername.append(serverDetails["username"])
        # self.listPassword.append(serverDetails["password"])

    def retrieveProdEnvDetails(self):
        print("prod env details")
    
    def _retrieveCommandsToExecute(self):
        executionCheckDetails = self.config["CommandsToExecute"]
        self.executeApplicationCommands = executionCheckDetails.getboolean("applicationCommands")
        self.executeLogsExtractionCommands = executionCheckDetails.getboolean("logExtractionCommands")
        self.downloadAndAnalyzeSARFile = executionCheckDetails.getboolean("downloadAndAnalyzeSARFile")
        self.downloadAndAnalyzeGCFile = executionCheckDetails.getboolean("downloadAndAnalyzeGCFile")

    def _addLogFileLocationsToServerDict(self, logFileLocations):
        logFilesList = []
        print(logFileLocations)
        for key_path in logFileLocations:
            option = logFileLocations[key_path]
            logFilesDict = {}
            if "," in option:
                options = option.split(",")
                print("options after split", options)
                if(len(options) == 3):
                    logFilesDict["pathToFile"] = options[0]
                    logFilesDict["fileToSearch"] = options[1]
                    logFilesDict["useWildCardSign"] = eval(str(options[2]))
                    logFilesList.append(logFilesDict)
                else:
                    print("options are not compelete to extracting information from log file", options)
            else:
                print("options didn't contains ','")
        return logFilesList

    def _addGCLogFileLocationsToServerDict(self, gcLogFileLocations):
        gcLogFilesList = []
        print(gcLogFileLocations)
        for key_path in gcLogFileLocations:
            option = gcLogFileLocations[key_path]
            gcLogFilesList.append(option)
        return gcLogFilesList



    def _retrieveLogFileDetails(self):
        logDetails = self.config["log-details"]
        self.stringToSearch = logDetails["stringToSearch"]
        self.pathToSearch = logDetails["pathToSearch"]
        self.fileToSearch = logDetails["fileNameToSearch"]
        self.useWildCard = logDetails.getboolean("useWildCardSign")

    def _retrieveApplicationStatusCommands(self):
        applicationCommandsSection = self.config["ApplicationStatusCommands"]
        for option in applicationCommandsSection:
            self.applicationCommandDict[option] = applicationCommandsSection.get(option=option)
            self.applicationStatusCommands.append(applicationCommandsSection.get(option=option))
            # print(option)
        # print(len(applicationCommandsSection))

    def _retrieveErroLogsCommands(self):
        cmdSection = self.config["SearchErrorLogs"]
        self.applicationErrorLogsCommand = cmdSection['cmd'] 

    def _retrieveStringToSearchCommands(self):
        stringToSearchCommands = self.config["StringsToSearch"]
        for option in stringToSearchCommands:
            self.stringsToSearchDict[option] = stringToSearchCommands.get(option=option)
            self.stringsToSearch.append(stringToSearchCommands.get(option=option))
            # print(option)

    def formatGrepCommand(self, stringToSearch):
        print(self.useWildCard)
        if self.useWildCard:
            append = "*"
        else:
            append = ""
        
        command = str(self.applicationErrorLogsCommand).format(stringToSearch, self.pathToSearch, self.fileToSearch+append)
        
        return command
    
    def formatGrepCommand(self, stringToSearch, pathToSearch, fileToSearch, useWildCard):
        print(useWildCard)
        if useWildCard:
            append = "*"
        else:
            append = ""
        
        command = str(self.applicationErrorLogsCommand).format(stringToSearch, pathToSearch, fileToSearch+append)
        
        return command

    def get_key(self, val, dict):
        for key, value in dict.items():
            # print(value, "  ", val)
            if str(value).__eq__(str(val)):
                return key 
        return "key_doesn't_exist"

def returnConfigParserObject():
    print("class Instance created")
    return ConfigurationParser()

if __name__ == "__main__":
    print("instance loaded")
    returnConfigParserObject()
