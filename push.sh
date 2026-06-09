#!/bin/bash

echo "========================================="
echo "  ARF Installation Script"
echo "========================================="

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Detected Python version: $python_version"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate
echo "✓ Virtual environment activated"

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"

# Set environment variables
export ROBOT_CONFIG=config/robot.yaml
export STM32_CONFIG=config/stm32_config.yaml
export HARDWARE_CONFIG=config/hardware.yaml
export PROTOCOL_CONFIG=config/protocol.yaml

echo "✓ Environment variables set"

# Create necessary directories
mkdir -p logs
mkdir -p cache
mkdir -p skills/user_skill
echo "✓ Directories created"

# Auto-detect serial port
echo "Detecting serial ports..."
if [ -e /dev/ttyACM0 ]; then
    export STM32_PORT=/dev/ttyACM0
    echo "✓ Found STM32 at /dev/ttyACM0"
elif [ -e /dev/ttyUSB0 ]; then
    export STM32_PORT=/dev/ttyUSB0
    echo "✓ Found STM32 at /dev/ttyUSB0"
else
    echo "⚠ No serial port detected, please configure manually"
fi

echo "========================================="
echo "  Installation Complete!"
echo "========================================="
echo ""
echo "To activate the environment:"
echo "  source venv/bin/activate"
echo ""
echo "To run the framework:"
echo "  python main.py"
echo ""
