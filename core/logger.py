"""
ARF Logger Module
统一日志管理
"""

from loguru import logger
import sys
from pathlib import Path


class ARFLogger:
    """ARF 日志管理器"""
    
    def __init__(self, log_dir="logs", level="INFO"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.level = level
        self._setup_logger()
    
    def _setup_logger(self):
        """配置 logger"""
        # 移除默认 handler
        logger.remove()
        
        # 添加控制台输出
        logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
            level=self.level,
            colorize=True
        )
        
        # 添加文件输出
        logger.add(
            self.log_dir / "arf_{time:YYYY-MM-DD}.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}",
            level=self.level,
            rotation="00:00",
            retention="7 days",
            compression="zip"
        )
        
        # 添加错误日志文件
        logger.add(
            self.log_dir / "arf_error_{time:YYYY-MM-DD}.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}",
            level="ERROR",
            rotation="00:00",
            retention="30 days",
            compression="zip"
        )
    
    def get_logger(self):
        """获取 logger 实例"""
        return logger


# 全局 logger 实例
arf_logger = ARFLogger()
log = arf_logger.get_logger()
