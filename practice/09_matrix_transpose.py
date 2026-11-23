def transpose(matrix):
    rows = len(matrix)        # 原矩阵有几行 → 转置后有几列
    cols = len(matrix[0])     # 原矩阵有几列 → 转置后有几行

    result = []
    for j in range(cols):         # 新矩阵的第 j 行
        new_row = []
        for i in range(rows):     # 新矩阵的第 j 行、第 i 列
            new_row.append(matrix[i][j])   
        result.append(new_row)
    return result


print(transpose([[1, 2, 3], [4, 5, 6]]))


def transpose_zip(matrix):
    return [list(row) for row in zip(*matrix)]


print(transpose_zip([[1, 2, 3], [4, 5, 6]]))
print(transpose([[1, 2], [3, 4]]))

