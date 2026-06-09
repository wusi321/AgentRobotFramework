"""
ARF Core Runtime
系统运行时核心
"""

from core.logger import log
from core.config_loader import config_loader
from core.state_manager import state_manager, RobotState
from transport.uart_transport import UARTTransport
from protocol.stm32_protocol import STM32Protocol
from robot.robot_api import RobotAPI
from runtime.skill_runtime import SkillRuntime
import signal
import sys


class Runtime:
    """ARF 运行时"""
    
    def __init__(self):
        self.transport = None
        self.protocol = None
        self.robot_api = None
        self.skill_runtime = None
        self.running = False
        
        # 注册信号处理
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """信号处理器"""
        log.warning(f"收到信号: {signum}")
        self.stop()
        sys.exit(0)
    
    def start(self):
        """启动运行时"""
        log.info("=" * 50)
        log.info("  ARF Runtime Starting...")
        log.info("=" * 50)
        
        try:
            # 1. 加载配置
            log.info("[1/5] 加载配置...")
            config_loader.load_all()
            
            # 2. 初始化传输层
            log.info("[2/5] 初始化传输层...")
            stm32_config = config_loader.get("stm32_config")
            transport_config = stm32_config.get("transport", {})
            
            if transport_config.get("type") == "uart":
                self.transport = UARTTransport(
                    port=transport_config.get("device", "/dev/ttyACM0"),
                    baudrate=transport_config.get("baudrate", 115200)
                )
            
            if not self.transport.connect():
                log.error("传输层连接失败")
                return False
            
            # 3. 初始化协议层
            log.info("[3/5] 初始化协议层...")
            self.protocol = STM32Protocol(self.transport)
            self.protocol.start()
            
            # 4. 初始化 Robot API
            log.info("[4/5] 初始化 Robot API...")
            self.robot_api = RobotAPI(self.protocol)
            
            # 5. 加载技能
            log.info("[5/5] 加载技能...")
            self.skill_runtime = SkillRuntime(self.robot_api)
            self.skill_runtime.load_all_skills()
            
            # 状态转换
            state_manager.transition(RobotState.IDLE)
            
            self.running = True
            
            log.info("=" * 50)
            log.info("  ARF Runtime Started Successfully!")
            log.info("=" * 50)
            
            return True
            
        except Exception as e:
            log.error(f"启动失败: {e}")
            self.stop()
            return False
    
    def stop(self):
        """停止运行时"""
        if not self.running:
            return
        
        log.info("正在停止 ARF Runtime...")
        
        self.running = False
        
        # 停止协议处理
        if self.protocol:
            self.protocol.stop()
        
        # 断开传输层
        if self.transport:
            self.transport.disconnect()
        
        # 状态转换
        state_manager.transition(RobotState.SHUTDOWN, force=True)
        
        log.info("✓ ARF Runtime 已停止")
    
    def execute_skill(self, skill_name: str, **kwargs):
        """
        执行技能
        
        Args:
            skill_name: 技能名称
            **kwargs: 技能参数
        """
        if not self.running:
            log.error("运行时未启动")
            return None
        
        return self.skill_runtime.execute_skill(skill_name, **kwargs)
    
    def list_skills(self):
        """列出所有技能"""
        if self.skill_runtime:
            return self.skill_runtime.list_skills()
        return []
    
    def get_status(self):
        """获取系统状态"""
        return {
            "running": self.running,
            "state": state_manager.get_state().value,
            "transport_connected": self.transport.is_connected() if self.transport else False,
            "skills": self.list_skills()
        }
