import numpy as np
class PID:
    def __init__(self, kp=0, ki=0, kd=0,framerate=60,random_error = False, std = 0.005):
        
        self.framerate = framerate
        self.random_error = random_error
        self.std = std

        self.kp = kp
        self.ki = ki
        self.kd = kd
      
        self.prev_error = 0
        self.integral = 0
        
    def update_angle(self, target,position):
        
        if self.random_error:
              position += np.random.normal(0,self.std)

        error = (target - position)
        self.integral += error 
        derivative = (error - self.prev_error) * self.framerate 
        angle = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.prev_error = error
                  
        return angle
    
    def reset(self):
        self.prev_error = 0
        self.integral = 0