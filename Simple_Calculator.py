import tkinter as tk

def button_click(number):
    current = display_var.get()
    display_var.set(current + str(number))

def evaluate():
    try:
        result = eval(display_var.get())
        display_var.set(result)
    except Exception:
        display_var.set("Error")

def clear():
    display_var.set("")

root = tk.Tk()
root.title("Simple Calculator")
root.geometry("400x500")
root.config(bg="#f4f6f7")

display_var = tk.StringVar()

display = tk.Label(
    root,
    textvariable=display_var,
    height=2,
    font=("Arial", 24, "bold"),
    relief="sunken",
    anchor="e",
    bg="white",
    fg="black",
    bd=10
)
display.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

buttons = [
    ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
    ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
    ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
    ("0", 4, 0), ("C", 4, 1), ("=", 4, 2), ("+", 4, 3)
]

for (text, row, col) in buttons:
    if text == "=":
        btn = tk.Button(
            root,
            text=text,
            width=10,
            height=2,
            font=("Arial", 18, "bold"),
            bg="#2ecc71",
            fg="white",
            activebackground="#27ae60",
            command=evaluate
        )
    elif text == "C":
        btn = tk.Button(
            root,
            text=text,
            width=10,
            height=2,
            font=("Arial", 18, "bold"),
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            command=clear
        )
    else:
        btn = tk.Button(
            root,
            text=text,
            width=10,
            height=2,
            font=("Arial", 18, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            command=lambda t=text: button_click(t)
        )
    btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

for i in range(5):
    root.grid_rowconfigure(i, weight=1)
for i in range(4):
    root.grid_columnconfigure(i, weight=1)

root.mainloop()
