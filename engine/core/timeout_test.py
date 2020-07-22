import sys
import time
from timeout_handle import set_timeout, timeout_quit, timeout_continue
sys.path.append('../')
import hacks.facade

# if __name__ == '__main__':
#   def after_timeout(): # 超时后的处理函数
#     print("do something after timeout.")
  
#   @set_timeout(2, after_timeout) # 限时 2 秒
#   def connect(): # 要执行的函数
#     time.sleep(12) # 函数执行时间，写大于2的值，可测试超时
#     return 'connect success.'
  
  
#   var = connect()
#   print(var)


sum = ''
def __init__(self):
    print("__init__")

def __del__(self):
    print('我被删除了')

engine = hacks.facade.Facade()

# test handler aa
def debug1(msg):
    print("Running handler: test handler aa")
    engine.debug(msg)

# test handler bb
def debug2(msg):
    print("Running handler: test handler bb")
    engine.debug(msg)

# test add
@set_timeout(2, 'skipped add3', timeout_continue) # 限时 2 秒
def add3(x, y):
    time.sleep(12)
    print("Running task: test add3")
    global sum
    sum = engine.add(x, y)


# test debug
@set_timeout(2, 'quit from debug4', timeout_quit) # 限时 2 秒
def debug4(msg):
    time.sleep(12)
    print("Running task: test debug4")
    engine.debug(msg)

if __name__ == '__main__':
    add3(123, 223)
    debug4(sum)
    debug1('hello handler  aa')
    if sum == 346:
        debug2('hello handler  bb')
