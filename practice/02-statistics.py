# 练习2：成绩统计
# 要求：给一个分数列表，输出平均分、最高分、最低分、及格人数
# 注:谁来作为比较的第一个对象，初始值怎么选；保留两位小数round(average, 2)

scores = [78, 92, 55, 88, 61, 45, 97, 73]

if len(scores) == 0:
    print("没有成绩，无法统计")
else:
    total = 0
    max_score = scores[0]
    min_score = scores[0]
    pass_count = 0

    for s in scores:
        total += s
        if s > max_score:
            max_score = s
        if s < min_score:
            min_score = s
        if s >= 60:
            pass_count += 1

    average = total / len(scores)
    print("平均分:", round(average, 2))
    print("最高分:", max_score)
    print("最低分:", min_score)
    print("及格人数:", pass_count)
