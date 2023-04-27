import matplotlib.pyplot as plt
import numpy as np
from Ball import Ball
from Plate import Plate
from PID import PID

class Simulation:
    def __init__(self,timestep, MyBall, MyPID, MyPlate, target):
        
        self.MyBall = MyBall
        self.MyPID = MyPID
        self.MyPlate = MyPlate
        
        self.timestep = timestep
        self.time = -timestep
        self.frame = -1
        self.target = target
        self.len_target = len(target)

        self.pos = [0,0]
        self.vel = [0,0]
        self.angle = [0,0]
        self.desired_angle = [0,0]
        self.camera_frame = int(1/self.MyPID.framerate/self.timestep)

    # Euler's method with PID controller
    def step_forward(self):
        self.time += self.timestep
        self.frame += 1

        acceleration = self.MyBall.accel(self.angle)
        self.vel = self.vel + acceleration * self.timestep
        self.pos = self.pos + self.vel * self.timestep
        target = self.target[self.frame%self.len_target]
        #Calculate Plate movement if camera is taking a picture
        if (self.frame%self.camera_frame == 0):
            
            self.desired_angle = self.MyPID.update_angle(target,self.pos)
     
        self.angle = self.MyPlate.move(self.desired_angle,self.timestep)

        return self.pos, np.rad2deg(self.angle), self.time , self.frame,self.quadratic_error(target,self.pos),target
    

        camera_timestep = 1/self.MyPID.framerate
        #create time vector
        time = np.arange(0, duration, self.timestep)
        #create target vector
        target = time * 0 + target
        #create position and angle vectors
        self.MyBall.pos = time*0
        self.MyPlate.angle = time*0

        #reset ball and plate
        self.reset()

        i=0
        while 1:
            time = i*self.timestep
            #Calculate Ball movement
            acceleration = self.MyBall.accel(self.MyPlate.angle[-1])
            self.MyBall.vel.append(self.MyBall.vel[-1] + acceleration * self.timestep)
            self.MyBall.pos.append(self.MyBall.pos[-1] + self.MyBall.vel[i] * self.timestep)
            
            #Calculate Plate movement if camera is taking a picture
            if (i%int(camera_timestep/self.timestep) == 0):
                desired_angle = self.MyPID.update_angle(target,self.MyBall.pos[-1])
              
            self.MyPlate.move(desired_angle,self.timestep)
            i+=1
            return self.MyBall.pos[-1],time

    def quadratic_error(self,target,pos):
        error = np.sum(np.sum((target-pos)**2))
       
        return error

    def update_target(self,target):
        self.target = target    
        self.len_target = len(target)
    def Time(self):
        return self.time
    def set_Kp(self,Kp):
        self.MyPID.kp = Kp
    def set_Ki(self,Ki):
        self.MyPID.ki = Ki
    def set_Kd(self,Kd):
        self.MyPID.kd = Kd