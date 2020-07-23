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

    def open_pod(self):
        self.ssh_instance.open_pod()
    
    def exec_pod_cmd(self, cmd):
        self.ssh_instance.exec_pod_cmd(cmd)
 
    def close_pod(self):
        self.ssh_instance.close_pod()

    def invoke_shell(self, cmd):
        return self.ssh_instance.invoke_shell(cmd)

    def debug(self, msg):
        return self.debug_instance.debug(msg)

    def add(self, x, y):
        return self.debug_instance.add(x, y)

    def quit_procedure(self): # 超时后的处理函数
        exit(1)
    
    def continue_warning(self, msg): # 超时后的处理函数
        print(msg)
        pass

if __name__ == '__main__':
    f = Facade()
    f.debug('hello')