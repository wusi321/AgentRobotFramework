#!/bin/bash

# ARF Git 高级管理脚本
# 提供多种 Git 操作选项

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# 显示菜单
show_menu() {
    clear
    echo -e "${CYAN}=========================================${NC}"
    echo -e "${CYAN}  ARF Git 管理工具${NC}"
    echo -e "${CYAN}=========================================${NC}"
    echo ""
    echo -e "${GREEN}1.${NC} 快速提交并推送 (add + commit + push)"
    echo -e "${GREEN}2.${NC} 查看状态 (git status)"
    echo -e "${GREEN}3.${NC} 查看提交历史 (git log)"
    echo -e "${GREEN}4.${NC} 查看变更差异 (git diff)"
    echo -e "${GREEN}5.${NC} 拉取远程更新 (git pull)"
    echo -e "${GREEN}6.${NC} 推送到远程 (git push)"
    echo -e "${GREEN}7.${NC} 创建新分支"
    echo -e "${GREEN}8.${NC} 切换分支"
    echo -e "${GREEN}9.${NC} 撤销最后一次提交"
    echo -e "${GREEN}10.${NC} 放弃工作区修改"
    echo -e "${YELLOW}0.${NC} 退出"
    echo ""
    echo -e "${CYAN}=========================================${NC}"
}

# 快速提交并推送
quick_commit() {
    echo -e "\n${BLUE}[快速提交模式]${NC}\n"
    
    # 检查状态
    if git diff-index --quiet HEAD --; then
        echo -e "${GREEN}✅ 工作区干净${NC}"
        return
    fi
    
    # 显示变更
    echo -e "${BLUE}变更的文件:${NC}"
    git status --short
    echo ""
    
    # 输入提交信息
    read -p "提交信息 (留空使用默认): " msg
    if [ -z "$msg" ]; then
        msg="Update - $(date '+%Y-%m-%d %H:%M')"
    fi
    
    # 执行提交
    git add .
    git commit -m "$msg"
    
    # 推送
    branch=$(git symbolic-ref --short HEAD)
    git push origin $branch
    
    if [ $? -eq 0 ]; then
        echo -e "\n${GREEN}✅ 提交并推送成功!${NC}"
    else
        echo -e "\n${RED}❌ 推送失败${NC}"
    fi
}

# 查看状态
show_status() {
    echo -e "\n${BLUE}[Git 状态]${NC}\n"
    git status
}

# 查看日志
show_log() {
    echo -e "\n${BLUE}[提交历史]${NC}\n"
    git log --oneline --graph --decorate --all -n 10
}

# 查看差异
show_diff() {
    echo -e "\n${BLUE}[工作区变更]${NC}\n"
    git diff
}

# 拉取更新
pull_updates() {
    echo -e "\n${BLUE}[拉取远程更新]${NC}\n"
    git pull
    if [ $? -eq 0 ]; then
        echo -e "\n${GREEN}✅ 拉取成功${NC}"
    else
        echo -e "\n${RED}❌ 拉取失败${NC}"
    fi
}

# 推送
push_changes() {
    echo -e "\n${BLUE}[推送到远程]${NC}\n"
    branch=$(git symbolic-ref --short HEAD)
    git push origin $branch
    if [ $? -eq 0 ]; then
        echo -e "\n${GREEN}✅ 推送成功${NC}"
    else
        echo -e "\n${RED}❌ 推送失败${NC}"
    fi
}

# 创建分支
create_branch() {
    echo -e "\n${BLUE}[创建新分支]${NC}\n"
    read -p "新分支名称: " branch_name
    if [ -z "$branch_name" ]; then
        echo -e "${RED}❌ 分支名不能为空${NC}"
        return
    fi
    
    git checkout -b $branch_name
    if [ $? -eq 0 ]; then
        echo -e "\n${GREEN}✅ 分支 '$branch_name' 创建成功${NC}"
    else
        echo -e "\n${RED}❌ 创建分支失败${NC}"
    fi
}

# 切换分支
switch_branch() {
    echo -e "\n${BLUE}[切换分支]${NC}\n"
    echo "可用分支:"
    git branch
    echo ""
    read -p "切换到分支: " branch_name
    if [ -z "$branch_name" ]; then
        return
    fi
    
    git checkout $branch_name
    if [ $? -eq 0 ]; then
        echo -e "\n${GREEN}✅ 已切换到 '$branch_name'${NC}"
    else
        echo -e "\n${RED}❌ 切换失败${NC}"
    fi
}

# 撤销最后一次提交
undo_commit() {
    echo -e "\n${BLUE}[撤销最后一次提交]${NC}\n"
    echo -e "${YELLOW}⚠️  这将撤销最后一次提交，但保留文件修改${NC}"
    read -p "确认撤销? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git reset --soft HEAD~1
        echo -e "${GREEN}✅ 已撤销最后一次提交${NC}"
    fi
}

# 放弃工作区修改
discard_changes() {
    echo -e "\n${BLUE}[放弃工作区修改]${NC}\n"
    echo -e "${RED}⚠️  警告: 这将丢失所有未提交的修改!${NC}"
    read -p "确认放弃所有修改? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git reset --hard HEAD
        git clean -fd
        echo -e "${GREEN}✅ 已放弃所有修改${NC}"
    fi
}

# 主循环
main() {
    while true; do
        show_menu
        read -p "请选择操作 [0-10]: " choice
        
        case $choice in
            1) quick_commit ;;
            2) show_status ;;
            3) show_log ;;
            4) show_diff ;;
            5) pull_updates ;;
            6) push_changes ;;
            7) create_branch ;;
            8) switch_branch ;;
            9) undo_commit ;;
            10) discard_changes ;;
            0) 
                echo -e "\n${GREEN}再见!${NC}\n"
                exit 0
                ;;
            *)
                echo -e "\n${RED}无效选择${NC}"
                ;;
        esac
        
        echo ""
        read -p "按 Enter 继续..."
    done
}

# 检查是否在 Git 仓库中
if [ ! -d ".git" ]; then
    echo -e "${RED}❌ 错误: 当前目录不是 Git 仓库${NC}"
    exit 1
fi

# 运行主程序
main
