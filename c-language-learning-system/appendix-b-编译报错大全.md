# 附录B：编译报错大全（30+常见报错中英对照+修复方案）

> 📌 遇到报错不要慌，按 `Ctrl+F` 搜索报错关键词，找到对应的原因和解决方案。

---

## 使用说明

每一条按照以下格式组织：
- **报错信息**（原文）
- **中文解释**
- **常见原因**
- **修复方案**
- **示例代码**

---

## 一、编译阶段错误（Compilation Errors）

### 1. `error: expected ';' before 'xxx'`

**中文**：在xxx之前缺少分号

**常见原因**：上一行语句末尾忘了分号

**修复**：在提示的行号**上一行**末尾加分号

```c
// ❌ 错误
printf("Hello")
return 0;

// ✅ 正确
printf("Hello");
return 0;
```

---

### 2. `error: 'xxx' undeclared (first use in this function)`

**中文**：xxx未声明就被使用了

**常见原因**：
- 变量名拼写错误
- 忘记声明变量
- 忘记 `#include` 对应的头文件

**修复**：检查拼写，确保变量在使用前已声明

```c
// ❌ 错误
printf("%d", score);  // score没有声明

// ✅ 正确
int score = 90;
printf("%d", score);
```

---

### 3. `error: expected ')' before ';' token`

**中文**：在分号之前缺少右括号

**常见原因**：括号不匹配，多了一个分号在括号里面

```c
// ❌ 错误
if (x > 0;) { }   // 条件表达式里多了分号

// ✅ 正确
if (x > 0) { }
```

---

### 4. `error: expected '}' at end of input`

**中文**：在文件末尾缺少右大括号

**常见原因**：某个 `{` 没有对应的 `}`

**修复**：检查所有大括号是否成对。VS Code中可以双击 `{` 来高亮匹配的 `}`。

---

### 5. `error: lvalue required as left operand of assignment`

**中文**：赋值运算符左边不是一个可修改的左值

**常见原因**：试图给常量或表达式赋值

```c
// ❌ 错误
5 = x;           // 不能给数字5赋值
x + y = 10;      // 不能给表达式赋值
"hello" = str;   // 不能给字符串常量赋值
```

---

### 6. `error: invalid operands to binary %`

**中文**：取余运算符 `%` 的操作数无效

**常见原因**：对浮点数使用了 `%`（取余只能用于整数）

```c
// ❌ 错误
float x = 5.0;
int result = x % 2;   // %不能用于float！

// ✅ 正确
int x = 5;
int result = x % 2;
```

---

### 7. `error: assignment to expression with array type`

**中文**：试图给数组类型的表达式赋值

**常见原因**：试图给数组名（常量指针）重新赋值

```c
// ❌ 错误
char str[20];
str = "Hello";   // 数组名不能赋值！用strcpy

// ✅ 正确
char str[20];
strcpy(str, "Hello");
```

---

### 8. `error: too few arguments to function 'xxx'`

**中文**：函数xxx的参数不够

**常见原因**：调用函数时传的参数少于声明时的参数个数

```c
// ❌ 错误
printf("%d %d", 10);   // 需要2个参数，只给了1个

// ✅ 正确
printf("%d %d", 10, 20);
```

---

### 9. `error: conflicting types for 'xxx'`

**中文**：类型冲突（函数声明和定义不一致）

**常见原因**：函数的声明和定义的返回类型或参数类型不一致

---

### 10. `error: redefinition of 'xxx'`

**中文**：重复定义了xxx

**常见原因**：同一个变量名在同一作用域被定义了两次

---

### 11. `error: subscripted value is neither array nor pointer`

**中文**：对非数组/非指针类型使用了 `[]` 下标

**常见原因**：对一个普通变量使用了数组下标

```c
// ❌ 错误
int x = 10;
printf("%d", x[0]);   // x不是数组也不是指针！

// ✅ 正确
int arr[] = {10};
printf("%d", arr[0]);
```

---

### 12. `error: void value not ignored as it ought to be`

**中文**：void类型的返回值被当作有值使用了

**常见原因**：试图接收void函数的返回值

```c
// ❌ 错误
void f() { }
int x = f();   // f没有返回值！

// ✅ 正确
f();   // 直接调用，不接收返回值
```

---

### 13. `error: dereferencing pointer to incomplete type`

**中文**：解引用了一个不完整类型的指针

**常见原因**：使用了未定义的结构体指针，或缺少头文件

---

### 14. `warning: implicit declaration of function 'xxx'`

**中文**（警告）：函数xxx被隐式声明

**常见原因**：调用了函数但忘记 `#include` 对应的头文件或写函数声明

**修复**：添加对应的 `#include` 或函数声明

```c
// ❌ 警告（可能导致运行时错误）
int main() {
    printf("%d\n", strlen("hi"));  // 忘记 #include <string.h>
}

// ✅ 正确
#include <string.h>
int main() {
    printf("%d\n", strlen("hi"));
}
```

---

### 15. `warning: comparison between signed and unsigned`

**中文**（警告）：有符号和无符号类型比较

**常见原因**：`int` 和 `unsigned int` 或 `size_t` 混用

---

### 16. `warning: unused variable 'xxx'`

**中文**（警告）：变量xxx声明了但从未使用

**修复**：删除不需要的变量，或者如果真的不需要了就删掉声明

---

## 二、链接阶段错误（Linker Errors）

### 17. `undefined reference to 'xxx'`

**中文**：找不到xxx的定义（链接错误）

**常见原因**：
- 函数声明了但没有写函数体
- 多文件编译时漏了某个 `.c` 文件
- 函数名拼写错误

**修复**：检查函数是否真的有实现，多文件编译时确保所有 `.c` 文件都参与编译

```bash
# ❌ 只编译了main.c，student.c没编
gcc main.c -o program

# ✅ 两个都编译
gcc main.c student.c -o program
```

---

### 18. `multiple definition of 'xxx'`

**中文**：xxx被多次定义

**常见原因**：在 `.h` 文件中定义了函数体（不只是声明），然后被多个 `.c` 文件包含

**修复**：`.h` 文件只放声明，不放函数体（定义）

---

## 三、运行时错误（Runtime Errors）

### 19. `Segmentation fault`（段错误）

**中文**：段错误——程序访问了不该访问的内存

**最常见的原因**：
- 解引用NULL指针
- 解引用野指针（未初始化的指针）
- 数组越界访问
- 使用已释放的内存（悬挂指针）
- 栈溢出（递归太深或局部数组太大）

```c
// ❌ 会导致段错误
int *p = NULL;
*p = 10;           // 解引用空指针！

int *q;            // 未初始化
*q = 20;           // 野指针！

int arr[5];
arr[100] = 42;     // 数组越界！

int *r = malloc(10);
free(r);
*r = 30;           // 使用已释放的内存！
```

---

### 20. `Stack overflow`（栈溢出）

**中文**：栈空间耗尽

**常见原因**：
- 递归没有正确的基准条件（无限递归）
- 局部数组太大

---

### 21. 程序输出乱码

**常见原因**：
- 字符串没有 `\0` 结尾
- printf的占位符和参数类型不匹配
- 中文编码问题（UTF-8 vs GBK）

---

### 22. 死循环——程序一直运行不停止

**常见原因**：
- while循环的更新条件忘记了
- for循环的条件永远不会为假
- 递归没有正确的基准条件

---

### 23. `double free or corruption`

**中文**：重复释放或内存损坏

**常见原因**：对同一个指针 `free` 了两次

---

## 四、逻辑错误（不报错但结果不对）

### 24. `=` 和 `==` 混淆

```c
// ❌ 逻辑错误：if里的条件是赋值不是比较！
if (x = 5) {  // 永远为真！因为赋值表达式值是5（非0=真）
    printf("总是执行\n");
}

// ✅ 正确
if (x == 5) {
    printf("x等于5时执行\n");
}
```

---

### 25. 整数除法截断

```c
// ❌ 结果是2不是2.5
float result = 5 / 2;

// ✅ 正确
float result = 5.0 / 2;   // 或者 (float)5 / 2
```

---

### 26. 数组下标从0开始

```c
int arr[5] = {10, 20, 30, 40, 50};
// arr[0]=10, arr[1]=20, ..., arr[4]=50
// arr[5] 不存在！访问会越界！
```

---

### 27. scanf的 `&` 忘记写

```c
// ❌ 编译可能不报错但运行崩溃
int x;
scanf("%d", x);   // 忘了 &

// ✅ 正确
scanf("%d", &x);
```

---

### 28. fgets保留了换行符

```c
char line[100];
fgets(line, 100, stdin);
// line末尾可能有 \n，需要手动去掉
line[strcspn(line, "\n")] = '\0';
```

---

### 29. feof的使用陷阱

```c
// ❌ 错误：最后一行会输出两次
while (!feof(fp)) {
    fscanf(fp, "%s", buf);
    printf("%s\n", buf);
}

// ✅ 正确：用fscanf的返回值判断
while (fscanf(fp, "%s", buf) == 1) {
    printf("%s\n", buf);
}
```

---

### 30. 忘记字符串结尾的 `\0`

```c
// ❌ 字符数组没有\0，%s输出会出问题
char str[] = {'H', 'i'};
printf("%s\n", str);  // 输出 Hi 后面跟乱码

// ✅ 正确
char str[] = "Hi";  // 自动加\0
// 或 char str[] = {'H', 'i', '\0'};
```

---

### 31. switch 忘记 break

```c
// ❌ 会"穿透"执行
switch (n) {
    case 1: printf("一");
    case 2: printf("二");  // n=1时会打印"一二"！
}

// ✅ 正确
switch (n) {
    case 1: printf("一"); break;
    case 2: printf("二"); break;
}
```

---

### 32. 返回局部变量的地址

```c
// ❌ 危险！返回后局部变量内存已释放
int* func() {
    int x = 10;
    return &x;   // 悬挂指针！
}

// ✅ 正确：用 static 或 malloc
int* func() {
    int *p = malloc(sizeof(int));
    *p = 10;
    return p;   // 调用者负责free
}
```

---

## 五、VS Code / MinGW 环境特定问题

### 中文乱码

**症状**：printf输出中文显示为乱码

**方案1**：编译时加参数
```bash
gcc -fexec-charset=GBK file.c -o file.exe
```

**方案2**：VS Code右下角将编码从UTF-8切换为GBK

---

### `gcc : 无法将"gcc"项识别为 cmdlet...`

**原因**：MinGW没有正确添加到系统PATH

**修复**：回到 module-1 的环境搭建部分，重新配置环境变量

---

### F5调试报错 `launch: program does not exist`

**原因**：没有先保存+编译

**修复**：先 `Ctrl+S` 保存，再按F5

---

> 📌 **排错黄金法则**：先看行号定位 → 看错误类型 → 查本附录 → 自己调试10分钟 → 搜索引擎 → 最后再问人。
