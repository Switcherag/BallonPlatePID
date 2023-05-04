import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from PIL import ImageTk, Image
import numpy as np
from Simulation import *
import time as tm
import threading
from detect import *

Kp = 15
Ki = 1
Kd = 6


Pingpong_Ball = Ball()
Wood_Plate = Plate()
PID_Controller = PID(Kp,Ki,Kd)

#import signal.npy
signal = EdgeDetect()

sim_timestep = 0.006
SimStart = 0
n = sim_timestep/0.0006
x = signal[:,0]
y = signal[:,1]
x_upsampled = np.interp(np.arange(0, len(x), 1/n), np.arange(0, len(x)), x)
y_upsampled = np.interp(np.arange(0, len(y), 1/n), np.arange(0, len(y)), y)
upsampled_signal = np.column_stack((x_upsampled, y_upsampled))
#upsampled_signal = np.repeat(signal, n, axis=0)

img_target = upsampled_signal


MySimulation = Simulation(sim_timestep,Pingpong_Ball,PID_Controller,Wood_Plate,img_target)


# Define the GUI window
root = tk.Tk()
root.title("Real-time Plot")
#open fullscreen windowed mode
root.attributes('-topmost', True)
def on_closing():
    print()
    print("Gui closed")
    print("Simulation time: ", MySimulation.Time(), "s")
    print()
    print("restart the kernel to run again please wait ...")
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Define the four squares
# create the frames and label widgets
plot1_frame = tk.Frame(root, width=400, height=400, bg="white", highlightbackground="black", highlightthickness=1)
plot2_frame = tk.Frame(root, width=400, height=400, bg="white", highlightbackground="black", highlightthickness=1)
button_frame = tk.Frame(root, width=400, height=200, bg="white", highlightbackground="black", highlightthickness=1)
slider_frame = tk.Frame(root, width=200, height=200, bg="white", highlightbackground="black", highlightthickness=1)
time_display = tk.Label(root, text="Time: 0.0 s")
text_display = tk.Label(root, text="Rapid Resonse -> High Kp Low Kd \nAccurate Response (offset) -> Low Kp High Kd")
# grid the widgets
plot1_frame.grid(row=0, column=0, padx=20, pady=10)
plot2_frame.grid(row=0, column=1, padx=20, pady=10)
button_frame.grid(row=2, column=0, padx=0, pady=10)
slider_frame.grid(row=2, column=1, padx=20, pady=10)

#put time display bewteww button and slider
time_display.grid(row=1, column=0, padx=0, pady=0)
#put text display in the middle
text_display.grid(row=1, column=1, padx=0, pady=0)

# Define the live plots for square 2
fig2 = plt.Figure(figsize=(5, 5), dpi=100)# Define the background image and buttons for square 4
img = Image.open("image.png")
img = img.resize((200, 200), Image.LANCZOS)
photo = ImageTk.PhotoImage(img)
background_label = tk.Label(button_frame, image=photo)
background_label.place(x=0, y=0)  

def set_Kp(event):
    MySimulation.set_Kp(Kp_slider.get())
def set_Ki(event):
    MySimulation.set_Ki(Ki_slider.get())
def set_Kd(event):
    MySimulation.set_Kd(Kd_slider.get())

# Define the sliders and print the value when the slider is moved
Kp_slider = tk.Scale(slider_frame, from_=0, to=20, orient=tk.HORIZONTAL, command= set_Kp, resolution=0.01, length=400, label="Kp")
Kp_slider.set(Kp)
Kp_slider.pack()

Ki_slider = tk.Scale(slider_frame, from_=0, to=10, orient=tk.HORIZONTAL, command= set_Ki, resolution=0.01, length=400, label="Ki")
Ki_slider.set(Ki)
Ki_slider.pack()

Kd_slider = tk.Scale(slider_frame, from_=0, to=20, orient=tk.HORIZONTAL, command= set_Kd, resolution=0.01, length=400, label="Kd")
Kd_slider.set(Kd)
Kd_slider.pack()

def reset_time():
    return
    
# Define the buttons on square 4
button1 = tk.Button(button_frame, text="Reset time", command=reset_time)
button1.place(x=250, y=0)

real_time = True
def Toggle_real_time():
    global real_time, SimStart
    SimStart = tm.time()
    if real_time == True:
        real_time = False
        
        button2.config(text="Asap")
    else:
        real_time = True
        
        button2.config(text="Real Time")

button2 = tk.Button(button_frame, text="Real Time", command=Toggle_real_time)
button2.place(x=250, y=50)

def downsample():
    global trail
    old_target = MySimulation.target
    downsampled_target = np.delete(old_target, np.arange(0, len(old_target), 2), axis=0)
    MySimulation.update_target(downsampled_target)
    trail = len(downsampled_target)
    
def upsample():
    global trail
    old_target = MySimulation.target
    x = old_target[:,0]
    y = old_target[:,1]
    x_upsampled = np.interp(np.arange(0, len(x), 1/2), np.arange(0, len(x)), x)
    y_upsampled = np.interp(np.arange(0, len(y), 1/2), np.arange(0, len(y)), y)
    upsampled_target = np.column_stack((x_upsampled, y_upsampled))
    MySimulation.update_target(upsampled_target)
    trail = len(upsampled_target)

button3 = tk.Button(button_frame, text="Upspeed", command=downsample)
button3.place(x=250, y=100)

button4 = tk.Button(button_frame, text="Downspeed", command=upsample)
button4.place(x=250, y=150)


# Define the live plot for square 1
fig1 = plt.Figure(figsize=(5, 5), dpi=100)
ax1 = fig1.add_subplot(111)
#while click pressed, update ball position
def Ball_placement(event):
    if event.button == 1 and event.inaxes == ax1:
        # Get the x and y coordinates of the event
        x, y = event.xdata, event.ydata
        x = event.xdata
        y = event.ydata
        MySimulation.pos = [x,y]
        MySimulation.vel = [0,0]
    
fig1.canvas.mpl_connect('motion_notify_event', Ball_placement)

# set limits for x and y axes
ax1.set_xlim(-.3,.3)
ax1.set_ylim(-.3,.3)
# Target plot
target_plot, = ax1.plot([], [], 'g-', markersize=3)
target_point, = ax1.plot([], [], 'go', markersize=10)
trajectory_plot, = ax1.plot([], [], 'b-')
target_plot.set_data(img_target[:,0], img_target[:,1])
# Ball plot
ball_plot, = ax1.plot([], [], 'ro')
# Add Tiltes and labels
ax1.set_title('Ball Trajectory')
ax1.set_xlabel('x (m)')
ax1.set_ylabel('y (m)')

def update_plotxy():
    # Draw the trajectory , the ball, and the target
        trajectory_plot.set_data(xdata, ydata) 
        ball_plot.set_data(xdata[-1], ydata[-1])
        target_point.set_data(target_coord[0], target_coord[1])
        ax1.relim() 
        canvas1.draw()
canvas1 = FigureCanvasTkAgg(fig1, master=plot1_frame)
canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Define the live plots for square 2
fig2 = plt.Figure(figsize=(5, 5), dpi=100)
ax2_1 = fig2.add_subplot()
line2_1, = ax2_1.plot([], [], 'b-')
line2_2, = ax2_1.plot([], [], 'r-')

# set limits for x and y axes
ax2_1.set_ylim(-21, 21)
#Set other y scale for line2_3
ax2_1_2 = ax2_1.twinx()
ax2_1_2.set_ylim(0, 4)
line2_3, = ax2_1_2.plot([], [], 'g-')

def update_plotaxy(x,y1,y2,error):
   
    # Code to update plot2_1 and plot2_2
    line2_1.set_data(x, y1)
    ax2_1.relim()
    ax2_1.autoscale_view(True,True,True)
    line2_2.set_data(x, y2)
    line2_3.set_data(x, error)
 
    canvas2.draw()

# Add Tiltes and labels
ax2_1.set_title('Plate angle and error)')
#add label to second y axis
ax2_1_2.set_ylabel('Log(error)')
ax2_1.set_xlabel('Time (s)')
ax2_1.set_ylabel('Angle (deg)')
ax2_1.legend(['Angle X', 'Angle Y'])
ax2_1_2.legend(['Error'])
canvas2 = FigureCanvasTkAgg(fig2, master=plot2_frame)
canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

   


#initilaize with empty numpy array
xdata = np.array([])
ydata = np.array([])

xtime = np.array([])
ydata1 =  np.array([])
ydata2 = np.array([])
y = np.array([])    
target_coord = np.array([])
trail = 2390
error = np.array([])
interror = np.array([])

# Define a function to update the plot and parameter graph
def update():
    global sim_timestep, xdata, ydata, ydata1, ydata2, y, xtime, MySimulation, error, target_coord, interror, real_time, SimStart

    delay = 0
    SimStart = tm.time()
    thread1 = threading.Thread(target=update_plotxy)

    # measure time execution of the update function
    while True:
        start = tm.time_ns()

        pos, angle, time, frame, quad_error, target = MySimulation.step_forward()
        # add new point to the numpy array
        xdata = np.append(xdata, pos[0])
        ydata = np.append(ydata, pos[1])
        ydata1 = np.append(ydata1, angle[0])
        ydata2 = np.append(ydata2, angle[1])
        xtime = np.append(xtime, time)
        error = np.append(error, quad_error*10)
        interror = np.append(interror, np.log(np.sum(error)+1))
        

        target_coord = target
        # keep only the trail latest points
        xdata = xdata[-trail:]
        ydata = ydata[-trail:]
        ydata1 = ydata1[-trail:]
        ydata2 = ydata2[-trail:]
        y = y[-trail:]
        xtime = xtime[-trail:]
        error = error[-trail:]
        interror = interror[-trail:]

        if frame%40== 0:
            thread2 = threading.Thread(target=update_plotaxy(xtime,ydata1,ydata2,interror))
            thread2.start()
           
        if not thread1.is_alive():
            thread1 = threading.Thread(target=update_plotxy)       
            thread1.start()

        # delay the next update to match the timestep
        root.update()
        end = tm.time_ns()
        
        if frame%1000 == 0:
        #Add a tilte above sliders in which the simulation time will be displayed
            title = "Real time: " + str(round(end/1000_000_000-SimStart, 2)) + "s \n Simulation time: " + str(round(MySimulation.Time(), 2)) + "s"
            time_display.config(text=title)
        if real_time:
            delay = max(frame*sim_timestep - (end/1000_000_000-SimStart),0)
            tm.sleep(delay)
            
        
# Add a button to update the plot and parameter graph
#update_button = tk.Button(root, text="Update", command=update)
#update_button.grid(row=1, column=2)
root.after(100, update)

# Start the GUI loop
root.mainloop()


