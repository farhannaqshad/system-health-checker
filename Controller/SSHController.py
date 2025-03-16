import paramiko
import os

class SshController:
    
    def __init__(self):
        self.sshClient = paramiko.SSHClient()
    
    # def getInstance(self):
    #     try: 
    #         # self.sshClient = paramiko.SSHClient()
    #         self.sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #     except Exception as e:
    #         print('unable to create sshClient Obj:: ', e)

    def createConnection(self, host, username, password):
        try:
            print("Currently executing for host:: " + host)
            self.sshClient.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
            self.sshClient.connect(host, username=username, password=password)
            return True
        except Exception as e:
            print("Unable to connect to SSH", e)
            if "not found in known_hosts" in e.__str__():
                self.sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.sshClient.connect(host, username=username, password=password)
                return True
            return False

    def closeConnection(self):
        try:
            self.sshClient.close()
        except Exception as e:
            print('Unable to close connection')
    
    def isConnectionActive(self):
        if self.sshClient.get_transport() is not None:
            if self.sshClient.get_transport().is_active():
                return True
        print("Connection is closed!")
        return False 
        
    def executeCommand(self, cmd):
        if(self.isConnectionActive()):
            try:
                client_stdin, client_stdout, client_stderr = self.sshClient.exec_command(cmd)
                commandOutput = client_stdout.readlines()
                # print(commandOutput)
                output = ""
                for line in commandOutput:
                    output += line
                return output
            except Exception as e:
                print("Error executing command:: ", e,  " :: command:: ", cmd)
                return ""       

def returnSSHControllerObj():
    return SshController()

if __name__ == "__main__":
    returnSSHControllerObj()