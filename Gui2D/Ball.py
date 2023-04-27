import numpy as np

class Ball:
    def __init__(self):
        self.m = 0.0027
        self.R = 0.022
        self.g = -9.8
        self.J = 2/3 * self.m * self.R**2
       
    def accel(self, angle):
        
        return -self.m * self.g * np.sin(angle) / (self.J / self.R**2 + self.m)