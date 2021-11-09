from Engine.Object import *


class Force:
    def __init__(self, axis, it, mag, id=None):
        self.axis = axis
        self.it = it
        self.actual_it = 0
        self.id = id
        self.mag = mag

    def iterate(self):
        self.actual_it += 1
        if self.actual_it == self.it:
            self.actual_it = 0
            return True
        return False
