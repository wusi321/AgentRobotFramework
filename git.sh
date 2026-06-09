#!/bin/bash

# ARF Git 自动提交脚本
# 自动检测变更、添加、提交并推送到 GitHub

echo "========================================="
echo "  ARF Git Auto Commit Script"
echo "========================================="

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查是否在 Git 仓库中
if [ ! -d ".git" ]; then
    echo -e "${RED}❌ 错误: 当前目录不是 Git 仓库${NC}"
    exit 1
fi

# 检查 Git 状态
echo -e "\n${BLUE}[1/6] 检查 Git 状态...${NC}"
git status

# 检查是否有变更
if git diff-index --quiet HEAD --; then
    echo -e "${GREEN}✅ 工作区干净，没有需要提交的变更${NC}"
    
    # 检查是否需要推送
    LOCAL=$(git rev-parse @)
    REMOTE=$(git rev-parse @{u} 2>/dev/null)
    
    if [ "$LOCAL" = "$REMOTE" ]; then
        echo -e "${GREEN}✅ 本地和远程同步${NC}"
        exit 0
    else
        echo -e "${YELLOW}⚠️  本地有未推送的提交${NC}"
        read -p "是否推送到远程? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo -e "\n${BLUE}[推送中...]${NC}"
            git push
            if [ $? -eq 0 ]; then
                echo -e "${GREEN}✅ 推送成功!${NC}"
            else
                echo -e "${RED}❌ 推送失败${NC}"
                exit 1
            fi
        fi
        exit 0
    fi
fi

# 显示变更文件
echo -e "\n${BLUE}[2/6] 检测到以下变更:${NC}"
git status --short

# 询问是否继续
echo -e "\n${YELLOW}是否继续提交这些变更?${NC}"
read -p "(y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}⚠️  取消提交${NC}"
    exit 0
fi

# 添加所有变更
echo -e "\n${BLUE}[3/6] 添加文件到暂存区...${NC}"
git add .

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ 添加文件失败${NC}"
    exit 1
fi

echo -e "${GREEN}✅ 文件已添加${NC}"

# 获取提交信息
echo -e "\n${BLUE}[4/6] 输入提交信息${NC}"
echo -e "${YELLOW}提示: 按 Enter 使用默认提交信息${NC}"
echo -e "默认信息: Update project files - $(date '+%Y-%m-%d %H:%M:%S')"
read -p "提交信息: " commit_message

# 使用默认提交信息
if [ -z "$commit_message" ]; then
    commit_message="Update project files - $(date '+%Y-%m-%d %H:%M:%S')"
fi

# 提交
echo -e "\n${BLUE}[5/6] 提交变更...${NC}"
git commit -m "$commit_message"

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ 提交失败${NC}"
    exit 1
fi

echo -e "${GREEN}✅ 提交成功${NC}"

# 推送到远程
echo -e "\n${BLUE}[6/6] 推送到远程仓库...${NC}"

# 获取当前分支
branch=$(git symbolic-ref --short HEAD)

# 推送
git push origin $branch

if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}=========================================${NC}"
    echo -e "${GREEN}  ✅ 所有操作完成!${NC}"
    echo -e "${GREEN}=========================================${NC}"
    echo -e "${GREEN}提交信息: $commit_message${NC}"
    echo -e "${GREEN}分支: $branch${NC}"
    echo -e "${GREEN}GitHub: https://github.com/wusi321/AgentRobotFramework${NC}"
else
    echo -e "${RED}❌ 推送失败${NC}"
    echo -e "${YELLOW}提示: 检查网络连接和 SSH 密钥配置${NC}"
    exit 1
fi
