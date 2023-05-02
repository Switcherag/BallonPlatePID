from Simulation import *

# Create the initial sine wave with amplitude 1 and phase 0
Kd = 0
Kp = 0

MyPID = PID(Kp,0,Kd)
PingBall = Ball()
WoodPlate = Plate(0)

MySimulation = Simulation(0.001, PingBall, WoodPlate, 5, MyPID)
target1 = MySimulation.time/15
target2 = np.sin(MySimulation.time)
target3 = MySimulation.time*0+.3
MySimulation.heatmap_target(a=0,b=100,target=target3,resolution=50)