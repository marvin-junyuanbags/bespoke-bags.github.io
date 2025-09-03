#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查找有SEO问题的文件 - bespoke-bags.com
"""

import os
from bs4 import BeautifulSoup

def check_seo_issues(file_path):
    """检查单个HTML文件的SEO问题"""
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # 检查基本SEO元素
        title = soup.find('title')
        if not title or not title.get_text().strip():
            issues.append('缺少title标签')
        elif len(title.get_text().strip()) > 60:
            issues.append('标题过长')
        elif len(title.get_text().strip()) < 30:
            issues.append('标题过短')
        
        # 检查meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if not meta_desc or not meta_desc.get('content', '').strip():
            issues.append('缺少meta description')
        elif len(meta_desc.get('content', '').strip()) > 160:
            issues.append('描述过长')
        elif len(meta_desc.get('content', '').strip()) < 120:
            issues.append('描述过短')
        
        # 检查H1标签
        h1_tags = soup.find_all('h1')
        if not h1_tags:
            issues.append('缺少H1标签')
        elif len(h1_tags) > 1:
            issues.append('H1标签过多')
        
        # 检查canonical链接
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        if not canonical:
            issues.append('缺少canonical链接')
        
        # 检查viewport设置
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        if not viewport:
            issues.append('缺少viewport设置')
        
        # 检查meta keywords
        keywords = soup.find('meta', attrs={'name': 'keywords'})
        if not keywords or not keywords.get('content', '').strip():
            issues.append('缺少meta keywords')
        
        # 检查Open Graph标签
        og_title = soup.find('meta', attrs={'property': 'og:title'})
        og_desc = soup.find('meta', attrs={'property': 'og:description'})
        og_url = soup.find('meta', attrs={'property': 'og:url'})
        og_image = soup.find('meta', attrs={'property': 'og:image'})
        
        if not og_title:
            issues.append('缺少og:title')
        if not og_desc:
            issues.append('缺少og:description')
        if not og_url:
            issues.append('缺少og:url')
        if not og_image:
            issues.append('缺少og:image')
        
        # 检查Twitter Card标签
        twitter_card = soup.find('meta', attrs={'name': 'twitter:card'})
        twitter_title = soup.find('meta', attrs={'name': 'twitter:title'})
        twitter_desc = soup.find('meta', attrs={'name': 'twitter:description'})
        twitter_image = soup.find('meta', attrs={'name': 'twitter:image'})
        
        if not twitter_card:
            issues.append('缺少Twitter卡片')
        if not twitter_title:
            issues.append('缺少Twitter标题')
        if not twitter_desc:
            issues.append('缺少Twitter描述')
        if not twitter_image:
            issues.append('缺少Twitter图片')
        
        # 检查JSON-LD结构化数据
        json_ld = soup.find('script', attrs={'type': 'application/ld+json'})
        if not json_ld:
            issues.append('缺少JSON-LD结构化数据')
        
    except Exception as e:
        issues.append(f'文件读取错误: {str(e)}')
    
    return issues

def main():
    """主函数"""
    website_dir = '.'
    problem_files = []
    
    print("查找 bespoke-bags.com 网站中有SEO问题的文件...")
    print("=" * 50)
    
    # 遍历所有HTML文件
    for root, dirs, files in os.walk(website_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                issues = check_seo_issues(file_path)
                
                if issues:
                    problem_files.append((file_path, issues))
    
    # 输出有问题的文件
    if problem_files:
        print(f"\n发现 {len(problem_files)} 个文件存在SEO问题:\n")
        for file_path, issues in problem_files:
            print(f"文件: {file_path}")
            print(f"问题: {', '.join(issues)}")
            print("-" * 50)
    else:
        print("\n🎉 所有文件的SEO都已优化完成！")

if __name__ == '__main__':
    main()