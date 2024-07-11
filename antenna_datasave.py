import tkinter as tk
from tkinter import ttk, messagebox
import serial
import time
import os

# Change directory to the specified path
os.chdir('/home/gmrt/Documents/STP-2024-June-Madhav-Hadge/')

# Set the correct serial port based on your system
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Adjust the port as necessary
time.sleep(2)  # Allow some time for the serial connection to establish

# File path for saving speed and pulses
file_path = 'motor_settings.txt'

# Function to read motor settings from the text file
def read_motor_settings():
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if len(lines) >= 2:
                speed_var.set(lines[0].strip())
                pulse_var.set(lines[1].strip())

# Function to write motor settings to the text file
def write_motor_settings():
    with open(file_path, 'w') as file:
        file.write(speed_var.get() + '\n')
        file.write(pulse_var.get() + '\n')

# Function to send command to Arduino
def send_command(command):
    ser.write(command.encode('utf-8'))

# Function to set motor speed
def set_speed():
    try:
        speed = int(speed_var.get())  # Get speed value from entry
        if 0 <= speed <= 255:
            ser.write(str().encode())
            ser.write(str(speed).encode())  # Send speed to Arduino
            write_motor_settings()  # Save settings to file
            messagebox.showinfo("Speed Set", f"Speed set to {speed}")
        else:
            messagebox.showerror("Error", "Speed must be between 0 and 255")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid integer speed value")

# Function to move motor forward
def forward():
    send_command('F')

# Function to move motor backward
def backward():
    send_command('B')

# Function to stop the motor
def stop_motor():
    send_command('S')

# Function to check motor pulse
def direction_count():
    send_command('D')

# Function to read encoder value
def read_encoder():
    send_command('E')  # Send command to Arduino to request encoder value
    encoder_value = ser.readline().decode().strip()  # Read the encoder value from serial
    encoder_value_label.config(text=f"Current Encoder Value: {encoder_value}")  # Update label with encoder value

# Function to write number of pulses and get angle
def write_encoder():
    try:
        speed = int(speed_var.get())  # Get speed from entry
        pulses = int(pulse_var.get())  # Get pulse count from entry
        
        # Send command 'P' followed by pulse count and speed to Arduino
        ser.write(str().encode())
        ser.write(f'P{pulses},{speed}'.encode())
        write_motor_settings()  # Save settings to file
        messagebox.showinfo("Pulse Count Set", f"Motor will run for {pulses} pulses at speed {speed}")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid integer values for pulse count and speed")

# Real-time clock function
def update_clock():
    current_time = time.localtime()
    string = time.strftime('%Y-%m-%d %H:%M:%S %p', current_time)
    clock_label.config(text=string)
    root.after(1000, update_clock)

# Function to start timer
def start_timer():
    try:
        # Get the time in seconds
        total_time = int(hours.get()) * 3600 + int(minutes.get()) * 60 + int(seconds.get())
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid integers for hours, minutes, and seconds.")
        return
    
    while total_time >= 0:
        mins, secs = divmod(total_time, 60)
        hrs, mins = divmod(mins, 60)
        
        hours.set(f"{hrs:02d}")
        minutes.set(f"{mins:02d}")
        seconds.set(f"{secs:02d}")
        
        root.update()
        time.sleep(1)
        
        total_time -= 1
        
    messagebox.showinfo("Time's up", "The timer has ended!")
    
def stop_timer():
    global timer_running
    
    # Check if the timer is currently running
    if timer_running:
        timer_running = False  # Stop the timer loop
        
        # Update the GUI to reflect the timer has stopped
        hours.set("00")
        minutes.set("00")
        seconds.set("00")
        
        # Optional: Perform any additional actions when stopping the timer
        
        # Display a message indicating the timer has been stopped
        messagebox.showinfo("Timer Stopped", "The timer has been stopped.")
    else:
        # If timer is not running, inform the user (this might be optional)
        messagebox.showinfo("Timer Not Running", "The timer is not currently running.")

    
# Initialize the timer_running flag
timer_running = False

# Main window
root = tk.Tk()
root.title("Arduino Motor Control")

# Configure grid weights for resizing
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)

# Frame for motor controls
control_frame = ttk.LabelFrame(root, text="Speed Controls", padding="10")
control_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

# Speed control
speed_label = ttk.Label(control_frame, text="Set Speed (0-255):")
speed_label.grid(row=0, column=0, padx=10, pady=5)
speed_var = tk.StringVar()
speed_entry = ttk.Entry(control_frame, textvariable=speed_var, width=10)
speed_entry.grid(row=0, column=1, padx=10, pady=5)

# Frame for direction controls
direction_frame = ttk.LabelFrame(root, text="Direction Controls", padding="20")
direction_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

# Direction control buttons
forward_button = ttk.Button(direction_frame, text="Clockwise", command=forward)
forward_button.grid(row=0, column=0, padx=10, pady=5)

backward_button = ttk.Button(direction_frame, text="Anticlockwise", command=backward)
backward_button.grid(row=0, column=1, padx=10, pady=5)

stop_button = ttk.Button(direction_frame, text="Stop", command=stop_motor)
stop_button.grid(row=0, column=2, padx=10, pady=5)

direction_button = ttk.Button(direction_frame, text="Direction Find", command=direction_count)
direction_button.grid(row=0, column=3, padx=10, pady=5)

# Frame for encoder controls
encoder_frame = ttk.LabelFrame(root, text="Encoder Value", padding="20")
encoder_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

encoder_value_label = ttk.Label(encoder_frame, text="Current Encoder Value: N/A")
encoder_value_label.grid(row=0, column=0, padx=10, pady=5)

read_encoder_button = ttk.Button(encoder_frame, text="Read Encoder Value", command=read_encoder)
read_encoder_button.grid(row=1, column=0, padx=10, pady=5)

# Frame for pulse count and angle calculation
pulse_frame = ttk.LabelFrame(root, text="Set Antenna Angle", padding="20")
pulse_frame.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

pulse_label = ttk.Label(pulse_frame, text="Enter Angle In Degrees:")
pulse_label.grid(row=0, column=0, padx=10, pady=5)
pulse_var = tk.StringVar()
pulse_entry = ttk.Entry(pulse_frame, textvariable=pulse_var, width=10)
pulse_entry.grid(row=0, column=1, padx=10, pady=5)

write_pulse_button = ttk.Button(pulse_frame, text="Set Angle", command=write_encoder)
write_pulse_button.grid(row=0, column=2, padx=10, pady=5)

angle_value_label = ttk.Label(pulse_frame, text="Current Angle Value: N/A")
angle_value_label.grid(row=1, column=0, padx=10, pady=5)

read_angle_button = ttk.Button(pulse_frame, text="Read Encoder Value")
read_angle_button.grid(row=1, column=2, padx=10, pady=5)


# Frame for setting the timer
timer_frame = ttk.LabelFrame(root, text="Set Clock For Rotation", padding="20")
timer_frame.grid(row=0, column=2, rowspan=2, padx=10, pady=10, sticky='nsew')

# Initialize StringVars for hours, minutes, and seconds
hours = tk.StringVar(value="00")
minutes = tk.StringVar(value="00")
seconds = tk.StringVar(value="00")

# Entry widgets for hours, minutes, and seconds inside the LabelFrame
tk.Entry(timer_frame, textvariable=hours, width=3, font=('calibri', 20)).grid(row=0, column=0, padx=5, pady=5)
tk.Entry(timer_frame, textvariable=minutes, width=3, font=('calibri', 20)).grid(row=0, column=1, padx=5, pady=5)
tk.Entry(timer_frame, textvariable=seconds, width=3, font=('calibri', 20)).grid(row=0, column=2, padx=5, pady=5)

# Start and stop buttons
start_button = ttk.Button(timer_frame, text="Start", command=start_timer)
start_button.grid(row=1, column=0, columnspan=3, pady=10)

stop_button = ttk.Button(timer_frame, text="Stop", command=stop_timer)
stop_button.grid(row=2, column=0, columnspan=3, pady=10)

# Clock label
clock_label = ttk.Label(timer_frame, text="", font=('calibri', 20, 'bold'))
clock_label.grid(row=3, column=0, columnspan=3, pady=10)

# Initialize settings from file
read_motor_settings()

# Start clock
update_clock()

# Main loop
root.mainloop()
