import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from skimage import io, color, feature, measure
import shutil

def EdgeDetect():

    os.chdir("Gui2D")
    os.chdir("image")
    # Get the current directory
    current_dir = os.getcwd()

    # Find all .png files in the current directory
    png_files = [f for f in os.listdir(current_dir) if f.endswith('.png')]

    # Print the list of .png files
    print("Available PNG files:")
    for i, png_file in enumerate(png_files):
        print(f"{i+1}. {png_file}")

    # Ask the user to select a file
    selection = input("Enter the number of the file you want be the pattern: ")

    # Check if the user input is valid
    if not selection.isdigit() or int(selection) < 1 or int(selection) > len(png_files):
        print("Invalid selection. Please enter a number between 1 and", len(png_files))
    else:
        # Copy the selected file to 'image.png' in the same directory
        selected_file = png_files[int(selection)-1]
        shutil.copy(os.path.join(current_dir, selected_file), os.path.join(current_dir, "image.png"))
        print(f"{selected_file} was selected.")

    # read image and convert to grayscale
    
    Irgb = io.imread("image.png")
    # Remove alpha channel
    try:
        Irgb = Irgb[:, :, :3]
        
    except IndexError:
        Igray = Irgb
        pass
    Igray = color.rgb2gray(Irgb)
    
    '''
    # display input image in grayscale
    plt.figure()    
    plt.imshow(Igray, cmap='gray')
    plt.title('Input Image in Grayscale')
    '''
    # apply Sobel edge detection
    edges = feature.canny(Igray)

    '''
    # display binary gradient mask
    plt.figure()
    plt.imshow(edges, cmap='gray')
    plt.title('Binary Gradient Mask')
    '''

    # detect boundaries and label connected components
    boundaries = measure.find_contours(edges, 0.5, fully_connected='high', positive_orientation='low')
    labels = measure.label(edges)
    '''
    # plot boundaries on original grayscale image
    plt.figure()
    plt.imshow(Igray, cmap='gray')
    plt.title('Different parts detected')
    colors = ['b', 'g', 'r', 'c', 'm', 'y']
    for k, boundary in enumerate(boundaries):
        cidx = k % len(colors)
        #plot with transparency
        plt.plot(boundary[:, 1], boundary[:, 0], colors[cidx], linewidth=2, alpha=0.5)

        # randomize text position for better visibility
        rndRow = np.random.randint(len(boundary))
        col = int(boundary[rndRow, 1])
        row = int(boundary[rndRow, 0])
        plt.text(col + 1, row - 1, str(labels[row, col]), color=colors[cidx], fontsize=14, fontweight='bold')
    '''
    # extract coordinates of selected boundary and downsample
    i = 0
    xy = np.round(boundaries[i]).astype(np.int32)
    N = 6 # adjust N to control amount of downsampling
    x1 = xy[::N, 1]
    y1 = -xy[::N, 0]
    
    
    # scale signal to between -.25 and 25
    scale = 0.25
    x1 = 2 * scale * (x1 - np.min(x1)) / (np.max(x1) - np.min(x1)) - scale
    y1 = 2 * scale * (y1 - np.min(y1)) / (np.max(y1) - np.min(y1)) - scale
    signal = np.column_stack((x1, y1))
    ''' 
    # Plot downsampled points with a moving point
    fig, ax = plt.subplots()
    ax.plot(x1, y1, '.-', markersize=10)
    ax.set_title('Downsampled Points')
    point = ax.plot([], [], 'ro')[0]

    def animate(i):
        point.set_data(x1[i], y1[i])
        return point,

    ani = FuncAnimation(fig, animate, frames=len(x1), blit=True, interval=10, repeat=True)
    plt.show()
    '''
    return signal

