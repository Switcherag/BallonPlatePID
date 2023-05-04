import numpy as np

class Plate:
    def __init__(self, initial_angle=0):
        self.angle_pos_max = np.deg2rad(20)
        self.angle_vel_max = np.deg2rad(40)
        self.angle = [initial_angle]
        
    def move(self,new_angle, timestep):
        
        new_angle = min(max(new_angle, -self.angle_pos_max), self.angle_pos_max)
        angle_vel = (new_angle - self.angle[-1]) / timestep
        angle_vel = min(max(angle_vel, -self.angle_vel_max), self.angle_vel_max)
        new_angle = self.angle[-1] + angle_vel * timestep
        self.angle += [new_angle]
        return new_angle
    
    def reset(self):
        self.angle = [self.angle[0]]
    