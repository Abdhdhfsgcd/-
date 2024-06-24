import platform  # مكتبة للحصول على معلومات عن نظام التشغيل
import psutil  # مكتبة لمعرفة معلومات عن النظام والأداء
import socket  # مكتبة للتعامل مع الشبكات


def get_system_info():
    info = {}

    # معلومات نظام التشغيل
    info["System"] = platform.system()
    info["Node Name"] = platform.node()
    info["Release"] = platform.release()
    info["Version"] = platform.version()
    info["Machine"] = platform.machine()
    info["Processor"] = platform.processor()

    # معلومات المعالج
    info["CPU Cores"] = psutil.cpu_count(logical=False)
    info["Logical Processors"] = psutil.cpu_count(logical=True)
    info["CPU Frequency"] = f"{psutil.cpu_freq().current:.2f} Mhz"
    info["CPU Usage"] = f"{psutil.cpu_percent(interval=1)}%"

    # معلومات الذاكرة
    virtual_mem = psutil.virtual_memory()
    info["Total Memory"] = f"{virtual_mem.total / (1024 ** 3):.2f} GB"
    info["Available Memory"] = f"{virtual_mem.available / (1024 ** 3):.2f} GB"
    info["Used Memory"] = f"{virtual_mem.used / (1024 ** 3):.2f} GB"
    info["Memory Usage"] = f"{virtual_mem.percent}%"

    # معلومات القرص الصلب
    disk_usage = psutil.disk_usage("/")
    info["Total Disk"] = f"{disk_usage.total / (1024 ** 3):.2f} GB"
    info["Used Disk"] = f"{disk_usage.used / (1024 ** 3):.2f} GB"
    info["Free Disk"] = f"{disk_usage.free / (1024 ** 3):.2f} GB"
    info["Disk Usage"] = f"{disk_usage.percent}%"

    # معلومات الشبكة
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    info["Hostname"] = hostname
    info["Local IP"] = local_ip

    return info


def display_system_info(info):
    for key, value in info.items():
        print(f"{key}: {value}")


def main():
    system_info = get_system_info()  # الحصول على معلومات النظام
    display_system_info(system_info)  # عرض معلومات النظام


if __name__ == "__main__":
    main()
