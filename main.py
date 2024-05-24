import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter
from tkinter import PhotoImage, Label
from tkinter import Tk, Entry, Button, Checkbutton, StringVar, IntVar
from datetime import datetime

# Database functions
def create_table():
    try:
        conn = sqlite3.connect('sweetcorn.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS sweetcorn(
                       id TEXT PRIMARY KEY,
                       name TEXT,
                       in_stock INTEGER,
                       description TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS login_logs(
                       id INTEGER PRIMARY KEY,
                       username TEXT,
                       login_time TEXT,
                       logout_time TEXT)''')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror('Database Error', f'An error occurred: {e}')

def fetch_sweetcorn():
    conn = sqlite3.connect('sweetcorn.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sweetcorn')
    sweetcorn = cursor.fetchall()
    conn.close()
    return sweetcorn

def insert_sweetcorn(id, name, stock, description):
    try:
        conn = sqlite3.connect('sweetcorn.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO sweetcorn(id, name, in_stock, description) VALUES (?, ?, ?, ?)', (id, name, stock, description))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror('Database Error', f'An error occurred: {e}')

def delete_sweetcorn(id):
    try:
        conn = sqlite3.connect('sweetcorn.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM sweetcorn WHERE id = ?', (id,))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror('Database Error', f'An error occurred: {e}')

def update_sweetcorn(new_name, new_stock, description, id):
    try:
        conn = sqlite3.connect('sweetcorn.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE sweetcorn SET name = ?, in_stock = ?, description = ? WHERE id = ?', (new_name, new_stock, description, id))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror('Database Error', f'An error occurred: {e}')

def update_sweetcorn_id(old_id, new_id):
    if id_exist(new_id):
        messagebox.showerror('Error', 'New ID already exists')
        return
    try:
        conn = sqlite3.connect('sweetcorn.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE sweetcorn SET id = ? WHERE id = ?', (new_id, old_id))
        conn.commit()
        conn.close()
        messagebox.showinfo('Success', 'ID has been updated')
    except sqlite3.Error as e:
        messagebox.showerror('Database Error', f'An error occurred: {e}')

def id_exist(id):
    try:
        conn = sqlite3.connect('sweetcorn.db')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM sweetcorn WHERE id = ?', (id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] > 0
    except sqlite3.Error as e:
        messagebox.showerror('Database Error', f'An error occurred: {e}')
        return False

def insert_login_log(username, login_time):
    conn = sqlite3.connect('sweetcorn.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO login_logs(username, login_time) VALUES (?, ?)', (username, login_time))
    conn.commit()
    conn.close()

def insert_logout_log(username, logout_time):
    conn = sqlite3.connect('sweetcorn.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE login_logs SET logout_time = ? WHERE username = ? AND logout_time IS NULL", (logout_time, username))
    conn.commit()
    conn.close()

def delete_user_by_id(user_id):
    conn = sqlite3.connect('sweetcorn.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM login_logs WHERE id=?", (user_id,))
    user = cursor.fetchone()
    if user:
        cursor.execute("DELETE FROM login_logs WHERE id=?", (user_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo(title="Deletion Success", message=f"User with ID {user_id} deleted successfully.")
    else:
        conn.close()
        messagebox.showerror(title="Error", message=f"User with ID {user_id} does not exist.")

def open_delete_user_window():
    global delete_user_window
    delete_user_window = Tk()
    delete_user_window.title("Delete User")
    delete_user_window.geometry("300x150+700+250")
    delete_user_window.resizable(50, 50)

    # Label and Entry for user input
    id_label = Label(delete_user_window, text="User ID:")
    id_label.grid(row=0, column=0, padx=15, pady=15)
    id_entry = Entry(delete_user_window)
    id_entry.grid(row=0, column=1, padx=15, pady=15)

    # Function to delete the user
    def delete_user():
        user_id = id_entry.get()
        if user_id:
            delete_user_by_id(int(user_id))
            delete_user_window.destroy()
        else:
            messagebox.showerror("Error", "Please enter a valid user ID.")

    # Button to confirm deletion
    delete_button = Button(delete_user_window, text="Delete", command=delete_user)
    delete_button.grid(row=1, column=0, columnspan=2, padx=15, pady=15)

    delete_user_window.mainloop()

# GUI functions
def create_chart():
    sweetcorn_details = fetch_sweetcorn()
    sweetcorn_name = [sweetcorn[1] for sweetcorn in sweetcorn_details]
    stock_values = [sweetcorn[2] for sweetcorn in sweetcorn_details]

    figure = Figure(figsize=(10, 3.8), dpi=80, facecolor='green')
    ax = figure.add_subplot(111)
    ax.bar(sweetcorn_name, stock_values, width=0.4, color='pink')
    ax.set_xlabel("Sweetcorn Name", color='#fff', fontsize=10)
    ax.set_ylabel("Stock value", color='#fff', fontsize=10)
    ax.set_title("Sweetcorn Stock Levels", color='#fff', fontsize=12)
    ax.tick_params(axis='y', labelcolor='#fff', labelsize=12)
    ax.tick_params(axis='x', labelcolor='#fff', labelsize=12)
    ax.set_facecolor("#1B181B")

    canvas = FigureCanvasTkAgg(figure, root)
    canvas.get_tk_widget().place(x=15, y=500, width=970, height=250)

def add_to_treeview():
    for i in tree.get_children():
        tree.delete(i)
    sweetcorn = fetch_sweetcorn()
    for corn in sweetcorn:
        tree.insert('', tk.END, values=corn)

def clear():
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    stock_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)

def insert():
    id = id_entry.get()
    name = name_entry.get()
    stock = stock_entry.get()
    description = description_entry.get()
    if not (id and name and stock and description):
        messagebox.showerror('Error', 'Enter all fields')
    elif id_exist(id):
        messagebox.showerror('Error', 'ID already exists')
    else:
        try:
            stock_value = int(stock)
            insert_sweetcorn(id, name, stock_value, description)
            add_to_treeview()
            clear()
            create_chart()
            messagebox.showinfo('Success', 'Data has been inserted')
        except ValueError:
            messagebox.showerror('Error', 'Stock should be an integer')
        except sqlite3.Error as e:
            messagebox.showerror('Database Error', f'An error occurred: {e}')
        except Exception as e:
            messagebox.showerror('Error', f'An unexpected error occurred: {e}')

def update():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror('Error', 'Choose a product to update')
    else:
        old_id = tree.item(selected_item)['values'][0]
        new_id = id_entry.get()
        name = name_entry.get()
        stock = stock_entry.get()
        description = description_entry.get()
        
        if not (new_id and name and stock and description):
            messagebox.showerror('Error', 'Enter all fields')
        elif new_id != old_id and id_exist(new_id):
            messagebox.showerror('Error', 'New ID already exists')
        else:
            try:
                stock_value = int(stock)
                if new_id != old_id:
                    update_sweetcorn_id(old_id, new_id)
                update_sweetcorn(name, stock_value, description, new_id)
                add_to_treeview()
                clear()
                create_chart()
                messagebox.showinfo('Success', 'Data has been updated')
            except ValueError:
                messagebox.showerror('Error', 'Stock should be an integer')
            except sqlite3.Error as e:
                messagebox.showerror('Database Error', f'An error occurred: {e}')

def delete():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror('Error', 'Choose a product to delete')
    else:
        id = tree.item(selected_item)['values'][0]
        delete_sweetcorn(id)
        add_to_treeview()
        clear()
        create_chart()
        messagebox.showinfo('Success', 'Data has been deleted')

# GUI Setup
root = customtkinter.CTk()
root.geometry("1000x780+300+0")
root.configure(bg="#1B181B")
root.resizable(50, 50)

tree = ttk.Treeview(root, column=("c1", "c2", "c3", "c4"), show='headings', height=10)
tree.column("#1", anchor=tk.CENTER)
tree.heading("#1", text="ID")
tree.column("#2", anchor=tk.CENTER)
tree.heading("#2", text="Name")
tree.column("#3", anchor=tk.CENTER)
tree.heading("#3", text="Stock")
tree.column("#4", anchor=tk.CENTER)
tree.heading("#4", text="Description")
tree.pack(pady=20)

frame = customtkinter.CTkFrame(root, width=900, height=300, fg_color="pink")
frame.pack(side="top", padx=10, pady=10)

id_label = customtkinter.CTkLabel(frame, text="ID", fg_color="white", text_color="black")
id_label.place(x=30, y=10)
id_entry = customtkinter.CTkEntry(frame, width=200, fg_color="white", text_color="black")
id_entry.place(x=150, y=10)

name_label = customtkinter.CTkLabel(frame, text="Name", fg_color="white", text_color="black")
name_label.place(x=30, y=60)
name_entry = customtkinter.CTkEntry(frame, width=200, fg_color="white", text_color="black")
name_entry.place(x=150, y=60)

stock_label = customtkinter.CTkLabel(frame, text="Stock", fg_color="white", text_color="black")
stock_label.place(x=30, y=110)
stock_entry = customtkinter.CTkEntry(frame, width=200, fg_color="white", text_color="black")
stock_entry.place(x=150, y=110)

description_label = customtkinter.CTkLabel(frame, text="Description", fg_color="white", text_color="black")
description_label.place(x=30, y=160)
description_entry = customtkinter.CTkEntry(frame, width=200, fg_color="white", text_color="black")
description_entry.place(x=150, y=160)

insert_button = customtkinter.CTkButton(frame, text="Insert", command=insert, fg_color="white", text_color="black")
insert_button.place(x=400, y=50)

update_button = customtkinter.CTkButton(frame, text="Update", command=update, fg_color="white", text_color="black")
update_button.place(x=400, y=100)

delete_button = customtkinter.CTkButton(frame, text="Delete", command=delete, fg_color="white", text_color="black")
delete_button.place(x=400, y=150)

create_table()
add_to_treeview()
create_chart()
root.mainloop()
