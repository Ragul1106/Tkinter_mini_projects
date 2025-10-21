from tkinter import Tk, Label, Listbox, Entry, Button, Scrollbar, END, messagebox

def add_contact():
    name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    email = email_entry.get().strip()

    if name == "" or phone == "" or email == "":
        messagebox.showwarning("Input Error", "Please fill all fields.")
    else:
        contact = f"{name} | {phone} | {email}"
        listbox.insert(END, contact)
        name_entry.delete(0, END)
        phone_entry.delete(0, END)
        email_entry.delete(0, END)

def remove_contact():
    try:
        selected_contact = listbox.curselection()[0]
        listbox.delete(selected_contact)
    except IndexError:
        messagebox.showwarning("Selection Error", "No contact selected.")

root = Tk()
root.title("📒 Contact Book")
root.geometry("400x400")
root.config(bg="#f5f7fa")

Label(root, text="Name:", font=("Poppins", 11), bg="#f5f7fa").pack(pady=(10,0))
name_entry = Entry(root, width=40, font=("Poppins", 10))
name_entry.pack(pady=5)

Label(root, text="Phone:", font=("Poppins", 11), bg="#f5f7fa").pack(pady=(10,0))
phone_entry = Entry(root, width=40, font=("Poppins", 10))
phone_entry.pack(pady=5)

Label(root, text="Email:", font=("Poppins", 11), bg="#f5f7fa").pack(pady=(10,0))
email_entry = Entry(root, width=40, font=("Poppins", 10))
email_entry.pack(pady=5)

add_button = Button(root, text="Add Contact", bg="#007bff", fg="white", font=("Poppins", 10, "bold"),
                    relief="flat", padx=10, pady=5, command=add_contact)
add_button.pack(pady=(10, 5))

remove_button = Button(root, text="Remove Contact", bg="#dc3545", fg="white", font=("Poppins", 10, "bold"),
                       relief="flat", padx=10, pady=5, command=remove_contact)
remove_button.pack(pady=(0, 10))

frame = Scrollbar(root)
listbox = Listbox(root, width=50, height=10, font=("Poppins", 10))
listbox.pack(pady=5)
scrollbar = Scrollbar(root, orient="vertical", command=listbox.yview)
scrollbar.pack(side="right", fill="y")
listbox.config(yscrollcommand=scrollbar.set)

root.mainloop()