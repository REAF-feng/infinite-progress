---
name: unit-test
description: 单元测试 — 为 Python/C/Flask 代码编写 pytest 单元测试和集成测试，覆盖正常路径和边界情况
allowed-tools: [Read, Glob, Grep, Write, Edit, Bash]
---

# 单元测试 (Unit Testing)

你是本项目的专属测试工程师。为代码编写高质量的自动化测试。

## 支持的技术栈

- **Python**：pytest（推荐）、unittest
- **Flask**：pytest + Flask test client
- **C 语言**：基于 assert 的单元测试、自定义测试框架
- **HTML/JS**：手动测试清单（自动化需要额外工具）

## 测试框架选择

| 场景 | 推荐工具 | 原因 |
|------|---------|------|
| Python 纯函数 | pytest | 简洁、参数化强 |
| Flask API | pytest + `app.test_client()` | 无需启动服务器 |
| Flask 模板 | pytest + `app.test_client()` + HTML 断言 | 验证返回内容 |
| C 函数 | assert 宏 + 测试驱动 main | 无额外依赖 |
| HTML/JS 交互 | 手动测试清单 | 当前项目无 JS 测试框架 |

## 测试覆盖要求

### 必须覆盖（优先级最高）
1. **正常路径**：每个函数的主要用法（happy path）
2. **边界值**：空列表、0、负数、空字符串、None
3. **异常输入**：错误类型、超范围值、格式错误
4. **资源边界**：文件不存在、权限不足、磁盘满

### Python 测试模板

```python
# test_app.py
import pytest
from app import app  # Flask 应用实例


@pytest.fixture
def client():
    """创建测试客户端"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestCheckinAPI:
    """打卡 API 测试套件"""

    def test_checkin_success(self, client):
        """测试正常打卡"""
        response = client.post('/api/checkin', json={
            'subject': 'python',
            'study_time_min': 30,
            'self_score': 4,
            'notes': '学习了函数基础'
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'streak' in data

    def test_checkin_invalid_subject(self, client):
        """测试无效科目被拒绝"""
        response = client.post('/api/checkin', json={
            'subject': 'invalid_subject',
            'study_time_min': 30,
            'self_score': 4,
            'notes': ''
        })
        assert response.status_code == 400

    @pytest.mark.parametrize('study_time', [0, -1, 99999])
    def test_checkin_edge_times(self, client, study_time):
        """测试边界学习时长"""
        response = client.post('/api/checkin', json={
            'subject': 'python',
            'study_time_min': study_time,
            'self_score': 3,
            'notes': ''
        })
        # 验证不会崩溃，返回合理状态码
        assert response.status_code in [200, 400]
```

### C 语言测试模板

```c
#include <assert.h>
#include <string.h>

/** 测试套件：字符串函数 */
void test_string_functions() {
    // 测试正常情况
    char buf[100] = {0};
    int result = string_copy(buf, "hello", sizeof(buf));
    assert(result == 0);
    assert(strcmp(buf, "hello") == 0);

    // 测试空字符串
    result = string_copy(buf, "", sizeof(buf));
    assert(result == 0);
    assert(strcmp(buf, "") == 0);

    // 测试缓冲区溢出保护
    result = string_copy(buf, "this is a very long string...", 10);
    assert(result == -1);  // 应拒绝并返回错误
}

int main(void) {
    test_string_functions();
    printf("All tests passed!\n");
    return 0;
}
```

## 测试流程

### 第一步：分析测试目标
1. 识别所有需要测试的函数/路由
2. 确定每个函数的输入域（正常值、边界值、异常值）
3. 识别外部依赖（数据库、文件系统、网络）并确定是否需要 mock

### 第二步：编写测试
1. 先写 happy path 测试（验证最基本功能）
2. 再写边界测试（空、零、最大值等）
3. 最后写异常测试（错误输入的处理）

### 第三步：运行与报告
```bash
# Python pytest
cd D:\无限进步
.venv\Scripts\python -m pytest test_*.py -v

# C 测试
gcc -o test_runner test_*.c && ./test_runner
```

### 输出格式

```
## 🧪 测试方案

### 测试目标
| 被测函数/路由 | 测试数 | 覆盖类型 |
|-------------|--------|---------|
| ... | N | 正常/边界/异常 |

### 生成的测试文件
- test_xxx.py
- ...

### 测试结果
（运行后输出）
```
