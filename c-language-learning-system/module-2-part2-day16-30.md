# 模块2：分阶段逐天讲课讲义（Day 16 - Day 30）

> 📌 本阶段进入数组、函数、指针入门——C语言从"能写"到"会写"的跃升期。

---

## Day 16：一维数组（上）—— 批量处理数据的开始

### 🎯 今日学习目标
学完后你能：
- 理解为什么需要数组
- 掌握一维数组的声明、初始化、访问
- 用循环遍历数组元素

---

### 📖 通俗化知识点讲解

#### 1. 数组是什么？

> **生活类比**：宿舍楼的信箱墙。
> - 一整面墙有100个信箱，统一编号 0号、1号、2号...99号
> - 每个信箱的大小一样（都只能放信件）
> - 你可以快速找到"第35号信箱"里有什么
>
> 数组就是内存中**连续排列**的一串**同类型**变量，通过编号（下标）访问。

```
int scores[5];   // 声明一个能存5个整数的数组

内存中的样子：
┌──────┬──────┬──────┬──────┬──────┐
│  ?   │  ?   │  ?   │  ?   │  ?   │   ← 未初始化，值是随机的
└──────┴──────┴──────┴──────┴──────┘
 scores[0] [1]   [2]   [3]   [4]        ← 下标从0开始！不是从1！
```

#### 2. 为什么下标从0开始？

> 数组名 `scores` 其实是第一个元素的内存地址。
> `scores[0]` = 地址+0个偏移 = 第一个元素
> `scores[1]` = 地址+1个偏移 = 第二个元素
>
> 所以下标本质是"偏移量"，从0开始就非常自然了。

#### 3. 数组的三种初始化方式

```c
// 方式1：声明后逐个赋值
int scores[5];
scores[0] = 88;
scores[1] = 92;
scores[2] = 76;
scores[3] = 85;
scores[4] = 90;

// 方式2：声明时整体初始化（最常用）
int scores[5] = {88, 92, 76, 85, 90};

// 方式3：不指定大小，让编译器自动数
int scores[] = {88, 92, 76, 85, 90};  // 编译器知道大小是5
```

---

### 💻 上机敲代码

```c
/*
 * 文件名：array_basic.c
 * 功能：一维数组基本操作
 */

#include <stdio.h>

int main()
{
    // ===== 一、数组的声明与初始化 =====
    int scores[5] = {88, 92, 76, 85, 90};  // 5个学生的成绩

    // 逐个访问（不用循环——只有5个还好，500个就疯了）
    printf("===== 逐个访问 =====\n");
    printf("第1个学生成绩：%d\n", scores[0]);  // 下标0是第一个！
    printf("第2个学生成绩：%d\n", scores[1]);
    printf("第3个学生成绩：%d\n", scores[2]);
    printf("第4个学生成绩：%d\n", scores[3]);
    printf("第5个学生成绩：%d\n", scores[4]);

    // ===== 二、用循环遍历数组（这才是正确方式） =====
    printf("\n===== for循环遍历 =====\n");
    for (int i = 0; i < 5; i++) {     // i从0到4
        printf("scores[%d] = %d\n", i, scores[i]);
    }

    // ===== 三、从键盘输入数组元素 =====
    int nums[5];
    printf("\n===== 输入数组元素 =====\n");
    for (int i = 0; i < 5; i++) {
        printf("请输入第%d个数：", i + 1);  // i+1让用户看到从1开始的编号
        scanf("%d", &nums[i]);              // 注意要加 &
    }
    printf("你输入的数组：");
    for (int i = 0; i < 5; i++) {
        printf("%d ", nums[i]);
    }
    printf("\n");

    // ===== 四、数组常用操作：求和、平均值、最大值 =====
    int data[] = {45, 78, 23, 91, 56, 34, 67};
    int size = sizeof(data) / sizeof(data[0]);  // 计算数组元素个数
    //        数组总字节数 ÷ 单个元素字节数 = 元素个数

    int sum = 0;
    int max = data[0];  // 先假设第一个是最大值
    int min = data[0];  // 先假设第一个是最小值

    for (int i = 0; i < size; i++) {
        sum += data[i];                    // 累加
        if (data[i] > max) max = data[i];  // 更新最大值
        if (data[i] < min) min = data[i];  // 更新最小值
    }

    float avg = (float)sum / size;  // 注意类型转换

    printf("\n===== 数组统计 =====\n");
    printf("数组元素：");
    for (int i = 0; i < size; i++) printf("%d ", data[i]);
    printf("\n元素个数：%d\n", size);
    printf("总和：%d\n", sum);
    printf("平均值：%.2f\n", avg);
    printf("最大值：%d\n", max);
    printf("最小值：%d\n", min);

    return 0;
}
```

---

### 📋 今日核心知识点总结

1. 数组是一串**同类型**数据的**连续**存储，通过**下标**访问
2. 下标**从0开始**，最后一个元素的下标是 `数组长度-1`
3. `int arr[5]` 有5个元素：`arr[0]` 到 `arr[4]`（没有 `arr[5]`！）
4. 遍历数组用 for 循环，`i` 从0到`size-1`
5. `sizeof(arr) / sizeof(arr[0])` 可以算出数组元素个数

> ⚠️ **数组越界**是最常见的Bug之一！访问 `arr[5]`（第6个元素）不会报错但结果不可预测！

---

## Day 17：一维数组（下）—— 排序与查找

### 🎯 今日学习目标
学完后你能：
- 理解冒泡排序的原理
- 掌握线性查找算法
- 用数组实现成绩排名功能

---

### 📖 通俗化知识点讲解

#### 1. 冒泡排序

> **生活类比**：体育课按身高排队。
> - 从队伍最左边开始，比较相邻两个人的身高
> - 如果左边的人比右边高 → 交换位置
> - 一轮下来，最高的人"冒泡"到了最右边
> - 重复这个过程，直到所有人有序

```
初始： [5, 3, 8, 1, 2]

第一轮（最大的8冒到最右边）：
  比较5和3 → 交换 → [3, 5, 8, 1, 2]
  比较5和8 → 不换 → [3, 5, 8, 1, 2]
  比较8和1 → 交换 → [3, 5, 1, 8, 2]
  比较8和2 → 交换 → [3, 5, 1, 2, 8]  ← 8已就位

第二轮（第二大的5冒到倒数第二）：
  ... → [3, 1, 2, 5, 8]  ← 5就位

第三轮：... → [1, 2, 3, 5, 8]  ← 全部有序！
```

---

### 💻 上机敲代码

```c
/*
 * 文件名：array_sort_search.c
 * 功能：数组排序（冒泡）与查找
 */

#include <stdio.h>

int main()
{
    // ===== 一、冒泡排序（从小到大） =====
    int scores[] = {85, 92, 78, 96, 63, 88, 74};
    int n = sizeof(scores) / sizeof(scores[0]);

    printf("排序前：");
    for (int i = 0; i < n; i++) printf("%d ", scores[i]);
    printf("\n");

    // 冒泡排序核心代码
    for (int i = 0; i < n - 1; i++) {         // 外层：进行n-1轮
        for (int j = 0; j < n - 1 - i; j++) { // 内层：每轮比较的区间逐渐缩小
            if (scores[j] > scores[j + 1]) {   // 前面的比后面大？交换！
                // 交换两个元素（经典的三步交换法）
                int temp = scores[j];           // 第一步：暂存前面的值
                scores[j] = scores[j + 1];      // 第二步：后面的值覆盖前面
                scores[j + 1] = temp;           // 第三步：暂存的值放后面
            }
        }
        // 打印每轮结果，观察冒泡过程
        printf("第%d轮后：", i + 1);
        for (int k = 0; k < n; k++) printf("%d ", scores[k]);
        printf("\n");
    }

    printf("\n排序完成（从小到大）：");
    for (int i = 0; i < n; i++) printf("%d ", scores[i]);
    printf("\n");

    // ===== 二、顺序查找（线性查找） =====
    printf("\n===== 顺序查找 =====\n");
    int target;  // 要找的值
    printf("请输入要查找的分数：");
    scanf("%d", &target);

    int found_index = -1;   // -1 表示"没找到"
    for (int i = 0; i < n; i++) {
        if (scores[i] == target) {
            found_index = i;   // 记录找到的位置
            break;             // 找到了就退出
        }
    }

    if (found_index != -1) {
        printf("找到了！%d 在数组的第 %d 个位置（下标%d）\n",
               target, found_index + 1, found_index);
    } else {
        printf("没找到 %d\n", target);
    }

    return 0;
}
```

---

### 📋 今日核心知识点总结

1. 冒泡排序：相邻比较+交换，每轮把最大的"冒"到最后
2. 交换两个变量的三步骤：`temp=a; a=b; b=temp;`（必须用临时变量！）
3. 顺序查找：从数组开头逐个比对，找到或遍历完为止
4. `found_index = -1` 是一个常用的"没找到"信号

---

## Day 18：二维数组—— 表格数据的处理

### 🎯 今日学习目标
学完后你能：
- 理解二维数组的本质（数组的数组）
- 掌握二维数组的声明、初始化、遍历
- 用二维数组处理学生多科目成绩

---

### 📖 通俗化知识点讲解

> **生活类比**：Excel表格。
> - 行（row）：第1行、第2行...
> - 列（col）：A列、B列...
> - 每个格子 = `表格[行号][列号]`

```c
int scores[3][4];  // 3行4列的表格
// 3个学生，每人4科成绩

// 内存中的样子（逻辑上）：
//         列0  列1  列2  列3
// 行0:  [ 85,  92,  78,  88 ]  ← 第1个学生的4科成绩
// 行1:  [ 76,  82,  90,  85 ]  ← 第2个学生的4科成绩
// 行2:  [ 91,  88,  84,  92 ]  ← 第3个学生的4科成绩
```

```c
// 初始化方式
int matrix[3][4] = {
    {85, 92, 78, 88},   // 第0行
    {76, 82, 90, 85},   // 第1行
    {91, 88, 84, 92}    // 第2行
};
// 注意：每一行的大括号之间用逗号隔开
```

---

### 💻 上机敲代码

```c
/*
 * 文件名：2d_array.c
 * 功能：二维数组——学生多科目成绩管理
 */

#include <stdio.h>

int main()
{
    // 3个学生，4门课的成绩
    char *subjects[] = {"数学", "英语", "C语言", "体育"};
    //  ↑ char* 是指向字符串的指针，Day 29会详细讲
    int scores[3][4] = {
        {85, 92, 78, 88},   // 张三的成绩
        {76, 82, 90, 85},   // 李四的成绩
        {91, 88, 84, 92}    // 王五的成绩
    };
    char *names[] = {"张三", "李四", "王五"};

    // ===== 一、打印成绩表 =====
    printf("===== 学生成绩表 =====\n");
    printf("姓名\t数学\t英语\tC语言\t体育\t总分\t平均分\n");
    //      \t 是制表符，让列对齐

    for (int i = 0; i < 3; i++) {       // 外层循环：遍历每个学生（行）
        printf("%s\t", names[i]);
        int total = 0;                   // 当前学生的总分

        for (int j = 0; j < 4; j++) {   // 内层循环：遍历每科成绩（列）
            printf("%d\t", scores[i][j]);
            total += scores[i][j];       // 累加成绩
        }
        float avg = total / 4.0;         // 计算平均分
        printf("%d\t%.1f\n", total, avg);
    }

    // ===== 二、每门课的平均分 =====
    printf("\n===== 各科目统计 =====\n");
    for (int j = 0; j < 4; j++) {       // 外层遍历列（科目）
        int sum = 0;
        for (int i = 0; i < 3; i++) {   // 内层遍历行（学生）
            sum += scores[i][j];
        }
        printf("%s平均分：%.1f\n", subjects[j], sum / 3.0);
    }

    // ===== 三、找出每个学生的最高分科目 =====
    printf("\n===== 每人最高分科目 =====\n");
    for (int i = 0; i < 3; i++) {
        int max_score = scores[i][0];
        int max_subject = 0;   // 记录最高分是第几科

        for (int j = 1; j < 4; j++) {
            if (scores[i][j] > max_score) {
                max_score = scores[i][j];
                max_subject = j;
            }
        }
        printf("%s 最高分：%s %d分\n",
               names[i], subjects[max_subject], max_score);
    }

    return 0;
}
```

---

### 📋 今日核心知识点总结

1. 二维数组：`类型 数组名[行数][列数]`
2. 遍历二维数组需要**双层嵌套循环**（外层行、内层列）
3. 行下标和列下标都从0开始
4. 初始化时可以每行用 `{}` 包裹，增强可读性
5. 两种遍历方向：按行遍历（常用）和按列遍历（统计用）

---

## Day 19：字符数组与字符串（上）

### 🎯 今日学习目标
学完后你能：
- 理解C语言中字符串的本质——字符数组+`\0`
- 掌握字符数组的声明和初始化
- 使用 `%s` 输入输出字符串

---

### 📖 通俗化知识点讲解

#### 1. C语言中字符串的本质

> **关键理解**：C语言**没有**专门的字符串类型！字符串是用**字符数组**来存储的，以 `\0`（空字符）作为结束标记。

```c
char name[6] = {'H', 'e', 'l', 'l', 'o', '\0'};
// 等价于：
char name[6] = "Hello";   // 编译器会自动在末尾加 \0

// 内存中的样子：
// ┌───┬───┬───┬───┬───┬───┐
// │ H │ e │ l │ l │ o │\0 │
// └───┴───┴───┴───┴───┴───┘
//   0   1   2   3   4   5
//                      ↑ \0 是字符串的"终点线"
```

> **生活类比**：`\0` 就像一句话末尾的句号。没有句号，你就不知道句子在哪结束。
> 如果字符数组没有 `\0`，`printf` 就会一直往后读内存，直到碰巧遇到一个 `\0`，输出一堆乱码。

#### 2. 字符串 vs 字符数组

```c
char str1[] = "Hello";        // 字符串，自动加\0，大小=6
char str2[] = {'H','e','l','l','o'};  // 字符数组，没有\0，大小=5
char str3[20] = "Hello";      // 预留20个字符空间，目前只用6个

// str1 可以用 %s 输出
printf("%s\n", str1);   // Hello ✅

// str2 没有\0，用%s输出会出问题！
printf("%s\n", str2);   // Hello???乱码 ❌
```

---

### 💻 上机敲代码

```c
/*
 * 文件名：string_basic.c
 * 功能：字符数组与字符串基本操作
 */

#include <stdio.h>

int main()
{
    // ===== 一、字符串的三种初始化方式 =====
    char name1[20] = "Zhang San";      // 方式1：直接写字符串
    char name2[] = "Li Si";            // 方式2：不指定大小
    char name3[20] = {'W','a','n','g','\0'}; // 方式3：逐个字符

    printf("名字1：%s\n", name1);
    printf("名字2：%s\n", name2);
    printf("名字3：%s\n", name3);

    // ===== 二、用scanf输入字符串 =====
    char nickname[20];
    printf("\n请输入你的昵称：");
    scanf("%s", nickname);   // 注意：字符串输入不需要 & ！
    printf("你好，%s！\n", nickname);

    // ===== 三、单个字符 vs 字符串 =====
    char ch = 'A';            // 单个字符：单引号
    char str[] = "A";         // 字符串：双引号（实际是 'A' + '\0'）

    printf("\n字符 ch = %c，占用 %d 字节\n", ch, (int)sizeof(ch));
    printf("字符串 str = %s，占用 %d 字节\n", str, (int)sizeof(str));
    // str 占用2字节：'A' + '\0'

    // ===== 四、遍历字符串中的每个字符 =====
    char word[] = "Hello";
    printf("\n逐个字符输出 \"Hello\"：\n");
    for (int i = 0; word[i] != '\0'; i++) {  // 遇到 \0 就停
        printf("word[%d] = '%c' (ASCII: %d)\n", i, word[i], word[i]);
    }

    // ===== 五、手算字符串长度 =====
    char text[] = "C Language";
    int length = 0;
    while (text[length] != '\0') {   // 数到 \0 为止
        length++;
    }
    printf("\n\"%s\" 的长度是：%d\n", text, length);
    // 输出：10（空格也算一个字符！）

    return 0;
}
```

---

### 📋 今日核心知识点总结

1. C语言没有String类型，字符串是**以`\0`结尾的字符数组**
2. `"Hello"` 实际占用6字节（5个字符+1个`\0`）
3. 用 `%s` 输入输出字符串，**scanf 不需要 `&`**（数组名本身就是地址）
4. `scanf("%s")` 遇到空格就会停止读入，这是个限制（Day 20会解决）
5. 判断字符串结束：检查当前字符 `!= '\0'`

---

## Day 20：字符串处理（下）—— 常用字符串函数

### 🎯 今日学习目标
学完后你能：
- 使用 `strlen`、`strcpy`、`strcmp`、`strcat` 等常用函数
- 理解 `gets`/`fgets` 读取带空格的字符串
- 掌握字符判断函数（`isalpha`、`isdigit`等）

---

### 📖 通俗化知识点讲解

#### 1. 四个最常用的字符串函数

| 函数 | 头文件 | 作用 | 例子 |
|------|--------|------|------|
| `strlen(s)` | `<string.h>` | 求字符串长度（不计\0） | `strlen("Hi")` → 2 |
| `strcpy(dst, src)` | `<string.h>` | 拷贝字符串 | `strcpy(a, b)` → a等于b |
| `strcmp(a, b)` | `<string.h>` | 比较两个字符串 | 相等返回0，a>b返回正数 |
| `strcat(dst, src)` | `<string.h>` | 拼接字符串 | `strcat(a, b)` → a = a+b |

#### 2. 读取带空格的字符串

```c
// scanf("%s") 遇到空格就停，无法读入"Hello World"
// 解决方法：
fgets(buffer, size, stdin);   // 安全，推荐！
// 注意：fgets 会保留末尾的换行符 \n
```

#### 3. 字符判断函数（`<ctype.h>`）

```c
isalpha(ch)   // 是字母吗？
isdigit(ch)   // 是数字吗？
isupper(ch)   // 是大写字母吗？
islower(ch)   // 是小写字母吗？
isspace(ch)   // 是空白字符吗？
toupper(ch)   // 转大写
tolower(ch)   // 转小写
```

---

### 💻 上机敲代码

```c
/*
 * 文件名：string_functions.c
 * 功能：字符串函数综合应用
 */

#include <stdio.h>
#include <string.h>   // strlen, strcpy, strcmp, strcat
#include <ctype.h>    // isalpha, isdigit, toupper, tolower

int main()
{
    // ===== 一、strlen 求长度 =====
    char msg[] = "Hello World!";
    printf("字符串：\"%s\"\n", msg);
    printf("长度（不含\\0）：%d\n", (int)strlen(msg));
    printf("占用字节（含\\0）：%d\n", (int)sizeof(msg));
    // strlen=12, sizeof=13（多了一个\0）

    // ===== 二、strcpy 拷贝 =====
    char source[] = "Original";
    char dest[20];               // 目标数组要足够大！
    strcpy(dest, source);        // 把source拷贝到dest
    printf("\n拷贝后 dest = %s\n", dest);

    // ===== 三、strcmp 比较 =====
    printf("\n===== 字符串比较 =====\n");
    char *s1 = "abc";
    char *s2 = "abc";
    char *s3 = "abd";
    char *s4 = "ABC";

    printf("strcmp(\"abc\", \"abc\") = %d\n", strcmp(s1, s2));  // 0（相等）
    printf("strcmp(\"abc\", \"abd\") = %d\n", strcmp(s1, s3));  // 负数（abc<abd）
    printf("strcmp(\"abc\", \"ABC\") = %d\n", strcmp(s1, s4));  // 正数（小写>大写）

    // ===== 四、strcat 拼接 =====
    char greeting[50] = "Hello";   // 目标数组要足够大！
    strcat(greeting, " ");         // 拼接空格
    strcat(greeting, "World");     // 拼接World
    strcat(greeting, "!");         // 拼接感叹号
    printf("\n拼接结果：%s\n", greeting);   // Hello World!

    // ===== 五、fgets 读取带空格的字符串 =====
    char fullName[50];
    printf("\n请输入你的全名（可以带空格）：");
    getchar();  // 吃掉之前残留的换行符
    fgets(fullName, 50, stdin);    // 从键盘读取最多49个字符

    // fgets会保留换行符，去掉它
    int len = strlen(fullName);
    if (fullName[len - 1] == '\n') {
        fullName[len - 1] = '\0';   // 把换行符替换成\0
    }
    printf("你的全名是：%s\n", fullName);

    // ===== 六、字符判断与转换 =====
    printf("\n===== 字符判断 =====\n");
    char test_chars[] = {'A', '5', ' ', 'b', '!'};
    for (int i = 0; i < 5; i++) {
        char c = test_chars[i];
        printf("'%c': ", c);
        if (isalpha(c)) printf("字母 ");
        if (isdigit(c)) printf("数字 ");
        if (isspace(c)) printf("空白 ");
        if (isupper(c)) printf("大写→%c ", tolower(c));
        if (islower(c)) printf("小写→%c ", toupper(c));
        printf("\n");
    }

    return 0;
}
```

---

### 📋 今日核心知识点总结

1. `#include <string.h>` 获取字符串函数，`#include <ctype.h>` 获取字符判断函数
2. `strcpy` 要确保目标数组**足够大**，否则会溢出
3. `strcmp` 返回0表示相等，不是返回1！
4. `fgets` 读取字符串**保留换行符**，通常需要手动去掉
5. 字符串操作前，先确认数组容量是否足够

---

## Day 21：数组与字符串阶段综合练习

### 🎯 今日学习目标
- 综合运用数组和字符串完成两个实用程序
- 为函数学习做铺垫

---

### 💻 上机敲代码

#### 项目1：简易学生成绩管理系统（数组版）

```c
/*
 * 文件名：student_score_system.c
 * 功能：学生成绩录入、查询、统计（数组版）
 * 覆盖：数组、字符串、循环、分支
 */

#include <stdio.h>
#include <string.h>

#define MAX_STUDENTS 50   // 最多管理50个学生
#define NAME_LEN 30       // 名字最长30字符

int main()
{
    char names[MAX_STUDENTS][NAME_LEN];  // 学生姓名（字符串数组）
    int scores[MAX_STUDENTS];           // 学生成绩
    int count = 0;                       // 当前学生人数
    int choice;

    while (1) {
        printf("\n╔══════════════════════════╗\n");
        printf("║   学生成绩管理系统 v1.0  ║\n");
        printf("╠══════════════════════════╣\n");
        printf("║ 1. 录入学生成绩          ║\n");
        printf("║ 2. 显示所有成绩          ║\n");
        printf("║ 3. 查询某个学生          ║\n");
        printf("║ 4. 成绩统计              ║\n");
        printf("║ 0. 退出                  ║\n");
        printf("╚══════════════════════════╝\n");
        printf("请选择：");
        scanf("%d", &choice);
        getchar();  // 吃掉换行符

        switch (choice) {
            case 1: {  // 录入
                if (count >= MAX_STUDENTS) {
                    printf("❌ 学生已满！\n");
                    break;
                }
                printf("请输入第%d个学生的姓名：", count + 1);
                fgets(names[count], NAME_LEN, stdin);
                // 去掉fgets的换行符
                int len = strlen(names[count]);
                if (names[count][len - 1] == '\n')
                    names[count][len - 1] = '\0';

                printf("请输入%s的成绩：", names[count]);
                scanf("%d", &scores[count]);
                getchar();  // 吃掉换行符
                count++;
                printf("✅ 录入成功！\n");
                break;
            }
            case 2:  // 显示所有
                if (count == 0) {
                    printf("还没有学生数据。\n");
                    break;
                }
                printf("\n===== 学生成绩列表 =====\n");
                printf("序号\t姓名\t\t成绩\n");
                for (int i = 0; i < count; i++) {
                    printf("%d\t%s\t\t%d\n", i+1, names[i], scores[i]);
                }
                break;

            case 3: {  // 查询
                char searchName[NAME_LEN];
                printf("请输入要查询的姓名：");
                fgets(searchName, NAME_LEN, stdin);
                int len = strlen(searchName);
                if (searchName[len - 1] == '\n')
                    searchName[len - 1] = '\0';

                int found = 0;
                for (int i = 0; i < count; i++) {
                    if (strcmp(names[i], searchName) == 0) {
                        printf("找到：%s，成绩：%d\n", names[i], scores[i]);
                        found = 1;
                        break;
                    }
                }
                if (!found) printf("未找到 %s\n", searchName);
                break;
            }
            case 4:  // 统计
                if (count == 0) {
                    printf("还没有学生数据。\n");
                    break;
                }
                int sum = 0, max = scores[0], min = scores[0];
                for (int i = 0; i < count; i++) {
                    sum += scores[i];
                    if (scores[i] > max) max = scores[i];
                    if (scores[i] < min) min = scores[i];
                }
                printf("\n===== 成绩统计 =====\n");
                printf("学生人数：%d\n", count);
                printf("平均分：%.1f\n", (float)sum / count);
                printf("最高分：%d\n", max);
                printf("最低分：%d\n", min);
                // 及格率
                int passCount = 0;
                for (int i = 0; i < count; i++) {
                    if (scores[i] >= 60) passCount++;
                }
                printf("及格率：%.1f%%\n", 100.0 * passCount / count);
                break;

            case 0:
                printf("感谢使用，再见！\n");
                return 0;

            default:
                printf("❌ 无效选项！\n");
        }
    }
}
```

---

## Day 22：第三阶段复习——数组与字符串能力自测

### 📋 第三阶段知识清单（Day 16-21）

| 知识点 | 掌握标准 | 自测 |
|--------|----------|------|
| 一维数组声明与初始化 | 能手写3种初始化方式 | ☐ |
| 数组遍历（for循环） | 能用循环遍历任意大小数组 | ☐ |
| 数组越界 | 理解为什么arr[5]只有0-4 | ☐ |
| sizeof计算数组大小 | `sizeof(arr)/sizeof(arr[0])` | ☐ |
| 冒泡排序 | 能手写完整冒泡排序代码 | ☐ |
| 顺序查找 | 能写出查找并返回位置的代码 | ☐ |
| 二维数组 | 能理解`arr[行][列]`的逻辑 | ☐ |
| 字符数组与\0 | 理解\0是字符串结束标志 | ☐ |
| strlen/strcpy/strcmp/strcat | 能说出4个函数的功能 | ☐ |
| fgets读取带空格字符串 | 能处理fgets保留的换行符 | ☐ |

---

## Day 23：函数（上）—— 代码复用的开始

### 🎯 今日学习目标
学完后你能：
- 理解为什么需要函数
- 掌握函数的定义、声明、调用
- 理解形式参数与实际参数

---

### 📖 通俗化知识点讲解

#### 1. 函数是什么？为什么需要它？

> **生活类比**：微波炉就是一个"函数"。
> - **输入**（参数）：放进去的食物、设定的时间
> - **处理**（函数体）：加热
> - **输出**（返回值）：热好的食物
>
> 你不需要知道微波炉内部怎么工作的（封装），只需要知道怎么用（接口）。
> 而且一台微波炉全家人用，不用每人买一台（代码复用）。

```c
// 函数的四个部分
int add(int a, int b)     // 函数头
{                          // ┐
    int result = a + b;    // │ 函数体
    return result;         // │
}                          // ┘

//  ↑     ↑         ↑
// 返回类型 函数名  参数列表
```

#### 2. 形式参数 vs 实际参数

```c
int add(int x, int y) {   // x, y 是形式参数（形参）——"占位符"
    return x + y;
}

int main() {
    int sum = add(3, 5);  // 3, 5 是实际参数（实参）——"实际传进去的值"
    // 调用过程：x=3, y=5, return 3+5=8, sum=8
}
```

#### 3. 函数的声明与定义的分离

```c
#include <stdio.h>

// 函数声明（告诉编译器：有这个函数，后面会定义）
// 写在main之前！只写函数头+分号
int add(int a, int b);

int main() {
    printf("%d\n", add(3, 5));  // main可以调用add了
    return 0;
}

// 函数定义（函数的具体实现）
int add(int a, int b) {
    return a + b;
}
```

> **为什么要分离？** 因为编译器从上往下读代码。如果函数定义在main后面，main就"不认识"它。提前声明就是给编译器一个"预告"。

---

### 💻 上机敲代码

```c
/*
 * 文件名：function_basic.c
 * 功能：函数的定义、声明、调用
 */

#include <stdio.h>

// ===== 函数声明（写在main前面） =====
int max(int a, int b);           // 返回两个数中的较大值
int factorial(int n);            // 计算n的阶乘
void printLine(int length);      // 打印分隔线（无返回值用void）
int isPrime(int n);              // 判断素数

// ===== main函数 =====
int main()
{
    // 调用max函数
    int bigger = max(15, 27);
    printf("15和27中较大的是：%d\n", bigger);

    // 调用factorial函数
    int n = 5;
    printf("%d! = %d\n", n, factorial(n));

    // 调用printLine（void函数，不需要接收返回值）
    printLine(30);

    // 批量判断素数
    printf("1到50之间的素数：\n");
    int count = 0;
    for (int i = 2; i <= 50; i++) {
        if (isPrime(i)) {
            printf("%d ", i);
            count++;
        }
    }
    printf("\n共 %d 个素数\n", count);

    return 0;
}

// ===== 函数定义（写在main后面） =====

// 函数1：求两个数的最大值
int max(int a, int b) {
    if (a > b) {
        return a;    // return：把结果"返回"给调用者
    } else {
        return b;    // return 之后的代码不会执行
    }
}

// 函数2：计算阶乘 n! = 1×2×3×...×n
int factorial(int n) {
    int result = 1;
    for (int i = 1; i <= n; i++) {
        result *= i;
    }
    return result;
}

// 函数3：打印分隔线（无返回值，用void）
void printLine(int length) {
    printf("\n");
    for (int i = 0; i < length; i++) {
        printf("=");
    }
    printf("\n\n");
}

// 函数4：判断素数
int isPrime(int n) {
    if (n < 2) return 0;             // 小于2的不是素数
    for (int i = 2; i * i <= n; i++) {
        if (n % i == 0) {
            return 0;                 // 找到了因子，不是素数
        }
    }
    return 1;                         // 是素数
}
```

---

### 📋 今日核心知识点总结

1. 函数四要素：**返回类型、函数名、参数列表、函数体**
2. `return` 把结果返回给调用者，并**结束函数执行**
3. `void` 表示"没有返回值"，不需要写return（或只写`return;`）
4. 函数声明 = 函数头 + 分号；函数定义 = 函数头 + 函数体
5. 函数让代码**可复用**、**易维护**、**结构清晰**

---

## Day 24-25：函数（中）—— 参数传递与作用域

### 🎯 今日学习目标
学完后你能：
- 理解值传递的本质
- 掌握局部变量和全局变量的区别
- 理解变量作用域和生命周期

---

### 📖 通俗化知识点讲解

#### 1. 值传递——C语言的参数传递方式

> **生活类比**：复印文件。
> 你把一份文件**复印**了交给同事——同事在复印件上写写画画，不影响你的原件。
>
> C语言中，调用函数时是把实参的**值复制一份**给形参。函数内修改形参，**不影响外部的原始变量**。

```c
void changeValue(int x) {
    x = 999;          // 修改的是x（复印件）
    printf("函数内：x = %d\n", x);  // 999
}

int main() {
    int num = 10;
    changeValue(num);    // 把num的值10复制给x
    printf("main中：num = %d\n", num);  // 还是10，没有变！
    return 0;
}
```

> ⚠️ 如果你真的想在函数内修改外部变量，需要用**指针**（Day 29会讲）。

#### 2. 局部变量 vs 全局变量

```c
#include <stdio.h>

int globalVar = 100;   // 全局变量：在所有函数外面声明
                        // 整个程序的任何函数都能访问

void test() {
    int localVar = 50;         // 局部变量：在函数内部声明
    printf("test中：globalVar=%d, localVar=%d\n", globalVar, localVar);
}

int main() {
    int localVar = 20;         // main函数的局部变量，和test的互不影响
    printf("main中：globalVar=%d, localVar=%d\n", globalVar, localVar);
    test();
    // printf("%d", test中的localVar);  // ❌ 编译错误！无法访问其他函数的局部变量
    return 0;
}
```

| 对比维度 | 局部变量 | 全局变量 |
|----------|----------|----------|
| 声明位置 | 函数内部 | 所有函数外面 |
| 作用范围 | 仅限本函数 | 整个程序 |
| 生命周期 | 函数调用时创建，返回时销毁 | 程序开始时创建，结束时销毁 |
| 初始值 | 随机值（需手动初始化） | 自动初始化为0 |
| 建议 | **尽量用局部变量** | 谨慎使用，容易造成混乱 |

---

### 💻 上机敲代码

```c
/*
 * 文件名：function_scope.c
 * 功能：值传递、作用域、局部/全局变量
 */

#include <stdio.h>

// 全局变量（尽量少用）
int callCount = 0;   // 统计函数被调用了多少次

// 函数声明
void swap(int a, int b);            // 值传递——不能真正交换
void showCallCount(void);           // 显示调用次数
void localVarDemo(void);            // 局部变量演示

int main()
{
    // ===== 值传递的限制 =====
    printf("===== 值传递演示 =====\n");
    int x = 10, y = 20;
    printf("交换前：x=%d, y=%d\n", x, y);
    swap(x, y);   // 试图交换——但不会成功！
    printf("交换后：x=%d, y=%d（没变！因为值传递）\n", x, y);

    // ===== 全局变量演示 =====
    showCallCount();
    showCallCount();
    showCallCount();

    // ===== 局部变量演示 =====
    localVarDemo();

    return 0;
}

// 试图交换两个数——但因为是值传递，外部变量不会改变！
void swap(int a, int b) {
    printf("  swap内交换前：a=%d, b=%d\n", a, b);
    int temp = a;
    a = b;
    b = temp;
    printf("  swap内交换后：a=%d, b=%d\n", a, b);
    callCount++;   // 修改全局变量
}

void showCallCount(void) {
    callCount++;
    printf("showCallCount 被调用了，总调用次数：%d\n", callCount);
}

void localVarDemo(void) {
    // 局部变量每次函数调用时重新创建
    int count = 0;    // 如果不初始化，值是随机的！
    count++;
    printf("localVarDemo: count = %d（每次都重新从0开始）\n", count);

    // 静态局部变量——只初始化一次，函数返回后值保留
    static int staticCount = 0;
    staticCount++;
    printf("localVarDemo: staticCount = %d（一直累计）\n", staticCount);
}
```

---

### 📋 今日核心知识点总结

1. C语言参数传递是**值传递**——函数收到的是实参的副本
2. 函数内修改形参**不影响**外部的实参变量
3. 局部变量：函数内部声明，只能在本函数使用
4. 全局变量：在所有函数外声明，整个程序都能用
5. `static` 局部变量：值在函数调用之间保持，但作用域仍是局部的

---

## Day 26：函数（下）—— 递归入门

### 🎯 今日学习目标
学完后你能：
- 理解递归的基本概念（函数调用自己）
- 掌握递归的两个必要条件（基准条件+递归条件）
- 用递归解决阶乘、斐波那契等经典问题

---

### 📖 通俗化知识点讲解

#### 1. 什么是递归？

> **生活类比**：俄罗斯套娃。
> 你打开一个娃娃，里面还有一个更小的娃娃，再打开，里面还有一个...
> 直到最小的那个打不开为止（基准条件）。
>
> 递归就是**函数调用自己**，每一层问题规模缩小，直到到达"最简单的情况"。

#### 2. 递归的两个必要条件

```c
int factorial(int n) {
    if (n <= 1) {         // ① 基准条件（Base Case）：停止递归
        return 1;         //    最简单的情况，直接返回
    }
    return n * factorial(n - 1);  // ② 递归条件：问题缩小后调用自己
}

// factorial(4) 的执行过程：
// factorial(4) = 4 * factorial(3)
//              = 4 * 3 * factorial(2)
//              = 4 * 3 * 2 * factorial(1)
//              = 4 * 3 * 2 * 1
//              = 24
```

> ⚠️ **没有基准条件的递归 = 无限循环 = 栈溢出（Stack Overflow）**
> 每次函数调用都占用一块内存（栈帧），无限递归会耗尽内存，程序崩溃。

---

### 💻 上机敲代码

```c
/*
 * 文件名：recursion_demo.c
 * 功能：递归入门——阶乘、斐波那契、汉诺塔思路
 */

#include <stdio.h>

// 函数声明
long long factorial(int n);           // 递归求阶乘
long long fibonacci(int n);           // 递归求斐波那契（效率低，仅演示）
long long fibonacci_iter(int n);      // 迭代求斐波那契（效率高）
void printBinary(int n);              // 递归打印二进制

int main()
{
    // ===== 一、递归求阶乘 =====
    printf("===== 递归求阶乘 =====\n");
    for (int i = 1; i <= 10; i++) {
        printf("%d! = %lld\n", i, factorial(i));
        // %lld 是 long long 类型的占位符
    }

    // ===== 二、斐波那契数列 =====
    printf("\n===== 斐波那契数列 =====\n");
    printf("递归版（慢）：");
    for (int i = 1; i <= 15; i++) {
        printf("%lld ", fibonacci(i));
    }
    printf("\n");

    printf("迭代版（快）：");
    for (int i = 1; i <= 15; i++) {
        printf("%lld ", fibonacci_iter(i));
    }
    printf("\n");

    // ===== 三、递归应用：十进制转二进制 =====
    printf("\n===== 十进制转二进制 =====\n");
    int nums[] = {5, 10, 42, 255};
    for (int i = 0; i < 4; i++) {
        printf("%d 的二进制：", nums[i]);
        printBinary(nums[i]);
        printf("\n");
    }

    return 0;
}

// 递归求阶乘
long long factorial(int n) {
    if (n <= 1) return 1;               // 基准条件
    return n * factorial(n - 1);         // 递归条件
}

// 递归求斐波那契（教学用，实际效率很低）
// fib(1)=1, fib(2)=1, fib(n)=fib(n-1)+fib(n-2)
long long fibonacci(int n) {
    if (n <= 2) return 1;                // 基准条件
    return fibonacci(n - 1) + fibonacci(n - 2);  // 递归条件
    // 这个实现有大量重复计算！fib(40)可能要算很久
}

// 迭代求斐波那契（推荐，效率高）
long long fibonacci_iter(int n) {
    if (n <= 2) return 1;
    long long a = 1, b = 1, c;
    for (int i = 3; i <= n; i++) {
        c = a + b;   // 下一个 = 前两个之和
        a = b;       // 往前移动
        b = c;
    }
    return c;
}

// 递归打印二进制（利用递归的"后进先出"特性）
void printBinary(int n) {
    if (n >= 2) {
        printBinary(n / 2);   // 先递归处理高位
    }
    printf("%d", n % 2);       // 再打印低位
    // 这样就实现了"从高位到低位"的顺序输出
}
```

---

### 📋 今日核心知识点总结

1. 递归 = 函数自己调用自己，每次问题规模缩小
2. 两个必要条件：**基准条件**（停止）+ **递归条件**（继续缩小）
3. 递归优势：代码简洁优雅（如二叉树遍历）
4. 递归劣势：可能效率低、占用栈空间、理解门槛高
5. 能用迭代（循环）解决的问题，优先用迭代

---

## Day 27：函数阶段综合练习——模块化改写

### 🎯 今日学习目标
- 把之前写的"一坨"代码用函数重构
- 体会函数带来的代码结构提升

---

### 💻 上机敲代码

```c
/*
 * 文件名：modular_calculator.c
 * 功能：用函数重构的计算器（模块化设计）
 * 覆盖：函数定义/调用、参数传递、返回值、菜单循环
 */

#include <stdio.h>
#include <math.h>    // fabs（浮点数绝对值）用

// ===== 函数声明（"目录"区） =====
void showMenu(void);                    // 显示菜单
double getNumber(void);                 // 获取用户输入的数字
double add(double a, double b);         // 加法
double subtract(double a, double b);    // 减法
double multiply(double a, double b);    // 乘法
double divide(double a, double b, int *error);  // 除法（带错误处理）
int getMod(int a, int b, int *error);          // 取余（带错误处理）
void showResult(double a, double b, char op, double result);  // 显示结果

// ===== 主函数（"控制中心"） =====
int main()
{
    int choice;
    double num1, num2, result;
    int error = 0;       // 错误标记：0=正常，1=出错

    while (1) {
        showMenu();
        printf("请选择操作：");
        scanf("%d", &choice);

        if (choice == 0) {
            printf("感谢使用，再见！\n");
            break;
        }

        if (choice >= 1 && choice <= 5) {
            printf("请输入第一个数：");
            num1 = getNumber();
            printf("请输入第二个数：");
            num2 = getNumber();
        }

        error = 0;   // 每次操作前重置错误标记
        switch (choice) {
            case 1:
                result = add(num1, num2);
                showResult(num1, num2, '+', result);
                break;
            case 2:
                result = subtract(num1, num2);
                showResult(num1, num2, '-', result);
                break;
            case 3:
                result = multiply(num1, num2);
                showResult(num1, num2, '*', result);
                break;
            case 4:
                result = divide(num1, num2, &error);  // 注意传了 &error
                if (!error) showResult(num1, num2, '/', result);
                break;
            case 5: {
                int intNum1 = (int)num1, intNum2 = (int)num2;
                // 检查是否为整数
                if (fabs(num1 - intNum1) > 0.0001 || fabs(num2 - intNum2) > 0.0001) {
                    printf("❌ 取余需要整数！\n");
                    break;
                }
                int modResult = getMod(intNum1, intNum2, &error);
                if (!error)
                    printf("%d %% %d = %d\n", intNum1, intNum2, modResult);
                break;
            }
            default:
                printf("❌ 无效选项！\n");
        }
    }
    return 0;
}

// ===== 函数实现（"工具箱"区） =====

void showMenu(void) {
    printf("\n╔══════════════════════════╗\n");
    printf("║   模块化计算器 v3.0     ║\n");
    printf("╠══════════════════════════╣\n");
    printf("║ 1. 加法  (+)           ║\n");
    printf("║ 2. 减法  (-)           ║\n");
    printf("║ 3. 乘法  (×)           ║\n");
    printf("║ 4. 除法  (÷)           ║\n");
    printf("║ 5. 取余  (%)           ║\n");
    printf("║ 0. 退出                ║\n");
    printf("╚══════════════════════════╝\n");
}

double getNumber(void) {
    double num;
    scanf("%lf", &num);
    return num;
}

double add(double a, double b) { return a + b; }
double subtract(double a, double b) { return a - b; }
double multiply(double a, double b) { return a * b; }

double divide(double a, double b, int *error) {
    if (fabs(b) < 0.000001) {   // 判断浮点数是否接近0
        printf("❌ 除数不能为0！\n");
        *error = 1;              // 通过指针修改error的值
        return 0;
    }
    *error = 0;
    return a / b;
}

int getMod(int a, int b, int *error) {
    if (b == 0) {
        printf("❌ 除数不能为0！\n");
        *error = 1;
        return 0;
    }
    *error = 0;
    return a % b;
}

void showResult(double a, double b, char op, double result) {
    printf("%.2f %c %.2f = %.2f\n", a, op, b, result);
}
```

---

### 📋 今日核心知识点总结

1. 好的程序 = 清晰的函数划分 + 合理的函数命名
2. 每个函数**只做一件事**（单一职责原则）
3. main 函数像"总指挥"，调用各个工具函数
4. 函数让调试变得简单——可以单独测试每个函数

---

## Day 28：第四阶段复习——函数能力自测

### 📋 第四阶段知识清单（Day 23-27）

| 知识点 | 自测方式 |
|--------|----------|
| 函数定义四要素 | 能口头说出返回类型/函数名/参数/函数体 |
| 函数声明 vs 定义 | 能解释为什么需要函数声明 |
| 值传递 | 能解释为什么swap函数不能真正交换 |
| 局部变量 vs 全局变量 | 能说出两者的声明位置、作用域差异 |
| static局部变量 | 能解释static变量的特殊行为 |
| 递归 | 能手写递归求阶乘 |
| 模块化编程 | 能把一个长程序拆成多个函数 |

---

## Day 29：指针入门（上）—— C语言的灵魂

### 🎯 今日学习目标
学完后你能：
- 理解指针的本质（存储地址的变量）
- 掌握 `&` 取地址和 `*` 解引用
- 用指针间接修改外部变量的值

---

### 📖 通俗化知识点讲解

#### 1. 指针是什么？

> **生活类比**：快递柜。
> - 你的快递在**3号柜第5层**——这个位置就是"地址"
> - 你把位置信息存在手机备忘录里——备忘录就是"指针变量"
> - 你根据备忘录上的位置去打开柜子拿快递——这就是"解引用"
>
> **指针 = 存储另一个变量地址的变量**

```
普通变量 int a = 10：
┌──────────┐
│ 变量名: a │
│ 值: 10   │
│ 地址: 0x7fff1234  ← 系统分配的编号，就像身份证号
└──────────┘

指针变量 int *p = &a：
┌──────────┐
│ 变量名: p │
│ 值: 0x7fff1234  ← p存的是a的地址
│ 自己的地址: 0x7fff5678
└──────────┘
```

```c
int a = 10;      // 声明普通变量，a = 10
int *p = &a;     // 声明指针变量，p = a的地址
                 // int* 表示"指向int的指针"
                 // &a 表示"获取a的地址"

printf("%d\n", a);   // 10 —— 直接访问a的值
printf("%p\n", &a);  // 某个地址 —— a的地址
printf("%p\n", p);   // 同一个地址！ —— p的值就是a的地址
printf("%d\n", *p);  // 10 —— *p 表示"访问p指向的那个变量的值"
```

#### 2. 三个关键符号

| 符号 | 名称 | 作用 | 示例 |
|------|------|------|------|
| `&` | 取地址运算符 | 获取变量的地址 | `&a` → a的地址 |
| `*` | 解引用运算符 | 通过地址访问变量 | `*p` → p指向的变量的值 |
| `int*` | 指针类型声明 | 声明一个指针变量 | `int *p` → p是指向int的指针 |

#### 3. 指针最重要的应用：让函数真正修改外部变量

```c
// 之前：值传递，无法修改
void swap_fail(int a, int b) { ... }  // 改不了main里的变量

// 用指针：把变量的地址传进去，函数通过地址直接修改原变量！
void swap_ok(int *a, int *b) {
    int temp = *a;   // *a 是"a指向的那个变量的值"
    *a = *b;
    *b = temp;
}
// 调用：swap_ok(&x, &y); —— 传入x和y的地址
```

---

### 💻 上机敲代码

```c
/*
 * 文件名：pointer_basic.c
 * 功能：指针基本概念——取地址、解引用、指针传参
 */

#include <stdio.h>

// 函数声明
void swap(int *a, int *b);            // 用指针真正交换两个数
void changeValue(int *p, int newVal); // 用指针修改外部变量

int main()
{
    // ===== 一、& 和 * 的基本用法 =====
    printf("===== & 和 * 的基本用法 =====\n");

    int num = 42;
    int *ptr = &num;    // ptr 存的是 num 的地址
                         // 读作：ptr 是一个指向 int 的指针，指向 num

    printf("num 的值：%d\n", num);           // 42
    printf("num 的地址：%p\n", (void*)&num); // 某个十六进制地址
    printf("ptr 的值（也是num的地址）：%p\n", (void*)ptr);
    printf("ptr 指向的内容 *ptr：%d\n", *ptr); // 42（通过指针访问num）

    // 通过指针修改 num 的值（间接修改）
    *ptr = 100;    // 相当于 num = 100
    printf("\n*ptr = 100 后，num 的值：%d\n", num);  // 100

    // ===== 二、指针的真正威力——函数传参 =====
    printf("\n===== 用指针实现真正的swap =====\n");

    int x = 10, y = 20;
    printf("交换前：x = %d, y = %d\n", x, y);

    swap(&x, &y);  // 传入 x 和 y 的地址！
                   // 注意：普通变量前加 &；数组名前不加 &
    printf("交换后：x = %d, y = %d\n", x, y);  // 真的交换了！

    // ===== 三、常用模式：指针参数作为"输出" =====
    printf("\n===== 指针参数输出值 =====\n");
    int score = 60;
    printf("修改前：score = %d\n", score);
    changeValue(&score, 95);
    printf("修改后：score = %d\n", score);

    // ===== 四、空指针 NULL =====
    int *nullPtr = NULL;   // NULL 表示"这个指针不指向任何东西"
    if (nullPtr == NULL) {
        printf("\nnullPtr 是空指针，不指向任何有效地址。\n");
    }
    // *nullPtr = 5;  // ❌ 解引用空指针会导致程序崩溃！

    return 0;
}

// 用指针交换两个变量的值
void swap(int *a, int *b) {
    int temp = *a;   // 把a指向的变量的值暂存到temp
    *a = *b;         // 把b指向的变量的值赋给a指向的变量
    *b = temp;       // 把temp赋给b指向的变量
}

// 通过指针修改外部变量
void changeValue(int *p, int newVal) {
    *p = newVal;     // 直接修改 p 指向的那个变量的值
}
```

---

### 📋 今日核心知识点总结

1. 指针变量存的是**另一个变量的地址**
2. `&变量` 获取变量的地址；`*指针` 访问指针指向的变量
3. 声明时 `int *p` 表示 p 是指向 int 的指针
4. 指针的值可以直接打印出来：`printf("%p", (void*)ptr)`
5. **指针让函数可以真正修改外部变量**——传入地址，通过解引用修改

> 📌 **今天的内容非常关键。如果没完全理解，把代码多敲几遍，对着 [appendix-c-指针核心图解笔记.md](appendix-c-指针核心图解笔记.md) 画内存图。**

---

## Day 30：指针入门（下）—— 指针与数组

### 🎯 今日学习目标
学完后你能：
- 理解数组名就是指向第一个元素的指针
- 通过指针遍历数组
- 理解指针的算术运算（+、-、++、--）

---

### 📖 通俗化知识点讲解

#### 1. 数组名就是指针

> **核心原理**：数组名 `arr` 等价于 `&arr[0]`——指向数组第一个元素的指针。

```c
int arr[] = {10, 20, 30, 40, 50};

// arr 和 &arr[0] 是同一个地址
printf("%p\n", (void*)arr);       // 输出：某个地址
printf("%p\n", (void*)&arr[0]);  // 输出：同一个地址

// 所以你可以这样访问数组元素：
printf("%d\n", arr[0]);    // 10（下标方式）
printf("%d\n", *arr);       // 10（指针方式！arr指向第一个元素）

printf("%d\n", arr[2]);    // 30（下标方式）
printf("%d\n", *(arr+2));   // 30（指针方式！arr+2指向第三个元素）
```

#### 2. 指针算术运算

```c
int arr[] = {10, 20, 30, 40, 50};
int *p = arr;   // p 指向 arr[0]

p + 1   // 不是地址值+1！而是"指向下一个int"——地址值+4字节（因为int占4字节）
p + 2   // 指向再下一个——地址值+8字节
p++     // p自己往后移一位（指向下一个元素）
*p      // 当前指向的元素的值
```

> **关键理解**：`指针 + N` 的实际地址偏移量 = `N × sizeof(指针指向的类型)`。编译器自动处理这个乘法，你不用操心！

#### 3. 数组名 vs 指针的区别

```c
int arr[5] = {1, 2, 3, 4, 5};
int *p = arr;

arr = ???  // ❌ 编译错误！数组名是"常量指针"，不能改变指向
p = arr;   // ✅ 可以
p = &arr[2];  // ✅ 可以，现在p指向arr[2]
p++;        // ✅ 可以，指针变量可以自增
// arr++;   // ❌ 数组名不行！
```

| | 数组名 `arr` | 指针变量 `p` |
|---|---|---|
| 值 | `&arr[0]`（第一个元素的地址） | 可以指向任何同类型变量 |
| 能否改变 | ❌ 常量，不能改 | ✅ 变量，可以改 |
| sizeof | 整个数组的大小 | 指针本身的大小（4或8字节） |

---

### 💻 上机敲代码

```c
/*
 * 文件名：pointer_array.c
 * 功能：指针与数组的关系
 */

#include <stdio.h>

// 函数声明
void printArray(int *arr, int size);      // 用指针接收数组
void reverseArray(int *arr, int size);    // 用指针反转数组

int main()
{
    // ===== 一、数组名就是指针 =====
    int nums[] = {10, 20, 30, 40, 50};
    int size = sizeof(nums) / sizeof(nums[0]);

    printf("===== 四种方式访问数组元素 =====\n");
    for (int i = 0; i < size; i++) {
        printf("nums[%d] = %d  |  *(nums+%d) = %d\n",
               i, nums[i], i, *(nums + i));
        // nums[i] 和 *(nums+i) 是完全等价的！
        // 实际上，编译器把 nums[i] 自动翻译成 *(nums+i)
    }

    // ===== 二、指针遍历数组 =====
    printf("\n===== 指针遍历 =====\n");
    int *p = nums;   // p 指向数组开头
    printf("指针方式遍历：");
    for (int i = 0; i < size; i++) {
        printf("%d ", *(p + i));   // p+i 偏移i个元素
    }
    printf("\n");

    // 另一种指针遍历方式（移动指针本身）
    printf("指针移动遍历：");
    for (int *ptr = nums; ptr < nums + size; ptr++) {
        //  ptr初始指向开头，每次++移到下一个元素
        printf("%d ", *ptr);
    }
    printf("\n");

    // ===== 三、数组名和指针的区别 =====
    printf("\n===== 数组名 vs 指针 =====\n");
    printf("sizeof(nums) = %d（整个数组的大小）\n", (int)sizeof(nums));
    printf("sizeof(p)    = %d（指针本身的大小）\n", (int)sizeof(p));
    // 在你的Windows 64位系统上，sizeof(p) 可能是8

    // ===== 四、函数传数组（实际传的是指针） =====
    printf("\n===== 函数处理数组 =====\n");
    printArray(nums, size);    // 传入数组名（指针）和大小

    reverseArray(nums, size);  // 反转数组
    printf("反转后：");
    printArray(nums, size);

    return 0;
}

// 用指针参数接收数组
void printArray(int *arr, int size) {
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);   // 指针也可以像数组一样用下标！
    }
    printf("\n");
}

// 用指针反转数组
void reverseArray(int *arr, int size) {
    int *left = arr;               // 指向开头
    int *right = arr + size - 1;    // 指向末尾
    while (left < right) {
        // 交换左右两个元素
        int temp = *left;
        *left = *right;
        *right = temp;
        left++;    // 左指针右移
        right--;   // 右指针左移
    }
}
```

---

### 📋 今日核心知识点总结

1. 数组名 = 指向第一个元素的**常量指针**
2. `arr[i]` 和 `*(arr + i)` **完全等价**
3. 指针+1 不是地址值+1，而是跳过**一个元素**的字节数
4. 函数传数组时，实际传的是指针，**必须同时传数组大小**
5. 数组名不能修改（常量），指针变量可以修改

---

> 📌 **继续学习**：Day 31-45 见 module-2 Part 3（指针深入+字符串+结构体）
