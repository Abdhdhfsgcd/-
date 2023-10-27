import tkinter as tk
import platform
import psutil

def get_system_info():
    system = platform.system()
    node = platform.node()
    release = platform.release()
    processor = platform.processor()
    memory = psutil.virtual_memory().total // (1024**3)  # في غيغابايت

    return f"نظام التشغيل: {system}\nاسم الجهاز: {node}\nإصدار النظام: {release}\nالمعالج: {processor}\nالذاكرة: {memory} GB"

root = tk.Tk()
root.title("تطبيق معلومات الحاسوب")

info_label = tk.Label(root, text=get_system_info(), justify="left", font=("Arial", 14))
info_label.pack(padx=20, pady=20)

root.mainloop()