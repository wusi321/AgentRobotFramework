# ARF 快速参考手册

> 常用命令和操作的快速查询表

---

## 🚀 快速启动

```bash
# 一键启动
./run.sh

# 验证安装
./venv/bin/python verify_installation.py

# 测试环境
./venv/bin/python test_env.py
```

---

## 📦 安装和环境

```bash
# 安装
./push.sh

# 激活虚拟环境
source venv/bin/activate

# 退出虚拟环境
deactivate

# 重新安装依赖
pip install -r requirements.txt
```

---

## 🔧 Git 操作

```bash
# 快速提交（推荐）
./git.sh

# 高级管理
./git_advanced.sh

# 手动提交
git add .
git commit -m "提交信息"
git push origin master

# 查看状态
git status

# 查看历史
git log --oneline -10
```

---

## 🤖 运行程序

```bash
# 方式1：启动脚本
./run.sh

# 方式2：手动激活
source venv/bin/activate
python main.py

# 方式3：直接运行
./venv/bin/python main.py

# 运行示例
./venv/bin/python examples/basic_usage.py
```

---

## 🧪 测试

```bash
# 单元测试
./venv/bin/python tests/test_protocol.py -v

# 验证安装
./venv/bin/python verify_installation.py

# 测试环境
./venv/bin/python test_env.py
```

---

## ⚙️ 配置文件

| 文件 | 用途 |
|------|------|
| `config/robot.yaml` | 机器人总体配置 |
| `config/hardware.yaml` | 硬件设备定义 |
| `config/stm32_config.yaml` | STM32 连接配置 |
| `config/protocol.yaml` | 协议参数 |
| `config/permission.yaml` | 权限控制 |

---

## 🔍 查看日志

```bash
# 实时查看
tail -f logs/arf_*.log

# 查看错误日志
cat logs/arf_error_*.log

# 清理日志
rm logs/*.log
```

---

## 🐛 故障排查

```bash
# 检查串口
ls /dev/tty*

# 测试串口
sudo chmod 666 /dev/ttyACM0

# 添加串口权限
sudo usermod -a -G dialout $USER

# 测试 GitHub SSH
ssh -T git@github.com

# 查看 Python 路径
which python

# 检查虚拟环境
python -c "import sys; print(sys.prefix)"
```

---

## 📚 Robot API 快速参考

### 电机控制

```python
from core.runtime import Runtime

runtime = Runtime()
runtime.start()

# 设置速度
runtime.robot_api.motor.set_speed(1, 0.5)

# 设置位置
runtime.robot_api.motor.set_position(1, 90.0)

# 停止电机
runtime.robot_api.motor.stop(1)

# 获取状态
status = runtime.robot_api.motor.get_status(1)

runtime.stop()
```

### 执行 Skill

```python
# 执行 walk 技能
result = runtime.execute_skill(
    "walk",
    speed=0.5,
    direction="forward",
    duration=3.0
)

# 停止 Skill
runtime.skill_runtime.stop_skill("walk")

# 列出所有 Skill
skills = runtime.list_skills()
```

### 事件订阅

```python
from core.event_bus import event_bus

# 订阅事件
def on_state_changed(data):
    print(f"状态变更: {data}")

event_bus.subscribe("state/changed", on_state_changed)

# 发布事件
event_bus.emit("custom/event", {"key": "value"})
```

### 状态管理

```python
from core.state_manager import state_manager, RobotState

# 获取当前状态
current = state_manager.get_state()

# 状态转换
state_manager.transition(RobotState.MOVING)

# 检查状态
if state_manager.is_state(RobotState.IDLE):
    print("机器人空闲")

# 紧急停止
state_manager.emergency_stop()
```

---

## 🎯 常用路径

```bash
# 项目根目录
~/arf/

# 配置目录
~/arf/config/

# 日志目录
~/arf/logs/

# Skill 目录
~/arf/skills/

# 文档目录
~/arf/docs/
```

---

## 📖 文档速查

| 文档 | 内容 |
|------|------|
| [START_HERE.md](START_HERE.md) | 新手入门 ⭐ |
| [HOW_TO_RUN.md](HOW_TO_RUN.md) | 运行说明 ⭐ |
| [QUICK_START.md](QUICK_START.md) | 快速开始 |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | 故障排查 |
| [GIT_GUIDE.md](GIT_GUIDE.md) | Git 使用 |
| [docs/architecture.md](docs/architecture.md) | 架构设计 |
| [框架art.md](框架art.md) | 完整文档 |

---

## 🔗 有用链接

- **GitHub**: https://github.com/wusi321/AgentRobotFramework
- **Issues**: https://github.com/wusi321/AgentRobotFramework/issues
- **Python**: https://www.python.org/
- **Git**: https://git-scm.com/

---

## 💡 快捷键（git_advanced.sh）

| 按键 | 功能 |
|------|------|
| 1 | 快速提交 |
| 2 | 查看状态 |
| 3 | 查看历史 |
| 4 | 查看差异 |
| 5 | 拉取更新 |
| 6 | 推送代码 |
| 0 | 退出 |

---

## ⚠️ 重要提示

1. **必须使用虚拟环境** - `source venv/bin/activate`
2. **串口权限** - `sudo usermod -a -G dialout $USER`
3. **Git 提交前检查** - `git status`
4. **定期备份** - 推送到 GitHub
5. **查看日志** - 出问题先看日志

---

## 🎉 一行命令速查

```bash
# 完整流程
./push.sh && ./run.sh

# 测试完整性
./venv/bin/python verify_installation.py && ./venv/bin/python test_env.py

# 快速提交
./git.sh

# 查看所有文档
ls *.md docs/*.md
```

---

**打印此页以便快速查询** 📄
