import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt

# إنشاء واجهة التطبيق
root = tk.Tk()
root.title("برنامج تحليل البيانات")

def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            df = pd.read_csv(file_path)
            analyze_data(df)
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في تحميل الملف: {e}")

def analyze_data(df):
    if 'value' not in df.columns:
        messagebox.showerror("خطأ", "الملف يجب أن يحتوي على عمود 'value'")
        return
    
    # عرض البيانات
    plt.figure(figsize=(10, 5))
    plt.plot(df['value'])
    plt.title('تحليل البيانات')
    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.show()

# زر لتحميل الملف
load_button = tk.Button(root, text="تحميل ملف CSV", command=load_file)
load_button.pack(pady=20)

root.mainloop()