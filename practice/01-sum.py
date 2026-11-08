#练习1：求1到100的和，分别用for和while循环实现
#注意事项：1.python的区间是左闭右开，因此range(1,101)表示从1到100
#          2.while循环用在不知道要循环几次但是知道什么条件下停止，for循环需要知道自己在遍历什么。
sum_for = 0
for i in range(1,101):
    sum_for += i
print("for循环求和结果为：",sum_for)

sum_while =0
i=1
while i<101:
    sum_while += i
    i+=1
print("while循环求和结果为：",sum_while)