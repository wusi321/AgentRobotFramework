"""
ARF Base Transport
传输层基类
"""

from abc import ABC, abstractmethod
from typing import Optional


class BaseTransport(ABC):
    """传输层抽象基类"""
    
    def __init__(self):
        self.connected = False
    
    @abstractmethod
    def connect(self) -> bool:
        """
        连接设备
        
        Returns:
            是否成功
        """
        pass
    
    @abstractmethod
    def disconnect(self):
        """断开连接"""
        pass
    
    @abstractmethod
    def send(self, data: bytes) -> bool:
        """
        发送数据
        
        Args:
            data: 数据字节流
        
        Returns:
            是否成功
        """
        pass
    
    @abstractmethod
    def receive(self, timeout: float = 1.0) -> Optional[bytes]:
        """
        接收数据
        
        Args:
            timeout: 超时时间（秒）
        
        Returns:
            接收到的数据或 None
        """
        pass
    
    @abstractmethod
    def is_connected(self) -> bool:
        """
        检查连接状态
        
        Returns:
            是否连接
        """
        pass
    
    def flush(self):
        """刷新缓冲区（可选实现）"""
        pass
