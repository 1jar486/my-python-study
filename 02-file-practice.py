import os 
import shutil
import sqlite3
import hashlib # 新增：python自带的工具箱
import hashlib # 新增：python自带的工具箱
from datetime import datetime

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

# 主逻辑开始
def main():
    init_db()

    # current_path = r'C:\Users\Administrator\Desktop\自动整理测试'
    current_path = os.path.dirname(os.path.realpath(__file__)) # 获取当前路径，让脚本自动识别自己在哪个文件路径
    print(f"我现在的办公地点是：{current_path}") 

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

if __name__ == "__main__":
    main()
            

