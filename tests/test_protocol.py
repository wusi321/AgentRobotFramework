"""
ARF Protocol Tests
协议层测试
"""

import pytest
from protocol.packet import Packet
from protocol.command import CommandID
import struct


def test_packet_creation():
    """测试数据包创建"""
    packet = Packet(
        device_id=1,
        command_id=CommandID.MOTOR_SET_SPEED,
        sequence_id=1,
        payload=struct.pack('<Bf', 1, 0.5)
    )
    
    assert packet.device_id == 1
    assert packet.command_id == CommandID.MOTOR_SET_SPEED
    assert packet.sequence_id == 1


def test_packet_serialization():
    """测试数据包序列化"""
    packet = Packet(
        device_id=1,
        command_id=CommandID.MOTOR_SET_SPEED,
        sequence_id=1,
        payload=struct.pack('<Bf', 1, 0.5)
    )
    
    data = packet.to_bytes()
    assert len(data) > 0
    assert data[:2] == b'\x55\xAA'  # 帧头


def test_packet_deserialization():
    """测试数据包反序列化"""
    # 创建数据包
    packet1 = Packet(
        device_id=1,
        command_id=CommandID.MOTOR_SET_SPEED,
        sequence_id=1,
        payload=struct.pack('<Bf', 1, 0.5)
    )
    
    # 序列化
    data = packet1.to_bytes()
    
    # 反序列化
    packet2 = Packet.from_bytes(data)
    
    assert packet2 is not None
    assert packet2.device_id == packet1.device_id
    assert packet2.command_id == packet1.command_id
    assert packet2.sequence_id == packet1.sequence_id


def test_packet_crc_verification():
    """测试 CRC 校验"""
    packet = Packet(
        device_id=1,
        command_id=CommandID.MOTOR_SET_SPEED,
        sequence_id=1,
        payload=struct.pack('<Bf', 1, 0.5)
    )
    
    data = packet.to_bytes()
    parsed_packet = Packet.from_bytes(data)
    
    assert parsed_packet.verify_crc()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
