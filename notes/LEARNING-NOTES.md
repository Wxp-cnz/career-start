# 学习笔记（与 AI 讨论整理）

> 用法：一个主题一条，编号往后加。新问题先自己写两行，再补细节。
> 目录：见下方「进度一览」，写完一条就更新。

| 编号 | 主题 | 日期 |
|---|---|---|
| 1 | 配环境：环境 / PATH / 虚拟环境 / uv 项目 / activate | 2026-11-18 |
| 2 | traceback 与断点调试 | 2026-11-18 |

---

## 1. 配环境相关知识

### 1.1 「环境」到底指什么

不是一个抽象词，是**三样能摸到的东西**：

1. **解释器**——`D:\python\python.exe` 这个文件。`.py` 文件自己不会动，是它逐行读、逐行执行
2. **一批库**——`requests`、`pandas` 这些第三方代码，实际是硬盘上某个文件夹里的 `.py` 文件
3. **一组路径和开关**——告诉系统「解释器在哪、库在哪」，最重要的是 PATH

配环境 = 让这三样在正确的时间出现在正确的位置。

### 1.2 环境变量与 PATH

**环境变量**：操作系统随身携带的一张便签，上面写着全局设置（`PATH`、`TEMP`、`HTTP_PROXY` 等）。程序启动时读它，据此决定行为。

**PATH 的特殊之处**：它决定你敲的命令去哪找。敲 `python` 时，系统拿这个名字去 PATH 列出的目录**从上到下挨个翻**，找到第一个 `python.exe` 就执行，后面的不管。

```
敲 python
  → D:\python\Scripts      没有
  → D:\python\             有 → 执行它，结束
  → C:\Windows\system32    不看
  → C:\Windows             不看
  → D:\Program Files\Git\cmd 不看
```

三个推论：

1. **顺序决定一切**：如果 `D:\python\Scripts` 里也有 `python.exe`，用的就是那个
2. **改完 PATH 要重开终端**：终端启动时把 PATH 复制了一份，事后改系统设置它不知道 → 这就是 `command not found` 的最常见原因
3. **`uv` 为什么能直接用**：`uv.exe` 落在 `D:\python\Scripts\`，这目录本来就在 PATH 里，装的时候什么都没多配

> 排查口诀：`command not found` 先问三件事——装了吗？在 PATH 里吗？终端是改完之后才开的吗？

### 1.3 虚拟环境为什么必要

Python 默认把所有第三方库塞进一个地方：`D:\python\Lib\site-packages`，**全局共享，同名库只能有一个版本**。

冲突场景：项目 A 要 pandas 1.5，项目 B 要 pandas 2.2 → 装哪个都会让另一个跑不起来。

虚拟环境的解法：**每个项目一个独立的库目录**。

### 1.4 虚拟环境的本质（比想象中土）

不是复制一整个 Python。`.venv` 总共才 3.6MB，而完整 Python 是几百 MB。它只做两件事：

1. 把 `python.exe` 复制一份放到 `.venv\Scripts\`
2. 改掉「去哪找库」这个设置

证据是 `.venv/pyvenv.cfg`：

```ini
home = D:\python                        # 标准库用谁家的（省几百 MB）
include-system-site-packages = false    # 不去全局 site-packages 找包
version_info = 3.13.11
prompt = career-start                   # 激活后提示符显示的名字
```

所以「虚拟环境」= 一个文件夹 + 一个配置文件 + 复制的一份 python.exe。库真的在 `.venv\Lib\site-packages`。

### 1.5 uv 项目是什么

「uv 项目」不是特殊东西，就是**一个普通文件夹**，只不过用文件把依赖状态固定下来了。

三个文件的分工：

| 文件 | 是什么 | 内容举例 | 提交 Git |
|---|---|---|---|
| `pyproject.toml` | 我想要什么 | `requests >= 2.34` | 是 |
| `uv.lock` | 实际装了什么 | `requests 2.34.2` + 依赖树 | 是 |
| `.venv/` | 硬盘上的真文件 | 3.6 MB 的包 | 否（可重建） |

`.venv` 不提交的理由：它能从另外两个文件完整重建。**仓库只存配方，不存成品。**

常用命令：

```bash
uv init --bare                      # 只生成 pyproject.toml
uv venv --python D:/python/python.exe  # 建 .venv，指定解释器
uv add requests                     # 装包：同时改 toml、lock、.venv
uv remove requests                  # 卸包，三处同改
uv sync                             # 按 lock 把 .venv 还原（clone 后第一步）
uv run python xxx.py                # 在虚拟环境里跑，不用 activate
```

一个坑：**uv 默认会挑它自己找到的第一个 Python**。本机装了多个时，要 `--python D:/python/python.exe` 显式指定，否则 `.venv` 可能指向一个以后会失效的目录。

### 1.6 activate 是什么

一个脚本文件，`.venv/Scripts/` 下有多个版本：

- `activate` —— 给 bash / Git Bash
- `activate.bat` —— 给 cmd
- `Activate.ps1` —— 给 PowerShell

**它只做一件事：改动当前终端窗口的 PATH，把 `.venv\Scripts` 插到最前面。** 插到最前面，就等于后续敲 `python` 先在这里找。

实际效果：

```
激活前  which python → D:\python\python.exe
激活后  which python → ...\career-start\.venv\Scripts\python.exe
```

用法与注意事项：

```bash
source .venv/Scripts/activate    # 必须 source，不能直接运行
```

- 必须 `source`：因为它要改**当前** shell 的环境变量。直接运行会在子进程里改，子进程一退出就白改
- 确认成功：提示符前面多出 `(career-start)`
- 退出：`deactivate`
- 关掉窗口就失效：它不动系统设置，只影响当前窗口

**结论：日常不用它。** `uv run python xxx.py` 等价于「只对这一次命令生效的 activate」，且不会忘。只有三种情况还需要 activate：VS Code 点运行按钮、进交互式 `python`、直接用 `pip`。

---

## 2. traceback 与断点调试

### 2.1 为什么调试能力比写代码能力更早需要

真实时间分配大约：**写 3 成，找问题 7 成**。能不能自己排出错，决定你是「独立干活的人」还是「每遇报错就问人的人」。面试也常考——给一段报错的代码，问你怎么查。

### 2.2 traceback 的固定结构

报错时 Python 打印的是一份**调用栈报告**，结构永远一样，从下往上读：

```
Traceback (most recent call last):
  File "practice\debug-drill.py", line 33, in <module>
    avg = average(scores)
  File "practice\debug-drill.py", line 23, in average
    return totol / len(scores)
           ^^^^^
NameError: name 'totol' is not defined
```

读的顺序（三步，固定动作）：

| 步骤 | 看哪里 | 得到什么 |
|---|---|---|
| ① | **最后一行** | 错误类型 + 一句话结论 |
| ② | 从下往上**最近的 `File` 行** | 你自己的代码在第几行（上面的 `site-packages` 路径一律不看） |
| ③ | 那一行的**具体变量**（`^^^^^` 就是它标出来的） | 哪个名字/类型/下标有问题 |

关键认知：**`Traceback (most recent call last)` 的意思是「越往下越靠里」**。最下面的 `File` 行才是错误真正发生的地方，上面的行是「谁调用了它」。

### 2.3 常见错误类型对照表

| 错误 | 中文 | 典型原因 | 改法 |
|---|---|---|---|
| `NameError` | 名字没定义 | 变量名拼错；变量在赋值前就被用；忘了 `import` | 对拼写；检查定义位置 |
| `TypeError` | 类型不对 | `"成绩：" + 88`；对 `None` 做运算；参数个数不对 | 用 `str()` / `int()` 转换 |
| `IndexError` | 下标越界 | 下标 ≥ `len(列表)`；空列表取 `[0]` | 检查长度；取最后一个用 `[-1]` |
| `KeyError` | 字典键不存在 | 用了没存的 key | `d.get(k, 默认值)` |
| `AttributeError` | 对象没这个属性 | 导入方式错（见下）；方法名写错 | 看 `import` 那行 |
| `ValueError` | 值不合法 | `int("abc")`；解包数量不符 | 检查输入 |
| `IndentationError` | 缩进不对 | 空格与 Tab 混用；层级错 | 统一 4 个空格 |
| `SyntaxError` | 语法错 | 少冒号、少括号、引号没闭合 | 看 `^` 标的位置 |

**踩过的坑（要记住）**：

```python
from random import random      # 这样导入的是「函数 random」，不是「模块 random」
random.randint(1, 100)         # AttributeError: 'builtin_function_or_method' object has no attribute 'randint'

import random                  # 正确：导入模块，用 random.randint()
```

同类问题：`import random` 和 `from random import randint` 都可以，但 `from random import random` 会把模块名覆盖掉。

### 2.4 修好 ≠ 修对

`debug-drill.py` 里第三个错，原始是 `scores[5]`（`IndexError`）。改成 `scores[3]` 能跑，输出也正好是 95——**但这是巧合**，因为 `scores = [88, 92, 79, 95]` 恰好最大值在最后一位。

```python
top = scores[3]        # 能跑，但依赖「数据长这样」
top = max(scores)      # 对：不依赖数据顺序和长度
```

判断标准：**换一组数据，代码还对吗？** 不对就说明是硬编码，不是真修好。

### 2.5 断点调试：breakpoint()

在代码里插一行 `breakpoint()`，运行到这里会**暂停**，进入交互式调试器（pdb）。

```python
def average(scores):
    total = 0
    for s in scores:
        breakpoint()        # 每次循环都停一次
        total += s
    return total / len(scores)
```

会用 4 个命令就够：

| 命令 | 作用 |
|---|---|
| `p 变量名` | 打印这个变量的当前值（如 `p total`） |
| `n` | 执行下一行（next） |
| `c` | 继续跑到底（continue） |
| `q` | 退出调试（quit） |

比 `print` 好在哪：

- 不用改代码（插一行就够了，不用到处加 `print` 再删）
- 能看**所有**变量的值，不限于你事先想到打印的那个
- 能一行一行看流程怎么走，看清「什么时候值变成错的」

用完删掉 `breakpoint()`，别提交进去。

### 2.6 排错的固定流程（背下来）

```
1. 复现   —— 稳定地跑出同一个错
2. 定位   —— 读 traceback：① 类型  ② 最近 File 行  ③ 那个变量
3. 假设   —— 说出「第 N 行的 X 是错的，因为……」
4. 验证   —— breakpoint() 看实际值，或临时 print
5. 改一处 —— 只改一个地方
6. 重跑   —— 错变了说明方向对，接着改；错没变说明假设错了，回第 3 步
```

最要命的坏习惯：**不读报错，直接乱改**。改一堆地方只会让错误信息变模糊，把一个小问题变成三个。
