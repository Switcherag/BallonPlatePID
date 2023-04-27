import numpy as np

class Ball:
    # Constants
   
    def __init__(self):
        self.pos = [0]
        self.vel = [0] 
        self.m = 0.0027
        self.R = 0.02
        self.g = -9.8
        self.J = 3e-8
        self.constant_friction = 1
        
    def accel(self, angle,static=False):
        friction = self.constant_friction
        if(static):
            friction = 0.9
        return -self.m * self.g * np.sin(angle) / (self.J / self.R**2 + self.m)*friction
    
    def accel_friction(self, angle, mu,static=False):
        friction = self.constant_friction
        if(static):
            friction = 0.9
        tan = -self.m * self.g * np.sin(angle)*friction
        norm = self.m * self.g * np.cos(angle)
        den = (self.J / self.R**2 + self.m)
        return  (tan + mu * norm )/ den  
    
    def reset(self):
        self.pos = [0]
        self.vel = [0]
    def setter(self, m, R, J):
        self.m = m
        self.R = R
        self.J = J
        