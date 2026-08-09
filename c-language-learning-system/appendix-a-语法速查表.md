# 附录A：C语言常用语法速查表

> 📌 适合打印成一张A4纸，贴在书桌前随时查阅。

---

## 一、程序基本结构

```c
#include <stdio.h>        // 头文件
#define PI 3.14159        // 宏常量

int main() {              // 主函数
    // 你的代码
    return 0;             // 返回值
}
```

---

## 二、数据类型

| 类型 | 关键字 | 占位符(printf) | 占位符(scanf) | 大小(字节) |
|------|--------|---------------|---------------|-----------|
| 整数 | `int` | `%d` | `%d` | 4 |
| 长整数 | `long long` | `%lld` | `%lld` | 8 |
| 单精度 | `float` | `%f` | `%f` | 4 |
| 双精度 | `double` | `%f` / `%lf` | `%lf` | 8 |
| 字符 | `char` | `%c` | ` %c` | 1 |
| 字符串 | `char[]` | `%s` | `%s` | — |

---

## 三、运算符优先级（高→低）

| 优先级 | 运算符 | 结合性 |
|--------|--------|--------|
| 1 | `()` `[]` `->` `.` | 左→右 |
| 2 | `!` `~` `++` `--` `+` `-` `*` `&` `(type)` `sizeof` | 右→左 |
| 3 | `*` `/` `%` | 左→右 |
| 4 | `+` `-` | 左→右 |
| 5 | `<<` `>>` | 左→右 |
| 6 | `<` `<=` `>` `>=` | 左→右 |
| 7 | `==` `!=` | 左→右 |
| 8 | `&`（按位与） | 左→右 |
| 9 | `^` | 左→右 |
| 10 | `|` | 左→右 |
| 11 | `&&` | 左→右 |
| 12 | `||` | 左→右 |
| 13 | `?:` | 右→左 |
| 14 | `=` `+=` `-=` `*=` `/=` `%=` | 右→左 |
| 15 | `,` | 左→右 |

---

## 四、控制结构速查

```c
// if-else
if (条件) { } else if (条件) { } else { }

// switch
switch (整数表达式) {
    case 值1: ...; break;
    case 值2: ...; break;
    default:  ...; break;
}

// for 循环
for (初始化; 条件; 更新) { }

// while 循环
while (条件) { }

// do-while 循环
do { } while (条件);   // ← 注意分号！
```

---

## 五、数组

```c
// 一维数组
类型 数组名[大小] = {值1, 值2, ...};
int arr[5] = {1, 2, 3, 4, 5};
int size = sizeof(arr) / sizeof(arr[0]);

// 二维数组
类型 数组名[行数][列数];
int matrix[3][4] = {{1,2,3,4}, {5,6,7,8}, {9,10,11,12}};

// 字符数组（字符串）
char str[20] = "Hello";          // 自动加\0
char str[] = {'H','e','l','l','o','\0'};  // 手动加\0
```

---

## 六、函数

```c
// 声明
返回类型 函数名(参数类型列表);

// 定义
返回类型 函数名(参数列表) {
    // 函数体
    return 值;  // void类型不需要return
}

// 递归模板
返回类型 递归函数(参数) {
    if (基准条件) return 基准值;  // 停止条件
    return 递归函数(缩小后的参数); // 递归调用
}
```

---

## 七、指针

```c
// 基本语法
int x = 10;
int *p = &x;     // p指向x
*p = 20;         // 通过p修改x
int **pp = &p;   // 二级指针

// 指针与数组
int arr[] = {1,2,3};
int *p = arr;         // p指向arr[0]
arr[i] == *(arr + i)  // 两者等价！

// 动态内存
int *p = (int*)malloc(n * sizeof(int));   // 分配
int *p = (int*)calloc(n, sizeof(int));    // 分配+清零
p = (int*)realloc(p, newSize);            // 调整大小
free(p);    // 释放
p = NULL;   // 防止悬挂指针

// 函数指针
返回类型 (*指针名)(参数类型列表);
例：int (*op)(int, int) = &add;
```

---

## 八、结构体

```c
// 定义
typedef struct {
    类型1 成员1;
    类型2 成员2;
} 类型别名;

// 声明与初始化
类型别名 变量名 = {值1, 值2};

// 访问成员
变量名.成员        // 普通变量用 .
指针->成员         // 指针变量用 ->
(*指针).成员       // 等价于上面

// 链表节点
typedef struct Node {
    int data;
    struct Node *next;   // 自引用指针
} Node;
```

---

## 九、文件操作

```c
FILE *fp = fopen("文件名", "模式");   // 打开
fclose(fp);                           // 关闭

// 模式： "r"只读 "w"只写(清空) "a"追加 "rb"/"wb"二进制

// 读写函数
fprintf(fp, "格式", ...);      // 格式化写
fscanf(fp, "格式", ...);       // 格式化读
fgets(buf, size, fp);          // 读一行（保留\n）
fputs(str, fp);                // 写字符串
fwrite(ptr, size, n, fp);      // 二进制写
fread(ptr, size, n, fp);       // 二进制读
fgetc(fp) / fputc(ch, fp);     // 单字符读写

// 文件定位
fseek(fp, offset, SEEK_SET);   // 定位（SET/CUR/END）
ftell(fp);                      // 获取当前位置
rewind(fp);                     // 回到开头

// 状态检测
feof(fp);    // 是否到末尾（先读再检测！）
ferror(fp);  // 是否有错误
fflush(fp);  // 强制刷新缓冲区
```

---

## 十、常用库函数

### `<stdio.h>`
`printf`, `scanf`, `fopen`, `fclose`, `fprintf`, `fscanf`, `fgets`, `fputs`, `fgetc`, `fputc`, `fread`, `fwrite`, `fseek`, `ftell`, `rewind`, `feof`, `ferror`, `fflush`, `sprintf`, `sscanf`

### `<stdlib.h>`
`malloc`, `calloc`, `realloc`, `free`, `rand`, `srand`, `exit`, `atoi`, `atof`, `abs`

### `<string.h>`
`strlen`, `strcpy`, `strncpy`, `strcmp`, `strncmp`, `strcat`, `strncat`, `strchr`, `strstr`, `strtok`, `memset`, `memcpy`

### `<ctype.h>`
`isalpha`, `isdigit`, `isalnum`, `isupper`, `islower`, `isspace`, `toupper`, `tolower`

### `<math.h>`
`pow`, `sqrt`, `sin`, `cos`, `tan`, `log`, `exp`, `fabs`, `ceil`, `floor`, `round`

### `<time.h>`
`time`, `clock`, `difftime`

---

## 十一、常用编译命令（gcc/MinGW）

```bash
gcc file.c -o output.exe          # 编译为可执行文件
gcc -Wall file.c -o output.exe    # 显示所有警告
gcc -g file.c -o output.exe       # 包含调试信息
gcc -O2 file.c -o output.exe      # 优化编译
gcc -c file.c -o file.o           # 只编译不链接
gcc file1.c file2.c -o output.exe # 多文件编译
```

---

## 十二、C语言关键字（32个）

```
auto     break    case     char     const    continue
default  do       double   else     enum     extern
float    for      goto     if       int      long
register return   short    signed   sizeof   static
struct   switch   typedef  union    unsigned void
volatile while
```

> 📌 这些关键字不能用作变量名！

---

## 十三、常见代码模式速查

```c
// 交换两个变量
temp = a; a = b; b = temp;

// 判断闰年
(year % 4 == 0 && year % 100 != 0) || (year % 400 == 0)

// 数字反转
while (n > 0) { rev = rev*10 + n%10; n /= 10; }

// 判断素数
int isPrime = 1;
for (int i = 2; i*i <= n; i++)
    if (n % i == 0) { isPrime = 0; break; }

// 冒泡排序
for (int i=0; i<n-1; i++)
    for (int j=0; j<n-1-i; j++)
        if (arr[j] > arr[j+1]) { 交换 }

// 数组最大值
int max = arr[0];
for (int i=1; i<n; i++)
    if (arr[i] > max) max = arr[i];

// 安全的malloc
int *p = (int*)malloc(n * sizeof(int));
if (p == NULL) { printf("内存不足\n"); exit(1); }
// 使用后
free(p); p = NULL;
```
