# Day 20：阶段二综合项目——游戏大厅

---

## 🎯 本节课学习目标

- 综合运用if、while、for、random、异常处理
- 独立完成一个包含多个小游戏的"游戏大厅"
- 为阶段二测评做准备

---

## 📖 项目需求

做一个**游戏大厅**，包含3个游戏：
1. 猜数字（1~100，最多7次）
2. 石头剪刀布（三局两胜）
3. 口算挑战（随机出10道加减法）

用户打开程序后看到菜单，选择玩哪个游戏，玩完可以返回菜单继续玩或退出。

---

## 💻 完整代码

```python
# =========================================
# 游戏大厅 —— 阶段二综合项目
# 知识点：if, while, for, random, 异常处理
# =========================================

import random

def show_menu():
    """显示游戏菜单"""
    print()
    print("=" * 40)
    print("         🎮 欢迎来到游戏大厅！")
    print("=" * 40)
    print("  1. 猜数字")
    print("  2. 石头剪刀布")
    print("  3. 口算挑战")
    print("  0. 退出")
    print("-" * 40)

def play_guess_number():
    """游戏1：猜数字"""
    print()
    print("=== 🎯 猜数字游戏 ===")
    print("规则：电脑想了一个1~100的数，你有7次机会猜中它。")
    
    answer = random.randint(1, 100)
    max_chances = 7
    
    for chance in range(1, max_chances + 1):
        # 安全输入
        while True:
            try:
                guess = int(input(f"第{chance}次猜测："))
                if 1 <= guess <= 100:
                    break
                else:
                    print("⚠️ 请输入1~100之间的数字！")
            except ValueError:
                print("⚠️ 请输入整数！")
        
        if guess == answer:
            print(f"🎉 恭喜！你在第{chance}次猜对了！答案就是{answer}")
            return   # 结束这个函数
        elif guess > answer:
            print("📈 大了")
        else:
            print("📉 小了")
    
    # for循环正常结束（没用break），说明没猜对
    print(f"😢 机会用完了！正确答案是{answer}")

def play_rps():
    """游戏2：石头剪刀布"""
    print()
    print("=== ✂️ 石头剪刀布（三局两胜）===")
    options = ["石头", "剪刀", "布"]
    
    player_wins = 0
    computer_wins = 0
    round_num = 1
    
    while player_wins < 2 and computer_wins < 2:
        print(f"\n--- 第{round_num}局 ---")
        print("1.石头  2.剪刀  3.布")
        
        # 用户出拳
        while True:
            try:
                choice = int(input("请出拳（1/2/3）："))
                if choice in [1, 2, 3]:
                    break
                else:
                    print("⚠️ 请输入1、2或3！")
            except ValueError:
                print("⚠️ 请输入数字！")
        
        player = options[choice - 1]
        computer = random.choice(options)
        
        print(f"你出：{player}  vs  电脑出：{computer}")
        
        # 判断输赢
        if player == computer:
            print("  平局！")
        elif (player == "石头" and computer == "剪刀") or \
             (player == "剪刀" and computer == "布") or \
             (player == "布" and computer == "石头"):
            print("  你赢了这一局！")
            player_wins = player_wins + 1
        else:
            print("  电脑赢了这一局！")
            computer_wins = computer_wins + 1
        
        print(f"当前比分：你 {player_wins} : {computer_wins} 电脑")
        round_num = round_num + 1
    
    # 宣布最终结果
    if player_wins == 2:
        print("\n🎉 恭喜你赢得了比赛！")
    else:
        print("\n😢 电脑赢得了比赛，再接再厉！")

def play_math_challenge():
    """游戏3：口算挑战"""
    print()
    print("=== 🧮 口算挑战 ===")
    print("规则：10道随机加减法，每题限时回答，最后统计得分。")
    
    score = 0
    for i in range(1, 11):
        a = random.randint(1, 50)
        b = random.randint(1, 50)
        
        # 随机决定是加法还是减法
        if random.choice([True, False]):
            # 加法
            correct = a + b
            symbol = "+"
        else:
            # 减法（确保不出现负数）
            if a < b:
                a, b = b, a     # 交换，让大数在前
            correct = a - b
            symbol = "-"
        
        # 安全输入
        while True:
            try:
                user_answer = int(input(f"第{i}题：{a} {symbol} {b} = "))
                break
            except ValueError:
                print("⚠️ 请输入整数！")
        
        if user_answer == correct:
            print("  ✅ 正确！")
            score = score + 1
        else:
            print(f"  ❌ 错误，正确答案是{correct}")
    
    print(f"\n你的得分：{score}/10")
    if score == 10:
        print("🏆 满分！你是计算天才！")
    elif score >= 8:
        print("👍 很棒！")
    elif score >= 6:
        print("📚 还不错，继续练习！")
    else:
        print("💪 需要加油，多练口算哦！")

# ========== 主程序 ==========
while True:
    show_menu()
    choice = input("请选择游戏（0~3）：")
    
    if choice == "0":
        print("谢谢游玩，再见！👋")
        break
    elif choice == "1":
        play_guess_number()
    elif choice == "2":
        play_rps()
    elif choice == "3":
        play_math_challenge()
    else:
        print("⚠️ 请输入0~3之间的数字！")
```

---

## 📝 代码结构分析

```
游戏大厅
├── show_menu()          显示菜单
├── play_guess_number()  游戏1：猜数字
├── play_rps()           游戏2：石头剪刀布
├── play_math_challenge()游戏3：口算挑战
└── 主程序               while True循环显示菜单
```

---

## ✅ 今日课后习题

### 【基础巩固题】

**题1：** 在猜数字游戏中，增加"难度选择"：简单（1~50，10次机会）、普通（1~100，7次）、困难（1~200，5次）。

### 【进阶实操题】

**题2：** 给游戏大厅增加第4个游戏——"反应速度测试"：随机等待几秒后显示"按回车！"，计算用户从提示出现到按下回车的反应时间。提示：用 `time.time()` 获取时间戳。

### 【拓展思考题】

**题3：** 给猜数字游戏增加"计分系统"，记录历史最佳成绩（最少猜中次数），保存到文件里（预习Day35的内容）。

---

> 🎉 阶段二到此结束！你已经能独立做出完整的多功能程序了！
