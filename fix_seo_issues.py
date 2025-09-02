#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SEO问题修复脚本 - 批量修复网站SEO问题
"""

import os
import re
from bs4 import BeautifulSoup
import json

class SEOFixer:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.fixed_files = []
        self.stats = {
            'total_files': 0,
            'fixed_files': 0,
            'fixes_applied': 0,
            'fix_types': {}
        }
    
    def fix_file(self, file_path):
        """修复单个HTML文件的SEO问题"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            relative_path = os.path.relpath(file_path, self.root_dir)
            fixes_applied = []
            modified = False
            
            # 获取基本信息
            title_tag = soup.find('title')
            title_text = title_tag.get_text().strip() if title_tag else ''
            
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            desc_text = meta_desc.get('content', '').strip() if meta_desc else ''
            
            # 生成页面URL
            if relative_path == 'index.html':
                page_url = 'https://bespoke-bags.com/'
            elif relative_path.startswith('blog/'):
                page_name = os.path.splitext(os.path.basename(relative_path))[0]
                page_url = f'https://bespoke-bags.com/blog/{page_name}.html'
            else:
                page_name = os.path.splitext(relative_path)[0]
                page_url = f'https://bespoke-bags.com/{page_name}.html'
            
            # 生成图片URL
            image_url = 'https://bespoke-bags.com/images/bespoke-bags (1).webp'
            
            # 获取head标签
            head = soup.find('head')
            
            # 修复缺少的canonical链接
            canonical = soup.find('link', attrs={'rel': 'canonical'})
            if not canonical and head:
                canonical_tag = soup.new_tag('link')
                canonical_tag['rel'] = 'canonical'
                canonical_tag['href'] = page_url
                head.append(canonical_tag)
                fixes_applied.append('添加canonical链接')
                modified = True
            
            # 修复缺少的OG标签
            if head:
                og_tags = {
                    'og:title': title_text,
                    'og:description': desc_text,
                    'og:image': image_url,
                    'og:url': page_url,
                    'og:type': 'website',
                    'og:site_name': 'Bespoke Bags'
                }
                
                for property_name, content in og_tags.items():
                    existing_tag = soup.find('meta', attrs={'property': property_name})
                    if not existing_tag and content:
                        og_tag = soup.new_tag('meta')
                        og_tag['property'] = property_name
                        og_tag['content'] = content
                        head.append(og_tag)
                        fixes_applied.append(f'添加{property_name}')
                        modified = True
            
            # 修复缺少的Twitter卡片
            if head:
                twitter_tags = {
                    'twitter:card': 'summary_large_image',
                    'twitter:title': title_text,
                    'twitter:description': desc_text,
                    'twitter:image': image_url,
                    'twitter:site': '@bespokebags'
                }
                
                for tag_name, content in twitter_tags.items():
                    existing_tag = soup.find('meta', attrs={'name': tag_name})
                    if not existing_tag and content:
                        twitter_tag = soup.new_tag('meta')
                        twitter_tag['name'] = tag_name
                        twitter_tag['content'] = content
                        head.append(twitter_tag)
                        fixes_applied.append(f'添加{tag_name}')
                        modified = True
            
            # 修复缺少的Schema.org JSON-LD标记
            json_ld = soup.find('script', attrs={'type': 'application/ld+json'})
            if not json_ld and head:
                schema_data = {
                    "@context": "https://schema.org",
                    "@type": "WebPage",
                    "name": title_text,
                    "description": desc_text,
                    "url": page_url,
                    "image": image_url,
                    "publisher": {
                        "@type": "Organization",
                        "name": "Bespoke Bags",
                        "url": "https://bespoke-bags.com"
                    }
                }
                
                script_tag = soup.new_tag('script', type='application/ld+json')
                script_tag.string = json.dumps(schema_data, ensure_ascii=False, indent=2)
                head.append(script_tag)
                fixes_applied.append('添加Schema.org JSON-LD标记')
                modified = True
            
            # 保存修改后的文件
            if modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(str(soup))
                
                self.fixed_files.append({
                    'file': relative_path,
                    'fixes': fixes_applied
                })
                self.stats['fixed_files'] += 1
                self.stats['fixes_applied'] += len(fixes_applied)
                
                for fix in fixes_applied:
                    fix_type = fix.split('(')[0] if '(' in fix else fix
                    self.stats['fix_types'][fix_type] = self.stats['fix_types'].get(fix_type, 0) + 1
            
            self.stats['total_files'] += 1
            
        except Exception as e:
            print(f"修复文件 {file_path} 时出错: {e}")
    
    def scan_and_fix_directory(self):
        """扫描并修复目录中的所有HTML文件"""
        for root, dirs, files in os.walk(self.root_dir):
            for file in files:
                if file.endswith('.html'):
                    file_path = os.path.join(root, file)
                    self.fix_file(file_path)
    
    def generate_report(self):
        """生成修复报告"""
        print("\n=== SEO修复报告 ===")
        print(f"总文件数: {self.stats['total_files']}")
        print(f"修复的文件数: {self.stats['fixed_files']}")
        print(f"总修复数: {self.stats['fixes_applied']}")
        
        print("\n=== 修复类型统计 ===")
        for fix_type, count in sorted(self.stats['fix_types'].items(), key=lambda x: x[1], reverse=True):
            print(f"{fix_type}: {count}次")
        
        print("\n=== 修复详情 ===")
        for item in self.fixed_files[:10]:  # 只显示前10个文件的修复
            print(f"\n文件: {item['file']}")
            for fix in item['fixes']:
                print(f"  - {fix}")
        
        if len(self.fixed_files) > 10:
            print(f"\n... 还有 {len(self.fixed_files) - 10} 个文件被修复")

def main():
    root_dir = os.getcwd()
    fixer = SEOFixer(root_dir)
    
    print("开始SEO修复...")
    fixer.scan_and_fix_directory()
    fixer.generate_report()
    
    print("\nSEO修复完成！")

if __name__ == '__main__':
    main()