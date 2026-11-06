def two_sum_brute(nums, target):
    """暴力解法：两层循环，时间复杂度 O(n^2)"""
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []


def two_sum(nums, target):
    """哈希表解法：时间复杂度 O(n)

    思路：一边遍历一边把见过的数字存进字典。
    每遇到一个新数字 num，先问一句：
    target - num 之前出现过吗？出现过就直接凑成答案。
    """
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []


if __name__ == "__main__":
    print(two_sum([2, 7, 11, 15], 9))
    print(two_sum([3, 2, 4], 6))
    print(two_sum([3, 3], 6))
