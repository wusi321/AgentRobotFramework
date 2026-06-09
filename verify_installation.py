#!/usr/bin/env python3
"""
ARF Installation Verification Script
ARF 安装验证脚本
"""

import sys
import os
from pathlib import Path


def check_python_version():
    """检查 Python 版本"""
    version = sys.version_info
    print(f"Python 版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print("❌ Python 版本过低，需要 3.11+")
        return False
    
    print("✅ Python 版本符合要求")
    return True


def check_dependencies():
    """检查依赖包"""
    required = [
        'yaml',
        'loguru',
        'serial',
    ]
    
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"✅ {package} 已安装")
        except ImportError:
            print(f"❌ {package} 未安装")
            missing.append(package)
    
    if missing:
        print(f"\n缺少依赖: {', '.join(missing)}")
        print("请运行: pip install -r requirements.txt")
        return False
    
    return True


def check_directory_structure():
    """检查目录结构"""
    required_dirs = [
        'core',
        'protocol',
        'transport',
        'robot',
        'runtime',
        'skills',
        'config',
        'docs'
    ]
    
    required_files = [
        'main.py',
        'push.sh',
        'requirements.txt',
        'autoskill.md'
    ]
    
    all_good = True
    
    print("\n检查目录结构...")
    
    for dir_name in required_dirs:
        if Path(dir_name).exists():
            print(f"✅ {dir_name}/")
        else:
            print(f"❌ {dir_name}/ 缺失")
            all_good = False
    
    for file_name in required_files:
        if Path(file_name).exists():
            print(f"✅ {file_name}")
        else:
            print(f"❌ {file_name} 缺失")
            all_good = False
    
    return all_good


def check_config_files():
    """检查配置文件"""
    config_files = [
        'config/robot.yaml',
        'config/hardware.yaml',
        'config/stm32_config.yaml',
        'config/protocol.yaml',
        'config/permission.yaml'
    ]
    
    print("\n检查配置文件...")
    
    all_good = True
    
    for config_file in config_files:
        if Path(config_file).exists():
            print(f"✅ {config_file}")
        else:
            print(f"❌ {config_file} 缺失")
            all_good = False
    
    return all_good


def check_serial_ports():
    """检查串口设备"""
    print("\n检查串口设备...")
    
    serial_devices = [
        '/dev/ttyACM0',
        '/dev/ttyACM1',
        '/dev/ttyUSB0',
        '/dev/ttyUSB1'
    ]
    
    found = []
    
    for device in serial_devices:
        if Path(device).exists():
            print(f"✅ 发现串口: {device}")
            found.append(device)
    
    if not found:
        print("⚠️  未发现串口设备")
        print("   可能原因：")
        print("   1. STM32 未连接")
        print("   2. 权限不足（需要加入 dialout 组）")
        print("   3. 驱动未安装")
        return False
    
    return True


def test_import_modules():
    """测试导入模块"""
    print("\n测试模块导入...")
    
    modules = [
        ('core.logger', 'log'),
        ('core.config_loader', 'config_loader'),
        ('core.event_bus', 'event_bus'),
        ('core.state_manager', 'state_manager'),
        ('protocol.packet', 'Packet'),
        ('transport.uart_transport', 'UARTTransport'),
        ('robot.robot_api', 'RobotAPI'),
    ]
    
    all_good = True
    
    for module_name, obj_name in modules:
        try:
            module = __import__(module_name, fromlist=[obj_name])
            getattr(module, obj_name)
            print(f"✅ {module_name}.{obj_name}")
        except Exception as e:
            print(f"❌ {module_name}.{obj_name} - {e}")
            all_good = False
    
    return all_good


def main():
    """主函数"""
    print("=" * 50)
    print("  ARF 安装验证")
    print("=" * 50)
    
    checks = [
        ("Python 版本", check_python_version),
        ("依赖包", check_dependencies),
        ("目录结构", check_directory_structure),
        ("配置文件", check_config_files),
        ("串口设备", check_serial_ports),
        ("模块导入", test_import_modules),
    ]
    
    results = []
    
    for name, check_func in checks:
        print(f"\n{'='*50}")
        print(f"检查: {name}")
        print('='*50)
        result = check_func()
        results.append((name, result))
    
    # 总结
    print("\n" + "=" * 50)
    print("  验证结果总结")
    print("=" * 50)
    
    all_passed = True
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} - {name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    
    if all_passed:
        print("🎉 所有检查通过！")
        print("可以运行: python main.py")
    else:
        print("⚠️  部分检查未通过")
        print("请根据上述提示修复问题")
    
    print("=" * 50)


if __name__ == "__main__":
    main()
