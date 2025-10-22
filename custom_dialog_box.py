import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import os

class SaveBeforeCloseDialog(tk.Toplevel):
    def __init__(self, parent, filename=None):
        super().__init__(parent)
        self.parent = parent
        self.title("Save changes?")
        self.resizable(False, False)
        self.grab_set()
        self.result = None
        body = ttk.Frame(self, padding=12)
        body.pack(fill="both", expand=True)
        label_text = f"Do you want to save changes to '{filename}'?" if filename else "Do you want to save changes to the current document?"
        ttk.Label(body, text=label_text, wraplength=300).pack(pady=(0, 12))
        btn_frame = ttk.Frame(body)
        btn_frame.pack(fill="x", pady=(6,0))
        ttk.Button(btn_frame, text="Save", command=self._save).pack(side="left", expand=True, padx=4)
        ttk.Button(btn_frame, text="Don't Save", command=self._dont_save).pack(side="left", expand=True, padx=4)
        ttk.Button(btn_frame, text="Cancel", command=self._cancel).pack(side="left", expand=True, padx=4)
        self.update_idletasks()
        x = self.parent.winfo_rootx() + (self.parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = self.parent.winfo_rooty() + (self.parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
        self.protocol("WM_DELETE_WINDOW", self._cancel)

    def _save(self):
        self.result = "save"
        self.destroy()

    def _dont_save(self):
        self.result = "dont_save"
        self.destroy()

    def _cancel(self):
        self.result = "cancel"
        self.destroy()

class TextEditorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Custom Dialogs - Text Editor")
        self.geometry("800x500")
        self.current_filename = None
        self._text_modified = False
        self._create_widgets()
        self._create_menu()
        self._bind_events()

    def _create_widgets(self):
        toolbar = ttk.Frame(self, padding=4)
        toolbar.pack(side="top", fill="x")
        ttk.Button(toolbar, text="New", command=self.new_file).pack(side="left", padx=2)
        ttk.Button(toolbar, text="Open", command=self.open_file).pack(side="left", padx=2)
        ttk.Button(toolbar, text="Save", command=self.save_file).pack(side="left", padx=2)
        text_frame = ttk.Frame(self)
        text_frame.pack(fill="both", expand=True, padx=6, pady=6)
        self.text = tk.Text(text_frame, wrap="word", undo=True)
        self.text.pack(side="left", fill="both", expand=True)
        self.text.focus_set()
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.text.yview)
        scrollbar.pack(side="right", fill="y")
        self.text.configure(yscrollcommand=scrollbar.set)
        self.status_var = tk.StringVar(value="Ready")
        status = ttk.Label(self, textvariable=self.status_var, relief="sunken", anchor="w", padding=4)
        status.pack(side="bottom", fill="x")

    def _create_menu(self):
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", accelerator="Ctrl+N", command=self.new_file)
        filemenu.add_command(label="Open...", accelerator="Ctrl+O", command=self.open_file)
        filemenu.add_command(label="Save", accelerator="Ctrl+S", command=self.save_file)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.exit_app)
        menubar.add_cascade(label="File", menu=filemenu)
        self.config(menu=menubar)

    def _bind_events(self):
        self.text.bind("<<Modified>>", self._on_text_modified)
        self.bind_all("<Control-n>", lambda e: self.new_file())
        self.bind_all("<Control-o>", lambda e: self.open_file())
        self.bind_all("<Control-s>", lambda e: self.save_file())
        self.protocol("WM_DELETE_WINDOW", self.exit_app)

    def _on_text_modified(self, event=None):
        if self.text.edit_modified():
            self._text_modified = True
            self._update_status("Modified")
            self.text.edit_modified(False)

    def _update_status(self, msg):
        filename_display = self.current_filename if self.current_filename else "Untitled"
        self.status_var.set(f"{filename_display} — {msg}")

    def new_file(self):
        if self._text_modified:
            dlg = SaveBeforeCloseDialog(self, filename=self.current_filename)
            self.wait_window(dlg)
            if dlg.result == "save":
                if not self.save_file():
                    return
            elif dlg.result == "cancel":
                return
        self.text.delete("1.0", tk.END)
        self.current_filename = None
        self._text_modified = False
        self._update_status("New file")

    def open_file(self):
        if self._text_modified:
            dlg = SaveBeforeCloseDialog(self, filename=self.current_filename)
            self.wait_window(dlg)
            if dlg.result == "save":
                if not self.save_file():
                    return
            elif dlg.result == "cancel":
                return
        fname = simpledialog.askstring("Open", "Enter file name to open (relative or absolute):", parent=self)
        if not fname:
            self._update_status("Open cancelled")
            return
        if not os.path.isabs(fname):
            fname = os.path.abspath(fname)
        if not os.path.exists(fname):
            create = messagebox.askyesno("File not found", f"'{fname}' not found. Create empty file?", parent=self)
            if not create:
                self._update_status("Open cancelled (file not found)")
                return
        try:
            if os.path.exists(fname):
                with open(fname, "r", encoding="utf-8") as f:
                    content = f.read()
            else:
                content = ""
            self.text.delete("1.0", tk.END)
            self.text.insert(tk.END, content)
            self.current_filename = fname
            self._text_modified = False
            self._update_status("Opened")
        except Exception as e:
            messagebox.showerror("Error opening file", str(e), parent=self)
            self._update_status("Open failed")

    def save_file(self):
        if not self.current_filename:
            fname = simpledialog.askstring("Save", "Enter file name to save as (relative or absolute):", parent=self)
            if not fname:
                self._update_status("Save cancelled")
                return False
            if not os.path.isabs(fname):
                fname = os.path.abspath(fname)
            self.current_filename = fname
        try:
            with open(self.current_filename, "w", encoding="utf-8") as f:
                f.write(self.text.get("1.0", tk.END))
            self._text_modified = False
            self._update_status("Saved")
            return True
        except Exception as e:
            messagebox.showerror("Error saving file", str(e), parent=self)
            self._update_status("Save failed")
            return False

    def exit_app(self):
        if not self._text_modified:
            if messagebox.askokcancel("Exit", "Are you sure you want to exit?", parent=self):
                self.destroy()
            else:
                self._update_status("Exit cancelled")
            return
        dlg = SaveBeforeCloseDialog(self, filename=self.current_filename)
        self.wait_window(dlg)
        if dlg.result == "save":
            if self.save_file():
                self.destroy()
            else:
                self._update_status("Exit cancelled (save failed)")
        elif dlg.result == "dont_save":
            self.destroy()
        else:
            self._update_status("Exit cancelled")

if __name__ == "__main__":
    app = TextEditorApp()
    app.mainloop()
