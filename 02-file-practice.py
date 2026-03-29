import os
import shutil
import sqlite3
from datetime import datetime

# 数据库功能函数
def init_db(): # 初始化数据库
    # 1.连接数据库。
    # 如果当前文件夹下没有'file_history.db'这个数据库文件，就会自动创建一个新的数据库文件。
    conn = sqlite3.connect('file_history.db') # conn 打开笔记的手
    
    # 2.创建游标
    cursor = conn.cursor() # 创建一个游标对象cursor，所有写字打字的操作都靠它

    # 3.编写SQL指令(SQL是专门跟数据库沟通的语言)
    # 下面代码的意思是，如果不存在一个名为 move_logs 的表，就创建一个新的表

    # id:自动增长的数字，给每一行一个唯一的编号。
    # file_name:文本类型，记录文件的名字。
    # source_path:文本类型，记录文件原来的位置。
    # dest_path:文本类型，记录文件搬到哪里了。
    # move_time:文本类型，记录文件搬家的时间。
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS move_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                        file_name TEXT, 
                        source_path TEXT,
                        dest_path TEXT,
                        move_time TEXT
                    )
                   ''') 
    # 4.提交保存
    conn.commit()
    return conn 

# 这个函数的作用是：往表格里填入一条具体的搬家记录
# 参数说明：文件名，从哪搬，搬到哪
def log_move(file_name, source, dest): 
    # 再次建立连接(每次操作数据库前都要握手)
    conn = sqlite3.connect('file_history.db') 
    cursor = conn.cursor() 

    # 5.获取当前系统时间，并转成我们看得懂的格式：年-月-日 时:分:秒
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 6.执行插入指令
    # 注意这里用了？占位符，这里是为了安全
    cursor.execute('''
                   INSERT INTO move_logs (file_name, source_path, dest_path, move_time)
                   VALUES (?, ?, ?, ?)
                   ''', (file_name, source, dest, now)) 
                    # 后面的元组(file_name, source, dest, now)会按照顺序填入到？的位置
    # 7.确认提交
    conn.commit()

    # 8.关闭连接
    conn.close()

    print(f"已记录到数据库：{file_name}")


# path = r'C:\Users\Administrator\Desktop\自动整理测试' # 需要操作的文件夹的绝对地址
# os.listdir()方法会返回一个列表，里面是这个文件夹里面的所有文件和文件夹的名字（不包含路径）

# rules = {
#     '.jpg': '图片素材',
#     '.png': '图片素材',
#     '.txt': '文档资料',
#     '.mp4': '视频剪辑',
    
# 识别文件及文件夹并打印
# for file in os.listdir(path): 
#     print(file)

# 主逻辑开始
def main():
    init_db() # 初始化数据库
    current_path = os.path.dirname(os.path.realpath(__file__)) # 获取当前路径，让脚本自动识别自己在哪个文件路径
    print(f"我现在的办公地点是：{current_path}")
    files = os.listdir(current_path)
    
    WHITE_LIST_EXTS = ['.JPG','.PNG','.PDF','.DOCX','.MD','.MP4','.ZIP']
    
    for file in os.listdir(current_path): # 扫描这个文件路径下的所有文件
        full_path = os.path.join(current_path, file)
        # os.path.isfile(file) 判断这个东西是不是文件
        # file != os.path.basename(__file__) 判断这个东西是不是脚本本身
        
        if not os.path.isfile(full_path):
            print(f"跳过文件夹":{file})
            continue
        
       # 1. if or file.startswith('.') 排除系统隐藏文件
        if file.upper() in ["NTUSER.DAT", "INDEX.DAT"] or file.startswith('.'):
            print(f"👻 跳过隐藏/系统文件: {file}")
            continue
        
        name, ext = os.path.splitext(file)
        ext_upper = ext.upper() # 获取文件后缀名大写

        if ext_upper not in WHITE_LIST_EXTS:
            print(f"跳过非目标文件")
            continue
        
        # 把后缀名的点去掉([1:])，并转成大写(upper())，作为文件夹的名字
        folder_name = ext[1:].upper() 
         # 双重拼接，先把文件夹路径和文件夹名字粘合成完整路径，再把这个路径和文件名粘合成新文件的完整路径
        target_folder = os.path.join(current_path, folder_name) # 新文件路径，放在以文件后缀名命名的文件夹里

        if not os.path.exists(target_folder): # 如果新文件路径已经存在了，说明这个文件夹里已经有一个同名的文件了
            os.makedirs(target_folder) # 就在文件名后面加个“_副本”来区分，避免覆盖掉原来的文件

        target_file_path = os.path.join(target_folder, file) # 新文件路径，放在以文件后缀名命名的文件夹里

        # 请替换第 112 到 115 行：
        count = 1  # 把计数器放到这里，每次遇到重名文件都从 1 开始加
        while os.path.exists(target_file_path): # 用 while 循环一直查，直到名字不冲突
            new_name = f"{name}_{count}{ext}"
            target_file_path = os.path.join(target_folder, new_name)
            count += 1

        old_file_path = os.path.join(current_path, file) # 旧文件路径
        # os.path.join(path, folder_name, file) 
       
        
        shutil.move(old_file_path, target_file_path) # 搬家
        print(f"成功搬运 {file} -> {folder_name}")

        log_move(file, old_file_path, target_file_path )

if __name__ == "__main__": # "__main__" 两段_ 防止出现语法错误
    main()
            

