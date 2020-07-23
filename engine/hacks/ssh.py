#!/usr/bin/env python
import os
import socket
import time
import paramiko

class SSH(object):

    def __init__(self, host, username, password=None, key=None):
        self.host = host
        self.username = username
        self.password = password
        self.key = None
        if key:
            self.key = paramiko.RSAKey.from_private_key_file(key, password)
        self.ssh = None
        self.pod_in = None
        self.pod_out = None
        self.pod_err = None

    def open_ssh(self, host, usr, passwd):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        try:
            self.ssh.connect(host, username=usr, password=passwd, pkey=self.key)
        except socket.error:
            print('SSH connection failed.')
        return self.ssh
 
    def close_ssh(self):
        self.ssh.close()

    def open_pod(self):
        self.pod_in, self.pod_out, self.pod_err = self.ssh.exec_command('sudo su')
        return self._read_pod_cmd_output()

    def exec_pod_cmd(self, cmd):
        self.pod_in.channel.send(cmd + os.linesep)
        return self._read_pod_cmd_output()

    def _read_pod_cmd_output(self):
        time.sleep(0.5)
        result = ""
        while self.pod_out.channel.recv_ready():
            result += str(self.pod_out.channel.recv(1024), encoding ="utf-8")
        print(result)
        return result.strip()

    def close_pod(self):
        self.pod_in.channel.send("exit" + os.linesep)
    
    def invoke_shell(self, cmd):
        channel = self.ssh.invoke_shell()
        channel.send(cmd+'\n')
        time.sleep(3)
        output = channel.recv(2024)
        output = output.decode('utf8')
        # print(output)
        return output
        # time.sleep(10)
        # stdout = channel.recv(1024*100000)
        # out_list = stdout.decode().split("\n")
        # print(out_list)
 
if __name__ == '__main__':
    pass