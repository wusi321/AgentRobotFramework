# ARF 架构设计文档

## 1. 总体架构

ARF 采用分层架构，自上而下分为：

```
┌─────────────────────────────────┐
│      Hermes AI Agent Layer      │  ← AI 决策层
├─────────────────────────────────┤
│      Skill Runtime Layer        │  ← 技能调度层
├─────────────────────────────────┤
│      Robot API Layer            │  ← 硬件抽象层
├─────────────────────────────────┤
│      Protocol Layer             │  ← 协议处理层
├─────────────────────────────────┤
│      Transport Layer            │  ← 传输层
├─────────────────────────────────┤
│      STM32 Runtime              │  ← 实时控制层
└─────────────────────────────────┘
```

## 2. 核心设计原则

### 2.1 分层解耦

**原则**：上层不依赖下层具体实现，只依赖接口

**好处**：
- 模块可独立替换
- 易于测试
- 维护成本低

### 2.2 统一抽象

**原则**：同类设备统一 API

**示例**：
```python
# 不同电机统一接口
robot.motor.set_speed(id, speed)  # PWM/CAN/485 自动适配
```

### 2.3 配置驱动

**原则**：行为由配置决定，而非硬编码

**好处**：
- 无需修改代码
- 支持多机器人
- 热更新

### 2.4 事件驱动

**原则**：模块间通过事件通信

**好处**：
- 低耦合
- 易扩展
- 可追踪

## 3. 模块职责

### 3.1 Core 核心模块

| 模块 | 职责 |
|------|------|
| runtime.py | 系统生命周期管理 |
| scheduler.py | 任务调度 |
| event_bus.py | 事件总线 |
| state_manager.py | 状态机 |
| permission_manager.py | 权限控制 |
| config_loader.py | 配置加载 |
| logger.py | 日志管理 |

### 3.2 Protocol 协议层

| 模块 | 职责 |
|------|------|
| packet.py | 数据包结构 |
| command.py | 命令定义 |
| crc.py | CRC 校验 |
| stm32_protocol.py | 协议处理器 |

### 3.3 Transport 传输层

| 模块 | 职责 |
|------|------|
| base_transport.py | 传输基类 |
| uart_transport.py | UART 实现 |
| can_transport.py | CAN 实现 |
| usb_transport.py | USB 实现 |

### 3.4 Robot API 硬件抽象

| 模块 | 职责 |
|------|------|
| robot_api.py | 统一入口 |
| motor/motor.py | 电机控制 |
| servo/servo.py | 舵机控制 |
| sensor/sensor.py | 传感器读取 |

### 3.5 Runtime 运行时

| 模块 | 职责 |
|------|------|
| skill_runtime.py | 技能管理 |
| task_manager.py | 任务管理 |
| watchdog.py | 看门狗 |

## 4. 数据流

### 4.1 命令执行流程

```
AI Agent
    ↓ (决策)
Skill Runtime
    ↓ (调用)
Robot API
    ↓ (构造命令)
Protocol Layer
    ↓ (序列化)
Transport Layer
    ↓ (发送)
STM32
    ↓ (执行)
Hardware
```

### 4.2 数据上报流程

```
Hardware
    ↓ (采集)
STM32
    ↓ (处理)
Transport Layer
    ↓ (接收)
Protocol Layer
    ↓ (解析)
Robot API
    ↓ (发布事件)
Skill Runtime / AI Agent
```

## 5. 安全机制

### 5.1 权限控制

- AI 不能直接操作硬件
- 所有命令经过权限检查
- 参数自动限幅

### 5.2 看门狗

- 心跳超时自动停机
- 防止失控

### 5.3 紧急停止

- 最高优先级
- 硬件 + 软件双保险

### 5.4 状态机

- 状态转换规则限制
- 防止非法操作

## 6. 扩展机制

### 6.1 用户 Skill

- 继承 Skill 基类
- 放入 skills/ 目录
- 自动加载

### 6.2 用户设备

- 实现设备接口
- 注册到 Robot API
- 零修改核心

### 6.3 用户协议

- 继承 Protocol 基类
- 注册命令处理器
- 热插拔

## 7. 性能考虑

### 7.1 实时性

- 实时控制下放 STM32
- 上位机只做规划

### 7.2 并发

- 异步 I/O
- 多线程接收

### 7.3 资源

- 日志分级
- 配置缓存
- 连接池

## 8. 未来演进

### V0.3
- 多设备抽象
- Skill 热加载
- 配置热更新

### V0.5
- 多 STM32 支持
- CAN 总线
- IMU 闭环

### V1.0
- 插件生态
- 可视化控制台
- OTA 更新
