def char_count(s):
    """返回字典：键是字符，值是该字符出现的次数。"""
    # count_dict = {}
    # for char in s:
    #     if char in count_dict:
    #         count_dict[char] += 1
    #     else:
    #         count_dict[char] = 1
    # return count_dict

    count_dict = {}
    for char in s:
        count_dict[char] = count_dict.get(char, 0) + 1
    return count_dict

print(char_count("hello"))      # {'h': 1, 'e': 1, 'l': 2, 'o': 1}
print(char_count("aab"))        # {'a': 2, 'b': 1}
print(char_count(""))           # {}