import pysftp
import pandas as pd
from datetime import datetime
import os

class sftpController:
    def __init__(self):
        self.cnopts = pysftp.CnOpts()
        self.cnopts.hostkeys = None
    
    #Filter Functions
    def isnotspace(self, val):
        return val != ''

    def filenameContains(self, df, contains):
        return df[df[0].str.contains(contains)]

    def latestFile(self, df): 
        return df[df[2]==df[2].max()]

    def biggestFile(self, df):
        return df[df[1]==df[1].max()]

    #Pipelines
    def getBigGC(self, df):
        df = self.filenameContains(df, "current")
        df = self.biggestFile(df)
        print(df)
        return df

    def getLatestSA(self, df):
        df = self.filenameContains(df, "sar")
        df = self.latestFile(df)
        print(df)
        return df
    
    def getLatestGC(self, df):
        df = self.filenameContains(df, "current")
        df = self.latestFile(df)
        print(df)
        return df

    #Utility Functions
    def fromEpoch(self, timestamp):
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%dT%H:%M:%S')

    def downloadFiles(self, listOfFiles, sftpObject, filename):
        if(len(listOfFiles)):
            for onefile in listOfFiles:
                sftpObject.get(onefile, filename)

    def downloadFile(self, host, username, password, filePath, serverName, fileType):
        try:
            with pysftp.Connection(host=host, username=username, password=password, cnopts=self.cnopts) as sftp:
                print(f'SFTP connection is succesfull :: {username}  {password} {host} {filePath}')
                with sftp.cd(filePath):
                    print('Enter path')
                    print(os.getcwd())
                    df = pd.DataFrame([[attr.filename, attr.st_size, self.fromEpoch(attr.st_mtime)] for attr in sftp.listdir_attr()])
                    if(fileType == "SA"):
                        df = self.getLatestSA(df)
                        pathToStore = os.getcwd()+"\SA_files\\"
                    else:
                        df = self.getLatestGC(df)
                        pathToStore = os.getcwd()+"\GC_files\\"
                    self.downloadFiles(list(df[0].values), sftp, pathToStore+serverName)
                    
                    print("Downloading file: " + serverName)
                print("Closing\n\n\n")
                sftp.close()
        except Exception as e:
            print("unable to download files :: ", e)


def returnSftpControllerObj():
    return sftpController()

if __name__ == "__main__":
    returnSftpControllerObj()