import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import sqlite3
import os

DB_PATH = "tasks.db"

class TaskDB:
    def __init__(self, path=DB_PATH):
        self.path = path
        self.conn = sqlite3.connect(self.path)
        self._create_table()

    def _create_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending'
        )
        """
        self.conn.execute(sql)
        self.conn.commit()

    def add_task(self, task_text):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO tasks (task, status) VALUES (?, ?)", (task_text, "pending"))
        self.conn.commit()
        return cur.lastrowid

    def update_task(self, task_id, new_text):
        self.conn.execute("UPDATE tasks SET task = ? WHERE id = ?", (new_text, task_id))
        self.conn.commit()

    def delete_task(self, task_id):
        self.conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()

    def toggle_status(self, task_id):
        cur = self.conn.cursor()
        cur.execute("SELECT status FROM tasks WHERE id = ?", (task_id,))
        row = cur.fetchone()
        if not row:
            return
        new_status = "done" if row[0] == "pending" else "pending"
        cur.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
        self.conn.commit()

    def get_all(self):
        cur = self.conn.cursor()
        cur.execute("SELECT id, task, status FROM tasks ORDER BY id DESC")
        return cur.fetchall()

    def close(self):
        self.conn.close()

class TodoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SQLite Todo App")
        self.geometry("600x420")
        self.resizable(False, False)
        self.db = TaskDB()
        self._create_widgets()
        self._layout_widgets()
        self._bind_events()
        self.load_tasks()

    def _create_widgets(self):
        self.top_frame = ttk.Frame(self, padding=8)
        self.task_var = tk.StringVar()
        self.entry = ttk.Entry(self.top_frame, textvariable=self.task_var, width=50)
        self.add_btn = ttk.Button(self.top_frame, text="Add Task", command=self.add_task)
        self.middle_frame = ttk.Frame(self, padding=(8,0))
        self.listbox = tk.Listbox(self.middle_frame, height=15, activestyle="none")
        self.scrollbar = ttk.Scrollbar(self.middle_frame, orient="vertical", command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.btn_frame = ttk.Frame(self.middle_frame, padding=(8,0))
        self.update_btn = ttk.Button(self.btn_frame, text="Edit Selected", command=self.edit_selected)
        self.delete_btn = ttk.Button(self.btn_frame, text="Delete Selected", command=self.delete_selected)
        self.toggle_btn = ttk.Button(self.btn_frame, text="Toggle Done/Undone", command=self.toggle_selected)
        self.export_btn = ttk.Button(self.btn_frame, text="Export to .txt", command=self.export_tasks)
        self.refresh_btn = ttk.Button(self.btn_frame, text="Refresh", command=self.load_tasks)
        self.status_var = tk.StringVar(value="Ready")
        self.status = ttk.Label(self, textvariable=self.status_var, relief="sunken", anchor="w", padding=4)

    def _layout_widgets(self):
        self.top_frame.pack(fill="x")
        self.entry.pack(side="left", padx=(0,8))
        self.add_btn.pack(side="left")
        self.middle_frame.pack(fill="both", expand=True, padx=8, pady=(6,0))
        self.listbox.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="left", fill="y")
        self.btn_frame.pack(side="left", fill="y", padx=12)
        for w in (self.update_btn, self.delete_btn, self.toggle_btn, self.export_btn, self.refresh_btn):
            w.pack(fill="x", pady=4)
        self.status.pack(side="bottom", fill="x")

    def _bind_events(self):
        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        self.listbox.bind("<Double-Button-1>", self.on_double_click)
        self.bind("<Return>", lambda e: self.add_task())
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def load_tasks(self):
        self.listbox.delete(0, tk.END)
        rows = self.db.get_all()
        for row in rows:
            tid, text, status = row
            display = f"[{'✓' if status=='done' else ' '}] {text} (id:{tid})"
            self.listbox.insert(tk.END, display)
        self._current_rows = rows
        self.status_var.set(f"Loaded {len(rows)} tasks")

    def add_task(self):
        text = self.task_var.get().strip()
        if not text:
            messagebox.showwarning("Input required", "Please enter a task.", parent=self)
            return
        self.db.add_task(text)
        self.task_var.set("")
        self.load_tasks()

    def get_selected_task(self):
        sel = self.listbox.curselection()
        if not sel:
            return None
        idx = sel[0]
        try:
            tid, text, status = self._current_rows[idx]
            return {"id": tid, "task": text, "status": status, "index": idx}
        except Exception:
            return None

    def edit_selected(self):
        sel = self.get_selected_task()
        if not sel:
            messagebox.showinfo("No selection", "Please select a task to edit.", parent=self)
            return
        new_text = simpledialog.askstring("Edit Task", "Edit task text:", initialvalue=sel["task"], parent=self)
        if new_text is None:
            return
        new_text = new_text.strip()
        if not new_text:
            messagebox.showwarning("Invalid", "Task cannot be empty.", parent=self)
            return
        self.db.update_task(sel["id"], new_text)
        self.load_tasks()

    def delete_selected(self):
        sel = self.get_selected_task()
        if not sel:
            messagebox.showinfo("No selection", "Please select a task to delete.", parent=self)
            return
        ok = messagebox.askyesno("Confirm delete", f"Delete task:\n\n{sel['task']}\n\nThis action cannot be undone.", parent=self)
        if not ok:
            return
        self.db.delete_task(sel["id"])
        self.load_tasks()

    def toggle_selected(self):
        sel = self.get_selected_task()
        if not sel:
            messagebox.showinfo("No selection", "Please select a task to toggle.", parent=self)
            return
        self.db.toggle_status(sel["id"])
        self.load_tasks()

    def export_tasks(self):
        default_name = "tasks.txt"
        path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=default_name,
                                            filetypes=[("Text files","*.txt"),("All files","*.*")],
                                            title="Export tasks to...")
        if not path:
            self.status_var.set("Export cancelled")
            return
        try:
            rows = self.db.get_all()
            with open(path, "w", encoding="utf-8") as f:
                for tid, text, status in rows:
                    f.write(f"{'[DONE]' if status=='done' else '[PENDING]'} {text} (id:{tid})\n")
            self.status_var.set(f"Exported {len(rows)} tasks to {os.path.basename(path)}")
            messagebox.showinfo("Exported", f"Tasks exported to:\n{path}", parent=self)
        except Exception as e:
            messagebox.showerror("Export failed", str(e), parent=self)

    def on_select(self, event=None):
        sel = self.get_selected_task()
        if sel:
            self.task_var.set(sel["task"])
            self.status_var.set(f"Selected id:{sel['id']} — {sel['status']}")
        else:
            self.status_var.set("Ready")

    def on_double_click(self, event=None):
        self.toggle_selected()

    def on_close(self):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?", parent=self):
            self.db.close()
            self.destroy()

if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
