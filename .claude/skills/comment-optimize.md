---
name: comment-optimize
description: 注释优化 — 优化代码注释质量，删除无效注释、补充关键逻辑说明、统一注释风格，特别适配新手学习者
allowed-tools: [Read, Glob, Grep, Write, Edit, Bash]
---

# 注释优化 (Comment Optimization)

你是本项目的专属注释优化专家。针对本项目"教学+自学"的性质，注释策略需兼顾**新手友好**和**代码整洁**。

## 项目背景

本项目包含：
- **python-course/** — Python 新手教程（40天课程），代码注释需对零基础友好
- **c-language-learning-system/** — C 语言自学体系，注释需解释底层概念
- **learning-checkin-app/** — Flask 实战项目，注释需帮助理解 Web 开发流程
- **HTML 页面** — 学习工具页面，注释需解释前端交互逻辑

## 注释策略（分等级）

### 等级 1 — 教学代码（python-course/ 和 c-language-learning-system/code/）

教学代码的注释策略是"**宁可多写，不让困惑**"：

```python
# ✅ 好的教学注释
# 创建一个空列表用于存储成绩
# 列表（list）是 Python 中的一种容器，用 [] 表示
scores = []

# 遍历每个学生的分数，i 是索引（从 0 开始）
for i in range(len(students)):
    # 计算当前学生的平均分
    # sum() 是内置函数，求和；len() 返回长度
    avg = sum(scores[i]) / len(scores[i])
```

### 等级 2 — 实战项目（learning-checkin-app/）

实战项目的注释策略是"**解释设计意图，而非复述代码**"：

```python
# ✅ 好的实战注释
@app.route('/api/checkin', methods=['POST'])
def api_checkin():
    """提交每日打卡 — 这是核心 API，前端四个学习页面都调用它"""
    # 从请求体中解析 JSON 数据
    data = request.get_json()

    # 安全检查：只允许白名单中的科目，防止非法数据写入数据库
    if subject not in ['english', 'typing', 'c_lang', 'python']:
        return jsonify({'success': False, 'error': '无效的科目'}), 400

    # ❌ 不好的注释（复述代码）
    # 调用 do_checkin 函数并传入参数
    do_checkin(subject, ...)
```

### 等级 3 — 工具脚本和 HTML 页面

```html
<!-- ✅ 好的 HTML 注释 -->
<!-- 
  打字训练模块
  核心流程: 加载文本 → 倒计时开始 → 用户输入 → 实时比对 → 计算WPM/准确率 → 保存成绩
  关键函数: startTimer(), checkInput(), calculateScore()
-->
<div id="typing-module" class="module">
```

## 注释优化的六个维度

### 1. 删除无效注释（-）
```python
# ❌ 删除
x = x + 1  # 将 x 加 1（废话）

# ❌ 删除：注释掉的旧代码
# old_function()

# ❌ 删除：误导性注释
# 这个函数返回 True  # 实际上可能返回 None
```

### 2. 补充缺失注释（+）
```python
# ✅ 补充：非显而易见的逻辑
# 这里用 // 而不是 /，因为需要整除（舍去小数部分）
pages = total_items // items_per_page

# ✅ 补充：为什么这样做
# 使用 copy() 创建副本，避免修改原列表影响其他函数
working_list = original_list.copy()
```

### 3. TODO/FIXME 标注
```python
# TODO: 后续需要添加分页功能，目前只返回前 100 条
# FIXME: 当 words.json 不存在时会崩溃，需要加异常处理
# HACK: 临时用 sleep(1) 等待数据库写入完成，后续改用回调
# NOTE: 这个函数的参数格式与数据库字段一一对应，修改时需同步
```

### 4. 统一注释风格
- Python：统一使用 `# ` 行注释 + docstring
- C：统一使用 `/** */` 块注释 + `//` 行注释
- HTML：统一使用 `<!-- -->` 块注释

### 5. 注释翻译
对于本项目的中文学习者，关键英文术语在注释中给出中文说明：
```c
/** 
 * Allocates memory for a new node on the heap.
 * 在堆上为新节点分配内存（malloc = memory allocation）
 */
Node* create_node(int value) {
```

### 6. 示例注释
对于复杂函数，在 docstring 中加入实际的输入输出示例（非常适合新手）：
```python
def format_study_time(minutes):
    """将学习时长格式化为可读字符串。

    Args:
        minutes (int): 分钟数

    Returns:
        str: 格式化后的字符串

    Example:
        >>> format_study_time(90)
        '1小时30分钟'
        >>> format_study_time(0)
        '0分钟'
        >>> format_study_time(45)
        '45分钟'
    """
```

## 执行流程

1. **扫描**：列出目标范围内所有源码文件
2. **分类**：将每个文件归入上述三个等级之一
3. **检查**：对每个文件按六个维度检查
4. **报告**：列出问题清单，标注优先级
5. **执行**：用户确认后逐文件修改

## 输出格式

```
## 📝 注释优化报告

### 文件: xxx.py（等级1 — 教学代码）
| 行号 | 问题类型 | 当前状态 | 建议修改 |
|------|---------|---------|---------|
| 15   | 缺失注释 | 无注释 | 补充循环逻辑说明 |
| 20   | 无效注释 | # 定义一个变量 | 删除废话注释 |
| 35   | TODO   | —       | 添加 TODO: 补充错误处理 |

### 总体统计
- 删除无效注释: N 处
- 补充缺失注释: N 处
- 添加 TODO/FIXME: N 处
- 统一风格: N 处
- 翻译术语: N 处
- 补充示例: N 处
```
