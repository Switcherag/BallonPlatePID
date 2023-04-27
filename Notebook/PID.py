import numpy as np
class PID:
    def __init__(self, kp=0, ki=0, kd=0,framerate=1000):
        
        self.framerate = framerate
        
        self.kp = kp
        self.ki = ki
        self.kd = kd
      
        self.prev_error = 0
        self.integral = 0
        
    def update_angle(self, target,position):
       
        error = (target - position)
        self.integral += error 
        derivative = (error - self.prev_error) * self.framerate 
        angle = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.prev_error = error
                  
        return angle
    
    def reset(self):
        self.prev_error = 0
        self.integral = 0