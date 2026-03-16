import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os

FILE = "contacts.json"

# Load contacts
if os.path.exists(FILE):
    with open(FILE, "r") as f:
        contacts = json.load(f)
else:
    contacts = {}

selected_contact = None
photo_path = ""

# ---------------- WINDOW ----------------

root = tk.Tk()
root.title("Advanced Contact Book")
root.geometry("450x600")
root.configure(bg="#eaf4ff")

# ---------------- SAVE ----------------

def save_contacts():
    with open(FILE, "w") as f:
        json.dump(contacts, f)

# ---------------- ADD ----------------

def add_contact():
    name = name_entry.get().strip()
    phone = phone_entry.get().strip()

    if name == "" or phone == "":
        messagebox.showwarning("Warning","Enter name and phone")
        return

    contacts[name] = {"phone": phone, "photo": photo_path}
    save_contacts()

    name_entry.delete(0,tk.END)
    phone_entry.delete(0,tk.END)

    messagebox.showinfo("Success","Contact Added")

# ---------------- SHOW ----------------

def show_contacts():
    listbox.delete(0,tk.END)

    for name,data in contacts.items():
        listbox.insert(tk.END,f"{name} | {data['phone']}")

# ---------------- SELECT ----------------

def fill_from_list(event):
    global selected_contact

    if not listbox.curselection():
        return

    index = listbox.curselection()[0]
    data = listbox.get(index)

    name, phone = data.split(" | ")

    selected_contact = name

    name_entry.delete(0,tk.END)
    name_entry.insert(0,name)

    phone_entry.delete(0,tk.END)
    phone_entry.insert(0,phone)

# ---------------- EDIT ----------------

def edit_contact():
    global selected_contact

    if selected_contact is None:
        messagebox.showwarning("Warning","Select contact")
        return

    new_name = name_entry.get().strip()
    new_phone = phone_entry.get().strip()

    if new_name == "" or new_phone == "":
        messagebox.showwarning("Warning","Enter name and phone")
        return

    contacts[new_name] = {"phone": new_phone, "photo": photo_path}

    if new_name != selected_contact:
        del contacts[selected_contact]

    selected_contact = None

    save_contacts()
    show_contacts()

    messagebox.showinfo("Updated","Contact Updated")

# ---------------- DELETE ----------------

def delete_contact():
    global selected_contact

    if selected_contact is None:
        messagebox.showwarning("Warning","Select contact")
        return

    del contacts[selected_contact]

    selected_contact = None

    save_contacts()
    show_contacts()

    name_entry.delete(0,tk.END)
    phone_entry.delete(0,tk.END)

    messagebox.showinfo("Deleted","Contact Deleted")

# ---------------- SEARCH ----------------

def search_contact():
    name = name_entry.get().strip().lower()

    listbox.delete(0,tk.END)

    for contact,data in contacts.items():
        if name in contact.lower():
            listbox.insert(tk.END,f"{contact} | {data['phone']}")

# ---------------- PHOTO ----------------

def upload_photo():
    global photo_path

    path = filedialog.askopenfilename(
        filetypes=[("Image files","*.png *.jpg *.jpeg")]
    )

    if path:
        photo_path = path
        photo_label.config(text="Photo Selected")

# ---------------- PROFILE ICON ----------------

canvas = tk.Canvas(root,width=90,height=90,bg="#eaf4ff",highlightthickness=0)
canvas.pack(pady=10)

canvas.create_oval(10,10,80,80,fill="#4da6ff")
canvas.create_text(45,45,text="👤",font=("Arial",30))

# ---------------- TITLE ----------------

title = tk.Label(
root,
text="Advanced Contact Book",
font=("Segoe UI",18,"bold"),
bg="#eaf4ff"
)
title.pack()

# ---------------- INPUT ----------------

tk.Label(root,text="Name",bg="#eaf4ff").pack()

name_entry = tk.Entry(root,width=30)
name_entry.pack(pady=5)

tk.Label(root,text="Phone Number",bg="#eaf4ff").pack()

phone_entry = tk.Entry(root,width=30)
phone_entry.pack(pady=5)

# ---------------- PHOTO ----------------

tk.Button(root,text="Upload Photo",command=upload_photo).pack(pady=5)

photo_label = tk.Label(root,text="",bg="#eaf4ff")
photo_label.pack()

# ---------------- BUTTONS ----------------

btn_frame = tk.Frame(root,bg="#eaf4ff")
btn_frame.pack(pady=10)

tk.Button(btn_frame,text="Add",width=10,bg="#4CAF50",fg="white",command=add_contact).grid(row=0,column=0,padx=5)

tk.Button(btn_frame,text="Edit",width=10,bg="#ffa500",fg="white",command=edit_contact).grid(row=0,column=1,padx=5)

tk.Button(btn_frame,text="Delete",width=10,bg="#f44336",fg="white",command=delete_contact).grid(row=0,column=2,padx=5)

tk.Button(btn_frame,text="Search",width=10,bg="#2196F3",fg="white",command=search_contact).grid(row=1,column=0,pady=5)

tk.Button(btn_frame,text="Show All",width=10,bg="#555",fg="white",command=show_contacts).grid(row=1,column=1,pady=5)

# ---------------- LIST ----------------

listbox = tk.Listbox(root,width=45,height=12)
listbox.pack(pady=15)

listbox.bind("<<ListboxSelect>>", fill_from_list)

# ---------------- FOOTER ----------------

footer = tk.Label(
root,
text="Developed by Roshni Tirkey",
bg="#eaf4ff"
)

footer.pack(pady=10)

root.mainloop()