import tkinter as tk
from time import strftime
import colorsys

# Create the main window
root = tk.Tk()
root.title("RGB Digital Clock")

# Function to update the time
def time():
    current_time = strftime('%H:%M:%S %p')  # Get the current time
    label.config(text=current_time)  # Update the label with the current time
    label.after(1000, time)  # Call the time function again after 1 second
    update_color()  # Update the text color every second

# Function to update the color
def update_color():
    global hue
    # Convert hue to RGB
    rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
    # Update label color
    label.config(fg='#%02x%02x%02x' % (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255)))
    # Increment hue
    hue = (hue + 0.01) % 1.0

# Initialize hue for color cycling
hue = 0.0

# Create a label widget to display the time
label = tk.Label(root, font=('calibri', 40, 'bold'), background='black')
label.pack(anchor='center')

# Call the time function to start the clock
time()

# Run the Tkinter event loop
root.mainloop()