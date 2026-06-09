#!/usr/bin/env python3
"""
ARF Basic Usage Example
基础使用示例
"""

import sys
sys.path.append('..')

from core.runtime import Runtime
from core.logger import log
import time


def example_1_basic_motor_control():
    """示例1：基础电机控制"""
    log.info("\n=== 示例1：基础电机控制 ===")
    
    runtime = Runtime()
    
    if not runtime.start():
        log.error("启动失败")
        return
    
    try:
        # 控制电机
        log.info("设置电机1速度为0.5")
        runtime.robot_api.motor.set_speed(1, 0.5)
        time.sleep(2)
        
        log.info("停止电机1")
        runtime.robot_api.motor.stop(1)
        
    finally:
        runtime.stop()


def example_2_skill_execution():
    """示例2：执行技能"""
    log.info("\n=== 示例2：执行技能 ===")
    
    runtime = Runtime()
    
    if not runtime.start():
        log.error("启动失败")
        return
    
    try:
        # 执行 walk 技能
        log.info("执行 walk 技能 - 前进")
        result = runtime.execute_skill(
            "walk",
            speed=0.5,
            direction="forward",
            duration=3.0
        )
        log.info(f"执行结果: {result}")
        
        time.sleep(1)
        
        # 执行 walk 技能 - 后退
        log.info("执行 walk 技能 - 后退")
        result = runtime.execute_skill(
            "walk",
            speed=0.3,
            direction="backward",
            duration=2.0
        )
        log.info(f"执行结果: {result}")
        
    finally:
        runtime.stop()


def example_3_event_subscription():
    """示例3：事件订阅"""
    log.info("\n=== 示例3：事件订阅 ===")
    
    from core.event_bus import event_bus
    
    # 订阅状态变更事件
    def on_state_changed(data):
        log.info(f"状态变更: {data['from']} -> {data['to']}")
    
    event_bus.subscribe("state/changed", on_state_changed)
    
    runtime = Runtime()
    
    if not runtime.start():
        log.error("启动失败")
        return
    
    try:
        time.sleep(2)
        
        # 触发状态变更
        from core.state_manager import state_manager, RobotState
        state_manager.transition(RobotState.MOVING)
        time.sleep(1)
        state_manager.transition(RobotState.IDLE)
        
    finally:
        runtime.stop()


def example_4_permission_control():
    """示例4：权限控制"""
    log.info("\n=== 示例4：权限控制 ===")
    
    from core.permission_manager import permission_manager
    
    # 检查速度权限
    allowed, msg = permission_manager.check_motor_permission(0.5)
    log.info(f"速度0.5: {allowed} - {msg}")
    
    allowed, msg = permission_manager.check_motor_permission(2.0)
    log.info(f"速度2.0: {allowed} - {msg}")
    
    # 参数验证
    validated = permission_manager.validate_motor_params(1, 2.0)
    log.info(f"验证后参数: {validated}")


def main():
    """主函数"""
    print("""
    ARF 使用示例
    
    1. 基础电机控制
    2. 执行技能
    3. 事件订阅
    4. 权限控制
    
    选择示例 (1-4): """, end='')
    
    choice = input().strip()
    
    if choice == '1':
        example_1_basic_motor_control()
    elif choice == '2':
        example_2_skill_execution()
    elif choice == '3':
        example_3_event_subscription()
    elif choice == '4':
        example_4_permission_control()
    else:
        log.error("无效选择")


if __name__ == "__main__":
    main()
