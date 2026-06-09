# Agent Robot Framework (ARF)

> ⚠️ **新用户必读**：请先阅读 [START_HERE.md](START_HERE.md) 和 [HOW_TO_RUN.md](HOW_TO_RUN.md)

基于 Hermes Agent + STM32 Runtime 的机器人通用框架

## 项目简介

ARF 是一个 AI Agent 驱动的机器人中间件框架，实现高层智能决策与实时运动控制分离，支持多协议兼容和用户自定义扩展。

## 核心特性

- ✅ AI 安全控制机器人（不直接操作硬件）
- ✅ 统一的 Robot API 抽象层
- ✅ 多协议支持（UART/CAN/USB/RS485）
- ✅ Skill 热插拔机制
- ✅ 用户自定义模块扩展
- ✅ 实时控制下放 STM32
- ✅ 配置驱动系统

## 架构概览

```
Hermes AI Agent (决策层)
    ↓
Skill Runtime (技能调度)
    ↓
Robot API Layer (统一抽象)
    ↓
Protocol Layer (协议解析)
    ↓
Transport Layer (通信传输)
    ↓
STM32 Runtime (实时控制)
    ↓
Hardware (电机/传感器/执行器)
```

## 快速开始

### 环境要求

- Ubuntu 22.04 ARM64
- Python 3.11+
- STM32 开发板
- Hermes Agent

### 安装

```bash
chmod +x push.sh
./push.sh
```

### 运行

```bash
# 方法1：使用启动脚本（推荐）
chmod +x run.sh
./run.sh

# 方法2：手动激活环境
source venv/bin/activate
python main.py
```

### 验证

```bash
python verify_installation.py
```

### 遇到问题？

查看 [故障排查指南](TROUBLESHOOTING.md)

## 版本路线

- **V0.1** - 最小可运行版本（当前）
- **V0.3** - 通用机器人框架化
- **V0.5** - 实时控制增强
- **V1.0** - 正式版

## Git 管理

### 快速提交代码

```bash
./git.sh
```

### 高级 Git 管理

```bash
./git_advanced.sh
```

详见 [GIT_GUIDE.md](GIT_GUIDE.md)

## 项目结构

详见 [框架art.md](框架art.md)

## 开发文档

- [配置说明](docs/config.md)
- [Skill 开发指南](docs/skill_dev.md)
- [协议规范](docs/protocol.md)
- [STM32 开发指南](docs/stm32_dev.md)

## License

MIT
