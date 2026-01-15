#!/bin/bash

# 自动更新 index.html 中的图片列表
# 使用方法：在终端中运行 bash update.sh

cd "$(dirname "$0")"

# 获取所有图片文件
images=$(ls -1 | grep -E '\.(png|jpg|jpeg)$' | sed "s/.*/'&',/")

# 创建临时文件
temp_file=$(mktemp)

# 读取 index.html 并替换 imageFiles 数组
awk -v images="$images" '
    /const imageFiles = \[/ {
        print "        // 图片文件列表（自动生成，请勿手动修改）"
        print "        const imageFiles = ["
        print images | "cat"
        close("cat")
        print "        ];"
        skip = 1
        next
    }
    /\];/ && skip {
        skip = 0
        next
    }
    !skip { print }
' index.html > "$temp_file"

# 替换原文件
mv "$temp_file" index.html

echo "✅ 图片列表已更新！共找到以下图片："
ls -1 | grep -E '\.(png|jpg|jpeg)$'
