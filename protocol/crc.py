"""
ARF CRC Module
CRC 校验模块
"""


def crc16(data: bytes) -> int:
    """
    CRC16 校验
    
    Args:
        data: 数据字节流
    
    Returns:
        CRC16 校验值
    """
    crc = 0xFFFF
    polynomial = 0xA001
    
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc = (crc >> 1) ^ polynomial
            else:
                crc >>= 1
    
    return crc


def verify_crc16(data: bytes, expected_crc: int) -> bool:
    """
    验证 CRC16
    
    Args:
        data: 数据字节流
        expected_crc: 期望的 CRC 值
    
    Returns:
        校验是否通过
    """
    calculated_crc = crc16(data)
    return calculated_crc == expected_crc
