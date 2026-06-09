"""
ARF UART Transport
UART 传输实现
"""

import serial
from typing import Optional
from transport.base_transport import BaseTransport
from core.logger import log


class UARTTransport(BaseTransport):
    """UART 传输层"""
    
    def __init__(self, port: str = "/dev/ttyACM0", baudrate: int = 115200):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.serial: Optional[serial.Serial] = None
    
    def connect(self) -> bool:
        """连接串口"""
        try:
            self.serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=1.0,
                write_timeout=1.0
            )
            self.connected = True
            log.info(f"✓ UART 连接成功: {self.port} @ {self.baudrate}")
            return True
        except Exception as e:
            log.error(f"UART 连接失败: {e}")
            self.connected = False
            return False
    
    def disconnect(self):
        """断开串口"""
        if self.serial and self.serial.is_open:
            self.serial.close()
            self.connected = False
            log.info("UART 断开连接")
    
    def send(self, data: bytes) -> bool:
        """发送数据"""
        if not self.is_connected():
            log.error("UART 未连接")
            return False
        
        try:
            self.serial.write(data)
            log.debug(f"UART 发送: {len(data)} 字节")
            return True
        except Exception as e:
            log.error(f"UART 发送失败: {e}")
            return False
    
    def receive(self, timeout: float = 1.0) -> Optional[bytes]:
        """接收数据"""
        if not self.is_connected():
            return None
        
        try:
            # 设置超时
            old_timeout = self.serial.timeout
            self.serial.timeout = timeout
            
            # 等待数据
            if self.serial.in_waiting > 0:
                data = self.serial.read(self.serial.in_waiting)
                log.debug(f"UART 接收: {len(data)} 字节")
                return data
            
            # 恢复超时
            self.serial.timeout = old_timeout
            return None
            
        except Exception as e:
            log.error(f"UART 接收失败: {e}")
            return None
    
    def is_connected(self) -> bool:
        """检查连接状态"""
        return self.connected and self.serial and self.serial.is_open
    
    def flush(self):
        """刷新缓冲区"""
        if self.serial and self.serial.is_open:
            self.serial.flush()
            self.serial.reset_input_buffer()
            self.serial.reset_output_buffer()
