def primes(n):
    """返回 1 到 n 之间（含 n）所有质数组成的列表。"""
    if n < 2:
        return []
    prime_list = []
    for i in range(2, n + 1):
        is_prime = True
        for j in range(2, int(i ** 0.5) + 1):
            if i % j == 0:
                is_prime = False
                break
        if is_prime:
            prime_list.append(i)
    return prime_list


print(primes(20))   # [2, 3, 5, 7, 11, 13, 17, 19]
print(primes(1))    # []
print(primes(2))    # [2]