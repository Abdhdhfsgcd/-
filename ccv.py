import psutil  # مكتبة لمعرفة معلومات عن النظام والأداء
import subprocess  # مكتبة لتنفيذ أوامر النظام
import winapps  # مكتبة لفحص البرامج المثبتة في النظام


# وظيفة لفحص موارد النظام (المعالج والذاكرة) وتقديم توصيات
def check_system_resources():
    cpu_usage = psutil.cpu_percent(interval=1)  # الحصول على نسبة استخدام المعالج
    memory_info = psutil.virtual_memory()  # الحصول على معلومات الذاكرة

    issues = []  # قائمة لتخزين المشاكل المكتشفة

    # التحقق من نسبة استخدام المعالج
    if cpu_usage > 80:
        issues.append(f"High CPU usage detected: {cpu_usage}%")
        issues.append("Recommendation: Close unnecessary programs.")
    # التحقق من نسبة استخدام الذاكرة
    if memory_info.percent > 80:
        issues.append(f"High Memory usage detected: {memory_info.percent}%")
        issues.append("Recommendation: Close unnecessary programs or upgrade your RAM.")

    # إذا لم تكن هناك مشاكل، العودة برسالة تدل على ذلك
    if not issues:
        return "System resources are within normal limits."

    # العودة بالمشاكل المكتشفة إذا وجدت
    return "\n".join(issues)


# وظيفة للتحقق من سلامة ملفات النظام باستخدام أمر sfc /scannow ومحاولة الإصلاح
def check_system_files():
    result = subprocess.run(
        ["sfc", "/scannow"], capture_output=True, text=True
    )  # تنفيذ الأمر والانتظار حتى ينتهي
    # التحقق من نتيجة الفحص
    if (
        "Windows Resource Protection did not find any integrity violations"
        in result.stdout
    ):
        return "System files are intact."
    elif (
        "Windows Resource Protection found corrupt files and successfully repaired them"
        in result.stdout
    ):
        return "Issues detected and repaired in system files."
    else:
        return "Issues detected in system files. Manual intervention might be required."


# وظيفة لفحص البرامج المثبتة في النظام وتقديم توصيات
def check_installed_programs():
    installed_programs = list(
        winapps.list_installed()
    )  # الحصول على قائمة بالبرامج المثبتة
    program_names = [
        program.name for program in installed_programs
    ]  # استخراج أسماء البرامج فقط
    recommendations = []

    # تقديم توصيات بناءً على البرامج المثبتة
    for program in installed_programs:
        if "old_version" in program.name.lower():
            recommendations.append(f"Recommendation: Consider updating {program.name}.")

    return "\n".join(program_names) + "\n\n" + "\n".join(recommendations)


# الدالة الرئيسية لتنفيذ الفحص الكامل وتقديم الحلول
def main():
    print("Checking system resources...")
    resource_issues = check_system_resources()  # فحص موارد النظام
    print(resource_issues)

    print("\nChecking system files integrity...")
    file_issues = check_system_files()  # التحقق من سلامة ملفات النظام
    print(file_issues)

    print("\nListing installed programs...")
    installed_programs = check_installed_programs()  # فحص البرامج المثبتة
    print("\n".join(installed_programs))


# التأكد من أن السكربت ينفذ كبرنامج رئيسي
if __name__ == "__main__":
    main()
