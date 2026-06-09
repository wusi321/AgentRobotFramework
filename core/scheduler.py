"""
ARF Scheduler
任务调度器
"""

import asyncio
from typing import Callable, Optional
from dataclasses import dataclass
from enum import Enum
from core.logger import log
import time


class TaskPriority(Enum):
    """任务优先级"""
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3


@dataclass
class Task:
    """任务数据类"""
    name: str
    callback: Callable
    priority: TaskPriority
    timestamp: float
    
    def __lt__(self, other):
        """优先级比较（用于优先队列）"""
        if self.priority.value != other.priority.value:
            return self.priority.value > other.priority.value
        return self.timestamp < other.timestamp


class Scheduler:
    """任务调度器"""
    
    def __init__(self):
        self.task_queue = asyncio.PriorityQueue()
        self.running = False
        self.current_task: Optional[Task] = None
    
    async def add_task(self, name: str, callback: Callable, 
                      priority: TaskPriority = TaskPriority.NORMAL):
        """
        添加任务
        
        Args:
            name: 任务名称
            callback: 任务回调函数
            priority: 任务优先级
        """
        task = Task(
            name=name,
            callback=callback,
            priority=priority,
            timestamp=time.time()
        )
        
        await self.task_queue.put((priority.value, task))
        log.debug(f"添加任务: {name}, 优先级: {priority.name}")
    
    async def run(self):
        """运行调度器"""
        self.running = True
        log.info("调度器启动")
        
        while self.running:
            try:
                # 获取最高优先级任务
                _, task = await asyncio.wait_for(
                    self.task_queue.get(),
                    timeout=0.1
                )
                
                self.current_task = task
                log.debug(f"执行任务: {task.name}")
                
                # 执行任务
                if asyncio.iscoroutinefunction(task.callback):
                    await task.callback()
                else:
                    task.callback()
                
                self.current_task = None
                
            except asyncio.TimeoutError:
                # 队列为空，继续等待
                await asyncio.sleep(0.01)
            except Exception as e:
                log.error(f"任务执行错误 {task.name if task else 'unknown'}: {e}")
                self.current_task = None
    
    def stop(self):
        """停止调度器"""
        self.running = False
        log.info("调度器停止")
    
    def get_queue_size(self) -> int:
        """获取队列大小"""
        return self.task_queue.qsize()
    
    def is_idle(self) -> bool:
        """是否空闲"""
        return self.current_task is None and self.task_queue.empty()


# 全局调度器
scheduler = Scheduler()
