# GitHub 入门指南 — 从零到实战

> 适用对象：零基础新手 | 预计学习时间：2-3 小时 | 更新日期：2026-07-11

---

## 目录

1. [概念速览 — Git 和 GitHub 是什么](#1-概念速览--git-和-github-是什么)
2. [环境搭建 — 安装 Git](#2-环境搭建--安装-git)
3. [首次配置 — Git 初始化设置](#3-首次配置--git-初始化设置)
4. [注册 GitHub 账号](#4-注册-github-账号)
5. [核心工作流 — 本地操作](#5-核心工作流--本地操作)
6. [核心工作流 — 连接远程仓库](#6-核心工作流--连接远程仓库)
7. [分支管理](#7-分支管理)
8. [Pull Request 协作流程](#8-pull-request-协作流程)
9. [日常开发场景速查](#9-日常开发场景速查)
10. [常见报错与解决](#10-常见报错与解决)
11. [进阶方向](#11-进阶方向)

---

## 1. 概念速览 — Git 和 GitHub 是什么

| 工具 | 一句话解释 | 类比 |
|------|-----------|------|
| **Git** | 版本控制系统，记录文件的每一次修改 | 游戏的"存档"系统 — 随时可以回到之前的存档点 |
| **GitHub** | 基于 Git 的代码托管网站 | 网盘 + 社交网络 — 存放代码、和别人协作 |

**它们的关系：Git 是工具，GitHub 是平台。** 你在自己电脑上用 Git 管理代码，然后把代码推送到 GitHub 上备份和分享。

### 什么场景用 Git？

- 写代码时改坏了想回退 → `git restore`
- 想尝试新功能又怕搞乱原代码 → `git branch`
- 多人协作时合并各自的改动 → `git merge` / Pull Request
- 代码发布新版本 → `git tag`
- 你的 Python 课程作业、C 语言练习、打卡项目 → 全部可以用 Git 管理！

---

## 2. 环境搭建 — 安装 Git

### Windows

1. 打开 [Git 官方下载页](https://git-scm.com/downloads/win)
2. 下载 **64-bit Git for Windows Setup**
3. 运行安装程序，**一路默认选项即可**（遇到编辑器选择时建议选 VS Code）
4. 安装完成后，在桌面右键 → 出现 **"Open Git Bash here"** 即安装成功

### 验证安装

打开 PowerShell 或 Git Bash，输入：

```bash
git --version
# 输出示例: git version 2.47.0
```

---

## 3. 首次配置 — Git 初始化设置

安装完成后必须配置用户名和邮箱（这些信息会显示在你的提交记录中）：

```bash
# 替换成你自己的名字和邮箱
git config --global user.name "你的名字"
git config --global user.email "your-email@example.com"

# 验证配置
git config --global user.name
git config --global user.email
```

**建议额外配置：**

```bash
# 默认分支名改为 main（GitHub 新仓库的默认名）
git config --global init.defaultBranch main

# 换行符自动转换（Windows 必备，避免协作时换行符混乱）
git config --global core.autocrlf true
```

---

## 4. 注册 GitHub 账号

1. 打开 [github.com](https://github.com)
2. 点击右上角 **Sign up**
3. 填写邮箱、密码、用户名
4. 完成邮箱验证
5. 登录后进入你的个人主页：`https://github.com/你的用户名`

### 推荐设置

- **个人头像** → Settings → Profile → 上传头像（让你的主页更专业）
- **两步验证** → Settings → Password and authentication → 开启 2FA（保护账号安全）
- **SSH Key**（见下一节，推送代码免输密码）

---

## 5. 核心工作流 — 本地操作

### 5.1 创建本地仓库

```bash
# 进入你的项目文件夹
cd D:\无限进步

# 初始化为 Git 仓库（只执行一次）
git init

# 查看仓库状态
git status
# 输出: On branch main, No commits yet
```

### 5.2 工作区 → 暂存区 → 仓库

Git 有三个区域，文件在其中流转：

```
工作区（Working Directory）  →  暂存区（Staging Area）  →  本地仓库（Repository）
 你正在编辑的文件               git add 后暂存              git commit 后永久保存
```

```bash
# 第一步：把修改添加到暂存区
git add 文件名           # 添加单个文件
git add .                # 添加当前目录所有修改（最常用）
git add *.py             # 添加所有 .py 文件

# 第二步：提交到本地仓库
git commit -m "写清楚这次改了什么"

# 好的 commit message 示例：
git commit -m "修复打卡页面的日期显示Bug"
git commit -m "添加Python第15课：函数参数详解"
git commit -m "重构数据库模块，拆分init_db函数"

# 查看提交历史
git log                  # 完整历史
git log --oneline        # 简洁模式，一行一条
git log --oneline -5     # 只看最近5条
```

### 5.3 撤销操作（救命命令）

```bash
# 场景1: 文件改坏了，想回到上次 commit 的状态
git restore 文件名

# 场景2: add 错了，移出暂存区
git restore --staged 文件名

# 场景3: commit message 写错了，修改最近一次提交
git commit --amend -m "新的提交信息"

# 场景4: 回到某个历史版本看看（不影响当前工作）
git log --oneline        # 先找到目标版本号
git checkout 版本号       # 切换到那个版本
git checkout main        # 回到最新版本
```

---

## 6. 核心工作流 — 连接远程仓库

### 6.1 在 GitHub 上创建远程仓库

1. 登录 GitHub → 点击右上角 **+** → **New repository**
2. 填写仓库名（如 `python-learning`）
3. 选择 Public（公开）或 Private（私有）
4. **不要勾选** "Add a README file"（因为本地已有代码）
5. 点击 **Create repository**

### 6.2 关联本地仓库并推送

创建后 GitHub 会显示一段代码，复制执行：

```bash
# 添加远程仓库地址（给远程仓库起个名叫 origin）
git remote add origin https://github.com/你的用户名/仓库名.git

# 第一次推送（-u 绑定上游分支，之后只用 git push 即可）
git push -u origin main

# 以后的推送
git push
```

### 6.3 从 GitHub 克隆到本地

```bash
# 把别人的（或你自己的）仓库下载到本地
git clone https://github.com/用户名/仓库名.git

# 进入克隆的目录，就可以开始开发了
cd 仓库名
```

### 6.4 拉取最新代码

```bash
# 把远程仓库的最新改动同步到本地
git pull

# 等价于 git fetch（下载） + git merge（合并）
```

### 6.5 配置 SSH Key（免密码推送）

每次都输密码很麻烦，配置 SSH Key 后一劳永逸：

```bash
# 第一步：生成 SSH Key（一路回车即可）
ssh-keygen -t ed25519 -C "你的邮箱"

# 第二步：复制公钥内容
cat ~/.ssh/id_ed25519.pub

# 第三步：打开 GitHub → Settings → SSH and GPG keys → New SSH key
# 粘贴公钥内容，标题随便填

# 第四步：测试连接
ssh -T git@github.com
# 成功输出: Hi 你的用户名! You've successfully authenticated...

# 第五步：把远程仓库地址从 HTTPS 改为 SSH
git remote set-url origin git@github.com:用户名/仓库名.git
```

---

## 7. 分支管理

### 7.1 什么是分支？

分支让你在不影响主线代码的情况下开发新功能。默认分支叫 `main`（旧名 `master`）。

```
main:    ●──●──●──●──●      （稳定版本）
                  \
feature:           ●──●      （正在开发的新功能，不影响 main）
```

### 7.2 分支操作速查

```bash
# 查看所有分支
git branch                  # 本地分支
git branch -a               # 包括远程分支

# 创建分支
git branch 新功能名

# 切换分支
git checkout 新功能名
# 或使用新命令
git switch 新功能名

# 创建并切换到新分支（一步到位）
git checkout -b 新功能名
# 或
git switch -c 新功能名

# 合并分支（先把要合并到的分支切换过去）
git checkout main           # 切换到 main
git merge 新功能名           # 把新功能合并到 main

# 删除分支（合并完成后）
git branch -d 新功能名       # 安全删除（已合并的）
git branch -D 新功能名       # 强制删除（没合并也要删）
```

### 7.3 解决合并冲突

当两个分支修改了同一文件的同一行时，Git 无法自动合并，需要手动处理：

```bash
# 发生冲突时，Git 会标记冲突位置：
<<<<<<< HEAD
这是当前分支（main）的内容
=======
这是要合并分支的内容
>>>>>>> 新功能名

# 手动编辑文件，保留正确的内容，删除 <<< === >>> 标记
# 然后：
git add 解决冲突的文件
git commit -m "解决合并冲突：xxx"
```

---

## 8. Pull Request 协作流程

Pull Request（简称 PR）是 GitHub 的核心协作机制：**你完成了一个功能的代码，发起 PR 请求别人审核后合并到主分支。**

### 标准流程

```bash
# 1. Fork 别人的仓库（在 GitHub 网页上点 Fork 按钮）
#    → 你的 GitHub 下会多一个同名仓库副本

# 2. 克隆你 Fork 的仓库到本地
git clone https://github.com/你的用户名/仓库名.git
cd 仓库名

# 3. 创建功能分支
git checkout -b fix-bug-xxx

# 4. 修改代码、测试、提交
git add .
git commit -m "修复xxx问题"

# 5. 推送到你的远程仓库
git push -u origin fix-bug-xxx

# 6. 回到 GitHub 网页，点击 "Compare & pull request"
#    → 写清楚你做了什么改动
#    → 点击 "Create pull request"
#    → 等待仓库维护者审核和合并
```

### 保持 Fork 与原仓库同步

```bash
# 添加原仓库为 upstream
git remote add upstream https://github.com/原作者/仓库名.git

# 拉取原仓库最新代码
git fetch upstream
git checkout main
git merge upstream/main

# 推送到你自己的 Fork
git push origin main
```

---

## 9. 日常开发场景速查

### 场景 A：每天开始写代码前

```bash
git pull          # 拉取最新代码（如果是协作项目）
git status        # 确认没有未保存的改动
```

### 场景 B：写完一个小功能后

```bash
git status                    # 查看改了哪些文件
git diff                      # 查看具体改了什么
git add .                     # 暂存所有修改
git commit -m "添加xxx功能"    # 提交
git push                      # 推送到 GitHub
```

### 场景 C：改坏了想回退

```bash
# 还没 commit → 直接丢弃所有修改
git restore .

# 已经 commit 但没 push → 撤销最近一次 commit（修改保留在工作区）
git reset --soft HEAD~1

# 已经 commit 且 push → 创建反向 commit
git revert HEAD
git push
```

### 场景 D：想忽略某些文件不提交

在项目根目录创建 `.gitignore` 文件：

```bash
# Python 项目 .gitignore 示例
__pycache__/
*.pyc
.venv/
.env
*.log
.idea/
.vscode/
dist/
build/
```

### 场景 E：查看某段代码是谁写的

```bash
git blame 文件名              # 逐行显示作者和提交时间
git blame 文件名 -L 10,20     # 只看第10-20行
```

---

## 10. 常见报错与解决

| 报错信息 | 原因 | 解决方法 |
|----------|------|---------|
| `fatal: not a git repository` | 当前目录不是 Git 仓库 | `git init` 初始化，或 `cd` 到正确的目录 |
| `fatal: remote origin already exists` | 已经关联过远程仓库 | `git remote set-url origin 新地址` 修改地址 |
| `error: failed to push` | 远程有新的提交你没拉取 | 先 `git pull`，解决冲突后再 `git push` |
| `fatal: refusing to merge unrelated histories` | 两个仓库没有共同历史 | `git pull --allow-unrelated-histories` |
| `Please enter a commit message` | 没写 commit message | 按 `i` 进入编辑模式，写完按 `Esc` → `:wq` 回车 |
| ` detached HEAD` | 切换到了某个历史版本而非分支 | `git checkout main` 回到主分支 |
| `Permission denied (publickey)` | SSH Key 没配置或过期 | 重新配置 SSH Key（见第 6.5 节） |
| `CONFLICT (content): Merge conflict` | 合并时有冲突 | 手动解决冲突文件，然后 add + commit（见第 7.3 节） |

---

## 11. 进阶方向

掌握上面的内容后，你已经可以应付 80% 的日常场景了。进阶方向包括：

| 主题 | 何时学 | 一句话说明 |
|------|--------|-----------|
| `git stash` | 切换分支时不想提交 | 暂存当前工作，切换回来再恢复 |
| `git rebase` | 想让提交历史更整洁 | 把多条 commit 合并、重排序 |
| `git tag` | 发布版本时 | 给某个 commit 打标签（如 v1.0.0） |
| `git cherry-pick` | 只需要某个 commit 的改动 | 把单个 commit "摘"过来 |
| GitHub Actions | 想自动化测试/部署 | 代码推送后自动运行测试、发布 |
| GitHub Pages | 想免费托管静态网站 | 把 HTML 页面发布成网站 |
| `.gitignore` 全局配置 | 每个项目都要用 | 系统级忽略文件（如 `.DS_Store`） |

---

## 附录：实用链接

- [Git 官方文档](https://git-scm.com/doc)
- [GitHub 官方文档](https://docs.github.com/)
- [GitHub Skills 互动教程](https://skills.github.com/)（免费，强烈推荐！）
- [Visualizing Git](https://git-school.github.io/visualizing-git/)（可视化理解 Git 操作）
- [Learn Git Branching](https://learngitbranching.js.org/)（游戏化学习分支操作）
- [Oh Shit, Git!?!](https://ohshitgit.com/)（常见翻车场景的急救方案，有中文版）

---

> **最后一条建议：不要试图一次性记住所有命令。** 打开终端，在真实的项目中用起来。遇到问题 → 查 → 解决 → 记住。反复几次，肌肉记忆就形成了。你的 `python-course`、`c-language-learning-system`、`learning-checkin-app` 都是很好的练习对象。
