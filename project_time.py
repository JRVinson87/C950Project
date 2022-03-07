# Class to keep track of time
from datetime import *


class KeepTime:
    current_time = datetime.now()
    delayed_time = datetime.combine(date.today(), time(9, 0o5))

    def __init__(self, t='8:00'):
        h = int(t.split(':')[0])
        m = int(t.split(':')[1])
        self.current_time = datetime.combine(date.today(), time(h, m))


"""        
    def set_start(self, t):
        h = int(t.split(':')[0])
        m = int(t.split(':')[1])
        self.current_time = datetime.combine(date.today(), time(h, m))
"""
