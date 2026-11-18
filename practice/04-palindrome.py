def is_palindrome(s):
    """判断字符串 s 是否回文。是返回 True，否返回 False。"""
    return s == s[::-1] 


def is_palindrome_two_pointers(s):
    """判断字符串 s 是否回文。是返回 True，否返回 False。"""
    left = 0
    right = len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True

print(is_palindrome("level"))   # True
print(is_palindrome("hello"))   # False
print(is_palindrome("abba"))    # True
print(is_palindrome("a"))       # True
print(is_palindrome_two_pointers("level"))   # True
print(is_palindrome_two_pointers("hello"))   # False
print(is_palindrome_two_pointers("abba"))    # True
print(is_palindrome_two_pointers("a"))       # True