import ssh
import discover
import csvloader
import paramiko
import time
import threading
import logging

def setupDevice(ip):
    print("Connecting to " + ip)
    output = []
    try:
        shell = ssh.ShellHandler(ip, username, password)
        output += shell.execute("ipconfig")
        output += shell.execute("timedate")
        version = shell.execute("version")
        print("Version:" + cat(version))
        if cat(version)[:28] != "DM-NVX-D30C [v7.0.5057.00023":
            print("Need update")
            sftp = shell.ssh.open_sftp()
            sftp.chdir("./")
            sftp.put("./firmware/dm-nvx-ed30-enc_7.0.5057.00023_r453766.zip", "./firmware/dm-nvx-ed30-enc_7.0.5057.00023_r453766.zip")
            shell.execute("imgupd")
        output += version
    except paramiko.AuthenticationException:
        setup = ssh.ShellHandler(ip, "crestron", "")
        print("Running first time setup on " + ip)
        output += setup.execute(username + "\n" + password + "\n" + password + "\n")
        setup.ssh.close()
        del(setup)
        time.sleep(1)
        return setupDevice(ip)

    return output

ips = discover.autodiscovery()

username = "admin"
password = "Solutionz1!"

def cat(x):
    if len(x) == 0:
        return ""
    else:
        return x[0] + cat(x[1:])
print(ips)
threads = []
for ip in ips:
    thread = threading.Thread(target=setupDevice, args=(ip,))
    thread.start()
    threads.append(thread)

for index, thread in enumerate(threads):
    print("Before join, thread " + str(index))
    thread.join()
    print("After join, thread " + str(index))