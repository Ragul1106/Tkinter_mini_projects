import tkinter as tk
from tkinter import ttk, messagebox
import re

EMAIL_RE = re.compile(r"[^@]+@[^@]+\.[^@]+")

class DynamicForm(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dynamic Form — Enable/Disable Submit")
        self.geometry("420x200")
        self.resizable(False, False)
        pad = 12

        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()

        frm = ttk.Frame(self, padding=pad)
        frm.pack(fill="both", expand=True)

        ttk.Label(frm, text="Name:").grid(row=0, column=0, sticky="w", pady=(0,6))
        self.name_entry = tk.Entry(frm, textvariable=self.name_var, width=40)
        self.name_entry.grid(row=0, column=1, sticky="w", pady=(0,6))
        self.name_entry.focus()

        ttk.Label(frm, text="Email:").grid(row=1, column=0, sticky="w", pady=(0,6))
        self.email_entry = tk.Entry(frm, textvariable=self.email_var, width=40)
        self.email_entry.grid(row=1, column=1, sticky="w", pady=(0,6))

        self.msg_var = tk.StringVar(value="")
        self.msg_label = ttk.Label(frm, textvariable=self.msg_var, foreground="red")
        self.msg_label.grid(row=2, column=0, columnspan=2, sticky="w", pady=(2,8))

        self.submit_btn = ttk.Button(frm, text="Submit", command=self.on_submit, state="disabled")
        self.submit_btn.grid(row=3, column=0, columnspan=2, pady=(6,0))

        self.name_var.trace_add("write", lambda *a: self._validate_fields())
        self.email_var.trace_add("write", lambda *a: self._validate_fields())

        self.bind("<Return>", self._on_enter_press)

        for c in range(2):
            frm.columnconfigure(c, weight=1)

    def _is_name_valid(self, name: str) -> bool:
        return bool(name.strip())

    def _is_email_valid(self, email: str) -> bool:
        return bool(EMAIL_RE.fullmatch(email.strip()))

    def _validate_fields(self):
        name = self.name_var.get()
        email = self.email_var.get()

        name_ok = self._is_name_valid(name)
        email_ok = self._is_email_valid(email)

        self.name_entry.config(bg="white" if name_ok or name=="" else "#ffd6d6")
        self.email_entry.config(bg="white" if email_ok or email=="" else "#ffd6d6")

        if not name_ok and name != "":
            self.msg_var.set("Name cannot be empty.")
        elif not email_ok and email != "":
            self.msg_var.set("Enter a valid email address (e.g. user@example.com).")
        else:
            self.msg_var.set("")

        if name_ok and email_ok:
            self.submit_btn.config(state="normal")
        else:
            self.submit_btn.config(state="disabled")

    def _on_enter_press(self, event):
        if str(self.submit_btn["state"]) == "normal":
            self.on_submit()

    def on_submit(self):
        name = self.name_var.get().strip()
        email = self.email_var.get().strip()

        if not self._is_name_valid(name):
            messagebox.showerror("Validation Error", "Name is required.", parent=self)
            return
        if not self._is_email_valid(email):
            messagebox.showerror("Validation Error", "Please enter a valid email address.", parent=self)
            return

        messagebox.showinfo("Success", f"Form submitted!\nName: {name}\nEmail: {email}", parent=self)
        self.name_var.set("")
        self.email_var.set("")
        self._validate_fields()

if __name__ == "__main__":
    app = DynamicForm()
    app.mainloop()