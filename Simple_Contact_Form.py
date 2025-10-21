import tkinter as tk
from tkinter import ttk

def submit_form():
    name = name_entry.get()
    email = email_entry.get()
    message = message_text.get("1.0", "end-1c")  

    if not name or not email or not message:
        result_label.config(text="⚠️ Please fill all fields!", foreground="#ff4d4d")
    else:
        print(f"Name: {name}\nEmail: {email}\nMessage: {message}")
        result_label.config(text="✅ Form Submitted Successfully!", foreground="#28a745")

def on_enter(e):
    submit_button['background'] = '#0052cc'
    submit_button['foreground'] = 'white'

def on_leave(e):
    submit_button['background'] = '#007bff'
    submit_button['foreground'] = 'white'

root = tk.Tk()
root.title("Contact Form")
root.geometry("450x380")
root.config(bg="#f2f5f7")

title_label = tk.Label(root, text="Contact Us", font=("Poppins", 18, "bold"), bg="#f2f5f7", fg="#333333")
title_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))

label_font = ("Poppins", 11)
entry_font = ("Poppins", 10)

name_label = tk.Label(root, text="Name:", font=label_font, bg="#f2f5f7")
name_label.grid(row=1, column=0, sticky="e", padx=10, pady=8)

email_label = tk.Label(root, text="Email:", font=label_font, bg="#f2f5f7")
email_label.grid(row=2, column=0, sticky="e", padx=10, pady=8)

message_label = tk.Label(root, text="Message:", font=label_font, bg="#f2f5f7")
message_label.grid(row=3, column=0, sticky="ne", padx=10, pady=8)

name_entry = ttk.Entry(root, font=entry_font, width=30)
name_entry.grid(row=1, column=1, pady=8, ipady=3)

email_entry = ttk.Entry(root, font=entry_font, width=30)
email_entry.grid(row=2, column=1, pady=8, ipady=3)

message_text = tk.Text(root, font=entry_font, height=6, width=32, wrap="word", relief="solid", bd=1)
message_text.grid(row=3, column=1, pady=8, padx=5)

submit_button = tk.Button( root, text="Submit", font=("Poppins", 11, "bold"), bg="#007bff", fg="white", activebackground="#0056b3",
                activeforeground="white", relief="flat", padx=10, pady=5, cursor="hand2", command=submit_form)
submit_button.grid(row=4, column=0, columnspan=2, pady=15)

submit_button.bind("<Enter>", on_enter)
submit_button.bind("<Leave>", on_leave)

result_label = tk.Label(root, text="", font=("Poppins", 10, "italic"), bg="#f2f5f7")
result_label.grid(row=5, column=0, columnspan=2, pady=10)

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=2)

root.mainloop()