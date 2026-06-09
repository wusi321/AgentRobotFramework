"""
ARF Config Loader
配置文件加载器
"""

import yaml
from pathlib import Path
from typing import Dict, Any
from core.logger import log


class ConfigLoader:
    """配置加载器"""
    
    def __init__(self, config_dir="config"):
        self.config_dir = Path(config_dir)
        self.configs = {}
    
    def load(self, config_name: str) -> Dict[str, Any]:
        """
        加载配置文件
        
        Args:
            config_name: 配置文件名（不含扩展名）
        
        Returns:
            配置字典
        """
        config_path = self.config_dir / f"{config_name}.yaml"
        
        if not config_path.exists():
            log.warning(f"配置文件不存在: {config_path}")
            return {}
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                self.configs[config_name] = config
                log.info(f"✓ 加载配置: {config_name}")
                return config
        except Exception as e:
            log.error(f"加载配置失败 {config_name}: {e}")
            return {}
    
    def load_all(self):
        """加载所有配置文件"""
        config_files = [
            "robot",
            "hardware",
            "stm32_config",
            "protocol",
            "permission"
        ]
        
        for config_name in config_files:
            self.load(config_name)
        
        log.info("✓ 所有配置加载完成")
    
    def get(self, config_name: str, key: str = None, default=None):
        """
        获取配置值
        
        Args:
            config_name: 配置文件名
            key: 配置键（支持 . 分隔的嵌套键）
            default: 默认值
        
        Returns:
            配置值
        """
        if config_name not in self.configs:
            self.load(config_name)
        
        config = self.configs.get(config_name, {})
        
        if key is None:
            return config
        
        # 支持嵌套键访问 如 "robot.name"
        keys = key.split('.')
        value = config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        
        return value if value is not None else default
    
    def reload(self, config_name: str):
        """重新加载配置"""
        log.info(f"重新加载配置: {config_name}")
        return self.load(config_name)


# 全局配置加载器
config_loader = ConfigLoader()
