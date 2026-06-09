"""
ARF Robot API
机器人统一 API 入口
"""

from robot.motor.motor import Motor
from core.logger import log


class RobotAPI:
    """机器人 API 统一入口"""
    
    def __init__(self, protocol_handler):
        self.protocol_handler = protocol_handler
        
        # 初始化各模块
        self.motor = Motor(protocol_handler)
        
        log.info("✓ Robot API 初始化完成")
    
    def emergency_stop(self):
        """紧急停止"""
        log.warning("执行紧急停止")
        # TODO: 实现紧急停止逻辑
        pass
    
    def get_health(self):
        """获取系统健康状态"""
        # TODO: 实现健康检查
        return {
            "status": "ok",
            "battery": 100,
            "temperature": 25
        }
