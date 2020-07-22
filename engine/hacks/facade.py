from hacks.ssh import SSH
from hacks.debug import Debug

class Facade(object):
    
    def __init__(self):
        pass

    ssh_instance = SSH('', '')
    debug_instance = Debug('')

    def open_ssh(self, host, usr, passwd):
        self.ssh_instance.open_ssh(host, usr, passwd)
    
    def close_ssh(self):
        self.ssh_instance.close_ssh()

    def exec_cmd(self, cmd):
        self.ssh_instance.exec_cmd(cmd)

    def open_pod(self):
        self.ssh_instance.open_pod()
    
    def exec_pod_cmd(self, cmd):
        self.ssh_instance.exec_pod_cmd(cmd)
 
    def close_pod(self):
        self.ssh_instance.close_pod()

    def debug(self, msg):
        return self.debug_instance.debug(msg)

    def add(self, x, y):
        return self.debug_instance.add(x, y)

if __name__ == '__main__':
    f = Facade()
    f.debug('hello')