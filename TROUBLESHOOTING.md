# ARF 故障排查指南

## 常见问题及解决方案

### 1. ModuleNotFoundError: No module named 'loguru'

**问题**：运行 `python main.py` 时报模块找不到

**原因**：未激活虚拟环境

**解决方案**：

```bash
# 方法1：激活虚拟环境（推荐）
source venv/bin/activate
python main.py

# 方法2：使用启动脚本
chmod +x run.sh
./run.sh

# 方法3：直接使用虚拟环境的 Python
./venv/bin/python main.py
```

**验证环境**：
```bash
# 检查是否在虚拟环境中
which python
# 应该显示：/home/xxx/arf/venv/bin/python

# 检查 loguru 是否安装
python -c "import loguru; print('OK')"
```

---

### 2. 串口连接失败

**错误信息**：
```
UART 连接失败: [Errno 13] Permission denied: '/dev/ttyACM0'
```

**解决方案A：添加用户到 dialout 组**

```bash
# 添加当前用户到 dialout 组
sudo usermod -a -G dialout $USER

# 重新登录或重启
# 或临时激活
newgrp dialout

# 验证
groups | grep dialout
```

**解决方案B：临时使用 sudo（不推荐）**

```bash
sudo ./venv/bin/python main.py
```

**解决方案C：修改串口设备权限**

```bash
sudo chmod 666 /dev/ttyACM0
```

---

### 3. 找不到串口设备

**错误信息**：
```
⚠️ No serial port detected
```

**检查步骤**：

**1. 检查 STM32 是否连接**
```bash
# 查看 USB 设备
lsusb

# 查看串口设备
ls /dev/tty*
```

**2. 查看系统日志**
```bash
# 连接 STM32 后查看
dmesg | tail -20

# 应该看到类似：
# usb 1-1: new full-speed USB device number X using xhci_hcd
# cdc_acm 1-1:1.0: ttyACM0: USB ACM device
```

**3. 检查驱动**
```bash
# 检查 cdc_acm 驱动是否加载
lsmod | grep cdc_acm

# 如果没有，手动加载
sudo modprobe cdc_acm
```

**4. 测试串口**
```bash
# 安装测试工具
sudo apt install minicom

# 测试串口
minicom -D /dev/ttyACM0 -b 115200
```

---

### 4. 虚拟环境创建失败

**错误信息**：
```
E: Unable to locate package python3-venv
```

**解决方案**：

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3-venv python3-pip

# 重新运行安装脚本
./push.sh
```

---

### 5. pip 依赖冲突

**错误信息**：
```
ERROR: pip's dependency resolver does not currently take into account...
generate-parameter-library-py requires jinja2, which is not installed
```

**解决方案**：

这是警告，不影响 ARF 运行。如果需要修复：

```bash
source venv/bin/activate
pip install jinja2 typeguard
```

---

### 6. 配置文件找不到

**错误信息**：
```
配置文件不存在: config/robot.yaml
```

**检查步骤**：

```bash
# 确保在项目根目录
pwd
# 应该显示：/home/xxx/arf

# 检查配置文件
ls config/
# 应该显示：robot.yaml hardware.yaml ...

# 如果缺少配置文件，重新下载
```

---

### 7. 协议通信失败

**错误信息**：
```
等待 ACK 超时: seq=1
```

**可能原因**：

1. STM32 固件未烧录或有问题
2. 串口波特率不匹配
3. 协议版本不一致

**解决方案**：

**1. 检查 STM32 固件**
- 确认固件已正确烧录
- 检查固件中的协议实现

**2. 检查波特率**
```yaml
# config/stm32_config.yaml
transport:
  baudrate: 115200  # 确保与 STM32 一致
```

**3. 启用调试日志**
```yaml
# config/robot.yaml
system:
  log_level: DEBUG  # 改为 DEBUG
```

**4. 手动测试协议**
```python
# 运行测试脚本
source venv/bin/activate
python tests/test_protocol.py -v
```

---

### 8. Skill 执行失败

**错误信息**：
```
技能不存在: walk
```

**检查步骤**：

```bash
# 检查 Skill 目录
ls skills/
# 应该有：walk/

# 检查 Skill 文件
ls skills/walk/
# 应该有：skill.py skill.yaml

# 查看日志
cat logs/arf_*.log | grep "加载技能"
```

---

### 9. 权限被拒绝

**错误信息**：
```
速度超限: 2.0, 最大允许: 0.8
```

**这是正常的权限控制！**

**解决方案**：

修改 `config/permission.yaml`:

```yaml
motor:
  max_speed: 1.0  # 调整最大速度
```

或在代码中使用合法参数：

```python
robot.motor.set_speed(1, 0.8)  # <= 0.8
```

---

### 10. 日志文件过大

**问题**：`logs/` 目录占用空间过大

**解决方案**：

```bash
# 清理旧日志
rm logs/*.log

# 或配置日志保留时间
# 编辑 core/logger.py，修改 retention 参数
```

---

## 调试技巧

### 1. 启用详细日志

```yaml
# config/robot.yaml
system:
  log_level: DEBUG
```

### 2. 查看实时日志

```bash
# 激活环境
source venv/bin/activate

# 运行并查看日志
python main.py 2>&1 | tee output.log

# 或在另一个终端
tail -f logs/arf_*.log
```

### 3. 测试单个模块

```bash
# 测试协议
python tests/test_protocol.py

# 测试配置加载
python -c "from core.config_loader import config_loader; config_loader.load_all()"

# 测试串口
python -c "from transport.uart_transport import UARTTransport; t = UARTTransport(); print(t.connect())"
```

### 4. 使用示例代码调试

```bash
python examples/basic_usage.py
# 选择对应的示例进行测试
```

---

## 性能调优

### 1. 降低日志级别

```yaml
# config/robot.yaml
system:
  log_level: WARNING  # 或 ERROR
```

### 2. 调整心跳频率

```yaml
# config/stm32_config.yaml
heartbeat:
  interval: 1.0  # 降低频率
```

### 3. 增加超时时间

```yaml
# config/protocol.yaml
protocol:
  ack_timeout: 5.0  # 增加超时
```

---

## 获取帮助

如果以上方案都无法解决问题：

1. **查看日志**：`logs/arf_error_*.log`
2. **运行验证**：`python verify_installation.py`
3. **提交 Issue**：包含错误信息和日志
4. **查看文档**：`docs/` 目录

---

## 常用命令速查

```bash
# 安装
./push.sh

# 验证
python verify_installation.py

# 运行（推荐）
./run.sh

# 运行（手动）
source venv/bin/activate
python main.py

# 测试
python tests/test_protocol.py

# 示例
python examples/basic_usage.py

# 清理日志
rm logs/*.log

# 检查串口
ls /dev/tty*

# 查看日志
tail -f logs/arf_*.log
```

---

**最后更新**：2024-XX-XX
