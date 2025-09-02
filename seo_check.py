#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SEO检查脚本 - 分析网站SEO问题
"""

import os
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json

class SEOChecker:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.issues = []
        self.stats = {
            'total_files': 0,
            'files_with_issues': 0,
            'total_issues': 0,
            'issue_types': {}
        }
    
    def check_file(self, file_path):
        """检查单个HTML文件的SEO问题"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            relative_path = os.path.relpath(file_path, self.root_dir)
            file_issues = []
            
            # 检查标题
            title = soup.find('title')
            if not title:
                file_issues.append('缺少title标签')
            elif len(title.get_text().strip()) == 0:
                file_issues.append('title标签为空')
            elif len(title.get_text().strip()) > 60:
                file_issues.append(f'title过长({len(title.get_text().strip())}字符)')
            elif len(title.get_text().strip()) < 30:
                file_issues.append(f'title过短({len(title.get_text().strip())}字符)')
            
            # 检查meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if not meta_desc:
                file_issues.append('缺少meta description')
            elif not meta_desc.get('content') or len(meta_desc.get('content', '').strip()) == 0:
                file_issues.append('meta description为空')
            elif len(meta_desc.get('content', '').strip()) > 160:
                file_issues.append(f'meta description过长({len(meta_desc.get("content", "").strip())}字符)')
            elif len(meta_desc.get('content', '').strip()) < 120:
                file_issues.append(f'meta description过短({len(meta_desc.get("content", "").strip())}字符)')
            
            # 检查H1标签
            h1_tags = soup.find_all('h1')
            if len(h1_tags) == 0:
                file_issues.append('缺少H1标签')
            elif len(h1_tags) > 1:
                file_issues.append(f'H1标签过多({len(h1_tags)}个)')
            
            # 检查标题层级
            headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            prev_level = 0
            for heading in headings:
                level = int(heading.name[1])
                if level > prev_level + 1:
                    file_issues.append(f'标题层级跳跃: {heading.name}跳过了h{prev_level + 1}')
                prev_level = level
            
            # 检查图片alt属性
            images = soup.find_all('img')
            for img in images:
                if not img.get('alt'):
                    file_issues.append('图片缺少alt属性')
                elif len(img.get('alt', '').strip()) == 0:
                    file_issues.append('图片alt属性为空')
            
            # 检查内部链接
            links = soup.find_all('a', href=True)
            for link in links:
                href = link.get('href')
                if href.startswith('/') or href.startswith('./'):
                    # 检查内部链接是否存在
                    if href.startswith('/'):
                        target_path = os.path.join(self.root_dir, href.lstrip('/'))
                    else:
                        target_path = os.path.join(os.path.dirname(file_path), href)
                    
                    if not os.path.exists(target_path) and not os.path.exists(target_path + '.html'):
                        file_issues.append(f'内部链接404: {href}')
            
            # 检查canonical链接
            canonical = soup.find('link', attrs={'rel': 'canonical'})
            if not canonical:
                file_issues.append('缺少canonical链接')
            elif not canonical.get('href'):
                file_issues.append('canonical链接为空')
            
            # 检查OG标签
            og_title = soup.find('meta', attrs={'property': 'og:title'})
            og_desc = soup.find('meta', attrs={'property': 'og:description'})
            og_image = soup.find('meta', attrs={'property': 'og:image'})
            og_url = soup.find('meta', attrs={'property': 'og:url'})
            
            if not og_title:
                file_issues.append('缺少og:title')
            if not og_desc:
                file_issues.append('缺少og:description')
            if not og_image:
                file_issues.append('缺少og:image')
            if not og_url:
                file_issues.append('缺少og:url')
            
            # 检查Twitter卡片
            twitter_card = soup.find('meta', attrs={'name': 'twitter:card'})
            twitter_title = soup.find('meta', attrs={'name': 'twitter:title'})
            twitter_desc = soup.find('meta', attrs={'name': 'twitter:description'})
            twitter_image = soup.find('meta', attrs={'name': 'twitter:image'})
            
            if not twitter_card:
                file_issues.append('缺少twitter:card')
            if not twitter_title:
                file_issues.append('缺少twitter:title')
            if not twitter_desc:
                file_issues.append('缺少twitter:description')
            if not twitter_image:
                file_issues.append('缺少twitter:image')
            
            # 检查Schema.org标记
            json_ld = soup.find('script', attrs={'type': 'application/ld+json'})
            if not json_ld:
                file_issues.append('缺少Schema.org JSON-LD标记')
            
            if file_issues:
                self.issues.append({
                    'file': relative_path,
                    'issues': file_issues
                })
                self.stats['files_with_issues'] += 1
                self.stats['total_issues'] += len(file_issues)
                
                for issue in file_issues:
                    issue_type = issue.split(':')[0] if ':' in issue else issue
                    self.stats['issue_types'][issue_type] = self.stats['issue_types'].get(issue_type, 0) + 1
            
            self.stats['total_files'] += 1
            
        except Exception as e:
            print(f"检查文件 {file_path} 时出错: {e}")
    
    def scan_directory(self):
        """扫描目录中的所有HTML文件"""
        for root, dirs, files in os.walk(self.root_dir):
            for file in files:
                if file.endswith('.html'):
                    file_path = os.path.join(root, file)
                    self.check_file(file_path)
    
    def generate_report(self):
        """生成SEO检查报告"""
        print("\n=== SEO检查报告 ===")
        print(f"总文件数: {self.stats['total_files']}")
        print(f"有问题的文件数: {self.stats['files_with_issues']}")
        print(f"总问题数: {self.stats['total_issues']}")
        
        if self.stats['total_files'] > 0:
            pass_rate = ((self.stats['total_files'] - self.stats['files_with_issues']) / self.stats['total_files']) * 100
            print(f"通过率: {pass_rate:.1f}%")
        
        print("\n=== 问题类型统计 ===")
        for issue_type, count in sorted(self.stats['issue_types'].items(), key=lambda x: x[1], reverse=True):
            print(f"{issue_type}: {count}个")
        
        print("\n=== 详细问题列表 ===")
        for item in self.issues[:20]:  # 只显示前20个文件的问题
            print(f"\n文件: {item['file']}")
            for issue in item['issues']:
                print(f"  - {issue}")
        
        if len(self.issues) > 20:
            print(f"\n... 还有 {len(self.issues) - 20} 个文件存在问题")

def main():
    root_dir = os.getcwd()
    checker = SEOChecker(root_dir)
    
    print("开始SEO检查...")
    checker.scan_directory()
    checker.generate_report()
    
    # 保存详细报告到文件
    with open('seo_report.json', 'w', encoding='utf-8') as f:
        json.dump({
            'stats': checker.stats,
            'issues': checker.issues
        }, f, ensure_ascii=False, indent=2)
    
    print("\n详细报告已保存到 seo_report.json")

if __name__ == '__main__':
    main()