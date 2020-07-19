#!/usr/bin/env python
import os
import socket
import time
import paramiko

class SSH_Hack(object):
    def __init__(self, host, username, password=None, key=None):
        self.host = host
        self.username = username
        self.password = password
        self.key = None

        if key:
            self.key = paramiko.RSAKey.from_private_key_file(key, password)

        self.pty = True
        self.ssh = None
        self.sftp = None
        self.client = None

        self.pod_in = None
        self.pod_out = None
        self.pod_err = None

    def open_ssh(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        try:
            self.ssh.connect(self.host, username=self.username, password=self.password, pkey=self.key)
        except socket.error:
            print('SSH connection failed.')
        return self.ssh

    def set_pty(self, pty):
        self.pty = pty

    def exec_cmd(self, cmd):
        command_in, command_out, command_error = self.ssh.exec_command(cmd, get_pty=self.pty)
        result = command_out.read().strip()
        print(result)
        return result

    def close_ssh(self):
        self.ssh.close()

    def open_pod(self):
        self.pod_in, self.pod_out, self.pod_err = self.ssh.exec_command('sudo su')
        return self._read_pod_cmd_output(2)

    def exec_pod_cmd(self, cmd):
        self.pod_in.channel.send(cmd + os.linesep)
        return self._read_pod_cmd_output()

    def _read_pod_cmd_output(self, timeout=30):
        time.sleep(0.5)
        time_count = 0
        while not self.pod_out.channel.recv_ready():
            time.sleep(0.1)
            time_count = time_count + 0.1
            if time_count > timeout:
                break

        result = ""
        while self.pod_out.channel.recv_ready():
            result += str(self.pod_out.channel.recv(1024), encoding ="utf-8")

        print(result)
        return result.strip()

    def close_pod(self):
        self.pod_in.channel.send("exit" + os.linesep)

    def sftp(self):
        try:
            self.client = paramiko.Transport((self.host, 22))
        except Exception as error:
            print('Connect as sftp failed.')
        else:
            try:
                self.client.connect(username=self.username, password=self.password, pkey=self.key)
            except Exception as error:
                print('Connect as sftp failed.')
            else:
                self.sftp = paramiko.SFTPClient.from_transport(self.client)
        return self.sftp

    def close_sftp(self):
        self.sftp.close()


if __name__ == '__main__':
    ssh_hack = SSH_Hack('tyserccd901', 'eccd', key='/home/omts/jenkins/ssh_key/forDirector/id_rsa')
    ssh_hack.ssh()
    print(ssh_hack.exec_cmd("pwd"))
    ssh_hack.close_ssh()
