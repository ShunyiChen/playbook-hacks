from hacks.ssh import SSH
from hacks.debug import Debug

class Facade(object):
    
    def __init__(self):
        pass

    ssh_instance = SSH('', '')
    debug_instance = Debug()

    def open_ssh(self, host, usr, passwd):
        self.ssh_instance.open_ssh(host, usr, passwd)

    def invoke_shell(self, cmd, passwd=None):
        return self.ssh_instance.invoke_shell(cmd, passwd)

    def quit_shell(self):
        return self.ssh_instance.quit_shell()

    def close_channel(self):
        return self.ssh_instance.close_channel()

    def debug(self, msg):
        return self.debug_instance.debug(msg)

    def quit_procedure(self): # 超时后的处理函数
        print('Exited.')
        exit(1)
        
    def continue_warning(self, msg): # 超时后的处理函数
        print(msg)
        pass

if __name__ == '__main__':
    f = Facade()
    f.debug('hello')