# Day04：Linux文件操作命令入门

---

## 📌 今日学习目标

**理论目标**：
- 理解Linux中"一切皆文件"的哲学
- 理解文件权限的基本概念（属主、属组、其他人）
- 理解绝对路径与相对路径的区别

**实操目标**：
- 掌握6条文件操作命令：`touch`、`mkdir`、`cp`、`mv`、`rm`、`cat`
- 能在终端中创建文件夹和文件，进行复制、移动、删除操作
- 学会用 `man` 命令查看帮助手册

**预计学习时间**：理论40min + 实操1h + 复盘20min

---

## 📖 通俗理论讲解

### 4.1 Linux哲学："一切皆文件"

在Linux世界里，**几乎所有东西都被视为"文件"**：
- 你写的文档 → 文件 ✓
- 你的硬盘 → `/dev/sda` 也是文件 ✓
- 你的键盘输入 → `/dev/input/event0` 也是文件 ✓
- 网络连接 → socket也是文件 ✓
- 正在运行的程序 → `/proc/`下面也是文件 ✓

**这有什么好处？**
你只需要学一套"文件操作"方法，就能操作一切——读文件、写文件、删文件，无论是文档还是硬件设备。

**类比**：不管你是吃中餐、西餐、日料，都用同一副筷子——学会用筷子就够了。

---

### 4.2 文件权限概念——入门版

昨天你用 `ls -l` 看到了类似这样的输出：

```
drwxr-xr-x  2  kali  kali  4096  Jul 10 08:00  Desktop
```

拆解给你看：

```
d   rwx   r-x   r-x    2    kali   kali   4096   Jul 10 08:00  Desktop
│   │││   │││   │││    │    │      │      │      │            │
│   │││   │││   │││    │    │      │      │      │            └─ 文件/目录名
│   │││   │││   │││    │    │      │      │      └─ 最后修改时间
│   │││   │││   │││    │    │      │      └─ 文件大小(字节)
│   │││   │││   │││    │    │      └─ 属组(group) = kali组
│   │││   │││   │││    │    └─ 属主(owner) = kali用户
│   │││   │││   │││    └─ 硬链接数(暂时不用管)
│   │││   │││   │││
│   │││   │││   └── 其他人的权限(r-x = 可读+不可写+可执行)
│   │││   │││
│   │││   └────── 属组的权限(r-x = 可读+不可写+可执行)
│   │││
│   └────── 属主的权限(rwx = 可读+可写+可执行)
│
└─ 文件类型(d=目录, -=普通文件, l=链接)
```

**权限字母速记**：
- **r** = Read（可读）—— 可以看文件内容
- **w** = Write（可写）—— 可以修改/删除文件
- **x** = eXecute（可执行）—— 可以运行这个程序（对于目录=可以进入）
- **-** = 没有这个权限

**数字权限（今天先知道有这回事）：**
```
r = 4,  w = 2,  x = 1
rwx = 4+2+1 = 7  （全部权限）
rw- = 4+2+0 = 6  （读写）
r-- = 4+0+0 = 4  （只读）
```

---

### 4.3 绝对路径 vs 相对路径

**绝对路径**：从根目录 `/` 开始写的完整路径
```
/home/kali/Desktop/test.txt
以 / 开头 → 这是绝对路径 → 无论你在哪里，写这个路径都能找到文件
```

**相对路径**：从你当前所在位置开始写
```
假设你现在在 /home/kali/
Desktop/test.txt     ← 相对路径（不以/开头）
./Desktop/test.txt   ← 同上，./ 表示"当前目录"
../kali/Desktop/test.txt ← ../ = 上级目录
```

**类比**：
- 绝对路径 = GPS定位："中国北京市海淀区中关村大街1号"（无论谁都能找到）
- 相对路径 = 口头指路："往前走到路口左转，再走200米"（取决于你站在哪）

---

## 🔧 实操环节

> ⚠️ 重要提醒：今天涉及删除命令 `rm`，请在操作前确认你在正确的目录。用 `pwd` 确认位置。

### 准备工作：创建练习目录

```bash
# 先"回家"，然后创建一个练习文件夹
cd ~
# 回到 /home/kali

mkdir cybersec-practice
# make directory = 创建文件夹
# 创建一个名叫 cybersec-practice 的文件夹

cd cybersec-practice
# 进入练习文件夹

pwd
# 确认你在 /home/kali/cybersec-practice
# 今天所有操作都在这个文件夹里，不会影响系统文件！
```

### 命令1：touch ——创建一个空文件

```bash
touch note.txt
# touch：创建一个空的文件（如果文件已存在，更新它的修改时间）
# 创建了一个叫 note.txt 的空文件

touch file1.txt file2.txt file3.txt
# touch可以一次创建多个文件

ls
# 看看创建了什么
# 输出：file1.txt  file2.txt  file3.txt  note.txt
```

### 命令2：mkdir ——创建文件夹

```bash
mkdir my-folder
# 创建一个叫 my-folder 的文件夹

mkdir -p a/b/c
# -p = parents（自动创建所有父级目录）
# 创建了 a/ 文件夹，a里面有b/，b里面有c/
# 没有-p的话，如果a不存在，直接mkdir a/b/c会报错

ls -R
# -R = Recursive（递归），连子文件夹内容一起显示
# 你会看到 a/ 里面有 b/，b/ 里面有 c/
```

### 命令3：cp ——复制文件

```bash
cp note.txt note-backup.txt
# cp = copy（复制）
# 格式：cp 源文件 目标文件
# 把 note.txt 复制一份，副本叫 note-backup.txt

cp note.txt my-folder/
# 把 note.txt 复制到 my-folder 文件夹里面
# 目标写成目录路径，文件会保持原名复制进去

cp -r my-folder my-folder-backup
# -r = recursive（递归复制，用于复制整个文件夹）
# 把 my-folder 文件夹整个复制一份
```

### 命令4：mv ——移动/重命名文件

```bash
mv note-backup.txt renamed-note.txt
# mv = move（移动）
# 格式：mv 源文件 目标文件
# 如果目标是文件名 → 重命名（把note-backup.txt改名为renamed-note.txt）

mv renamed-note.txt my-folder/
# 如果目标是文件夹 → 移动（把renamed-note.txt移进my-folder/）

# ⚠️ 如果mv的目标文件名已经存在，会覆盖！小心使用！
```

### 命令5：rm ——删除文件（危险操作！）

```bash
# ⚠️ 注意：Linux没有"回收站"，删了就真没了！

rm file1.txt
# rm = remove（删除）
# 删除file1.txt
# 终端不会问你"确定要删除吗？"——直接删！

rm -i file2.txt
# -i = interactive（交互模式）
# 删除前会问：rm: remove regular empty file 'file2.txt'?
# 输入 y = yes（确认），输入 n = no（取消）
# 建议新手养成加 -i 的习惯

rm -r a/
# -r = recursive（递归删除文件夹）
# 删除 a/ 文件夹及其所有内容

# ⚠️ 危险命令警告！永远不要执行以下命令：
# sudo rm -rf /      ← 这会删除整个系统！！
# sudo rm -rf /*     ← 同上！！
# 等你学深了会理解为什么这很危险，现在记住：不要乱用sudo rm！
```

### 命令6：cat ——查看文件内容

```bash
cat note.txt
# cat = concatenate（连接/显示文件内容）
# 显示note.txt的内容
# （现在是空的，因为我们用touch创建的）

echo "Hello, Cybersecurity World!" > hello.txt
# echo：输出文字
# >：重定向——把输出写入文件（覆盖写入）
# 这行命令创建了hello.txt并写入了内容

cat hello.txt
# 输出：Hello, Cybersecurity World!

echo "This is line 2" >> hello.txt
# >>：追加写入（不覆盖原有内容，加在末尾）

cat hello.txt
# 输出：
# Hello, Cybersecurity World!
# This is line 2
```

### 额外技能：用man命令自学

```bash
man ls
# man = manual（手册）
# 打开ls命令的完整说明文档
# 按 空格键 翻页
# 按 q 退出
# 按 / 可以搜索（输入关键词按回车）

# 学会用man，你就可以自己探索任何命令的参数了！
# 这也是一份优秀的安全英文阅读材料
```

---

## 📋 今日知识点总结

| 编号 | 知识点 | 命令/概念 | 一句话说明 |
|------|--------|-----------|-----------|
| 1 | 一切皆文件 | — | Linux里所有东西都抽象成"文件" |
| 2 | 文件权限 | rwx | r=读(4), w=写(2), x=执行(1) |
| 3 | 绝对路径 | `/home/kali/file` | 从/开始，写全路径 |
| 4 | 相对路径 | `./file` | 从当前位置开始 |
| 5 | touch | `touch file` | 创建空文件 |
| 6 | mkdir | `mkdir -p a/b` | 创建文件夹，-p自动创建父级 |
| 7 | cp | `cp 源 目标` | 复制文件，-r复制文件夹 |
| 8 | mv | `mv 源 目标` | 移动或重命名 |
| 9 | rm | `rm -i file` | 删除，新手加-i确认 |
| 10 | cat | `cat file` | 查看文件内容 |
| 11 | man | `man 命令` | 查看命令帮助手册 |

---

## 📝 今日迷你练习

```
1. 在 ~/cybersec-practice/ 下创建文件夹 project/src/
2. 在 project/src/ 下创建文件 main.py（用touch）
3. 用 echo 向 main.py 写入 print("Hello Security")
4. 用 cat 查看 main.py 确认内容写入成功
5. 复制 main.py 到 project/ 目录下
6. 将 project/ 下的 main.py 改名为 backup.py
7. 删除 cybersec-practice/ 下的 file3.txt（如果有的话）
```

> 答案在实操中自行验证——用 `ls -R` 和 `cat` 检查每一步的结果。

---

## 🔗 配套资源

| 资源名称 | 获取方式 |
|----------|---------|
| Linux命令行入门（英文） | 搜索 "Linux Command Line for Beginners" |
| man手册中文翻译 | 终端输入 `sudo apt install manpages-zh`（安装中文man） |
| 在线Linux终端模拟器 | 搜索 "JSLinux" 或 "Webminal"（方便没开虚拟机时练习） |

---

## ✅ 完成检查

- [ ] 理解了"一切皆文件"的含义
- [ ] 理解了文件权限 rwx 的含义
- [ ] 能区分绝对路径和相对路径
- [ ] 独立完成了 touch、mkdir、cp、mv、rm、cat 的操作
- [ ] 用过至少一次 man 命令查帮助
- [ ] 完成今日迷你练习

---

> 📂 **明天预告**：Day05——Vim编辑器入门与文本处理命令（grep、sort、uniq、wc）
