"""
ARF Event Bus
事件总线 - 实现模块解耦
"""

from typing import Callable, Dict, List
from collections import defaultdict
from core.logger import log
import asyncio


class EventBus:
    """事件总线"""
    
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = defaultdict(list)
        self._async_subscribers: Dict[str, List[Callable]] = defaultdict(list)
    
    def subscribe(self, event_type: str, callback: Callable):
        """
        订阅事件（同步）
        
        Args:
            event_type: 事件类型
            callback: 回调函数
        """
        self._subscribers[event_type].append(callback)
        log.debug(f"订阅事件: {event_type}")
    
    def subscribe_async(self, event_type: str, callback: Callable):
        """
        订阅事件（异步）
        
        Args:
            event_type: 事件类型
            callback: 异步回调函数
        """
        self._async_subscribers[event_type].append(callback)
        log.debug(f"订阅异步事件: {event_type}")
    
    def unsubscribe(self, event_type: str, callback: Callable):
        """
        取消订阅
        
        Args:
            event_type: 事件类型
            callback: 回调函数
        """
        if callback in self._subscribers[event_type]:
            self._subscribers[event_type].remove(callback)
            log.debug(f"取消订阅: {event_type}")
        
        if callback in self._async_subscribers[event_type]:
            self._async_subscribers[event_type].remove(callback)
            log.debug(f"取消异步订阅: {event_type}")
    
    def emit(self, event_type: str, data=None):
        """
        发布事件（同步）
        
        Args:
            event_type: 事件类型
            data: 事件数据
        """
        log.debug(f"发布事件: {event_type}")
        
        for callback in self._subscribers[event_type]:
            try:
                callback(data)
            except Exception as e:
                log.error(f"事件回调错误 {event_type}: {e}")
    
    async def emit_async(self, event_type: str, data=None):
        """
        发布事件（异步）
        
        Args:
            event_type: 事件类型
            data: 事件数据
        """
        log.debug(f"发布异步事件: {event_type}")
        
        tasks = []
        for callback in self._async_subscribers[event_type]:
            tasks.append(callback(data))
        
        if tasks:
            try:
                await asyncio.gather(*tasks, return_exceptions=True)
            except Exception as e:
                log.error(f"异步事件回调错误 {event_type}: {e}")
    
    def clear(self, event_type: str = None):
        """
        清除订阅
        
        Args:
            event_type: 事件类型，None 表示清除所有
        """
        if event_type:
            self._subscribers[event_type].clear()
            self._async_subscribers[event_type].clear()
            log.debug(f"清除订阅: {event_type}")
        else:
            self._subscribers.clear()
            self._async_subscribers.clear()
            log.debug("清除所有订阅")
    
    def get_subscribers(self, event_type: str) -> int:
        """获取订阅者数量"""
        return len(self._subscribers[event_type]) + len(self._async_subscribers[event_type])


# 全局事件总线
event_bus = EventBus()
