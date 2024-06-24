import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from cryptography.fernet import Fernet
import os


# إنشاء مفتاح تشفير
def generate_key(password):
    return Fernet.generate_key()


# تشفير البيانات باستخدام كلمة المرور
def encrypt(data, password):
    key = generate_key(password)
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data)
    return encrypted_data, key


# فك تشفير البيانات باستخدام كلمة المرور
def decrypt(encrypted_data, key):
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data)
    return decrypted_data


# تحميل الصورة وتشفيرها بكلمة مرور
def encrypt_image():
    password = password_entry.get()
    if not password:
        messagebox.showwarning("تحذير", "يرجى إدخال كلمة المرور")
        return

    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, "rb") as file:
            data = file.read()

        encrypted_data, key = encrypt(data, password.encode())

        encrypted_file_path = file_path + ".enc"
        with open(encrypted_file_path, "wb") as file:
            file.write(encrypted_data)

        with open(encrypted_file_path + ".key", "wb") as key_file:
            key_file.write(key)

        messagebox.showinfo("نجاح", f"تم تشفير الصورة وحفظها في {encrypted_file_path}")


# فك تشفير الصورة باستخدام كلمة المرور
def decrypt_image():
    password = password_entry.get()
    if not password:
        messagebox.showwarning("تحذير", "يرجى إدخال كلمة المرور")
        return

    file_path = filedialog.askopenfilename(filetypes=[("Encrypted Files", "*.enc")])
    key_file_path = file_path + ".key"

    if file_path and os.path.exists(key_file_path):
        with open(file_path, "rb") as file:
            encrypted_data = file.read()

        with open(key_file_path, "rb") as key_file:
            key = key_file.read()

        try:
            decrypted_data = decrypt(encrypted_data, key)
            decrypted_file_path = file_path[:-4]  # إزالة الامتداد '.enc'
            with open(decrypted_file_path, "wb") as file:
                file.write(decrypted_data)

            messagebox.showinfo(
                "نجاح", f"تم فك تشفير الصورة وحفظها في {decrypted_file_path}"
            )
        except Exception as e:
            messagebox.showerror("خطأ", "فشل فك تشفير الصورة. كلمة المرور غير صحيحة.")
    else:
        messagebox.showerror("خطأ", "لم يتم العثور على ملف المفتاح.")


# إنشاء واجهة المستخدم
root = tk.Tk()
root.title("تشفير وفك تشفير الصور")

password_label = tk.Label(root, text="كلمة المرور:")
password_label.pack(pady=5)

password_entry = tk.Entry(root, show="*", width=30)
password_entry.pack(pady=5)

encrypt_button = tk.Button(root, text="تشفير الصورة", command=encrypt_image)
encrypt_button.pack(pady=10)

decrypt_button = tk.Button(root, text="فك تشفير الصورة", command=decrypt_image)
decrypt_button.pack(pady=10)

root.mainloop()
