# Day 19：实用小工具开发——把逻辑变成生产力

---

## 🎯 本节课学习目标

- 用所学知识开发3个实用小工具
- 强化"遇到需求→拆解逻辑→写代码"的思维
- 体会编程解决实际问题的乐趣

---

## 💻 工具1：倒计时器

```python
import time     # 导入时间模块，用来暂停

print("=== 番茄钟倒计时 ===")
minutes = int(input("请输入倒计时分钟数："))
total_seconds = minutes * 60

while total_seconds > 0:
    # 把总秒数换算成 分:秒 格式
    mins = total_seconds // 60
    secs = total_seconds % 60
    print(f"剩余时间：{mins:02d}:{secs:02d}", end="\r")  # \r让光标回到行首
    time.sleep(1)            # 暂停1秒
    total_seconds = total_seconds - 1

print("\n⏰ 时间到！该休息了！")
```

---

## 💻 工具2：存款计算器

```python
print("=== 复利存款计算器 ===")
principal = float(input("本金（元）："))       # 初始存入金额
rate = float(input("年利率（%，如3.5代表3.5%）：")) / 100
years = int(input("存款年数："))

total = principal                    # 初始总额
for year in range(1, years + 1):
    interest = total * rate          # 当年利息
    total = total + interest         # 利息加入本金
    print(f"第{year}年：本金+利息 = {total:.2f}元")

print(f"\n{years}年后，{principal}元变成{total:.2f}元")
print(f"总收益：{total - principal:.2f}元")
```

---

## 💻 工具3：简单抽奖轮盘

```python
import random

print("=== 幸运大转盘 ===")
prizes = ["一等奖：iPhone", "二等奖：耳机", "三等奖：奶茶", 
          "参与奖：贴纸", "谢谢参与", "再来一次"]

print("按回车键开始抽奖！（输入q退出）")

while True:
    command = input()
    if command == "q":
        print("退出抽奖，祝你好运！")
        break
    
    # 模拟转盘旋转效果
    print("转盘旋转中", end="")
    for i in range(3):
        print(".", end="", flush=True)
        # flush=True让文字立刻显示，不等缓冲
        for _ in range(5000000):     # 空循环，制造延迟效果
            pass
    print()
    
    result = random.choice(prizes)
    print(f"🎉 恭喜获得：{result}")
    print()
    print("再抽一次？（回车继续 / q退出）")
```

---

## 📝 本节课编程思维总结

| 步骤 | 内容 |
|------|------|
| ① 分析需求 | 这个程序要干什么？输入什么？输出什么？ |
| ② 拆解逻辑 | 一步一步怎么做？先做什么后做什么？ |
| ③ 选择工具 | 用if？用while？用for？需要import什么？ |
| ④ 逐个实现 | 一次只写一个功能，写完测试，通了再写下一个 |
| ⑤ 测试边界 | 故意输入不合理的值，看程序会不会崩 |

---

## ✅ 今日课后习题

### 【基础巩固题】

**题1：** 修改倒计时器，让它在最后10秒时发出警告提示"快结束了！"

**题2：** 修改存款计算器，让用户可以按月存款（每月固定存一笔钱），计算N个月后的总额。

---

### 【进阶实操题】

**题3：独立开发"体重记录器"**
让用户输入初始体重和目标体重，以及每周预计减重，计算需要多少周达到目标。要考虑：如果预计减重<=0，提示设置不合理。

**题4：独立开发"简易选择题测验"**
预设3道选择题（题目+选项+答案），逐题显示，用户输入答案后判断对错，最后显示得分。

---

> 🎉 学编程的终极目标就是用代码解决生活中的问题！
