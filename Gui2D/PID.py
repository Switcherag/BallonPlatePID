import numpy as np
class PID:
    def __init__(self, kp, ki, kd):
        
        self.framerate = 60
        
        self.kp = kp
        self.ki = ki
        self.kd = kd
      
        self.prev_error = [0,0]
        self.integral = [[0,0]]
        
    def update_angle(self, target,position):
        history = 10
       
        error = (target - position)
        self.integral += [error/history]
        self.integral = self.integral[-history:]

        derivative = (error - self.prev_error) * self.framerate 
        angle = self.kp * error + self.ki * np.sum(self.integral) + self.kd * derivative
        self.prev_error = error
                  
        return angle
