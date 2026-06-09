"""
ARF Command Definitions
命令定义
"""

from enum import IntEnum


class CommandID(IntEnum):
    """命令 ID 枚举"""
    
    # Motor commands (0x01xx)
    MOTOR_SET_SPEED = 0x0101
    MOTOR_SET_POSITION = 0x0102
    MOTOR_STOP = 0x0103
    MOTOR_SET_TORQUE = 0x0104
    MOTOR_GET_STATUS = 0x0105
    
    # Servo commands (0x02xx)
    SERVO_MOVE = 0x0201
    SERVO_ENABLE = 0x0202
    SERVO_DISABLE = 0x0203
    SERVO_GET_STATUS = 0x0204
    
    # Sensor commands (0x03xx)
    SENSOR_READ = 0x0301
    SENSOR_START_STREAM = 0x0302
    SENSOR_STOP_STREAM = 0x0303
    
    # Navigation commands (0x04xx)
    NAV_GOTO = 0x0401
    NAV_STOP = 0x0402
    NAV_GET_POSITION = 0x0403
    
    # System commands (0x05xx)
    SYS_HEARTBEAT = 0x0501
    SYS_WATCHDOG = 0x0502
    SYS_EMERGENCY_STOP = 0x0503
    SYS_GET_STATE = 0x0504
    SYS_RESET = 0x0505
    
    # ACK commands (0x06xx)
    ACK_SUCCESS = 0x0601
    ACK_ERROR = 0x0602
    
    # User defined (0xF0xx)
    USER_CUSTOM_1 = 0xF001
    USER_CUSTOM_2 = 0xF002


class ACKStatus(IntEnum):
    """ACK 状态码"""
    SUCCESS = 0
    ERROR_PARAM = 1
    ERROR_TIMEOUT = 2
    ERROR_EXECUTION = 3
    ERROR_UNREGISTERED = 4
    ERROR_PERMISSION = 5


def get_command_name(command_id: int) -> str:
    """
    获取命令名称
    
    Args:
        command_id: 命令 ID
    
    Returns:
        命令名称
    """
    try:
        return CommandID(command_id).name
    except ValueError:
        return f"UNKNOWN_0x{command_id:04X}"
