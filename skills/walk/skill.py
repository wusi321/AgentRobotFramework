"""
Walk Skill
移动技能
"""

from core.logger import log
import time


class WalkSkill:
    """Walk Skill 实现"""
    
    def __init__(self, robot_api):
        self.robot = robot_api
        self.running = False
    
    def init(self):
        """初始化"""
        log.info("Walk Skill 初始化")
        return True
    
    def run(self, speed: float = 0.5, direction: str = "forward", duration: float = 5.0):
        """
        执行移动
        
        Args:
            speed: 速度 (0.0 ~ 1.0)
            direction: 方向 (forward, backward, left, right)
            duration: 持续时间（秒）
        
        Returns:
            执行结果
        """
        log.info(f"执行 Walk: speed={speed}, direction={direction}, duration={duration}s")
        
        self.running = True
        
        try:
            # 根据方向设置电机速度
            if direction == "forward":
                self.robot.motor.set_speed(1, speed)
                self.robot.motor.set_speed(2, speed)
            elif direction == "backward":
                self.robot.motor.set_speed(1, -speed)
                self.robot.motor.set_speed(2, -speed)
            elif direction == "left":
                self.robot.motor.set_speed(1, -speed)
                self.robot.motor.set_speed(2, speed)
            elif direction == "right":
                self.robot.motor.set_speed(1, speed)
                self.robot.motor.set_speed(2, -speed)
            
            # 等待指定时间
            time.sleep(duration)
            
            # 停止电机
            self.robot.motor.stop(1)
            self.robot.motor.stop(2)
            
            log.info("✓ Walk 执行完成")
            
            return {
                "success": True,
                "distance": speed * duration  # 简化计算
            }
            
        except Exception as e:
            log.error(f"Walk 执行失败: {e}")
            self.stop()
            return {
                "success": False,
                "distance": 0
            }
        finally:
            self.running = False
    
    def pause(self):
        """暂停"""
        log.info("Walk 暂停")
        self.robot.motor.stop(1)
        self.robot.motor.stop(2)
    
    def resume(self):
        """恢复"""
        log.info("Walk 恢复")
    
    def stop(self):
        """停止"""
        log.info("Walk 停止")
        self.running = False
        self.robot.motor.stop(1)
        self.robot.motor.stop(2)
    
    def status(self):
        """获取状态"""
        return {
            "running": self.running
        }
