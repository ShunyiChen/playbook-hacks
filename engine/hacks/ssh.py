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
        self.channel = None

    def open_ssh(self, host, usr, passwd):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        try:
            self.ssh.connect(host, username=usr, password=passwd, pkey=self.key)
        except socket.error:
            print('SSH connection failed.')
        return self.ssh
  
    def invoke_shell(self, cmd, passwd=None):
        if self.channel is None:
            self.channel = self.ssh.invoke_shell()
        self.channel.send(cmd+'\n')
        time.sleep(1)
        resp = ''
        while self.channel.recv_ready():
            channel_bytes = self.channel.recv(9999)
            channel_data = channel_bytes.decode('utf8')
            if channel_data.endswith(("~ # ", "~> ", "# ", " / # ",":/# ", "~]# ")):
                print("---------"+channel_data)
            elif channel_data.endswith(("? ")):
                self.channel.send('yes'+'\n')
            elif channel_data.endswith(("password: ")):
                self.channel.send(passwd+'\n')
            else:
                print("error:xxxxxxxxxx"+channel_data)
        return resp

     
    def quit_shell(self):
        return self.invoke_shell('exit')

    def close_channel(self):
        self.channel.close()

if __name__ == '__main__':
    pass