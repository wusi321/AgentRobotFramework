# Agent Robot Framework（ARF）

> 基于 Hermes Agent + STM32 Runtime 的机器人通用框架
> 面向具身智能、机器人控制、四足机器人、机械臂、移动平台等场景。
> 目标是构建一个 **AI 可理解、可扩展、协议统一、实时安全、支持用户自定义模块** 的机器人 Agent 框架。

---

# 1. 项目目标

## 1.1 项目定位

ARF（Agent Robot Framework）是一个：

> **AI Agent 驱动的机器人中间件框架**

其核心目标是：

```txt
让 AI 能够安全、稳定、可扩展地控制机器人
```

但：

```txt
AI 不直接控制实时硬件
```

而是：

```txt
AI → Skill → Robot API → Protocol → STM32 → Hardware
```

实现：

* 高层智能决策
* 实时运动控制分离
* 多协议兼容
* Skill 热插拔
* 用户自定义设备
* 私有协议扩展

---

## 1.2 为什么不直接让 AI 控制硬件

错误方式：

```txt
AI
 ↓
串口
 ↓
PWM
```

问题：

### 1. 时延不可控

LLM 推理时间：

```txt
200ms ~ 数秒
```

机器人控制周期：

```txt
1ms ~ 10ms
```

例如四足机器人：

```txt
500Hz ~ 1000Hz
```

AI 无法完成实时控制。

---

### 2. 安全性低

AI 可能：

```txt
误判
循环输出
非法参数
协议错误
```

可能导致：

```txt
电机堵转
摔倒
烧毁舵机
碰撞
```

---

### 3. Skill 难以维护

如果：

```python
skill直接 serial.write()
```

则：

换协议：

```txt
PWM → CAN
```

所有 Skill 全部重写。

维护成本极高。

---

## 1.3 核心设计原则

### 原则1：分层设计

高层：

```txt
AI 决策
```

中层：

```txt
行为控制
```

底层：

```txt
实时控制
```

---

### 原则2：统一抽象

所有设备：

```txt
统一 API
```

例如：

不同电机：

```txt
PWM
CAN
485
```

统一：

```python
robot.motor.move()
```

---

### 原则3：协议透明

Skill：

```txt
不知道底层协议
```

只调用：

```python
robot.servo.move()
```

---

### 原则4：用户扩展优先

用户可：

* 写 Skill
* 写协议
* 写电机驱动
* 写传感器
* 写私有模块

无需修改框架核心。

---

### 原则5：实时控制下放

STM32：

负责：

```txt
PID
PWM
FOC
IMU闭环
步态
```

上位机：

负责：

```txt
规划
视觉
AI决策
路径
```

---

# 2. 系统总体架构

## 2.1 架构图

```txt
┌──────────────────────────┐
│      Hermes AI Agent     │
│      大模型决策层         │
└──────────────────────────┘
              │
              ▼
┌──────────────────────────┐
│       Skill Runtime       │
│ 技能调度/任务生命周期管理  │
└──────────────────────────┘
              │
              ▼
┌──────────────────────────┐
│      Robot API Layer      │
│     硬件统一抽象接口       │
└──────────────────────────┘
              │
              ▼
┌──────────────────────────┐
│      Protocol Layer       │
│     命令协议/数据解析      │
└──────────────────────────┘
              │
              ▼
┌──────────────────────────┐
│      Transport Layer      │
│ UART/CAN/USB/RS485       │
└──────────────────────────┘
              │
              ▼
┌──────────────────────────┐
│      STM32 Runtime        │
│ 实时控制/驱动/状态管理     │
└──────────────────────────┘
              │
      ┌───────┼────────┐
      ▼       ▼        ▼
   电机      传感器     执行器
```

---

## 2.2 各层职责

### Layer1：AI Agent

负责：

```txt
自然语言理解
任务规划
行为决策
Skill 调度
```

例如：

用户：

```txt
去桌子旁边
```

AI：

拆解：

```txt
定位桌子
规划路径
开始移动
避障
停止
```

但：

不负责：

```txt
PWM
PID
CAN帧
```

---

### Layer2：Skill Runtime

负责：

```txt
技能生命周期
调度
任务执行
上下文
权限
```

例如：

```txt
walk skill
vision follow skill
pick object skill
```

---

### Layer3：Robot API

核心层。

作用：

```txt
统一机器人能力
```

例如：

Skill：

```python
robot.motor.move()
```

无需关心：

```txt
PWM
CAN
RS485
```

Robot API 自动处理。

---

### Layer4：Protocol Layer

负责：

```txt
命令序列化
协议解析
CRC
数据包管理
```

统一协议。

屏蔽：

```txt
串口差异
CAN差异
```

---

### Layer5：Transport Layer

负责：

```txt
怎么发送
```

支持：

```txt
UART
USB CDC
CAN
RS485
```

只负责：

```txt
send()
receive()
```

不关心数据内容。

---

### Layer6：STM32 Runtime

负责：

```txt
实时控制
设备管理
任务调度
```

包括：

```txt
PWM
FOC# 3. 项目目录结构设计

本框架采用：

```txt
强分层 + 强模块化 + 可插拔
```

原则：

```txt
任何模块都可以单独替换
```

例如：

```txt
UART → CAN
PWM → CAN Motor
Hermes → 其他 Agent
```

不影响整体系统。

---

# 3.1 上位机目录结构（Ubuntu22.04 ARM64）

目录：

```txt
agent_os/
│
├── main.py
├── push.sh
├── requirements.txt
├── autoskill.md
│
├── core/
│   ├── runtime.py
│   ├── scheduler.py
│   ├── context_manager.py
│   ├── event_bus.py
│   ├── permission_manager.py
│   ├── config_loader.py
│   ├── state_manager.py
│   └── logger.py
│
├── robot/
│   ├── robot_api.py
│   │
│   ├── motor/
│   │   ├── motor.py
│   │   ├── pwm_motor.py
│   │   ├── can_motor.py
│   │   └── user_motor.py
│   │
│   ├── servo/
│   │   ├── servo.py
│   │   └── user_servo.py
│   │
│   ├── sensor/
│   │   ├── imu.py
│   │   ├── camera.py
│   │   ├── lidar.py
│   │   ├── ultrasonic.py
│   │   └── user_sensor.py
│   │
│   ├── navigation/
│   │   ├── goto.py
│   │   ├── obstacle.py
│   │   └── planner.py
│   │
│   └── system/
│       ├── power.py
│       ├── state.py
│       └── health.py
│
├── transport/
│   ├── base_transport.py
│   ├── uart_transport.py
│   ├── usb_transport.py
│   ├── can_transport.py
│   └── rs485_transport.py
│
├── protocol/
│   ├── base_protocol.py
│   ├── stm32_protocol.py
│   ├── packet.py
│   ├── parser.py
│   ├── crc.py
│   └── serializer.py
│
├── runtime/
│   ├── skill_runtime.py
│   ├── task_manager.py
│   └── watchdog.py
│
├── skills/
│   ├── walk/
│   │   ├── skill.py
│   │   ├── skill.yaml
│   │   └── README.md
│   │
│   ├── vision_follow/
│   ├── grasp/
│   └── user_skill/
│
├── plugin/
│   ├── user_plugin.py
│   └── extension_loader.py
│
├── config/
│   ├── robot.yaml
│   ├── stm32_config.yaml
│   ├── protocol.yaml
│   ├── hardware.yaml
│   ├── user_config.yaml
│   └── permission.yaml
│
├── logs/
│
└── cache/
```

---

# 3.2 核心目录职责

---

## main.py

系统入口。

负责：

```txt
初始化
加载配置
启动 runtime
连接 STM32
注册 skill
启动 Hermes
```

示例：

```python
from core.runtime import Runtime

def main():
    runtime = Runtime()
    runtime.start()

if __name__ == "__main__":
    main()
```

---

## push.sh

一键部署。

负责：

```txt
安装依赖
配置环境变量
自动发现串口
注册 Hermes skill
创建虚拟环境
```

例如：

```bash
#!/bin/bash

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

export ROBOT_CONFIG=config/robot.yaml
export STM32_CONFIG=config/stm32_config.yaml
```

---

## autoskill.md

这是：

> AI 的能力文档

Hermes：

读取：

```txt
autoskill.md
```

理解：

机器人有哪些能力。

例如：

```md
# robot skills

## walk

Description:
Move robot

Input:
speed(float)
direction(string)

Example:
walk speed=0.5
```

Hermes 自动学习。

而不是：

```txt
prompt硬编码
```

避免：

```txt
prompt 地狱
```

---

# 3.3 Core 核心模块

---

## runtime.py

系统运行核心。

负责：

```txt
生命周期管理
系统启动
系统停止
模块初始化
```

类似：

```txt
kernel
```

---

## scheduler.py

任务调度器。

负责：

```txt
skill 调度
优先级管理
任务抢占
```

例如：

正常：

```txt
walk
```

突然：

```txt
fall detected
```

立即：

```txt
stop motor
```

优先级更高。

建议：

```txt
priority queue
```

---

## event_bus.py

极其重要。

这是：

> 解耦核心

禁止：

```txt
模块互相直接调用
```

改为：

事件机制。

例如：

传感器：

发布：

```python
event.emit(
    "imu/update",
    imu_data
)
```

行为模块：

订阅：

```python
event.subscribe(
    "imu/update"
)
```

实现：

```txt
模块低耦合
```

未来维护舒服很多。

---

## permission_manager.py

AI 权限控制。

例如：

禁止：

```txt
连续高速输出
超限角度
危险动作
```

例如：

```python
if speed > max_speed:
    deny()
```

防止：

```txt
AI 发疯
```

---

## state_manager.py

机器人状态机。

例如：

状态：

```txt
idle
moving
walking
charging
error
shutdown
```

避免：

```txt
混乱控制
```

---

# 3.4 Robot API 设计（重点）

这是整个项目核心。

Skill：

绝对禁止：

```python
serial.write()
```

正确方式：

```python
robot.motor.move()
```

统一抽象。

---

## robot_api.py

统一入口：

```python
robot.motor
robot.sensor
robot.navigation
robot.system
```

示例：

```python
robot.motor.move(
    id=1,
    speed=0.5
)
```

---

## 电机抽象

统一：

```python
set_speed()

stop()

set_position()

set_torque()
```

底层：

自动判断：

```txt
PWM
CAN
485
```

---

## 传感器抽象

统一：

```python
read()

start_stream()

stop_stream()
```

例如：

```python
imu = robot.sensor.imu.read()
```

不关心：

```txt
串口
I2C
SPI
```

---

# 4. 私有协议设计（核心）

不要：

```txt
AA BB 01 02
```

以后一定崩。

必须：

> 可扩展协议

---

## 4.1 数据包结构

统一：

```c
typedef struct
{
    uint16_t head;
    uint8_t version;

    uint8_t device_id;

    uint16_t command_id;

    uint16_t sequence_id;

    uint32_t timestamp;

    uint16_t payload_length;

    uint8_t payload[256];

    uint16_t crc;

}packet_t;
```

---

## 4.2 字段说明

### head

帧头：

```txt
0xAA55
```

用于同步。

---

### version

协议版本。

未来升级：

```txt
v1 → v2
```

兼容。

---

### device_id

设备编号。

例如：

```txt
1 电机板
2 imu板
3 机械臂
```

支持：

```txt
多 STM32
```

---

### command_id

命令类型。

例如：

```txt
0x0001 move_motor
0x0002 stop_motor
0x0003 read_sensor
```

---

### sequence_id

事务号。

防：

```txt
重复包
乱序包
```

非常重要。

---

### timestamp

时间戳。

用于：

```txt
同步
调试
滤波
```

---

### payload

负载。

例如：

电机：

```txt
id speed angle
```

---

### crc

校验。

建议：

```txt
CRC16
```

提高可靠性。

PID
传感器采集
IMU
步态
```
# 4.3 协议命令规范

协议必须：

```txt
统一命令空间
```

否则后期：

```txt
command id 混乱
```

最终不可维护。

建议：

采用：

```txt
模块化命令空间
```

格式：

```txt
0xAABB
```

规则：

```txt
AA = 模块
BB = 命令
```

例如：

| 模块          |     范围 |
| ----------- | -----: |
| Motor       | 0x01xx |
| Servo       | 0x02xx |
| Sensor      | 0x03xx |
| Navigation  | 0x04xx |
| System      | 0x05xx |
| User Define | 0xF0xx |

---

### Motor 命令

| 命令           |     ID |
| ------------ | -----: |
| set speed    | 0x0101 |
| set position | 0x0102 |
| stop         | 0x0103 |
| torque       | 0x0104 |
| status       | 0x0105 |

---

### Servo

| 命令      |     ID |
| ------- | -----: |
| move    | 0x0201 |
| enable  | 0x0202 |
| disable | 0x0203 |
| status  | 0x0204 |

---

### Sensor

| 命令           |     ID |
| ------------ | -----: |
| read         | 0x0301 |
| start stream | 0x0302 |
| stop stream  | 0x0303 |

---

### System

| 命令             |     ID |
| -------------- | -----: |
| heartbeat      | 0x0501 |
| watchdog       | 0x0502 |
| emergency stop | 0x0503 |
| system state   | 0x0504 |

---

### 用户扩展

预留：

```txt
0xF0xx
```

例如：

```txt
0xF001
```

用户自定义机械臂。

避免：

```txt
修改核心框架
```

---

# 4.4 Payload 数据规范

必须：

```txt
TLV结构
```

不要写死。

推荐：

```txt
Type Length Value
```

例如：

电机：

```txt
Type: motor_id
Length: 1
Value: 2
```

速度：

```txt
Type: speed
Length: 4
Value: float32
```

最终：

```txt
motor_id
speed
direction
torque
```

可扩展。

不会：

```txt
协议崩溃
```

---

# 4.5 ACK机制（必须）

所有控制命令：

必须：

```txt
请求 → ACK
```

例如：

上位机：

```txt
move motor
```

STM32：

返回：

```txt
success
```

格式：

```txt
ack_type
status
sequence_id
error_code
```

状态：

```txt
0 成功
1 参数错误
2 超时
3 执行失败
4 未注册设备
```

否则：

AI 根本不知道：

```txt
命令有没有执行
```

---

# 4.6 心跳机制（必须）

避免：

```txt
串口断连
STM32死机
```

心跳：

```txt
500ms
```

发送：

```txt
heartbeat
```

连续：

```txt
>3次失败
```

进入：

```txt
safe mode
```

执行：

```txt
motor stop
```

防炸机。

---

# 4.7 紧急停止（必须硬件级）

定义：

```txt
0x0503
```

任何时刻：

最高优先级。

收到：

立即：

```txt
disable pwm
motor stop
```

不能：

```txt
排队等待
```

否则会摔。

建议：

加：

```txt
硬件急停按键
```

直连 STM32。

---

# 5. Robot API 标准

这是：

> 整个系统的灵魂

作用：

```txt
统一硬件能力
```

Skill：

永远：

```txt
不允许接触底层协议
```

Skill：

只调用：

```python
robot.xxx.xxx()
```

---

# 5.1 Robot API 总入口

统一：

```python
robot.motor
robot.servo
robot.sensor
robot.navigation
robot.system
robot.user
```

例如：

```python
robot.motor.move()
```

---

# 5.2 Motor API

所有电机统一。

不管：

```txt
PWM
CAN
485
```

接口一致。

---

### set_speed()

```python
robot.motor.set_speed(
    id=1,
    speed=0.5
)
```

参数：

| 参数    |    类型 |
| ----- | ----: |
| id    |   int |
| speed | float |

范围：

```txt
-1.0 ~ 1.0
```

统一归一化。

底层：

自动换算。

例如：

```txt
PWM duty
RPM
CAN speed
```

---

### set_position()

```python
robot.motor.set_position(
    id=1,
    angle=90
)
```

支持：

```txt
闭环位置控制
```

---

### stop()

```python
robot.motor.stop(id=1)
```

立即停止。

---

### get_state()

```python
state = robot.motor.get_state(1)
```

返回：

```python
{
    "speed":0.5,
    "temperature":30,
    "error":0
}
```

---

# 5.3 Servo API

统一：

```python
robot.servo.move()
```

例如：

```python
robot.servo.move(
    id=2,
    angle=90,
    speed=0.5
)
```

支持：

```txt
普通PWM舵机
串口舵机
CAN舵机
```

统一抽象。

---

# 5.4 Sensor API

统一：

```python
robot.sensor.xxx.read()
```

例如：

IMU：

```python
imu = robot.sensor.imu.read()
```

返回：

```python
{
    "roll":0,
    "pitch":0,
    "yaw":0
}
```

超声波：

```python
distance = robot.sensor.ultrasonic.read()
```

---

### start_stream()

流模式：

```python
robot.sensor.camera.start_stream()
```

用于：

```txt
相机
激光雷达
高频IMU
```

---

# 5.5 Navigation API

移动机器人统一接口。

---

### goto()

```python
robot.navigation.goto(
    x=1.0,
    y=2.0
)
```

上位机：

负责：

```txt
路径规划
```

STM32：

负责：

```txt
运动控制
```

---

### stop()

```python
robot.navigation.stop()
```

---

# 5.6 System API

系统状态。

---

### get_health()

```python
robot.system.get_health()
```

返回：

```python
{
    "battery":80,
    "cpu_temp":55,
    "motor_error":0
}
```

---

### emergency_stop()

```python
robot.system.emergency_stop()
```

最高优先级。

---

# 6. Skill Runtime

核心思想：

```txt
Skill = 能力模块
```

例如：

```txt
walk
sit
follow
pick
dance
```

必须：

```txt
热插拔
```

---

# 6.1 Skill 生命周期

统一：

```python
init()

run()

pause()

resume()

stop()

status()
```

例如：

```python
class WalkSkill:

    def init(self):
        pass

    def run(self):
        pass

    def stop(self):
        pass
```

统一规范。

---

# 6.2 Skill 目录规范

示例：

```txt
skills/
└── walk/
    ├── skill.py
    ├── skill.yaml
    ├── README.md
    └── assets/
```

---

### skill.py

逻辑实现。

---

### skill.yaml

元数据。

例如：

```yaml
name: walk

description:
  walk robot

version: 1.0

permission:
  motor
  navigation

input:
  speed: float
  gait: string

output:
  success: bool
```

Hermes：

自动读取。

自动知道：

```txt
walk 怎么调用
```

---

# 6.3 autoskill.md

给：

Hermes

读的。

例如：

```md
# Skills

## walk

Move robot.

Parameters:
speed(float)

Example:
walk speed=0.5
```

避免：

```txt
prompt硬编码
```# 7. STM32 Runtime 架构设计（核心）

STM32 Runtime：

> 整个机器人实时控制核心

原则：

```txt id="0y4p65"
所有实时控制全部下放 STM32
```

Hermes：

永远：

```txt id="z5ye1i"
不碰实时控制
```

避免：

```txt id="tk3mwx"
延迟
卡顿
机器人抽搐
```

STM32：

负责：

```txt id="3m24ku"
PWM
PID
FOC
IMU
状态机
安全控制
协议执行
```

---

# 7.1 STM32 Runtime 总架构

目录：

```txt id="z1mjlwm"
stm32_runtime/
│
├── app/
│   ├── main.c
│   ├── app_init.c
│   └── app_task.c
│
├── driver/
│   ├── pwm/
│   ├── can/
│   ├── uart/
│   ├── usb/
│   ├── i2c/
│   ├── spi/
│   ├── adc/
│   ├── timer/
│   └── gpio/
│
├── device/
│   ├── motor/
│   ├── servo/
│   ├── imu/
│   ├── ultrasonic/
│   ├── lidar/
│   ├── encoder/
│   ├── oled/
│   ├── buzzer/
│   └── user_device/
│
├── service/
│   ├── locomotion/
│   ├── balance/
│   ├── posture/
│   ├── gait/
│   ├── navigation/
│   └── safety/
│
├── protocol/
│   ├── packet.c
│   ├── parser.c
│   ├── command.c
│   ├── heartbeat.c
│   ├── crc.c
│   └── dispatcher.c
│
├── middleware/
│   ├── scheduler.c
│   ├── event_bus.c
│   ├── state_machine.c
│   ├── watchdog.c
│   └── logger.c
│
├── config/
│   ├── st_config.h
│   ├── hardware_config.h
│   ├── protocol_config.h
│   └── pin_config.h
│
├── user_module/
│   ├── user_motor.c
│   ├── user_sensor.c
│   └── user_protocol.c
│
└── freertos/
```

---

# 7.2 为什么不推荐传统 STM32 工程结构

传统：

```txt id="f0l4rj"
main.c
gpio.c
tim.c
usart.c
```

问题：

项目变大后：

```txt id="5ubd1n"
强耦合
维护困难
无法扩展
```

最终：

```txt id="ih09uv"
几万行 main.c
```

必炸。

改：

> Driver → Device → Service

分层。

---

# 7.3 Driver 层

负责：

```txt id="zwjlwm"
直接硬件操作
```

例如：

PWM：

```c id="gm3zdf"
pwm_set_duty()
```

CAN：

```c id="7jlwm8"
can_send()
```

UART：

```c id="tmjlwm"
uart_receive()
```

特点：

```txt id="9jlwm0"
不包含业务逻辑
```

只：

```txt id="lwjlwm"
操作寄存器
```

---

# 7.4 Device 层

核心思想：

```txt id="mkjlwm"
设备抽象
```

例如：

不同电机：

```txt id="bljlwm"
PWM电机
CAN电机
485电机
```

统一：

```c id="e7jlwm"
motor_set_speed()
```

屏蔽差异。

---

## 电机抽象接口

统一：

```c id="87jlwm"
typedef struct
{
    void (*set_speed)(float speed);

    void (*set_position)(float pos);

    void (*stop)(void);

    float (*get_speed)(void);

}motor_driver_t;
```

例如：

PWM 电机：

```c id="3cjlwm"
pwm_motor_driver
```

CAN 电机：

```c id="fqjlwm"
can_motor_driver
```

上层：

永远：

```c id="owjlwm"
motor->set_speed()
```

无需知道：

```txt id="jlwm9x"
底层协议
```

实现：

真正：

```txt id="rjlwm4"
全兼容
```

---

## 传感器抽象接口

统一：

```c id="jlwm29"
typedef struct
{
    bool (*init)(void);

    bool (*read)(void* data);

}sensor_driver_t;
```

例如：

MPU6050：

```txt id="jlwm10"
I2C
```

ICM20948：

```txt id="jlwm11"
SPI
```

但：

上层：

统一：

```c id="jlwm12"
sensor_read()
```

---

# 7.5 Service 层（极其重要）

作用：

```txt id="jlwm13"
行为逻辑
```

例如：

四足机器人：

不要：

```txt id="jlwm14"
skill直接控制腿
```

而是：

```txt id="jlwm15"
walk service
```

负责：

```txt id="jlwm16"
逆运动学
步态
姿态平衡
```

AI：

只：

```txt id="jlwm17"
调用 walk()
```

---

## locomotion

负责：

```txt id="jlwm18"
机器人移动
```

例如：

```c id="jlwm19"
move_forward()
```

内部：

自动：

```txt id="jlwm20"
控制多个电机
```

---

## balance

负责：

```txt id="jlwm21"
IMU闭环
```

例如：

```txt id="jlwm22"
pitch
roll
```

自动修正。

---

## gait

负责：

```txt id="jlwm23"
步态
```

例如：

```txt id="jlwm24"
walk
trot
crawl
```

避免：

AI：

```txt id="jlwm25"
直接控制腿角度
```

---

# 7.6 Middleware 层

作用：

```txt id="jlwm26"
基础运行机制
```

例如：

---

## scheduler

任务调度。

建议：

```txt id="jlwm27"
FreeRTOS
```

线程：

```txt id="jlwm28"
sensor task
motor task
communication task
safety task
```

例如：

| 任务        |    频率 |
| --------- | ----: |
| motor     |  1kHz |
| imu       | 500Hz |
| uart      | 100Hz |
| heartbeat |   2Hz |

---

## event_bus

事件系统。

例如：

IMU：

发布：

```txt id="jlwm30"
imu/update
```

步态：

监听：

```txt id="jlwm31"
imu/update
```

低耦合。

---

## watchdog

必须。

例如：

超过：

```txt id="jlwm32"
1000ms
```

没收到：

上位机：

自动：

```txt id="jlwm33"
motor stop
```

避免：

```txt id="jlwm34"
机器人暴走
```

---

## state_machine

状态机。

状态：

```txt id="jlwm35"
boot
idle
walking
error
emergency
shutdown
```

避免：

```txt id="jlwm36"
逻辑混乱
```

---

# 8. 用户扩展机制

目标：

```txt id="jlwm37"
用户无需改框架源码
```

即可：

```txt id="jlwm38"
新增设备
新增协议
新增模块
```

---

# 8.1 新增电机

用户：

只需：

```txt id="jlwm39"
继承 motor interface
```

例如：

```c id="jlwm40"
motor_driver_t my_motor =
{
    .set_speed = my_speed,
    .stop = my_stop
};
```

注册：

```c id="jlwm41"
register_motor()
```

即可。

无需：

```txt id="jlwm42"
修改框架核心
```

---

# 8.2 新增传感器

用户：

新增：

```txt id="jlwm43"
user_sensor.c
```

实现：

```c id="jlwm44"
sensor_driver_t
```

即可。

---

# 8.3 用户私有协议

例如：

用户有：

```txt id="jlwm45"
私有CAN协议
```

写：

```c id="jlwm46"
user_protocol.c
```

注册：

```c id="jlwm47"
register_protocol()
```

即可。

无需：

```txt id="jlwm48"
修改 packet parser
```

---

# 8.4 用户 Skill

新增：

```txt id="jlwm49"
skills/my_skill
```

包含：

```txt id="jlwm50"
skill.py
skill.yaml
```

自动：

```txt id="jlwm51"
加载
```

Hermes：

自动：

```txt id="jlwm52"
理解
```

---

# 8.5 热插拔原则

新增# 9. 配置文件设计（核心）

原则：

> 配置驱动系统（Configuration Driven）

不要：

```txt id="8kwcjq"
写死参数
```

应该：

```txt id="x4wnk2"
yaml配置化
```

优点：

```txt id="8v9w5v"
无需改代码
热更新
用户可扩展
支持不同机器人
```

例如：

同一框架：

```txt id="nkk3hs"
四足狗
机械臂
履带机器人
轮式机器人
```

只改：

```txt id="ax5b4s"
yaml
```

即可。

---

# 9.1 配置结构

统一：

```txt id="8f6rfj"
config/
│
├── robot.yaml
├── hardware.yaml
├── stm32_config.yaml
├── protocol.yaml
├── skill.yaml
├── permission.yaml
└── user_config.yaml
```

---

# 9.2 robot.yaml

定义：

> 机器人总体信息

例如：

```yaml id="pfjlwm"
robot:
  name: robot_dog

  type: quadruped

  version: 1.0

  emergency_stop: true

  watchdog_timeout_ms: 1000

  control_frequency_hz: 100

  skill_timeout_ms: 5000

system:

  auto_reconnect: true

  reconnect_interval_ms: 1000
```

字段：

| 字段                |    作用 |
| ----------------- | ----: |
| name              | 机器人名称 |
| type              |    类型 |
| control_frequency |  控制频率 |
| watchdog          |    超时 |
| skill_timeout     |  技能超时 |

---

# 9.3 hardware.yaml

核心。

定义：

> 有哪些硬件

例如：

```yaml id="igjlwm"
motor:

  - id: 1
    type: pwm_motor
    pwm_channel: 1
    reverse: false

  - id: 2
    type: can_motor
    can_id: 0x01

servo:

  - id: 1
    type: pwm_servo

imu:

  type: icm20948
  interface: spi

ultrasonic:

  trigger_pin: PA1
  echo_pin: PA2
```

优点：

新增设备：

只：

```txt id="t9jlwm"
改yaml
```

无需：

```txt id="jlwm60"
改逻辑
```

---

# 9.4 stm32_config.yaml

定义：

> 下位机连接方式

例如：

```yaml id="jlwm61"
transport:

  type: uart

  device: /dev/ttyACM0

  baudrate: 115200

retry:

  max_retry: 3

heartbeat:

  enable: true

  timeout_ms: 1000
```

支持：

```txt id="jlwm62"
UART
USB CDC
CAN
RS485
```

统一配置。

---

# 9.5 protocol.yaml

协议配置。

例如：

```yaml id="jlwm63"
protocol:

  version: 1

  crc: crc16

  frame_head: 0xAA55

  max_payload_size: 256
```

方便：

未来：

```txt id="jlwm64"
升级协议
```

---

# 9.6 permission.yaml

权限控制。

限制：

```txt id="jlwm65"
AI权限
```

例如：

```yaml id="jlwm66"
motor:

  max_speed: 0.8

servo:

  max_angle: 180

system:

  allow_shutdown: false
```

防止：

```txt id="jlwm67"
AI输出危险动作
```

---

# 9.7 user_config.yaml

用户自定义。

例如：

```yaml id="jlwm68"
user_motor:

  max_torque: 0.6

private_protocol:

  enable: true
```

避免：

污染：

```txt id="jlwm69"
核心配置
```

---

# 10. 安全机制（极其重要）

这一章：

决定：

```txt id="jlwm70"
机器人是否会炸
```

必须：

> 默认安全

而不是：

```txt id="jlwm71"
默认开放
```

---

# 10.1 权限沙箱

Hermes：

不能：

直接：

```txt id="jlwm72"
无限控制
```

应该：

经过：

```txt id="jlwm73"
permission manager
```

例如：

AI：

请求：

```python id="jlwm74"
robot.motor.set_speed(
    speed=2.0
)
```

检查：

```yaml id="jlwm75"
max_speed: 0.8
```

自动：

```txt id="jlwm76"
拒绝
```

---

# 10.2 参数限幅

必须：

所有：

```txt id="jlwm77"
角度
速度
电流
扭矩
```

做：

```txt id="jlwm78"
clamp
```

例如：

```python id="jlwm79"
speed = clamp(
    speed,
    -0.8,
    0.8
)
```

否则：

容易：

```txt id="jlwm80"
堵转
过热
损坏
```

---

# 10.3 Watchdog

必须：

STM32：

监控：

```txt id="jlwm81"
上位机存活
```

超过：

```txt id="jlwm82"
1000ms
```

无数据：

执行：

```txt id="jlwm83"
stop all motor
```

避免：

```txt id="jlwm84"
USB断开后继续跑
```

---

# 10.4 Emergency Stop

最高优先级。

收到：

```txt id="jlwm85"
0x0503
```

立即：

```txt id="jlwm86"
关闭PWM
停止CAN输出
进入安全状态
```

不能：

```txt id="jlwm87"
排队
```

建议：

支持：

### 软件急停

```python id="jlwm88"
robot.system.emergency_stop()
```

### 硬件急停

独立：

```txt id="jlwm89"
按钮
```

直连：

STM32。

---

# 10.5 命令去重

避免：

```txt id="jlwm90"
重复包
```

利用：

```txt id="jlwm91"
sequence id
```

重复：

直接：

```txt id="jlwm92"
drop
```

---

# 10.6 ACK + Retry

命令：

必须：

```txt id="jlwm93"
ack
```

失败：

自动：

```txt id="jlwm94"
retry
```

例如：

```txt id="jlwm95"
最多3次
```

防：

```txt id="jlwm96"
串口丢包
```

---

# 10.7 Safe Mode

异常：

进入：

```txt id="jlwm97"
safe mode
```

例如：

场景：

```txt id="jlwm98"
电压低
姿态异常
通信丢失
电机过热
```

行为：

```txt id="jlwm99"
停止动作
降频
报警
```

---

# 11. 四足机器人专项架构

针对：

> 你的机器狗

建议：

> 强烈分层

不要：

```txt id="jlwm100"
AI直接控制关节
```

会炸。

---

# 11.1 推荐架构

分：

```txt id="jlwm101"
决策层
行为层
控制层
执行层
```

结构：

```txt id="jlwm102"
Hermes
   ↓
Behavior Skill
   ↓
Walk Service
   ↓
IK
   ↓
Motor Controller
```

---

# 11.2 AI 层

负责：

```txt id="jlwm103"
去哪
干什么
任务规划
```

例如：

```txt id="jlwm104"
走到桌子
```

而不是：

```txt id="jlwm105"
腿抬10°
```

---

# 11.3 行为层

负责：

```txt id="jlwm106"
walk
sit
stand
follow
```

例如：

```python id="jlwm107"
robot.walk(
    speed=0.3,
    gait="trot"
)
```

---

# 11.4 步态层（Gait）

建议：

STM32 做。

包括：

```txt id="jlwm108"
walk
trot
pace
crawl
```

频率：

```txt id="jlwm109"
100~500Hz
```

不能：

放：

```txt id="jlwm110"
Hermes
```

太慢。

---

# 11.5 IK 层

负责：

```txt id="jlwm111"
逆运动学
```

输入：

```txt id="jlwm112"
足端坐标
```

输出：

```txt id="jlwm113"
关节角
```

例如：

```txt id="jlwm114"
x y z
```

转：

```txt id="jlwm115"
hip
knee
ankle
```

建议：

> STM32 实时计算

不要：

放：

```txt id="jlwm116"
上位机
```

否则：

延迟明显。

---

# 11.6 IMU 平衡层

负责：

```txt id="jlwm117"
roll
pitch
```

自动：

修正：

```txt id="jlwm118"
腿部姿态
```

形成：

```txt id="jlwm119"
闭环稳定
```

---

# 11.7 状态机

状态：

```txt id="jlwm120"
idle
stand
walk
run
fall
recover
error
```

例如：

跌倒：

自动：

```txt id="jlwm121"
recover
```

而不是：

等：

```txt id="jlwm122"
AI反应
```
：

# 12. 开发路线图（强烈建议按阶段）

这个项目：

```txt id="2h92v3"
绝对不要一次写完
```

否则：

```txt id="r6k1f8"
100%烂尾
```

正确方式：

> MVP → 验证 → 重构 → 扩展

建议：

```txt id="7p9m4a"
V0.1 → V0.3 → V0.5 → V1.0
```

逐步演化。

---

# V0.1 最小可运行版本（2~4周）

目标：

> 跑通完整链路

先：

不要追求：

```txt id="2ab79x"
全兼容
```

只验证：

```txt id="6m7t9d"
架构对不对
```

---

## 功能目标

实现：

```txt id="t6x4f2"
Hermes
↓
Skill
↓
Robot API
↓
UART
↓
STM32
↓
电机动作
```

即可。

---

## 上位机

仅：

### 一个 transport

```txt id="s8y44q"
UART
```

---

### 一个 protocol

```txt id="a3z2k0"
ARF v0
```

---

### 两个 skill

```txt id="d5f8sx"
walk
stop
```

---

### 一个 Robot API

```python id="0j98nx"
robot.motor.set_speed()
```

---

## STM32

只做：

```txt id="g9n2rp"
PWM
串口
简单PID
```

不要：

```txt id="vh92mr"
CAN
485
FOC
```

---

## 验证标准

输入：

```txt id="j6n4tx"
向前走
```

机器人：

能：

```txt id="w6r4js"
稳定执行
```

即可。

---

# V0.3 通用机器人框架化

目标：

> 真正形成框架

增加：

---

## 多设备抽象

支持：

```txt id="j39dca"
motor
servo
sensor
```

统一 API。

---

## skill.yaml

Hermes：

自动理解：

能力。

---

## autoskill.md

自动生成。

---

## event bus

解耦。

---

## state machine

系统状态管理。

---

## watchdog

安全机制。

---

## 配置系统

支持：

```txt id="g4b4xe"
yaml
```

---

## 验证标准

新增一个：

```txt id="u9c2es"
新舵机
```

无需：

改核心。

只写：

```txt id="q9t2fr"
driver
yaml
```

即可运行。

说明：

架构成功。

---

# V0.5 实时控制增强

目标：

> 可用于复杂机器人

增加：

---

## CAN

支持：

```txt id="a2d7vz"
私有CAN
```

---

## 多 STM32

例如：

```txt id="w8z7uq"
运动控制板
传感器板
机械臂板
```

---

## IMU闭环

支持：

```txt id="4s4v1h"
balance
```

---

## gait

支持：

```txt id="z4w2yh"
walk
trot
```

---

## IK

逆运动学。

---

## Navigation

路径规划。

---

## 多线程

建议：

```txt id="h3d8mc"
FreeRTOS
```

---

## 验证标准

四足狗：

稳定：

```txt id="h7v1zm"
行走
转向
恢复平衡
```

---

# V1.0 正式版

目标：

> 通用机器人 Agent 框架

支持：

---

## 插件生态

用户：

直接：

```txt id="w2n7ku"
pip install
```

即可：

安装：

```txt id="v8t1az"
skill
driver
protocol
```

---

## Skill 市场

例如：

```txt id="j8k3qf"
follow human
object tracking
speech control
mapping
```

---

## 用户协议

支持：

```txt id="p5w8nk"
私有CAN
私有485
```

热插拔。

---

## 可视化控制台

例如：

WebUI：

```txt id="h2n6rv"
状态监控
日志
传感器
电机
```

---

## OTA

STM32：

在线更新。

---

## 模型切换

Hermes：

支持：

```txt id="u7q2wm"
本地模型
OpenAI
DeepSeek
```

---

# 13. 技术选型（推荐）

你现在目标：

```txt id="x9p7vn"
Ubuntu22.04 ARM64
STM32
Hermes
```

建议：

如下。

---

# 13.1 上位机技术栈

系统：

```txt id="g2x5hm"
Ubuntu 22.04 ARM64
```

推荐：

理由：

```txt id="s7m2kx"
稳定
生态成熟
驱动好
```

---

## Python

建议：

```txt id="k9n3wa"
Python 3.11
```

不要：

```txt id="r1t9qw"
3.8
```

太老。

---

## 环境管理

推荐：

```txt id="y5v8jm"
venv
```

不要：

```txt id="a4q7ve"
conda
```

太重。

---

## Hermes

负责：

```txt id="t2m5kq"
Agent Runtime
```

只：

负责：

```txt id="w6j4pn"
规划
决策
调用 skill
```

不要：

直接控制硬件。

---

## 配置

推荐：

```txt id="d5m3rs"
yaml
```

库：

```txt id="c8q2la"
pyyaml
```

---

## 通信

串口：

推荐：

```txt id="m4x7ph"
pyserial
```

CAN：

推荐：

```txt id="b9v5cz"
python-can
```

USB：

推荐：

```txt id="q3n8wd"
pyusb
```

---

## 日志

推荐：

```txt id="y6f4hq"
loguru
```

比：

Python logging：

舒服很多。

---

## 异步

推荐：

```txt id="h5d9tx"
asyncio
```

不要：

全线程。

否则：

后期：

```txt id="x4j2nc"
线程地狱
```

---

# 13.2 STM32 技术栈

建议：

> 统一 STM32 HAL

不要：

```txt id="q9k7mf"
StdPeriph
```

老。

---

## RTOS

强烈建议：

```txt id="s2v5cw"
FreeRTOS
```

理由：

你后面一定：

```txt id="u5j3hr"
多任务
```

例如：

```txt id="z4n2kb"
uart
motor
imu
watchdog
```

裸机：

后期：

很难维护。

---

## 编译器

建议：

### 开发

STM32CubeIDE

或者：

IAR Embedded Workbench

---

### 构建

推荐：

```txt id="x8k2tr"
CMake
```

后期：

多工程舒服。

---

## 通信协议优先级

建议：

优先：

```txt id="f5d2pw"
UART
```

然后：

```txt id="r9q7wh"
CAN
```

最后：

```txt id="g7m2ka"
RS485
```

不要：

一开始全上。

---

# 14. 未来扩展路线

先：

把：

```txt id="d4v6pw"
运动控制
```

做稳。

然后：

扩展。

---

# 14.1 多 STM32

未来：

支持：

```txt id="g2w9qn"
主控板
腿控板
传感器板
机械臂板
```

通过：

```txt id="u6x3mp"
CAN Bus
```

组网。

建议：

架构：

```txt id="m3k8wc"
master-slave
```

---

# 14.2 视觉

建议：

上位机：

负责。

例如：

```txt id="k4n2zh"
YOLO
SLAM
tracking
```

STM32：

别碰。

算力不够。

---

# 14.3 语音

增加：

```txt id="y3r8wm"
ASR
TTS
```

例如：

```txt id="u2n6cz"
麦克风
扬声器
```

---

# 14.4 机械臂

增加：

```txt id="n5w7pj"
arm skill
```

统一：

```python id="v7m2qa"
robot.arm.move()
```

即可。

---

# 14.5 多机器人

未来：

支持：

```txt id="x5q8hc"
robot1
robot2
robot3
```

协同。

---

# 15. 最终推荐 V1.0 目录树（建议直接按这个开工）

```txt id="r3n9qw"
ARF/
│
├── main.py
├── push.sh
├── requirements.txt
├── autoskill.md
│
├── core/
│   ├── runtime.py
│   ├── scheduler.py
│   ├── event_bus.py
│   ├── state_manager.py
│   ├── permission_manager.py
│   ├── config_loader.py
│   └── logger.py
│
├── runtime/
│   ├── skill_runtime.py
│   ├── task_manager.py
│   └── watchdog.py
│
├── robot/
│   ├── robot_api.py
│   ├── motor/
│   ├── servo/
│   ├── sensor/
│   ├── navigation/
│   └── system/
│
├── transport/
│   ├── uart_transport.py
│   ├── can_transport.py
│   └── rs485_transport.py
│
├── protocol/
│   ├── stm32_protocol.py
│   ├── parser.py
│   ├── packet.py
│   └── crc.py
│
├── skills/
│   ├── walk/
│   ├── stop/
│   └── user_skill/
│
├── plugin/
│
├── config/
│
├── logs/
│
└── stm32_runtime/
    │
    ├── driver/
    ├── device/
    ├── service/
    ├── middleware/
    ├── protocol/
    ├── user_module/
    └── app/
```

最终建议：

> **先做 V0.1：只跑通 Hermes → Skill → UART → STM32 → 电机。**

如果这个链路跑不稳，后面架构再漂亮都没意义。等你确认链路稳定，再扩展抽象层和插件化。


```txt id="jlwm53"
模块
skill
协议
```

必须：

```txt id="jlwm54"
零修改核心
```

这是：

系统寿命关键。


