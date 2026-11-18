# Python 工程基础笔记

## 0. 日常命令

### 0.1 运行脚本

```bash
uv run python practice/01-sum.py    # 推荐：自动使用项目虚拟环境
python practice/01-sum.py           # 仅在已 activate 时可用
uv run python                       # 交互式解释器，Ctrl+D 或 exit() 退出
```

`uv run` 每次自动定位 `.venv`，不依赖当前终端是否激活。

### 0.2 提交代码

Git 的三段式：**工作区 → 暂存区 → 本地版本库 → 远程仓库**

| 命令 | 作用 |
|---|---|
| `git status` | 查看哪些文件被修改、哪些已暂存 |
| `git add 文件名` | 把指定文件放入暂存区 |
| `git commit -m "说明"` | 把暂存区内容保存为一个版本 |
| `git push` | 把本地提交推送到远程仓库 |
| `git log --oneline` | 查看提交历史，一行一条 |

一次完整提交：

```bash
git status                          # 先看改了什么
git add practice/04-palindrome.py   # 只暂存这个文件
git commit -m "feat(practice): 完成练习 4 判断回文"
git push
```

- 保存文件（Ctrl+S）不等于提交，只改动了工作区
- 优先 `git add 具体文件名`，避免 `git add .` 把无关文件一起提交
- 暂存错了用 `git restore --staged 文件名` 撤回

### 0.3 提交信息格式

`类型(范围): 说明`，类型用下列前缀：

| 前缀 | 用于 |
|---|---|
| `feat` | 新增功能或练习 |
| `fix` | 修复错误 |
| `docs` | 文档、笔记 |
| `refactor` | 重写实现但不改变行为 |
| `chore` | 环境、依赖、配置 |

## 1. 运行环境

### 1.1 环境的三要素

1. **解释器**：`python.exe`，逐行执行 `.py` 文件
2. **第三方库**：被 import 的包，实际是磁盘上的目录
3. **路径设置**：告诉系统解释器与库在哪里，核心是 `PATH`

### 1.2 PATH

敲下命令后，系统按 `PATH` 中列出的目录**从上到下依次查找**同名可执行文件，命中第一个即执行。

- **顺序决定结果**：靠前的目录优先
- **修改 PATH 后必须重开终端**：已打开的终端持有启动时的 PATH 副本
- `command not found` 的三个原因：没装、所在目录不在 PATH、终端开在修改之前

### 1.3 虚拟环境

**问题**：第三方库默认装入全局 `site-packages`，同名库只能存在一个版本，多项目互相覆盖。

**方案**：每个项目一个独立的库目录（`.venv`）。

**实现**：不是复制整个 Python。`.venv` 内只含：

- `Scripts/python.exe`：启动器
- `Lib/site-packages/`：本项目安装的库
- `pyvenv.cfg`：指向真正的解释器，并声明是否使用全局库

```ini
home = <Python 安装目录>                 # 标准库来源
include-system-site-packages = false     # 不使用全局 site-packages
version_info = 3.13.11
```

### 1.4 uv

uv 用三个文件固定依赖状态，使环境可复现：

| 文件 | 内容 | 提交 Git |
|---|---|---|
| `pyproject.toml` | 依赖声明（版本范围） | 是 |
| `uv.lock` | 实际解析出的精确版本 | 是 |
| `.venv/` | 真实的库文件 | 否，可由前两者重建 |

```bash
uv init --bare                              # 生成 pyproject.toml
uv venv --python <解释器路径>                # 创建 .venv
uv add <包名>                               # 装包，同时更新 toml、lock、.venv
uv remove <包名>                            # 卸载，同上
uv sync                                     # 按 lock 还原 .venv
uv run python file.py                       # 在虚拟环境中执行，无需激活
```

注意：机器上有多个 Python 时，`uv venv` 需用 `--python` 显式指定，否则会选用它自行发现的解释器。

### 1.5 activate

`activate`（bash）、`activate.bat`（cmd）、`Activate.ps1`（PowerShell）的作用：**把 `.venv/Scripts` 插入当前终端的 PATH 最前面**，使后续 `python`、`pip` 指向虚拟环境。

```bash
source .venv/Scripts/activate   # bash 必须用 source
deactivate                      # 退出
```

- 必须 `source`：需要修改**当前** shell 的环境变量，直接执行只在子进程中生效
- 只影响当前终端窗口，不改系统设置
- 激活后提示符会显示环境名
- 用 `uv run` 时不需要激活

## 2. 调试

### 2.1 traceback 的结构

Python 报错输出的调用栈，**从下往上读**：

```
Traceback (most recent call last):
  File "app.py", line 12, in <module>
    result = compute(data)
  File "app.py", line 5, in compute
    return total / count
           ^^^^^
NameError: name 'total' is not defined
```

| 顺序 | 位置 | 得到的信息 |
|---|---|---|
| 1 | 最后一行 | 错误类型与原因 |
| 2 | 最靠下的 `File` 行 | 出错的具体位置（更靠上的 `File` 行是调用者） |
| 3 | 该行被 `^^^^^` 标注的变量 | 哪个名字、类型或下标有问题 |

`most recent call last` 意为「越往下越内层」，最下面的 `File` 行即错误发生处。

### 2.2 常见错误类型

| 错误 | 含义 | 常见原因 |
|---|---|---|
| `NameError` | 名字未定义 | 拼写错误；变量未赋值；缺少 `import` |
| `TypeError` | 类型不匹配 | 字符串与数字相加；对 `None` 运算；参数个数不符 |
| `IndexError` | 下标越界 | 下标 ≥ `len()`；空序列取下标 |
| `KeyError` | 字典键不存在 | 访问未写入的键 |
| `AttributeError` | 对象无此属性 | 导入方式错误；方法名拼写错误 |
| `ValueError` | 值不合法 | 类型正确但内容不合法，如 `int("abc")` |
| `IndentationError` | 缩进错误 | 空格与 Tab 混用；缩进层级不符 |
| `SyntaxError` | 语法错误 | 缺少冒号或括号；引号未闭合 |

`IndentationError` 是 `SyntaxError` 的子类。

**导入导致 `AttributeError` 的典型情况**：

```python
from random import random    # 导入的是函数 random
random.randint(1, 10)        # AttributeError：函数没有 randint 属性

import random                # 正确：导入模块
random.randint(1, 10)
```

### 2.3 断点调试

在代码中插入 `breakpoint()`，执行到该行时暂停并进入 pdb。

| 命令 | 作用 |
|---|---|
| `p 表达式` | 打印变量或表达式的值 |
| `n` | 执行下一行（不进入函数） |
| `s` | 执行下一行（进入函数） |
| `l` | 显示当前位置附近的源码 |
| `c` | 继续执行至结束 |
| `q` | 退出调试器，程序终止 |

- pdb 提示符为 `(Pdb)`，其下**只输入单字母命令**，不带路径或参数
- 退出后在普通终端重新运行，才会执行修改后的代码
- 与 `print` 相比：不必修改源码、可查看全部变量、可逐行观察执行流程
- 调试结束后应删除 `breakpoint()`

### 2.4 排错流程

```
1. 复现：稳定得到同一个错误
2. 定位：读 traceback，确定类型、位置、变量
3. 假设：明确指出「第几行的哪个变量有问题，原因是……」
4. 验证：用 breakpoint() 或 print 确认假设
5. 修改：一次只改一处
6. 重跑：错误变化说明方向正确；错误不变则假设有误，回到第 3 步
```

**修好不等于修对**：能运行之后，还需检查是否依赖特定数据。例如取列表最大值应写 `max(data)`，而非 `data[3]`——后者换一组数据即失效。
