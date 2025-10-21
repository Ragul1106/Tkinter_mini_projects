import tkinter as tk
from tkinter import ttk, messagebox
import os

TASKS_FILE = "tasks.txt"

def add_task(event=None):
    task = task_var.get().strip()
    if not task:
        status_var.set("⚠️ Please enter a task.")
        return
    task_listbox.insert(tk.END, task)
    task_var.set("")
    status_var.set("Task added ✓")

def delete_task(event=None):
    sel = task_listbox.curselection()
    if not sel:
        status_var.set("⚠️ No task selected.")
        return
    for index in reversed(sel):
        task_listbox.delete(index)
    status_var.set("Task deleted ✓")

def clear_all():
    if task_listbox.size() == 0:
        status_var.set("Nothing to clear.")
        return
    if messagebox.askyesno("Clear All", "Delete all tasks?"):
        task_listbox.delete(0, tk.END)
        status_var.set("All tasks cleared.")

def on_double_click(event):
    delete_task()

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n")
                if line:
                    task_listbox.insert(tk.END, line)
    except Exception:
        pass

def save_tasks():
    try:
        with open(TASKS_FILE, "w", encoding="utf-8") as f:
            for i in range(task_listbox.size()):
                f.write(task_listbox.get(i) + "\n")
    except Exception:
        pass

def on_close():
    save_tasks()
    root.destroy()

root = tk.Tk()
root.title("To-Do List")
root.geometry("380x420")
root.resizable(False, False)
root.configure(bg="#f5f7fb")

style = ttk.Style(root)
try:
    style.theme_use("clam")
except:
    pass

frame = ttk.Frame(root, padding=16)
frame.pack(fill="both", expand=True)

title = ttk.Label(frame, text="📝 My To-Do List", font=("Segoe UI", 16, "bold"))
title.grid(row=0, column=0, columnspan=3, pady=(0, 10), sticky="w")

task_var = tk.StringVar()
task_entry = ttk.Entry(frame, textvariable=task_var, width=30, font=("Segoe UI", 10))
task_entry.grid(row=1, column=0, columnspan=2, sticky="we", padx=(0,8))
task_entry.focus()

add_btn = ttk.Button(frame, text="Add", command=add_task, width=10)
add_btn.grid(row=1, column=2, sticky="e")

list_frame = ttk.Frame(frame)
list_frame.grid(row=2, column=0, columnspan=3, pady=12, sticky="nsew")
frame.rowconfigure(2, weight=1)
frame.columnconfigure(0, weight=1)

scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
task_listbox = tk.Listbox(
    list_frame,
    height=12,
    activestyle="none",
    selectmode=tk.EXTENDED,
    yscrollcommand=scrollbar.set,
    font=("Segoe UI", 10),
    bd=0,
    relief="solid",
    highlightthickness=1,
    highlightbackground="#d9e0ea",
    selectbackground="#cfe3ff",
)
scrollbar.config(command=task_listbox.yview)
task_listbox.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

delete_btn = ttk.Button(frame, text="Delete Selected", command=delete_task)
delete_btn.grid(row=3, column=0, pady=(6,0), sticky="w")

clear_btn = ttk.Button(frame, text="Clear All", command=clear_all)
clear_btn.grid(row=3, column=1, pady=(6,0))

quit_btn = ttk.Button(frame, text="Quit", command=on_close)
quit_btn.grid(row=3, column=2, pady=(6,0), sticky="e")

status_var = tk.StringVar(value="Welcome — add a task and press Enter")
status_label = ttk.Label(root, textvariable=status_var, relief="flat", anchor="w", background="#f5f7fb")
status_label.pack(fill="x", side="bottom", ipady=6, padx=8, pady=(0,8))

task_entry.bind("<Return>", add_task)
task_listbox.bind("<Double-Button-1>", on_double_click)
task_listbox.bind("<Delete>", lambda e: delete_task())

load_tasks()
root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
