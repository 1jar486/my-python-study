import os 
import shutil

current_path = os.getcwd() # 获取当前路径，让脚本自动识别自己在哪个文件路径
print(f"我现在的办公地点是：{current_path}")

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

for file in os.listdir(current_path):
        # os.path.join()拼接完整路径，也就是获取这个文件夹里面的文件或文件夹的绝对地址
        full_path = os.path.join(current_path, file)
        # 如果这不是一个文件，即它是一个文件夹 os.path.isfile() 判断是否是文件，必须给它完整路径
        if not os.path.isfile(full_path):
            continue # 不是文件直接跳过，不管它

        name, ext = os.path.splitext(file) # 分别获取文件名和后缀名

        if not ext:
            continue # 没有后缀名的文件直接跳过，不管它
        
        # 把后缀名的点去掉([1:])，并转成大写(upper())，作为文件夹的名字
        folder_name = ext[1:].upper() 
         # 双重拼接，先把文件夹路径和文件夹名字粘合成完整路径，再把这个路径和文件名粘合成新文件的完整路径
        new_file_path = os.path.join(current_path, folder_name, file) # 新文件路径，放在以文件后缀名命名的文件夹里

        if os.path.exists(new_file_path): # 如果新文件路径已经存在了，说明这个文件夹里已经有一个同名的文件了
            new_file_path = os.path.join(current_path, folder_name, name + '_副本' + ext) # 就在文件名后面加个“_副本”来区分，避免覆盖掉原来的文件

        
        print(f"原名是：{file} --> 切开的后缀名是：{ext}")
        
        
        if not os.path.exists(os.path.join(current_path, folder_name)): # 如果这个文件夹不存在
            os.makedirs(os.path.join(current_path, folder_name)) # 就创建一个以后缀名命名的文件夹

        old_file_path = os.path.join(current_path, file) # 旧文件路径
        # os.path.join(path, folder_name, file) 
       
        count = 1
        new_name = f"{folder_name}_{count}{ext}" # 新文件名，格式是：文件夹名字_数字.后缀名
        new_file_path = os.path.join(current_path, folder_name, new_name) # 新文件路径，放在以文件后缀名命名的文件夹里
        count += 1
        shutil.move(old_file_path, new_file_path) # 搬家
        print(f"成功搬运 {file} -> {folder_name}")
            

