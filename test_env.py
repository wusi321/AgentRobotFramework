#!/usr/bin/env python3
"""
快速环境测试
"""

import sys

print("=" * 50)
print("  ARF 环境测试")
print("=" * 50)

# 测试 Python 版本
print(f"\nPython 版本: {sys.version}")

# 测试模块导入
modules = [
    'yaml',
    'loguru',
    'serial',
]

print("\n模块测试：")
for mod in modules:
    try:
        __import__(mod)
        print(f"  ✅ {mod}")
    except ImportError as e:
        print(f"  ❌ {mod} - {e}")

# 测试 ARF 模块
print("\nARF 模块测试：")
arf_modules = [
    'core.logger',
    'core.config_loader',
    'core.event_bus',
    'protocol.packet',
    'transport.uart_transport',
]

for mod in arf_modules:
    try:
        __import__(mod)
        print(f"  ✅ {mod}")
    except Exception as e:
        print(f"  ❌ {mod} - {e}")

print("\n" + "=" * 50)
print("测试完成！")
print("如果有 ❌，请检查虚拟环境是否激活")
print("=" * 50)
