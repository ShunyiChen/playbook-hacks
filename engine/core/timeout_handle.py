import signal
import time

print('================= RUNNING PLAYBOOK =================')

def timeout_quit(): # 超时后的处理函数
    exit(1)
    
def timeout_continue(): # 超时后的处理函数
    pass

def set_timeout(num, msg, callback):
  def wrap(func):
    def handle(signum, frame): # 收到信号 SIGALRM 后的回调函数，第一个参数是信号的数字，第二个参数是the interrupted stack frame.
      raise RuntimeError
    
    def to_do(*args, **kwargs):
      try:
        signal.signal(signal.SIGALRM, handle) # 设置信号和回调函数
        signal.alarm(num) # 设置 num 秒的闹钟
        # print('start alarm signal.')
        r = func(*args, **kwargs)
        # print('close alarm signal.')
        signal.alarm(0) # 关闭闹钟
        return r
      except RuntimeError as e:
        print(msg)
        callback()
    return to_do
  return wrap
  
if __name__ == '__main__':
    pass
 