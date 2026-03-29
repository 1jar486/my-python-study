# 第一周 2026/03/26
# 计算利润
# 场景：详细场景：
#你是一名“个人开发者”，在闲鱼或淘宝上架了一款“自动填表工具”。
# 每天都有零星的订单，单价 199 元。
# 但你很焦虑，因为你不知道除去平台 5% 的服务费，
# 加上你租用的阿里云服务器每月 50 元的开销，
# 你到底卖多少单才能回本？什么时候能开始盈利？
#核心功能描述：
#参数预设： 锁定单价、税率、固定成本。
#动态输入： 每天收工前手动输入当天的销售数量。
#利润透视： 程序自动算出总流水、被平台扣掉的钱以及最后的净利润。
#智能预警： 当利润为负数（亏损）或达到目标（如 2000 元）时，给出不同的经营建议。

# 1.定义固定数据
price = 199 #软件单价
fixed_cost = 50 # 每月固定的服务器成本
tax_rate = 0.05 # 平台抽成比例
# 2.获取用户输入的销量加入异常处理
# 用户输错数字或者输错符号
while True:
    try:
        sales_volume = int(input("大佬，请输入本月销量: "))
        if sales_volume < 0:
            print("销量不能为负数，请重新输入一个非负整数。")
            continue
        break #输入正确后跳出循环
    except ValueError:
        print("输入无效，请输入一个纯数字。(例如: 20)，不要输入文字、字母或者特殊字符")
        

# 3.计算利润
total_revenue = price * sales_volume #计算总收入
platform_fee = price * tax_rate * sales_volume #计算平台抽成
profit = total_revenue - platform_fee - fixed_cost #计算利润

# 4.输出结果
print(f"----------本月财务报表----------") 
print(f"总收入: {total_revenue:.2f} 元") #保留两位小数
print(f"平台抽成: {platform_fee:.2f} 元")
print(f"本月利润: {profit:.2f} 元")

if profit > 2000:
    print("大佬，利润不错哦！继续加油！")
elif profit > 0-2000:
    print("大佬，利润还行，但还有提升空间哦！")
elif profit <= 0:
    print("大佬，亏损了哦！需要调整策略了！")


