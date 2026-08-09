# 模块2：分阶段逐天讲课讲义（Day 31 - Day 45）

> 📌 本阶段是C语言的"分水岭"——指针深入、动态内存、结构体。啃下来，你就从入门走向了进阶。

---

## Day 31：指针深入（一）—— 多级指针与指针数组

### 🎯 今日学习目标
学完后你能：
- 理解二级指针 `int **pp` 的概念
- 区分指针数组和数组指针
- 画出多级指针的内存模型图

---

### 📖 通俗化知识点讲解

#### 1. 二级指针（指向指针的指针）

> **生活类比**：图书馆找书。
> - 书在书架上（变量值）
> - 索书号告诉你书在哪（一级指针，指向书）
> - 你把索书号写在便签上，便签放在电脑旁边（二级指针，指向便签）
>
> 二级指针 = 存储"另一个指针的地址"的变量。

```c
int value = 100;
int *p = &value;      // 一级指针：p 存的是 value 的地址
int **pp = &p;        // 二级指针：pp 存的是 p 的地址

// 内存模型：
// pp ──→ p ──→ value(100)
// 地址A   地址B   地址C

// 访问 value 的三种方式：
value   = 100    // 直接访问
*p      = 100    // 通过一级指针访问
**pp    = 100    // 通过二级指针访问（解引用两次）
```

#### 2. 指针数组（Array of Pointers）

> **生活类比**：宿舍楼每层有一个楼层长。指针数组 = 一个本子，记录着每个楼层长的房间号。

```c
// 指针数组：数组的元素是指针
int a = 10, b = 20, c = 30;
int *ptrArr[3] = {&a, &b, &c};  // 存了3个int*指针

// 访问：
*ptrArr[0]  // = 10（第一个指针指向的值）
*ptrArr[1]  // = 20（第二个指针指向的值）
```

#### 3. 数组指针（Pointer to Array）
```c
int arr[5] = {1, 2, 3, 4, 5};
int (*pArr)[5] = &arr;   // pArr 是指向"5个int的数组"的指针
// 注意：(*pArr) 的括号不能省！
// int *pArr[5] 是指针数组（5个指针）
// int (*pArr)[5] 是数组指针（1个指针，指向5个int的数组）
```

---

### 💻 上机敲代码

```c
/*
 * 文件名：multi_pointer.c
 * 功能：二级指针、指针数组、数组指针
 */

#include <stdio.h>

int main()
{
    // ===== 一、二级指针 =====
    printf("===== 二级指针 =====\n");
    int value = 100;
    int *p = &value;      // p → value
    int **pp = &p;        // pp → p → value

    printf("value = %d\n", value);      // 直接访问
    printf("*p = %d\n", *p);            // 通过一级指针
    printf("**pp = %d\n", **pp);        // 通过二级指针
    printf("\n地址关系：\n");
    printf("value 的地址：%p\n", (void*)&value);
    printf("p 存的地址：%p（就是value的地址）\n", (void*)p);
    printf("p 自己的地址：%p\n", (void*)&p);
    printf("pp存的地址：%p（就是p的地址）\n", (void*)pp);

    // 通过二级指针修改 value
    **pp = 999;
    printf("\n**pp = 999 后，value = %d\n", value);  // 999

    // ===== 二、指针数组 =====
    printf("\n===== 指针数组 =====\n");
    int n1 = 10, n2 = 20, n3 = 30, n4 = 40, n5 = 50;
    int *ptrArray[5] = {&n1, &n2, &n3, &n4, &n5};
    //  ptrArray 是一个有5个元素的数组，每个元素是 int*

    printf("通过指针数组访问：\n");
    for (int i = 0; i < 5; i++) {
        printf("ptrArray[%d] → %d\n", i, *ptrArray[i]);
        // ptrArray[i] 取出第i个指针（地址）
        // *ptrArray[i] 解引用，取出该地址存储的值
    }

    // ===== 三、指针数组的实际应用：字符串数组 =====
    printf("\n===== 字符串数组（指针数组实现） =====\n");
    // 每个字符串常量在内存中有一个地址
    char *fruits[] = {
        "Apple",    // fruits[0] 指向 "Apple" 的首字符 'A'
        "Banana",   // fruits[1] 指向 "Banana" 的首字符 'B'
        "Cherry",   // fruits[2] 指向 "Cherry" 的首字符 'C'
        "Durian"    // fruits[3] 指向 "Durian" 的首字符 'D'
    };
    int count = sizeof(fruits) / sizeof(fruits[0]);

    printf("水果清单：\n");
    for (int i = 0; i < count; i++) {
        printf("  %d. %s\n", i + 1, fruits[i]);
        // fruits[i] 是一个 char* 指针，%s 可以直接输出它指向的字符串
    }

    return 0;
}
```

---

### 📋 今日核心知识点总结

1. 二级指针 `int **pp`：存的是"一级指针的地址"
2. `*pp` 得到一级指针，`**pp` 得到最终的值
3. 指针数组 `int *arr[N]`：数组的每个元素是指针
4. 数组指针 `int (*p)[N]`：一个指针，指向整个数组
5. 字符串数组常用指针数组实现：`char *names[] = {"A", "B", "C"};`

---

## Day 32：指针深入（二）—— 函数指针

### 🎯 今日学习目标
学完后你能：
- 理解函数指针的概念
- 掌握函数指针的声明和调用
- 了解回调函数的基本思想

---

### 📖 通俗化知识点讲解

> **生活类比**：手机通讯录。
> 你不需要记住每个人的电话号码（函数的机器码地址），只需要在通讯录里存个名字（函数指针），打电话时点一下名字就行（通过函数指针调用）。
>
> **函数指针 = 存储函数入口地址的指针变量**

```c
// 声明一个函数指针：
// 返回类型 (*指针名)(参数类型列表);

int (*funcPtr)(int, int);   // funcPtr 是指向"接收两个int、返回int的函数"的指针

// 让指针指向具体函数：
funcPtr = &add;    // 或者直接 funcPtr = add;（函数名本身就是地址）

// 通过指针调用函数：
int result = funcPtr(3, 5);   // 等价于 add(3, 5)
```

---

### 💻 上机敲代码

```c
/*
 * 文件名：function_pointer.c
 * 功能：函数指针——让函数成为"变量"
 */

#include <stdio.h>

// 四个运算函数（它们有相同的签名：double f(double, double)）
double add(double a, double b)      { return a + b; }
double subtract(double a, double b) { return a - b; }
double multiply(double a, double b) { return a * b; }
double divide(double a, double b)   { return a / b; }

// 函数指针作为参数：通用计算器
double calculate(double a, double b, double (*operation)(double, double))
{
    //                         ↑ 第三个参数是一个函数指针
    return operation(a, b);   // 调用传入的函数
}

int main()
{
    // ===== 一、函数指针基本语法 =====
    // 声明一个函数指针：指向 double xxx(double, double) 类型的函数
    double (*funcPtr)(double, double);

    // 指向加法函数
    funcPtr = add;   // 函数名本身就是地址，不用写 &
    printf("通过函数指针计算 3.5 + 2.5 = %.1f\n", funcPtr(3.5, 2.5));

    funcPtr = multiply;
    printf("通过函数指针计算 3.5 × 2.5 = %.1f\n", funcPtr(3.5, 2.5));

    // ===== 二、函数指针数组——更优雅的菜单系统 =====
    printf("\n===== 函数指针数组 =====\n");
    double (*operations[4])(double, double) = {add, subtract, multiply, divide};
    char *opNames[] = {"加法", "减法", "乘法", "除法"};
    char opSymbols[] = {'+', '-', '*', '/'};

    double num1 = 10.0, num2 = 3.0;
    for (int i = 0; i < 4; i++) {
        double result = operations[i](num1, num2);  // 调用数组中第i个函数
        printf("%.1f %c %.1f = %.2f  (%s)\n",
               num1, opSymbols[i], num2, result, opNames[i]);
    }

    // ===== 三、回调函数——把函数传给另一个函数 =====
    printf("\n===== 回调函数演示 =====\n");
    double x = 8.0, y = 3.0;
    // calculate 接收两个数和一个"操作函数"
    printf("%.1f + %.1f = %.1f\n", x, y, calculate(x, y, add));
    printf("%.1f - %.1f = %.1f\n", x, y, calculate(x, y, subtract));
    printf("%.1f * %.1f = %.1f\n", x, y, calculate(x, y, multiply));
    printf("%.1f / %.1f = %.1f\n", x, y, calculate(x, y, divide));

    return 0;
}

// calculate 函数定义（声明在main之前，定义在这里）
double calculate(double a, double b, double (*operation)(double, double))
{
    if (operation == divide && b == 0) {
        printf("错误：除数不能为0！\n");
        return 0;
    }
    return operation(a, b);
}
```

---

### 📋 今日核心知识点总结

1. 函数指针声明：`返回类型 (*指针名)(参数类型列表);`
2. 函数名本身就代表函数地址，`funcPtr = functionName` 即可
3. 函数指针的典型应用：回调函数、菜单系统、策略模式
4. 函数指针数组让代码更简洁：`ops[i](a, b)` 直接调用

---

## Day 33：指针深入（三）—— 动态内存分配入门

### 🎯 今日学习目标
学完后你能：
- 理解堆内存和栈内存的区别
- 使用 `malloc()` 和 `free()` 管理动态内存
- 体会"按需分配"的灵活性

---

### 📖 通俗化知识点讲解

#### 1. 栈 vs 堆——两种内存

> **生活类比**：
> - **栈内存**：酒店前台的临时寄存处——离开酒店就清空（函数返回就释放），空间有限
> - **堆内存**：自己租的长期仓库——想租多大租多大，想什么时候退租就什么时候退租，但要**自己记得退租**

| 对比 | 栈（Stack） | 堆（Heap） |
|------|------------|-----------|
| 分配方式 | 编译器自动 | 程序员手动 malloc/free |
| 大小限制 | 较小（几MB） | 很大（受物理内存限制） |
| 生命周期 | 函数结束时自动释放 | 程序员决定何时free |
| 速度 | 快 | 较慢 |
| 典型用法 | 局部变量、函数参数 | 大小不确定的数据、需要跨函数使用的数据 |

#### 2. malloc 和 free

```c
#include <stdlib.h>   // malloc 和 free 需要这个头文件！

// malloc：申请内存
int *p = (int*)malloc(sizeof(int));     // 申请一个int大小的空间
int *arr = (int*)malloc(10 * sizeof(int)); // 申请10个int的连续空间（相当于数组）

// 检查是否申请成功
if (arr == NULL) {
    printf("内存分配失败！\n");
    return 1;
}

// 使用...（和普通数组一样）
arr[0] = 10;
arr[1] = 20;

// free：释放内存（必须做！）
free(arr);
arr = NULL;   // 好习惯：释放后把指针设为NULL
```

> ⚠️ **内存泄漏**：`malloc` 了但没 `free`，程序占用的内存越来越多，最终耗尽系统内存。
> 申请和释放必须**一一对应**！

---

### 💻 上机敲代码

```c
/*
 * 文件名：dynamic_memory_intro.c
 * 功能：malloc/free 入门——动态数组
 */

#include <stdio.h>
#include <stdlib.h>   // malloc, free

int main()
{
    // ===== 一、动态分配一个变量 =====
    int *p = (int*)malloc(sizeof(int));
    //  malloc 返回 void* 类型，需要强制转换为 (int*)
    //  sizeof(int) 告诉 malloc 要分配多少字节

    if (p == NULL) {
        printf("内存分配失败！\n");
        return 1;
    }

    *p = 42;
    printf("动态分配的 int 值：%d\n", *p);
    free(p);      // 用完了，归还内存
    p = NULL;     // 好习惯

    // ===== 二、动态数组——运行时决定大小！ =====
    int n;
    printf("\n你想存多少个学生的成绩？");
    scanf("%d", &n);

    // 根据用户输入动态分配刚好够用的内存
    int *scores = (int*)malloc(n * sizeof(int));

    if (scores == NULL) {
        printf("内存分配失败，可能输入的数目太大了。\n");
        return 1;
    }

    // 使用动态数组（和普通数组一模一样）
    printf("请输入 %d 个成绩：\n", n);
    for (int i = 0; i < n; i++) {
        printf("第%d个：", i + 1);
        scanf("%d", &scores[i]);
    }

    // 计算平均分
    int sum = 0;
    for (int i = 0; i < n; i++) {
        sum += scores[i];
    }
    printf("\n共 %d 个学生，平均分：%.1f\n", n, (float)sum / n);

    // 释放内存
    free(scores);
    scores = NULL;

    // ===== 对比：普通数组的局限 =====
    // int scores[100];  ← 这样写必须提前确定大小
    // 如果只有10个学生，浪费90个空间
    // 如果有200个学生，存不下！
    // 动态数组完美解决了这个问题。

    return 0;
}
```

---

### 📋 今日核心知识点总结

1. `malloc(size)` 在堆上分配内存，返回 `void*` 指针
2. `free(ptr)` 释放 malloc 分配的内存
3. **malloc 和 free 必须一一对应**，否则内存泄漏
4. 动态分配的数组和普通数组用法完全一样
5. 动态分配的优势：**运行时决定大小**，按需分配

---

## Day 34-35：字符串与指针进阶

### 🎯 今日学习目标
- 深入理解 `char*` 和 `char[]` 的底层区别
- 编写自己的字符串处理函数
- 处理命令行参数

---

### 📖 通俗化知识点讲解

#### 1. `char*` vs `char[]`——表面一样，底层不同

```c
char str1[] = "Hello";   // 在栈上分配6字节的可修改数组
char *str2  = "Hello";   // 指向常量区的只读字符串

str1[0] = 'h';   // ✅ 可以修改！（修改栈上的数组）
str2[0] = 'h';   // ❌ 未定义行为！常量区不可修改，程序可能崩溃！
```

| | `char arr[]` | `char *ptr` |
|---|---|---|
| 存储位置 | 栈 | 指针在栈，字符串在常量区 |
| 可修改？ | ✅ 是 | ❌ 否（试图修改可能崩溃） |
| sizeof | 字符串长度+1 | 指针大小（4或8字节） |
| 可以重新指向？ | ❌ 数组名是常量 | ✅ 可以 `ptr = "other"` |

#### 2. 自己实现 strlen / strcpy / strcmp

> 面试和考试常考！理解这些函数的内部实现，你对指针的理解会上一个台阶。

---

### 💻 上机敲代码

```c
/*
 * 文件名：string_advanced.c
 * 功能：手写字符串函数 + char* vs char[] + 命令行参数
 */

#include <stdio.h>

// 自己实现的字符串函数
size_t my_strlen(const char *s);              // 求长度
char* my_strcpy(char *dest, const char *src); // 拷贝
int my_strcmp(const char *a, const char *b);  // 比较
char* my_strcat(char *dest, const char *src); // 拼接

int main(int argc, char *argv[])   // 命令行参数！
{
    // ===== 一、命令行参数 =====
    printf("===== 命令行参数 =====\n");
    printf("argc = %d（参数个数，含程序名）\n", argc);
    for (int i = 0; i < argc; i++) {
        printf("argv[%d] = %s\n", i, argv[i]);
    }

    // ===== 二、char* vs char[] =====
    printf("\n===== char* vs char[] =====\n");
    char arr[] = "Hello";  // 栈上的可修改数组
    char *ptr = "World";   // 指向常量区

    printf("sizeof(arr) = %d（整个数组6字节，含\\0）\n", (int)sizeof(arr));
    printf("sizeof(ptr) = %d（指针本身大小，可能是8字节）\n", (int)sizeof(ptr));

    arr[0] = 'h';   // ✅ 安全
    printf("修改后 arr = %s\n", arr);
    // ptr[0] = 'w';  // ❌ 危险！不要这样做！

    // ===== 三、测试自己实现的字符串函数 =====
    printf("\n===== 自实现字符串函数测试 =====\n");

    char s1[] = "Hello World";
    printf("my_strlen(\"%s\") = %d\n", s1, (int)my_strlen(s1));

    char s2[50];
    my_strcpy(s2, s1);
    printf("my_strcpy 结果：s2 = %s\n", s2);

    printf("my_strcmp(\"abc\", \"abd\") = %d\n", my_strcmp("abc", "abd"));
    printf("my_strcmp(\"abc\", \"abc\") = %d\n", my_strcmp("abc", "abc"));

    char s3[50] = "Hello";
    my_strcat(s3, " C");
    my_strcat(s3, " Language");
    printf("my_strcat 结果：s3 = %s\n", s3);

    return 0;
}

// ===== 自实现字符串函数 =====

// 求字符串长度：从开头数到 \0
size_t my_strlen(const char *s) {
    size_t len = 0;
    while (s[len] != '\0') {   // 等价于 while (*s != '\0')
        len++;
    }
    return len;
}

// 拷贝字符串：把src的每个字符复制到dest
char* my_strcpy(char *dest, const char *src) {
    int i = 0;
    while (src[i] != '\0') {
        dest[i] = src[i];
        i++;
    }
    dest[i] = '\0';   // 别忘了结尾的 \0！
    return dest;
}

// 比较字符串：逐个字符比较
int my_strcmp(const char *a, const char *b) {
    int i = 0;
    while (a[i] != '\0' && b[i] != '\0') {
        if (a[i] != b[i]) {
            return a[i] - b[i];   // 返回第一个不同字符的ASCII差值
        }
        i++;
    }
    return a[i] - b[i];   // 处理长度不同的情况
}

// 拼接字符串：把src接到dest后面
char* my_strcat(char *dest, const char *src) {
    int i = 0;
    // 先找到 dest 的末尾（\0 的位置）
    while (dest[i] != '\0') {
        i++;
    }
    // 从末尾开始拷贝 src
    int j = 0;
    while (src[j] != '\0') {
        dest[i] = src[j];
        i++;
        j++;
    }
    dest[i] = '\0';   // 别忘了结尾的 \0！
    return dest;
}

// 重写 my_strlen，用指针版本（效率更高）：
// size_t my_strlen(const char *s) {
//     const char *p = s;
//     while (*p != '\0') p++;
//     return p - s;   // 两个指针相减 = 它们之间的元素个数
// }
```

---

### 📋 今日核心知识点总结

1. `char[]` 在栈上可修改，`char*`指向常量区不可修改
2. `sizeof(数组名)` = 整个数组大小；`sizeof(指针)` = 4或8字节
3. `argc` 是命令行参数个数，`argv[]` 是参数字符串数组
4. 手写 strlen/strcpy/strcmp 是面试高频题，必须能盲打出来

---

## Day 36：指针与函数进阶——传址与返回指针

### 🎯 今日学习目标
- 掌握指针作为函数参数的各种模式
- 理解函数返回指针的注意事项

---

### 📖 通俗化知识点讲解

#### 1. 指针参数的三种用途

```c
// 用途1：修改外部变量（输出参数）
void getMinMax(int *arr, int n, int *min, int *max);

// 用途2：传递大数据（避免复制整个数据）
void processLargeData(const BigStruct *data);  // const 保证不修改

// 用途3：传递数组
void sort(int *arr, int n);
```

#### 2. 函数返回指针的陷阱

```c
int* createDangerous() {
    int local = 10;
    return &local;   // ❌ 危险！返回局部变量的地址
    // 函数返回后，local 的内存已被释放，这个指针指向垃圾数据！
}

int* createSafe() {
    int *p = (int*)malloc(sizeof(int));  // 在堆上分配
    *p = 10;
    return p;   // ✅ 安全！堆上的数据不会自动释放
}
```

---

### 💻 上机敲代码

```c
/*
 * 文件名：pointer_function_adv.c
 * 功能：指针与函数进阶应用
 */

#include <stdio.h>
#include <stdlib.h>

// 函数声明
void getMinMax(const int *arr, int n, int *min, int *max);
int* createArray(int n);           // 在堆上创建数组并返回
void swapAny(void *a, void *b, size_t size);  // 通用交换（了解即可）

int main()
{
    // ===== 一、多个输出参数（指针参数） =====
    int scores[] = {85, 92, 78, 96, 63, 88};
    int n = sizeof(scores) / sizeof(scores[0]);
    int min, max;

    // 传入 min 和 max 的地址，函数通过指针"输出"结果
    getMinMax(scores, n, &min, &max);
    printf("成绩范围：%d ~ %d\n", min, max);

    // ===== 二、函数返回堆上创建的数组 =====
    int size;
    printf("\n要创建多大的数组？");
    scanf("%d", &size);

    int *myArray = createArray(size);  // createArray内malloc
    if (myArray != NULL) {
        // 初始化数组
        for (int i = 0; i < size; i++) {
            myArray[i] = i * 10;
        }
        // 打印数组
        printf("数组内容：");
        for (int i = 0; i < size; i++) {
            printf("%d ", myArray[i]);
        }
        printf("\n");

        free(myArray);   // 用完了，释放！
        myArray = NULL;
    }

    return 0;
}

// 同时获取最小值和最大值（通过指针"返回"两个值）
void getMinMax(const int *arr, int n, int *min, int *max) {
    // const int *arr 表示：arr指向的数据只读，不去修改它
    *min = arr[0];   // *min 修改的是 main 中的 min 变量
    *max = arr[0];   // *max 修改的是 main 中的 max 变量
    for (int i = 1; i < n; i++) {
        if (arr[i] < *min) *min = arr[i];
        if (arr[i] > *max) *max = arr[i];
    }
}

// 在堆上创建数组，返回指针
// 调用者负责 free！
int* createArray(int n) {
    int *arr = (int*)malloc(n * sizeof(int));
    if (arr == NULL) {
        printf("内存分配失败！\n");
        return NULL;
    }
    printf("成功分配了 %d 个int的空间（%d字节）\n",
           n, (int)(n * sizeof(int)));
    return arr;
}
```

---

### 📋 今日核心知识点总结

1. 指针参数可以"输出"多个值（如同时返回min和max）
2. 函数可以返回堆上的指针，**调用者要负责free**
3. **绝对不要返回局部变量的地址**——函数返回后局部变量的内存已失效
4. `const int *p` 表示p指向的数据只读，不可通过p修改

---

## Day 37：第五阶段复习（Day 29-36）——指针专题强化

### 🎯 今日学习目标
- 集中复习指针核心概念
- 手画内存图练习
- 完成指针专题自我检测

---

### 📖 指针知识体系思维导图

```
指针
├── 基本概念
│   ├── & 取地址 → 获取变量的内存地址
│   ├── * 解引用 → 通过地址访问变量
│   └── 声明 int *p → p是指向int的指针
├── 指针与数组
│   ├── 数组名 = &数组[0]（常量指针）
│   ├── arr[i] = *(arr + i)
│   └── 指针可以自增减遍历数组
├── 指针与函数
│   ├── 传址调用 → 函数内修改外部变量
│   ├── 数组参数 = 指针参数
│   └── 返回指针 → 不能返回局部变量地址
├── 多级指针
│   ├── int **pp → 指向指针的指针
│   └── 指针数组 vs 数组指针
├── 函数指针
│   ├── 声明：返回类型 (*名)(参数)
│   └── 回调函数
└── 动态内存
    ├── malloc(n * sizeof(type)) → 申请
    └── free(ptr) → 释放（必须！）
```

---

### 💻 指针终极练习：手写代码

**关掉讲义，独立完成以下代码，然后对照检查：**

```c
/*
 * 指针自测题：
 * 1. 写一个 swap 函数，交换两个整数
 * 2. 写一个函数，统计数组中的最大值、最小值、平均值（通过指针返回）
 * 3. 写一个函数，反转字符串（用指针，不用下标）
 * 4. 动态创建一个数组，填充斐波那契数列的前n项
 */

// （参考答案在 module-3 中）
```

---

## Day 38：结构体（上）—— 自定义数据类型

### 🎯 今日学习目标
学完后你能：
- 理解为什么需要结构体
- 掌握结构体的定义、声明、访问
- 使用结构体组织关联数据

---

### 📖 通俗化知识点讲解

#### 1. 为什么需要结构体？

> **生活类比**：学生档案袋。
> 一个学生有多项信息：姓名（字符串）、年龄（整数）、身高（小数）、成绩（整数）。
> 用单独的变量：
> ```c
> char name1[20]; int age1; float height1; int score1;  // 学生1
> char name2[20]; int age2; float height2; int score2;  // 学生2
> // 松散、容易搞混、不方便管理
> ```
> 用结构体——把这些信息"打包"成一个整体：
> ```c
> struct Student {
>     char name[20];
>     int age;
>     float height;
>     int score;
> };
> // 一个 Student 变量就包含了所有信息，干净利落！
> ```

#### 2. 结构体三步曲

```c
// 第一步：定义结构体类型（"设计蓝图"）
struct Student {
    char name[30];    // 成员变量
    int age;
    float score;
};   // ← 注意分号！

// 第二步：声明结构体变量（"按蓝图造房子"）
struct Student stu1;           // 在栈上
struct Student stu2 = {"张三", 18, 92.5};  // 声明+初始化

// 第三步：访问成员变量（用 . 运算符）
printf("姓名：%s\n", stu1.name);
stu1.age = 19;
stu1.score = 95.0;
```

#### 3. 用 typedef 简化

```c
// 不用每次写 struct Student，用 typedef 起个别名
typedef struct {
    char name[30];
    int age;
    float score;
} Student;   // Student 现在是一个类型名，可以直接用

Student s1 = {"李四", 19, 88.5};  // 不需要 struct 关键字了
```

---

### 💻 上机敲代码

```c
/*
 * 文件名：struct_basic.c
 * 功能：结构体基本操作——学生信息管理
 */

#include <stdio.h>
#include <string.h>

// 定义学生结构体类型
typedef struct {
    char name[30];      // 姓名
    int age;            // 年龄
    float score;        // 成绩
    char gender;        // 性别：'M'男 'F'女
} Student;

// 函数声明
void printStudent(const Student *s);            // 打印学生信息
void inputStudent(Student *s);                   // 输入学生信息
float getAverageScore(const Student arr[], int n);  // 计算平均分

int main()
{
    // ===== 一、结构体变量的使用 =====
    Student s1 = {"张三", 18, 92.5, 'M'};   // 声明并初始化
    Student s2;

    // 逐个成员赋值
    strcpy(s2.name, "李四");
    s2.age = 19;
    s2.score = 88.0;
    s2.gender = 'F';

    printf("===== 学生信息 =====\n");
    printStudent(&s1);    // 传指针，避免复制整个结构体
    printStudent(&s2);

    // ===== 二、结构体数组 =====
    printf("\n===== 结构体数组 =====\n");
    Student class3[3] = {
        {"王五", 18, 85.0, 'M'},
        {"赵六", 19, 91.5, 'F'},
        {"孙七", 18, 78.5, 'M'}
    };

    for (int i = 0; i < 3; i++) {
        printf("%d. ", i + 1);
        printStudent(&class3[i]);
    }
    printf("班级平均分：%.1f\n", getAverageScore(class3, 3));

    return 0;
}

// 打印学生信息（const 表示只读，不修改）
void printStudent(const Student *s) {
    printf("%s | %d岁 | %s | 成绩：%.1f\n",
           s->name,                     // s->name 等价于 (*s).name
           s->age,
           s->gender == 'M' ? "男" : "女",
           s->score);
}

// 输入学生信息（通过指针修改）
void inputStudent(Student *s) {
    printf("姓名：");
    scanf("%s", s->name);        // s->name 是数组，不加 &
    printf("年龄：");
    scanf("%d", &s->age);        // s->age 是普通变量，要加 &
    printf("成绩：");
    scanf("%f", &s->score);
    printf("性别(M/F)：");
    scanf(" %c", &s->gender);
}

// 计算平均分
float getAverageScore(const Student arr[], int n) {
    float sum = 0;
    for (int i = 0; i < n; i++) {
        sum += arr[i].score;     // 结构体数组用 . 访问成员
    }
    return sum / n;
}
```

---

### 📋 今日核心知识点总结

1. 结构体 = 把多个相关变量"打包"成一个新类型
2. 定义结构体类型用 `struct 名字 { 成员; };`（注意分号！）
3. 访问成员：普通变量用 `.`（点），指针用 `->`（箭头）
4. `typedef` 可以给结构体类型起别名，简化代码
5. 结构体数组：`Student arr[50]`，每个元素是一个结构体

---

## Day 39：结构体（下）—— 结构体与指针、嵌套结构体

### 🎯 今日学习目标
- 掌握结构体指针（`->` 运算符）
- 理解结构体的嵌套
- 在函数间传递结构体

---

### 📖 通俗化知识点讲解

#### 1. `->` 箭头运算符

```c
Student s = {"张三", 18, 90};
Student *p = &s;       // p 是指向结构体的指针

// 访问成员的两种等价方式：
(*p).name     // 方式1：先解引用再打点（写起来麻烦）
p->name       // 方式2：用箭头（推荐！简洁明了）
```

#### 2. 结构体嵌套

```c
typedef struct {
    int year;
    int month;
    int day;
} Date;

typedef struct {
    char name[30];
    Date birthday;     // 嵌套 Date 结构体！
} Person;

Person p = {"张三", {2008, 5, 20}};
printf("出生年份：%d\n", p.birthday.year);  // 多层点号访问
```

---

### 💻 上机敲代码

```c
/*
 * 文件名：struct_advanced.c
 * 功能：结构体指针、嵌套结构体、链表节点预热
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// 日期结构体（用于嵌套）
typedef struct {
    int year;
    int month;
    int day;
} Date;

// 学生结构体（嵌套了Date）
typedef struct {
    int id;              // 学号
    char name[30];       // 姓名
    Date birthday;       // 出生日期（嵌套结构体）
    float scores[3];     // 三门课成绩
} Student;

// 函数声明
void printStudent(const Student *s);
float getTotalScore(const Student *s);
int compareByScore(const Student *a, const Student *b);

int main()
{
    // ===== 一、结构体嵌套 =====
    printf("===== 结构体嵌套 =====\n");
    Student stu1 = {
        2026001,                  // 学号
        "张三",                   // 姓名
        {2008, 3, 15},           // 出生日期
        {85.5, 92.0, 78.5}       // 三门课成绩
    };
    printStudent(&stu1);

    // ===== 二、结构体指针数组 =====
    printf("\n===== 学生成绩排名 =====\n");
    Student class2[] = {
        {1, "Alice",   {2007, 8, 10}, {90, 85, 92}},
        {2, "Bob",     {2008, 1, 22}, {78, 82, 80}},
        {3, "Charlie", {2007, 11, 5}, {95, 93, 97}},
        {4, "Diana",   {2008, 5, 18}, {88, 91, 85}},
    };
    int n = sizeof(class2) / sizeof(class2[0]);

    // 创建指针数组方便排序
    Student *rank[n];   // 指针数组！
    for (int i = 0; i < n; i++) {
        rank[i] = &class2[i];   // 每个指针指向一个学生
    }

    // 按总分排序指针数组（冒泡，只交换指针，不交换结构体数据）
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - 1 - i; j++) {
            if (compareByScore(rank[j], rank[j+1]) < 0) {
                // 只交换指针，不交换整个结构体！
                Student *temp = rank[j];
                rank[j] = rank[j+1];
                rank[j+1] = temp;
            }
        }
    }

    printf("排名\t学号\t姓名\t总分\n");
    for (int i = 0; i < n; i++) {
        printf("第%d名\t%d\t%s\t%.1f\n",
               i + 1, rank[i]->id, rank[i]->name, getTotalScore(rank[i]));
    }

    return 0;
}

void printStudent(const Student *s) {
    printf("学号：%d | 姓名：%s\n", s->id, s->name);
    printf("出生日期：%d年%d月%d日\n",
           s->birthday.year, s->birthday.month, s->birthday.day);
    printf("成绩：%.1f, %.1f, %.1f\n",
           s->scores[0], s->scores[1], s->scores[2]);
    printf("总分：%.1f\n", getTotalScore(s));
}

float getTotalScore(const Student *s) {
    return s->scores[0] + s->scores[1] + s->scores[2];
}

// 比较两个学生的总分（用于排序）
int compareByScore(const Student *a, const Student *b) {
    float diff = getTotalScore(a) - getTotalScore(b);
    if (diff > 0) return 1;
    if (diff < 0) return -1;
    return 0;
}
```

---

### 📋 今日核心知识点总结

1. 结构体指针访问成员用 `p->member`（等价于 `(*p).member`）
2. 结构体可以嵌套结构体，访问用多层 `.`
3. 指针数组排序：只交换指针，不交换结构体（效率高！）
4. 函数传结构体建议传指针（避免复制整个结构体）

---

## Day 40：联合体（union）与枚举（enum）

### 🎯 今日学习目标
- 理解联合体与结构体的关键区别
- 掌握枚举类型的使用
- 了解 typedef 的高级用法

---

### 📖 通俗化知识点讲解

#### 1. 联合体 union——同一块空间的不同"身份"

> **生活类比**：一个多功能转换插座。
> 同一个物理位置，这次插中国插头，下次插美国插头。但**同一时刻只能用一个**。

```c
union Data {
    int i;        // 4字节
    float f;      // 4字节
    char str[20]; // 20字节
};
// 联合体的大小 = 最大成员的大小（20字节）
// 所有成员共享同一块内存！修改一个会影响其他。

// vs 结构体：
struct Data {
    int i;        // 4字节
    float f;      // 4字节
    char str[20]; // 20字节
};
// 结构体大小 = 所有成员大小之和（约28字节）
// 每个成员有自己独立的内存空间
```

#### 2. 枚举 enum——给整数起"别名"

```c
enum Weekday { MON=1, TUE, WED, THU, FRI, SAT, SUN };
//             MON=1，TUE自动=2，WED=3...

enum Weekday today = WED;
printf("%d\n", today);   // 输出：3

// vs #define 和 const：
// enum 的优点：一组相关常量，有类型检查
```

---

### 💻 上机敲代码

```c
/*
 * 文件名：union_enum.c
 * 功能：联合体与枚举的使用
 */

#include <stdio.h>
#include <string.h>

// 枚举：定义一组相关的命名常量
typedef enum {
    TYPE_INT,      // 0
    TYPE_FLOAT,    // 1
    TYPE_STRING    // 2
} DataType;

// 联合体：同一块内存，不同解释方式
typedef union {
    int intValue;
    float floatValue;
    char stringValue[20];
} DataValue;

// 带标记的联合体（用枚举来标识当前存的是什么类型）
typedef struct {
    DataType type;      // 标记：这个数据是什么类型
    DataValue value;    // 数据本身
} TaggedData;

// 全局函数声明
void printTaggedData(const TaggedData *data);

int main()
{
    // ===== 一、枚举的使用 =====
    printf("===== 枚举 =====\n");
    typedef enum { RED, GREEN, BLUE } Color;   // RED=0, GREEN=1, BLUE=2
    Color myColor = BLUE;

    if (myColor == BLUE) {
        printf("我最喜欢的颜色是蓝色（编号%d）\n", myColor);
    }

    // 用 switch 处理枚举（经典模式）
    switch (myColor) {
        case RED:   printf("红色\n"); break;
        case GREEN: printf("绿色\n"); break;
        case BLUE:  printf("蓝色\n"); break;
    }

    // ===== 二、联合体的使用 =====
    printf("\n===== 联合体大小对比 =====\n");
    printf("union DataValue 大小：%d 字节\n", (int)sizeof(DataValue));
    // 输出：20（最大成员stringValue的大小）
    printf("int：%d，float：%d，char[20]：%d\n",
           (int)sizeof(int), (int)sizeof(float), 20);

    // ===== 三、带标记的联合体 =====
    printf("\n===== 标记联合体 =====\n");

    TaggedData data1;
    data1.type = TYPE_INT;
    data1.value.intValue = 42;
    printTaggedData(&data1);

    TaggedData data2;
    data2.type = TYPE_FLOAT;
    data2.value.floatValue = 3.14f;
    printTaggedData(&data2);

    TaggedData data3;
    data3.type = TYPE_STRING;
    strcpy(data3.value.stringValue, "Hello C");
    printTaggedData(&data3);

    // ⚠️ 联合体陷阱演示
    data3.value.intValue = 999;  // 覆盖了stringValue的内容！
    printf("注意！覆盖后：");
    printTaggedData(&data3);     // type还是STRING，但值是999了
    // 实际开发中，修改值后要同步更新type

    return 0;
}

void printTaggedData(const TaggedData *data) {
    printf("数据（类型=");
    switch (data->type) {
        case TYPE_INT:
            printf("整数）：%d\n", data->value.intValue);
            break;
        case TYPE_FLOAT:
            printf("浮点）：%.2f\n", data->value.floatValue);
            break;
        case TYPE_STRING:
            printf("字符串）：%s\n", data->value.stringValue);
            break;
        default:
            printf("未知）：?\n");
    }
}
```

---

### 📋 今日核心知识点总结

1. **union**：所有成员共享同一块内存，大小 = 最大成员大小
2. union 同一时刻只能存一个成员的值，修改一个影响全部
3. **enum**：给整数常量起有意义的名字，提高代码可读性
4. enum + union + struct 组合可以实现"带标记的变体类型"

---

## Day 41：动态内存分配深入

### 🎯 今日学习目标
- 掌握 `calloc` 和 `realloc`
- 理解常见内存错误（泄漏、悬挂指针、双重释放）
- 掌握动态二维数组的创建

---

### 📖 通俗化知识点讲解

#### 1. malloc 家族三兄弟

```c
// malloc：分配但不初始化（内容是随机值）
int *p1 = (int*)malloc(10 * sizeof(int));

// calloc：分配并初始化为0
int *p2 = (int*)calloc(10, sizeof(int));
// calloc(个数, 每个大小) —— 参数形式和malloc不同！

// realloc：调整已分配内存的大小
p1 = (int*)realloc(p1, 20 * sizeof(int));  // p1从10个int扩大到20个int
```

#### 2. 四大内存错误

| 错误类型 | 示例 | 后果 |
|----------|------|------|
| **内存泄漏** | malloc后忘了free | 内存逐渐耗尽 |
| **悬挂指针** | free后继续使用该指针 | 访问已释放的内存，未定义行为 |
| **双重释放** | 对同一指针free两次 | 程序崩溃 |
| **越界访问** | 访问malloc(n)的第n+1个元素 | 数据损坏或崩溃 |

```c
// 避免悬挂指针的标准做法：
free(ptr);
ptr = NULL;    // 之后如果误用ptr，至少能检测到

// 检查 malloc 的返回值！
int *p = (int*)malloc(1000000000000);  // 不可能这么大
if (p == NULL) {
    printf("内存不足！\n");
    exit(1);
}
```

---

### 💻 上机敲代码

```c
/*
 * 文件名：dynamic_memory_adv.c
 * 功能：calloc/realloc + 动态二维数组
 */

#include <stdio.h>
#include <stdlib.h>

int main()
{
    // ===== 一、malloc vs calloc =====
    printf("===== malloc vs calloc =====\n");

    int *arr1 = (int*)malloc(5 * sizeof(int));
    int *arr2 = (int*)calloc(5, sizeof(int));  // 自动初始化为0

    printf("malloc 分配（随机值）：");
    for (int i = 0; i < 5; i++) printf("%d ", arr1[i]);
    printf("\n");

    printf("calloc 分配（全为0）：");
    for (int i = 0; i < 5; i++) printf("%d ", arr2[i]);
    printf("\n");

    // ===== 二、realloc 调整大小 =====
    printf("\n===== realloc 调整大小 =====\n");

    int *arr = (int*)malloc(3 * sizeof(int));
    arr[0] = 10; arr[1] = 20; arr[2] = 30;
    printf("初始（3个元素）：%d %d %d\n", arr[0], arr[1], arr[2]);

    // 扩大为5个元素
    arr = (int*)realloc(arr, 5 * sizeof(int));
    // realloc 会保留原来的数据！
    arr[3] = 40; arr[4] = 50;
    printf("扩大后（5个元素）：%d %d %d %d %d\n",
           arr[0], arr[1], arr[2], arr[3], arr[4]);

    // 缩小为2个元素
    arr = (int*)realloc(arr, 2 * sizeof(int));
    printf("缩小后（2个元素）：%d %d\n", arr[0], arr[1]);

    free(arr);
    free(arr1);
    free(arr2);

    // ===== 三、动态二维数组 =====
    printf("\n===== 动态二维数组 =====\n");

    int rows = 3, cols = 4;

    // 方法：先分配"行指针数组"，再为每一行分配列
    int **matrix = (int**)malloc(rows * sizeof(int*));
    //  matrix 是一个指向"指针数组"的指针
    //  matrix[0] 到 matrix[rows-1] 各是一个 int*

    for (int i = 0; i < rows; i++) {
        matrix[i] = (int*)malloc(cols * sizeof(int));
        // 每一行都是一个独立的动态数组
    }

    // 使用动态二维数组（和普通二维数组一样！）
    int value = 1;
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            matrix[i][j] = value++;
        }
    }

    // 打印
    printf("动态二维数组（3行4列）：\n");
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            printf("%2d ", matrix[i][j]);
        }
        printf("\n");
    }

    // 释放动态二维数组（先释放每行，再释放行指针数组）
    for (int i = 0; i < rows; i++) {
        free(matrix[i]);    // 先释放每一行
    }
    free(matrix);            // 再释放行指针数组
    matrix = NULL;

    printf("\n动态二维数组已释放。\n");
    return 0;
}
```

---

### 📋 今日核心知识点总结

1. `calloc(n, size)`：分配+**初始化为0**
2. `realloc(ptr, newSize)`：调整大小，**保留原数据**
3. 动态二维数组：先分配行指针数组，再逐行分配
4. 释放动态二维数组：**先释放行，再释放行指针数组**
5. 每次 `malloc/calloc/realloc` 都要检查返回值是否为NULL
6. `free` 后把指针设为NULL，防止悬挂指针

---

## Day 42-43：链表入门——动态数据结构

### 🎯 今日学习目标
- 理解链表的原理和与数组的对比
- 实现单链表的创建、遍历、插入、删除
- 体会指针在数据结构中的核心作用

---

### 📖 通俗化知识点讲解

#### 1. 数组 vs 链表

> **生活类比**：
> - **数组**：电影院的一排固定座位（连续排列，有编号，但中间插入一个人需要所有人挪位置）
> - **链表**：寻宝游戏的线索纸条（每张纸条上写了下一个线索的位置，可以任意添加删除纸条，不需要移动其他纸条）

| | 数组 | 链表 |
|---|---|---|
| 内存 | 连续 | 分散 |
| 访问 | 随机访问 O(1) | 必须从头找 O(n) |
| 插入/删除 | 需要移动元素 O(n) | 只需改指针 O(1) |
| 大小 | 固定或需要realloc | 动态增长 |

#### 2. 链表节点的结构

```c
// 链表的核心：节点包含"数据 + 指向下一个节点的指针"
typedef struct Node {
    int data;            // 数据域
    struct Node *next;   // 指针域：指向下一个节点
} Node;   // 这种"自己包含指向自己的指针"叫自引用结构体
```

```
链表在内存中的样子（逻辑视图）：

[HEAD] → [data:10|next:●] → [data:20|next:●] → [data:30|next:NULL]
          节点1                 节点2                 节点3（末尾）
```

---

### 💻 上机敲代码

```c
/*
 * 文件名：linked_list.c
 * 功能：单链表的完整实现（创建、遍历、插入、删除、释放）
 */

#include <stdio.h>
#include <stdlib.h>

// 链表节点定义
typedef struct Node {
    int data;            // 数据
    struct Node *next;   // 指向下一个节点的指针
} Node;

// ===== 链表操作函数声明 =====
Node* createNode(int data);                       // 创建新节点
void insertAtHead(Node **head, int data);         // 头部插入
void insertAtTail(Node **head, int data);         // 尾部插入
void insertAfter(Node *prevNode, int data);       // 在指定节点后插入
void deleteNode(Node **head, int key);             // 删除指定值的节点
void printList(Node *head);                        // 打印链表
void freeList(Node **head);                        // 释放整个链表
int  listLength(Node *head);                       // 链表长度
Node* searchNode(Node *head, int key);             // 查找节点

int main()
{
    Node *head = NULL;   // 链表头指针，初始为空

    // ===== 一、创建链表 =====
    printf("===== 创建链表 =====\n");
    insertAtTail(&head, 10);
    insertAtTail(&head, 20);
    insertAtTail(&head, 30);
    printf("初始链表：");
    printList(head);
    printf("长度：%d\n", listLength(head));

    // ===== 二、头部插入 =====
    printf("\n===== 头部插入 =====\n");
    insertAtHead(&head, 5);
    insertAtHead(&head, 1);
    printf("头部插入5和1后：");
    printList(head);

    // ===== 三、指定位置插入 =====
    printf("\n===== 指定位置插入 =====\n");
    Node *found = searchNode(head, 20);
    if (found != NULL) {
        insertAfter(found, 25);
        printf("在20后插入25：");
        printList(head);
    }

    // ===== 四、删除节点 =====
    printf("\n===== 删除节点 =====\n");
    deleteNode(&head, 10);
    printf("删除10后：");
    printList(head);

    deleteNode(&head, 1);
    printf("删除头部1后：");
    printList(head);

    deleteNode(&head, 100);  // 删除不存在的值
    printf("尝试删除不存在的100后：");
    printList(head);

    // ===== 五、释放整个链表 =====
    printf("\n释放链表...\n");
    freeList(&head);
    printf("链表已释放，head = %p\n", (void*)head);

    return 0;
}

// ===== 链表操作函数实现 =====

// 创建新节点
Node* createNode(int data) {
    Node *newNode = (Node*)malloc(sizeof(Node));
    if (newNode == NULL) {
        printf("内存分配失败！\n");
        exit(1);
    }
    newNode->data = data;
    newNode->next = NULL;
    return newNode;
}

// 头部插入（注意：需要二级指针，因为可能要修改head！）
void insertAtHead(Node **head, int data) {
    Node *newNode = createNode(data);
    newNode->next = *head;   // 新节点的next指向原来的头
    *head = newNode;         // head 指向新节点
}

// 尾部插入
void insertAtTail(Node **head, int data) {
    Node *newNode = createNode(data);

    if (*head == NULL) {     // 链表为空？
        *head = newNode;     // 新节点就是头
        return;
    }

    // 找到最后一个节点
    Node *current = *head;
    while (current->next != NULL) {
        current = current->next;
    }
    current->next = newNode;  // 最后一个节点的next指向新节点
}

// 在指定节点后插入
void insertAfter(Node *prevNode, int data) {
    if (prevNode == NULL) {
        printf("前驱节点不能为空！\n");
        return;
    }
    Node *newNode = createNode(data);
    newNode->next = prevNode->next;   // 新节点先指向后面的
    prevNode->next = newNode;         // 前驱节点指向新节点
}

// 删除指定值的节点
void deleteNode(Node **head, int key) {
    Node *temp = *head;
    Node *prev = NULL;

    // 情况1：要删除的是头节点
    if (temp != NULL && temp->data == key) {
        *head = temp->next;   // head 指向第二个节点
        free(temp);           // 释放原来的头节点
        printf("删除了头节点%d\n", key);
        return;
    }

    // 情况2：要删除的不是头节点，先找到它
    while (temp != NULL && temp->data != key) {
        prev = temp;
        temp = temp->next;
    }

    // 没找到
    if (temp == NULL) {
        printf("未找到值为%d的节点\n", key);
        return;
    }

    // 找到了，删除它
    prev->next = temp->next;   // 跳过temp
    free(temp);
    printf("删除了节点%d\n", key);
}

// 打印链表
void printList(Node *head) {
    Node *current = head;
    while (current != NULL) {
        printf("[%d]", current->data);
        if (current->next != NULL) {
            printf(" → ");
        }
        current = current->next;
    }
    printf(" → NULL\n");
}

// 释放整个链表
void freeList(Node **head) {
    Node *current = *head;
    Node *next;
    while (current != NULL) {
        next = current->next;   // 先记住下一个
        free(current);          // 释放当前
        current = next;         // 移到下一个
    }
    *head = NULL;  // 把头指针置空，防止悬挂指针
}

// 链表长度
int listLength(Node *head) {
    int count = 0;
    Node *current = head;
    while (current != NULL) {
        count++;
        current = current->next;
    }
    return count;
}

// 查找节点
Node* searchNode(Node *head, int key) {
    Node *current = head;
    while (current != NULL) {
        if (current->data == key) {
            return current;   // 找到了，返回节点指针
        }
        current = current->next;
    }
    return NULL;   // 没找到
}
```

---

### 📋 今日核心知识点总结

1. 链表节点 = 数据域 + 指向下一个节点的指针（自引用结构体）
2. 链表优势：插入删除O(1)，不需要连续内存，动态扩展
3. 修改头指针的操作需要**二级指针**（如 insertAtHead、deleteNode）
4. 释放链表：**逐个节点释放**，不能只free头节点
5. 链表是理解数据结构的基础，也是指针应用的集大成者

---

## Day 44：第六阶段复习（Day 38-43）——结构体/链表/动态内存

### 📋 第六阶段知识清单

| 知识点 | 自测方式 |
|--------|----------|
| 结构体定义与使用 | 手写Student结构体，包含嵌套Date |
| `->` 和 `.` 的区别 | 解释 `s.name` vs `ps->name` |
| 联合体 | 说出union和struct的核心区别 |
| 枚举 | 写出星期/颜色的enum定义 |
| malloc/calloc/realloc | 说出三者的区别和使用场景 |
| 内存泄漏 | 写出malloc后忘记free的代码示例 |
| 动态二维数组 | 能手写动态二维数组的创建和释放 |
| 链表节点定义 | 写出自引用结构体 Node |
| 链表插入/删除 | 手写 insertAtHead 和 deleteNode |
| 链表遍历 | 写出打印链表所有元素的循环 |

---

## Day 45：阶段性综合项目——动态学生管理系统

### 🎯 今日学习目标
- 综合运用结构体、动态内存、链表
- 完成一个较完整的数据管理项目
- 为最后的文件操作打基础

---

### 💻 上机敲代码

```c
/*
 * 文件名：student_management_dynamic.c
 * 功能：基于链表的动态学生管理系统
 * 功能：添加、删除、查找、修改、显示全部、统计
 * 覆盖：结构体、动态内存、链表、函数指针、模块化设计
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// ===== 数据结构定义 =====
typedef struct {
    int year, month, day;
} Date;

typedef struct Student {
    int id;                  // 学号
    char name[30];           // 姓名
    char gender;             // 性别
    Date birthday;           // 生日
    float score;             // 成绩
    struct Student *next;    // 链表指针
} Student;

// ===== 函数声明 =====
Student* createStudent(int id, const char *name, char gender,
                       int y, int m, int d, float score);
void insertStudent(Student **head, Student *newStu);
void deleteStudent(Student **head, int id);
Student* findStudent(Student *head, int id);
void modifyScore(Student *head, int id, float newScore);
void printAll(Student *head);
void printStatistics(Student *head);
void freeAll(Student **head);
void showMenu(void);

int main()
{
    Student *head = NULL;
    int choice, id, y, m, d;
    char name[30], gender;
    float score;

    // 预置一些测试数据
    insertStudent(&head, createStudent(1001, "Alice",   'F', 2007, 8, 10, 90.5));
    insertStudent(&head, createStudent(1002, "Bob",     'M', 2007, 3, 22, 78.0));
    insertStudent(&head, createStudent(1003, "Charlie", 'M', 2008, 1, 15, 95.5));

    while (1) {
        showMenu();
        printf("请选择：");
        scanf("%d", &choice);
        getchar();  // 吃掉换行符

        switch (choice) {
            case 1:  // 添加学生
                printf("学号："); scanf("%d", &id);
                if (findStudent(head, id)) {
                    printf("❌ 学号已存在！\n"); break;
                }
                printf("姓名："); scanf("%s", name);
                printf("性别(M/F)："); scanf(" %c", &gender);
                printf("生日(年 月 日)："); scanf("%d %d %d", &y, &m, &d);
                printf("成绩："); scanf("%f", &score);
                insertStudent(&head, createStudent(id, name, gender, y, m, d, score));
                printf("✅ 添加成功！\n");
                break;

            case 2:  // 删除学生
                printf("要删除的学号："); scanf("%d", &id);
                deleteStudent(&head, id);
                break;

            case 3:  // 查找学生
                printf("要查找的学号："); scanf("%d", &id);
                Student *found = findStudent(head, id);
                if (found) {
                    printf("学号：%d | 姓名：%s | 性别：%c | ",
                           found->id, found->name, found->gender);
                    printf("生日：%d-%d-%d | 成绩：%.1f\n",
                           found->birthday.year, found->birthday.month,
                           found->birthday.day, found->score);
                } else {
                    printf("未找到学号%d\n", id);
                }
                break;

            case 4:  // 修改成绩
                printf("学号："); scanf("%d", &id);
                printf("新成绩："); scanf("%f", &score);
                modifyScore(head, id, score);
                break;

            case 5:  // 显示全部
                printAll(head);
                break;

            case 6:  // 统计
                printStatistics(head);
                break;

            case 0:  // 退出
                freeAll(&head);
                printf("感谢使用，再见！\n");
                return 0;

            default:
                printf("❌ 无效选项！\n");
        }
    }
}

void showMenu(void) {
    printf("\n╔══════════════════════════════╗\n");
    printf("║  动态学生管理系统（链表版）  ║\n");
    printf("╠══════════════════════════════╣\n");
    printf("║ 1. 添加学生   2. 删除学生   ║\n");
    printf("║ 3. 查找学生   4. 修改成绩   ║\n");
    printf("║ 5. 显示全部   6. 成绩统计   ║\n");
    printf("║ 0. 退出                     ║\n");
    printf("╚══════════════════════════════╝\n");
}

Student* createStudent(int id, const char *name, char gender,
                       int y, int m, int d, float score) {
    Student *s = (Student*)malloc(sizeof(Student));
    if (s == NULL) { printf("内存不足！\n"); exit(1); }
    s->id = id;
    strcpy(s->name, name);
    s->gender = gender;
    s->birthday.year = y;
    s->birthday.month = m;
    s->birthday.day = d;
    s->score = score;
    s->next = NULL;
    return s;
}

void insertStudent(Student **head, Student *newStu) {
    newStu->next = *head;  // 头插法（简单高效）
    *head = newStu;
}

void deleteStudent(Student **head, int id) {
    Student *curr = *head, *prev = NULL;
    while (curr != NULL && curr->id != id) {
        prev = curr;
        curr = curr->next;
    }
    if (curr == NULL) {
        printf("未找到学号%d\n", id);
        return;
    }
    if (prev == NULL) *head = curr->next;  // 删除头节点
    else prev->next = curr->next;
    free(curr);
    printf("✅ 删除成功！\n");
}

Student* findStudent(Student *head, int id) {
    Student *curr = head;
    while (curr != NULL) {
        if (curr->id == id) return curr;
        curr = curr->next;
    }
    return NULL;
}

void modifyScore(Student *head, int id, float newScore) {
    Student *s = findStudent(head, id);
    if (s) {
        printf("成绩 %.1f → %.1f\n", s->score, newScore);
        s->score = newScore;
    } else {
        printf("未找到学号%d\n", id);
    }
}

void printAll(Student *head) {
    if (head == NULL) { printf("暂无学生数据。\n"); return; }
    printf("\n学号\t姓名\t性别\t生日\t\t成绩\n");
    printf("──────────────────────────────────────\n");
    Student *curr = head;
    while (curr != NULL) {
        printf("%d\t%s\t%c\t%d-%02d-%02d\t%.1f\n",
               curr->id, curr->name, curr->gender,
               curr->birthday.year, curr->birthday.month, curr->birthday.day,
               curr->score);
        curr = curr->next;
    }
}

void printStatistics(Student *head) {
    if (head == NULL) { printf("暂无学生数据。\n"); return; }
    int count = 0, pass = 0;
    float sum = 0, max = -1, min = 101;
    Student *curr = head;
    while (curr != NULL) {
        count++;
        sum += curr->score;
        if (curr->score > max) max = curr->score;
        if (curr->score < min) min = curr->score;
        if (curr->score >= 60) pass++;
        curr = curr->next;
    }
    printf("\n===== 成绩统计 =====\n");
    printf("学生人数：%d\n", count);
    printf("平均分：%.1f\n", sum / count);
    printf("最高分：%.1f\n", max);
    printf("最低分：%.1f\n", min);
    printf("及格率：%.1f%%\n", 100.0 * pass / count);
}

void freeAll(Student **head) {
    Student *curr = *head;
    while (curr != NULL) {
        Student *next = curr->next;
        free(curr);
        curr = next;
    }
    *head = NULL;
}
```

---

### 📋 今日核心知识点总结

1. 综合运用了到目前为止所学的几乎所有知识
2. 链表版学生管理系统 vs 数组版：无需预设大小，学生数量无限扩展
3. 程序的数据**只存在于内存中**，关掉程序就没了 → 下一阶段学文件操作解决这个问题！

---

> 📌 **继续学习**：Day 46-60 见 module-2 Part 4（文件操作 + 综合项目 + 总复习）
