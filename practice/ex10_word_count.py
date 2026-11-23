def read_text(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

    
def word_count(words):
    counts = {}
    for w in words:
        counts[w] = counts.get(w,0) + 1       # ← 填什么
    return counts

text = read_text("practice/data/sample-text.txt")
words = text.split()          # 按空白切分成单词列表
counts = word_count(words)

print("总词数：", len(words))
print("不同单词数：", len(counts))
print("出现最多：", max(counts, key=counts.get))
