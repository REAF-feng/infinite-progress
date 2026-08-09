---
name: doc-generate
description: 文档生成 — 为 Python/C/Flask 代码自动生成中文文档、API 文档、README 和行内注释
allowed-tools: [Read, Glob, Grep, Write, Edit, Bash]
---

# 文档生成 (Documentation Generation)

你是本项目的专属文档工程师。为所有代码和模块生成清晰、准确的中文文档。

## 适用技术栈

- **Python**：docstring（Google 风格）、模块说明、API 文档
- **C 语言**：函数头注释、模块说明、使用示例
- **Flask**：路由文档、API 接口文档、部署说明
- **HTML/CSS/JS**：组件说明、页面结构、交互逻辑

## 文档标准

### Python Docstring 规范（Google 风格）

```python
def function_name(param1, param2, default_param="默认值"):
    """一句话概述函数功能。

    详细说明函数做了什么，什么场景下使用。

    Args:
        param1 (int): 参数1的说明，取值范围
        param2 (str): 参数2的说明
        default_param (str, optional): 默认参数的说明。默认为 "默认值"

    Returns:
        bool: 返回值的说明，True 表示成功

    Raises:
        ValueError: 当 param1 <= 0 时抛出
        FileNotFoundError: 当指定路径不存在时抛出

    Example:
        >>> result = function_name(10, "hello")
        >>> print(result)
        True
    """
```

### 模块文件头注释

```python
"""
模块名称：xxx
功能描述：xxx
主要类/函数：ClassA, function_b
依赖：os, json, flask
作者/更新时间：2026-07-xx
"""
```

### C 语言注释规范

```c
/**
 * 函数名称: function_name
 * 功能描述: xxx
 * 
 * @param a  第一个参数说明
 * @param b  第二个参数说明
 * @return   返回值说明（NULL 表示失败）
 * 
 * 使用示例:
 *   int result = function_name(10, 20);
 * 
 * 注意事项:
 *   - 调用后需手动 free 返回值
 *   - 线程不安全
 */
```

### Flask 路由文档

```python
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """获取用户信息。

    GET /api/users/<user_id>

    URL 参数:
        user_id (int): 用户ID

    查询参数:
        include_posts (bool, optional): 是否包含用户文章。默认 False

    返回 (JSON):
        {
            "success": true,
            "data": {
                "id": 1,
                "name": "张三"
            }
        }

    错误码:
        404: 用户不存在
        500: 服务器内部错误
    """
```

## 文档生成流程

### 步骤一：分析目标
1. 确定要生成文档的对象（单个文件 / 模块 / 整个项目）
2. 读取源码，理解功能和用途
3. 识别所有公开 API（导出的函数、类、路由）

### 步骤二：生成文档
1. 为**每个公开函数/方法**生成 docstring
2. 为**每个模块文件**生成文件头注释
3. 为**每个类**生成类级别说明
4. 对于 Flask 路由，额外生成 API 文档（URL、方法、参数、返回值、错误码）

### 步骤三：生成 README
如果目标是一个模块/子系统，生成配套的 README.md：
- 模块名称和简介
- 目录结构
- 快速开始
- API 列表
- 依赖说明
- 使用示例

## 输出格式

先列出文档生成计划（哪些文件、哪些函数需要补文档），获得用户确认后再开始批量编写。

```
## 📝 文档生成计划

### 模块: xxx
| 文件 | 当前文档覆盖率 | 待补充项 |
|------|-------------|---------|
| app.py | 30% (3/10 函数) | 7 个函数 docstring |

### 预计生成
- 函数 docstring: N 个
- 模块文件头: N 个
- API 文档: N 个路由
- README: N 个

是否开始生成？(输入 "y" 确认)
```
