# ARF 5分钟快速开始

## 1. 安装（1分钟）

```bash
# 克隆项目
git clone <repo_url>
cd ARF

# 运行安装脚本
chmod +x push.sh
./push.sh

# 激活环境
source venv/bin/activate
```

## 2. 验证安装（30秒）

```bash
python verify_installation.py
```

看到 "🎉 所有检查通过！" 即可。

## 3. 配置 STM32（1分钟）

### 3.1 连接 STM32

USB 连接 STM32 到电脑

### 3.2 检查串口

```bash
ls /dev/ttyACM*
# 或
ls /dev/ttyUSB*
```

### 3.3 修改配置

编辑 `config/stm32_config.yaml`:

```yaml
transport:
  device: /dev/ttyACM0  # 改成你的串口
```

## 4. 运行框架（10秒）

### 方法1：使用启动脚本（推荐）

```bash
chmod +x run.sh
./run.sh
```

### 方法2：手动激活环境

```bash
source venv/bin/activate
python main.py
```

### 方法3：直接使用虚拟环境 Python

```bash
./venv/bin/python main.py
```

看到输出：

```
[✓] 加载配置
[✓] UART 连接成功
[✓] 协议处理器启动
[✓] Robot API 初始化完成
[✓] 加载了 1 个技能
[✓] ARF Runtime Started Successfully!
```

## 5. 测试功能（2分钟）

### 5.1 测试电机

修改 `main.py`，在演示程序处：

```python
# 设置电机1速度
runtime.robot_api.motor.set_speed(1, 0.5)
time.sleep(2)

# 停止电机
runtime.robot_api.motor.stop(1)
```

### 5.2 执行 Skill

```python
# 执行 walk 技能
result = runtime.execute_skill(
    "walk",
    speed=0.5,
    direction="forward",
    duration=3.0
)
print(f"结果: {result}")
```

### 5.3 运行示例

```bash
python examples/basic_usage.py
```

## 6. 开发第一个 Skill（2分钟）

### 6.1 创建目录

```bash
mkdir skills/my_skill
```

### 6.2 创建 skill.py

`skills/my_skill/skill.py`:

```python
from core.logger import log

class MySkill:
    def __init__(self, robot_api):
        self.robot = robot_api
    
    def init(self):
        log.info("MySkill 初始化")
        return True
    
    def run(self):
        log.info("MySkill 执行")
        # 你的逻辑
        return {"success": True}
    
    def stop(self):
        log.info("MySkill 停止")
```

### 6.3 创建 skill.yaml

`skills/my_skill/skill.yaml`:

```yaml
name: my_skill
description: My custom skill
version: "1.0.0"

input:
  param1:
    type: float
    default: 0.5

output:
  success:
    type: bool
```

### 6.4 测试

```python
result = runtime.execute_skill("my_skill")
```

## 7. 常见问题

### Q: 串口连接失败？

```bash
# 检查权限
sudo usermod -a -G dialout $USER
# 重新登录

# 检查设备
dmesg | tail
```

### Q: 模块导入错误？

```bash
# 确保在项目根目录
cd ARF

# 激活虚拟环境
source venv/bin/activate

# 重新安装依赖
pip install -r requirements.txt
```

### Q: STM32 没响应？

1. 检查固件是否烧录
2. 检查串口配置
3. 查看日志 `logs/`

## 8. 下一步

- 📖 阅读 [架构文档](docs/architecture.md)
- 🛠️ 查看 [API 参考](docs/api.md)
- 💡 浏览 [示例代码](examples/)
- 🚀 开始你的机器人项目！

## 9. 获取帮助

- GitHub Issues
- 文档：`docs/`
- 示例：`examples/`

---

**祝你使用愉快！🎉**
