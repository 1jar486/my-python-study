import os 
import shutil
import sqlite3
import hashlib # 新增：python自带的工具箱
from datetime import datetime
import time # 新增，用于获取当前时间戳和计算时间差

# 数据库功能函数
def init_db(): # 初始化数据库
    '''初始化数据库，创建记录表'''
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
    '''将文件移动记录写入数据库'''
   
    try:
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
    except Exception as e:
        print(f"数据库记录失败：{e}")
       
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

# 新增部分
def get_file_md5(file_path):
    '''计算特定文件的md5数字指纹
        1. 创建一个空的 MD5 计算器。
        2. 以“二进制只读”(rb) 模式打开文件。不管它是图片还是视频，在电脑底层都是二进制0和1。
        3. 每次只读一小块（4096字节），喂给计算器。直到读完为止。
        4. 吐出最终计算好的 32 位十六进制字符串。
    '''
    # 1.创建MD5对象
    md5_hash = hashlib.md5()

    try:
        # 2.以二进制读取模式(‘rb')打开文件
        with open(file_path,"rb") as f:
            # 3.循环分块读取，每次读取4kb
            chunk = f.read(4096)
            # 只要chunk有东西，就一直循环
            while chunk:
                md5_hash.update(chunk) # 把刚读取出来的一小块内容"喂给计算器,更新当前的指纹状态
                chunk = f.read(4096)
        # 4.最终返回的指纹结果(hexdigest会把结果转换成易读的英文字母+数字)
        return md5_hash.hexdigest()
    except Exception as e:
        print(f"读取文件指纹时出错{file_path}:{e}")
        return None
        
def organize_files_by_extension(current_path):
    '''封装原有的分类逻辑：遍历目录 -> MD5去重-> 过滤 -> 按后缀分类 -> MD5去重 -> 搬运'''
    print("\n" + "=" * 40)
    print(f"阶段一：开始按后缀名分类整理文件...")

    # 遍历当前目录下的所有东西
    for file in os.listdir(current_path):
        # 拼接绝对路径
        full_path = os.path.join(current_path,file)

        # 过滤逻辑开启
        # 1. 排除已经建好的分类文件夹
        if not os.path.isfile(full_path):
            print(f"📁 发现文件夹，不作处理: {file}")
            continue

        # 2. 排除系统文件、隐藏文件
        if file.upper() in ["NTUSER.DAT", "INDEX.DAT"] or file.startswith('.'):
            print(f"👻 跳过隐藏/系统文件: {file}")
            continue       
        
       # 3. 排除Python脚本和数据库账本
        # 增加 file == "file_history.db" 这个条件
        if  file == os.path.basename(__file__) or file == "file_history.db":
            print(f"🛠️ 跳过代码脚本/数据库: {file}")
            continue
        
        # 过滤逻辑结束
        # 分离文件名和后缀名
        name, ext = os.path.splitext(file)

        # 如果文件没有后缀名，为了安全起见,我们跳过它
        if not ext:
            print(f"跳过无后缀文件：{file}")
            continue

        # 把后缀名的点去掉([1:])，并转成大写(upper())，作为文件夹的名字
        folder_name = ext[1:].upper() 


         # 双重拼接，先把文件夹路径和文件夹名字粘合成完整路径，再把这个路径和文件名粘合成新文件的完整路径
        # 例如：target_folder = r'C:\Users\Administrator\Desktop\自动整理测试\去掉.的大写后缀'  去掉.的大写后缀如：JPG,DOCX,TXT,PNG,MP4等
        # 假设正在处理这个文件 target_folder = r'C:\Users\Administrator\Desktop\自动整理测试\MP4'
        target_folder = os.path.join(current_path, folder_name) # 新文件路径，放在以文件后缀名命名的文件夹里 
        
        if not os.path.exists(target_folder): # 如果新文件路径已经存在了，说明这个文件夹里已经有一个同名的文件了
            os.makedirs(target_folder) # 就在文件名后面加个“_副本”来区分，避免覆盖掉原来的文件
        
        target_file_path = os.path.join(target_folder, file) # 新文件路径，放在以文件后缀名命名的文件夹里
        source_file_path = full_path
        # 旧的重名逻辑处理
        # count = 1  # 把计数器放到这里，每次遇到重名文件都从 1 开始加
        # while os.path.exists(target_file_path): # 用 while 循环一直查，直到名字不冲突
        #     new_name = f"{name}_{count}{ext}"
        #     target_file_path = os.path.join(target_folder, new_name)
        #     count += 1
        
        # 核心排重与放冲突逻辑开始
        # 如果目标文件夹里，已经存在一个和它一摸一样的文件了
        if os.path.exists(target_file_path):
            # 1.计算要搬迁的源文件的指纹
            source_md5 = get_file_md5(source_file_path)
            
            # 2.计算目标文件夹里那个重名文件的指纹
            target_md5 = get_file_md5(target_file_path)

            # 3.对比指纹
            if source_md5 == target_md5:
                # 情况A:指纹一样，内容完全相同。不需要搬了
                print(f"发现重复的文件，已跳过搬运：{file}")
                continue
            else:
                # 情况B:指纹不一样,说明只是名字碰巧一样，它们是两个独立的文件
                # 启动重命名机制 
                count = 1
                while os.path.exists(target_file_path):
                    new_name = f"{name}_{count}{ext}" # 组装新名字：原名_1.后缀
                    target_file_path = os.path.join(target_folder,new_name)
                    count += 1
                    # 核心排重与冲突逻辑结束
        try:
            shutil.move(source_file_path,target_file_path)
            print(f"成功搬运：{file}->{target_folder}")
            #记录到数据库
            log_move(os.path.basename(target_file_path),source_file_path,target_file_path)
        except Exception as e:
            print(f"搬运{file}时发生错误：{e}")

def archive_inactive_files(base_path, days_threshold=30):
    '''
    核心目标：扫描分类文件夹，将超过指定天数未修改的文件移入 Archive 子文件夹。
    为初学者解释背后的考量：我们不仅要移动文件，还要处理权限、符号链接和重名等边缘情况。
    '''
    print("\n" + "="*40)
    print("⏳ 开始执行长时间未活动文件归档检查...")
    
    # 获取当前操作系统的绝对时间（以秒为单位的浮点数）
    current_time = time.time()
    
    # 计算时间阈值：将天数转换为秒数。30天 * 24小时 * 60分钟 * 60秒
    seconds_threshold = days_threshold * 24 * 60 * 60

    # 1. 遍历当前目录下的所有项目（寻找分类文件夹，如 JPG, TXT 等）
    for item_name in os.listdir(base_path):
        folder_path = os.path.join(base_path, item_name)
        
        # 【边界防御】必须是文件夹，且排除隐藏文件夹（点开头）以及归档文件夹本身
        if not os.path.isdir(folder_path) or item_name.startswith('.') or item_name.upper() == 'ARCHIVE':
            continue
            
        # 此时，我们进入了一个分类文件夹，例如 `base_path/JPG`
        
        # 2. 遍历该分类文件夹内的所有文件
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            
            # 【边界防御】跳过子文件夹，我们只处理当前层级的文件
            if not os.path.isfile(file_path):
                continue
                
            # 【边界防御】跳过符号链接（快捷方式），移动快捷方式可能破坏系统原本的指向
            if os.path.islink(file_path):
                continue
                
            try:
                # 3. 获取文件的最后修改时间 (Modification Time)
                # os.path.getmtime() 返回的也是自1970年以来的秒数
                last_modified_time = os.path.getmtime(file_path)
                
                # 4. 判断逻辑：如果（现在 - 最后修改时间） > 30天的秒数
                if (current_time - last_modified_time) > seconds_threshold:
                    
                    # 确定归档文件夹的位置：分类文件夹下的 Archive 目录
                    archive_folder_path = os.path.join(folder_path, "Archive")
                    
                    # 如果归档文件夹不存在，则自动创建
                    if not os.path.exists(archive_folder_path):
                        os.makedirs(archive_folder_path)
                        print(f"📂 创建了归档目录: {archive_folder_path}")
                        
                    # 确定文件的最终目标路径
                    target_file_path = os.path.join(archive_folder_path, file_name)
                    
                    # 5. 【边界防御】处理重名冲突：如果 Archive 里面已经有了同名文件
                    if os.path.exists(target_file_path):
                        name, ext = os.path.splitext(file_name)
                        count = 1
                        # 循环寻找一个没有被占用的新名字
                        while os.path.exists(target_file_path):
                            # 我们在名字里加上 _archived_1 的后缀以示区别
                            new_name = f"{name}_archived_{count}{ext}"
                            target_file_path = os.path.join(archive_folder_path, new_name)
                            count += 1
                            
                    # 6. 执行物理移动
                    shutil.move(file_path, target_file_path)
                    print(f"📦 已归档老文件: {file_name} -> {item_name}/Archive")
                    
                    # 7. 记录到数据库
                    log_move(os.path.basename(target_file_path), file_path, target_file_path)
                    
            except (PermissionError, OSError) as e:
                # 【边界防御】如果文件正在被别的程序使用，或者没有权限移动，捕获异常并跳过，防止程序死掉
                print(f"⚠️ 无法归档文件 {file_name} (可能正在被使用或权限不足): {e}")
            except Exception as e:
                print(f"❌ 归档 {file_name} 时发生未知错误: {e}")

# 主逻辑开始
def main():
    # 1.环境准备
    init_db()
    # current_path = r'C:\Users\Administrator\Desktop\自动整理测试'
    current_path = os.path.dirname(os.path.realpath(__file__)) # 获取当前路径，让脚本自动识别自己在哪个文件路径
    print(f"我现在的办公地点是：{current_path}") 

    # 2. 执行阶段一：基础分类整理 (调用新封装的函数)
    organize_files_by_extension(current_path)
    
    # 3. 执行阶段二：自动化归档（30天过期检查） 
    archive_inactive_files(current_path, days_threshold=30)
    
    print("\n🎉 所有文件整理与归档任务执行完毕！")
if __name__ == "__main__":
    main()
            

