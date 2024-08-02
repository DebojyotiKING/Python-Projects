import tkinter as tk
from tkinter import messagebox
import math

# Function to evaluate the expression
def evaluate_expression(event=None):
    try:
        result = eval(display.get())
        display.delete(0, tk.END)
        display.insert(tk.END, str(result))
    except Exception as e:
        messagebox.showerror("Error", "Invalid Input")

# Function to append a character to the display
def append_character(char):
    display.insert(tk.END, char)

# Function to clear the display
def clear_display():
    display.delete(0, tk.END)

# Create the main window
root = tk.Tk()
root.title("Scientific Calculator")
root.configure(bg="#282C34")

# Create the display
display = tk.Entry(root, font=("Arial", 20), borderwidth=5, relief=tk.SUNKEN, bg="#ABB2BF", fg="#282C34")
display.grid(row=0, column=0, columnspan=6, padx=10, pady=10, sticky="nsew")

# Bind the Return key to evaluate the expression
root.bind("<Return>", evaluate_expression)

# Define the buttons
buttons = [
    '7', '8', '9', '/', 'C', '(',
    '4', '5', '6', '*', 'sqrt', ')',
    '1', '2', '3', '-', 'pow', 'log',
    '0', '.', '=', '+', 'pi'
]

row_val = 1
col_val = 0

for button in buttons:
    if button == "=":
        btn = tk.Button(root, text=button, font=("Arial", 18), bg="#61AFEF", fg="#282C34", command=evaluate_expression)
    elif button == "C":
        btn = tk.Button(root, text=button, font=("Arial", 18), bg="#E06C75", fg="#282C34", command=clear_display)
    elif button == "sqrt":
        btn = tk.Button(root, text=button, font=("Arial", 18), bg="#98C379", fg="#282C34", command=lambda: append_character('math.sqrt('))
    elif button == "pow":
        btn = tk.Button(root, text=button, font=("Arial", 18), bg="#98C379", fg="#282C34", command=lambda: append_character('math.pow('))
    elif button == "log":
        btn = tk.Button(root, text=button, font=("Arial", 18), bg="#98C379", fg="#282C34", command=lambda: append_character('math.log('))
    elif button == "pi":
        btn = tk.Button(root, text=button, font=("Arial", 18), bg="#D19A66", fg="#282C34", command=lambda: append_character('math.pi'))
    else:
        btn = tk.Button(root, text=button, font=("Arial", 18), bg="#61AFEF", fg="#282C34", command=lambda b=button: append_character(b))
    
    btn.grid(row=row_val, column=col_val, padx=5, pady=5, sticky="nsew")
    
    col_val += 1
    if col_val > 5:
        col_val = 0
        row_val += 1

# Make the buttons expand and fill the available space
for i in range(6):
    root.grid_columnconfigure(i, weight=1)
for i in range(row_val + 1):
    root.grid_rowconfigure(i, weight=1)

# Start the main loop
root.mainloop()