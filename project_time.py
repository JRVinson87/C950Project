# Class to keep track of time
from datetime import *


class KeepTime:
    current_time = datetime.combine(date.today(), time(8, 00))
    delayed_time = datetime.combine(date.today(), time(9, 0o5))



