from tracemalloc import start
import paramiko

ip = "169.254.108.215"
username = "admin"
password = "Solutionz1!"

class ShellHandler:
    '''
    A helper class to execute commands and get outputs
    from an SSH shell.
    '''
    def __init__(self, host, user, psw):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(host, username=user, password=psw, port=22)

        channel = self.ssh.invoke_shell()
        self.stdin = channel.makefile('wb')
        self.stdout = channel.makefile('r')

    def __del__(self):
        self.ssh.close()

    def getSSH(self):
        return self.ssh
    # Execute a command on this interactive shell
    def execute(self, cmd):
        # Writes the command to the shell input
        cmd = cmd.strip('\n')
        self.stdin.write(cmd + '\n')

        # Gets the exit status of the shell
        finish = 'end of stdOUT buffer. finished with exit status'
        echo_cmd = 'echo {} $?'.format(finish)
        self.stdin.write(echo_cmd + '\n')

        self.stdin.flush()

        shout = []

        started = False
        for line in self.stdout:
            # Stops the output stream from getting stuck
            # by stopping when it sees the prompt for a 
            # second time.
            if line == 'DM-NVX-E30>\r\n' or line == 'DM-NVX-D30C>\r\n':
                if started == True:
                    break
                started = True

            # Clear the output if this is one of the starting lines
            if str(line).startswith(cmd) or str(line).startswith(echo_cmd):
                shout = []
            elif (line != "\r\n" and line != "\n" and line != 'DM-NVX-E30>\r\n' and line != 'DM-NVX-D30C>\r\n'):
                shout.append(line.strip())

        return shout
'''
# Some sample code

# Create a ShellHandler object
try:
    shell = ShellHandler(ip, username, password)
except paramiko.AuthenticationException:
    shell = ShellHandler(ip, "crestron", "")

# Run multiple commands and append the output to a list
output = []
output += shell.execute("ipconfig")
output += shell.execute("timedate")
output += shell.execute("version")

# Print each element in the list
for line in output:
    print(line)
'''