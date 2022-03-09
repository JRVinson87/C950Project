# Class to keep track of time
from datetime import *


# Class to allow trucks to keep track of their time delivering.
class KeepTime:
    current_time = datetime.now()
    delayed_time = datetime.combine(date.today(), time(9, 0o5))

    # Constructor to allow trucks to enter their start time if they are waiting for delayed packages.
    def __init__(self, t='8:00'):
        h = int(t.split(':')[0])
        m = int(t.split(':')[1])
        self.current_time = datetime.combine(date.today(), time(h, m))

