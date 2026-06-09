"""
ARF Motor Module
电机控制模块
"""

from typing import Dict, Any
from core.logger import log
from core.permission_manager import permission_manager
from protocol.packet import Packet
from protocol.command import CommandID
import struct


class Motor:
    """电机控制类"""
    
    def __init__(self, protocol_handler):
        self.protocol_handler = protocol_handler
        self._sequence_id = 0
    
    def _get_next_sequence(self) -> int:
        """获取下一个序列号"""
        self._sequence_id = (self._sequence_id + 1) % 65536
        return self._sequence_id
    
    def set_speed(self, motor_id: int, speed: float) -> bool:
        """
        设置电机速度
        
        Args:
            motor_id: 电机 ID
            speed: 速度 (-1.0 ~ 1.0)
        
        Returns:
            是否成功
        """
        # 权限检查和参数验证
        validated = permission_manager.validate_motor_params(motor_id, speed)
        
        if validated["clamped"]:
            log.warning(f"电机速度被限幅: {validated['original_speed']} -> {validated['speed']}")
        
        # 构造 payload
        payload = struct.pack('<Bf', motor_id, validated['speed'])
        
        # 创建数据包
        packet = Packet(
            device_id=1,
            command_id=CommandID.MOTOR_SET_SPEED,
            sequence_id=self._get_next_sequence(),
            payload=payload
        )
        
        # 发送
        success = self.protocol_handler.send_packet(packet)
        
        if success:
            log.info(f"✓ 设置电机速度: ID={motor_id}, Speed={validated['speed']:.2f}")
        else:
            log.error(f"✗ 设置电机速度失败: ID={motor_id}")
        
        return success
    
    def set_position(self, motor_id: int, angle: float) -> bool:
        """
        设置电机位置
        
        Args:
            motor_id: 电机 ID
            angle: 角度（度）
        
        Returns:
            是否成功
        """
        payload = struct.pack('<Bf', motor_id, angle)
        
        packet = Packet(
            device_id=1,
            command_id=CommandID.MOTOR_SET_POSITION,
            sequence_id=self._get_next_sequence(),
            payload=payload
        )
        
        success = self.protocol_handler.send_packet(packet)
        
        if success:
            log.info(f"✓ 设置电机位置: ID={motor_id}, Angle={angle:.2f}°")
        else:
            log.error(f"✗ 设置电机位置失败: ID={motor_id}")
        
        return success
    
    def stop(self, motor_id: int) -> bool:
        """
        停止电机
        
        Args:
            motor_id: 电机 ID
        
        Returns:
            是否成功
        """
        payload = struct.pack('<B', motor_id)
        
        packet = Packet(
            device_id=1,
            command_id=CommandID.MOTOR_STOP,
            sequence_id=self._get_next_sequence(),
            payload=payload
        )
        
        success = self.protocol_handler.send_packet(packet)
        
        if success:
            log.info(f"✓ 停止电机: ID={motor_id}")
        else:
            log.error(f"✗ 停止电机失败: ID={motor_id}")
        
        return success
    
    def get_status(self, motor_id: int) -> Dict[str, Any]:
        """
        获取电机状态
        
        Args:
            motor_id: 电机 ID
        
        Returns:
            状态字典
        """
        payload = struct.pack('<B', motor_id)
        
        packet = Packet(
            device_id=1,
            command_id=CommandID.MOTOR_GET_STATUS,
            sequence_id=self._get_next_sequence(),
            payload=payload
        )
        
        # 发送并等待响应
        response = self.protocol_handler.send_and_wait(packet, timeout=1.0)
        
        if response:
            # 解析响应
            try:
                speed, temperature, error = struct.unpack('<ffI', response.payload)
                return {
                    "speed": speed,
                    "temperature": temperature,
                    "error": error
                }
            except Exception as e:
                log.error(f"解析电机状态失败: {e}")
        
        return {}
