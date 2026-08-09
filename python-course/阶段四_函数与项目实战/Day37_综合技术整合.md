# Day 37：综合技术整合——函数 + 文件 + JSON + 异常处理

---

## 🎯 本节课学习目标

- 把函数、文件、JSON、异常处理整合到一个程序中
- 学习"三层架构"思维：数据层→逻辑层→界面层
- 为最终大项目打基础

---

## 📖 知识点讲解

### 1. 三层架构（程序设计的黄金模板）

```
┌─────────────────────┐
│   界面层 (UI)        │  ← 负责和用户交互（input/print）
├─────────────────────┤
│   逻辑层 (Service)   │  ← 负责处理业务规则（计算/判断）
├─────────────────────┤
│   数据层 (Data)      │  ← 负责数据的存取（文件读写/JSON）
└─────────────────────┘
```

**好处：** 各层互不干扰。比如把文件存储改成数据库，只需改数据层，界面层和逻辑层不用动。

### 2. 项目文件结构

```
记账本/
├── main.py          # 主入口（界面层）
├── service.py       # 业务逻辑
└── data.py          # 数据存取层
```

---

## 💻 完整代码：三合一通讯录

```python
"""
通讯录管理系统 —— 三层架构演示
data.py   : 数据存取层
service.py: 业务逻辑层
main.py   : 用户界面层
"""

# ================== data.py ==================
import json
import os

DATA_FILE = "contacts.json"

def load_data():
    """从JSON文件加载通讯录数据"""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_data(contacts):
    """保存通讯录数据到JSON文件"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(contacts, f, ensure_ascii=False, indent=2)

# ================== service.py ==================
# (此处依赖data.py)

def add_contact(name, phone, email, address=""):
    """添加联系人"""
    contacts = load_data()
    # 检查是否重名
    for c in contacts:
        if c["name"] == name:
            return False, "该姓名已存在！"
    
    contact = {
        "name": name,
        "phone": phone,
        "email": email,
        "address": address
    }
    contacts.append(contact)
    save_data(contacts)
    return True, "添加成功！"

def delete_contact(name):
    """删除联系人"""
    contacts = load_data()
    for i, c in enumerate(contacts):
        if c["name"] == name:
            contacts.pop(i)
            save_data(contacts)
            return True, "删除成功！"
    return False, "未找到该联系人！"

def search_contact(keyword):
    """搜索联系人（按姓名或电话模糊匹配）"""
    contacts = load_data()
    results = []
    for c in contacts:
        if keyword in c["name"] or keyword in c["phone"]:
            results.append(c)
    return results

def get_all_contacts():
    """获取所有联系人"""
    return load_data()

def get_statistics():
    """统计信息"""
    contacts = load_data()
    return {
        "total": len(contacts),
        "has_phone": sum(1 for c in contacts if c["phone"]),
        "has_email": sum(1 for c in contacts if c["email"]),
    }

# ================== main.py ==================
# (此处依赖data.py和service.py)

def show_menu():
    print("\n" + "=" * 40)
    print("         📇 通讯录管理系统")
    print("=" * 40)
    print("  1. 添加联系人")
    print("  2. 删除联系人")
    print("  3. 查找联系人")
    print("  4. 显示全部")
    print("  5. 统计信息")
    print("  0. 退出")
    print("-" * 40)

def main():
    while True:
        show_menu()
        choice = input("请选择：").strip()
        
        if choice == "0":
            print("👋 再见！")
            break
        elif choice == "1":
            print("\n--- 添加联系人 ---")
            name = input("姓名：").strip()
            phone = input("电话：").strip()
            email = input("邮箱：").strip()
            addr = input("地址（可跳过）：").strip()
            success, msg = add_contact(name, phone, email, addr)
            print(f"{'✅' if success else '❌'} {msg}")
        
        elif choice == "2":
            name = input("要删除的联系人姓名：").strip()
            success, msg = delete_contact(name)
            print(f"{'✅' if success else '❌'} {msg}")
        
        elif choice == "3":
            keyword = input("搜索关键词：").strip()
            results = search_contact(keyword)
            if results:
                for c in results:
                    print(f"📇 {c['name']} | 📞 {c['phone']} | ✉ {c['email']}")
            else:
                print("未找到匹配的联系人")
        
        elif choice == "4":
            contacts = get_all_contacts()
            if not contacts:
                print("通讯录为空")
            else:
                for i, c in enumerate(contacts, 1):
                    print(f"{i}. {c['name']:<6} 📞{c['phone']:<13} ✉{c['email']}")
        
        elif choice == "5":
            stats = get_statistics()
            print(f"总联系人：{stats['total']}")
            print(f"有电话：{stats['has_phone']}")
            print(f"有邮箱：{stats['has_email']}")
        
        else:
            print("⚠️ 请输入0~5之间的数字！")

if __name__ == "__main__":
    main()
```

---

## 📝 本节课核心知识点总结

| 序号 | 知识点 | 一句话记忆 |
|------|--------|------------|
| 1 | 三层架构 | 界面→逻辑→数据，各管各的 |
| 2 | 模块化 | 一个文件只做一件事，易维护 |
| 3 | `os.path.exists()` | 检查文件是否存在 |
| 4 | `isinstance(data, list)` | 验证数据类型，防止脏数据 |
| 5 | `if __name__ == "__main__"` | 判断是否是直接运行此文件 |

---

## ✅ 今日课后习题

### 【进阶实操题】

**题1：** 给上面的通讯录增加"编辑联系人"功能（修改电话或邮箱）。

**题2：** 参照三层架构，把Day30的记账本重构为三个文件的版本。

---

### 【拓展思考题】

**题3：** 在三层架构基础上，增加一个"导出为Excel CSV"的功能。提示：在data.py中增加`export_csv(filename)`函数，用csv模块或直接写文本。

---

> 🎉 学会三层架构，你就脱离了"写脚本"的水平，进入"写软件"的境界！
