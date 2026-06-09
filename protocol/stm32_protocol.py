"""
ARF STM32 Protocol Handler
STM32 协议处理器
"""

from typing import Optional, Dict
import threading
import time
from protocol.packet import Packet
from protocol.command import CommandID, ACKStatus
from transport.base_transport import BaseTransport
from core.logger import log
from core.event_bus import event_bus


class STM32Protocol:
    """STM32 协议处理器"""
    
    def __init__(self, transport: BaseTransport):
        self.transport = transport
        self.running = False
        self.receive_thread: Optional[threading.Thread] = None
        self.pending_acks: Dict[int, Packet] = {}
        self.ack_timeout = 2.0
        self.last_heartbeat = 0
        self.heartbeat_interval = 0.5
    
    def start(self):
        """启动协议处理"""
        if not self.transport.is_connected():
            log.error("传输层未连接")
            return False
        
        self.running = True
        self.receive_thread = threading.Thread(target=self._receive_loop, daemon=True)
        self.receive_thread.start()
        
        log.info("✓ 协议处理器启动")
        return True
    
    def stop(self):
        """停止协议处理"""
        self.running = False
        if self.receive_thread:
            self.receive_thread.join(timeout=2.0)
        log.info("协议处理器停止")
    
    def send_packet(self, packet: Packet) -> bool:
        """
        发送数据包
        
        Args:
            packet: 数据包
        
        Returns:
            是否成功
        """
        data = packet.to_bytes()
        success = self.transport.send(data)
        
        if success:
            log.debug(f"发送数据包: {packet}")
        
        return success
    
    def send_and_wait(self, packet: Packet, timeout: float = 2.0) -> Optional[Packet]:
        """
        发送数据包并等待响应
        
        Args:
            packet: 数据包
            timeout: 超时时间
        
        Returns:
            响应数据包或 None
        """
        # 注册等待 ACK
        self.pending_acks[packet.sequence_id] = None
        
        # 发送
        if not self.send_packet(packet):
            del self.pending_acks[packet.sequence_id]
            return None
        
        # 等待响应
        start_time = time.time()
        while time.time() - start_time < timeout:
            if packet.sequence_id in self.pending_acks:
                response = self.pending_acks[packet.sequence_id]
                if response is not None:
                    del self.pending_acks[packet.sequence_id]
                    return response
            time.sleep(0.01)
        
        # 超时
        log.warning(f"等待 ACK 超时: seq={packet.sequence_id}")
        if packet.sequence_id in self.pending_acks:
            del self.pending_acks[packet.sequence_id]
        
        return None
    
    def _receive_loop(self):
        """接收循环"""
        buffer = b''
        
        while self.running:
            try:
                # 接收数据
                data = self.transport.receive(timeout=0.1)
                
                if data:
                    buffer += data
                    
                    # 尝试解析数据包
                    while len(buffer) >= 17:  # 最小包长度
                        packet = Packet.from_bytes(buffer)
                        
                        if packet and packet.verify_crc():
                            # 处理数据包
                            self._handle_packet(packet)
                            
                            # 移除已处理的数据
                            packet_length = 15 + packet.payload_length + 2
                            buffer = buffer[packet_length:]
                        else:
                            # 查找下一个帧头
                            next_head = buffer.find(b'\x55\xAA', 1)
                            if next_head > 0:
                                buffer = buffer[next_head:]
                            else:
                                break
                
                # 发送心跳
                current_time = time.time()
                if current_time - self.last_heartbeat > self.heartbeat_interval:
                    self._send_heartbeat()
                    self.last_heartbeat = current_time
                
            except Exception as e:
                log.error(f"接收循环错误: {e}")
                time.sleep(0.1)
    
    def _handle_packet(self, packet: Packet):
        """处理接收到的数据包"""
        log.debug(f"收到数据包: {packet}")
        
        # 处理 ACK
        if packet.command_id in [CommandID.ACK_SUCCESS, CommandID.ACK_ERROR]:
            if packet.sequence_id in self.pending_acks:
                self.pending_acks[packet.sequence_id] = packet
        
        # 发布事件
        event_bus.emit(f"packet/received", packet)
    
    def _send_heartbeat(self):
        """发送心跳"""
        packet = Packet(
            device_id=0,
            command_id=CommandID.SYS_HEARTBEAT,
            sequence_id=int(time.time() * 1000) % 65536
        )
        self.send_packet(packet)
