#!/bin/bash

# ARF 启动脚本

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "❌ 虚拟环境不存在，请先运行: ./push.sh"
    exit 1
fi

# 激活虚拟环境并运行
echo "启动 ARF..."
source venv/bin/activate
python main.py
