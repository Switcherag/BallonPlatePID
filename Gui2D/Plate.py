import numpy as np

class Plate:
    def __init__(self):
        self.angle_pos_max = np.deg2rad(20)
        self.angle_vel_max = np.deg2rad(140)
        self.prev_angle = [0,0]
        
    def move(self,new_angle, timestep):
        #new angle is like [0.1,0.1]
        # check if new angle is within limits in position and velocity

        new_angle = np.clip(new_angle, -self.angle_pos_max, self.angle_pos_max)
        new_angle_vel = (new_angle - self.prev_angle) / timestep
        new_angle_vel = np.clip(new_angle_vel, -self.angle_vel_max, self.angle_vel_max)
        new_angle = self.prev_angle + new_angle_vel * timestep
        self.prev_angle = new_angle
        
        return new_angle
