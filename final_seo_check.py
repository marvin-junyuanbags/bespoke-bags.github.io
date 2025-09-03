#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终SEO检查脚本
检查网站所有HTML文件的SEO优化情况
"""

import os
import re
from bs4 import BeautifulSoup
import json

def check_seo_issues(file_path):
    """检查单个HTML文件的SEO问题"""
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            soup = BeautifulSoup(content, 'html.parser')
            
        # 检查标题
        title = soup.find('title')
        if not title:
            issues.append("缺少title标签")
        elif len(title.get_text()) > 60:
            issues.append(f"标题过长({len(title.get_text())}字符)")
        elif len(title.get_text()) < 30:
            issues.append(f"标题过短({len(title.get_text())}字符)")
            
        # 检查描述
        description = soup.find('meta', attrs={'name': 'description'})
        if not description:
            issues.append("缺少meta description")
        elif len(description.get('content', '')) > 160:
            issues.append(f"描述过长({len(description.get('content', ''))}字符)")
        elif len(description.get('content', '')) < 120:
            issues.append(f"描述过短({len(description.get('content', ''))}字符)")
            
        # 检查H1标签
        h1_tags = soup.find_all('h1')
        if not h1_tags:
            issues.append("缺少H1标签")
        elif len(h1_tags) > 1:
            issues.append(f"H1标签过多({len(h1_tags)}个)")
            
        # 检查图片alt属性
        images = soup.find_all('img')
        missing_alt = 0
        for img in images:
            if not img.get('alt'):
                missing_alt += 1
        if missing_alt > 0:
            issues.append(f"{missing_alt}个图片缺少alt属性")
            
        # 检查canonical链接
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        if not canonical:
            issues.append("缺少canonical链接")
            
        # 检查OG标签
        og_title = soup.find('meta', attrs={'property': 'og:title'})
        og_description = soup.find('meta', attrs={'property': 'og:description'})
        og_image = soup.find('meta', attrs={'property': 'og:image'})
        og_url = soup.find('meta', attrs={'property': 'og:url'})
        
        if not og_title:
            issues.append("缺少og:title")
        if not og_description:
            issues.append("缺少og:description")
        if not og_image:
            issues.append("缺少og:image")
        if not og_url:
            issues.append("缺少og:url")
            
        # 检查Twitter卡片
        twitter_card = soup.find('meta', attrs={'name': 'twitter:card'})
        twitter_title = soup.find('meta', attrs={'name': 'twitter:title'})
        twitter_description = soup.find('meta', attrs={'name': 'twitter:description'})
        twitter_image = soup.find('meta', attrs={'name': 'twitter:image'})
        
        if not twitter_card:
            issues.append("缺少Twitter卡片")
        if not twitter_title:
            issues.append("缺少Twitter标题")
        if not twitter_description:
            issues.append("缺少Twitter描述")
        if not twitter_image:
            issues.append("缺少Twitter图片")
            
        # 检查结构化数据
        json_ld = soup.find('script', attrs={'type': 'application/ld+json'})
        if not json_ld:
            issues.append("缺少JSON-LD结构化数据")
        else:
            try:
                json.loads(json_ld.get_text())
            except json.JSONDecodeError:
                issues.append("JSON-LD格式错误")
                
    except Exception as e:
        issues.append(f"文件读取错误: {str(e)}")
        
    return issues

def main():
    """主函数"""
    base_dir = os.getcwd()
    total_files = 0
    files_with_issues = 0
    all_issues = {}
    
    print("开始最终SEO检查...")
    print("=" * 50)
    
    # 遍历所有HTML文件
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, base_dir)
                
                total_files += 1
                issues = check_seo_issues(file_path)
                
                if issues:
                    files_with_issues += 1
                    all_issues[rel_path] = issues
                    print(f"\n❌ {rel_path}:")
                    for issue in issues:
                        print(f"   - {issue}")
                else:
                    print(f"✅ {rel_path}: SEO优化良好")
    
    print("\n" + "=" * 50)
    print("SEO检查完成!")
    print(f"总文件数: {total_files}")
    print(f"有问题的文件: {files_with_issues}")
    print(f"SEO优化良好的文件: {total_files - files_with_issues}")
    
    if all_issues:
        print("\n需要关注的主要问题:")
        issue_counts = {}
        for issues in all_issues.values():
            for issue in issues:
                issue_type = issue.split('(')[0] if '(' in issue else issue
                issue_counts[issue_type] = issue_counts.get(issue_type, 0) + 1
        
        for issue, count in sorted(issue_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  - {issue}: {count}次")
    else:
        print("\n🎉 所有文件的SEO优化都很完善!")

if __name__ == "__main__":
    main()