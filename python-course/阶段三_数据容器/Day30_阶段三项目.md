# Day 30：阶段三综合项目——个人记账本（控制台版）

---

## 🎯 本节课学习目标

- 综合运用列表、字典、字符串处理
- 独立完成一个完整的"记账本"程序
- 为阶段四的函数和文件读写版做好准备

---

## 📖 项目需求

做一个**个人记账本**，支持：
1. 记录收入（金额、类别、备注、日期）
2. 记录支出（金额、类别、备注、日期）
3. 查看所有账目（按日期排序）
4. 按月统计（显示该月总收入和总支出）
5. 按类别统计
6. 当前余额查询

---

## 💻 完整代码

```python
# =========================================
# 个人记账本 —— 阶段三综合项目
# 知识点：列表, 字典, 字符串, for, while, if
# =========================================

from datetime import datetime    # 获取当前日期

records = []    # 所有账目记录，每条是一个字典
                # 格式：{"type": "收入/支出", "amount": 金额,
                #        "category": 类别, "note": 备注, "date": 日期}

# ========== 辅助函数 ==========

def get_current_date():
    """获取当前日期，格式：2026-01-15"""
    return datetime.now().strftime("%Y-%m-%d")

def show_balance():
    """计算并显示当前余额"""
    income = sum(r["amount"] for r in records if r["type"] == "收入")
    expense = sum(r["amount"] for r in records if r["type"] == "支出")
    balance = income - expense
    print(f"\n💰 总收入：{income:.2f}元")
    print(f"💸 总支出：{expense:.2f}元")
    print(f"💎 当前余额：{balance:.2f}元")

# ========== 添加记录 ==========

def add_record(record_type):
    """添加一条收入或支出记录"""
    print(f"\n=== 添加{record_type} ===")
    
    # 输入金额（带验证）
    while True:
        try:
            amount = float(input("金额："))
            if amount > 0:
                break
            print("⚠️ 金额必须大于0！")
        except ValueError:
            print("⚠️ 请输入数字！")
    
    # 选择类别
    if record_type == "收入":
        categories = ["工资", "奖金", "兼职", "理财", "其他"]
    else:
        categories = ["餐饮", "交通", "购物", "住房", "娱乐", "医疗", "教育", "其他"]
    
    print("类别：")
    for i, cat in enumerate(categories, 1):
        print(f"  {i}. {cat}")
    
    while True:
        try:
            choice = int(input("请选择类别（输入数字）："))
            if 1 <= choice <= len(categories):
                category = categories[choice - 1]
                break
            print(f"⚠️ 请输入1~{len(categories)}！")
        except ValueError:
            print("⚠️ 请输入数字！")
    
    note = input("备注（可跳过）：")
    if not note:
        note = "无"
    
    date = input(f"日期（直接回车则为今天 {get_current_date()}）：")
    if not date:
        date = get_current_date()
    
    # 创建记录并添加到列表
    record = {
        "type": record_type,
        "amount": amount,
        "category": category,
        "note": note,
        "date": date
    }
    records.append(record)
    print(f"✅ 已记录：{record_type} {amount:.2f}元 [{category}]")

# ========== 查看记录 ==========

def view_records():
    """查看所有账目（按日期排序）"""
    if not records:
        print("\n📭 暂无账目记录")
        return
    
    # 按日期排序
    sorted_records = sorted(records, key=lambda r: r["date"])
    
    print(f"\n{'日期':<12}{'类型':<6}{'金额':<10}{'类别':<8}{'备注'}")
    print("-" * 60)
    for r in sorted_records:
        emoji = "💰" if r["type"] == "收入" else "💸"
        print(f"{r['date']:<12}{emoji}{r['type']:<4}"
              f"¥{r['amount']:<8.2f}{r['category']:<8}{r['note']}")

# ========== 统计功能 ==========

def monthly_stats():
    """按月统计"""
    if not records:
        print("\n📭 暂无账目记录")
        return
    
    month = input("\n请输入要统计的月份（格式：2026-01）：")
    
    month_income = 0
    month_expense = 0
    for r in records:
        if r["date"].startswith(month):    # 日期以"2026-01"开头
            if r["type"] == "收入":
                month_income += r["amount"]
            else:
                month_expense += r["amount"]
    
    print(f"\n=== {month} 月度报告 ===")
    print(f"收入：¥{month_income:.2f}")
    print(f"支出：¥{month_expense:.2f}")
    print(f"结余：¥{month_income - month_expense:.2f}")

def category_stats():
    """按类别统计"""
    if not records:
        print("\n📭 暂无账目记录")
        return
    
    # 用字典统计每个类别的支出
    cat_totals = {}
    for r in records:
        if r["type"] == "支出":
            cat = r["category"]
            cat_totals[cat] = cat_totals.get(cat, 0) + r["amount"]
    
    if not cat_totals:
        print("\n暂无支出记录")
        return
    
    sorted_cats = sorted(cat_totals.items(), key=lambda x: x[1], reverse=True)
    print(f"\n=== 支出类别排行 ===")
    for cat, total in sorted_cats:
        bar = "█" * int(total / max(cat_totals.values()) * 20)
        print(f"  {cat:<6} ¥{total:<8.2f} {bar}")

# ========== 主程序 ==========

print("=" * 40)
print("     💰 个人记账本")
print("=" * 40)

while True:
    print("\n" + "-" * 40)
    print("1. 记一笔收入    2. 记一笔支出")
    print("3. 查看所有账目  4. 查看余额")
    print("5. 月度统计      6. 类别统计")
    print("0. 退出")
    print("-" * 40)
    
    choice = input("请选择功能：")
    
    if choice == "0":
        print("\n👋 再见！记得常来记账哦~")
        break
    elif choice == "1":
        add_record("收入")
    elif choice == "2":
        add_record("支出")
    elif choice == "3":
        view_records()
    elif choice == "4":
        show_balance()
    elif choice == "5":
        monthly_stats()
    elif choice == "6":
        category_stats()
    else:
        print("⚠️ 请输入0~6之间的数字！")
```

---

## 📝 代码知识点拆解

| 功能 | 用到的核心技术 |
|------|---------------|
| 数据存储 | 列表套字典 `[{...}, {...}]` |
| 金额验证 | `try...except ValueError` |
| 类别选择 | 枚举 `enumerate(categories, 1)` |
| 余额计算 | `sum()` + 列表推导式 |
| 日期筛选 | `str.startswith(month)` |
| 排序显示 | `sorted(key=lambda...)` |
| 分类统计 | `dict.get(key, 0)` 累加 |

---

## ✅ 今日课后习题

### 【基础巩固题】

**题1：** 给记账本增加"删除记录"功能（按序号删除）。

### 【进阶实操题】

**题2：** 给记账本增加"导出CSV"功能——将所有记录输出为逗号分隔的文本格式，可以直接复制到Excel。格式如：`日期,类型,金额,类别,备注`

### 【拓展思考题】

**题3：** 当前记账本所有数据都存在内存里，关掉程序就没了。想一想，如果要长期保存数据，应该怎么做？（预习Day35文件读写）

---

> 🎉 恭喜完成阶段三！从现在起，你已经可以写出真正有用的程序了！
