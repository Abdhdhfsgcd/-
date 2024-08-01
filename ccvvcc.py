import tkinter as tk
from tkinter import messagebox
import sqlite3

# إنشاء أو الاتصال بقاعدة البيانات
conn = sqlite3.connect("employees.db")
c = conn.cursor()

# إنشاء جدول الموظفين إذا لم يكن موجودًا بالفعل
c.execute(
    """
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
"""
)
conn.commit()


# دالة لإضافة موظف جديد
def add_employee():
    name = entry_name.get()
    if name:
        c.execute("INSERT INTO employees (name) VALUES (?)", (name,))
        conn.commit()
        entry_name.delete(0, tk.END)
        messagebox.showinfo("Success", "Employee added successfully")
        view_employees()
    else:
        messagebox.showwarning("Warning", "Please enter a name")


# دالة لتحديث اسم الموظف
def update_employee():
    selected_item = listbox.curselection()
    if selected_item:
        emp_id = listbox.get(selected_item).split(",")[0].split(":")[1].strip()
        new_name = entry_name.get()
        if new_name:
            c.execute("UPDATE employees SET name = ? WHERE id = ?", (new_name, emp_id))
            conn.commit()
            entry_name.delete(0, tk.END)
            messagebox.showinfo("Success", "Employee updated successfully")
            view_employees()
        else:
            messagebox.showwarning("Warning", "Please enter a name")
    else:
        messagebox.showwarning("Warning", "Please select an employee to update")


# دالة لحذف موظف
def delete_employee():
    selected_item = listbox.curselection()
    if selected_item:
        emp_id = listbox.get(selected_item).split(",")[0].split(":")[1].strip()
        c.execute("DELETE FROM employees WHERE id = ?", (emp_id,))
        conn.commit()
        messagebox.showinfo("Success", "Employee deleted successfully")
        view_employees()
    else:
        messagebox.showwarning("Warning", "Please select an employee to delete")


# دالة لعرض جميع الموظفين
def view_employees():
    listbox.delete(0, tk.END)
    c.execute("SELECT * FROM employees")
    rows = c.fetchall()
    for row in rows:
        listbox.insert(tk.END, f"ID: {row[0]}, Name: {row[1]}")


# دالة لتحديد الموظف لعرضه في حقل الإدخال
def select_employee(event):
    selected_item = listbox.curselection()
    if selected_item:
        emp_name = listbox.get(selected_item).split(",")[1].split(":")[1].strip()
        entry_name.delete(0, tk.END)
        entry_name.insert(tk.END, emp_name)


# إنشاء واجهة المستخدم
root = tk.Tk()
root.title("Employee Management System")

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Employee Name:").grid(row=0, column=0)

entry_name = tk.Entry(frame)
entry_name.grid(row=0, column=1)

tk.Button(frame, text="Add Employee", command=add_employee).grid(
    row=1, column=0, pady=5
)
tk.Button(frame, text="Update Employee", command=update_employee).grid(
    row=1, column=1, pady=5
)
tk.Button(frame, text="Delete Employee", command=delete_employee).grid(
    row=1, column=2, pady=5
)

listbox = tk.Listbox(root, width=50)
listbox.pack(pady=10)
listbox.bind("<<ListboxSelect>>", select_employee)

view_employees()

# تشغيل واجهة المستخدم
root.mainloop()

# إغلاق الاتصال بقاعدة البيانات عند إغلاق البرنامج
conn.close()
