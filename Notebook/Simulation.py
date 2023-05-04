import matplotlib.pyplot as plt
import numpy as np
from Ball import Ball
from Plate import Plate
from PID import PID

class Simulation:
    def __init__(self,timestep, MyBall, MyPlate, duration, MyPID=PID()):
        
        self.MyBall = MyBall
        self.MyPID = MyPID
        self.MyPlate = MyPlate
        self.duration = duration
        self.timestep = timestep
        self.time = np.arange(0, duration, timestep)
        self.target = self.time * 0 + .3

    # Euler's method with PID controller
    def euler_integration(self, angle_init=0, pos_init=0, vel_init=0,acivate_PID=True,use_friction=False, mu=0):
        camera_timestep = 1/self.MyPID.framerate
        num_timesteps = len(self.time)-1
        self.reset()
        
        acceleration = np.zeros(num_timesteps)
        vel = np.zeros(num_timesteps+1)
        pos = np.zeros(num_timesteps+1)
        angle = np.zeros(num_timesteps+1) + np.deg2rad(angle_init)
        
        for i in range(num_timesteps):
            #Calculate Ball movement
            acceleration[i] = self.MyBall.accel(angle[i])
            if use_friction:
                acceleration[i] = self.MyBall.accel_friction(angle[i], mu,static=True)
            
            vel[i+1] = vel[i] + acceleration[i] * self.timestep
            pos[i+1] = pos[i] + vel[i] * self.timestep
            if acivate_PID:
            #Calculate Plate movement if camera is taking a picture
                if (i%int(camera_timestep/self.timestep) == 0):
                    
                    desired_angle = self.MyPID.update_angle(self.target[i+1],pos[i+1])
                    
                angle[i+1] = desired_angle
                self.MyPlate.move(desired_angle,self.timestep)
        self.MyBall.pos = pos
        self.MyPlate.angle = angle        
        return pos, angle, self.time
    def euler_dt(self,target,duration=10):

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

    def quadratic_error(self):
        error = np.sum((self.MyBall.pos - self.target)**2)*self.timestep*1000
        return error
    def response_time(self):
        #return the time when the ball stay between 0.95 and 1.05 of the target
         
        for i in range(len(self.MyBall.pos)):
            if not(self.MyBall.pos[i] > 0.95*self.target[i] and self.MyBall.pos[i] < 1.05*self.target[i]):
                error = i*self.timestep
                
            
        return error
    def exceeding_error(self):
        #measure the maximum overshoot above the target
        error = 0
        for i in range(len(self.MyBall.pos)):
            if self.MyBall.pos[i] > self.target[i]:
                error = max(error,self.MyBall.pos[i]-self.target[i])
        return error
    
    def plot1D(self):
        position,angles,time = self.euler_integration()
        # Visualization
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

        # Position plot
        ax1.plot(time, position)
        ax1.set_title("Ball position for target .3")
        ax1.set_xlabel("Time (s)")
        ax1.set_ylabel("Position (m)")
        #plot target
        ax1.plot(time, self.target, label="target")
        
        # Add integral of error to the plot
        ax1.text(0.75, 0.2, f"Integrate error = {self.quadratic_error():.5f}\nResponse time = {self.response_time():.3f}", transform=ax1.transAxes)

        # Angle plot
        ax2.plot(time, np.degrees(angles))
        ax2.set_title(" angle of the plate")
        ax2.set_xlabel("Time (s)")
        ax2.set_ylabel("Angle (degrees)")
        ax2.text(0.75, 0.2, f"Paramètres :\n    Kp = {self.MyPID.kp:.3f}\n"
                                            f" Ki = {self.MyPID.ki:.3f}\n"
                                            f" Kd = {self.MyPID.kd:.3f}", transform=ax2.transAxes)

        plt.tight_layout()
        plt.show()

    def heatmap(self,a,b,target1,target2,target3,resolution=100):
        # Create figure and subplots
        fig, axs = plt.subplots(3, 3, figsize=(10,10))
        a = a
        b = b

        Kp_values = np.linspace(a, b, num=resolution)
        Kd_values = np.linspace(a, b, num=resolution)
        Ki_values = 0

        # initialisation d'un tableau pour stocker les valeurs de la fonction de coût
        quadratic_error = np.zeros((len(Kp_values), len(Kd_values)))
        response_time = np.zeros((len(Kp_values), len(Kd_values)))
        exceeding_error = np.zeros((len(Kp_values), len(Kd_values)))

        quadratic_error1 = np.zeros((len(Kp_values), len(Kd_values)))
        response_time1 = np.zeros((len(Kp_values), len(Kd_values)))
        exceeding_error1 = np.zeros((len(Kp_values), len(Kd_values)))

        quadratic_error2 = np.zeros((len(Kp_values), len(Kd_values)))
        response_time2 = np.zeros((len(Kp_values), len(Kd_values)))
        exceeding_error2 = np.zeros((len(Kp_values), len(Kd_values)))

        # calcul des valeurs correspondantes de la fonction de coût pour chaque paire de valeurs de Kp et Kd
        self.target = self.time*0+target1
        for i, Kp in enumerate(Kp_values):
            
            #add loading bar \r
            print(f"iteration {i+1}/{len(Kp_values)}", end="\r")
            for j, Kd in enumerate(Kd_values):
                self.MyPID.kp = Kp
                self.MyPID.kd = Kd
                self.euler_integration()
                
                quadratic_error[i,j] = self.quadratic_error()
                response_time[i,j] = self.response_time()
                exceeding_error[i,j] = self.exceeding_error()

        # calcul des valeurs correspondantes de la fonction de coût pour chaque paire de valeurs de Kp et Kd
        self.target = self.time*0+target2
        for i, Kp in enumerate(Kp_values):
            #add loading bar \r
            print(f"iteration {i+1}/{len(Kp_values)}", end="\r")
            for j, Kd in enumerate(Kd_values):
                self.MyPID.kp = Kp
                self.MyPID.kd = Kd
                self.euler_integration()
                
                quadratic_error1[i,j] = self.quadratic_error()
                response_time1[i,j] = self.response_time()
                exceeding_error1[i,j] = self.exceeding_error()
        
        # calcul des valeurs correspondantes de la fonction de coût pour chaque paire de valeurs de Kp et Kd
        self.target = self.time*0+target3
        for i, Kp in enumerate(Kp_values):
            #add loading bar \r
            print(f"iteration {i+1}/{len(Kp_values)}", end="\r")
            for j, Kd in enumerate(Kd_values):
                self.MyPID.kp = Kp
                self.MyPID.kd = Kd
                self.euler_integration()
                
                quadratic_error2[i,j] = self.quadratic_error()
                response_time2[i,j] = self.response_time()
                exceeding_error2[i,j] = self.exceeding_error()
        # Plot heatmaps and colorbars
        axs[0][0].imshow(quadratic_error, cmap='rainbow', aspect='auto',origin='lower',extent=[a,b,a,b], vmin=np.min(quadratic_error), vmax=2*np.min(quadratic_error))
        axs[0][1].imshow(response_time, cmap='rainbow', aspect='auto',origin='lower',extent=[a,b,a,b], vmin=np.min(response_time), vmax=2*np.min(response_time))
        axs[0][2].imshow(exceeding_error, cmap='rainbow', aspect='auto',origin='lower',extent=[a,b,a,b], vmin=np.min(exceeding_error), vmax=target1*.1)
        axs[1][0].imshow(quadratic_error1, cmap='rainbow', aspect='auto',origin='lower',extent=[a,b,a,b], vmin=np.min(quadratic_error1), vmax=2*np.min(quadratic_error1))
        axs[1][1].imshow(response_time1, cmap='rainbow', aspect='auto',origin='lower',extent=[a,b,a,b], vmin=np.min(response_time1), vmax=2*np.min(response_time1))
        axs[1][2].imshow(exceeding_error1, cmap='rainbow', aspect='auto',origin='lower',extent=[a,b,a,b], vmin=np.min(exceeding_error1), vmax=target2*.1)
        axs[2][0].imshow(quadratic_error2, cmap='rainbow', aspect='auto',origin='lower',extent=[a,b,a,b], vmin=np.min(quadratic_error2), vmax=2*np.min(quadratic_error2))
        axs[2][1].imshow(response_time2, cmap='rainbow', aspect='auto',origin='lower',extent=[a,b,a,b], vmin=np.min(response_time2), vmax=2*np.min(response_time2))
        axs[2][2].imshow(exceeding_error2, cmap='rainbow', aspect='auto',origin='lower',extent=[a,b,a,b], vmin=np.min(exceeding_error2), vmax=target3*.1)
    
         # Set titles in respect of the target
        axs[0][0].set_title("Quadratic error, target = " + str(target1))
        axs[0][1].set_title("Response time, target = " + str(target1))
        axs[0][2].set_title("Exceeding error, target = " + str(target1))
        axs[1][0].set_title("Quadratic error, target = " + str(target2))
        axs[1][1].set_title("Response time, target = " + str(target2))
        axs[1][2].set_title("Exceeding error, target = " + str(target2))
        axs[2][0].set_title("Quadratic error, target = " + str(target3))
        axs[2][1].set_title("Response time, target = " + str(target3))
        axs[2][2].set_title("Exceeding error, target = " + str(target3))
        
        # Set labels in a loop
        for i in range(3):
            for j in range(3):
                axs[i][j].set_xlabel("Kd")
                axs[i][j].set_ylabel("Kp")

        
        

        
        # Show the plot
        plt.show()

    def heatmap_target(self,a,b,targets,targets_names,resolution=100):
        
        Kp_values = np.linspace(a, b, num=resolution)
        Kd_values = np.linspace(a, b, num=resolution)
        Ki_values = [0,0.01,0.05,.1,.5,1,5,10]

        #define targets
        # initialisation d'un tableau pour stocker les valeurs de la fonction de coût
        quadratic_error = np.zeros((len(targets),len(Ki_values),len(Kp_values),len(Kd_values) ))

        # Create figure and subplots
        fig, axs = plt.subplots(len(targets)+1,len(Ki_values), figsize=(20, 20), facecolor='w', edgecolor='k')

        quadratic_min = 0
        quadratic_max = 40    
        for t, target in enumerate(targets):
            self.target = target
            for i, Ki in enumerate(Ki_values):
                #add loading bar \r
                print(f"iteration {i+1}/{len(Ki_values)}", end="\r")
                
                for j, Kp in enumerate(Kp_values):
                    for k, Kd in enumerate(Kd_values):
                        self.MyPID.kp = Kp
                        self.MyPID.kd = Kd
                        self.MyPID.ki = Ki
                        self.euler_integration()
                        
                        quadratic_error[t,i,j,k] = self.quadratic_error()
                    axs[t][i].imshow(quadratic_error[t][i], cmap='rainbow', aspect='auto',origin='lower',extent=[a,b,a,b], vmin=quadratic_min, vmax=quadratic_max,interpolation='none')            
                axs[0][i].set_title("Ki = " + str(Ki_values[i]))
                #set a title to the  figure
                # label the axis on the other side while keeping the other one left
                axs[t][0].set_ylabel("Kd target = " + targets_names[t])
                axs[t][i].set_xlabel("Kp")
            
             
            print("Quadratic_min = ", np.min(quadratic_error[t,:,:,:]))
            
                
        
      
        # last plot with the sum of the quadratic error
        for k in range(len(Ki_values)):
            axs[-1][k].imshow(np.max(quadratic_error[:,k,:,:],axis=0), cmap='rainbow', aspect='auto',origin='lower',extent=[a,b,a,b], vmin=quadratic_min, vmax=quadratic_max,interpolation='none')
            #set a title to the  figure
            # label the axis on the other side while keeping the other one left
            axs[-1][0].set_ylabel("Kd for all target")
            axs[-1][k].set_xlabel("Kp")
         

        plt.show()
    def reset(self):
        self.MyBall.reset()
        self.MyPlate.reset()
        self.MyPID.reset()
        return self