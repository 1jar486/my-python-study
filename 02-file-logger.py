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

def main():
    if __name__ == "__main__":
        main()