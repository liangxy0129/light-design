#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动更新 index.html 中的图片列表
使用方法：python3 update.py
"""

import os
import re
from pathlib import Path

# 获取脚本所在目录
script_dir = Path(__file__).parent

# 图片文件夹路径
image_dir = script_dir / 'standard-pic'

# 获取所有图片文件
image_extensions = ('.png', '.jpg', '.jpeg')
if image_dir.exists():
    # 如果 standard-pic 文件夹存在，从该文件夹扫描
    image_files = sorted([
        f'standard-pic/{f.name}' for f in image_dir.iterdir()
        if f.is_file() and f.suffix.lower() in image_extensions
    ])
else:
    # 兼容旧版本，从根目录扫描
    image_files = sorted([
        f.name for f in script_dir.iterdir()
        if f.is_file() and f.suffix.lower() in image_extensions
    ])

# 读取 index.html
html_file = script_dir / 'index.html'
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# 生成新的 imageFiles 数组
image_list = ',\n            '.join([f"'{img}'" for img in image_files])
new_image_files = f"""// 图片文件列表（自动生成，请勿手动修改）
        const imageFiles = [
            {image_list}
        ];"""

# 替换 imageFiles 数组 - 使用更精确的正则表达式
pattern = r'// 图片文件列表（自动生成，请勿手动修改）\s*const imageFiles = \[[^\]]*\];'
if re.search(pattern, html_content, flags=re.DOTALL):
    new_content = re.sub(
        pattern,
        new_image_files,
        html_content,
        flags=re.DOTALL
    )

    # 写回文件
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print("✅ 图片列表已更新！共找到以下图片：")
    for img in image_files:
        print(f"  - {img}")
else:
    print("❌ 错误：无法找到图片列表位置")
    print("请确保 index.html 文件格式正确")
