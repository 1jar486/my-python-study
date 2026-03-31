import os 
import shutil
from datetime import datetime

# 用来清理下载的哪些文件
# 将文件分类放在文件夹（Documents,images,Software,Archives）里

# 自动获取当前电脑的用户主目录(比如：c:\Users\YourName)
# 这样这个代码能够在任何人的电脑上都能运行
home_path = os.path.expanduser("~")

# 定义下载文件夹和桌面的路径
DOWNLOADS_DIR = os.path.join(home_path, "Downloads")
DESKTOP_DIR = os.path.join(home_path, "Desktop")

# 定义我们要创建的分类文件夹名称
TARGET_FOLDERS = ["Documents", "Images", "Software", "Archives"]

# 定义文件分拣规则：后缀名 -> 目标文件夹
FILE_MAP = {
    ".pdf":"Documents",
    ".docx":"Documents",
    ".txt":"Documents",
    ".xlsx":"Documents",
    ".jpg":"Images",
    ".png":"Images",
    ".jpeg":"Images",
    ".gif":"Images",
    ".exe":"Software",
    ".msi":"Software",
    ".dmg":"Software",
    ".zip":"Archives",
    ".rar":"Archives",
    ".7z":"Archives",
    ".tar":"Archives"
}

def clean_downloads():
    '''这是程序的主引擎：执行清理逻辑'''

    # 计数器：记录今天搬了多少东西
    moved_count = 0
    print("清理重新启动...")

    # 1.确保目标文件夹都在
    for folder in TARGET_FOLDERS:
        full_path = os.path.join(DOWNLOADS_DIR, folder)
        if not os.path.exists(full_path):
            os.makedirs(full_path)
            print(f"已创建分类文件夹：{folder}")
    
    # 2.开始分拣文件
    # os.listdir 会列出下载文件夹里所有的东西
    for filename in os.listdir(DOWNLOADS_DIR):
        file_path = os.path.join(DOWNLOADS_DIR, filename)
        # 排除文件夹
        if os.path.isdir(file_path):
            continue
    # 获取后缀名(例如'.pdf'), 并转为小写，防止出错
    _,extension = os.path.splitext(filename)
    extension = extension.lower()

    # 3.匹配并搬运
    if extension in FILE_MAP:
        target_folder_name = FILE_MAP[extension]
        target_path = os.path.join(DOWNLOADS_DIR,target_folder_name,filename)
    try:
        shutil.move(file_path,target_path)
        moved_count += 1
        print(f"已移动：{filename}->{target_folder_name}")
    except Exception as e:
        print(f"移动{filename}时出错：{e}")
    
    # 4.生成日志报告
    write_log(moved_count)
    print(f"\n整理完成！共整理了{moved_count}个文件。报告已生成在桌面。")

def write_log(count):
    '''写日志的小助手'''
    log_file = os.path.join(DESKTOP_DIR,"Cleanup_log.txt")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_file,"a",encoding="utf-8") as f:
        f.write(f"[{now}] 整理成功：移动了{count}个文件\n")
if __name__ == "__main__":
    clean_downloads()

    



