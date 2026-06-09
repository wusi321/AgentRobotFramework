"""
ARF Skill Runtime
技能运行时管理
"""

import yaml
import importlib.util
from pathlib import Path
from typing import Dict, Any, Optional
from core.logger import log


class SkillRuntime:
    """技能运行时"""
    
    def __init__(self, robot_api, skills_dir="skills"):
        self.robot_api = robot_api
        self.skills_dir = Path(skills_dir)
        self.skills: Dict[str, Any] = {}
        self.skill_configs: Dict[str, Dict] = {}
    
    def load_all_skills(self):
        """加载所有技能"""
        if not self.skills_dir.exists():
            log.warning(f"技能目录不存在: {self.skills_dir}")
            return
        
        for skill_dir in self.skills_dir.iterdir():
            if skill_dir.is_dir():
                self.load_skill(skill_dir.name)
        
        log.info(f"✓ 加载了 {len(self.skills)} 个技能")
    
    def load_skill(self, skill_name: str) -> bool:
        """
        加载单个技能
        
        Args:
            skill_name: 技能名称
        
        Returns:
            是否成功
        """
        skill_path = self.skills_dir / skill_name
        
        if not skill_path.exists():
            log.error(f"技能不存在: {skill_name}")
            return False
        
        try:
            # 加载配置
            config_file = skill_path / "skill.yaml"
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    self.skill_configs[skill_name] = config
            
            # 加载 Python 模块
            skill_file = skill_path / "skill.py"
            if skill_file.exists():
                spec = importlib.util.spec_from_file_location(skill_name, skill_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # 实例化技能类（假设类名为 XxxSkill）
                class_name = ''.join(word.capitalize() for word in skill_name.split('_')) + 'Skill'
                skill_class = getattr(module, class_name)
                skill_instance = skill_class(self.robot_api)
                
                # 初始化技能
                skill_instance.init()
                
                self.skills[skill_name] = skill_instance
                log.info(f"✓ 加载技能: {skill_name}")
                return True
            
        except Exception as e:
            log.error(f"加载技能失败 {skill_name}: {e}")
        
        return False
    
    def execute_skill(self, skill_name: str, **kwargs) -> Optional[Dict]:
        """
        执行技能
        
        Args:
            skill_name: 技能名称
            **kwargs: 技能参数
        
        Returns:
            执行结果
        """
        if skill_name not in self.skills:
            log.error(f"技能不存在: {skill_name}")
            return None
        
        skill = self.skills[skill_name]
        
        try:
            log.info(f"执行技能: {skill_name}")
            result = skill.run(**kwargs)
            return result
        except Exception as e:
            log.error(f"技能执行失败 {skill_name}: {e}")
            return None
    
    def stop_skill(self, skill_name: str):
        """停止技能"""
        if skill_name in self.skills:
            self.skills[skill_name].stop()
            log.info(f"停止技能: {skill_name}")
    
    def get_skill_config(self, skill_name: str) -> Optional[Dict]:
        """获取技能配置"""
        return self.skill_configs.get(skill_name)
    
    def list_skills(self) -> list:
        """列出所有技能"""
        return list(self.skills.keys())
