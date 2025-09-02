#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网站质量检查脚本
检查网站的整体质量、性能和可用性
"""

import os
import re
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin, urlparse

def check_page_performance(file_path):
    """检查页面性能相关指标"""
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            soup = BeautifulSoup(content, 'html.parser')
        
        # 检查CSS文件数量
        css_links = soup.find_all('link', rel='stylesheet')
        if len(css_links) > 3:
            issues.append(f"CSS文件过多({len(css_links)}个)，可能影响加载速度")
        
        # 检查JavaScript文件
        js_scripts = soup.find_all('script', src=True)
        if len(js_scripts) > 5:
            issues.append(f"JavaScript文件过多({len(js_scripts)}个)")
        
        # 检查图片优化
        images = soup.find_all('img')
        large_images = []
        for img in images:
            src = img.get('src', '')
            if src and not src.endswith('.webp') and not src.startswith('data:'):
                if any(ext in src.lower() for ext in ['.jpg', '.jpeg', '.png']):
                    large_images.append(src)
        
        if large_images:
            issues.append(f"发现{len(large_images)}张未优化图片(非WebP格式)")
        
        # 检查内联样式
        inline_styles = soup.find_all(attrs={'style': True})
        if len(inline_styles) > 10:
            issues.append(f"内联样式过多({len(inline_styles)}个)，建议移至CSS文件")
        
    except Exception as e:
        issues.append(f"性能检查错误: {str(e)}")
    
    return issues

def check_accessibility(file_path):
    """检查可访问性"""
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            soup = BeautifulSoup(content, 'html.parser')
        
        # 检查图片alt属性
        images = soup.find_all('img')
        missing_alt = [img for img in images if not img.get('alt')]
        if missing_alt:
            issues.append(f"{len(missing_alt)}张图片缺少alt属性")
        
        # 检查表单标签
        inputs = soup.find_all(['input', 'textarea', 'select'])
        unlabeled_inputs = []
        for inp in inputs:
            input_id = inp.get('id')
            if input_id:
                label = soup.find('label', attrs={'for': input_id})
                if not label:
                    unlabeled_inputs.append(input_id)
            elif not inp.get('aria-label') and not inp.get('placeholder'):
                unlabeled_inputs.append('unnamed')
        
        if unlabeled_inputs:
            issues.append(f"{len(unlabeled_inputs)}个表单元素缺少标签")
        
        # 检查标题层级
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        if headings:
            heading_levels = [int(h.name[1]) for h in headings]
            for i in range(1, len(heading_levels)):
                if heading_levels[i] - heading_levels[i-1] > 1:
                    issues.append("标题层级跳跃，影响可访问性")
                    break
        
        # 检查链接文本
        links = soup.find_all('a')
        generic_links = []
        for link in links:
            text = link.get_text().strip().lower()
            if text in ['click here', 'read more', 'more', 'here', '点击这里', '更多', '阅读更多']:
                generic_links.append(text)
        
        if generic_links:
            issues.append(f"{len(generic_links)}个链接使用了通用文本")
        
    except Exception as e:
        issues.append(f"可访问性检查错误: {str(e)}")
    
    return issues

def check_content_quality(file_path):
    """检查内容质量"""
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            soup = BeautifulSoup(content, 'html.parser')
        
        # 提取主要内容
        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile(r'content|post|article'))
        
        if main_content:
            text_content = main_content.get_text().strip()
            word_count = len(text_content.split())
            
            if word_count < 300:
                issues.append(f"内容过短({word_count}词)，建议至少300词")
            elif word_count > 3000:
                issues.append(f"内容过长({word_count}词)，考虑分页")
            
            # 检查段落长度
            paragraphs = main_content.find_all('p')
            long_paragraphs = [p for p in paragraphs if len(p.get_text().split()) > 100]
            if long_paragraphs:
                issues.append(f"{len(long_paragraphs)}个段落过长，影响阅读体验")
            
            # 检查列表使用
            lists = main_content.find_all(['ul', 'ol'])
            if word_count > 500 and len(lists) == 0:
                issues.append("长文章建议使用列表提高可读性")
        
        # 检查重复内容
        title = soup.find('title')
        h1 = soup.find('h1')
        if title and h1:
            title_text = title.get_text().strip()
            h1_text = h1.get_text().strip()
            if title_text.lower() == h1_text.lower():
                issues.append("标题和H1完全相同，建议有所区别")
        
    except Exception as e:
        issues.append(f"内容质量检查错误: {str(e)}")
    
    return issues

def check_mobile_friendliness(file_path):
    """检查移动端友好性"""
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            soup = BeautifulSoup(content, 'html.parser')
        
        # 检查viewport meta标签
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        if not viewport:
            issues.append("缺少viewport meta标签")
        else:
            viewport_content = viewport.get('content', '')
            if 'width=device-width' not in viewport_content:
                issues.append("viewport设置不正确")
        
        # 检查固定宽度元素
        style_tags = soup.find_all('style')
        inline_styles = soup.find_all(attrs={'style': True})
        
        fixed_width_pattern = re.compile(r'width\s*:\s*\d+px')
        for tag in style_tags + inline_styles:
            style_content = tag.get('style', '') if hasattr(tag, 'get') else str(tag)
            if fixed_width_pattern.search(style_content):
                issues.append("发现固定像素宽度，可能影响移动端显示")
                break
        
        # 检查字体大小
        small_font_pattern = re.compile(r'font-size\s*:\s*(\d+)px')
        for tag in style_tags + inline_styles:
            style_content = tag.get('style', '') if hasattr(tag, 'get') else str(tag)
            matches = small_font_pattern.findall(style_content)
            for match in matches:
                if int(match) < 14:
                    issues.append("字体过小，移动端可读性差")
                    break
        
    except Exception as e:
        issues.append(f"移动端检查错误: {str(e)}")
    
    return issues

def check_single_file(file_path):
    """检查单个文件的所有质量指标"""
    all_issues = {
        'performance': check_page_performance(file_path),
        'accessibility': check_accessibility(file_path),
        'content': check_content_quality(file_path),
        'mobile': check_mobile_friendliness(file_path)
    }
    
    return all_issues

def main():
    """主函数"""
    directories_to_check = ['blog']
    total_files = 0
    files_with_issues = 0
    all_issues = {
        'performance': [],
        'accessibility': [],
        'content': [],
        'mobile': []
    }
    
    print("开始网站质量检查...\n")
    
    for directory in directories_to_check:
        if not os.path.exists(directory):
            continue
            
        for filename in os.listdir(directory):
            if filename.endswith('.html'):
                file_path = os.path.join(directory, filename)
                total_files += 1
                
                file_issues = check_single_file(file_path)
                
                has_issues = any(issues for issues in file_issues.values())
                
                if has_issues:
                    files_with_issues += 1
                    print(f"⚠️  {filename}:")
                    
                    for category, issues in file_issues.items():
                        if issues:
                            print(f"  {category.upper()}:")
                            for issue in issues:
                                print(f"    - {issue}")
                                all_issues[category].append(issue)
                    print()
                else:
                    print(f"✅ {filename}: 质量检查通过")
    
    # 输出总结
    print(f"\n=== 网站质量检查总结 ===")
    print(f"总文件数: {total_files}")
    print(f"有问题的文件: {files_with_issues}")
    print(f"通过率: {((total_files - files_with_issues) / total_files * 100):.1f}%")
    
    print(f"\n=== 问题分类统计 ===")
    for category, issues in all_issues.items():
        if issues:
            print(f"\n{category.upper()} ({len(issues)}个问题):")
            issue_counts = {}
            for issue in issues:
                issue_counts[issue] = issue_counts.get(issue, 0) + 1
            
            for issue, count in sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"  - {issue}: {count}次")
    
    return files_with_issues == 0

if __name__ == '__main__':
    success = main()
    if success:
        print("\n🎉 网站质量检查全部通过！")
    else:
        print("\n📋 网站质量检查完成，请查看上述报告。")