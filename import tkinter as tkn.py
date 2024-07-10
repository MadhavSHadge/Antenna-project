import tkinter as tk
from tkinter import messagebox
import time

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

root = tk.Tk()
root.title("Timer")

# Variables to store the time
hours = tk.StringVar(value="00")
minutes = tk.StringVar(value="00")
seconds = tk.StringVar(value="00")

# Entry widgets for hours, minutes, and seconds
tk.Entry(root, textvariable=hours, width=3, font=('calibri', 20, 'bold')).grid(row=0, column=0)
tk.Label(root, text=":", font=('calibri', 20, 'bold')).grid(row=0, column=1)
tk.Entry(root, textvariable=minutes, width=3, font=('calibri', 20, 'bold')).grid(row=0, column=2)
tk.Label(root, text=":", font=('calibri', 20, 'bold')).grid(row=0, column=3)
tk.Entry(root, textvariable=seconds, width=3, font=('calibri', 20, 'bold')).grid(row=0, column=4)

# Start button
tk.Button(root, text="Start Timer", command=start_timer).grid(row=1, column=0, columnspan=5)

root.mainloop()
