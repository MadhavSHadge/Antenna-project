import tkinter as tk
from tkinter import ttk, messagebox
import serial
import time
import os
os.chdir('D:\STP-2024-June-Madhav-Hadge')

# Set the correct serial port based on your system
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Adjust the port as necessary
time.sleep(2)  # Allow some time for the serial connection to establish

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
        messagebox.showinfo("Pulse Count Set", f"Motor will run for {pulses} pulses at speed {speed}")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid integer values for pulse count and speed")


# Main window
root = tk.Tk()
root.title("Arduino Motor Control")

# Frame for motor controls
control_frame = ttk.LabelFrame(root, text="Motor Controls", padding="10")
control_frame.grid(row=0, column=0, padx=10, pady=10, sticky='w')

# Speed control
speed_label = ttk.Label(control_frame, text="Set Speed (0-255):")
speed_label.grid(row=0, column=0, padx=10, pady=5)
speed_var = tk.StringVar()
speed_entry = ttk.Entry(control_frame, textvariable=speed_var, width=10)
speed_entry.grid(row=0, column=1, padx=10, pady=5)

set_speed_button = ttk.Button(control_frame, text="Set Speed", command=set_speed)
set_speed_button.grid(row=0, column=2, padx=10, pady=5)

# Frame for direction controls
direction_frame = ttk.LabelFrame(root, text="Direction Controls", padding="20")
direction_frame.grid(row=1, column=0, padx=10, pady=10, sticky='w')

# Direction control
forward_button = ttk.Button(direction_frame, text="Forward", command=forward)
forward_button.grid(row=0, column=0, padx=10, pady=5)

backward_button = ttk.Button(direction_frame, text="Backward", command=backward)
backward_button.grid(row=0, column=1, padx=10, pady=5)

stop_button = ttk.Button(direction_frame, text="Stop", command=stop_motor)
stop_button.grid(row=0, column=2, padx=10, pady=5)

direction_button = ttk.Button(direction_frame, text="Direction Count", command=direction_count)
direction_button.grid(row=0, column=3, padx=10, pady=5)

# Frame for encoder controls
encoder_frame = ttk.LabelFrame(root, text="Encoder Controls", padding="20")
encoder_frame.grid(row=2, column=0, padx=10, pady=10, sticky='w')

encoder_value_label = ttk.Label(encoder_frame, text="Current Encoder Value: N/A")
encoder_value_label.grid(row=0, column=1, padx=10, pady=5)

# Read Encoder Value button
read_encoder_button = ttk.Button(encoder_frame, text="Read Encoder Value", command=read_encoder)
read_encoder_button.grid(row=1, column=1, padx=10, pady=5)

# Frame for pulse count and angle calculation
pulse_frame = ttk.LabelFrame(root, text="Pulse Count to Angle", padding="20")
pulse_frame.grid(row=3, column=0, padx=10, pady=10, sticky='w')

pulse_label = ttk.Label(pulse_frame, text="Enter Pulse Count:")
pulse_label.grid(row=0, column=0, padx=10, pady=5)
pulse_var = tk.StringVar()
pulse_entry = ttk.Entry(pulse_frame, textvariable=pulse_var, width=10)
pulse_entry.grid(row=0, column=1, padx=10, pady=5)

write_pulse_button = ttk.Button(pulse_frame, text="Calculate Angle", command=write_encoder)
write_pulse_button.grid(row=0, column=2, padx=10, pady=5)

# Function to handle window close event
def on_closing():
    ser.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
