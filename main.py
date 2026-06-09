#!/usr/bin/env python3
"""
ARF Main Entry Point
ARF 主程序入口
"""

import sys
import os

# 检查虚拟环境
if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
    print("=" * 60)
    print("⚠️  警告：未在虚拟环境中运行")
    print("=" * 60)
    print("\n请先激活虚拟环境：")
    print("  source venv/bin/activate")
    print("\n然后再运行：")
    print("  python main.py")
    print("\n或直接使用：")
    print("  ./venv/bin/python main.py")
    print("=" * 60)
    sys.exit(1)

from core.runtime import Runtime
from core.logger import log
import time


def main():
    """主函数"""
    log.info("Agent Robot Framework (ARF) v0.1.0")
    
    # 创建运行时
    runtime = Runtime()
    
    # 启动
    if not runtime.start():
        log.error("启动失败")
        return
    
    try:
        # 演示：执行 walk 技能
        log.info("\n" + "=" * 50)
        log.info("  运行演示程序")
        log.info("=" * 50)
        
        time.sleep(2)
        
        # 获取系统状态
        status = runtime.get_status()
        log.info(f"系统状态: {status}")
        
        # 执行 walk 技能
        log.info("\n执行 walk 技能...")
        result = runtime.execute_skill(
            "walk",
            speed=0.5,
            direction="forward",
            duration=5.0
        )
        log.info(f"执行结果: {result}")
        
        # 保持运行
        log.info("\n系统运行中，按 Ctrl+C 停止...")
        while runtime.running:
            time.sleep(1)
    
    except KeyboardInterrupt:
        log.info("\n收到停止信号")
    
    finally:
        runtime.stop()


if __name__ == "__main__":
    main()
