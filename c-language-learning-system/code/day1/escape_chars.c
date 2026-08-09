/*
 * 文件名：escape_chars.c
 * 功能：认识C语言转义字符
 */

#include <stdio.h>

int main()
{
    printf("转义字符演示：\n\n");    // \n\n 连续两个换行 = 空一行

    printf("第一行\n");              // \n 换行
    printf("第二行\t中间有制表符\n"); // \t 跳格（Tab键效果，对齐用）
    printf("他说：\"你好！\"\n");     // \" 输出双引号本身
    printf("路径是：C:\\code\\\n");   // \\ 输出反斜杠本身
    printf("下划线在这里：_\b^\n");   // \b 退格（光标左移一格）

    return 0;
}
