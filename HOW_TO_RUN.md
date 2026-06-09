# 如何运行 ARF

## 重要提示 ⚠️

ARF 使用 Python 虚拟环境管理依赖。你**必须**先激活虚拟环境才能运行程序。

---

## 正确的运行方式

### 方式 1：使用启动脚本（最简单）

```bash
chmod +x run.sh
./run.sh
```

这个脚本会自动激活虚拟环境并运行程序。

---

### 方式 2：手动激活虚拟环境

```bash
# 1. 激活虚拟环境
source venv/bin/activate

# 2. 运行程序
python main.py

# 3. 退出虚拟环境（可选）
deactivate
```

**提示**：激活后，命令行提示符前会出现 `(venv)`

```bash
(venv) lcf@lcf:~/arf$ python main.py
```

---

### 方式 3：直接使用虚拟环境的 Python

```bash
./venv/bin/python main.py
```

不需要激活虚拟环境，直接使用虚拟环境里的 Python 解释器。

---

## ❌ 错误的运行方式

### 不要直接运行 `python3 main.py`

```bash
# ❌ 错误！
python3 main.py

# 会报错：
# ModuleNotFoundError: No module named 'loguru'
```

**原因**：`python3` 使用的是系统 Python，不是虚拟环境中的 Python。

---

## 如何判断是否在虚拟环境中？

### 方法 1：查看提示符

激活虚拟环境后，提示符会变成：

```bash
(venv) lcf@lcf:~/arf$
```

### 方法 2：检查 Python 路径

```bash
which python

# 在虚拟环境中：
# /home/lcf/arf/venv/bin/python

# 不在虚拟环境中：
# /usr/bin/python3
```

### 方法 3：测试导入

```bash
python -c "import loguru; print('在虚拟环境中')"

# 在虚拟环境中：会打印 "在虚拟环境中"
# 不在虚拟环境中：会报错 ModuleNotFoundError
```

---

## 完整运行流程

### 第一次运行

```bash
# 1. 进入项目目录
cd ~/arf

# 2. 运行安装脚本（只需一次）
chmod +x push.sh
./push.sh

# 3. 运行程序
chmod +x run.sh
./run.sh
```

### 以后运行

```bash
# 进入项目目录
cd ~/arf

# 直接运行
./run.sh
```

---

## 其他命令

### 验证安装

```bash
./venv/bin/python verify_installation.py
```

### 测试环境

```bash
./venv/bin/python test_env.py
```

### 运行示例

```bash
source venv/bin/activate
python examples/basic_usage.py
```

### 运行测试

```bash
source venv/bin/activate
python tests/test_protocol.py -v
```

---

## 常见问题

### Q: 为什么要用虚拟环境？

A: 虚拟环境可以：
- 隔离项目依赖
- 避免污染系统 Python
- 不同项目使用不同版本的库
- 更容易部署和迁移

### Q: 每次都要激活虚拟环境吗？

A: 有两种选择：
1. 使用 `./run.sh`（自动激活）
2. 手动激活一次，然后可以运行多个命令

```bash
source venv/bin/activate
python main.py
python examples/basic_usage.py
python tests/test_protocol.py
```

### Q: 忘记激活虚拟环境怎么办？

A: 程序会提示你：

```
⚠️  警告：未在虚拟环境中运行
请先激活虚拟环境：
  source venv/bin/activate
```

### Q: 虚拟环境被删除了怎么办？

A: 重新运行安装脚本：

```bash
./push.sh
```

---

## 开发建议

如果你要开发 ARF，建议：

1. **使用 IDE**：配置 Python 解释器为 `venv/bin/python`
2. **终端工作**：在项目终端中运行 `source venv/bin/activate`
3. **使用 tmux/screen**：保持虚拟环境激活状态

### VSCode 配置

创建 `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python"
}
```

### PyCharm 配置

1. File → Settings → Project → Python Interpreter
2. 选择 `venv/bin/python`

---

## 总结

✅ **推荐方式**：
```bash
./run.sh
```

✅ **手动方式**：
```bash
source venv/bin/activate
python main.py
```

❌ **错误方式**：
```bash
python3 main.py  # 不要这样！
```

---

**记住**：所有 ARF 命令都需要在虚拟环境中运行！🎯
