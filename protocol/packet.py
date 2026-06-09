"""
ARF Packet Module
数据包结构定义
"""

import struct
from dataclasses import dataclass
from typing import Optional
import time
from protocol.crc import crc16


# 协议常量
FRAME_HEAD = 0xAA55
PROTOCOL_VERSION = 0x01
MAX_PAYLOAD_SIZE = 256


@dataclass
class Packet:
    """数据包结构"""
    head: int = FRAME_HEAD
    version: int = PROTOCOL_VERSION
    device_id: int = 0
    command_id: int = 0
    sequence_id: int = 0
    timestamp: int = 0
    payload_length: int = 0
    payload: bytes = b''
    crc: int = 0
    
    def to_bytes(self) -> bytes:
        """
        转换为字节流
        
        Returns:
            字节流
        """
        # 更新 payload 长度
        self.payload_length = len(self.payload)
        
        # 更新时间戳（毫秒）
        if self.timestamp == 0:
            self.timestamp = int(time.time() * 1000)
        
        # 打包头部
        header = struct.pack(
            '<HBBHHIH',
            self.head,
            self.version,
            self.device_id,
            self.command_id,
            self.sequence_id,
            self.timestamp,
            self.payload_length
        )
        
        # 组合数据
        data = header + self.payload
        
        # 计算 CRC
        self.crc = crc16(data)
        
        # 添加 CRC
        full_packet = data + struct.pack('<H', self.crc)
        
        return full_packet
    
    @classmethod
    def from_bytes(cls, data: bytes) -> Optional['Packet']:
        """
        从字节流解析
        
        Args:
            data: 字节流
        
        Returns:
            Packet 对象或 None
        """
        if len(data) < 15:  # 最小包长度
            return None
        
        try:
            # 解析头部
            header = struct.unpack('<HBBHHIH', data[:15])
            
            head = header[0]
            version = header[1]
            device_id = header[2]
            command_id = header[3]
            sequence_id = header[4]
            timestamp = header[5]
            payload_length = header[6]
            
            # 检查帧头
            if head != FRAME_HEAD:
                return None
            
            # 检查数据长度
            expected_length = 15 + payload_length + 2
            if len(data) < expected_length:
                return None
            
            # 提取 payload
            payload = data[15:15+payload_length]
            
            # 提取 CRC
            crc_bytes = data[15+payload_length:15+payload_length+2]
            crc = struct.unpack('<H', crc_bytes)[0]
            
            # 创建 Packet
            packet = cls(
                head=head,
                version=version,
                device_id=device_id,
                command_id=command_id,
                sequence_id=sequence_id,
                timestamp=timestamp,
                payload_length=payload_length,
                payload=payload,
                crc=crc
            )
            
            return packet
            
        except Exception:
            return None
    
    def verify_crc(self) -> bool:
        """
        验证 CRC
        
        Returns:
            校验是否通过
        """
        # 重新计算 CRC
        header = struct.pack(
            '<HBBHHIH',
            self.head,
            self.version,
            self.device_id,
            self.command_id,
            self.sequence_id,
            self.timestamp,
            self.payload_length
        )
        
        data = header + self.payload
        calculated_crc = crc16(data)
        
        return calculated_crc == self.crc
    
    def __repr__(self) -> str:
        return (f"Packet(device={self.device_id}, cmd=0x{self.command_id:04X}, "
                f"seq={self.sequence_id}, payload_len={self.payload_length})")
