# Day 40：终极项目（下）——UI界面 + 整合 + 结课总结

---

## 🎯 本节课学习目标

- 完成UI界面层，让记账本完整运行
- 整合前三层的所有代码
- 回顾40天学习旅程，明确下一步方向

---

## 💻 代码实现：ui.py

```python
"""界面显示工具"""
from models import CURRENCY

def print_header(title):
    """打印标题栏"""
    print()
    print("=" * 50)
    print(f"  {title}")
    print("=" * 50)

def print_table(headers, rows, col_widths=None):
    """打印通用表格"""
    if not col_widths:
        col_widths = [max(len(str(h)), 10) for h in headers]
    
    # 打印表头
    header_line = "".join(f"{h:<{w}}" for h, w in zip(headers, col_widths))
    print(header_line)
    print("-" * sum(col_widths))
    
    # 打印数据行
    for row in rows:
        row_line = "".join(f"{str(c):<{w}}" for c, w in zip(row, col_widths))
        print(row_line)

def print_progress_bar(label, percent, width=30):
    """打印进度条"""
    filled = int(width * percent / 100)
    bar = "█" * filled + "░" * (width - filled)
    print(f"  {label}: {bar} {percent:.1f}%")

def print_alert(message, level="info"):
    """打印提示信息"""
    emojis = {"info": "ℹ️", "success": "✅", "warning": "⚠️", "error": "❌"}
    print(f"\n{emojis.get(level, '')} {message}")

def confirm_action(prompt="确定要执行此操作吗？"):
    """确认操作"""
    while True:
        answer = input(f"{prompt} (y/n): ").strip().lower()
        if answer in ["y", "yes"]:
            return True
        elif answer in ["n", "no"]:
            return False
        print("请输入 y 或 n")
```

---

## 💻 代码实现：main.py（主程序，完整可运行）

```python
"""个人记账本 —— 主程序"""
import os
import sys
from datetime import datetime

# 初始化数据
from data_manager import init_data_dir, backup_records, export_csv
from service import (
    add_record, get_all_records, get_records_by_month,
    get_records_by_category, delete_record, get_balance,
    get_monthly_stats, check_budget, set_budget
)
from models import INCOME_CATEGORIES, EXPENSE_CATEGORIES, CURRENCY
from ui import print_header, print_table, print_progress_bar, print_alert, confirm_action

# 程序启动时初始化
init_data_dir()

def input_amount(prompt="金额："):
    """安全输入金额"""
    while True:
        try:
            amount = float(input(prompt))
            if amount <= 0:
                print_alert("金额必须大于0！", "warning")
                continue
            return amount
        except ValueError:
            print_alert("请输入有效数字！", "warning")

def select_category(categories):
    """选择类别"""
    for i, cat in enumerate(categories, 1):
        print(f"  {i}. {cat}")
    while True:
        try:
            choice = int(input("请选择（输入编号）："))
            if 1 <= choice <= len(categories):
                return categories[choice - 1]
            print_alert(f"请输入1~{len(categories)}！", "warning")
        except ValueError:
            print_alert("请输入数字！", "warning")

def menu_add_income():
    """添加收入"""
    print_header("💰 记录收入")
    amount = input_amount("收入金额：")
    category = select_category(INCOME_CATEGORIES)
    note = input("备注（可跳过）：").strip()
    record = add_record("收入", amount, category, note)
    print_alert(f"已记录：收入 {CURRENCY}{amount:.2f} [{category}]", "success")

def menu_add_expense():
    """添加支出"""
    print_header("💸 记录支出")
    amount = input_amount("支出金额：")
    category = select_category(EXPENSE_CATEGORIES)
    note = input("备注（可跳过）：").strip()
    record = add_record("支出", amount, category, note)
    print_alert(f"已记录：支出 {CURRENCY}{amount:.2f} [{category}]", "success")
    
    # 检查预算
    budget_info = check_budget()
    if budget_info["is_over"]:
        print_alert(f"⚠️ 本月已超出预算！预算{CURRENCY}{budget_info['budget']:.0f}，"
                    f"已花{CURRENCY}{budget_info['spent']:.2f}", "warning")
    elif budget_info["percent"] > 80:
        print_alert(f"提醒：本月预算已使用{budget_info['percent']:.1f}%，"
                    f"剩余{CURRENCY}{budget_info['remaining']:.2f}", "info")

def menu_view_records():
    """查看账单"""
    while True:
        print_header("📋 查看账单")
        print("  1. 全部账单")
        print("  2. 按月份查看")
        print("  3. 按类别查看")
        print("  0. 返回")
        
        choice = input("请选择：").strip()
        
        if choice == "0":
            return
        elif choice == "1":
            records = get_all_records()
            if not records:
                print_alert("暂无记录", "info")
            else:
                headers = ["编号", "日期", "类型", "金额", "类别", "备注"]
                rows = [[r["id"], r["date"], r["type"], 
                        f"{CURRENCY}{r['amount']:.2f}", r["category"], r["note"]] 
                        for r in records[:50]]  # 最多显示50条
                print_table(headers, rows)
                print(f"\n共{len(records)}条记录（显示前50条）")
        elif choice == "2":
            month_str = input("请输入月份（如 2026-01）：").strip()
            try:
                year, month = map(int, month_str.split("-"))
                records = get_records_by_month(year, month)
                print_header(f"{year}年{month}月账单")
                for r in records:
                    emoji = "💰" if r["type"] == "收入" else "💸"
                    print(f"  {r['date']} {emoji} {CURRENCY}{r['amount']:.2f} [{r['category']}] {r['note']}")
                print(f"  共{len(records)}条记录")
            except ValueError:
                print_alert("格式错误！请输入如 2026-01", "error")
        elif choice == "3":
            print("类别：")
            all_cats = INCOME_CATEGORIES + EXPENSE_CATEGORIES
            for i, cat in enumerate(all_cats, 1):
                print(f"  {i}. {cat}")
            cat_choice = input("选择类别编号（或直接输入类别名）：").strip()
            # 简化处理
            records = get_records_by_category(cat_choice)
            if not records:
                # 尝试数字
                try:
                    idx = int(cat_choice) - 1
                    cat_choice = all_cats[idx]
                    records = get_records_by_category(cat_choice)
                except:
                    pass
            if records:
                for r in records:
                    print(f"  {r['date']} {CURRENCY}{r['amount']:.2f} {r['note']}")
                print(f"  共{len(records)}条记录")
            else:
                print_alert("未找到该类别记录", "info")
        else:
            print_alert("请输入0~3", "warning")

def menu_statistics():
    """统计分析"""
    while True:
        print_header("📊 统计分析")
        print("  1. 当前余额")
        print("  2. 本月统计")
        print("  3. 预算管理")
        print("  0. 返回")
        
        choice = input("请选择：").strip()
        
        if choice == "0":
            return
        elif choice == "1":
            balance, income, expense = get_balance()
            print(f"\n  💰 总收入：{CURRENCY}{income:.2f}")
            print(f"  💸 总支出：{CURRENCY}{expense:.2f}")
            print(f"  💎 当前余额：{CURRENCY}{balance:.2f}")
        elif choice == "2":
            now = datetime.now()
            stats = get_monthly_stats(now.year, now.month)
            print(f"\n  📅 {now.year}年{now.month}月统计")
            print(f"  收入：{CURRENCY}{stats['income']:.2f}")
            print(f"  支出：{CURRENCY}{stats['expense']:.2f}")
            print(f"  结余：{CURRENCY}{stats['balance']:.2f}")
            print(f"  交易笔数：{stats['transaction_count']}")
            
            if stats["category_breakdown"]:
                print("\n  支出类别分布：")
                total_expense = stats["expense"] or 1
                for cat, amt in sorted(stats["category_breakdown"].items(), 
                                       key=lambda x: x[1], reverse=True):
                    pct = amt / total_expense * 100
                    print(f"  {cat:<6} {CURRENCY}{amt:<8.2f}", end="")
                    print_progress_bar("", pct, 20)
        elif choice == "3":
            info = check_budget()
            print(f"\n  月度预算：{CURRENCY}{info['budget']:.0f}")
            print(f"  已花费：{CURRENCY}{info['spent']:.2f}")
            print(f"  剩余：{CURRENCY}{info['remaining']:.2f}")
            print_progress_bar("使用率", min(info["percent"], 100))
            
            if input("\n修改预算？(y/n)：").strip().lower() == "y":
                new_budget = input_amount("新预算金额：")
                set_budget(new_budget)
                print_alert(f"预算已更新为{CURRENCY}{new_budget:.0f}", "success")
        else:
            print_alert("请输入0~3", "warning")

def menu_tools():
    """工具箱"""
    print_header("🔧 工具箱")
    print("  1. 备份数据")
    print("  2. 导出CSV")
    print("  3. 删除记录")
    print("  0. 返回")
    
    choice = input("请选择：").strip()
    
    if choice == "1":
        if confirm_action("确定备份当前数据？"):
            path = backup_records()
            print_alert(f"备份成功！文件：{path}", "success")
    elif choice == "2":
        path = export_csv()
        print_alert(f"导出成功！文件：{path}（可用Excel打开）", "success")
    elif choice == "3":
        record_id = input("输入要删除的记录编号：").strip()
        try:
            rid = int(record_id)
            if confirm_action(f"确定删除编号为{rid}的记录？"):
                if delete_record(rid):
                    print_alert("删除成功！", "success")
                else:
                    print_alert("未找到该记录", "error")
        except ValueError:
            print_alert("请输入有效编号", "warning")

def main():
    """主函数"""
    print_header("💰 个人记账本 v1.0")
    print("  记录每一笔，掌控你的财富！")
    
    # 检查预算
    budget_info = check_budget()
    if budget_info["percent"] >= 100:
        print_alert(f"⚠️ 本月预算已用完！已支出{CURRENCY}{budget_info['spent']:.2f}", "warning")
    
    while True:
        print()
        balance, _, _ = get_balance()
        print(f"💎 当前余额：{CURRENCY}{balance:.2f}  |  ", end="")
        print(f"1.收入 2.支出 3.账单 4.统计 5.工具 0.退出")
        print("-" * 50)
        
        choice = input("请选择：").strip()
        
        if choice == "0":
            if confirm_action("确定退出？"):
                print("\n👋 感谢使用，再见！")
                break
        elif choice == "1":
            menu_add_income()
        elif choice == "2":
            menu_add_expense()
        elif choice == "3":
            menu_view_records()
        elif choice == "4":
            menu_statistics()
        elif choice == "5":
            menu_tools()
        else:
            print_alert("请输入0~5的数字", "warning")

if __name__ == "__main__":
    main()
```

---

## 🎓 40天Python学习旅程回顾

```
阶段一（Day 1-10）  入门基础      变量、类型、输入输出、运算符、if、循环
阶段二（Day 11-20） 逻辑控制      嵌套判断、循环控制、异常处理、random
阶段三（Day 21-30） 数据容器      列表、元组、集合、字典、字符串、嵌套结构
阶段四（Day 31-40） 函数与实战    函数定义、参数、文件读写、JSON、项目实战
```

### 你现在能做什么？

✅ 独立写出完整的Python程序  
✅ 处理各种数据类型和文件  
✅ 设计程序架构（三层分离）  
✅ 使用Python标准库和第三方库  
✅ 从零开发一个完整的应用（记账本）  

### 下一步学什么？

| 方向 | 内容 | 推荐资源 |
|------|------|----------|
| Web开发 | Flask/Django做网站 | 《Flask Web开发》 |
| 数据分析 | Pandas/NumPy/Matplotlib | 《利用Python进行数据分析》 |
| 自动化 | Selenium/Requests/办公自动化 | 《Python编程快速上手》 |
| 游戏开发 | Pygame | pygame官网教程 |
| AI/机器学习 | Scikit-learn/TensorFlow | 《机器学习实战》 |

---

## ✅ 今日课后习题

**题1（终极挑战）：** 给记账本增加"多账户支持"——可以管理多个账户（如现金、银行卡、支付宝），每个账户独立记录收支。

**题2（终极挑战）：** 给记账本增加"图表可视化"功能——用 `matplotlib` 绘制月度收支趋势折线图。提示：`pip install matplotlib`。

---

> 🎉🎉🎉 **恭喜你完成了40天Python零基础到会的全部课程！** 🎉🎉🎉  
> 从今天起，你不再是一个"零基础小白"，而是一个**合格的Python初学者**。  
> 编程之路刚刚开始，保持每天写代码的习惯，你会越来越强！
