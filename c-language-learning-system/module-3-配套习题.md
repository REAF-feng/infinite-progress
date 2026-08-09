# 模块3：分层配套编程习题（三级梯度）

> 📌 每完成一天讲义后，当天做对应的基础巩固题。进阶实操题在每个阶段结束时集中完成。综合拓展题每10天挑战一次。

---

## 使用说明

### 三级梯度体系

| 级别 | 图标 | 难度 | 完成时机 | 目标 |
|------|------|------|----------|------|
| **L1 基础巩固** | 🟢 | 简单 | 每天课后立即完成 | 夯实当日语法，形成肌肉记忆 |
| **L2 进阶实操** | 🟡 | 中等 | 每个阶段结束时 | 独立编写小型功能程序 |
| **L3 综合拓展** | 🔴 | 挑战 | 每10天挑战一次 | 跨知识点整合，锻炼逻辑调试能力 |

### 做题规则
1. **先独立做，别看答案**——至少自己尝试15分钟
2. **编译通过才算做完**——代码能运行是底线
3. **对照答案优化**——做完后和参考答案对比，学习更好的写法
4. **记录错题**——把卡住的题和报错记入 module-5 打卡模板

---

## 第一阶段：基础语法层（Day 1-7）

### 🟢 L1-1：Hello World 相关（Day 1-3）

**题1-1** 填空题：补全代码，使其输出 `I love C language!`
```c
#include <______>
int ______() {
    ______("I love C language!\n");
    ______ 0;
}
```

**题1-2** 改错题：下面的代码有3处错误，请找出并改正
```c
include <stdio.h>
int main {
    printf("Hello World\n")
    return 0;
}
```

**题1-3** 仿写题：仿照 Hello World 程序，写一个程序输出以下内容：
```
************************
*   我的第一个C程序     *
*   姓名：[你的名字]    *
*   日期：2026年7月     *
************************
```

**题1-4** 变量操作：写出以下代码的输出结果
```c
int a = 10, b = 20;
a = b;
b = 30;
printf("a=%d, b=%d\n", a, b);
```

**题1-5** 数据类型匹配：把左边的值和右边的类型连线（口述即可）
```
3.14        int
'A'         float
2026        double
3.1415926   char
100         int
```

<details>
<summary>📝 参考答案 L1-1</summary>

**题1-1**：
```c
#include <stdio.h>
int main() {
    printf("I love C language!\n");
    return 0;
}
```

**题1-2**：三处错误：
1. `include` 前缺少 `#` → `#include`
2. `int main` 缺少 `()` → `int main()`
3. `printf(...)` 缺少 `;` → `printf("Hello World\n");`

**题1-3**：略（参考Day 1的Hello World框架修改）

**题1-4**：`a=20, b=30`（a被赋值为b的旧值20，然后b变成30，但a不受影响）

**题1-5**：`3.14→float`, `'A'→char`, `2026→int`, `3.1415926→double`, `100→int`
</details>

---

### 🟢 L1-2：输入输出与运算符（Day 4-7）

**题2-1** 填空题：补全代码，从键盘读取一个整数并输出
```c
int age;
printf("请输入年龄：");
scanf("___", &age);       // 填占位符
printf("你的年龄是：___\n", age);  // 填占位符
```

**题2-2** 改错题：找出3处错误
```c
int a, b;
scanf("%d%d", a, b);   // 错误！
printf("%d + %d = %d", a, b, a+b);
```

**题2-3** 手算题：不用电脑，写出以下代码的输出
```c
int x = 10;
printf("%d\n", x++);   // ?
printf("%d\n", ++x);   // ?
printf("%d\n", x--);   // ?
printf("%d\n", --x);   // ?
```

**题2-4** 运算符练习：写出以下表达式的值
```c
int a = 7, b = 3;
// (1) a / b      = ?
// (2) a % b      = ?
// (3) a / b * b  = ?   （注意运算顺序）
// (4) (float)a / b = ?
```

**题2-5** 仿写题：写一个程序，输入圆的半径，输出圆的周长和面积（π取3.14）。

<details>
<summary>📝 参考答案 L1-2</summary>

**题2-1**：`scanf("%d", &age);` / `printf("你的年龄是：%d\n", age);`

**题2-2**：`scanf("%d%d", &a, &b);` —— a和b前缺少 `&` 取地址符！

**题2-3**：
```
10    (x++: 先输出10，x变成11)
12    (++x: x从11变12，输出12)
12    (x--: 先输出12，x变成11)
10    (--x: x从11变10，输出10)
```

**题2-4**：
```
7 / 3 = 2      （整数除法截断）
7 % 3 = 1      （7除以3余1）
2 * 3 = 6      （先除得2，再乘3得6，不等于7！）
2.333...       （浮点除法，精度保留）
```

**题2-5**：
```c
#include <stdio.h>
#define PI 3.14
int main() {
    float r;
    printf("请输入圆的半径：");
    scanf("%f", &r);
    printf("周长 = %.2f\n", 2 * PI * r);
    printf("面积 = %.2f\n", PI * r * r);
    return 0;
}
```
</details>

---

### 🟡 L2-1：第一阶段进阶实操（Day 7后完成）

**题L2-1** 温度转换器：编写程序，输入摄氏温度，输出华氏温度。
公式：华氏度 = 摄氏度 × 9/5 + 32
要求：输出保留1位小数。

**题L2-2** 三数排序：输入三个整数，按从小到大的顺序输出。
（提示：先比较找出最小、最大、中间）

**题L2-3** 简易收银台：输入商品单价和数量，计算总价。
- 满100元打9折
- 满200元打8折
- 输出：原价、折扣后价格、节省金额

<details>
<summary>📝 参考答案 L2</summary>

**题L2-1**：
```c
#include <stdio.h>
int main() {
    float celsius, fahrenheit;
    printf("请输入摄氏温度：");
    scanf("%f", &celsius);
    fahrenheit = celsius * 9.0 / 5.0 + 32;
    printf("%.1f°C = %.1f°F\n", celsius, fahrenheit);
    return 0;
}
// 易错点：用 9/5 而不是 9.0/5.0，结果是整数除法！
```

**题L2-2**：
```c
#include <stdio.h>
int main() {
    int a, b, c, temp;
    scanf("%d %d %d", &a, &b, &c);
    // 冒泡思想：确保a≤b≤c
    if (a > b) { temp = a; a = b; b = temp; }
    if (a > c) { temp = a; a = c; c = temp; }
    if (b > c) { temp = b; b = c; c = temp; }
    printf("%d %d %d\n", a, b, c);
    return 0;
}
```

**题L2-3**：
```c
#include <stdio.h>
int main() {
    float price, total;
    int quantity;
    printf("单价："); scanf("%f", &price);
    printf("数量："); scanf("%d", &quantity);
    total = price * quantity;
    float discount = 1.0;
    if (total >= 200) discount = 0.8;
    else if (total >= 100) discount = 0.9;
    printf("原价：%.2f\n", total);
    printf("实付：%.2f\n", total * discount);
    printf("节省：%.2f\n", total * (1 - discount));
    return 0;
}
```
</details>

---

### 🔴 L3-1：第一阶段综合拓展（Day 7后挑战）

**题L3-1** 数字加密器：输入一个4位整数，按以下规则加密后输出：
1. 每位数字加5，然后对10取余
2. 将第1位和第4位交换，第2位和第3位交换
例如：输入1234 → 每位加5取余得6789 → 交换得9876

---

## 第二阶段：逻辑控制层（Day 8-17）

### 🟢 L1-3：条件分支习题（Day 8-10）

**题3-1** 填空题：判断一个数是否是3的倍数
```c
if (num ___ 3 ___ 0) {   // 填两个运算符
    printf("%d是3的倍数\n", num);
}
```

**题3-2** 改错题：
```c
int score = 85;
if (score >= 90) {
    printf("A\n");
} else if (score >= 80) {
    printf("B\n");
} else (score >= 70) {    // 这里有问题！
    printf("C\n");
}
```

**题3-3** 仿写题：用switch语句实现——输入1-7，输出对应的星期几。

**题3-4** 手算题：以下代码输出什么？
```c
int x = 5;
if (x = 10) {    // 注意：= 不是 ==
    printf("Yes\n");
} else {
    printf("No\n");
}
```

<details>
<summary>📝 参考答案 L1-3</summary>

**题3-1**：`if (num % 3 == 0)`

**题3-2**：`else (score >= 70)` 错误，应该是 `else if (score >= 70)`

**题3-3**：
```c
int day;
scanf("%d", &day);
switch (day) {
    case 1: printf("星期一\n"); break;
    case 2: printf("星期二\n"); break;
    // ... 以此类推
    default: printf("无效输入\n");
}
```

**题3-4**：输出 `Yes`。因为 `x = 10` 是赋值表达式，值为10（非0=真），所以if条件永远为真！这是经典Bug。
</details>

---

### 🟢 L1-4：循环结构习题（Day 11-15）

**题4-1** 填空题：用for循环输出1到100的和
```c
int sum = ___;
for (int i = ___; i <= ___; i++) {
    sum = sum ___ i;
}
printf("1+2+...+100 = %d\n", sum);
```

**题4-2** 改错题：下面的程序想输出10次"Hello"，哪里错了？
```c
for (int i = 0; i <= 10; i++); {   // 注意这里有没有分号？
    printf("Hello\n");
}
```

**题4-3** 改错题：下面的while循环为什么是死循环？
```c
int i = 1;
while (i <= 10) {
    printf("%d\n", i);
    // 缺少了什么？
}
```

**题4-4** 嵌套循环手算：以下代码输出多少个 `*`？
```c
for (int i = 1; i <= 3; i++) {
    for (int j = 1; j <= 4; j++) {
        printf("*");
    }
    printf("\n");
}
```

**题4-5** 仿写题：输出100以内所有能被3整除但不能被5整除的数。

<details>
<summary>📝 参考答案 L1-4</summary>

**题4-1**：`int sum = 0; for (int i = 1; i <= 100; i++) { sum = sum + i; }`

**题4-2**：`for(...);` 多了一个分号！分号是空语句，循环体变成了空的，`printf` 只在循环结束后执行一次。去掉分号即可。

**题4-3**：缺少 `i++;`，i永远等于1，条件永远为真。

**题4-4**：12个（3行×4列）。外层3次，每次内层4次。

**题4-5**：
```c
for (int i = 1; i <= 100; i++) {
    if (i % 3 == 0 && i % 5 != 0) {
        printf("%d ", i);
    }
}
```
</details>

---

### 🟡 L2-2：第二阶段进阶实操（Day 17后完成）

**题L2-4** 猜数字游戏增强版：
- 随机生成1-100的数字（用 `rand()`）
- 玩家有7次猜测机会
- 每次猜完提示"大了"或"小了"
- 7次内猜中显示"你赢了"，用完机会显示"你输了，答案是X"
- 每次显示剩余次数

**题L2-5** 图形打印：
- 输入一个正整数n
- 打印n行的等腰三角形
- 例如n=4输出：
```
   *
  ***
 *****
*******
```

**题L2-6** 数字特性判断：
输入一个整数，输出它的所有特性：
- 是奇数还是偶数
- 是否是素数
- 是否是回文数（如121、12321）
- 各位数字之和

<details>
<summary>📝 参考答案 L2</summary>

**题L2-4** 核心代码：
```c
srand(time(NULL));
int secret = rand() % 100 + 1;
int guess, attempts = 7;
while (attempts > 0) {
    printf("剩余%d次，请猜：", attempts);
    scanf("%d", &guess);
    if (guess == secret) { printf("🎉 你赢了！\n"); break; }
    if (guess > secret) printf("太大了\n");
    else printf("太小了\n");
    attempts--;
}
if (attempts == 0) printf("你输了，答案是%d\n", secret);
```

**题L2-5** 核心代码：
```c
for (int i = 1; i <= n; i++) {
    for (int j = 1; j <= n - i; j++) printf(" ");
    for (int j = 1; j <= 2*i-1; j++) printf("*");
    printf("\n");
}
```

**题L2-6** 回文数判断核心：
```c
int original = num, reversed = 0, temp = num;
while (temp > 0) {
    reversed = reversed * 10 + temp % 10;
    temp /= 10;
}
if (reversed == original) printf("是回文数\n");
```
</details>

---

### 🔴 L3-2：第二阶段综合拓展（Day 17后挑战）

**题L3-2** 简易ATM模拟：
```
功能：查询余额、存款、取款、退出
初始余额：1000元
要求：
- 取款不能超过余额
- 取款金额必须是100的整数倍
- 每次操作后显示余额
- 用循环保持程序运行
- 输入密码（预设123456），3次错误锁定
```

---

## 第三阶段：数组与函数（Day 18-28）

### 🟢 L1-5：数组习题

**题5-1** 填空题：求数组元素之和
```c
int arr[] = {5, 8, 3, 9, 2};
int size = sizeof(____) / sizeof(____[0]);  // 计算数组大小
int sum = 0;
for (int i = 0; i < ____; i++) {
    sum += ____[i];
}
```

**题5-2** 数组越界判断：以下代码访问了哪些不合法的下标？
```c
int arr[5] = {1, 2, 3, 4, 5};
printf("%d\n", arr[5]);   // 合法？不合法？
printf("%d\n", arr[-1]);  // 合法？不合法？
```

**题5-3** 字符串`\0`陷阱：
```c
char str1[] = {'H', 'i', '!'};
char str2[] = "Hi!";
printf("str1占用%d字节\n", sizeof(str1));  // ?
printf("str2占用%d字节\n", sizeof(str2));  // ?
```

<details>
<summary>📝 参考答案 L1-5</summary>

**题5-1**：`sizeof(arr) / sizeof(arr[0])`、`i < size`、`arr[i]`

**题5-2**：`arr[5]` 不合法（数组只有0-4），`arr[-1]` 不合法（负下标）。两者都不会报编译错误，但都是未定义行为！

**题5-3**：str1=3字节（无\0），str2=4字节（H+i+!+\0）。这就是为什么str1不能用%s输出。
</details>

---

### 🟢 L1-6：函数习题

**题6-1** 指出函数声明和函数定义：
```c
// A
int max(int a, int b);

// B
int max(int a, int b) {
    return a > b ? a : b;
}
```

**题6-2** 值传递陷阱：以下代码执行后，main中的x是多少？
```c
void change(int n) { n = 100; }
int main() {
    int x = 5;
    change(x);
    printf("%d\n", x);  // ?
    return 0;
}
```

**题6-3** 递归手算：`factorial(4)` 的完整调用展开过程。

<details>
<summary>📝 参考答案 L1-6</summary>

**题6-1**：A是函数声明（只有函数头+分号），B是函数定义（有函数体）。

**题6-2**：x=5。change函数修改的是形参n（x的副本），不影响x。

**题6-3**：
```
f(4) = 4 * f(3)
     = 4 * 3 * f(2)
     = 4 * 3 * 2 * f(1)
     = 4 * 3 * 2 * 1
     = 24
```
</details>

---

### 🟡 L2-3：第三阶段进阶实操

**题L2-7** 学生成绩统计系统（数组版）：
- 输入n个学生的姓名和成绩
- 计算平均分、最高分、最低分
- 按成绩从高到低排序并输出排名
- 统计各分数段人数（90-100/80-89/70-79/60-69/60以下）

**题L2-8** 字符串工具包：
用函数实现以下字符串操作：
- `my_strlen`：求字符串长度
- `my_strrev`：反转字符串
- `my_strcount`：统计字符串中某个字符出现的次数
- `my_ispalindrome`：判断字符串是否是回文

---

## 第四阶段：指针与结构体（Day 29-45）

### 🟢 L1-7：指针基础习题

**题7-1** 填空题：
```c
int a = 10;
int *p = ___;    // p指向a
printf("%d\n", ___);  // 通过p输出a的值（10）
___ = 20;        // 通过p修改a为20
printf("%d\n", a);   // 输出20
```

**题7-2** 指针与数组：写出以下4种方式输出 `arr[2]` 的等价表达式
```c
int arr[] = {10, 20, 30, 40, 50};
// 方式1: arr[2]
// 方式2: *(arr + __)
// 方式3: 用一个指针变量p
// 方式4: 用p和下标
```

**题7-3** 内存图绘制：画出以下代码的内存布局（用方框和箭头）
```c
int x = 5;
int *p = &x;
int **pp = &p;
```

**题7-4** 找出Bug：
```c
int *getPointer() {
    int local = 42;
    return &local;   // 有问题吗？
}
```

<details>
<summary>📝 参考答案 L1-7</summary>

**题7-1**：`int *p = &a;`、`printf("%d\n", *p);`、`*p = 20;`

**题7-2**：
```c
// 方式1: arr[2]
// 方式2: *(arr + 2)
// 方式3: int *p = arr; *(p + 2)
// 方式4: int *p = arr; p[2]
```

**题7-3**：
```
pp → p → x(5)
[&p]  [&x]  [5]
```

**题7-4**：有问题！返回了局部变量local的地址。函数返回后local的内存已释放，这个指针变成悬挂指针。应使用malloc在堆上分配，或使用static变量。
</details>

---

### 🟢 L1-8：动态内存习题

**题8-1** 填空题：创建一个动态数组
```c
int n;
scanf("%d", &n);
int *arr = (int*)______(n * ______(int));
// 使用arr...
______(arr);   // 释放内存
arr = ______;  // 防止悬挂指针
```

**题8-2** 内存泄漏检测：以下代码哪里有问题？
```c
void process() {
    int *data = (int*)malloc(100 * sizeof(int));
    if (data == NULL) return;
    // 处理数据...
    if (某个条件) {
        return;   // ← 有问题！
    }
    free(data);
}
```

<details>
<summary>📝 参考答案 L1-8</summary>

**题8-1**：`malloc`、`sizeof`、`free`、`NULL`

**题8-2**：提前return时没有free(data)，造成内存泄漏！应该在所有return路径上都确保free。
</details>

---

### 🟢 L1-9：结构体习题

**题9-1** 结构体成员访问：
```c
typedef struct { int x; int y; } Point;
Point p1 = {3, 5};
Point *pp = &p1;
// pp->x = ?  （写出来）
// (*pp).y = ? （写出来）
```

**题9-2** 改错题：
```c
struct Student {
    char name[30];
    int age;
}   // ← 少什么？

Student s;  // 能用 Student 直接声明吗？（没用typedef）
```

**题9-3** 链表手画题：
```
从头插入：10 → 20 → 30
画出每个节点的内存布局，标注 data 和 next
```

---

### 🟡 L2-4：第四阶段进阶实操

**题L2-9** 动态数组版学生管理系统：
- 用 `malloc` 动态分配学生数组
- 支持运行时添加/删除学生（用 `realloc` 调整大小）
- 实现增删改查功能
- 确保所有 malloc 都有对应的 free

**题L2-10** 链表练习——多项式加法：
- 用链表表示一元多项式（每个节点存系数和指数）
- 实现两个多项式相加

---

## 第五阶段：文件操作与综合项目（Day 46-60）

### 🟢 L1-10：文件操作习题

**题10-1** 填空题：文件的打开、写入、关闭
```c
______ *fp = ______("data.txt", "___");  // 写模式打开
fprintf(____, "Hello File!\n");
______(fp);   // 关闭
```

**题10-2** 文件读取判断：
```c
// 以下哪种方式正确判断文件是否读完？
// A. while (!feof(fp)) { fscanf(...); printf(...); }  // 有问题吗？
// B. while (fscanf(fp, "%d", &num) == 1) { printf(...); }
```

<details>
<summary>📝 参考答案 L1-10</summary>

**题10-1**：`FILE *fp = fopen("data.txt", "w");` → `fprintf(fp, ...)` → `fclose(fp);`

**题10-2**：B是正确的。A有经典Bug——`feof` 只在**尝试读取失败后**才返回真，不是提前预测。用A方式会导致最后一行被输出两次。
</details>

---

### 🟡 L2-5：第五阶段进阶实操

**题L2-11** 文件合并工具：输入两个文本文件名，将第二个文件的内容追加到第一个文件末尾。

**题L2-12** CSV成绩分析器：
- 读取CSV格式的成绩文件（姓名,数学,英语,C语言）
- 计算每人的总分和平均分
- 按总分排名
- 输出统计报告到另一个文件

---

### 🔴 L3-3：终极综合项目

**题L3-3** 图书管理系统（结业项目）——详见 Day 60 上机考核题。完整需求：
1. 链表存储图书信息
2. 文件持久化
3. 增删改查 + 排序
4. 模糊搜索
5. CSV导出

---

## 附录：常见易错点汇总

| 易错点 | 错误写法 | 正确写法 | 出现频率 |
|--------|----------|----------|----------|
| `=` vs `==` | `if (a = 5)` | `if (a == 5)` | ⭐⭐⭐⭐⭐ |
| 数组越界 | `arr[5]`（5个元素数组） | `arr[0]~arr[4]` | ⭐⭐⭐⭐ |
| 整数除法 | `5 / 2` → 2 | `5.0 / 2` → 2.5 | ⭐⭐⭐⭐ |
| scanf缺& | `scanf("%d", a)` | `scanf("%d", &a)` | ⭐⭐⭐⭐⭐ |
| for后多分号 | `for(...);` | `for(...)` 无分号 | ⭐⭐⭐ |
| 字符串=\0 | `char s[]={'H','i'}` | `char s[]="Hi"` | ⭐⭐⭐ |
| 缺少break | case后忘写break | 每个case加break | ⭐⭐⭐⭐ |
| 忘记free | malloc后没free | malloc/free成对 | ⭐⭐⭐⭐ |
| 返回局部变量地址 | `return &local` | 用malloc或static | ⭐⭐⭐ |
| fclose忘记 | fopen后忘fclose | fopen/fclose成对 | ⭐⭐⭐ |
| NULL指针解引用 | `*p` 当p==NULL | 先检查 `if(p)` | ⭐⭐⭐ |
| 字符串比较用== | `if(s1 == s2)` | `if(strcmp(s1,s2)==0)` | ⭐⭐⭐⭐ |
| fgets保留\n | 直接使用 | 去掉末尾换行符 | ⭐⭐⭐ |

---

> 📌 习题完成后，用 [module-4-能力评估.md](module-4-能力评估.md) 进行阶段性测评！
