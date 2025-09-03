#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片路径修复脚本
将HTML文件中缺失的jpg/png/svg图片引用替换为现有的webp图片
"""

import os
import re
import glob
from pathlib import Path

def get_available_webp_images(images_dir):
    """获取所有可用的webp图片文件"""
    webp_files = []
    for file in os.listdir(images_dir):
        if file.endswith('.webp'):
            webp_files.append(file)
    return sorted(webp_files)

def create_image_mapping(webp_files):
    """创建图片映射关系"""
    mapping = {}
    
    # 为常见的图片名称创建映射
    common_mappings = {
        'logo.png': 'bespoke-bags (1).webp',
        'logo.svg': 'bespoke-bags (1).webp',
        'handbags-hero.jpg': 'bespoke-bags (2).webp',
        'luxury-handbags.jpg': 'bespoke-bags (3).webp',
        'business-handbags.jpg': 'bespoke-bags (4).webp',
        'fashion-handbags.jpg': 'bespoke-bags (5).webp',
        'eco-handbags.jpg': 'bespoke-bags (6).webp',
        'backpacks-hero.jpg': 'bespoke-bags (7).webp',
        'hiking-backpacks.jpg': 'bespoke-bags (8).webp',
        'business-backpacks.jpg': 'bespoke-bags (9).webp',
        'travel-backpacks.jpg': 'bespoke-bags (10).webp',
        'school-backpacks.jpg': 'bespoke-bags (11).webp',
        'travel-bags-hero.jpg': 'bespoke-bags (12).webp',
        'carry-on-luggage.jpg': 'bespoke-bags (13).webp',
        'duffel-bags.jpg': 'bespoke-bags (14).webp',
        'rolling-luggage.jpg': 'bespoke-bags (15).webp',
        'garment-bags.jpg': 'bespoke-bags (16).webp',
        'business-travel.jpg': 'bespoke-bags (17).webp',
        'leisure-travel.jpg': 'bespoke-bags (18).webp',
        'adventure-travel.jpg': 'bespoke-bags (19).webp',
        'extended-travel.jpg': 'bespoke-bags (20).webp'
    }
    
    # 添加预定义的映射
    mapping.update(common_mappings)
    
    # 为其他图片创建自动映射
    webp_index = 21
    used_webp = set(common_mappings.values())
    
    return mapping, webp_index, used_webp

def fix_html_file(file_path, mapping, webp_files, webp_index, used_webp):
    """修复单个HTML文件中的图片路径"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = False
        
        # 查找所有图片引用
        img_pattern = r'src="([^"]*\.(jpg|jpeg|png|gif|svg))"'
        matches = re.findall(img_pattern, content)
        
        for match in matches:
            img_path = match[0]
            img_filename = os.path.basename(img_path)
            
            # 检查是否已有映射
            if img_filename in mapping:
                replacement = mapping[img_filename]
            else:
                # 为新图片创建映射
                while f'bespoke-bags ({webp_index}).webp' in used_webp and webp_index <= 131:
                    webp_index += 1
                
                if webp_index <= 131:
                    replacement = f'bespoke-bags ({webp_index}).webp'
                    mapping[img_filename] = replacement
                    used_webp.add(replacement)
                    webp_index += 1
                else:
                    # 如果没有更多webp文件，使用第一个
                    replacement = 'bespoke-bags (1).webp'
            
            # 构建新的路径
            img_dir = os.path.dirname(img_path)
            if img_dir:
                new_path = f'{img_dir}/{replacement}'
            else:
                new_path = replacement
            
            # 替换内容
            old_src = f'src="{img_path}"'
            new_src = f'src="{new_path}"'
            content = content.replace(old_src, new_src)
            changes_made = True
        
        # 如果有更改，写回文件
        if changes_made:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'✓ 修复了 {file_path}')
            return True
        else:
            return False
            
    except Exception as e:
        print(f'✗ 处理文件 {file_path} 时出错: {e}')
        return False

def main():
    """主函数"""
    base_dir = Path(__file__).parent
    images_dir = base_dir / 'images'
    
    print('开始修复图片路径...')
    
    # 获取所有webp图片
    webp_files = get_available_webp_images(images_dir)
    print(f'找到 {len(webp_files)} 个webp图片文件')
    
    # 创建映射关系
    mapping, webp_index, used_webp = create_image_mapping(webp_files)
    
    # 查找所有HTML文件
    html_files = []
    for pattern in ['*.html', 'blog/*.html', 'products/*.html', 'services/*.html', 'about/*.html', 'contact/*.html']:
        html_files.extend(glob.glob(str(base_dir / pattern)))
    
    print(f'找到 {len(html_files)} 个HTML文件')
    
    # 修复每个文件
    fixed_count = 0
    for html_file in html_files:
        if fix_html_file(html_file, mapping, webp_files, webp_index, used_webp):
            fixed_count += 1
    
    print(f'\n修复完成！共修复了 {fixed_count} 个文件')
    print(f'图片映射关系:')
    for original, replacement in sorted(mapping.items()):
        print(f'  {original} -> {replacement}')

if __name__ == '__main__':
    main()