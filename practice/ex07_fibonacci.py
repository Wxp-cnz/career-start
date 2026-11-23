# nums=[1,1]
# while len(nums)<20:
#   nums.append(nums[-1]+nums[-2])
# print(nums)

def fibonacci_list(n):
    list_fib = [1, 1]
    if n == 1:
        return [1]
    if n == 0:
        return []    
    for _ in range(2, n):
        list_fib.append(list_fib[-1] + list_fib[-2])
    return list_fib

print(fibonacci_list(20))

def fibonacci_roll(n):
    a, b = 1, 1
    for _ in range(n):
        print(a, end=" ")       # 先打印当前的 a
        a, b = b, a + b         # 再往前挪
    print()                      # 换行


fibonacci_roll(20)