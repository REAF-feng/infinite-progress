# Day 39：终极项目（上）——个人记账本完整版 · 设计与实现

---

## 🎯 本节课学习目标

- 运用全部40天所学知识
- 从零设计并实现一个完整的桌面应用
- 理解"需求分析→架构设计→编码实现"的全流程

---

## 📖 项目需求文档

### 功能清单

| 编号 | 功能 | 说明 |
|------|------|------|
| F1 | 记录收入 | 金额、类别（工资/奖金/兼职/理财/其他）、备注、日期 |
| F2 | 记录支出 | 金额、类别（餐饮/交通/购物/住房/娱乐/医疗/教育/其他）、备注、日期 |
| F3 | 查看账单 | 支持全部查看、按月份筛选、按类别筛选 |
| F4 | 统计分析 | 月度收支报告、类别消费占比、月度趋势 |
| F5 | 数据管理 | 数据持久化（JSON）、备份功能、数据导出CSV |
| F6 | 预算功能 | 设置月度预算、超出预算提醒 |

### 项目结构

```
记账本/
├── main.py          # 主入口，菜单界面
├── models.py        # 数据模型和常量定义
├── data_manager.py  # 数据存取层（JSON读写）
├── service.py       # 业务逻辑层
├── ui.py            # 界面显示工具
└── data/
    ├── records.json # 账目数据文件
    └── config.json  # 配置文件（预算等）
```

---

## 💻 代码实现：models.py

```python
"""数据模型和常量定义"""

# 收入类别
INCOME_CATEGORIES = ["工资", "奖金", "兼职", "理财", "其他收入"]

# 支出类别
EXPENSE_CATEGORIES = ["餐饮", "交通", "购物", "住房", "娱乐", "医疗", "教育", "其他支出"]

# 默认预算
DEFAULT_BUDGET = 3000.0

# 货币符号
CURRENCY = "¥"
```

---

## 💻 代码实现：data_manager.py

```python
"""数据存取层：负责JSON文件的读写"""
import json
import os
from datetime import datetime

DATA_DIR = "data"
RECORDS_FILE = os.path.join(DATA_DIR, "records.json")
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")

def init_data_dir():
    """初始化数据目录和文件"""
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # 初始化账目文件
    if not os.path.exists(RECORDS_FILE):
        save_records([])
    
    # 初始化配置文件
    if not os.path.exists(CONFIG_FILE):
        save_config({"monthly_budget": 3000.0, "currency": "CNY"})

def load_records():
    """加载所有账目记录"""
    try:
        with open(RECORDS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_records(records):
    """保存账目记录"""
    with open(RECORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

def load_config():
    """加载配置"""
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"monthly_budget": 3000.0}

def save_config(config):
    """保存配置"""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def backup_records():
    """备份当前数据"""
    records = load_records()
    backup_file = os.path.join(DATA_DIR, f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(backup_file, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    return backup_file

def export_csv(filename="export.csv"):
    """导出为CSV格式"""
    import csv
    records = load_records()
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["日期", "类型", "金额", "类别", "备注"])
        for r in records:
            writer.writerow([r["date"], r["type"], r["amount"], r["category"], r["note"]])
    return filename
```

---

## 💻 代码实现：service.py

```python
"""业务逻辑层：记账核心功能"""
from datetime import datetime
from data_manager import load_records, save_records, load_config, save_config

def add_record(record_type, amount, category, note=""):
    """添加一条账目记录"""
    records = load_records()
    record = {
        "id": len(records) + 1,
        "type": record_type,
        "amount": round(amount, 2),
        "category": category,
        "note": note if note else "无",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    records.append(record)
    save_records(records)
    return record

def get_all_records(sort_by_date=True):
    """获取所有记录"""
    records = load_records()
    if sort_by_date:
        records.sort(key=lambda r: r["date"], reverse=True)
    return records

def get_records_by_month(year, month):
    """按月份筛选记录"""
    prefix = f"{year}-{month:02d}"
    records = load_records()
    return [r for r in records if r["date"].startswith(prefix)]

def get_records_by_category(category):
    """按类别筛选"""
    records = load_records()
    return [r for r in records if r["category"] == category]

def delete_record(record_id):
    """删除记录"""
    records = load_records()
    for i, r in enumerate(records):
        if r["id"] == record_id:
            records.pop(i)
            save_records(records)
            return True
    return False

def get_balance():
    """计算当前余额"""
    records = load_records()
    income = sum(r["amount"] for r in records if r["type"] == "收入")
    expense = sum(r["amount"] for r in records if r["type"] == "支出")
    return income - expense, income, expense

def get_monthly_stats(year, month):
    """获取月度统计"""
    records = get_records_by_month(year, month)
    income = sum(r["amount"] for r in records if r["type"] == "收入")
    expense = sum(r["amount"] for r in records if r["type"] == "支出")
    
    # 按类别统计支出
    category_stats = {}
    for r in records:
        if r["type"] == "支出":
            cat = r["category"]
            category_stats[cat] = category_stats.get(cat, 0) + r["amount"]
    
    return {
        "year": year,
        "month": month,
        "income": income,
        "expense": expense,
        "balance": income - expense,
        "transaction_count": len(records),
        "category_breakdown": category_stats
    }

def check_budget():
    """检查是否超出预算"""
    now = datetime.now()
    stats = get_monthly_stats(now.year, now.month)
    config = load_config()
    budget = config.get("monthly_budget", 3000)
    
    remaining = budget - stats["expense"]
    is_over = remaining < 0
    
    return {
        "budget": budget,
        "spent": stats["expense"],
        "remaining": remaining,
        "is_over": is_over,
        "percent": (stats["expense"] / budget * 100) if budget > 0 else 0
    }

def set_budget(amount):
    """设置月度预算"""
    config = load_config()
    config["monthly_budget"] = round(amount, 2)
    save_config(config)
    return config["monthly_budget"]
```

---

## 📝 今天的内容

今天我们完成了整个项目的基础架构（models + data_manager + service），明天（Day40）我们将实现用户界面（ui.py + main.py），让整个记账本跑起来！

---

## ✅ 今日课后习题

**题1：** 仔细阅读上面三层代码，画出函数调用关系的思维导图。

**题2：** 给 `service.py` 添加一个 `get_yearly_report(year)` 函数，返回指定年份的12个月度统计汇总。

---

> 🎉 完成今天的内容，明天就是大结局了！
