# Day 12：while循环进阶——输入验证与无限循环

---

## 🎯 本节课学习目标

- 用while循环实现"输入验证"（不合法就反复让用户重输）
- 掌握 `while True` + `break` 的经典模式
- 用while实现菜单循环

---

## 📖 知识点讲解

### 1. 输入验证——"不按规矩来就让你重来"

现实中的程序，用户经常会乱输入。比如要一个1~100的数字，用户偏要输入"abc"。一个健壮的程序应该检查输入，不合格就让人重来。

```python
while True:
    输入 = input("请输入...")
    if 输入合法:
        break       # 合法了，跳出循环
    else:
        print("输入不合法，请重新输入！")  # 回到while开头，再来一次
```

**这就是 `while True` + `break` 的经典模式！**

### 2. 为什么要判断输入合法性？

如果用户输入了不合法的数据而你不检查，程序会在后面的计算中崩溃。与其让程序崩溃，不如在入口处就把关。

---

## 💻 课堂演示代码

```python
# ========== 示例1：确保用户输入的是数字 ==========

while True:
    user_input = input("请输入一个正整数：")
    # .isdigit() 能检查字符串是否全是数字字符
    if user_input.isdigit():
        num = int(user_input)
        if num > 0:
            break    # 输入合法，跳出循环
        else:
            print("⚠️ 请输入大于0的数！")
    else:
        print("⚠️ 输入的不是数字，请重新输入！")

print(f"你输入的数字是：{num}")

# ========== 示例2：确保输入在指定范围内 ==========

print()
print("=== 打分系统（1~10分）===")

while True:
    try:
        score = int(input("请打分（1~10）："))
        if 1 <= score <= 10:
            break    # 在范围内，通过
        else:
            print("⚠️ 分数必须在1到10之间！")
    except ValueError:
        print("⚠️ 请输数字，不要输入字母！")

print(f"你打的分是：{score}分")

# ========== 示例3：限制尝试次数 ==========

print()
print("=== 密码验证（最多3次机会）===")
password = "python123"
max_try = 3
try_count = 0

while try_count < max_try:
    pwd = input("请输入密码：")
    try_count = try_count + 1

    if pwd == password:
        print("✅ 密码正确，登录成功！")
        break    # 猜对了，跳出循环
    else:
        left = max_try - try_count
        if left > 0:
            print(f"❌ 密码错误，还有{left}次机会")
        else:
            print("❌ 3次机会用完，账号已锁定！")

# ========== 示例4：确认操作 ==========

print()
while True:
    confirm = input("确定要删除所有数据吗？(输入 y 确认，n 取消)：")
    if confirm == "y":
        print("数据已删除")
        break
    elif confirm == "n":
        print("操作已取消")
        break
    else:
        print("⚠️ 请输入 y 或 n")
```

---

## 📝 本节课核心知识点总结

| 序号 | 知识点 | 一句话记忆 |
|------|--------|------------|
| 1 | 输入验证 | 永远不信任用户输入，先检查再用 |
| 2 | `while True` + `break` | 不知道要循环多少次的标准写法 |
| 3 | `.isdigit()` | 检查字符串是不是纯数字 |
| 4 | `try...except` | 尝试运行，出错就捕获（预习Day15） |
| 5 | 次数限制 | `while count < max:` 加计数变量 |

---

## ✅ 今日课后习题

### 【基础巩固题】

**题1：这段代码在用户输入"abc"时会怎样？修改它让它能正确处理。**
```python
num = int(input("请输入一个数字："))
print(f"你输入的是：{num}")
```

**题2：写出限制5次尝试的密码验证框架**
```python
password = "123456"
count = 0
while ______ < ______:
    pwd = input("请输入密码：")
    count = ______
    if ______:
        print("登录成功")
        ______
    else:
        print(f"错误，还剩{______}次")
```

---

### 【进阶实操题】

**题3：健壮的年龄输入器**
让用户输入年龄，要求：必须是数字、必须在0~150之间。不满足条件就一直提示重输。

**题4：猜数字游戏升级版**
随机生成1~100的数字（用 `import random; answer = random.randint(1,100)`），让用户猜，每次猜完提示大/小，统计猜了几次。还要处理用户输入非数字的情况。

---

### 【拓展思考题】

**题5：ATM取款机模拟**
模拟ATM取款流程：
1. 初始余额10000元
2. 输入取款金额，必须满足：是数字、是100的整数倍、不超过余额
3. 取款成功后显示余额，问是否继续
4. 余额为0或用户选择退出时程序结束

---

> 🎉 会做输入验证的程序才算是"生产级别"的程序！
