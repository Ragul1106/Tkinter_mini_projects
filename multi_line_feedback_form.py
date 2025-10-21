import tkinter as tk
from tkinter import ttk

def submit_feedback():
    feedback = feedback_text.get("1.0", "end-1c").strip()  
    if feedback:
        result_label.config(text=f"Your Feedback:\n{feedback}", foreground="#2e8b57")
    else:
        result_label.config(text="⚠️ Please enter feedback before submitting.", foreground="#ff4d4d")

def clear_feedback():
    feedback_text.delete("1.0", "end")
    result_label.config(text="", foreground="black")
    
root = tk.Tk()
root.title("📝 Feedback Form")
root.geometry("500x400")
root.config(bg="#f2f5f7")

title_label = tk.Label(root, text="We Value Your Feedback", font=("Poppins", 16, "bold"), bg="#f2f5f7", fg="#333")
title_label.pack(pady=(20, 10))

instruction_label = tk.Label(root, text="Please share your feedback below:", font=("Poppins", 11), bg="#f2f5f7", fg="#555")
instruction_label.pack()

feedback_text = tk.Text(root, height=8, width=50, font=("Poppins", 10), relief="solid", bd=1, wrap="word")
feedback_text.pack(pady=10)

button_frame = tk.Frame(root, bg="#f2f5f7")
button_frame.pack(pady=10)

submit_btn = ttk.Button(button_frame, text="Submit", command=submit_feedback)
submit_btn.grid(row=0, column=0, padx=10)

clear_btn = ttk.Button(button_frame, text="Clear", command=clear_feedback)
clear_btn.grid(row=0, column=1, padx=10)

result_label = tk.Label(root, text="", font=("Poppins", 11), bg="#f2f5f7", justify="left", wraplength=460)
result_label.pack(pady=20)

root.mainloop()