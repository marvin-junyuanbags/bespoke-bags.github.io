#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SEO质量检查脚本
检查所有HTML文件的SEO元素完整性
"""

import os
import re
from bs4 import BeautifulSoup
import json

def check_seo_elements(file_path):
    """检查单个HTML文件的SEO元素"""
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            soup = BeautifulSoup(content, 'html.parser')
        
        # 检查基本SEO元素
        title = soup.find('title')
        if not title or len(title.get_text().strip()) < 10:
            issues.append("标题缺失或过短")
        elif len(title.get_text().strip()) > 60:
            issues.append("标题过长（>60字符）")
        
        # 检查meta描述
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if not meta_desc or len(meta_desc.get('content', '').strip()) < 120:
            issues.append("Meta描述缺失或过短")
        elif len(meta_desc.get('content', '').strip()) > 160:
            issues.append("Meta描述过长（>160字符）")
        
        # 检查关键词
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        if not meta_keywords:
            issues.append("Meta关键词缺失")
        
        # 检查canonical链接
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        if not canonical:
            issues.append("Canonical链接缺失")
        
        # 检查Open Graph标签
        og_title = soup.find('meta', attrs={'property': 'og:title'})
        og_desc = soup.find('meta', attrs={'property': 'og:description'})
        og_image = soup.find('meta', attrs={'property': 'og:image'})
        
        if not og_title:
            issues.append("OG标题缺失")
        if not og_desc:
            issues.append("OG描述缺失")
        if not og_image:
            issues.append("OG图片缺失")
        
        # 检查Twitter卡片
        twitter_card = soup.find('meta', attrs={'name': 'twitter:card'})
        if not twitter_card:
            issues.append("Twitter卡片缺失")
        
        # 检查结构化数据
        structured_data = soup.find('script', attrs={'type': 'application/ld+json'})
        if not structured_data:
            issues.append("结构化数据缺失")
        else:
            try:
                json.loads(structured_data.get_text())
            except json.JSONDecodeError:
                issues.append("结构化数据格式错误")
        
        # 检查H1标签
        h1_tags = soup.find_all('h1')
        if len(h1_tags) == 0:
            issues.append("H1标签缺失")
        elif len(h1_tags) > 1:
            issues.append("多个H1标签")
        
        # 检查图片alt属性
        images = soup.find_all('img')
        images_without_alt = [img for img in images if not img.get('alt')]
        if images_without_alt:
            issues.append(f"{len(images_without_alt)}张图片缺少alt属性")
        
        # 检查内部链接
        internal_links = soup.find_all('a', href=True)
        broken_links = []
        for link in internal_links:
            href = link.get('href')
            if href.startswith('../') or href.startswith('./'):
                # 检查相对链接是否存在
                link_path = os.path.normpath(os.path.join(os.path.dirname(file_path), href))
                if not os.path.exists(link_path):
                    broken_links.append(href)
        
        if broken_links:
            issues.append(f"发现{len(broken_links)}个损坏的内部链接")
        
    except Exception as e:
        issues.append(f"文件读取错误: {str(e)}")
    
    return issues

def main():
    """主函数"""
    blog_dir = 'blog'
    results = {}
    total_files = 0
    files_with_issues = 0
    
    print("开始SEO质量检查...\n")
    
    # 检查博客目录下的所有HTML文件
    for filename in os.listdir(blog_dir):
        if filename.endswith('.html') and filename != 'index.html':
            file_path = os.path.join(blog_dir, filename)
            total_files += 1
            
            issues = check_seo_elements(file_path)
            
            if issues:
                files_with_issues += 1
                results[filename] = issues
                print(f"❌ {filename}:")
                for issue in issues:
                    print(f"   - {issue}")
                print()
            else:
                print(f"✅ {filename}: 所有SEO元素正常")
    
    # 输出总结
    print(f"\n=== SEO检查总结 ===")
    print(f"总文件数: {total_files}")
    print(f"有问题的文件: {files_with_issues}")
    print(f"通过率: {((total_files - files_with_issues) / total_files * 100):.1f}%")
    
    if results:
        print(f"\n需要修复的问题:")
        all_issues = []
        for issues in results.values():
            all_issues.extend(issues)
        
        issue_counts = {}
        for issue in all_issues:
            issue_counts[issue] = issue_counts.get(issue, 0) + 1
        
        for issue, count in sorted(issue_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  - {issue}: {count}次")
    
    return len(results) == 0

if __name__ == '__main__':
    success = main()
    if success:
        print("\n🎉 所有文件SEO检查通过！")
    else:
        print("\n⚠️  发现SEO问题，请查看上述报告进行修复。")