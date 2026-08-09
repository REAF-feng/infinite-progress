# 模块2：分阶段逐天讲课讲义（Day 46 - Day 60）

> 📌 最后一阶段！学完文件操作，你的程序就能"记住"数据了。加上综合项目和总复习，暑假筑基圆满完成。

---

## Day 46：文件操作（上）—— 文件的打开与关闭

### 🎯 今日学习目标
学完后你能：
- 理解文件指针 `FILE*` 的概念
- 掌握 `fopen()` 的各种模式
- 正确关闭文件（`fclose()`）

---

### 📖 通俗化知识点讲解

#### 1. 为什么需要文件操作？

> **生活类比**：之前写的程序就像在**黑板上演算**——程序一关，数据全部消失。
> 文件操作 = 把数据写在**笔记本**上——关了电脑，数据还在硬盘里。

#### 2. 文件操作的基本流程

```
打开文件(fopen) → 读写操作 → 关闭文件(fclose)
```

```c
FILE *fp;   // 文件指针，不是真的指向文件，而是指向一个"文件信息结构体"

fp = fopen("data.txt", "w");   // 打开（或创建）文件用于写入
if (fp == NULL) {
    printf("文件打开失败！\n");
    return 1;
}
// ... 读写操作 ...
fclose(fp);   // 必须关闭！否则数据可能没写入硬盘
```

#### 3. fopen 的打开模式

| 模式 | 含义 | 文件不存在时 | 文件存在时 |
|------|------|-------------|-----------|
| `"r"` | 只读 | 报错 | 从头读 |
| `"w"` | 只写 | 创建新文件 | **清空原内容** |
| `"a"` | 追加 | 创建新文件 | 在末尾追加 |
| `"r+"` | 读写 | 报错 | 从头读写 |
| `"w+"` | 读写 | 创建新文件 | **清空原内容** |
| `"a+"` | 读写+追加 | 创建新文件 | 在末尾追加 |

> ⚠️ `"w"` 模式会**清空文件原有内容**！如果不想覆盖，用 `"a"` 追加模式。

---

### 💻 上机敲代码

```c
/*
 * 文件名：file_open_close.c
 * 功能：文件的打开、写入、关闭
 */

#include <stdio.h>
#include <stdlib.h>   // exit()

int main()
{
    FILE *fp;

    // ===== 一、写入模式 "w" =====
    fp = fopen("hello.txt", "w");   // 在当前目录创建 hello.txt
    if (fp == NULL) {
        printf("❌ 无法创建文件！请检查磁盘空间和权限。\n");
        return 1;
    }
    printf("✅ 文件 hello.txt 创建成功！\n");

    // 写入一些内容（明天详细讲fprintf）
    fprintf(fp, "Hello, 这是我写入文件的第一行文字！\n");
    fprintf(fp, "文件操作是C语言的重要技能。\n");

    fclose(fp);   // 关闭文件，数据真正写入硬盘
    printf("✅ 数据已写入，文件已关闭。\n");

    // ===== 二、追加模式 "a" =====
    fp = fopen("hello.txt", "a");   // 追加模式，不清空原有内容
    if (fp == NULL) {
        printf("❌ 无法打开文件！\n");
        return 1;
    }
    fprintf(fp, "这一行是追加的，不会覆盖前面的内容。\n");
    fclose(fp);
    printf("✅ 追加内容成功！\n");

    // ===== 三、只读模式 "r" =====
    fp = fopen("hello.txt", "r");   // 只读模式
    if (fp == NULL) {
        printf("❌ 文件不存在！\n");
        return 1;
    }
    printf("\n===== 文件内容 =====\n");

    // 逐行读取（明天详细讲fgets）
    char line[256];
    while (fgets(line, sizeof(line), fp) != NULL) {
        printf("%s", line);   // line里自带换行符，不用再加\n
    }

    fclose(fp);

    // ===== 四、打开不存在的文件 =====
    fp = fopen("not_exist.txt", "r");
    if (fp == NULL) {
        printf("\n⚠️ not_exist.txt 不存在，无法以只读模式打开。\n");
        printf("   这就是为什么要检查 fopen 的返回值！\n");
    }

    return 0;
}
```

---

### 📋 今日核心知识点总结

1. `FILE *fp = fopen("文件名", "模式")` 打开文件
2. `fclose(fp)` 关闭文件——**必须做**！不然数据可能丢失
3. 永远检查 `fopen` 的返回值是否为 NULL
4. `"w"` 会清空原有内容，`"a"` 在末尾追加，`"r"` 只读
5. 文件路径中建议用 `/` 或 `\\`，不用单个 `\`

---

## Day 47：文件操作（中）—— 文件读写函数

### 🎯 今日学习目标
学完后你能：
- 使用 `fprintf`/`fscanf` 读写格式化文本
- 使用 `fgets`/`fputs` 读写字符串
- 使用 `fread`/`fwrite` 读写二进制数据
- 区分文本文件和二进制文件

---

### 📖 通俗化知识点讲解

#### 1. 文件读写函数一览

| 函数 | 方向 | 用途 | 类似屏幕版 |
|------|------|------|-----------|
| `fprintf(fp, ...)` | 写 | 格式化写入 | `printf(...)` |
| `fscanf(fp, ...)` | 读 | 格式化读取 | `scanf(...)` |
| `fputs(str, fp)` | 写 | 写入字符串 | `puts(str)` |
| `fgets(str, n, fp)` | 读 | 读取一行字符串 | `gets(str)`(已废弃) |
| `fputc(ch, fp)` | 写 | 写入单个字符 | `putchar(ch)` |
| `fgetc(fp)` | 读 | 读取单个字符 | `getchar()` |
| `fwrite(ptr,sz,n,fp)` | 写 | 写入二进制块 | — |
| `fread(ptr,sz,n,fp)` | 读 | 读取二进制块 | — |

> **记忆口诀**：屏幕版的函数名前加 `f`，再加一个文件指针参数。
> `printf(...)` → `fprintf(fp, ...)`
> `scanf(...)` → `fscanf(fp, ...)`

#### 2. 文本文件 vs 二进制文件

| | 文本文件 | 二进制文件 |
|---|---|---|
| 存储格式 | 人类可读的字符 | 计算机内部的二进制 |
| 打开方式 | 任何文本编辑器 | 需要专门工具 |
| 例子 | .txt .c .csv | .exe .jpg .mp3 |
| C语言函数 | fprintf/fscanf | fwrite/fread |
| 优点 | 人类可读可编辑 | 体积小，读写快 |
| 缺点 | 体积大，有精度损失 | 人类不可读 |

---

### 💻 上机敲代码

```c
/*
 * 文件名：file_read_write.c
 * 功能：文件读写函数综合演示
 */

#include <stdio.h>
#include <stdlib.h>

// 学生结构体（用于二进制读写演示）
typedef struct {
    int id;
    char name[30];
    float score;
} Student;

int main()
{
    // ===== 一、fprintf / fscanf 格式化读写 =====
    printf("===== fprintf / fscanf 演示 =====\n");

    // 写入
    FILE *fp = fopen("scores.txt", "w");
    if (fp == NULL) { printf("文件创建失败！\n"); return 1; }

    fprintf(fp, "张三 85\n");     // 像printf一样用，只是输出到文件
    fprintf(fp, "李四 92\n");
    fprintf(fp, "王五 78\n");
    fclose(fp);

    // 读取
    fp = fopen("scores.txt", "r");
    if (fp == NULL) { printf("文件打开失败！\n"); return 1; }

    char name[30];
    int score;
    printf("从文件读取的成绩：\n");
    while (fscanf(fp, "%s %d", name, &score) == 2) {
        // fscanf 返回值 = 成功读取的项数
        // 读到文件末尾或格式不匹配时返回值 < 2
        printf("  %s: %d分\n", name, score);
    }
    fclose(fp);

    // ===== 二、fgets / fputs 行读写 =====
    printf("\n===== fgets / fputs 演示 =====\n");

    fp = fopen("notes.txt", "w");
    if (fp == NULL) { printf("文件创建失败！\n"); return 1; }

    fputs("第一行：今天学了文件操作。\n", fp);
    fputs("第二行：fgets可以读一行。\n", fp);
    fputs("第三行：fputs可以写一行。\n", fp);
    fclose(fp);

    fp = fopen("notes.txt", "r");
    if (fp == NULL) { printf("文件打开失败！\n"); return 1; }

    char line[256];
    int lineNum = 1;
    printf("逐行读取：\n");
    while (fgets(line, sizeof(line), fp) != NULL) {
        printf("  第%d行: %s", lineNum, line);
        // fgets保留换行符，所以line里已经有\n了
        lineNum++;
    }
    fclose(fp);

    // ===== 三、fwrite / fread 二进制读写 =====
    printf("\n===== fwrite / fread 二进制读写 =====\n");

    // 准备数据
    Student students[2] = {
        {1001, "Alice", 90.5},
        {1002, "Bob",   85.0}
    };

    // 二进制写入
    fp = fopen("students.dat", "wb");   // "wb" = 二进制写模式
    if (fp == NULL) { printf("文件创建失败！\n"); return 1; }

    fwrite(students, sizeof(Student), 2, fp);
    //      数据地址    每个元素大小  元素个数  文件指针
    fclose(fp);
    printf("已将2个学生数据以二进制格式写入 students.dat\n");

    // 二进制读取
    Student readBack[2] = {0};   // 初始化为0
    fp = fopen("students.dat", "rb");   // "rb" = 二进制读模式
    if (fp == NULL) { printf("文件打开失败！\n"); return 1; }

    size_t itemsRead = fread(readBack, sizeof(Student), 2, fp);
    fclose(fp);

    printf("从文件读取了 %d 个学生：\n", (int)itemsRead);
    for (int i = 0; i < (int)itemsRead; i++) {
        printf("  学号：%d, 姓名：%s, 成绩：%.1f\n",
               readBack[i].id, readBack[i].name, readBack[i].score);
    }

    // 查看二进制文件和文本文件的大小差异
    printf("\n提示：可以用记事本打开 scores.txt 看，但不要用记事本打开 students.dat\n");

    return 0;
}
```

---

### 📋 今日核心知识点总结

1. `fprintf` / `fscanf` = 文件版的 `printf` / `scanf`
2. `fscanf` 返回值 = 成功读取的项数，可用来判断是否读到文件末尾
3. `fgets` 保留换行符 `\n`，通常不需要额外加换行
4. `fwrite` / `fread` 用于二进制文件，参数需要地址、元素大小、元素个数
5. 二进制模式：`"wb"`（写）、`"rb"`（读）；文本模式：`"w"`、`"r"`

---

## Day 48：文件操作（下）—— 文件定位与错误处理

### 🎯 今日学习目标
- 使用 `fseek`/`ftell`/`rewind` 在文件中定位
- 掌握 `feof`/`ferror` 判断文件状态
- 了解文件缓冲区（`fflush`）

---

### 📖 通俗化知识点讲解

#### 1. 文件位置指针

> **生活类比**：在Word文档里写东西。
> - 光标在哪，就从哪开始写/读——这就是"文件位置指针"
> - `ftell` = 告诉你光标在什么位置
> - `fseek` = 把光标移动到指定位置
> - `rewind` = 光标回到文档最开头

```c
// ftell：获取当前位置（距文件开头的字节数）
long pos = ftell(fp);

// fseek：移动位置指针
fseek(fp, 0, SEEK_SET);   // 移到开头
fseek(fp, 0, SEEK_END);   // 移到末尾
fseek(fp, -10, SEEK_CUR); // 从当前位置往前移10字节

// rewind：回到开头（等价于 fseek(fp, 0, SEEK_SET)）
rewind(fp);
```

#### 2. feof 和 ferror

```c
if (feof(fp)) {
    printf("已经读到文件末尾了。\n");
}
if (ferror(fp)) {
    printf("读取过程中发生了错误！\n");
}
```

---

### 💻 上机敲代码

```c
/*
 * 文件名：file_position.c
 * 功能：文件定位、错误处理、缓冲区
 */

#include <stdio.h>

int main()
{
    FILE *fp;

    // ===== 一、fseek / ftell / rewind =====
    printf("===== 文件定位 =====\n");

    fp = fopen("position_demo.txt", "w+");  // 读写模式
    if (fp == NULL) { printf("文件创建失败！\n"); return 1; }

    // 写入一些内容
    fputs("ABCDEFGHIJKLMNOPQRSTUVWXYZ", fp);
    printf("写入完成。\n");

    // ftell 获取当前位置
    printf("当前文件位置：%ld（应该是文件末尾）\n", ftell(fp));

    // rewind 回到开头
    rewind(fp);
    printf("rewind后位置：%ld\n", ftell(fp));

    // 读取前5个字符
    printf("前5个字符：");
    for (int i = 0; i < 5; i++) {
        printf("%c", fgetc(fp));
    }
    printf("\n当前位置：%ld\n", ftell(fp));   // 应该是5

    // fseek 跳到第10个字符
    fseek(fp, 10, SEEK_SET);  // 从开头偏移10个字节
    printf("跳到位置10，后面的5个字符：");
    for (int i = 0; i < 5; i++) {
        printf("%c", fgetc(fp));
    }
    printf("\n");   // 应该输出 KLMNO

    fclose(fp);

    // ===== 二、计算文件大小 =====
    printf("\n===== 计算文件大小 =====\n");
    fp = fopen("position_demo.txt", "r");
    if (fp == NULL) return 1;

    fseek(fp, 0, SEEK_END);    // 移到文件末尾
    long fileSize = ftell(fp);  // 末尾的位置 = 文件大小
    printf("position_demo.txt 文件大小：%ld 字节\n", fileSize);
    fclose(fp);

    // ===== 三、feof 检测文件结束 =====
    printf("\n===== feof 演示 =====\n");
    fp = fopen("position_demo.txt", "r");
    if (fp == NULL) return 1;

    printf("逐个字符读取直到文件末尾：\n");
    int ch;
    int count = 0;
    while (1) {
        ch = fgetc(fp);
        if (feof(fp)) {   // 先读，再检查是否到了文件末尾
            printf("\n读到文件末尾了！（共%d个字符）\n", count);
            break;
        }
        if (ferror(fp)) {
            printf("\n读取错误！\n");
            break;
        }
        putchar(ch);
        count++;
    }
    fclose(fp);

    // ===== 四、fflush 强制写入 =====
    printf("\n===== fflush 演示 =====\n");
    fp = fopen("flush_demo.txt", "w");
    fprintf(fp, "这行数据先进入缓冲区...\n");
    fflush(fp);   // 强制把缓冲区的数据写入硬盘
    printf("fflush后，数据已写入硬盘（即使不fclose）。\n");
    // 通常在以下情况使用fflush：
    // 1. 写入重要数据后，防止程序崩溃导致数据丢失
    // 2. 读写切换前（从写切换到读，需要fflush或fseek）
    fclose(fp);

    return 0;
}
```

---

### 📋 今日核心知识点总结

1. `ftell(fp)` 获取当前文件位置；`fseek(fp, offset, origin)` 移动位置
2. `rewind(fp)` = `fseek(fp, 0, SEEK_SET)` 回到开头
3. SEEK_SET（0，从开头）、SEEK_CUR（1，从当前位置）、SEEK_END（2，从末尾）
4. `feof(fp)` 检测是否读到文件末尾（先读再检测）
5. `fflush(fp)` 强制将缓冲区数据写入硬盘

---

## Day 49-50：文件操作综合练习

### 🎯 今日学习目标
- 完成文件版学生管理系统的数据持久化
- 掌握实际项目中的文件操作模式

---

### 💻 上机敲代码：文件版简易通讯录

```c
/*
 * 文件名：file_contact_book.c
 * 功能：文件版通讯录——数据持久化到硬盘
 * 功能：添加、显示全部、搜索、数据保存到 contacts.txt
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_CONTACTS 100
#define NAME_LEN 30
#define PHONE_LEN 20
#define FILENAME "contacts.txt"

typedef struct {
    char name[NAME_LEN];
    char phone[PHONE_LEN];
    char email[50];
} Contact;

// 函数声明
int loadContacts(Contact contacts[]);       // 从文件加载通讯录
int saveContacts(Contact contacts[], int n); // 保存通讯录到文件
void addContact(Contact contacts[], int *n); // 添加联系人
void showAll(Contact contacts[], int n);     // 显示全部
void searchContact(Contact contacts[], int n); // 搜索联系人

int main()
{
    Contact contacts[MAX_CONTACTS];
    int count;   // 当前联系人数
    int choice;

    // 程序启动时从文件加载数据
    count = loadContacts(contacts);
    printf("📇 从文件加载了 %d 个联系人。\n", count);

    while (1) {
        printf("\n╔══════════════════════╗\n");
        printf("║    📇 简易通讯录     ║\n");
        printf("╠══════════════════════╣\n");
        printf("║ 1. 添加联系人        ║\n");
        printf("║ 2. 显示全部联系人     ║\n");
        printf("║ 3. 搜索联系人        ║\n");
        printf("║ 4. 保存到文件        ║\n");
        printf("║ 0. 保存并退出        ║\n");
        printf("╚══════════════════════╝\n");
        printf("请选择：");
        scanf("%d", &choice);
        getchar();

        switch (choice) {
            case 1: addContact(contacts, &count); break;
            case 2: showAll(contacts, count); break;
            case 3: searchContact(contacts, count); break;
            case 4:
                saveContacts(contacts, count);
                printf("✅ 数据已保存到 %s\n", FILENAME);
                break;
            case 0:
                saveContacts(contacts, count);
                printf("✅ 数据已保存。再见！\n");
                return 0;
            default:
                printf("❌ 无效选项！\n");
        }
    }
}

// 从文件加载通讯录（返回加载的联系人数）
int loadContacts(Contact contacts[]) {
    FILE *fp = fopen(FILENAME, "r");
    if (fp == NULL) {
        // 文件不存在 = 第一次使用，正常情况
        return 0;
    }

    int n = 0;
    // 文件格式：每行一个联系人，格式为 "姓名 电话 邮箱"
    while (n < MAX_CONTACTS &&
           fscanf(fp, "%s %s %s",
                  contacts[n].name,
                  contacts[n].phone,
                  contacts[n].email) == 3) {
        n++;
    }
    fclose(fp);
    return n;
}

// 保存通讯录到文件
int saveContacts(Contact contacts[], int n) {
    FILE *fp = fopen(FILENAME, "w");
    if (fp == NULL) {
        printf("❌ 无法创建文件 %s！\n", FILENAME);
        return 0;
    }

    for (int i = 0; i < n; i++) {
        fprintf(fp, "%s %s %s\n",
                contacts[i].name,
                contacts[i].phone,
                contacts[i].email);
    }
    fclose(fp);
    return 1;
}

// 添加联系人
void addContact(Contact contacts[], int *n) {
    if (*n >= MAX_CONTACTS) {
        printf("❌ 通讯录已满（最多%d人）！\n", MAX_CONTACTS);
        return;
    }

    Contact *c = &contacts[*n];
    printf("姓名：");
    fgets(c->name, NAME_LEN, stdin);
    c->name[strcspn(c->name, "\n")] = '\0';  // 去掉换行符

    printf("电话：");
    fgets(c->phone, PHONE_LEN, stdin);
    c->phone[strcspn(c->phone, "\n")] = '\0';

    printf("邮箱：");
    fgets(c->email, 50, stdin);
    c->email[strcspn(c->email, "\n")] = '\0';

    (*n)++;
    printf("✅ %s 已添加到通讯录！\n", c->name);
}

// 显示全部
void showAll(Contact contacts[], int n) {
    if (n == 0) {
        printf("通讯录为空。\n");
        return;
    }
    printf("\n===== 通讯录（共%d人）=====\n", n);
    printf("%-4s %-20s %-15s %s\n", "序号", "姓名", "电话", "邮箱");
    printf("───────────────────────────────────────────────\n");
    for (int i = 0; i < n; i++) {
        printf("%-4d %-20s %-15s %s\n",
               i + 1, contacts[i].name, contacts[i].phone, contacts[i].email);
    }
}

// 搜索联系人
void searchContact(Contact contacts[], int n) {
    char keyword[NAME_LEN];
    printf("请输入要搜索的姓名（支持部分匹配）：");
    fgets(keyword, NAME_LEN, stdin);
    keyword[strcspn(keyword, "\n")] = '\0';

    printf("\n搜索结果：\n");
    int found = 0;
    for (int i = 0; i < n; i++) {
        if (strstr(contacts[i].name, keyword) != NULL) {
            // strstr 判断 keyword 是否是 name 的子串
            printf("  %s | %s | %s\n",
                   contacts[i].name, contacts[i].phone, contacts[i].email);
            found++;
        }
    }
    if (found == 0) {
        printf("  未找到匹配的联系人。\n");
    }
}
```

---

## Day 51-52：预处理指令与多文件编译

### 🎯 今日学习目标
- 理解编译的四个阶段：预处理→编译→汇编→链接
- 掌握 `#include`、`#define`、`#ifdef` 等预处理指令
- 学会将程序拆分成多个 `.c` 和 `.h` 文件

---

### 📖 通俗化知识点讲解

#### 1. 编译四阶段

> **生活类比**：出版一本书。
> 1. **预处理**：编辑审查原稿，处理各种标记（#开头的指令）
> 2. **编译**：把中文翻译成英文（C→汇编）
> 3. **汇编**：把英文排成印刷版（汇编→机器码.o文件）
> 4. **链接**：把各章节装订成册（多个.o合并成.exe）

#### 2. 条件编译

```c
// 防止头文件重复包含（每个.h文件的标准写法）
#ifndef MY_HEADER_H      // 如果没定义过这个宏
#define MY_HEADER_H      // 就定义它

// ... 头文件内容 ...

#endif                   // 结束条件编译

// 调试用代码
#ifdef DEBUG
    printf("调试信息：x = %d\n", x);   // 只在DEBUG模式下编译
#endif
```

#### 3. 多文件项目结构

```
project/
├── main.c          # 主函数
├── student.h       # 学生结构体和函数声明
├── student.c       # 学生相关函数实现
├── utils.h         # 工具函数声明
└── utils.c         # 工具函数实现
```

---

### 💻 上机敲代码

#### 文件1：`student.h`（头文件——声明）

```c
/*
 * 文件名：student.h
 * 功能：学生模块的头文件（声明）
 */

#ifndef STUDENT_H              // 防止重复包含
#define STUDENT_H

// 结构体定义
typedef struct {
    int id;
    char name[30];
    float score;
} Student;

// 函数声明（只有声明，没有实现）
void printStudent(const Student *s);
float getAverage(const Student arr[], int n);
Student* findById(Student arr[], int n, int id);

#endif   // STUDENT_H
```

#### 文件2：`student.c`（源文件——实现）

```c
/*
 * 文件名：student.c
 * 功能：学生模块的实现
 */

#include <stdio.h>
#include "student.h"   // 包含自己的头文件

// 打印学生信息
void printStudent(const Student *s) {
    printf("学号：%d | 姓名：%s | 成绩：%.1f\n",
           s->id, s->name, s->score);
}

// 计算平均分
float getAverage(const Student arr[], int n) {
    float sum = 0;
    for (int i = 0; i < n; i++) {
        sum += arr[i].score;
    }
    return n > 0 ? sum / n : 0;
}

// 按学号查找
Student* findById(Student arr[], int n, int id) {
    for (int i = 0; i < n; i++) {
        if (arr[i].id == id) {
            return &arr[i];
        }
    }
    return NULL;
}
```

#### 文件3：`main.c`（主程序）

```c
/*
 * 文件名：main.c
 * 功能：多文件编译演示——主程序
 */

#include <stdio.h>
#include "student.h"   // 只需要包含头文件！

int main()
{
    // 使用 student.h 中声明的 Student 类型和函数
    Student class[] = {
        {1, "Alice", 90.5},
        {2, "Bob",   85.0},
        {3, "Carol", 92.5}
    };
    int n = sizeof(class) / sizeof(class[0]);

    printf("===== 全班学生 =====\n");
    for (int i = 0; i < n; i++) {
        printStudent(&class[i]);
    }

    printf("\n班级平均分：%.1f\n", getAverage(class, n));

    // 查找学生
    Student *found = findById(class, n, 2);
    if (found) {
        printf("\n找到学号2的学生：");
        printStudent(found);
    }

    return 0;
}
```

#### 编译多文件项目

```bash
# 方法1：一步到位
gcc main.c student.c -o program.exe

# 方法2：先分别编译，再链接（大项目的做法）
gcc -c main.c -o main.o        # 只编译，不链接
gcc -c student.c -o student.o  # 只编译，不链接
gcc main.o student.o -o program.exe  # 链接
```

---

### 📋 今日核心知识点总结

1. 每个 `.h` 文件必须有 `#ifndef/#define/#endif` 防护
2. `.h` 文件放**声明**（类型定义、函数声明），`.c` 文件放**实现**（函数体）
3. 条件编译 `#ifdef DEBUG` 用于调试代码开关
4. `#define` 宏可以带参数：`#define SQUARE(x) ((x)*(x))`（注意括号！）
5. 多文件编译：`gcc file1.c file2.c -o output.exe`

---

## Day 53-54：GDB调试入门 + 常用开发工具

### 🎯 今日学习目标
- 理解调试的重要性
- 掌握 printf 调试法和 VS Code 断点调试
- 了解 GDB 基本命令

---

### 📖 通俗化知识点讲解

#### 1. 调试的三种层次

| 层次 | 方法 | 适用场景 |
|------|------|----------|
| **初级** | printf 大法 | 快速定位简单Bug |
| **中级** | VS Code 断点调试 | 日常开发，观察变量变化 |
| **高级** | GDB 命令行调试 | Linux环境、无GUI场景 |

#### 2. printf 调试法（最简单实用）

```c
// 在可疑代码前后加 printf，观察变量值
printf("DEBUG: 进入函数前 x=%d, y=%d\n", x, y);
int result = someMysteriousFunction(x, y);
printf("DEBUG: 函数返回 result=%d\n", result);
```

#### 3. VS Code 断点调试

1. 在代码行号左侧点击，出现红色圆点（断点）
2. 按 `F5` 启动调试
3. 程序运行到断点处暂停
4. 可以查看变量值、单步执行、进入函数内部

---

### 💻 上机敲代码：调试练习

```c
/*
 * 文件名：debug_practice.c
 * 功能：调试练习——这段代码有Bug，请用调试器找出来！
 */

#include <stdio.h>

// 这个函数应该反转数组，但它有Bug！
void reverseArray(int arr[], int n) {
    // Bug提示：循环条件或交换逻辑有误
    for (int i = 0; i < n; i++) {
        int temp = arr[i];
        arr[i] = arr[n - 1 - i];
        arr[n - 1 - i] = temp;
    }
}

// 这个函数应该计算阶乘，但它对0的处理有Bug！
int factorial(int n) {
    if (n == 0) {
        return 0;   // Bug在这里！0! 应该等于1
    }
    int result = 1;
    for (int i = 1; i <= n; i++) {
        result *= i;
    }
    return result;
}

int main()
{
    // 测试1：反转数组
    int arr[] = {1, 2, 3, 4, 5};
    int n = sizeof(arr) / sizeof(arr[0]);

    printf("反转前：");
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("\n");

    reverseArray(arr, n);

    printf("反转后：");
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("\n");
    // 预期：5 4 3 2 1
    // 实际：?（用调试器看看为什么）

    // 测试2：阶乘
    printf("\n0! = %d（应该是1）\n", factorial(0));
    printf("5! = %d（应该是120）\n", factorial(5));

    printf("\n💡 提示：\n");
    printf("1. reverseArray的Bug：循环到n而不是n/2，导致反转两次回到原样\n");
    printf("   修复：for (int i = 0; i < n/2; i++)\n");
    printf("2. factorial的Bug：0!返回0，应该是1\n");
    printf("   修复：if (n == 0) return 1;\n");

    return 0;
}
```

---

## Day 55：综合复习——C语言知识体系全景图

### 🎯 今日学习目标
- 全面梳理C语言知识体系
- 查漏补缺，标记薄弱环节
- 准备结业项目

---

### 📋 C语言完整知识体系清单

```
C语言知识体系（54天学习内容回顾）
│
├── 基础语法（Day 1-7）
│   ├── ✅ 程序结构（#include, main(), return 0）
│   ├── ✅ 数据类型（int, float, double, char）
│   ├── ✅ 变量与常量（声明、赋值、const, #define）
│   ├── ✅ 输入输出（printf, scanf, 占位符）
│   ├── ✅ 运算符（算术、关系、逻辑、赋值、自增自减）
│   └── ✅ 类型转换（隐式转换、强制转换、整数除法陷阱）
│
├── 逻辑控制（Day 8-15）
│   ├── ✅ if / if-else / if-else if-else
│   ├── ✅ switch-case-break-default
│   ├── ✅ for 循环（初始化/条件/更新）
│   ├── ✅ while 循环（先判断）
│   ├── ✅ do-while 循环（先执行）
│   ├── ✅ break / continue
│   ├── ✅ 嵌套循环
│   └── ✅ 随机数（rand, srand）
│
├── 数组（Day 16-22）
│   ├── ✅ 一维数组（声明、初始化、遍历）
│   ├── ✅ 二维数组（行×列、双层循环遍历）
│   ├── ✅ 冒泡排序
│   ├── ✅ 顺序查找
│   ├── ✅ 字符数组与字符串（\0结尾）
│   └── ✅ 字符串函数（strlen, strcpy, strcmp, strcat）
│
├── 函数（Day 23-28）
│   ├── ✅ 函数定义/声明/调用
│   ├── ✅ 形式参数 vs 实际参数
│   ├── ✅ 值传递（C语言的唯一传递方式）
│   ├── ✅ 局部变量 vs 全局变量
│   ├── ✅ static 变量
│   └── ✅ 递归（基准条件+递归条件）
│
├── 指针（Day 29-37）★ 最核心最难点
│   ├── ✅ 指针概念（存地址的变量）
│   ├── ✅ & 取地址 / * 解引用
│   ├── ✅ 指针与数组（arr[i] = *(arr+i)）
│   ├── ✅ 指针运算（++、--、+N）
│   ├── ✅ 传址调用（真正修改外部变量）
│   ├── ✅ const 指针
│   ├── ✅ 二级指针 int **pp
│   ├── ✅ 指针数组 vs 数组指针
│   ├── ✅ 函数指针（回调函数）
│   ├── ✅ 动态内存（malloc, calloc, realloc, free）
│   ├── ✅ 动态二维数组
│   └── ✅ 内存泄漏与防范
│
├── 字符串进阶（Day 34-35）
│   ├── ✅ char* vs char[]
│   ├── ✅ 自实现 strlen/strcpy/strcmp
│   └── ✅ 命令行参数 argc/argv
│
├── 结构体与联合体（Day 38-40）
│   ├── ✅ 结构体定义/声明/访问
│   ├── ✅ . 运算符 vs -> 运算符
│   ├── ✅ typedef 类型别名
│   ├── ✅ 结构体嵌套
│   ├── ✅ 结构体数组
│   ├── ✅ 结构体指针
│   ├── ✅ 联合体 union（共享内存）
│   └── ✅ 枚举 enum（命名常量）
│
├── 链表（Day 42-43）
│   ├── ✅ 自引用结构体 Node
│   ├── ✅ 链表创建与遍历
│   ├── ✅ 头插法 / 尾插法
│   ├── ✅ 删除节点
│   └── ✅ 释放链表
│
├── 文件操作（Day 46-50）
│   ├── ✅ FILE* 文件指针
│   ├── ✅ fopen / fclose
│   ├── ✅ 文件打开模式（r/w/a/r+/w+/a+）
│   ├── ✅ fprintf / fscanf（格式化读写）
│   ├── ✅ fgets / fputs（字符串读写）
│   ├── ✅ fwrite / fread（二进制读写）
│   ├── ✅ fseek / ftell / rewind（文件定位）
│   ├── ✅ feof / ferror（状态检测）
│   └── ✅ fflush（强制刷新缓冲区）
│
├── 预处理（Day 51-52）
│   ├── ✅ #include（包含头文件）
│   ├── ✅ #define（宏定义）
│   ├── ✅ #ifdef / #ifndef / #endif（条件编译）
│   └── ✅ 多文件编译（.h + .c）
│
└── 调试（Day 53-54）
    ├── ✅ printf 调试法
    ├── ✅ VS Code 断点调试
    └── ✅ GDB 基础命令
```

**逐一检查每个 ☐，确保全部变成 ☑！**

---

## Day 56-58：综合项目——完整通讯录系统

### 🎯 项目目标
综合运用C语言全部核心知识，完成一个可写入简历的作品级程序。

### 📋 项目需求

```
通讯录管理系统 v3.0（终极版）

功能需求：
1. 添加联系人（姓名、电话、邮箱、地址、分组）
2. 删除联系人（按姓名或序号）
3. 修改联系人信息
4. 查找联系人（按姓名模糊搜索、按分组筛选）
5. 显示全部联系人（按姓名排序）
6. 分组管理（添加/删除分组）
7. 数据持久化（程序启动时自动加载，退出时自动保存）
8. 数据导出（导出为CSV格式，可用Excel打开）

技术要求：
- 使用链表存储数据（支持无限数量联系人）
- 使用结构体组织数据
- 使用动态内存分配
- 使用文件操作持久化数据
- 模块化设计（.h + .c 多文件）
- 规范的代码注释和命名
```

> 📁 **完整代码较长，详见 module-6 中的项目清单。此处给出核心框架和关键代码片段。**

### 💻 核心代码框架

```c
/*
 * 通讯录系统核心框架（完整实现建议作为独立项目完成）
 *
 * 文件结构：
 * contact.h      - 数据结构定义 + 函数声明
 * contact.c      - 核心功能实现
 * file_io.c      - 文件读写模块
 * ui.c           - 用户界面模块
 * main.c         - 主程序入口
 */

// ===== contact.h =====
#ifndef CONTACT_H
#define CONTACT_H

#define NAME_LEN 30
#define PHONE_LEN 20
#define EMAIL_LEN 50
#define ADDR_LEN 80
#define GROUP_LEN 20
#define DATA_FILE "contacts_v3.dat"

typedef struct Contact {
    char name[NAME_LEN];
    char phone[PHONE_LEN];
    char email[EMAIL_LEN];
    char address[ADDR_LEN];
    char group[GROUP_LEN];
    struct Contact *next;    // 链表指针
} Contact;

// 核心操作
Contact* contact_create(const char *name, const char *phone,
                        const char *email, const char *addr,
                        const char *group);
void contact_free(Contact *c);
void list_add(Contact **head, Contact *newContact);
int  list_delete(Contact **head, const char *name);
Contact* list_find(Contact *head, const char *name);
void list_print_all(Contact *head);
void list_sort(Contact **head);
int  list_count(Contact *head);
void list_free_all(Contact **head);

// 文件操作
int  save_to_file(Contact *head, const char *filename);
int  load_from_file(Contact **head, const char *filename);
int  export_csv(Contact *head, const char *filename);

#endif
```

---

## Day 59：总复习（一）—— 理论笔试模拟

### 📝 理论自测题

**一、选择题（每题4分，共40分）**

1. 以下哪个是正确的 main 函数定义？
   A. `void main() {}`
   B. `int main() {}`
   C. `Main() {}`
   D. `int main(void) {}`

2. `printf("%d", 5/2);` 的输出是？
   A. 2.5
   B. 2
   C. 2.0
   D. 编译错误

3. 设 `int a=5; int *p=&a;` 则 `*p` 的值是？
   A. a的地址
   B. 5
   C. p的地址
   D. 不确定

4. `int arr[5] = {1,2,3,4,5};` 则 `*(arr+2)` 的值是？
   A. 1
   B. 2
   C. 3
   D. 4

5. `malloc` 分配的内存位于？
   A. 栈
   B. 堆
   C. 全局区
   D. 代码区

6. 链表相对于数组的主要优势是？
   A. 随机访问快
   B. 插入删除效率高
   C. 占用内存少
   D. 实现简单

7. `fopen("test.txt", "w")` 如果文件已存在会？
   A. 报错
   B. 追加内容
   C. 清空原内容
   D. 打开失败

8. `strcmp("abc", "abd")` 的返回值是？
   A. 0
   B. 正数
   C. 负数
   D. 不确定

9. 以下哪个正确声明了函数指针？
   A. `int *func(int, int);`
   B. `int (*func)(int, int);`
   C. `int *func(int)(int);`
   D. `(int *)func(int, int);`

10. 关于 `const int *p` 说法正确的是？
    A. p的值不可修改
    B. p指向的数据不可修改
    C. p和它指向的数据都不可修改
    D. p是一个常量

**二、简答题（每题10分，共30分）**

1. 画出以下代码的内存布局图：
   ```c
   int a = 10;
   int *p = &a;
   int **pp = &p;
   ```

2. 解释值传递和传址调用的区别，并给出代码示例。

3. 简述 `malloc`/`calloc`/`realloc`/`free` 四个函数的用途和注意事项。

**三、代码分析题（每题15分，共30分）**

1. 找出以下代码中的所有错误并修正：
   ```c
   char *str = "Hello";
   str[0] = 'h';
   printf("%s", str);
   ```

2. 分析以下代码的执行结果，并画出链表变化过程：
   ```c
   Node *head = NULL;
   insertHead(&head, 10);
   insertHead(&head, 20);
   deleteNode(&head, 10);
   ```

> 📝 参考答案见 module-4

---

## Day 60：总复习（二）—— 上机编程考核 + 结业总结

### 🎯 今日目标
- 完成结业上机考核
- 回顾60天学习历程
- 规划大一学习路线

---

### 💻 结业上机考核（限时2小时）

**题目：简易图书管理系统**

```
功能要求（按优先级排序）：
[必做] 1. 添加图书（书名、作者、ISBN、价格）
[必做] 2. 显示全部图书
[必做] 3. 按书名搜索
[必做] 4. 删除图书
[选做] 5. 数据保存到文件 books.txt
[选做] 6. 程序启动时从文件加载数据
[选做] 7. 按价格排序显示
[选做] 8. 修改图书信息

评分标准：
- 程序能编译运行：30分
- 必做功能全部实现：30分
- 代码规范（命名、注释、缩进）：15分
- 有错误处理：10分
- 选做功能：每个5分

及格线：60分
优秀线：85分
```

---

### 🎓 60天结业总结

```
╔══════════════════════════════════════════════════════════╗
║            🎉 恭喜你完成了60天C语言筑基之旅！            ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  📊 你学会了：                                           ║
║  ├── 12种基本数据类型和运算符                            ║
║  ├── 4种程序控制结构（if/switch/for/while）              ║
║  ├── 数组（一维/二维/字符串）                            ║
║  ├── 函数（定义/调用/递归/模块化）                       ║
║  ├── 指针（★最核心！地址/解引用/指针运算/动态内存）     ║
║  ├── 结构体（自定义类型/链表）                           ║
║  ├── 文件操作（文本/二进制/持久化）                      ║
│  └── 调试题（printf法/VS Code断点/GDB）                ║
║                                                          ║
║  🏆 你完成的程序：                                       ║
║  ├── 四则运算计算器                                      ║
║  ├── 猜数字游戏                                          ║
║  ├── 学生成绩管理系统（数组版 + 链表版）                 ║
║  ├── 通讯录系统（文件持久化版）                          ║
│  └── 图书管理系统（结业项目）                          ║
║                                                          ║
║  🚀 下一步：                                              ║
║  ├── 打开 module-6-长期拓展.md 查看大学规划              ║
║  ├── 完成 module-4 中的结业测评                          ║
║  └── 在 LeetCode / 洛谷 上刷算法题                      ║
║                                                          ║
║  💪 记住：编程是一门手艺，手艺是练出来的！                ║
║     大学四年，你比别人领先了整整60天！                    ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
```

---

> 📌 **你已完成 module-2 全部60天课程！** 接下来完成 module-3（配套习题）巩固技能，用 module-4（能力评估）检测水平，用 module-5（打卡模板）坚持每天打卡。
