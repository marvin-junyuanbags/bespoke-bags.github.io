#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SEO URL修复脚本
修复HTML文件中JSON-LD结构化数据和OG标签中的URL格式问题
将反斜杠替换为正斜杠
"""

import os
import re
import glob
from pathlib import Path

def fix_html_file(file_path):
    """修复单个HTML文件中的URL格式"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = False
        
        # 修复JSON-LD中的URL
        json_ld_pattern = r'"url":\s*"(https://bespoke-bags\.com/[^"]*\\[^"]*)",'
        matches = re.findall(json_ld_pattern, content)
        
        for match in matches:
            fixed_url = match.replace('\\', '/')
            old_line = f'"url": "{match}",'
            new_line = f'"url": "{fixed_url}",'
            content = content.replace(old_line, new_line)
            changes_made = True
        
        # 修复OG URL标签
        og_url_pattern = r'<meta content="(https://bespoke-bags\.com/[^"]*\\[^"]*)" property="og:url"/>'
        og_matches = re.findall(og_url_pattern, content)
        
        for match in og_matches:
            fixed_url = match.replace('\\', '/')
            old_tag = f'<meta content="{match}" property="og:url"/>'
            new_tag = f'<meta content="{fixed_url}" property="og:url"/>'
            content = content.replace(old_tag, new_tag)
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

def check_seo_issues(file_path):
    """检查HTML文件的SEO问题"""
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查标题长度
        title_match = re.search(r'<title>([^<]+)</title>', content)
        if title_match:
            title = title_match.group(1)
            if len(title) > 60:
                issues.append(f'标题过长 ({len(title)} 字符): {title[:50]}...')
            elif len(title) < 30:
                issues.append(f'标题过短 ({len(title)} 字符): {title}')
        else:
            issues.append('缺少标题标签')
        
        # 检查描述长度
        desc_match = re.search(r'<meta content="([^"]+)" name="description"/>', content)
        if desc_match:
            description = desc_match.group(1)
            if len(description) > 160:
                issues.append(f'描述过长 ({len(description)} 字符): {description[:50]}...')
            elif len(description) < 120:
                issues.append(f'描述过短 ({len(description)} 字符): {description[:50]}...')
        else:
            issues.append('缺少描述标签')
        
        # 检查H1标签
        h1_matches = re.findall(r'<h1[^>]*>([^<]+)</h1>', content)
        if not h1_matches:
            issues.append('缺少H1标签')
        elif len(h1_matches) > 1:
            issues.append(f'H1标签过多 ({len(h1_matches)} 个)')
        
        # 检查图片alt属性
        img_without_alt = re.findall(r'<img(?![^>]*alt=)[^>]*>', content)
        if img_without_alt:
            issues.append(f'有 {len(img_without_alt)} 个图片缺少alt属性')
        
        return issues
        
    except Exception as e:
        return [f'检查文件时出错: {e}']

def main():
    """主函数"""
    base_dir = Path(__file__).parent
    
    print('开始修复SEO URL格式问题...')
    
    # 查找所有HTML文件
    html_files = []
    for pattern in ['*.html', 'blog/*.html', 'products/*.html', 'services/*.html', 'about/*.html', 'contact/*.html']:
        html_files.extend(glob.glob(str(base_dir / pattern)))
    
    print(f'找到 {len(html_files)} 个HTML文件')
    
    # 修复URL格式
    fixed_count = 0
    for html_file in html_files:
        if fix_html_file(html_file):
            fixed_count += 1
    
    print(f'\nURL格式修复完成！共修复了 {fixed_count} 个文件')
    
    # 检查SEO问题
    print('\n开始检查SEO问题...')
    seo_issues = {}
    
    for html_file in html_files[:10]:  # 只检查前10个文件作为示例
        issues = check_seo_issues(html_file)
        if issues:
            seo_issues[html_file] = issues
    
    if seo_issues:
        print('\n发现的SEO问题:')
        for file_path, issues in seo_issues.items():
            print(f'\n{os.path.basename(file_path)}:')
            for issue in issues:
                print(f'  - {issue}')
    else:
        print('\n未发现明显的SEO问题')

if __name__ == '__main__':
    main()