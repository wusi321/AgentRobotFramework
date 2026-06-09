"""
ARF Permission Manager
AI 权限控制管理
"""

from typing import Dict, Any
from core.logger import log
from core.config_loader import config_loader


class PermissionManager:
    """权限管理器"""
    
    def __init__(self):
        self.permissions = {}
        self.load_permissions()
    
    def load_permissions(self):
        """加载权限配置"""
        self.permissions = config_loader.load("permission")
        log.info("✓ 权限配置加载完成")
    
    def check_motor_permission(self, speed: float) -> tuple[bool, str]:
        """
        检查电机权限
        
        Args:
            speed: 速度值
        
        Returns:
            (是否允许, 消息)
        """
        motor_config = self.permissions.get("motor", {})
        max_speed = motor_config.get("max_speed", 1.0)
        
        if abs(speed) > max_speed:
            return False, f"速度超限: {speed}, 最大允许: {max_speed}"
        
        return True, "OK"
    
    def check_servo_permission(self, angle: float) -> tuple[bool, str]:
        """
        检查舵机权限
        
        Args:
            angle: 角度值
        
        Returns:
            (是否允许, 消息)
        """
        servo_config = self.permissions.get("servo", {})
        max_angle = servo_config.get("max_angle", 180)
        min_angle = servo_config.get("min_angle", 0)
        
        if angle < min_angle or angle > max_angle:
            return False, f"角度超限: {angle}, 范围: [{min_angle}, {max_angle}]"
        
        return True, "OK"
    
    def check_system_permission(self, action: str) -> tuple[bool, str]:
        """
        检查系统权限
        
        Args:
            action: 操作类型
        
        Returns:
            (是否允许, 消息)
        """
        system_config = self.permissions.get("system", {})
        
        if action == "shutdown":
            allow_shutdown = system_config.get("allow_shutdown", False)
            if not allow_shutdown:
                return False, "不允许关机操作"
        
        return True, "OK"
    
    def clamp_value(self, value: float, min_val: float, max_val: float) -> float:
        """
        限幅函数
        
        Args:
            value: 原始值
            min_val: 最小值
            max_val: 最大值
        
        Returns:
            限幅后的值
        """
        clamped = max(min_val, min(max_val, value))
        
        if clamped != value:
            log.warning(f"参数限幅: {value} -> {clamped}")
        
        return clamped
    
    def validate_motor_params(self, motor_id: int, speed: float) -> Dict[str, Any]:
        """
        验证并修正电机参数
        
        Args:
            motor_id: 电机 ID
            speed: 速度
        
        Returns:
            验证后的参数字典
        """
        motor_config = self.permissions.get("motor", {})
        max_speed = motor_config.get("max_speed", 1.0)
        
        # 限幅
        validated_speed = self.clamp_value(speed, -max_speed, max_speed)
        
        return {
            "motor_id": motor_id,
            "speed": validated_speed,
            "original_speed": speed,
            "clamped": validated_speed != speed
        }
    
    def validate_servo_params(self, servo_id: int, angle: float) -> Dict[str, Any]:
        """
        验证并修正舵机参数
        
        Args:
            servo_id: 舵机 ID
            angle: 角度
        
        Returns:
            验证后的参数字典
        """
        servo_config = self.permissions.get("servo", {})
        max_angle = servo_config.get("max_angle", 180)
        min_angle = servo_config.get("min_angle", 0)
        
        # 限幅
        validated_angle = self.clamp_value(angle, min_angle, max_angle)
        
        return {
            "servo_id": servo_id,
            "angle": validated_angle,
            "original_angle": angle,
            "clamped": validated_angle != angle
        }


# 全局权限管理器
permission_manager = PermissionManager()
