# ARF 快速开始指南

## 1. 系统要求

- Ubuntu 22.04 ARM64
- Python 3.11+
- STM32 开发板
- USB 连接线

## 2. 安装

### 2.1 克隆项目

```bash
git clone <repo_url>
cd ARF
```

### 2.2 运行安装脚本

```bash
chmod +x push.sh
./push.sh
```

### 2.3 激活虚拟环境

```bash
source venv/bin/activate
```

## 3. 配置

### 3.1 配置串口

编辑 `config/stm32_config.yaml`:

```yaml
transport:
  type: uart
  device: /dev/ttyACM0  # 根据实际情况修改
  baudrate: 115200
```

### 3.2 配置硬件

编辑 `config/hardware.yaml` 根据实际硬件配置电机、舵机、传感器。

### 3.3 配置权限

编辑 `config/permission.yaml` 设置 AI 控制权限。

## 4. 运行

### 4.1 连接 STM32

1. 将 STM32 通过 USB 连接到主机
2. 烧录固件（见 STM32 开发指南）
3. 检查串口设备：

```bash
ls /dev/ttyACM*
# 或
ls /dev/ttyUSB*
```

### 4.2 启动框架

```bash
python main.py
```

### 4.3 验证

系统启动后应该看到：

```
[✓] 加载配置
[✓] UART 连接成功
[✓] 协议处理器启动
[✓] Robot API 初始化完成
[✓] 加载了 1 个技能
[✓] ARF Runtime Started Successfully!
```

## 5. 测试

### 5.1 测试电机

编辑 `main.py` 添加测试代码：

```python
# 设置电机速度
runtime.robot_api.motor.set_speed(1, 0.5)
time.sleep(2)
runtime.robot_api.motor.stop(1)
```

### 5.2 测试 Skill

```python
# 执行 walk 技能
result = runtime.execute_skill(
    "walk",
    speed=0.5,
    direction="forward",
    duration=5.0
)
print(f"结果: {result}")
```

## 6. 开发自定义 Skill

见 [Skill 开发指南](skill_dev.md)

## 7. 常见问题

### Q: 串口连接失败

A: 检查：
1. 设备路径是否正确
2. 权限是否足够（需要加入 dialout 组）
3. 串口是否被其他程序占用

```bash
sudo usermod -a -G dialout $USER
# 重新登录后生效
```

### Q: 找不到 STM32 设备

A: 
1. 检查 USB 连接
2. 检查 STM32 固件是否正确烧录
3. 使用 `dmesg | tail` 查看设备日志

### Q: CRC 校验失败

A:
1. 检查串口波特率配置
2. 检查 STM32 协议版本是否匹配
3. 查看详细日志定位问题

## 8. 下一步

- [Skill 开发指南](skill_dev.md)
- [STM32 开发指南](stm32_dev.md)
- [协议规范](protocol.md)
- [扩展开发](extension.md)
