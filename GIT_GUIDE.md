# Git 脚本使用指南

ARF 提供了两个 Git 管理脚本，方便快速提交和管理代码。

---

## 📋 脚本列表

### 1. git.sh - 快速提交脚本 ⭐ 推荐日常使用

**用途**：自动检测变更、添加、提交并推送

**特点**：
- ✅ 自动检测文件变更
- ✅ 智能提示和确认
- ✅ 支持自定义提交信息
- ✅ 一键推送到 GitHub
- ✅ 彩色输出，直观清晰

### 2. git_advanced.sh - 高级管理工具

**用途**：提供完整的 Git 操作菜单

**功能**：
- 快速提交并推送
- 查看状态和历史
- 创建和切换分支
- 撤销提交
- 放弃修改
- 等等...

---

## 🚀 使用方法

### 快速提交（git.sh）

```bash
# 运行脚本
./git.sh
```

**执行流程**：

1. **检查状态** - 显示所有变更文件
2. **确认提交** - 询问是否继续
3. **添加文件** - 自动 `git add .`
4. **输入信息** - 输入提交信息（可留空使用默认）
5. **提交代码** - 执行 `git commit`
6. **推送远程** - 自动推送到 GitHub

**示例输出**：

```
=========================================
  ARF Git Auto Commit Script
=========================================

[1/6] 检查 Git 状态...
位于分支 master
您的分支与上游分支 'origin/master' 一致。

[2/6] 检测到以下变更:
 M config/robot.yaml
 M core/logger.py
?? new_file.py

是否继续提交这些变更?
(y/n) y

[3/6] 添加文件到暂存区...
✅ 文件已添加

[4/6] 输入提交信息
提示: 按 Enter 使用默认提交信息
默认信息: Update project files - 2024-06-09 16:20:00
提交信息: 修复日志系统bug

[5/6] 提交变更...
✅ 提交成功

[6/6] 推送到远程仓库...
=========================================
  ✅ 所有操作完成!
=========================================
提交信息: 修复日志系统bug
分支: master
GitHub: https://github.com/wusi321/AgentRobotFramework
```

---

### 高级管理（git_advanced.sh）

```bash
# 运行脚本
./git_advanced.sh
```

**菜单选项**：

```
=========================================
  ARF Git 管理工具
=========================================

1. 快速提交并推送 (add + commit + push)
2. 查看状态 (git status)
3. 查看提交历史 (git log)
4. 查看变更差异 (git diff)
5. 拉取远程更新 (git pull)
6. 推送到远程 (git push)
7. 创建新分支
8. 切换分支
9. 撤销最后一次提交
10. 放弃工作区修改
0. 退出
=========================================
请选择操作 [0-10]:
```

---

## 💡 使用场景

### 场景 1：修改了代码，想快速提交

```bash
# 使用 git.sh（推荐）
./git.sh

# 输入提交信息，比如：
# 提交信息: 添加传感器模块
```

### 场景 2：查看当前状态

```bash
# 使用 git_advanced.sh
./git_advanced.sh

# 选择：2（查看状态）
```

### 场景 3：查看最近的提交历史

```bash
./git_advanced.sh

# 选择：3（查看提交历史）
```

### 场景 4：创建开发分支

```bash
./git_advanced.sh

# 选择：7（创建新分支）
# 输入分支名：dev
```

### 场景 5：撤销错误的提交

```bash
./git_advanced.sh

# 选择：9（撤销最后一次提交）
```

---

## 🎯 最佳实践

### 提交信息规范

建议使用清晰的提交信息：

```
✅ 好的提交信息：
- 添加电机控制模块
- 修复串口通信bug
- 更新文档：添加安装说明
- 优化性能：减少日志输出

❌ 不好的提交信息：
- 修改
- update
- fix bug
- 111
```

### 提交频率

建议：
- ✅ 完成一个功能后立即提交
- ✅ 修复一个bug后提交
- ✅ 每天工作结束前提交
- ❌ 不要积累太多修改一次提交

### 分支管理

建议：
- `master` - 稳定版本
- `dev` - 开发版本
- `feature-xxx` - 新功能分支
- `bugfix-xxx` - Bug修复分支

---

## 📝 常用命令对照

| 操作 | git.sh | git_advanced.sh | 原生命令 |
|------|--------|----------------|---------|
| 快速提交 | `./git.sh` | 选项 1 | `git add . && git commit -m "xxx" && git push` |
| 查看状态 | - | 选项 2 | `git status` |
| 查看历史 | - | 选项 3 | `git log` |
| 创建分支 | - | 选项 7 | `git checkout -b xxx` |
| 撤销提交 | - | 选项 9 | `git reset --soft HEAD~1` |

---

## ⚠️ 注意事项

### 1. 使用前确保

- ✅ 在项目根目录（~/arf）
- ✅ Git 仓库已初始化
- ✅ 远程仓库已配置
- ✅ 有推送权限

### 2. 危险操作

以下操作**不可逆**，使用前请确认：

- ❌ 放弃工作区修改（选项 10）
- ❌ 强制推送（原生命令 `git push -f`）

### 3. 推送失败

如果推送失败，检查：

1. **网络连接**
   ```bash
   ping github.com
   ```

2. **SSH 密钥**
   ```bash
   ssh -T git@github.com
   ```

3. **远程仓库**
   ```bash
   git remote -v
   ```

---

## 🔧 故障排查

### 问题 1：权限错误

```bash
bash: ./git.sh: Permission denied
```

**解决**：
```bash
chmod +x git.sh git_advanced.sh
```

### 问题 2：推送被拒绝

```bash
error: failed to push some refs to 'github.com:wusi321/AgentRobotFramework.git'
```

**解决**：
```bash
# 先拉取远程更新
git pull origin master

# 再推送
./git.sh
```

### 问题 3：SSH 连接失败

```bash
Connection closed by 20.205.243.166 port 22
```

**解决**：
```bash
# 改用 HTTPS
git remote set-url origin https://github.com/wusi321/AgentRobotFramework.git
```

---

## 📚 扩展阅读

- [Git 官方文档](https://git-scm.com/doc)
- [GitHub 帮助](https://docs.github.com)
- [Git 常用命令](https://www.runoob.com/git/git-basic-operations.html)

---

## 🎉 快速开始

```bash
# 1. 修改代码
vim core/logger.py

# 2. 快速提交
./git.sh

# 3. 查看 GitHub
# https://github.com/wusi321/AgentRobotFramework
```

就这么简单！✨

---

**最后更新**：2024-06-09
