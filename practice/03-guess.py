# 练习2：猜数字
# 要求：程序随机想一个 1–100 的数，用户输入猜，提示大了/小了，猜对结束
# 注:1. 使用 random.randint(1, 100) 生成随机整数，区间为闭区间。
# 2. 使用 while 循环实现重复猜测。
# 3. 使用 int() 函数将用户输入的字符串转换为整数
# 4.random中常用的函数：random.randint(a, b) 生成[a, b]之间的随机整数，random.random() 生成[0.0, 1.0)之间的随机小数，random.choice(seq) 从序列中随机选取一个元素，random.shuffle(seq) 将序列中的元素随机打乱顺序。
import random
a=random.randint(1,100)
b=int(input('请输入一个1-100的整数：'))
while b!=a:
    if b>a:
        print('大了')
    else:
        print('小了')
    b=int(input('请重新输入一个1-100的整数：'))
print('猜对了！')