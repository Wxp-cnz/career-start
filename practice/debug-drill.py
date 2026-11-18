# 调试练习：这个文件里有 3 个错误，用 traceback 逐个找出来

# 规则：
#   1. 直接运行，会报第一个错。修好，再运行，会报第二个错。修到输出干净为止。
#   2. 每看到一个报错，按这个顺序读：
#        第一步：看最后一行 —— 错误类型 + 一句话说明（这是「结论」）
#        第二步：从最后一行往上找最近的 `File "xxx.py", line N` —— 这才是「你代码里」出错的行
#        第三步：看那一行里哪个变量是 None / 类型不对 / 下标超了
#   3. 不要靠猜，不要一次性改多处。改一处，跑一次。

# 修完之后的正确输出应该是：
#   平均分： 88.5
#   学生：小妮子
#   成绩：88
#   评价：继续加油
#   最高分： 95


def average(scores):
    total = 0
    for s in scores:
        total += s
    return total / len(scores)


def report(name, score):
    print("学生：" + name)
    print("成绩：" + str(score))
    print("评价：" + ("优秀" if score >= 90 else "继续加油"))


scores = [88, 92, 79, 95]
avg = average(scores)
print("平均分：", avg)

report("小妮子", scores[0])

top = max(scores)
print("最高分：", top)
