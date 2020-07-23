class Debug(object):
    
    def __init__(self):
        pass
  
    def debug(self, msg):
        if type(msg) is int:
           print(str(msg))
        if type(msg) is str:
           print(msg)
           
    def add(self, x, y):
        return x + y