# Linux常用命令速查表

> 按使用频率从高到低排列。⭐ = 必须记住，★ = 常用，无标记 = 了解即可

---

## 一、基础操作（必须倒背如流）

| 命令 | 用途 | 常用参数 | 示例 | 星级 |
|------|------|----------|------|------|
| `pwd` | 显示当前路径 | — | `pwd` | ⭐ |
| `ls` | 列出文件和目录 | `-l` 详细信息, `-a` 含隐藏, `-h` 人类可读大小 | `ls -lah` | ⭐ |
| `cd` | 切换目录 | `~` 家目录, `..` 上级, `-` 上一个, `/` 根 | `cd ~/Documents` | ⭐ |
| `whoami` | 当前用户名 | — | `whoami` | ⭐ |
| `clear` | 清屏 | — | `clear` | ⭐ |
| `man` | 查看命令手册 | — | `man ls`（按q退出） | ⭐ |

## 二、文件操作

| 命令 | 用途 | 常用参数 | 示例 | 星级 |
|------|------|----------|------|------|
| `touch` | 创建空文件 | — | `touch file.txt` | ⭐ |
| `mkdir` | 创建目录 | `-p` 递归创建父目录 | `mkdir -p a/b/c` | ⭐ |
| `cp` | 复制 | `-r` 递归(文件夹), `-i` 覆盖前确认 | `cp -r src/ dest/` | ⭐ |
| `mv` | 移动/重命名 | `-i` 覆盖前确认 | `mv old.txt new.txt` | ⭐ |
| `rm` | 删除 | `-r` 递归, `-i` 确认, `-f` 强制 | `rm -i file.txt` | ⭐ |
| `cat` | 查看文件内容 | `-n` 显示行号 | `cat file.txt` | ⭐ |
| `less` | 分页查看(大文件) | — | `less large.log`（q退出） | ★ |
| `head` | 看文件前N行 | `-n` 行数 | `head -n 20 file.txt` | ★ |
| `tail` | 看文件后N行 | `-n` 行数, `-f` 实时追踪 | `tail -f /var/log/syslog` | ★ |
| `find` | 搜索文件 | `-name` 按名称, `-type` 按类型 | `find / -name "*.log"` | ★ |
| `file` | 判断文件类型 | — | `file unknown.bin` | |

## 三、文本处理

| 命令 | 用途 | 常用参数 | 示例 | 星级 |
|------|------|----------|------|------|
| `grep` | 搜索文本 | `-i` 忽略大小写, `-v` 反向, `-c` 计数, `-r` 递归 | `grep -r "password" ./` | ⭐ |
| `echo` | 输出文本 | `-n` 不换行, `-e` 解读转义符 | `echo "Hello"` | ⭐ |
| `sort` | 排序 | `-n` 数值, `-r` 逆序, `-u` 去重 | `sort -n numbers.txt` | ★ |
| `uniq` | 去重 | `-c` 计数, `-d` 只显示重复行 | `sort data.txt \| uniq -c` | ★ |
| `wc` | 统计 | `-l` 行数, `-w` 单词数, `-c` 字节数 | `wc -l file.txt` | ★ |
| `awk` | 文本列处理 | `'{print $1}'` 打印第1列 | `awk '{print $1}' access.log` | ★ |
| `sed` | 流编辑器 | `'s/旧/新/g'` 替换 | `sed 's/foo/bar/g' file.txt` | |
| `cut` | 按分隔符切分 | `-d` 分隔符, `-f` 字段号 | `cut -d: -f1 /etc/passwd` | |
| `tr` | 字符替换/删除 | — | `echo "ABC" \| tr 'A-Z' 'a-z'` | |
| `xxd` | 十六进制查看 | — | `xxd file.bin` | ★ |

## 四、权限与用户

| 命令 | 用途 | 常用参数 | 示例 | 星级 |
|------|------|----------|------|------|
| `chmod` | 修改权限 | `+x` 加执行, 数字法 | `chmod 755 script.sh` | ⭐ |
| `sudo` | 管理员权限执行 | — | `sudo apt update` | ⭐ |
| `su` | 切换用户 | `-` 同时切换环境 | `su - root` | ★ |
| `id` | 查看用户ID信息 | — | `id` | ★ |
| `passwd` | 修改密码 | — | `passwd` | |

## 五、进程与服务

| 命令 | 用途 | 常用参数 | 示例 | 星级 |
|------|------|----------|------|------|
| `ps` | 查看进程 | `aux` 所有用户全部进程 | `ps aux` | ★ |
| `top` | 实时进程监控 | — | `top`（按q退出） | ★ |
| `kill` | 终止进程 | `-9` 强制终止 | `kill -9 1234` | ★ |
| `systemctl` | 管理系统服务 | `start/stop/restart/status` | `sudo systemctl status ssh` | ★ |
| `&` | 后台运行 | — | `python3 server.py &` | |
| `jobs` | 查看后台任务 | — | `jobs` | |
| `fg` | 将后台任务调到前台 | — | `fg %1` | |

## 六、网络相关（安全方向高频）

| 命令 | 用途 | 常用参数 | 示例 | 星级 |
|------|------|----------|------|------|
| `ifconfig` | 查看网络接口 | — | `ifconfig` | ⭐ |
| `ip` | 现代网络配置 | `addr`, `route` | `ip addr` | ★ |
| `ping` | 测试连通性 | `-c` 发包次数 | `ping -c 4 8.8.8.8` | ⭐ |
| `netstat` | 网络连接状态 | `-tlnp` TCP监听端口 | `netstat -tlnp` | ★ |
| `ss` | 替代netstat | `-tlnp` | `ss -tlnp` | ★ |
| `curl` | HTTP请求 | `-X` 方法, `-H` 头, `-d` 数据 | `curl -X GET http://example.com` | ★ |
| `wget` | 下载文件 | `-O` 指定文件名 | `wget https://example.com/file.zip` | ★ |
| `nslookup` | DNS查询 | — | `nslookup example.com` | |

## 七、软件管理（Kali/Debian系）

| 命令 | 用途 | 常用参数 | 示例 | 星级 |
|------|------|----------|------|------|
| `apt update` | 更新软件列表 | 需要sudo | `sudo apt update` | ⭐ |
| `apt install` | 安装软件 | `-y` 自动确认 | `sudo apt install python3 -y` | ⭐ |
| `apt remove` | 卸载软件 | — | `sudo apt remove python3` | ★ |
| `apt search` | 搜索软件 | — | `apt search "web scanner"` | |
| `dpkg -i` | 安装.deb包 | — | `sudo dpkg -i package.deb` | |

## 八、压缩与归档

| 命令 | 用途 | 常用参数 | 示例 | 星级 |
|------|------|----------|------|------|
| `tar` | 打包/解包 | `-czf` 创建gzip, `-xzf` 解压 | `tar -czf backup.tar.gz folder/` | ★ |
| `gzip` | 压缩文件 | `-d` 解压 | `gzip file.txt` | |
| `unzip` | 解压.zip | — | `unzip file.zip` | ★ |

## 九、Vim速记 (vimtutor)

| 操作 | 按键 | 模式 |
|------|------|------|
| 进入插入模式 | `i` | Normal → Insert |
| 行尾插入 | `A` | Normal → Insert |
| 下方新行插入 | `o` | Normal → Insert |
| 返回普通模式 | `Esc` | Insert → Normal |
| 删除一行 | `dd` | Normal |
| 删除一个字符 | `x` | Normal |
| 撤销 | `u` | Normal |
| 复制一行 | `yy` | Normal |
| 粘贴 | `p` | Normal |
| 保存 | `:w` | Command |
| 退出 | `:q` | Command |
| 保存并退出 | `:wq` | Command |
| 不保存强制退出 | `:q!` | Command |
| 搜索 | `/关键词` | Normal |
| 跳到第N行 | `:N` | Command |

---

## 🎯 每日命令抽查法

每天随机抽5个命令，不看笔记，默写：
1. 命令名称
2. 用途（一句话）
3. 常用参数（至少1个）
4. 一个使用示例

**示例**：
```
命令：grep
用途：在文本中搜索匹配的行
常用参数：-i（忽略大小写）
示例：grep "error" /var/log/syslog
```

---

> 📌 打印此表贴在书桌旁，每天敲命令时瞄一眼，两周就能记熟。
