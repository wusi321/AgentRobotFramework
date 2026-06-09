"""
ARF State Manager
机器人状态机管理
"""

from enum import Enum
from typing import Optional, Callable, Dict
from core.logger import log
from core.event_bus import event_bus


class RobotState(Enum):
    """机器人状态枚举"""
    BOOT = "boot"
    IDLE = "idle"
    MOVING = "moving"
    WALKING = "walking"
    CHARGING = "charging"
    ERROR = "error"
    EMERGENCY = "emergency"
    SHUTDOWN = "shutdown"


class StateManager:
    """状态管理器"""
    
    def __init__(self):
        self._current_state = RobotState.BOOT
        self._previous_state: Optional[RobotState] = None
        self._state_callbacks: Dict[RobotState, list] = {state: [] for state in RobotState}
        self._transition_rules = self._init_transition_rules()
    
    def _init_transition_rules(self) -> Dict[RobotState, list]:
        """
        初始化状态转换规则
        
        Returns:
            状态转换规则字典
        """
        return {
            RobotState.BOOT: [RobotState.IDLE, RobotState.ERROR],
            RobotState.IDLE: [RobotState.MOVING, RobotState.WALKING, RobotState.CHARGING, 
                             RobotState.ERROR, RobotState.EMERGENCY, RobotState.SHUTDOWN],
            RobotState.MOVING: [RobotState.IDLE, RobotState.ERROR, RobotState.EMERGENCY],
            RobotState.WALKING: [RobotState.IDLE, RobotState.ERROR, RobotState.EMERGENCY],
            RobotState.CHARGING: [RobotState.IDLE, RobotState.ERROR],
            RobotState.ERROR: [RobotState.IDLE, RobotState.EMERGENCY, RobotState.SHUTDOWN],
            RobotState.EMERGENCY: [RobotState.IDLE, RobotState.SHUTDOWN],
            RobotState.SHUTDOWN: []
        }
    
    def get_state(self) -> RobotState:
        """获取当前状态"""
        return self._current_state
    
    def get_previous_state(self) -> Optional[RobotState]:
        """获取前一个状态"""
        return self._previous_state
    
    def can_transition(self, target_state: RobotState) -> bool:
        """
        检查是否可以转换到目标状态
        
        Args:
            target_state: 目标状态
        
        Returns:
            是否可以转换
        """
        allowed_states = self._transition_rules.get(self._current_state, [])
        return target_state in allowed_states
    
    def transition(self, target_state: RobotState, force: bool = False) -> bool:
        """
        状态转换
        
        Args:
            target_state: 目标状态
            force: 是否强制转换（跳过规则检查）
        
        Returns:
            转换是否成功
        """
        if not force and not self.can_transition(target_state):
            log.warning(f"状态转换被拒绝: {self._current_state.value} -> {target_state.value}")
            return False
        
        self._previous_state = self._current_state
        self._current_state = target_state
        
        log.info(f"状态转换: {self._previous_state.value} -> {self._current_state.value}")
        
        # 发布状态变更事件
        event_bus.emit("state/changed", {
            "from": self._previous_state.value,
            "to": self._current_state.value
        })
        
        # 执行状态回调
        self._execute_callbacks(target_state)
        
        return True
    
    def on_state(self, state: RobotState, callback: Callable):
        """
        注册状态回调
        
        Args:
            state: 状态
            callback: 回调函数
        """
        self._state_callbacks[state].append(callback)
        log.debug(f"注册状态回调: {state.value}")
    
    def _execute_callbacks(self, state: RobotState):
        """执行状态回调"""
        for callback in self._state_callbacks[state]:
            try:
                callback()
            except Exception as e:
                log.error(f"状态回调执行错误 {state.value}: {e}")
    
    def is_state(self, *states: RobotState) -> bool:
        """
        检查当前是否是指定状态之一
        
        Args:
            states: 状态列表
        
        Returns:
            是否匹配
        """
        return self._current_state in states
    
    def emergency_stop(self):
        """紧急停止"""
        log.warning("触发紧急停止")
        self.transition(RobotState.EMERGENCY, force=True)
        event_bus.emit("system/emergency_stop", None)


# 全局状态管理器
state_manager = StateManager()
