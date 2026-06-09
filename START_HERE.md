# 🚀 从这里开始

## 欢迎使用 ARF (Agent Robot Framework)！

这是一个 AI Agent 驱动的机器人中间件框架。

---

## 📋 快速开始（3 步）

### 1️⃣ 安装（1 分钟）

```bash
chmod +x push.sh
./push.sh
```

### 2️⃣ 验证（30 秒）

```bash
./venv/bin/python verify_installation.py
```

### 3️⃣ 运行（10 秒）

```bash
chmod +x run.sh
./run.sh
```

✅ 看到 "ARF Runtime Started Successfully!" 就成功了！

---

## ⚠️ 重要提示

### 必须使用虚拟环境运行

❌ **错误**：
```bash
python3 main.py  # 会报错！
```

✅ **正确**：
```bash
./run.sh  # 推荐
# 或
source venv/bin/activate
python main.py
```

详见：[HOW_TO_RUN.md](HOW_TO_RUN.md)

---

## 📚 文档导航

### 新手必读
1. **[HOW_TO_RUN.md](HOW_TO_RUN.md)** - 如何运行（必读！）
2. **[QUICK_START.md](QUICK_START.md)** - 5分钟快速开始
3. **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - 故障排查

### 深入学习
4. **[README.md](README.md)** - 项目说明
5. **[docs/architecture.md](docs/architecture.md)** - 架构设计
6. **[docs/quick_start.md](docs/quick_start.md)** - 详细教程

### 开发参考
7. **[框架art.md](框架art.md)** - 完整设计文档
8. **[PROJECT_STATUS.md](PROJECT_STATUS.md)** - 项目状态
9. **[TODO.md](TODO.md)** - 开发计划
10. **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - 实现总结

---

## 🎯 核心概念

### 架构分层

```
AI Agent (Hermes)     ← 决策层
    ↓
Skill Runtime         ← 技能调度
    ↓
Robot API            ← 硬件抽象（你主要用这个）
    ↓
Protocol Layer       ← 协议处理
    ↓
Transport (UART)     ← 通信传输
    ↓
STM32 Runtime        ← 实时控制
```

### 设计理念

1. **AI 不直接控制硬件** - 保证安全
2. **统一 Robot API** - 屏蔽底层差异
3. **配置驱动** - 无需改代码
4. **事件解耦** - 模块独立
5. **权限沙箱** - 防止误操作

---

## 💡 使用示例

### 控制电机

```python
from core.runtime import Runtime

runtime = Runtime()
runtime.start()

# 设置电机速度
runtime.robot_api.motor.set_speed(1, 0.5)

# 停止电机
runtime.robot_api.motor.stop(1)

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
```

更多示例：`examples/basic_usage.py`

---

## 🛠️ 常用命令

```bash
# 安装
./push.sh

# 验证
./venv/bin/python verify_installation.py

# 运行
./run.sh

# 测试环境
./venv/bin/python test_env.py

# 运行示例
source venv/bin/activate
python examples/basic_usage.py

# 查看日志
tail -f logs/arf_*.log
```

---

## 🔧 配置 STM32

### 1. 连接 STM32

USB 连接到电脑

### 2. 查找串口

```bash
ls /dev/ttyACM*
# 或
ls /dev/ttyUSB*
```

### 3. 修改配置

编辑 `config/stm32_config.yaml`:

```yaml
transport:
  device: /dev/ttyACM0  # 改成你的串口
  baudrate: 115200
```

### 4. 权限设置

```bash
sudo usermod -a -G dialout $USER
# 重新登录后生效
```

---

## 🐛 遇到问题？

### 1. 查看错误信息

```bash
cat logs/arf_error_*.log
```

### 2. 运行诊断

```bash
./venv/bin/python verify_installation.py
```

### 3. 查看故障排查

[TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### 4. 测试环境

```bash
./venv/bin/python test_env.py
```

---

## 📂 项目结构

```
ARF/
├── core/              # 核心模块
├── protocol/          # 协议层
├── transport/         # 传输层
├── robot/             # Robot API
├── runtime/           # 运行时
├── skills/            # 技能库
├── config/            # 配置文件
├── docs/              # 文档
├── examples/          # 示例代码
├── stm32_example/     # STM32 示例
├── tests/             # 测试
├── main.py            # 主程序
├── run.sh             # 启动脚本 ⭐
└── push.sh            # 安装脚本
```

---

## 🎓 学习路线

### 第1天：环境搭建
- [ ] 运行 `./push.sh` 安装
- [ ] 运行 `./run.sh` 验证
- [ ] 阅读 [HOW_TO_RUN.md](HOW_TO_RUN.md)

### 第2天：理解架构
- [ ] 阅读 [README.md](README.md)
- [ ] 阅读 [docs/architecture.md](docs/architecture.md)
- [ ] 运行 `examples/basic_usage.py`

### 第3天：配置硬件
- [ ] 连接 STM32
- [ ] 配置串口
- [ ] 测试通信

### 第4天：开发 Skill
- [ ] 学习 `skills/walk/` 示例
- [ ] 创建自己的 Skill
- [ ] 测试执行

### 第5天：扩展功能
- [ ] 添加新设备
- [ ] 修改配置
- [ ] 集成到项目

---

## ✨ 核心特性

- ✅ **分层架构** - 清晰的职责划分
- ✅ **统一 API** - 屏蔽底层差异
- ✅ **配置驱动** - 灵活可配置
- ✅ **事件驱动** - 模块解耦
- ✅ **权限控制** - AI 安全沙箱
- ✅ **扩展友好** - 用户可自定义

---

## 🤝 贡献

欢迎贡献代码和文档！

查看 [TODO.md](TODO.md) 了解开发计划。

---

## 📞 获取帮助

1. 查看 [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. 查看 [docs/](docs/) 目录
3. 运行 `verify_installation.py`
4. 提交 GitHub Issue

---

## 🎉 开始你的机器人项目

现在你已经了解了基础，可以开始使用 ARF 开发你的机器人项目了！

```bash
./run.sh
```

祝你开发愉快！🚀

---

**ARF Team**
