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
TARGET_FOLDERS = ["Documents", "Images", "Software", "Archives", "Videos"]

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
    ".tar":"Archives",
    ".mp4":"Videos",
    ".mkv":"Videos"
}

def get_unique_path(dest_dir, filename):
    """
    如果目标文件已存在，返回一个自动重命名后的可用路径。
    例如：存在 1.pdf 则返回 1_1.pdf，再存在则 1_2.pdf，依此类推。
    """
    name, ext = os.path.splitext(filename)
    counter = 1
    dest_path = os.path.join(dest_dir, filename)
    while os.path.exists(dest_path):
        new_name = f"{name}_{counter}{ext}"
        dest_path = os.path.join(dest_dir, new_name)
        counter += 1
    return dest_path

def clean_downloads():
    '''这是程序的主引擎：执行清理逻辑'''

    # 计数器：记录今天搬了多少东西
    # moved_count = 0
    # 定义一个空列表
    moved_files = [] 
    print("清理程序启动...")

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

        # 排除特殊后缀的文件
        if extension.lower() == ".crdownload":
            continue
 
        # 3.匹配并搬运
        if extension in FILE_MAP:
            target_folder_name = FILE_MAP[extension]
            target_path = os.path.join(DOWNLOADS_DIR,target_folder_name)

            # ★ 关键修改：生成不冲突的目标路径
            dest_path = get_unique_path(target_path, filename)
            try:
                shutil.move(file_path,dest_path)
                info = f"{filename}->{target_folder_name}"
                moved_files.append(info)
                print(f"已移动：{info}")
            except Exception as e:
                print(f"移动{filename}时出错：{e}")
    
    # 4.生成日志报告
    write_log(moved_files)
    print(f"\n整理完成！详情请查看桌面日志")

def write_log(file_list):
    '''写日志助手升级：现在能写文件名字'''
    log_file = os.path.join(DESKTOP_DIR,"cleanup_log.txt")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    count = len(file_list)

    with open(log_file,"a",encoding="utf-8") as f:
        f.write(f"\n{'='* 30}\n")
        f.write(f"清理时间：{now}\n")
        f.write(f"统计数据：总共移动了{count}个文件\n")
        if count>0:
            f.write("详细清单：\n")
            for item in file_list:
                f.write(f" - {item}\n")
        f.write(f"{'='*30}\n")
if __name__ == "__main__":
    clean_downloads()
